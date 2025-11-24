import os
import re
from pathlib import Path
import shutil

PROJECT_ROOT = Path(os.getcwd())

TARGET_PATTERN = r"Path\(__file__\)\.resolve\(\)\.parents\[\d+\]"
SAFE_REPLACEMENT = "Path(os.getcwd())"

# Any additional DB path patterns to normalize
DB_PATTERNS = [
    r"Path\(__file__\)\.resolve\(\)\.parents\[\d+\]\s*/\s*['\"]backend['\"]",
]
DB_REPLACEMENT = "Path(os.getcwd()) / 'backend'"

# Which folders to scan
SCAN_DIRS = [
    PROJECT_ROOT / "streamlit_app",
    PROJECT_ROOT / "backend",
]

def backup_file(file: Path):
    backup = file.with_suffix(file.suffix + ".bak")
    shutil.copy(file, backup)
    return backup

def fix_paths_in_file(file: Path):
    text = file.read_text()
    original = text

    # Fix general __file__ path references
    text = re.sub(TARGET_PATTERN, SAFE_REPLACEMENT, text)

    # Fix backend path references
    for pattern in DB_PATTERNS:
        text = re.sub(pattern, DB_REPLACEMENT, text)

    if text != original:
        backup = backup_file(file)
        file.write_text(text)
        print(f"  ✨ Fixed + backed up: {file}  (backup: {backup})")
        return True
    else:
        print(f"  ✔ No path fixes needed: {file}")
        return False

def run():
    print("\n🚀 FIX-PATH SCRIPT — Starting\n")
    print(f"Working directory: {PROJECT_ROOT}")

    modified = 0
    scanned = 0

    for folder in SCAN_DIRS:
        print(f"\n🔍 Scanning folder: {folder}")
        for file in folder.rglob("*.py"):
            scanned += 1
            if "fix_paths.py" in file.name:
                continue
            if fix_paths_in_file(file):
                modified += 1

    print("\n=======================================")
    print("📦 FIX-PATH SUMMARY")
    print("=======================================")
    print(f"Total files scanned:   {scanned}")
    print(f"Files modified:        {modified}")
    print("---------------------------------------")
    print("Next steps:")
    print("1. Review .bak backup files if needed")
    print("2. Commit & push changes to GitHub")
    print("3. Restart your Streamlit Cloud app")
    print("=======================================\n")


if __name__ == "__main__":
    run()
