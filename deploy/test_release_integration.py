"""Opt-in actual image updates on isolated, disposable local Docker projects.

Requires NOTEY_RELEASE_TEST_PACKAGE (downloaded CI release-package),
NOTEY_MECHANISM_TEST_DIR (reviewed installed shared runtime), and the existing
local notey:foundation-review image. No production project or account is used.
"""
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import unittest

from delivery_adapter import NoteyAdapter
import backup_archive


@unittest.skipUnless(os.environ.get("NOTEY_RELEASE_TEST_PACKAGE") and
                     os.environ.get("NOTEY_MECHANISM_TEST_DIR"), "opt-in local release integration")
class ReleaseIntegrationTest(unittest.TestCase):
    """Exercise real app/DB updates; fake only storage and injected health failure."""

    def exercise(self, fail_health):
        """Use a random synthetic project and clean only its named resources."""
        sys.path.insert(0, os.environ["NOTEY_MECHANISM_TEST_DIR"])
        from common import DeliveryError, save_json
        from runtime import Runner, app_lock
        package = Path(os.environ["NOTEY_RELEASE_TEST_PACKAGE"]).resolve()
        manifest = json.loads((package / "release.json").read_text())
        project = "notey-n02-test-" + secrets.token_hex(6)
        network = project + "-proxy"
        with tempfile.TemporaryDirectory(prefix=project) as temporary:
            root = Path(temporary)
            env = root / "runtime.env"
            env.write_text("NOTEY_DB_PASSWORD=" + secrets.token_hex(32) + "\nSECRET_KEY_BASE=" +
                           secrets.token_hex(64) + "\nRELEASE_COOKIE=" + secrets.token_hex(32) +
                           "\nPHX_HOST=localhost\n")
            env.chmod(0o600)
            config = {"app": "notey", "project": "notey", "runtime_env": str(env),
                      "proxy_network": network}
            override = root / "emulation.yaml"
            # OTP documents single-mapped JIT for amd64 emulation on Apple ARM.
            # This test-only override never changes the published recipe or Lara.
            override.write_text('services:\n  web:\n    environment:\n      ERL_FLAGS: "+S 2:2 +JMsingle true"\n')
            def command(args, **kwargs):
                # Test-only transport redirects every real Docker Compose command
                # into a random project. Production adapter restrictions stay intact.
                args = list(args)
                if "--project-name" in args:
                    args[args.index("--project-name") + 1] = project
                    position = args.index("-f") + 2
                    args[position:position] = ["-f", str(override)]
                result = subprocess.run(args, **kwargs)
                if result.returncode and args[:3] != ["docker", "image", "inspect"]:
                    diagnostic = result.stderr.decode(errors="replace")
                    for line in env.read_text().splitlines():
                        diagnostic = diagnostic.replace(line.split("=", 1)[1], "[redacted]")
                    print("Isolated Docker fixture diagnostic:", diagnostic[-3000:], file=sys.stderr)
                return result
            def docker(*args, data=None, check=True):
                return subprocess.run(["docker", *args], input=data, capture_output=True, check=check)
            old_id = json.loads(docker("image", "inspect", "notey:foundation-review").stdout)[0]["Id"]
            current = {"app": "notey", "revision": "a"*40, "image_id": old_id,
                       "compose": str(package / "compose.yaml")}
            candidate = dict(manifest, directory=str(package), compose=str(package / "compose.yaml"))
            archive = root / "offhost-fixture.tar"
            outer = self
            class LocalAdapter(NoteyAdapter):
                def call(self, phase, old, new=None):
                    if phase == "backup":
                        self.snapshot(old, archive)
                        # Fake the already-separately-tested encrypted Drive layer.
                        backup_archive.verify(archive)
                        return {"app": "notey", "revision": old["revision"],
                                "id": "synthetic-offhost", "verified": True}
                    result = self.phase(phase, old, new)
                    if phase == "migrate" and fail_health:
                        sql("ALTER TABLE foundation_checks DROP COLUMN inserted_at;")
                    return result
                def health(self):
                    self.compose(candidate, ["exec", "-T", "web", "curl", "--fail", "--silent",
                                             "http://localhost:4000/health"])
                    if fail_health:
                        raise RuntimeError("Injected readiness failure after actual activation")
            adapter = LocalAdapter(config, command)
            def sql(query, database="notey", check=True):
                args = ["exec", "-T", "db", "psql", "-X", "-U", "notey", "-d", database,
                        "-At", "-v", "ON_ERROR_STOP=1", "-c", query]
                if check:
                    return adapter.compose(current, args)
                try:
                    adapter.compose(current, args)
                except RuntimeError:
                    return None
                outer.fail("Incompatible old-schema query unexpectedly succeeded")
            network_created = False
            try:
                docker("network", "create", network)
                network_created = True
                adapter.compose(current, ["up", "-d", "--pull", "never", "--wait", "db"])
                adapter.phase("migrate", current, current)
                adapter.phase("activate", current, current)
                fixture = "00000000-0000-0000-0000-000000000022"
                sql("INSERT INTO foundation_checks (id,inserted_at) VALUES ('" + fixture + "',now());")
                state = root / "state"; state.mkdir(mode=0o700)
                save_json(state / "current.json", current)
                runner = Runner(state, adapter)
                with app_lock(state):
                    if fail_health:
                        with self.assertRaises(DeliveryError):
                            runner.deploy(candidate)
                        self.assertEqual(runner.load("transaction")["status"], "recovery_required")
                        self.assertEqual(runner.load("transaction")["stage"], "health")
                        self.assertEqual(runner.load("current"), current)
                        running = adapter.compose(candidate, ["ps", "--status", "running", "--services"])
                        self.assertNotIn(b"web", running.splitlines())
                        self.assertEqual(sql("SELECT id FROM foundation_checks;").strip(), fixture.encode())
                        sql("SELECT inserted_at FROM foundation_checks;", check=False)
                        backup_archive.unpack(archive, root / "restore")
                        adapter.compose(current, ["exec", "-T", "db", "createdb", "-U", "notey", "n02_restore"])
                        dump = (root / "restore/database.dump").read_bytes()
                        args = ["docker", "compose", "--project-name", project, "--env-file", str(env),
                                "-f", current["compose"], "exec", "-T", "db", "pg_restore", "-U", "notey",
                                "-d", "n02_restore", "--exit-on-error", "--no-owner", "--no-acl"]
                        environment = dict(os.environ, NOTEY_IMAGE=old_id, NOTEY_REVISION=current["revision"],
                                           NOTEY_PROXY_NETWORK=network)
                        subprocess.run(args, input=dump, env=environment, capture_output=True, check=True)
                        self.assertEqual(sql("SELECT id FROM foundation_checks WHERE inserted_at IS NOT NULL;",
                                             "n02_restore").strip(), fixture.encode())
                    else:
                        self.assertTrue(runner.deploy(candidate))
                        self.assertEqual(runner.ready()["image_id"], candidate["image_id"])
                        self.assertNotEqual(old_id, candidate["image_id"])
                        self.assertEqual(sql("SELECT id FROM foundation_checks;").strip(), fixture.encode())
            finally:
                if network_created:
                    # These resources were created exclusively by this test; no
                    # production project, existing volume or image is removed.
                    try:
                        adapter.compose(current, ["down", "--volumes", "--remove-orphans"])
                    finally:
                        docker("network", "rm", network)

    def test_actual_ci_image_update_preserves_database(self):
        """Load the CI artifact and update from the existing local foundation image."""
        self.exercise(False)

    def test_failed_health_holds_app_and_dump_recovers_incompatible_schema(self):
        """Stop after failed readiness; restore a dropped column into a new database."""
        self.exercise(True)
