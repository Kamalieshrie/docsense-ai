import sqlite3
import os

def migrate():
    db_path = None
    storage = "./storage"

    if os.path.exists(storage):
        for f in os.listdir(storage):
            if f.endswith(".db"):
                db_path = os.path.join(storage, f)
                print(f"Found DB: {db_path}")
                break

    if not db_path:
        print("No database found in ./storage")
        print("Files:", os.listdir(storage) if os.path.exists(storage) else "folder missing")
        return

    conn   = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(documents)")
    cols = [r[1] for r in cursor.fetchall()]
    print(f"Columns: {cols}")

    if "sharepoint_url" not in cols:
        cursor.execute("ALTER TABLE documents ADD COLUMN sharepoint_url TEXT DEFAULT ''")
        print("Added: sharepoint_url")
    else:
        print("Already exists: sharepoint_url")

    if "sharepoint_json_url" not in cols:
        cursor.execute("ALTER TABLE documents ADD COLUMN sharepoint_json_url TEXT DEFAULT ''")
        print("Added: sharepoint_json_url")
    else:
        print("Already exists: sharepoint_json_url")

    conn.commit()
    conn.close()
    print("Migration complete!")

migrate()