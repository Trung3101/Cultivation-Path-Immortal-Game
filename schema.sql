-- Bảng chính chứa thông tin vật phẩm
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    rank TEXT,
    description TEXT,
    effect TEXT,
    origin TEXT,
    icon TEXT,
    stackable INTEGER,
    usable INTEGER,
    craftable INTEGER,
    rarity TEXT,
    price INTEGER,
    require_level INTEGER,
    require_gender TEXT,
    class_restriction TEXT
);

-- Bảng chứa nguyên liệu chế tạo
CREATE TABLE IF NOT EXISTS item_ingredients (
    item_id TEXT,
    ingredient_id TEXT,
    quantity INTEGER,
    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (ingredient_id) REFERENCES items(id)
);

-- Bảng nâng cấp vật phẩm
CREATE TABLE IF NOT EXISTS item_upgrades (
    item_id TEXT,
    upgrade_to TEXT,
    requirements TEXT,
    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (upgrade_to) REFERENCES items(id)
);

SELECT * FROM items WHERE id = 'Item_sword_001';

--------------------------------------------------------------------------
-- Túi đồ người chơi
CREATE TABLE IF NOT EXISTS player_items (
    player_id TEXT,
    item_id TEXT,
    quantity INTEGER
);

-- Nguyên liệu nâng cấp
CREATE TABLE IF NOT EXISTS item_ingredients (
    recipe_id TEXT,
    ingredient_id TEXT,
    quantity INTEGER
);

-- Cây nâng cấp
CREATE TABLE IF NOT EXISTS item_upgrades (
    item_id TEXT,
    upgrade_to TEXT,
    note TEXT
);

-- Thưởng nhiệm vụ
CREATE TABLE IF NOT EXISTS quest_rewards (
    quest_id TEXT,
    reward_id TEXT,
    quantity INTEGER
);

-- Bảng chính items đầy đủ (kèm deleted)
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    name TEXT,
    type TEXT,
    rank TEXT,
    description TEXT,
    effect TEXT,
    origin TEXT,
    icon TEXT,
    stackable INTEGER,
    usable INTEGER,
    craftable INTEGER,
    ingredients TEXT,
    rarity TEXT,
    price INTEGER,
    require_level INTEGER,
    require_gender TEXT,
    class_restriction TEXT,
    deleted INTEGER DEFAULT 0
);

SELECT name FROM sqlite_master WHERE type='table';
--------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS item_edit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    editor TEXT,
    timestamp TEXT,
    field_changed TEXT,
    old_value TEXT,
    new_value TEXT
);
--------------------------------------------------------------------------
CREATE TABLE item_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT,
    material_name TEXT,
    quantity INTEGER,
    note TEXT,
    FOREIGN KEY (item_id) REFERENCES items(id)
);
--------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
