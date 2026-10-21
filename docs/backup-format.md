# Foundation backup format

N02 / [issue #22](https://github.com/JuliaMathias/notey/issues/22) requires a
database recovery point and a file manifest contract. `deploy/backup_archive.py`
implements that contract using Python 3.11 or newer and its standard library.
This module packages and verifies a completed dump; it does not take a live
backup, encrypt it, upload it, schedule it or delete old backups. Those operations
remain separate acceptance gates. Never upload its plaintext output.

## Contents and boundaries

Each uncompressed tar archive contains `manifest.json`, `database.dump` and
explicitly supplied `files/<relative path>` entries. Format 1 identifies Notey,
PostgreSQL major version 17, the full source revision, the Docker image ID, and
each payload's byte count and SHA-256. N02 uses only synthetic file fixtures;
actual private-file and asynchronous-job consistency belongs to issue #21.
Application credentials and recovery keys are outside this format. Record the
backup timestamp and encrypted-object identity in the eventual storage receipt.

Use PostgreSQL 17's `pg_dump --format=custom --no-owner --no-acl`. It takes a
consistent database snapshot. File writers must be quiesced separately before
future file integration; a database snapshot does not make arbitrary files
consistent with it. SHA-256 detects changed bytes; it does not authenticate an
untrusted backup. Encryption/authenticity and recovery-key verification remain
required before production use.

Creation refuses an existing archive and creates its file with mode 600.
Verification checks every payload against its manifest and rejects duplicate,
unexpected, non-regular and unsafe members. Recovery first verifies the full
archive, then copies regular-file bytes into a **new** directory with mode 700;
it never uses tar's general-purpose extraction or overwrites a runtime directory.
File modes are 600. Recovery scratch space must remain private and large enough
for the unencrypted dump; remove only the named scratch data after verification.

## Runnable local verification

Ordinary deterministic tests:

```sh
python3 -m unittest discover -s deploy -p 'test_backup_archive.py' -v
```

The separate PostgreSQL check needs Docker and this repository's running local
development database container. It creates two randomly named `n02_source_*` /
`n02_restore_*` databases in that service, never uses `notey_dev`, `notey_test`
or Lara, and drops precisely those temporary databases afterward:

```sh
docker compose -f compose.dev.yaml up -d --wait
NOTEY_BACKUP_TEST_CONTAINER=notey-dev-db-1 \
  python3 -m unittest discover -s deploy -p 'test_backup_postgres.py' -v
```

1. The test creates `recovery_probe` with UUID
   `00000000-0000-0000-0000-000000000022` and text `N02 synthetic recovery`.
2. It takes a real custom-format PostgreSQL dump and packages it with the text
   file `N02 synthetic file contract`.
3. It drops the source table's `note` column and proves the previous query fails.
   Running older application code cannot recover a column's deleted contents.
4. It verifies/unpacks the archive and uses `pg_restore --exit-on-error
   --single-transaction --no-owner --no-acl` into the second, empty database.
5. It requires the exact UUID/text and file bytes to survive. Any failed assertion
   or command fails the check. Cleanup drops only the two randomly named databases.

Record the revision, PostgreSQL version, command, test count and outcome.
Execution on 2026-10-21: six deterministic tests and the separate PostgreSQL 17
recovery test passed on this Mac. This is local archive/database evidence; it is
not encrypted Drive recovery or a Lara rollout/restore result.

Sources: [PostgreSQL pg_dump](https://www.postgresql.org/docs/17/app-pgdump.html),
[PostgreSQL pg_restore](https://www.postgresql.org/docs/17/app-pgrestore.html).
