# Automatic releases: setup, operation and recovery

N02 implementation is prepared in [Notey PR #30](https://github.com/JuliaMathias/notey/pull/30)
and [infrastructure PR #18](https://github.com/JuliaMathias/home-server-infra/pull/18).
Neither this runbook nor passing fake-service tests establish live acceptance.
Initial activation is a **manual rollout exception after Julia merges both PRs**.
Ordinary later user merges deploy automatically after successful exact-revision CI.
Never merge either PR on Julia's behalf.

## What runs where

GitHub builds one amd64 image, runs its migrations/readiness/persistence checks,
then publishes that same package as an immutable `release-FULL_SHA`. PR runs
cannot publish. Lara checks approximately every five minutes with a repository
read credential. It independently verifies the release, completed main CI, human
merge, tag, checksums, image ID and revision label. It loads the prebuilt image;
there is no source build or dependency installation on Lara. Newer releases can
coalesce to the latest eligible release between checks. A failed/unverified newer
release blocks rather than silently choosing another one.

The shared controller owns locking, stages, storage and retention. Notey's
`deploy/delivery_adapter.py` owns its Compose/PostgreSQL operations. This is like
an Elixir behaviour with a Notey implementation: the common sequence stays the
same, while each application supplies its own data and health operations.
Other applications opt in separately using the infrastructure repository's
[adoption and OAuth guide](https://github.com/JuliaMathias/home-server-infra/blob/9e3ba00fbd284a0e72095e932269994b5c0a5fa2/docs/app-delivery.md);
they choose independent policies and credentials.

Immutable releases were enabled with Julia's approval on 2026-10-22 and
`NOTEY_IMMUTABLE_RELEASES_CONFIRMED=true` was verified. Published assets/tags
cannot be replaced; corrections need a new revision/release. A publication rerun
that collides with an existing release fails; inspect its original workflow and
release rather than deleting/replacing the locked identity.

## Prerequisites and private setup

Use the existing Lara tmux session:

```sh
ssh -t lara 'tmux attach -t notey-n02'
```

Record the **actual user-merged** app and infrastructure SHAs, verify their CI,
and fetch origin/main in `/srv/lara/worktrees/infra-app-delivery`. Preserve the
canonical infrastructure checkout's other work. Use `/usr/bin/python3` (3.11+),
existing Docker/Compose and GnuPG. Do not install tools as an incidental step.

1. Follow the infrastructure guide's **Dedicated Google OAuth setup** on the Mac.
   Create a dedicated Desktop OAuth client, request only `drive.file`, and run
   the reviewed `authorize_drive.py` helper with private input/output files.
   It creates a dedicated unshared backup folder. Complete Google's appropriate
   production/personal-use consent setup: External Testing refresh tokens for
   this scope normally expire after seven days. No live authorization has run.
2. Create a fine-grained GitHub token restricted to `JuliaMathias/notey`, with
   Contents, Actions and Pull requests **read** permissions (plus required
   metadata). Choose and record its expiry; do not silently choose indefinite
   credentials. Save directly in the private host file, never chat/Git/shell
   history. CI needs no tailnet credential.
3. On the Mac, create a dedicated encryption key interactively with an existing
   GnuPG installation (`gpg --full-generate-key`), with encryption capability and
   a strong passphrase. Record the full recipient fingerprint, key expiry and
   renewal procedure. Export only its public key to Lara. Keep the private key,
   passphrase and recovery instructions in Julia's password manager plus a
   protected offline copy. Use file output for private exports, never terminal
   output or chat. Check a recoverable external copy, not just the active keyring.
4. On Lara create `/srv/lara/apps/notey/delivery` and its `state`, `scratch`,
   `public-keyring` directories mode 700. Install the Google credential as
   `delivery/drive.json` and GitHub token as `delivery/github.token`, mode 600.
   Import the public key into the dedicated keyring and verify its fingerprint:
   `gpg --homedir /srv/lara/apps/notey/delivery/public-keyring --import /PRIVATE/public.asc`.
   `--list-secret-keys` in that keyring must show **no private key**.
5. From the reviewed merged infrastructure worktree run
   `bash delivery/v1/install-mechanism.sh FULL_MERGED_INFRA_SHA`. This exports
   only the versioned runtime/units to `/srv/lara/app-delivery/SHA`, starting
   nothing. Set `delivery/mechanism` to that export's `delivery/v1` directory.
   Pinning means another infrastructure update cannot silently update Notey.
6. On the Mac export the reviewed merged app's adapter files into a new private
   temporary directory using `git archive APP_SHA deploy/delivery_adapter.py
   deploy/backup_archive.py deploy/initialize_delivery.py deploy/delivery.example.json`.
   Transfer and extract with `--strip-components=1` into the NEW Lara directory
   `delivery/adapter/APP_SHA`; no app source development checkout is needed there.
7. Copy the example into private `delivery/config.json` (mode 600), replacing
   the two reviewed SHA placeholders and recipient fingerprint. Confirm the
   existing `.env`, `lara-proxy`, HTTPS route and project name `notey`. Preserve
   existing secrets. Do not regenerate passwords or substitute database volumes.
   Leave expiry disabled and restore fields unset initially.

The example is a configuration schema with placeholders, not a ready credential.
It implements before-deployment plus daily backups, retaining all verified points
within five days AND at least the newest 30. Expired objects move to **Drive
Trash**, never permanent deletion or automatic Trash emptying. Google controls
Trash lifetime; trashed files can consume quota. Other apps do not inherit this
policy. The Drive grant can alter/trash its accessible files; encryption protects
contents but does not prevent deletion or make Drive an immutable vault.

## Record current runtime, then prove off-host recovery

The existing N01 recipe is at
`/srv/lara/apps/notey/releases/23e61d8642ed9ab37c3fa1b60441933e7be6a6db/deploy/compose.yaml`.
Verify it is still the running healthy release before using this path. The
initializer checks the actual web/database health, image and revision, refuses
existing current state, and changes no services:

```sh
/usr/bin/python3 /srv/lara/apps/notey/delivery/adapter/APP_SHA/initialize_delivery.py \
  /srv/lara/apps/notey/delivery/config.json \
  /srv/lara/apps/notey/releases/23e61d8642ed9ab37c3fa1b60441933e7be6a6db/deploy/compose.yaml
/usr/bin/python3 /srv/lara/apps/notey/delivery/mechanism/control.py backup /srv/lara/apps/notey/delivery/config.json
```

The first backup is permitted before recording recovery evidence. Deployment and
expiry are blocked until that evidence exists. The backup must return a verified
off-host receipt in `delivery/state/last-backup.json`. Before generating it, save
a new connection-check UUID using the current app and record it as the exact
synthetic recovery fixture; preserve the unidentified phone record.

1. Download that exact receipt ID, verifying folder/app metadata and ciphertext:
   `/usr/bin/python3 delivery/mechanism/download_backup.py delivery/config.json BACKUP_ID /PRIVATE/notey-recovery.gpg`
   from `/srv/lara/apps/notey`. Transfer the ciphertext privately to the Mac.
2. Using the externally recovered key copy, decrypt into a NEW private file:
   `gpg --output /PRIVATE/snapshot.tar --decrypt /PRIVATE/notey-recovery.gpg`.
   Never place the private key on Lara. Verify/unpack on the Mac:
   `python3 deploy/backup_archive.py unpack /PRIVATE/snapshot.tar /PRIVATE/notey-restored-NEW`.
   The tool verifies hashes and refuses overwrite. Record manifest revision/image.
3. Restore `database.dump` into a NEW local PostgreSQL 17 database named
   `n02_live_recovery_check`, checking first that it does not exist. With local
   `compose.dev.yaml` running, use `docker compose -f compose.dev.yaml exec -T db
   createdb -U notey n02_live_recovery_check`, then pipe the dump into
   `docker compose -f compose.dev.yaml exec -T db pg_restore -U notey
   --dbname=n02_live_recovery_check --no-owner --no-acl --exit-on-error`.
   Query `foundation_checks` for the exact saved UUID; schema/data and Ecto
   migration history must be readable. Never restore over a running database.
4. Repeat after an isolated incompatible-schema exercise using the maintained
   [synthetic PostgreSQL test](backup-format.md#runnable-local-verification).
   It demonstrates why an old image cannot recover a dropped column.
5. Record actual UTC time, backup ID, source/image, ciphertext verification,
   external-key copy used, restored UUID/schema and outcomes in issue #22;
   omit secrets/private contents. Only after success set `recovery_verified_at`
   to that timezone-aware ISO timestamp, `recovery_verified_for` to the full
   recipient fingerprint and `recovery_backup_id` to the verified object ID.
   Then enable expiry if the scope/folder/retention checks also passed. A key
   change requires a new restore before changing these receipt fields.
6. Cleanup only `n02_live_recovery_check`, the exact agent-created UUID and named
   temporary recovery files after evidence is recorded. Preserve all other rows,
   databases, runtime volumes, credentials and recovery copies.

**Execution:** live Drive/external-key database recovery is not run; account
authorization and key custody require Julia's direct setup. The separate real
GnuPG synthetic test used fake off-host storage and is not Drive evidence.

## First update and timer activation

Before changing runtime, record current app/image/database identity, HTTPS root
route response hash on port 443, Notey response and container/network state of
the existing shared services. Do not start/stop AI services to make a baseline
look healthy. Verify latest main release publication and completed CI.

Run `control.py check CONFIG` manually through tmux once. It verifies/imports
the image, pauses only Notey web, verifies an encrypted off-host backup, runs the
release migration, activates only web without pulling, and checks HTTPS readiness.
The prior image, database, recipe and `.env` remain available. Check `status`,
current/previous identities and the backup receipt. A failure must follow the
recovery procedure below before any retry.

After this first successful update and recovery proof, install the four reviewed
systemd templates from the pinned export as described in infrastructure
`docs/app-delivery.md`, validate them and reload systemd. Enable only
`lara-app-check@notey.timer` and `lara-app-backup@notey.timer`. Review the daily
04:00 America/Sao_Paulo schedule (up to ten minutes jitter); use a Notey-specific
drop-in if changing it. Verify `systemctl list-timers` and service/journal status.
No other application's units or routing should change.

For acceptance, make a later ordinary user merge with passing CI, observe its
immutable release and automatic exact image activation. On laptop Tailscale,
visit `https://lara.taila21247.ts.net:8443`, save a new connection-check UUID,
reload and verify it remains. Confirm actual WebSocket transport and the prior
synthetic fixture's persistence. Recheck port 443 response hash, routes and shared
service state against the baseline. Repeat the physical-phone procedure in
testing.md when relevant; record user-reported and observed evidence separately.

**Pass criteria:** exact tested image deployed without Lara builds/downloaded
dependencies; verified pre-migration backup; UUID data persists; HTTPS/WebSocket
works; only Notey changes; both timers and daily receipt succeed. Record failed,
pending and unrun gates explicitly. Do not close #22 at PR merge.

## Failures and migration recovery

Inspect `control.py status CONFIG`, `state/transaction.json` and
`journalctl -u lara-app-check@notey.service` / backup service. Tool errors suppress
child diagnostics that could contain credentials; inspect private configuration
directly without printing it into issue/chat logs. Backup failure before migration
attempts to resume the current web image; no migration runs. A migration,
activation, health or interrupted-transaction failure blocks subsequent operations.

1. Stop future Notey timer triggers; inspect active service and app-scoped one-off
   migration containers. A timeout does not prove a database migration stopped.
   Preserve the transaction, images, recipes, `.env`, database and receipt. Keep
   the receipt ID in `protected_backup_ids` before resolving the incident.
2. Confirm Notey web is stopped. Inspect schema/migration state privately. If a
   compatible prior image is proven safe, an operator may explicitly reactivate
   its recorded recipe/image and verify health/data. Never infer compatibility
   merely because an older image exists.
3. Otherwise download/decrypt the recorded pre-migration backup externally and
   restore into a NEW isolated database as above. Validate the expected schema,
   exact synthetic record and migration history. Preserve the failed production
   database for investigation; never run reset, down -v or volume pruning.
4. Before a production data cutover, obtain Julia's approval for the exact
   recovery point and any writes lost since it. Prepare a reviewed incident
   procedure to point Notey at the validated restored database or quarantine the
   failed database and rename the restored one. Do not automatically overwrite,
   drop or rename production databases. Include connection-drain and readiness
   checks in that concrete incident procedure.
5. After verified operator recovery, archive the transaction record as a new
   private incident file and reconcile `current.json` with the actual image,
   revision and recipe. Remove the active transaction marker only after recording
   the resolution; never clear it merely to make a timer retry. Retry/enable only
   Notey's timers after health, data, backup and shared-service checks pass.

This conservative hold can cause downtime after failed migrations. It preserves
the information needed to recover without pretending that image rollback can
reverse arbitrary data changes. The local isolated successful/failed-health
exercises passed separately; the first automatic user-merged Lara deployment
remains an acceptance gate.

## Verification recorded during implementation

- CI [39735572645](https://github.com/JuliaMathias/notey/actions/runs/39735572645)
  passed on `cbdb595`: app tests, Dialyzer, assets/release, actual amd64 image,
  migration/readiness/restart persistence. PR publication correctly skipped.
- Local app adapter/archive/initializer: 14 deterministic tests passed; the
  ordinary suite discovers 17 tests and skips three explicit integration opt-ins.
- Real local PostgreSQL 17 destructive-column dump/restore passed separately.
- Two actual local Docker update/recovery exercises passed with CI run
  39735572645 image config `7a25f7d` / OCI manifest `52f56ec`: update from the
  existing foundation image preserved UUID `00000000-0000-0000-0000-000000000022`;
  injected failed readiness stopped web and held recovery; restoring the
  pre-migration dump recovered its dropped inserted_at column and exact UUID.
  Storage was fake and container HTTP used local ARM emulation with the
  upstream OTP `+JMsingle true` test-only override. This is not Lara/Drive evidence.
- Shared infrastructure: 40 deterministic tests passed; actual public-key
  encryption/external-key byte recovery passed separately with fake storage.
- Live Drive consent, key custody, first immutable published release, installed
  timers and post-N02 Lara/browser acceptance:
  **not run**. No automatic updater or expiry is active on Lara.

Official setup sources: [Google Desktop OAuth](https://developers.google.com/identity/protocols/oauth2/native-app),
[token expiration](https://developers.google.com/identity/protocols/oauth2#expiration),
[Drive per-file scope](https://developers.google.com/workspace/drive/api/guides/api-specific-auth).

Image-store sources: [Docker containerd store](https://docs.docker.com/engine/storage/containerd/)
and [OTP emulation constraint](https://github.com/erlang/otp/issues/10355).
