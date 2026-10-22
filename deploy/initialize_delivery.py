"""Record the verified existing Notey deployment without changing its services.

Run only during the reviewed bootstrap after both PRs are user-merged. Reads the
current Compose/runtime configuration privately; it never prints its secrets.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess


def initialize(config_file, compose_file):
    """Seed a new state directory only after matching live container identity."""
    config_file = Path(config_file)
    if config_file.is_symlink() or config_file.stat().st_mode & 0o077:
        raise ValueError("Controller configuration must be private")
    config = json.loads(config_file.read_text())
    if config["app"] != "notey" or config["project"] != "notey":
        raise ValueError("Initializer is restricted to Notey")
    compose_file = Path(compose_file).resolve(strict=True)
    state = Path(config["state_dir"])
    if (state / "current.json").exists():
        raise ValueError("Existing delivery state must be preserved")
    command = ["docker", "compose", "--project-name", "notey", "--env-file",
               config["runtime_env"], "-f", str(compose_file)]
    environment = dict(os.environ)
    # The deployed private env is authoritative for this one-time inspection.
    environment.pop("NOTEY_IMAGE", None)
    environment.pop("NOTEY_REVISION", None)
    recipe = json.loads(subprocess.check_output(command + ["config", "--format", "json"], env=environment))
    revision = recipe["services"]["web"]["environment"]["NOTEY_REVISION"]
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Current revision is not an exact source identity")
    image = json.loads(subprocess.check_output(
        ["docker", "image", "inspect", recipe["services"]["web"]["image"]]))[0]
    for service in ("db", "web"):
        identifier = subprocess.check_output(command + ["ps", "-q", service], env=environment, text=True).strip()
        if not identifier:
            raise ValueError("Existing Notey service is not running")
        container = json.loads(subprocess.check_output(["docker", "inspect", identifier]))[0]
        if container["State"].get("Health", {}).get("Status") != "healthy":
            raise ValueError("Existing Notey service is not healthy")
        if service == "web" and (container["Image"] != image["Id"]
                or "NOTEY_REVISION=" + revision not in container["Config"]["Env"]):
            raise ValueError("Live release identity differs from the recorded recipe")
    state.mkdir(mode=0o700, parents=True, exist_ok=True)
    if state.is_symlink() or state.stat().st_mode & 0o077:
        raise ValueError("State directory must be private")
    descriptor = os.open(state / "current.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as output:
        json.dump({"app": "notey", "revision": revision, "image_id": image["Id"],
                   "compose": str(compose_file)}, output)
    print("Existing healthy Notey release recorded; no service or secret changed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config_file")
    parser.add_argument("compose_file")
    args = parser.parse_args()
    try:
        initialize(args.config_file, args.compose_file)
    except Exception:
        raise SystemExit("Initialization failed; existing runtime/state was preserved. Inspect configuration privately.") from None
