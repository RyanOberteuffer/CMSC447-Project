import streamlit as st


st.set_page_config(page_title="Login", page_icon="x", layout="centered")

#title
st.title("Login")
st.caption("Sign in with your UMBC Google account.")

#home button
if st.button("Back to Home"):
    st.switch_page("pages/home_page.py")

#check if authenticated
auth_configured = hasattr(st.user, "is_logged_in")

if not auth_configured:
    st.warning("Google login is not configured yet.")
    st.code(
        """Create .streamlit/secrets.toml with your Google OAuth settings,
then restart Streamlit.""",
        language="toml"
    )
    st.stop()

if not st.user.is_logged_in:
    st.write("Use Google to sign in.")
    if st.button("Sign in with Google", use_container_width=True):
        st.login()
    st.stop()

email = st.user.get("email", "")
name = st.user.get("name", "User")

# umbc only
if not email.lower().endswith("@umbc.edu"):
    st.error("Access is restricted to UMBC Google accounts.")
    if st.button("Log out", use_container_width=True):
        st.logout()
    st.stop()

st.success(f"Signed in as {name}")
st.write(f"Email: {email}")

col1, col2 = st.columns(2)

with col1:
    if st.button("Continue", use_container_width=True):
        st.switch_page("pages/home_page.py")

with col2:
    if st.button("Log out", use_container_width=True):
        st.logout()