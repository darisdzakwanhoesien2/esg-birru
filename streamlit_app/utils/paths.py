# streamlit_app/utils/paths.py
from pathlib import Path

def get_project_root() -> Path:
    """
    Returns project root:
    esg-birru/
    """
    return Path(__file__).resolve().parents[2]

def get_db_root() -> Path:
    """
    Returns backend/db/json_db
    """
    return get_project_root() / "backend" / "db" / "json_db"
