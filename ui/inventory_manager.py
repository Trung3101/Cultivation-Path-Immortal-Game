# ui/inventory_manager.py
import os
import json

# Thứ tự cấp bậc và phẩm chất
RANK_ORDER = [
    "Phàm", "Nhân", "Vương", "Hoàng", "Huyền", "Địa", "Thiên", "Tiên",
    "Thiên Đạo", "Đại Đạo", "Chí Tôn", "Vũ Trụ", "Hỗn Nguyên", "Vô", "Căn Nguyên", "Kết Thúc"
]

TIER_ORDER = ["hạ", "trung", "thượng", "cực"]

class InventoryManager:
    def __init__(self, username):
        self.username = username.lower()
        self.filename = f"data/inventory_{self.username}.json"
        self.max_slots = 25  # Mặc định 25 ô
        self.items = []

        self.load_inventory()

    def load_inventory(self):
        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists(self.filename):
            self.items = []
            self.save_inventory()
        else:
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.items = data.get("items", [])
                    self.max_slots = data.get("max_slots", 25)
                except:
                    self.items = []
                    self.max_slots = 25

    def save_inventory(self):
        data = {
            "items": self.items,
            "max_slots": self.max_slots
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def sort_items(self):
        def sort_key(item):
            rank = item.get("rank", "Phàm")
            tier = item.get("tier", "hạ")
            rank_index = RANK_ORDER.index(rank) if rank in RANK_ORDER else 0
            tier_index = TIER_ORDER.index(tier) if tier in TIER_ORDER else 0
            return rank_index * 10 + tier_index

        self.items.sort(key=sort_key)
        self.save_inventory()

    def add_item(self, new_item):
        # Nếu item stack được (có quantity)
        for item in self.items:
            if item["id"] == new_item["id"] and "quantity" in item:
                item["quantity"] += new_item.get("quantity", 1)
                self.sort_items()
                return True

        # Nếu là item mới, cần kiểm tra slot
        if len(self.items) >= self.max_slots:
            return False  # Không đủ ô

        self.items.append(new_item)
        self.sort_items()
        return True

    def get_items(self):
        return self.items

    def expand_slots(self, amount):
        self.max_slots += amount
        self.save_inventory()
