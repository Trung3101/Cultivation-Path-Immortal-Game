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

SELECT name FROM sqlite_master WHERE type='table';
