import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

ROLE_ADMIN = "Admin"
ROLE_GENERAL = "General"

ROLES = [ROLE_ADMIN, ROLE_GENERAL]

def login():

    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)

    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

item_1 = st.Page("general/blog.py",
    title="Blog Writer",
    icon=":material/help:",
    default=(role == "Requester"),
)

item_2 = st.Page(
    "general/marketingstrategy.py",
    title="Marketing Strategy",
    icon=":material/help:",
)

item_3 = st.Page(
    "admin/code_analyzer.py",
    title="Codebase Analyzer",
    icon=":material/help:",
    default=(role == "Admin"),
)

item_4 = st.Page("admin/adminitem1.py",
    title="Google Gemini",
    icon=":material/help:",

)

account_pages = [logout_page, settings]
request_pages = [item_1, item_2]
admin_pages = [item_3, item_4]

st.logo("images/icon_blue.png", icon_image="images/icon_blue.png")

page_dict = {}
if st.session_state.role == ROLE_ADMIN:
    page_dict[ROLE_ADMIN] = admin_pages
if st.session_state.role in [ROLE_GENERAL, ROLE_ADMIN]:
    page_dict[ROLE_GENERAL] = request_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()