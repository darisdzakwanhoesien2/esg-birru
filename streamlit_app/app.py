# streamlit_app/app.py
"""
Hybrid router for Streamlit app (Option C).
This file handles:
 - session initialisation
 - login check
 - dynamic page router + sidebar navigation filtered by roles
"""

import streamlit as st
from importlib import import_module
from pathlib import Path
from utils.auth_utils import (
    ensure_session,
    is_logged_in,
    get_current_user,
    require_roles_for_page,
)
from utils.data_access import load_json

# Map friendly names to module paths (pages have run(st) entrypoint)
PAGES = {
    "Login": "streamlit_app.pages.01_Login",
    "Dashboard": "streamlit_app.pages.02_Dashboard",
    "Assessment (Level 1)": "streamlit_app.pages.03_Company_Assessment_Level1",
    "Assessment (Level 2)": "streamlit_app.pages.04_Company_Assessment_Level2",  # placeholder exists later
    "Upload Document": "streamlit_app.pages.05_Document_Uploader",
    "OCR Processor": "streamlit_app.pages.06_OCR_Processor",
    "Media Checker": "streamlit_app.pages.07_Media_Checker",  # later batch
    "Graph Explorer": "streamlit_app.pages.08_Graph_Explorer",  # later batch
    "Reports (L1)": "streamlit_app.pages.09_Reports_Level1",  # later batch
    "Reports (L2)": "streamlit_app.pages.10_Reports_Level2",  # later batch
    "Aggregator Overview": "streamlit_app.pages.11_Aggregator_Company_Overview",
    "Question Editor (Admin)": "streamlit_app.pages.12_Admin_Question_Editor",
    "User Manager (Admin)": "streamlit_app.pages.13_Admin_User_Manager",
    "Industry Clustering": "streamlit_app.pages.14_Industry_Clustering",
    "API Diagnostics": "streamlit_app.pages.15_API_Diagnostics",
}

DATA_PATH = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"

def import_and_run(module_path, st=st):
    try:
        mod = import_module(module_path)
        if hasattr(mod, "run"):
            mod.run(st)
        else:
            st.error(f"Module {module_path} missing run(st) function.")
    except Exception as e:
        st.exception(e)

def main():
    ensure_session()

    st.set_page_config(page_title="Certify App", layout="wide")
    st.title("Certify — Compliance & Certification Platform")

    # show a small top bar with user info
    if is_logged_in():
        user = get_current_user()
        st.sidebar.markdown(f"**Logged in as:** {user['email']}")
        st.sidebar.markdown(f"**Roles:** {', '.join(user['roles'])}")
    else:
        st.sidebar.markdown("**Not logged in**")

    # Build navigation items filtered by RBAC
    nav_items = []
    for name, module in PAGES.items():
        # allow Login always
        if name == "Login" or require_roles_for_page(name, get_current_user()):
            nav_items.append(name)

    # Sidebar navigation
    st.sidebar.header("Navigation")
    choice = st.sidebar.radio("Go to", nav_items, index=(0 if not is_logged_in() else 1))

    # Quick logout
    if is_logged_in():
        if st.sidebar.button("Logout"):
            from utils.auth_utils import logout
            logout()
            st.experimental_rerun()

    # Load the chosen page module and run it
    module_path = PAGES.get(choice)
    if module_path:
        import_and_run(module_path)
    else:
        st.error("Page not found")

if __name__ == "__main__":
    main()
