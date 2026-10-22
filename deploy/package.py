"""Describe the exact tested image and Compose recipe for immutable publication."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


def package(destination, revision, run_id):
    """Save the already-tested amd64 image; never rebuild it during publication."""
    if not re.fullmatch(r"[0-9a-f]{40}", revision) or not run_id.isdecimal():
        raise ValueError("An exact source revision and CI run are required")
    folder = Path(destination)
    folder.mkdir(exist_ok=False)
    image = json.loads(subprocess.check_output(
        ["docker", "image", "inspect", "notey:" + revision], text=True))[0]
    if (image["Architecture"] != "amd64" or image["Os"] != "linux"
            or image["Config"]["Labels"].get("org.opencontainers.image.revision") != revision):
        raise ValueError("Packaged image does not match its source/platform")
    # Keep the image ID plus archive digest: tags alone are replaceable names.
    with (folder / "image.tar.gz").open("wb") as output:
        saved = subprocess.Popen(["docker", "save", image["Id"]], stdout=subprocess.PIPE)
        try:
            compressed = subprocess.run(["gzip", "-n"], stdin=saved.stdout, stdout=output)
            saved.stdout.close()
            if saved.wait() or compressed.returncode:
                raise RuntimeError("Image packaging failed")
        finally:
            if saved.poll() is None:
                saved.terminate()
                saved.wait()
    shutil.copyfile("deploy/compose.yaml", folder / "compose.yaml")
    artifacts = {}
    for name in ("image.tar.gz", "compose.yaml"):
        with (folder / name).open("rb") as stream:
            artifacts[name] = hashlib.file_digest(stream, "sha256").hexdigest()
    manifest = {"contract": 1, "app": "notey", "revision": revision,
                "run_id": int(run_id), "image_id": image["Id"], "artifacts": artifacts}
    (folder / "release.json").write_text(json.dumps(manifest, sort_keys=True))
    return manifest


if __name__ == "__main__":
    package("release-package", os.environ["GITHUB_SHA"], os.environ["GITHUB_RUN_ID"])
