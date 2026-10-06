"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": "Đọc và báo cáo thông tin về tệp và thư mục.",
            "system_prompt": "Bạn là một nhà thám hiểm, nhiệm vụ của bạn là đọc và báo cáo thông tin về tệp và thư mục."
        },
        {
            "name": "implementer",
            "description": "Thực hiện các tác vụ lập trình và phát triển.",
            "system_prompt": "Bạn là một nhà phát triển, nhiệm vụ của bạn là thực hiện các tác vụ lập trình và phát triển."
        },
        {
            "name": "reviewer",
            "description": "Kiểm tra độc lập các tác vụ đã thực hiện.",
            "system_prompt": "Bạn là một người kiểm tra, nhiệm vụ của bạn là kiểm tra độc lập các tác vụ đã thực hiện."
        }
    ]