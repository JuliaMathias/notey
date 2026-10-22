"""One-time bootstrap must reflect healthy actual containers and preserve state."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from initialize_delivery import initialize


class InitializeTest(unittest.TestCase):
    """Use synthetic Docker metadata without operating services or secrets."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = self.root / "config.json"
        self.state = self.root / "state"
        self.config.write_text(json.dumps({"app": "notey", "project": "notey",
                                          "runtime_env": "private.env", "state_dir": str(self.state)}))
        self.config.chmod(0o600)
        self.compose = self.root / "compose.yaml"; self.compose.write_text("synthetic")
        self.healthy = True; self.revision = "a"*40

    def output(self, command, **kwargs):
        """Expose only the recipe/image/container metadata used by bootstrap."""
        if "config" in command:
            return json.dumps({"services": {"web": {"image": "old-image",
                                "environment": {"NOTEY_REVISION": "a"*40}}}}).encode()
        if command[:3] == ["docker", "image", "inspect"]:
            return b'[{"Id":"sha256:synthetic"}]'
        if "ps" in command:
            return command[-1] + "-container"
        return json.dumps([{"State": {"Health": {"Status": "healthy" if self.healthy else "unhealthy"}},
                            "Image": "sha256:synthetic", "Config": {"Env": ["NOTEY_REVISION=" + self.revision]}}]).encode()

    def test_healthy_matching_runtime_is_recorded_without_service_operations(self):
        """Record private current state once, then refuse any overwrite."""
        with patch("initialize_delivery.subprocess.check_output", side_effect=self.output) as commands:
            initialize(self.config, self.compose)
            current = self.state / "current.json"
            before = current.read_bytes()
            self.assertEqual(current.stat().st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(before)["revision"], "a"*40)
            with self.assertRaises(ValueError): initialize(self.config, self.compose)
            self.assertEqual(current.read_bytes(), before)
            self.assertFalse(any("up" in call.args[0] or "stop" in call.args[0] for call in commands.call_args_list))

    def test_unhealthy_or_mismatched_runtime_cannot_seed_state(self):
        """Do not teach the controller an unverified current deployment."""
        for healthy, revision in ((False, "a"*40), (True, "b"*40)):
            self.healthy = healthy; self.revision = revision
            with patch("initialize_delivery.subprocess.check_output", side_effect=self.output):
                with self.assertRaises(ValueError): initialize(self.config, self.compose)
            self.assertFalse((self.state / "current.json").exists())
