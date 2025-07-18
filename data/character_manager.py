# 📄 data/deletion_log.py
import sqlite3

def log_character_deletion(character_name, realm, deleted_by):
    conn = sqlite3.connect("dao_do_items.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO deletion_logs (character_name, realm, deleted_by) VALUES (?, ?, ?)",
        (character_name, realm, deleted_by)
    )
    conn.commit()
    conn.close()
