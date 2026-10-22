"""Notey's version 1 Docker/PostgreSQL adapter for the shared Lara controller.

Install from a reviewed merged revision beside backup_archive.py. It accepts
only phase names; credentials stay in owner-only host files and never in argv.
The shared controller serializes calls and owns recovery markers.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

import backup_archive


class NoteyAdapter:
    """Operate only the dedicated Notey project, preserving shared services."""

    def __init__(self, config, run=subprocess.run):
        self.config = config
        self.run = run
        if config["app"] != "notey" or config["project"] != "notey":
            raise ValueError("Adapter is restricted to the Notey Compose project")
        env_file = Path(config["runtime_env"])
        if env_file.is_symlink() or not env_file.is_file() or env_file.stat().st_mode & 0o077:
            raise ValueError("Runtime environment must be a private regular file")

    def command(self, arguments, environment=None, output=None):
        """Capture tool diagnostics privately; never print interpolated credentials."""
        result = self.run(arguments, env=environment, stdout=output or subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=600)
        if result.returncode:
            raise RuntimeError("Notey operation failed")
        return result.stdout

    def compose(self, release, arguments, output=None):
        """Select the exact recorded recipe/image without rewriting runtime secrets."""
        environment = dict(os.environ, NOTEY_IMAGE=self.image_reference(release),
                           NOTEY_REVISION=release["revision"],
                           NOTEY_PROXY_NETWORK=self.config["proxy_network"])
        command = ["docker", "compose", "--project-name", "notey", "--env-file",
                   self.config["runtime_env"], "-f", release["compose"], *arguments]
        return self.command(command, environment, output)

    def image_reference(self, release):
        """Resolve classic/config versus containerd/manifest IDs without trusting tags.

        Docker's two image stores can identify the same saved image differently.
        Only accept an OCI manifest whose verified config digest is the exact CI
        image ID, within the already checksum-verified single-image package.
        """
        try:
            self.command(["docker", "image", "inspect", release["image_id"]])
            return release["image_id"]
        except RuntimeError:
            if "directory" not in release:
                raise
        with tarfile.open(Path(release["directory"]) / "image.tar.gz", "r:gz") as archive:
            index = json.load(archive.extractfile("index.json"))
            if len(index["manifests"]) != 1:
                raise ValueError("Expected a single-platform image")
            identifier = index["manifests"][0]["digest"]
            if not re.fullmatch(r"sha256:[0-9a-f]{64}", identifier):
                raise ValueError("Invalid OCI manifest identity")
            payload = archive.extractfile("blobs/sha256/" + identifier[7:]).read(1024 * 1024 + 1)
            if len(payload) > 1024 * 1024 or "sha256:" + hashlib.sha256(payload).hexdigest() != identifier:
                raise ValueError("OCI manifest identity mismatch")
            manifest = json.loads(payload)
            if manifest["config"]["digest"] != release["image_id"]:
                raise ValueError("OCI image does not identify the tested configuration")
            config = archive.extractfile("blobs/sha256/" + release["image_id"][7:]).read(1024 * 1024 + 1)
            if "sha256:" + hashlib.sha256(config).hexdigest() != release["image_id"]:
                raise ValueError("OCI configuration identity mismatch")
        self.command(["docker", "image", "inspect", identifier])
        return identifier

    def verify(self, current, candidate):
        """Import the checked image and reject recipe changes outside N02's scope."""
        self.command(["docker", "load", "--input", str(Path(candidate["directory"]) / "image.tar.gz")])
        reference = self.image_reference(candidate)
        image = json.loads(self.command(["docker", "image", "inspect", reference]))[0]
        if (image["Id"] != reference or image["Architecture"] != "amd64"
                or image["Os"] != "linux"
                or image["Config"]["Labels"].get("org.opencontainers.image.revision") != candidate["revision"]):
            raise ValueError("Wrong release image identity/platform/source")
        old = json.loads(self.compose(current, ["config", "--format", "json"]))
        new = json.loads(self.compose(candidate, ["config", "--format", "json"]))
        if (set(new["services"]) != {"web", "db"}
                or new["services"]["db"]["image"] != old["services"]["db"]["image"]
                or new["services"]["db"].get("volumes") != old["services"]["db"].get("volumes")
                or new["services"]["web"].get("volumes")
                or new["services"]["web"]["image"] != reference):
            raise ValueError("Recipe changes need a separate deployment review")
        for service in new["services"].values():
            if (service.get("ports") or service.get("privileged") or service.get("cap_add")
                    or service.get("network_mode") or service.get("build")):
                raise ValueError("Host publication/privilege/build is not allowed")
        self.command(["docker", "network", "inspect", self.config["proxy_network"]])

    def snapshot(self, current, destination):
        """Take a real consistent PostgreSQL dump and apply Notey's manifest format."""
        with tempfile.TemporaryDirectory(dir=Path(destination).parent) as temporary:
            dump = Path(temporary) / "database.dump"
            with dump.open("xb") as output:
                dump.chmod(0o600)
                self.compose(current, ["exec", "-T", "db", "pg_dump", "-U", "notey", "-d", "notey",
                                       "--format=custom", "--no-owner", "--no-acl"], output)
            backup_archive.create(destination, dump, current["revision"], current["image_id"])

    def phase(self, name, current, candidate=None):
        """Implement the controller phases; backup alone returns a public receipt."""
        if name == "verify":
            self.verify(current, candidate)
        elif name == "pause":
            self.compose(current, ["stop", "web"])
        elif name == "backup":
            # The installed mechanism directory is explicitly pinned by bootstrap.
            from backup import encrypted_backup
            from drive import DriveStore
            settings = self.config["backup"]
            return encrypted_backup(lambda path: self.snapshot(current, path), "notey", current,
                                    settings, DriveStore(settings["credential_file"]))
        elif name == "migrate":
            self.compose(candidate, ["run", "--rm", "--no-deps", "--pull", "never", "web", "/app/bin/migrate"])
        elif name in ("activate", "resume"):
            release = candidate if name == "activate" else current
            self.compose(release, ["up", "-d", "--no-deps", "--pull", "never", "--wait", "--wait-timeout", "120", "web"])
        elif name == "stop":
            self.compose(candidate, ["stop", "web"])
        elif name == "health":
            self.health()
        else:
            raise ValueError("Unknown adapter phase")

    def health(self):
        """Check the configured private HTTPS endpoint with certificate verification."""
        if not self.config["health_url"].startswith("https://"):
            raise ValueError("Production readiness requires HTTPS")
        with urllib.request.urlopen(self.config["health_url"], timeout=20) as response:
            if response.status != 200 or json.load(response) != {"status": "ok"}:
                raise RuntimeError("Notey HTTPS readiness failed")


def main():
    """Load private host configuration and dispatch one trusted controller phase."""
    try:
        config_path = Path(os.environ["LARA_DELIVERY_CONFIG"])
        if config_path.is_symlink() or config_path.stat().st_mode & 0o077:
            raise ValueError("Controller configuration must be private")
        config = json.loads(config_path.read_text())
        sys.path.insert(0, config["mechanism_dir"])
        current = json.loads(os.environ["LARA_DELIVERY_CURRENT"])
        candidate = json.loads(os.environ["LARA_DELIVERY_CANDIDATE"])
        result = NoteyAdapter(config).phase(sys.argv[1], current, candidate)
        if result is not None:
            print(json.dumps(result))
        return 0
    except Exception:
        # Docker/HTTP exceptions can embed interpolated secrets. Keep them off logs.
        print("Notey adapter failed; inspect its private configuration and controller stage", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
