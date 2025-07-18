import sqlite3

DB_PATH = "dao_do_items.db"

def get_ingredients_for_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, material_name, quantity, note FROM item_ingredients WHERE item_id = ?", (item_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def add_ingredient(item_id, material_name, quantity, note=""):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO item_ingredients (item_id, material_name, quantity, note) VALUES (?, ?, ?, ?)",
                (item_id, material_name, quantity, note))
    conn.commit()
    conn.close()

def update_ingredient(ingredient_id, material_name, quantity, note=""):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE item_ingredients SET material_name=?, quantity=?, note=? WHERE id=?",
                (material_name, quantity, note, ingredient_id))
    conn.commit()
    conn.close()

def delete_ingredient(ingredient_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM item_ingredients WHERE id=?", (ingredient_id,))
    conn.commit()
    conn.close()
