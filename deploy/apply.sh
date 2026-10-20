#!/bin/sh
# Activate an already-built Notey release; never alter shared ingress or user data.
set -eu
if [ "$#" -ne 1 ]; then
  echo 'Usage: deploy/apply.sh /absolute/path/to/private.env' >&2
  exit 2
fi
case "$1" in /*) ;; *) echo 'The private env path must be absolute.' >&2; exit 2 ;; esac
[ -f "$1" ] || { echo 'Private env file not found.' >&2; exit 2; }
recipe=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/compose.yaml
# Keep full interpolation out of logs, because it includes credentials.
docker compose --project-name notey --env-file "$1" -f "$recipe" config --quiet
docker network inspect lara-proxy >/dev/null
image=$(docker compose --project-name notey --env-file "$1" -f "$recipe" config --format json | python3 -c 'import json,sys; print(json.load(sys.stdin)["services"]["web"]["image"])')
docker image inspect "$image" >/dev/null
docker compose --project-name notey --env-file "$1" -f "$recipe" up -d --wait --wait-timeout 120 db
docker compose --project-name notey --env-file "$1" -f "$recipe" run --rm --no-deps web /app/bin/migrate
docker compose --project-name notey --env-file "$1" -f "$recipe" up -d --wait --wait-timeout 120 web
