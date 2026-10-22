"""Opt-in real PostgreSQL recovery check; never targets a runtime database.

Run with NOTEY_BACKUP_TEST_CONTAINER=notey-dev-db-1. The existing local service
must allow local-socket access as its synthetic `notey` role. Two randomly named
databases are created and cleaned up; ordinary tests do not need Docker.
"""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import uuid

import backup_archive


@unittest.skipUnless(os.environ.get("NOTEY_BACKUP_TEST_CONTAINER"), "opt-in local PostgreSQL check")
class PostgresRecoveryTest(unittest.TestCase):
    """Verify a real dump recovers data lost through an incompatible migration."""

    def command(self, *args, data=None, check=True):
        """Run a DB utility only inside the explicitly selected local container."""
        return subprocess.run(["docker", "exec", "-i", self.container, *args],
                              input=data, capture_output=True, check=check)

    def test_recover_database_after_destructive_schema_change(self):
        """Image rollback alone cannot recover a dropped column; dump restore can."""
        self.container = os.environ["NOTEY_BACKUP_TEST_CONTAINER"]
        source = "n02_source_" + uuid.uuid4().hex
        restored = "n02_restore_" + uuid.uuid4().hex
        try:
            for database in (source, restored):
                self.command("createdb", "-U", "notey", database)
            self.command("psql", "-X", "-U", "notey", "-d", source,
                         "-v", "ON_ERROR_STOP=1", "-c",
                         "CREATE TABLE recovery_probe (id uuid PRIMARY KEY, note text); "
                         "INSERT INTO recovery_probe VALUES "
                         "('00000000-0000-0000-0000-000000000022', 'N02 synthetic recovery');")
            dump = self.command("pg_dump", "-U", "notey", "-d", source,
                                "--format=custom", "--no-owner", "--no-acl").stdout
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "database.dump").write_bytes(dump)
                (root / "source.txt").write_text("N02 synthetic file contract\n")
                archive = root / "backup.tar"
                backup_archive.create(archive, root / "database.dump", "a" * 40,
                                      "sha256:" + "b" * 64,
                                      {"source.txt": root / "source.txt"})
                self.command("psql", "-X", "-U", "notey", "-d", source,
                             "-v", "ON_ERROR_STOP=1", "-c",
                             "ALTER TABLE recovery_probe DROP COLUMN note;")
                old_query = self.command("psql", "-X", "-U", "notey", "-d", source,
                                         "-c", "SELECT note FROM recovery_probe;", check=False)
                self.assertNotEqual(old_query.returncode, 0)
                backup_archive.unpack(archive, root / "verified")
                self.command("pg_restore", "-U", "notey", "-d", restored,
                             "--exit-on-error", "--single-transaction", "--no-owner", "--no-acl",
                             data=(root / "verified/database.dump").read_bytes())
                actual = self.command("psql", "-X", "-U", "notey", "-d", restored,
                                      "-At", "-c", "SELECT id, note FROM recovery_probe;").stdout
                self.assertEqual(actual.strip(),
                                 b"00000000-0000-0000-0000-000000000022|N02 synthetic recovery")
                self.assertEqual((root / "verified/files/source.txt").read_text(),
                                 "N02 synthetic file contract\n")
        finally:
            for database in (source, restored):
                self.command("dropdb", "-U", "notey", "--if-exists", database)


if __name__ == "__main__":
    unittest.main()
