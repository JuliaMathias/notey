# Initial manual deployment on Lara

N01 deploys an empty/synthetic foundation. Develop on the Mac. Use an immutable archive of a reviewed revision for deployment, not an editable application development checkout on Lara. The first rollout is active; Julia reported the physical-phone acceptance procedure passed on 2026-10-21. See [delivery status](delivery.md).

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

## Slow-network build downloads

The build fetches locked production dependencies with `HEX_HTTP_CONCURRENCY=1` and `HEX_HTTP_TIMEOUT=120`: one Hex request at a time, allowing up to 120 seconds per request. These settings apply only to that build command, not the running application. Dependency versions remain in `mix.lock`; TLS and registry verification remain enabled. A longer timeout cannot fix an unavailable network or guarantee every download succeeds. See [Hex configuration](https://hex.hexdocs.pm/Mix.Tasks.Hex.Config.html).

Initial Lara builds on 2026-10-21 failed first on installer DNS lookup and then on registry/package timeouts. A build-only public-host mapping and temporary builder resolver isolated the lookup problem; neither is a permanent host DNS or application-network change. Do not hardcode those transient CDN addresses into source. Investigate current connectivity if installer lookup fails again; the Hex dependency timeout does not govern `mix local.hex`, Rebar or Debian downloads.

Validation used an isolated native amd64 builder capped at two CPUs and 4 GiB. The production image completed with the dependency timeout change, and its release executable reported Elixir 1.19.5 / OTP 28 and loaded `NoteyWeb.FoundationLive`. The temporary builder was then stopped, preserving its cache. This is build/package evidence, not deployment, database or HTTPS acceptance. A validation image from an unmerged change must not be presented as the deployed merged release.

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

## Deployed release — 2026-10-21

The first deployment uses merged Notey revision `23e61d8642ed9ab37c3fa1b60441933e7be6a6db`. Source and deployment recipes are retained at `/srv/lara/apps/notey/releases/23e61d8642ed9ab37c3fa1b60441933e7be6a6db`; this is an immutable release directory, not an application development checkout. Its `source.tar` SHA-256 is `594635a6d2747b383947d625100c995b7d9fae9010b03ead6b6f10488435ba06`.

- App image tag: `notey:23e61d8642ed9ab37c3fa1b60441933e7be6a6db`; amd64 image ID: `sha256:df8a07872039be08fa5dd306cdb13809b852cfdee7b734717c4b67e01fb973e3`.
- PostgreSQL image ID: `sha256:79bd7c99e923138f136f8009d6bffa66e21e9d4fda5c0c561b00fc9c90cfe537`.
- Private runtime file: `/srv/lara/apps/notey/.env`, mode 600. Keep existing secrets on subsequent releases.
- `deploy/apply.sh` ran migration `20261020195000`, created the dedicated persistent database volume and started healthy database/web containers. Neither publishes a host port.
- HTTPS: `https://lara.taila21247.ts.net:8443`; `/health` returns HTTP 200 with `{"status":"ok"}` under normal certificate verification.

The active ingress recipe is `/srv/lara/infrastructure-deployments/72c37eeb195d2851ec157d7f7c3c601b3eb663f7/caddy/compose.yaml`, from the merged infrastructure companion. Its certificate mount points to the existing `/srv/lara/infrastructure/caddy/certs` directory, read-only, instead of a relative directory. No certificates were copied or permissions changed. Compose project `lara-caddy`, Caddy image, named volumes and `lara-proxy` were preserved. Use this active recipe for ingress operations; do not assume an unrelated infrastructure working branch represents the live recipe.

Caddy publishes `100.89.181.91:443` and `100.89.181.91:8443`. The previous port-443 response was compared before and after activation and remained identical. The activation briefly recreated Caddy for the additional port; a subsequent retry and comparison passed. No AI endpoints were exposed. Transcription was already stopped before rollout; generation was running and separately managed.

On this release, a synthetic UUID survived restarting `db web` with the recorded app Compose file, followed by `up -d --wait --wait-timeout 120`. Browser reload and a new save also passed afterward. This establishes persistence through an application/database restart, not host-reboot acceptance or off-host recovery. Julia reported phone/cellular testing passed; the specific browser and phone UUID were not supplied. The isolated build container was stopped after image creation, retaining its cache.

Recovery remains service-specific: stop only Notey web if the initial app fails, preserve its database and investigate; there is no earlier production application release to roll back to. For ingress recovery, use the recorded previously deployed configuration from the infrastructure runbook, preserving its existing certificate mount, volumes and port 443. Validate before activation and coordinate with any later infrastructure changes. Do not replace the live ingress with an arbitrary working-tree configuration.
