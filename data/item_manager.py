import sqlite3

# Lấy thông tin 1 vật phẩm theo ID
def get_item_by_id(item_id):
    conn = sqlite3.connect("dao_do_items.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cur.fetchone()
    columns = [desc[0] for desc in cur.description]
    conn.close()

    if row:
        return dict(zip(columns, row))
    return None

# Cập nhật thông tin vật phẩm
def update_item(item_id, updates: dict):
    conn = sqlite3.connect("dao_do_items.db")
    cur = conn.cursor()

    # Lấy danh sách cột thực tế trong bảng items
    cur.execute("PRAGMA table_info(items)")
    valid_columns = [row[1] for row in cur.fetchall()]

    # Lọc bỏ các cột không hợp lệ
    filtered_updates = {
        k: v for k, v in updates.items()
        if k in valid_columns and k != "id" and k != "deleted"
    }

    if not filtered_updates:
        conn.close()
        return

    fields = ", ".join(f"{k} = ?" for k in filtered_updates)
    values = list(filtered_updates.values()) + [item_id]

    sql = f"UPDATE items SET {fields} WHERE id = ?"
    cur.execute(sql, values)
    conn.commit()
    conn.close()

# Lấy danh sách tất cả vật phẩm chưa bị xoá
def get_all_items():
    conn = sqlite3.connect("dao_do_items.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE deleted = 0")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    items = []
    for row in rows:
        item_dict = dict(zip(columns, row))
        item_dict.pop("deleted", None)  # bỏ cột deleted khi hiển thị
        items.append(item_dict)

    return items
