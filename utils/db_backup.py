#!/usr/bin/env python
"""
Database backup utility for FatPyWeb project.
Run this script to create a backup of the database.
"""

import os
import sys
import datetime
import subprocess
import argparse
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))


def backup_sqlite(db_path, backup_dir):
    """Create a backup of an SQLite database."""
    if not os.path.exists(db_path):
        print(f"Database file does not exist: {db_path}")
        return False

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"db_backup_{timestamp}.sqlite3")

    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    # Copy the database file
    import shutil

    shutil.copy2(db_path, backup_path)

    print(f"Backup created: {backup_path}")
    return True


def backup_postgres(db_name, db_user, backup_dir):
    """Create a backup of a PostgreSQL database."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"db_backup_{timestamp}.sql")

    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    # Run pg_dump to create backup
    try:
        subprocess.run(
            ["pg_dump", "-U", db_user, "-d", db_name, "-f", backup_path], check=True
        )
        print(f"Backup created: {backup_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error backing up database: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Create a database backup")
    parser.add_argument(
        "--type",
        choices=["sqlite", "postgres"],
        default="sqlite",
        help="Database type (default: sqlite)",
    )
    parser.add_argument("--db-path", help="Path to SQLite database file")
    parser.add_argument("--db-name", help="PostgreSQL database name")
    parser.add_argument("--db-user", help="PostgreSQL database user")
    parser.add_argument(
        "--backup-dir",
        default="backups",
        help="Directory for backups (default: backups)",
    )

    args = parser.parse_args()

    if args.type == "sqlite":
        db_path = args.db_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "db.sqlite3"
        )
        backup_sqlite(db_path, args.backup_dir)
    elif args.type == "postgres":
        if not args.db_name or not args.db_user:
            print("Error: PostgreSQL backups require --db-name and --db-user")
            sys.exit(1)
        backup_postgres(args.db_name, args.db_user, args.backup_dir)


if __name__ == "__main__":
    main()
