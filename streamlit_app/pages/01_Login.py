# streamlit_app/pages/01_Login.py
import streamlit as st
from utils.auth_utils import login, is_logged_in, get_current_user

def run(st=st):
    st.header("Sign in")

    if is_logged_in():
        user = get_current_user()
        st.success(f"Already signed in as {user['email']}")
        if st.button("Go to Dashboard"):
            st.experimental_rerun()
        return

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in")
        if submitted:
            ok = login(email.strip(), password)
            if ok:
                st.success("Login successful")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
    st.markdown("---")
    st.info("Use your company account to sign in. Admin credentials are available in the seed DB.")
