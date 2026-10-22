#!/bin/bash
# Exercise the actual packaged image only on a disposable GitHub-hosted runner.
set -euo pipefail
[[ ${GITHUB_ACTIONS:-} == true && ${RUNNER_ENVIRONMENT:-} == github-hosted ]]
[[ ${GITHUB_RUN_ID:-} =~ ^[0-9]+$ && ${GITHUB_RUN_ATTEMPT:-} =~ ^[0-9]+$ ]]
[[ ${GITHUB_SHA:-} =~ ^[0-9a-f]{40}$ ]]
project="notey-ci-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}"
private_env=$(mktemp)
chmod 600 "$private_env"
export NOTEY_CI_PROJECT="$project" NOTEY_CI_ENV="$private_env"
python3 - <<'PY'
import os, secrets
from pathlib import Path
values = {
    'NOTEY_IMAGE': 'notey:' + os.environ['GITHUB_SHA'],
    'NOTEY_REVISION': os.environ['GITHUB_SHA'],
    'NOTEY_PROXY_NETWORK': os.environ['NOTEY_CI_PROJECT'],
    'PHX_HOST': 'localhost', 'PHX_PORT': '8443',
    'NOTEY_DB_PASSWORD': secrets.token_urlsafe(32),
    'SECRET_KEY_BASE': secrets.token_urlsafe(64),
    'RELEASE_COOKIE': secrets.token_urlsafe(32),
}
Path(os.environ['NOTEY_CI_ENV']).write_text(''.join(k + '=' + v + '\n' for k, v in values.items()))
PY
compose=(docker compose --project-name "$project" --env-file "$private_env" -f deploy/compose.yaml)
cleanup() {
  # Only this run's synthetic project/network; never a runtime project.
  "${compose[@]}" down -v >/dev/null 2>&1 || true
  docker network rm "$project" >/dev/null 2>&1 || true
  rm -f "$private_env"
}
trap cleanup EXIT
docker network create "$project" >/dev/null
"${compose[@]}" config --quiet
"${compose[@]}" up -d --wait --wait-timeout 120 db
"${compose[@]}" run --rm --no-deps web /app/bin/migrate
"${compose[@]}" up -d --wait --wait-timeout 120 web
"${compose[@]}" exec -T web curl --fail --silent http://localhost:4000/health
"${compose[@]}" exec -T db psql -U notey -d notey -v ON_ERROR_STOP=1 -c \
  "INSERT INTO foundation_checks (id, inserted_at) VALUES ('00000000-0000-0000-0000-000000000022', now());"
"${compose[@]}" restart db web
"${compose[@]}" up -d --wait --wait-timeout 120 db web
actual=$("${compose[@]}" exec -T db psql -U notey -d notey -At -c \
  "SELECT id FROM foundation_checks WHERE id='00000000-0000-0000-0000-000000000022';")
[[ "$actual" == 00000000-0000-0000-0000-000000000022 ]]
"${compose[@]}" exec -T web curl --fail --silent http://localhost:4000/health
