import os
import re
from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent
STREAMLIT_DIR = PROJECT_ROOT / "streamlit_app"
PAGES_DIR = STREAMLIT_DIR / "pages"
UTILS_DIR = STREAMLIT_DIR / "utils"

REQUIRED_INIT_FILES = [
    STREAMLIT_DIR / "__init__.py",
    PAGES_DIR / "__init__.py",
    UTILS_DIR / "__init__.py",
]

# Patterns to replace
REPLACEMENTS = {
    r"from utils\.": "from streamlit_app.utils.",
    r"import utils\.": "import streamlit_app.utils.",
    r"from data_access": "from streamlit_app.utils.data_access",
    r"import data_access": "from streamlit_app.utils import data_access",
    r"from streamlit_app\.pages\.": "from streamlit_app.pages.",
}

def ensure_init_files():
    print("🔧 Ensuring __init__.py files exist...")
    for path in REQUIRED_INIT_FILES:
        if not path.exists():
            print(f"  ➕ Creating {path}")
            path.write_text("")  # empty file
        else:
            print(f"  ✔ {path} exists")

def fix_imports_in_file(filepath: Path):
    text = filepath.read_text()
    original = text

    for pattern, replacement in REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text)

    if text != original:
        backup = filepath.with_suffix(".bak")
        shutil.copy(filepath, backup)
        filepath.write_text(text)
        print(f"  ✨ Fixed imports in: {filepath}")
    else:
        print(f"  ✔ No changes needed: {filepath}")

def scan_and_fix_imports():
    print("\n🔧 Scanning for Python files...")
    for py_file in STREAMLIT_DIR.rglob("*.py"):
        if "fix_imports.py" in py_file.name:
            continue
        fix_imports_in_file(py_file)

def report_structure():
    print("\n📁 PROJECT STRUCTURE CHECK\n")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"- streamlit_app exists: {STREAMLIT_DIR.exists()}")
    print(f"- pages exists:         {PAGES_DIR.exists()}")
    print(f"- utils exists:         {UTILS_DIR.exists()}")
    print("\nFiles inside streamlit_app:")
    for p in STREAMLIT_DIR.glob("*"):
        print("  -", p.name)
    print("\nPython files found:")
    for p in STREAMLIT_DIR.rglob("*.py"):
        print("  -", p)

def main():
    print("\n🚀 STARTING AUTO-FIX SCRIPT\n")
    report_structure()
    ensure_init_files()
    scan_and_fix_imports()
    print("\n✅ Auto-fix completed!")
    print("👉 Commit all changes and redeploy on Streamlit Cloud.")


if __name__ == "__main__":
    main()
