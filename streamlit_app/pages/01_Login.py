import streamlit as st
from streamlit_app.utils.auth_utils import login, is_logged_in, get_current_user

def run(st=st):
    st.header("Sign in")

    if is_logged_in():
        user = get_current_user()
        st.success(f"Logged in as {user['email']}")
        return

    with st.form("login_form"):
        email = st.text_input("Email", value="admin@certify.com")
        password = st.text_input("Password", type="password", value="")
        submitted = st.form_submit_button("Sign in")

    if submitted:
        success = login(email, password)

        if success:
            st.success("Login successful")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

            # 🔎 SHOW DEBUG INFO
            st.subheader("Debug info")
            st.json({
                "input_email": email,
                "input_password": password,
                "expected_password": st.session_state.get("_DEBUG_EXPECTED"),
                "password_match": st.session_state.get("_DEBUG_PASSWORD_OK"),
                "users_loaded": st.session_state.get("_DEBUG_USERS"),
                "reason": st.session_state.get("_DEBUG_REASON"),
            })


# # streamlit_app/pages/01_Login.py

# import streamlit as st
# from streamlit_app.utils.auth_utils import login, is_logged_in, get_current_user

# def run(st=st):
#     st.header("Sign in")

#     # If already logged in, show status
#     if is_logged_in():
#         user = get_current_user()
#         st.success(f"Logged in as {user['email']}")
#         st.info("Use the sidebar to navigate.")
#         return

#     # --- Login form ---
#     with st.form("login_form", clear_on_submit=False):
#         email = st.text_input("Email", value="")
#         password = st.text_input("Password", type="password", value="")
#         submitted = st.form_submit_button("Sign in")

#     # --- Handle submit ---
#     if submitted:
#         success = login(email.strip(), password)

#         if success:
#             st.success("Login successful")
#             st.experimental_rerun()
#         else:
#             st.error("Invalid credentials")


# # streamlit_app/pages/01_Login.py
# import streamlit as st
# from streamlit_app.utils.auth_utils import login, is_logged_in, get_current_user

# def run(st=st):
#     st.header("Sign in")

#     if is_logged_in():
#         user = get_current_user()
#         st.success(f"Already signed in as {user['email']}")
#         if st.button("Go to Dashboard"):
#             st.experimental_rerun()
#         return

#     with st.form("login_form"):
#         email = st.text_input("Email")
#         password = st.text_input("Password", type="password")
#         submitted = st.form_submit_button("Sign in")
#         if submitted:
#             ok = login(email.strip(), password)
#             if ok:
#                 st.success("Login successful")
#                 st.experimental_rerun()
#             else:
#                 st.error("Invalid credentials")
#     st.markdown("---")
#     st.info("Use your company account to sign in. Admin credentials are available in the seed DB.")
