"""Notey backup format and integrity checks, independent of storage/encryption.

The caller supplies a completed PostgreSQL custom-format dump. File support is
exercised with synthetic fixtures in N02; integrating real assets belongs to #21.
Archives contain no credentials or recovery keys. Encrypt before off-host upload.
"""

import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import tarfile


def checksum(path):
    """Return a file's SHA-256 without loading the entire file into memory."""
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def safe_name(name):
    """Require a canonical relative archive path without traversal components."""
    path = PurePosixPath(name)
    if (not name or name == "." or path.is_absolute() or str(path) != name
            or any(part in (".", "..") for part in path.parts)
            or "\\" in name or "\x00" in name):
        raise ValueError("Unsafe backup member name")
    return name


def create(destination, dump, revision, image, files=None):
    """Create a new archive containing a dump, explicit files and their manifest.

    Refuse overwrites and symlinks. Callers must quiesce any writers to files while
    taking a recovery point; PostgreSQL's pg_dump supplies its own DB snapshot.
    """
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("A full source revision is required")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", image):
        raise ValueError("A Docker image ID is required")
    sources = {"database.dump": Path(dump)}
    for name, source in (files or {}).items():
        sources["files/" + safe_name(name)] = Path(source)
    entries = []
    for name, source in sources.items():
        if source.is_symlink() or not source.is_file():
            raise ValueError("Only regular backup input files are supported")
        entries.append({"path": name, "size": source.stat().st_size,
                        "sha256": checksum(source)})
    manifest = {"format": 1, "application": "notey", "revision": revision,
                "image": image, "postgres_major": 17, "entries": entries}
    payload = json.dumps(manifest, sort_keys=True).encode()
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as output, tarfile.open(fileobj=output, mode="w") as archive:
        info = tarfile.TarInfo("manifest.json")
        info.size = len(payload)
        info.mode = 0o600
        archive.addfile(info, io.BytesIO(payload))
        for name, source in sources.items():
            info = tarfile.TarInfo(name)
            info.size = source.stat().st_size
            info.mode = 0o600
            with source.open("rb") as stream:
                archive.addfile(info, stream)
    # Catch changed input and malformed output before encryption/upload.
    verify(destination)
    return manifest


def verify(path):
    """Validate all members and bytes before allowing any recovery operation."""
    with tarfile.open(path, "r:") as archive:
        members = archive.getmembers()
        names = [safe_name(member.name) for member in members]
        if len(set(names)) != len(names) or any(not m.isfile() for m in members):
            raise ValueError("Backup contains duplicate or non-file members")
        if "manifest.json" not in names:
            raise ValueError("Missing backup manifest")
        info = archive.getmember("manifest.json")
        if info.size > 1024 * 1024:
            raise ValueError("Backup manifest exceeds its size limit")
        manifest = json.load(archive.extractfile(info))
        if (manifest.get("format") != 1 or manifest.get("application") != "notey"
                or manifest.get("postgres_major") != 17
                or not re.fullmatch(r"[0-9a-f]{40}", manifest.get("revision", ""))
                or not re.fullmatch(r"sha256:[0-9a-f]{64}", manifest.get("image", ""))):
            raise ValueError("Unsupported backup manifest")
        entries = manifest["entries"]
        paths = [safe_name(entry["path"]) for entry in entries]
        if (len(paths) != len(set(paths)) or "database.dump" not in paths
                or set(names) != {"manifest.json", *paths}
                or any(p != "database.dump" and not p.startswith("files/") for p in paths)):
            raise ValueError("Backup members do not match the manifest")
        for entry in entries:
            member = archive.getmember(entry["path"])
            with archive.extractfile(member) as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            if member.size != entry["size"] or digest != entry["sha256"]:
                raise ValueError("Backup checksum or size mismatch")
    return manifest


def unpack(path, destination):
    """Copy verified contents to a new directory; never overwrite runtime data."""
    manifest = verify(path)
    destination = Path(destination)
    destination.mkdir(mode=0o700, parents=False, exist_ok=False)
    with tarfile.open(path, "r:") as archive:
        for member in archive.getmembers():
            target = destination / member.name
            target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            with archive.extractfile(member) as source, target.open("xb") as output:
                target.chmod(0o600)
                while chunk := source.read(1024 * 1024):
                    output.write(chunk)
    return manifest
