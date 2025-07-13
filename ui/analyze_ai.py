# ui/analyze_ai.py

def mock_ai_analyze(description: str) -> dict:
    """
    Mô phỏng AI phân tích dựa trên mô tả vật phẩm.
    Kết quả gồm: tính chất, nguy cơ, khuyến nghị.
    """
    desc_lower = description.lower()

    analysis = {
        "tính_chất": "Không xác định",
        "nguy_cơ": "Không có thông tin nguy hiểm rõ ràng.",
        "khuyến_nghị": "Có thể sử dụng bình thường."
    }

    if "độc" in desc_lower or "kịch độc" in desc_lower:
        analysis["tính_chất"] = "Có độc tính cao"
        analysis["nguy_cơ"] = "Có thể gây hỏng linh căn hoặc tẩu hỏa nhập ma nếu sử dụng không đúng cách."
        analysis["khuyến_nghị"] = "Luyện hóa bằng Thanh Tâm Đan trước khi dùng."

    elif "âm khí" in desc_lower or "hàn" in desc_lower:
        analysis["tính_chất"] = "Mang khí âm"
        analysis["nguy_cơ"] = "Không phù hợp cho người tu dương hệ hoặc chính đạo."
        analysis["khuyến_nghị"] = "Nên phối hợp với công pháp Huyền Âm hoặc luyện khi đạt trạng thái Ngũ Hành Bình Hòa."

    elif "long" in desc_lower or "long khí" in desc_lower:
        analysis["tính_chất"] = "Ẩn chứa khí tức Long Tộc"
        analysis["nguy_cơ"] = "Sử dụng không đúng cách có thể bị Long Hồn phản phệ."
        analysis["khuyến_nghị"] = "Chỉ nên dùng sau khi kích hoạt Long Hồn Chi Mộng."

    elif "phong ấn" in desc_lower:
        analysis["tính_chất"] = "Bị phong ấn"
        analysis["nguy_cơ"] = "Giải ấn sai cách có thể phản phệ hoặc kích hoạt bẫy chú."
        analysis["khuyến_nghị"] = "Dùng pháp bảo Thanh Linh Kết Giới hoặc tìm NPC phong ấn sư."

    elif "trí tuệ" in desc_lower or "hồn khí" in desc_lower:
        analysis["tính_chất"] = "Có hồn trí riêng"
        analysis["nguy_cơ"] = "Có thể bị xâm nhập tâm trí người dùng."
        analysis["khuyến_nghị"] = "Luyện tâm ổn định trước khi sử dụng hoặc thông qua Ảo Cảnh Định Thần."

    return analysis
