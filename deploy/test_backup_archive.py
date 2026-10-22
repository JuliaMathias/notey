"""Deterministic format tests using synthetic data, with no remote services."""

import io
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

import backup_archive


class BackupArchiveTest(unittest.TestCase):
    """Exercise portable recovery contents and rejection of damaged archives."""

    def setUp(self):
        """Prepare a synthetic dump and file outside the repository."""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.dump = self.root / "dump"
        self.dump.write_bytes(b"synthetic pg_dump fixture")
        self.note = self.root / "note"
        self.note.write_text("synthetic source fixture\n")
        self.archive = self.root / "backup.tar"

    def create(self):
        """Call the production packager with explicit synthetic inputs."""
        return backup_archive.create(self.archive, self.dump, "a" * 40,
                                     "sha256:" + "b" * 64,
                                     {"session/source.txt": self.note})

    def test_round_trip_preserves_dump_files_and_release_identity(self):
        """Recovery preserves bytes and identifies the matching app revision."""
        manifest = self.create()
        restored = self.root / "restored"
        self.assertEqual(backup_archive.unpack(self.archive, restored), manifest)
        self.assertEqual((restored / "database.dump").read_bytes(), self.dump.read_bytes())
        self.assertEqual((restored / "files/session/source.txt").read_bytes(), self.note.read_bytes())
        self.assertEqual(manifest["revision"], "a" * 40)
        self.assertEqual(self.archive.stat().st_mode & 0o777, 0o600)
        self.assertEqual(restored.stat().st_mode & 0o777, 0o700)

    def test_existing_backup_and_restore_directory_are_preserved(self):
        """Re-running recovery cannot overwrite existing backup/runtime data."""
        self.create()
        original = self.archive.read_bytes()
        with self.assertRaises(FileExistsError):
            self.create()
        self.assertEqual(self.archive.read_bytes(), original)
        with self.assertRaises(FileExistsError):
            backup_archive.unpack(self.archive, self.root)

    def test_operator_cli_verifies_before_unpacking_and_refuses_overwrite(self):
        """The runbook's actual command restores bytes once and preserves them."""
        self.create()
        command = [sys.executable, backup_archive.__file__, "unpack", str(self.archive),
                   str(self.root / "cli-restore")]
        subprocess.run(command, capture_output=True, check=True)
        restored = self.root / "cli-restore/database.dump"
        self.assertEqual(restored.read_bytes(), self.dump.read_bytes())
        self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertEqual(restored.read_bytes(), self.dump.read_bytes())

    def test_changed_dump_is_rejected_before_restore_directory_is_created(self):
        """A damaged member must fail integrity checks before writing files."""
        self.create()
        content = self.archive.read_bytes().replace(b"synthetic pg_dump", b"corrupted pg_dump")
        self.archive.write_bytes(content)
        with self.assertRaises(ValueError):
            backup_archive.unpack(self.archive, self.root / "restored")
        self.assertFalse((self.root / "restored").exists())

    def test_traversal_and_noncanonical_file_paths_are_rejected(self):
        """No caller-supplied file can escape the restore directory."""
        for name in (".", "../secret", "/secret", "a/../../secret", "a//b", "a/./b", "a\\b"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                backup_archive.safe_name(name)

    def test_symlink_input_is_rejected(self):
        """Do not follow backup inputs into unintended directories."""
        link = self.root / "link"
        link.symlink_to(self.dump)
        with self.assertRaises(ValueError):
            backup_archive.create(self.archive, link, "a" * 40, "sha256:" + "b" * 64)

    def test_extra_duplicate_and_link_members_are_rejected(self):
        """Reject contents absent from the manifest, duplicates and links."""
        self.create()
        original = self.archive.read_bytes()
        for kind in ("extra", "duplicate", "link", "traversal"):
            self.archive.write_bytes(original)
            with tarfile.open(self.archive, "a") as archive:
                name = {"extra": "extra", "duplicate": "database.dump",
                        "link": "link", "traversal": "../outside"}[kind]
                info = tarfile.TarInfo(name)
                if kind == "link":
                    info.type = tarfile.SYMTYPE
                    info.linkname = "/outside"
                archive.addfile(info, io.BytesIO())
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                backup_archive.verify(self.archive)


if __name__ == "__main__":
    unittest.main()
