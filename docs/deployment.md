# Initial manual deployment on Lara

N01 deploys an empty/synthetic foundation. Develop on the Mac. Use an immutable archive of a reviewed revision for deployment, not an editable application development checkout on Lara. The actual rollout remains pending until the required PRs are user-merged; see [delivery status](delivery.md).

## Ownership and prerequisites

- App files: `/srv/lara/apps/notey`; deployment Compose/recipe comes from this repository.
- Shared ingress: `JuliaMathias/home-server-infra`, [issue #11](https://github.com/JuliaMathias/home-server-infra/issues/11), separate PR. Preserve existing HTTPS 443 and AI services. Target Notey URL: `https://lara.taila21247.ts.net:8443`.
- Existing Docker/Compose and Python 3, `lara-proxy`, Tailscale address/hostname and certificate must be checked on Lara before applying anything. No host packages, firewall policy, certificate copying or AI port publishing is part of this recipe.
- Initial foundation uses dedicated `notey` PostgreSQL, persistent named volume `notey_postgres_data`, internal database network and alias `notey-web` on `lara-proxy`. No app/database host ports.
- Bootstrap creates host/shared prerequisites; it does not run app schema migrations. Notey owns its dedicated database Compose service and Ecto migrations. No shared-infrastructure bootstrap change is necessary for this app recipe.

## Prepare the exact source and image

After user merge, verify the merged SHA and passing CI. Build on Lara for its actual architecture from a Git archive of that SHA, or transfer a verified image built for that architecture. Example from the Mac (replace `REVISION` with the actual full SHA):

```sh
git archive --format=tar REVISION > /tmp/notey-release.tar
scp /tmp/notey-release.tar lara:/srv/lara/apps/notey-release.tar
```

On Lara create `/srv/lara/apps/notey` and an empty `/srv/lara/apps/notey/releases/REVISION` directory, then extract the archive there. Do not overwrite another release or the runtime `.env`. Build from that source directory:

```sh
docker build --tag notey:REVISION .
docker image inspect notey:REVISION --format '{{.Id}} {{.Architecture}}'
```

Record source SHA and resulting image identity in the issue. Build one release at a time, check available memory/CPU, and do not start competing AI evaluations. The Compose runtime limits do not limit Docker image builds.

## Secrets and activation

Copy `deploy/.env.example` to `/srv/lara/apps/notey/.env` on Lara with mode 600, outside Git. Generate fresh URL-safe random database password and release cookie, and at least 64 random characters for `SECRET_KEY_BASE`, using Python's `secrets` or `mix phx.gen.secret`; write directly to the private file, without printing values. Set the exact `NOTEY_IMAGE`, `NOTEY_REVISION`, verified `PHX_HOST` and `PHX_PORT=8443`. Never run `docker compose config` without `--quiet` in a recorded log, as interpolation can reveal secrets.

From the extracted source directory, run:

```sh
./deploy/apply.sh /srv/lara/apps/notey/.env
```

The script validates configuration/image/network availability, starts/waits for the dedicated database, runs release migrations once, then starts/waits for the app. It does not build images, alter Caddy, reset/drop databases, prune images or remove volumes. A failed migration stops rollout; do not continue by hand or hide the error.

Enable the separately reviewed infrastructure ingress using that PR's runbook after the app is healthy. No automatic rollout exists until N02; this is an explicit manual-rollout exception for the initial foundation. Keep issue #1 open until real deployment/device gates pass.

## Restart, verification and recovery

Use the same private env and Compose file from the deployed release. Restart only the app/database, then wait for readiness:

```sh
docker compose --project-name notey --env-file /srv/lara/apps/notey/.env -f deploy/compose.yaml restart db web
docker compose --project-name notey --env-file /srv/lara/apps/notey/.env -f deploy/compose.yaml up -d --wait --wait-timeout 120
```

Follow [testing.md](testing.md) for actual HTTPS/WebSocket, phone-over-cellular and persistence evidence. Record the source/image and URL; do not infer acceptance from container health alone.

Before future nontrivial migrations, obtain a consistent recovery point and assess schema compatibility. If an image fails without an incompatible migration, restore the prior recorded image/revision in the private env and run `deploy/apply.sh` again. Do not automatically reverse migrations or delete volumes. For N01's first-ever installation there is no prior app release; stop the Notey web service, preserve PostgreSQL state and investigate. Existing Lara routes and shared AI stay running.

Google Drive backup/restore automation is N02 and not implemented here. A Docker volume surviving restart is persistence, not a verified off-host backup. Never run `docker compose down -v`, `volume prune`, `ecto.reset` or secret regeneration against an existing database as an update procedure.
