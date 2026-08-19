import shutil
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / "inventory.db"
BACKUP_DIR = BASE_DIR / "backups"


def create_backup():
    if not DATABASE_FILE.exists():
        raise FileNotFoundError("Database file not found.")

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    backup_file = (
        BACKUP_DIR
        / f"inventory_backup_{timestamp}.db"
    )

    shutil.copy2(
        DATABASE_FILE,
        backup_file
    )

    return backup_file


def restore_backup(backup_file):
    backup_file = Path(backup_file)

    if not backup_file.exists():
        raise FileNotFoundError(
            "Backup file not found."
        )

    if not DATABASE_FILE.exists():
        shutil.copy2(
            backup_file,
            DATABASE_FILE
        )
        return

    old_database = (
        BASE_DIR
        / f"inventory_before_restore_"
        f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.db"
    )

    shutil.copy2(
        DATABASE_FILE,
        old_database
    )

    shutil.copy2(
        backup_file,
        DATABASE_FILE
    )


def list_backups():
    if not BACKUP_DIR.exists():
        return []

    return sorted(
        BACKUP_DIR.glob("inventory_backup_*.db"),
        key=lambda file: file.stat().st_mtime,
        reverse=True
    )