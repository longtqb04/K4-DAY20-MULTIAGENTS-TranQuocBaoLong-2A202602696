"""GUIDE Phần 1 - Dựng tác tử (agent) bằng Deep Agents.   >>> SINH VIÊN CÀI ĐẶT make_backend VÀ build_agent <<<

Pseudo-code: guides/pseudocode/01_agent.md
Kiểm tra:    pytest tests/test_02_agent.py
"""
from pathlib import Path
import os
import shutil
import sys

# TODO 1: import các thành phần cần dùng, ví dụ:
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from .model import make_model
from .subagents import get_subagents

# ---- CÓ SẴN, KHÔNG SỬA: system prompt dùng chung cho mọi sinh viên (để đường cơ sở so sánh được) ----
PATHS_NOTE = (
    "PATHS: every path is relative to the sandbox root and never starts with '/'. "
    "The task files are in the folder workspace/ (for example workspace/app.log). "
    "Use exactly this relative form both in the file tools and in the shell (execute); "
    "the shell starts in the sandbox root. "
)
BASE_PROMPT = (
    "You are an engineering assistant working in a sandbox. "
    + PATHS_NOTE
    + "Use the shell to run Python and tests. "
    "When you are done, reply with a short summary that mentions only files you really created or changed."
)
SKILLS_NOTE = (
    " Skills are in the folder skills/ (one sub-folder per skill with a SKILL.md). "
    "As your FIRST action, read the SKILL.md of every skill whose description could apply to the task, "
    "then follow them. Never modify skills/."
)
SUBAGENTS_NOTE = (
    " You have specialised subagents (see the description of the task tool). "
    "For anything beyond a trivial step, delegate to a suitable subagent and put ALL the task rules and file paths "
    "in the delegation message, because a subagent sees only what you send. "
    "Check what a subagent returns before you rely on it."
)
# --------------------------------------------------------------------------------------------------


def make_backend(sandbox: Path):
    """Tạo backend (môi trường thực thi) cho tác tử.

    Yêu cầu:
      - Thư mục gốc (root_dir) là `sandbox`; đường dẫn tương đối `workspace/...` và `skills/...`
        phải dùng được ở CẢ công cụ tệp lẫn shell (shell chạy với thư mục làm việc = `sandbox`).
      - Tác tử chạy được lệnh shell và gọi được `python` (cần đặt PATH).
      - KHÔNG chuyển biến môi trường của bạn vào shell của tác tử (khóa API không được lộ).
    """
    # Keep the agent shell isolated from the parent process while still making
    # the active Python interpreter and basic shell utilities available.
    path_entries = [str(Path(sys.executable).parent)]
    if os.name == "nt":
        # LocalShellBackend uses cmd.exe on Windows. These utilities provide
        # the Unix-style commands used by the lab tasks and tests.
        git = shutil.which("git")
        if git:
            git_root = Path(git).resolve().parent.parent
            git_usr_bin = git_root / "usr" / "bin"
            if git_usr_bin.is_dir():
                path_entries.append(str(git_usr_bin))
        path_entries.extend([
            os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32"),
            os.environ.get("SystemRoot", r"C:\Windows"),
        ])
    else:
        path_entries.extend(["/usr/local/bin", "/usr/bin", "/bin"])

    env = {
        "PATH": os.pathsep.join(path_entries),
        "HOME": str(sandbox),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    if os.name == "nt" and os.environ.get("SystemRoot"):
        env["SystemRoot"] = os.environ["SystemRoot"]
    return LocalShellBackend(
        root_dir = sandbox,
        virtual_mode = True,
        # ảo, gốc = sandbox
        inherit_env = False,
        # trình cha
        env = env,
        timeout = 120,
    )


def build_agent(sandbox: Path, mode: str = "single", use_skills: bool = False, model=None):
    """Tạo tác tử Deep Agents.

    Tham số:
      sandbox:    thư mục chứa `workspace/` (và `skills/` nếu có).
      mode:       "single"    -> tác tử mặc định (có subagent `general-purpose` sẵn của Deep Agents)
                  "subagents" -> thêm các subagent từ `get_subagents()` (nối PATHS_NOTE vào `system_prompt` của MỖI subagent,
                                 vì subagent không nhận BASE_PROMPT) và thêm SUBAGENTS_NOTE vào prompt chính
      use_skills: True -> nạp thư mục "/skills/" qua tham số `skills=` của create_deep_agent
                  và thêm SKILLS_NOTE vào prompt.
      model:      mô hình ngôn ngữ; None -> dùng `make_model()`.
    mode không hợp lệ -> ném ValueError.
    Trả về: đồ thị (graph) đã biên dịch, gọi bằng `.invoke({"messages": [...]})`.
    """
    if mode not in ["single", "subagents"]:
        raise ValueError(f"Invalid mode: {mode}")

    kwargs = {}
    prompt = BASE_PROMPT

    if mode == "subagents":
        kwargs["subagents"] = [
            {**subagent, "system_prompt": subagent["system_prompt"] + " " + PATHS_NOTE}
            for subagent in get_subagents()
        ]
        prompt += SUBAGENTS_NOTE
    
    if use_skills:
        kwargs["skills"] = ["/skills/"]
        prompt += SKILLS_NOTE

    return create_deep_agent(
        model = model or make_model(),
        system_prompt = prompt,
        backend = make_backend(sandbox),
        **kwargs
    ) 
