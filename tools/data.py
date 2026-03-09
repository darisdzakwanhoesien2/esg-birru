import sys
from pathlib import Path

# ==================================================
# CONFIG
# ==================================================
ROOT = Path(__file__).resolve().parents[1]
CODEBASE_ROOT = ROOT / "codebase"
DOCS_ROOT = ROOT / "docs"

EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    "node_modules",
    "extracted",
    "docs",
}

EXCLUDE_FILES = {
    ".DS_Store",
}

TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".txt",
    ".csv",
    ".toml",
    ".ini",
    ".env",
}

# ==================================================
# HELPERS
# ==================================================
def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def should_skip(path: Path) -> bool:
    if path.name in EXCLUDE_FILES:
        return True
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def fence_for_extension(ext: str) -> str:
    return {
        ".py": "python",
        ".json": "json",
        ".md": "markdown",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".csv": "csv",
        ".toml": "toml",
        ".ini": "ini",
        ".txt": "",
    }.get(ext.lower(), "")


# ==================================================
# MAIN LOGIC
# ==================================================
def dump_codebase(codebase_name: str):
    codebase_path = CODEBASE_ROOT / codebase_name

    if not codebase_path.exists():
        raise FileNotFoundError(f"❌ Codebase not found: {codebase_path}")

    out_dir = DOCS_ROOT / codebase_name
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "code_dump.md"

    lines = []
    lines.append(f"# 📦 Full Code Dump — `{codebase_name}`\n")
    lines.append("> Auto-generated snapshot of the entire codebase\n")
    lines.append("---\n")

    for path in sorted(codebase_path.rglob("*")):
        if path.is_dir():
            continue
        if should_skip(path):
            continue
        if not is_text_file(path):
            continue

        rel_path = path.relative_to(codebase_path)
        ext = path.suffix.lower()
        fence = fence_for_extension(ext)

        lines.append(f"## 📁 `{rel_path}`\n")

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(errors="ignore")

        lines.append(f"```{fence}")
        lines.append(content.rstrip())
        lines.append("```")
        lines.append("")

    out_file.write_text("\n".join(lines), encoding="utf-8")

    print(f"✅ Full codebase dumped to {out_file}")


# ==================================================
# CLI
# ==================================================
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/dump_codebase_to_markdown.py <codebase_name>")
        sys.exit(1)

    dump_codebase(sys.argv[1])