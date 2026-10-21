# Architecture and decisions

Status: foundation implemented locally; deployed behavior must be verified independently. Product requirements live in [product.md](product.md); current gates live in [delivery.md](delivery.md).

## ADR 001 — One Phoenix application, PostgreSQL and UUIDs

Use Phoenix LiveView and PostgreSQL in a single application, as requested. `Notey.Schema` supplies binary UUID primary/foreign keys and UTC microsecond timestamps. Generator defaults and Repo migration defaults agree; actual migrations explicitly declare UUID columns. The synthetic `foundation_checks` table exercises persistence before domain features are added.

An umbrella, generic workflow framework and separate Bible database would add boundaries without a present need. Future contexts are Library, Processing, ReferenceLibrary and Notes, introduced with their workflows rather than empty frameworks now. Notey PostgreSQL owns validated Bible editions, import provenance and exact verses; private PDFs remain source files. The experimental AI-area SQLite database is staging evidence to preserve and validate, not a second permanent application database.

Database provisioning and migrations are different: Compose creates the PostgreSQL service/role/database/volume; Ecto migrations version tables inside that database. `Notey.Release.migrate/0` runs migrations in the built release without installing Mix on Lara. Never automatically run `ecto.reset` in deployment.

## ADR 002 — Separate application releases on a shared host

Develop Notey locally; deploy an immutable production release image under `/srv/lara/apps/notey`. Compose runs a dedicated database on an internal network and the web application on `lara-proxy`, with alias `notey-web`. No app or database host port is published by Notey's Compose file. Initial limits are one CPU and 512 MiB per service, with two BEAM schedulers; these are bounded foundation settings to evaluate, not measured feature capacity.

Caddy, certificates and network ingress belong to `JuliaMathias/home-server-infra`. Companion [issue #11](https://github.com/JuliaMathias/home-server-infra/issues/11) proposes Notey at `https://lara.taila21247.ts.net:8443`, bound only to Lara's Tailscale IPv4. Keep the current port 443 route untouched. Future apps receive their own explicit ingress entries; do not make Notey the host-wide root by accident. Port routing is the smallest initial addition; path-prefix hosting complicates LiveView/asset URLs, while per-app DNS/certificates need a separate design.

AI inference ports remain private. This change does not publish them or assume every future app can share Notey's access policy. The initial Notey stack does not join `lara-backend`; integration is added under the appropriate capability issue after checking its contract and access requirements.

## ADR 003 — Source-aware domain workflows stay in Notey

Applications own session data, prompts, orchestration, review decisions and exports; shared services own generic transcription, extraction and inference/resource coordination. Ordinary automated tests use local PostgreSQL and deterministic fake remote adapters when integration is introduced. Live remote/model evaluations are a separate evidence class.

Planned evidence uses stable UUID note blocks and source units, immutable extraction/source revisions and many-to-many links. Locators identify audio intervals, PDF pages/regions, images and exact Bible edition/ranges. A valid source ID proves traceability, not that a paragraph is true. Source-link warnings after edits are nonblocking. These domain structures are not implemented by N01.

## ADR 004 — Private access, explicit release and recovery gates

Tailscale-only access is approved; extra application login is deferred. Tailnet membership is an access boundary, not application-level per-user authorization. N20 checks all actual source/result/export routes. N01 uses synthetic data only.

Automatic rollout after a user merges passing changes is approved, implemented in N22. Initial N01 rollout is manual and must state exact source/image identity, migrations, readiness and persistence checks. Never merge PRs for the user. A rollback image alone cannot reverse arbitrary schema migrations. Use a compatible prior release only when the migration is backward compatible; otherwise stop and follow the issue-specific recovery plan.

Google Drive is the approved future backup destination. Encryption, external recovery-key handling and isolated restore evidence remain gates. Backup frequency and expiry are proposals, not approved destructive cleanup. PostgreSQL volumes and source files are runtime state outside Git; no backup/recovery guarantee exists yet.

## Sources and compatibility

The scaffold was generated with Phoenix 1.8.7; `mix.lock` records the actual resolved dependencies (Phoenix 1.8.16, LiveView 1.1.33 at foundation validation). `.tool-versions` pins the toolchain, and image digests pin multi-platform base images. Digest pins do not make apt repositories or remote build tooling permanently reproducible; dependency/security updates require another tested PR.

- [Phoenix release guidance](https://phoenix.hexdocs.pm/releases.html): release runtime, migrations and Docker generation.
- [Phoenix generator options](https://phoenix.hexdocs.pm/Mix.Tasks.Phx.New.html): PostgreSQL and binary-ID conventions.
- [Hex build images](https://bob.hex.pm/docker): builder tag compatibility, checked against actual registry manifests.
- [GitHub issue dependency API](https://docs.github.com/en/rest/issues/issue-dependencies): native blocking relationships, verified after issue publication.

The earlier proposal to use Lara's root route for Notey is superseded by ADR 002: preserve root access and independently route multiple applications.
