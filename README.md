# Notey

A personal study workspace combining recordings, personal notes, slides and verified references into complete, source-linked notes.

## Status

Task [N01 / #1](https://github.com/JuliaMathias/notey/issues/1) establishes the foundation. The app currently has a minimal LiveView page that persists a synthetic UUID record in PostgreSQL, plus a database readiness endpoint. Session uploads, AI processing, Bible imports and finished-note workflows are not implemented.

The foundation is deployed at [Notey on Lara](https://lara.taila21247.ts.net:8443), accessible through Tailscale. Merged-main CI passed with 11 PostgreSQL tests, coverage and Dialyzer checks, assets and a production release. On 2026-10-21, laptop HTTPS, live save/reload and persistence across a Lara app/database restart passed. Julia reported the physical-phone cellular/Tailscale procedure passed on 2026-10-21; N01 runtime acceptance is complete. The final evidence documentation was user-merged in PR #29 (`c27241d`). See [delivery status](docs/delivery.md). The approved 25 tasks are published in [GitHub Project 8](https://github.com/users/JuliaMathias/projects/8).

## Local setup

Prerequisites: Git, Docker Engine/Desktop with Compose, Erlang 28.3.1 and Elixir 1.19.5 (OTP 28), as pinned in `.tool-versions`. Use your existing tool manager to install/select those versions. Dependency and asset downloads need internet access. Node.js is not required: Mix downloads pinned Tailwind/esbuild executables.

```sh
docker compose -f compose.dev.yaml up -d --wait
mix setup
mix phx.server
```

Open <http://localhost:4000>. Click **Save connection check**, then reload: the UUID should remain. Local PostgreSQL is bound only to `127.0.0.1:55432`; development-only credentials are in `compose.dev.yaml`. `NOTEY_DB_HOST`, `NOTEY_DB_PORT`, `NOTEY_DB_USER` and `NOTEY_DB_PASSWORD` override the defaults. Development and tests do not need Lara or an AI service.

```sh
mix format --check-formatted
mix compile --warnings-as-errors
mix coveralls.html
mix dialyzer
mix assets.build
```

Tests use the real local PostgreSQL and roll back their fixtures. Use `mix test` for a run without coverage. `mix coveralls.html` runs the tests with line coverage, enforces the initial 35% minimum and writes `cover/excoveralls.html`. CI saves the report as a downloadable artifact and publishes coverage to Coveralls.io using its GitHub integration. Notey must be enabled in your Coveralls account; see the [setup instructions](docs/testing.md#coverallsio-setup-and-verification). Dialyzer checks code/type consistency locally and in CI; its first run builds a reusable analysis cache and takes longer. [Testing guidance](docs/testing.md) covers production builds, manual browser checks and evidence. Stop the local database with `docker compose -f compose.dev.yaml stop`; preserve its named volume. `mix ecto.reset` destroys the selected development database, so do not use it against valuable data.

## Deployment and ownership

Develop on this Mac. Lara hosts separately deployed applications and shared infrastructure. [Deployment instructions](docs/deployment.md) describe the release, dedicated PostgreSQL, migrations, restart and active Tailscale ingress at `https://lara.taila21247.ts.net:8443`. N02 / issue #22 is in progress: the [backup format and local recovery check](docs/backup-format.md) are implemented, with pull deployment and backup/key policies approved. Shared runtime implementation and live credential/recovery setup remain pending. No automatic deployment exists yet; N02 adds it after a user merge, never automatic PR merging.

Notey owns sessions, prompts, workflows, evidence, Bible imports and exports. Shared AI services own domain-neutral inference/extraction. Keep credentials, model weights, runtime databases, original recordings/notebooks, Bible text and generated private notes outside Git and release images. Git stores recipes, code, migrations and synthetic fixtures; it is not a backup of application data.

## Structure and planning

- `lib/notey/`: application supervision, database, synthetic foundation check and readiness.
- `lib/notey_web/`: LiveView, HTTP health route and web components.
- `priv/repo/`: application schema migrations; no private reference data.
- `test/`: deterministic tests with local PostgreSQL.
- `config/`, `compose.dev.yaml`: configurable runtime and local development.
- `Dockerfile`, `rel/`, `deploy/`: production release and deployment recipe.
- [Product](docs/product.md), [architecture](docs/architecture.md), [delivery](docs/delivery.md), [testing](docs/testing.md), [deployment](docs/deployment.md).
- [Design review](docs/design-review.md) contains the Figma link and remaining wireframe feedback. [Issue drafts](docs/issue-drafts.md) are the historical approved planning snapshot; GitHub issues are the implementation backlog.

Use issue branches and signed descriptive commits. Use the [PR template](.github/PULL_REQUEST_TEMPLATE.md), including an explicit manual-testing decision and instructions when needed. Open linked PRs with actual test evidence; the user reviews and merges. Squash merging is preferred. See [AGENTS.md](AGENTS.md).
