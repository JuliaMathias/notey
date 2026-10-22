"""Notey adapter behavior checks using fake Docker commands and synthetic data."""
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import tarfile
import unittest

from delivery_adapter import NoteyAdapter


class AdapterTest(unittest.TestCase):
    """Constrain operations to Notey and preserve existing database configuration."""

    def setUp(self):
        """Prepare private synthetic config and observable fake command results."""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = self.root / "runtime.env"
        self.env.write_text("SYNTHETIC=not-a-secret\n")
        self.env.chmod(0o600)
        self.config = {"app": "notey", "project": "notey", "runtime_env": str(self.env),
                       "proxy_network": "lara-proxy"}
        self.current = {"app": "notey", "revision": "a"*40, "image_id": "sha256:"+"a"*64,
                        "compose": "old-compose.yaml"}
        self.candidate = {"app": "notey", "revision": "b"*40, "image_id": "sha256:"+"b"*64,
                          "compose": "new-compose.yaml", "directory": "/synthetic/release"}
        self.calls = []
        self.old = {"services": {"db": {"image": "postgres-pinned", "volumes": ["same-volume"]},
                                 "web": {"image": self.current["image_id"]}}}
        self.new = deepcopy(self.old)
        self.new["services"]["web"]["image"] = self.candidate["image_id"]
        self.adapter = NoteyAdapter(self.config, self.command)

    def command(self, args, **kwargs):
        """Serve image/recipe metadata and dump bytes without running Docker."""
        self.calls.append((args, kwargs))
        output = b""
        if args[:3] == ["docker", "image", "inspect"]:
            output = json.dumps([{"Id": self.candidate["image_id"], "Architecture": "amd64", "Os": "linux",
                                  "Config": {"Labels": {"org.opencontainers.image.revision": "b"*40}}}]).encode()
        elif args[-3:] == ["config", "--format", "json"]:
            output = json.dumps(self.old if "old-compose.yaml" in args else self.new).encode()
        elif "pg_dump" in args:
            kwargs["stdout"].write(b"synthetic custom-format dump")
        return subprocess.CompletedProcess(args, 0, output, b"")

    def test_verified_image_and_recipe_require_no_build_or_remote_dependency_pull(self):
        """Import only the expected image and inspect existing database identity."""
        self.adapter.verify(self.current, self.candidate)
        self.assertTrue(any(args[:2] == ["docker", "load"] for args, _ in self.calls))
        self.assertFalse(any("build" in args or "pull" in args for args, _ in self.calls))

    def test_database_replacement_and_published_ports_are_rejected(self):
        """Major DB/storage/host changes cannot be incidental application updates."""
        for kind in ("image", "volumes", "ports"):
            self.new = deepcopy(self.old)
            self.new["services"]["web"]["image"] = self.candidate["image_id"]
            self.new["services"]["db"][kind] = "changed" if kind == "image" else ["changed"]
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.adapter.verify(self.current, self.candidate)

    def test_migration_activation_and_pause_are_scoped_to_notey(self):
        """Use exact image IDs, no-pull activation and no unrelated services."""
        for phase in ("pause", "migrate", "activate", "stop", "resume"):
            self.adapter.phase(phase, self.current, self.candidate)
        for args, kwargs in self.calls:
            if args[:3] == ["docker", "image", "inspect"]:
                continue
            self.assertIn("notey", args)
            self.assertNotIn("down", args)
            self.assertNotIn("build", args)
            self.assertIn(kwargs["env"]["NOTEY_IMAGE"], (self.current["image_id"], self.candidate["image_id"]))
        self.assertTrue(any("never" in args for args, _ in self.calls))

    def test_snapshot_calls_real_packager_and_keeps_release_identity(self):
        """The adapter supplies dump bytes to the production archive contract."""
        from backup_archive import unpack
        archive = self.root / "snapshot.tar"
        self.adapter.snapshot(self.current, archive)
        manifest = unpack(archive, self.root / "restored")
        self.assertEqual(manifest["revision"], self.current["revision"])
        self.assertEqual((self.root / "restored/database.dump").read_bytes(), b"synthetic custom-format dump")
        self.assertFalse(any("migrate" in args for args, _ in self.calls))

    def test_containerd_manifest_is_bound_to_the_exact_ci_config_digest(self):
        """Different Docker stores must resolve the same cryptographically bound image."""
        config = b'{"synthetic":"image config"}'
        config_id = "sha256:" + hashlib.sha256(config).hexdigest()
        manifest = json.dumps({"config": {"digest": config_id}}).encode()
        manifest_id = "sha256:" + hashlib.sha256(manifest).hexdigest()
        release = dict(self.candidate, image_id=config_id, directory=str(self.root))
        def write_archive(config_bytes):
            entries = {"index.json": json.dumps({"manifests": [{"digest": manifest_id}]}).encode(),
                       "blobs/sha256/" + manifest_id[7:]: manifest,
                       "blobs/sha256/" + config_id[7:]: config_bytes}
            with tarfile.open(self.root / "image.tar.gz", "w:gz") as archive:
                for name, payload in entries.items():
                    member = tarfile.TarInfo(name); member.size = len(payload)
                    archive.addfile(member, io.BytesIO(payload))
        def inspect(args, **kwargs):
            return subprocess.CompletedProcess(args, 1 if args[-1] == config_id else 0, b"", b"")
        adapter = NoteyAdapter(self.config, inspect)
        write_archive(config)
        self.assertEqual(adapter.image_reference(release), manifest_id)
        write_archive(b"corrupt image config")
        with self.assertRaises(ValueError):
            adapter.image_reference(release)
