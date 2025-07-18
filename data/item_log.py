import sqlite3

def get_connection():
    return sqlite3.connect("dao_do_items.db")

def log_edit(item_id, editor, field_changed, old_value, new_value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO item_edit_log (item_id, editor, timestamp, field_changed, old_value, new_value)
        VALUES (?, ?, datetime('now'), ?, ?, ?)
    """, (item_id, editor, field_changed, str(old_value), str(new_value)))
    conn.commit()

def get_edit_log(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, editor, field_changed, old_value, new_value
        FROM item_edit_log
        WHERE item_id = ?
        ORDER BY timestamp DESC
    """, (item_id,))
    rows = cur.fetchall()
    logs = []
    for r in rows:
        logs.append({
            "timestamp": r[0],
            "editor": r[1],
            "field_changed": r[2],
            "old_value": r[3],
            "new_value": r[4]
        })
    return logs

    