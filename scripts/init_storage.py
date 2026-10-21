"""Initialize the empty SQLite foundation; never read or ingest source CSVs."""
import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE = ROOT / 'data/local/ttc.sqlite3'
SCHEMA_PATH = ROOT / 'sql/storage_schema.sql'
SCHEMA_VERSION = 1
APPLICATION_ID = 0x54544352  # TTCR


def schema_statements():
    pending = ''
    for line in SCHEMA_PATH.read_text(encoding='utf-8').splitlines(keepends=True):
        pending += line
        if sqlite3.complete_statement(pending):
            yield pending
            pending = ''
    if pending.strip():
        raise RuntimeError('Incomplete storage schema statement')


def schema_signature(connection):
    return connection.execute(
        "SELECT type, name, sql FROM sqlite_schema "
        "WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name"
    ).fetchall()


def initialize_database(database):
    """Create a fresh v1 database, or validate an exact existing v1 schema.

    Reject unrelated, changed or unsupported-version databases. No migrations,
    repairs, data deletion, metadata imports or CSV loads are performed.
    """
    if sqlite3.sqlite_version_info < (3, 38, 0):
        raise RuntimeError('SQLite 3.38+ with JSON support is required')
    statements = list(schema_statements())
    with sqlite3.connect(':memory:') as expected:
        for statement in statements:
            expected.execute(statement)
        signature = schema_signature(expected)
    database = Path(database).resolve()
    if database.suffix not in {'.sqlite3', '.sqlite', '.db'}:
        raise ValueError('Database path must end in .sqlite3, .sqlite or .db')
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database, isolation_level=None, timeout=10)
    try:
        connection.execute('PRAGMA foreign_keys = ON')
        connection.execute('BEGIN IMMEDIATE')
        version = connection.execute('PRAGMA user_version').fetchone()[0]
        application_id = connection.execute('PRAGMA application_id').fetchone()[0]
        existing = schema_signature(connection)
        if version == 0 and application_id == 0 and not existing:
            for statement in statements:
                connection.execute(statement)
            connection.execute(f'PRAGMA application_id = {APPLICATION_ID}')
            connection.execute(f'PRAGMA user_version = {SCHEMA_VERSION}')
        elif (version, application_id, existing) != (SCHEMA_VERSION, APPLICATION_ID, signature):
            raise RuntimeError('Database identity/version/schema mismatch; no changes made')
        if schema_signature(connection) != signature:
            raise RuntimeError('Initialized schema differs from expected definitions')
        if connection.execute('PRAGMA foreign_key_check').fetchall():
            raise RuntimeError('Foreign-key validation failed')
        if connection.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
            raise RuntimeError('Database integrity validation failed')
        counts = {
            name: connection.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
            for kind, name, _ in signature if kind == 'table'
        }
        connection.execute('COMMIT')
        return dict(database=str(database), engine='sqlite', sqlite_version=sqlite3.sqlite_version,
                    schema_version=SCHEMA_VERSION, foreign_keys=True, row_counts=counts)
    except BaseException:
        if connection.in_transaction:
            connection.execute('ROLLBACK')
        raise
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, default=DEFAULT_DATABASE)
    args = parser.parse_args()
    print(json.dumps(initialize_database(args.database), indent=2))


if __name__ == '__main__':
    main()
