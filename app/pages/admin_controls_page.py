import streamlit as st
from pathlib import Path
import sys
import pandas as pd
from app.backend.db import DB
from app.backend.table_object_classes.user import User
from app.backend.table_function_classes.db_user_functions import DBUserFunctions

def handle_add_user(db_functions: DBUserFunctions, row_id_, row):
    user = User.from_row(row)
    if st.session_state['user'].has_higher_privilege(user):
        db_functions.add_user(user)
    else:
        st.error("You are not authorized to add a user of this permission level.")

def handle_remove_user(db_functions: DBUserFunctions, row_id_, row):
    user = User.from_row(row)
    if st.session_state['user'].has_higher_privilege(user):
        db_functions.remove_user(user)
    else:
        st.error("You are not authorized to remove a user of this permission level.")

def handle_edit_user(db_functions: DBUserFunctions, row_id_, row):
    user = User.from_row(rows[row_id_])
    if st.session_state['user'].has_higher_privilege(user):
        user.update_from_row(row)
        db_functions.edit_user(user)
    else:
        st.error("You are not authorized to edit a user of this permission level.")

PAGE_DIR = Path(__file__).resolve().parent
APP_DIR = PAGE_DIR.parent
PROJECT_ROOT = APP_DIR.parent
sys.path.append(str(PROJECT_ROOT))

if not "db" in st.session_state:
    st.session_state["db"] = DB()

if not "user_functions" in st.session_state:
    st.session_state["user_functions"] = DBUserFunctions(st.session_state["db"])
db_user_functions = st.session_state["user_functions"]

st.set_page_config(page_title="Book Management", page_icon="x", layout="wide")
st.title("Admin Controls")
st.caption("Add and remove users, change permissions.")

#home button
if st.button("Back to Home"):
    st.switch_page("pages/home_page.py")

# Sample Data
rows = db.get_printable_table("Users")
if 'base_df' not in st.session_state:
    st.session_state['base_df'] = pd.DataFrame(rows, columns=["ID", "Username", "Email", "Role"])

st.title("User Management")

# Configure the columns
edited_df = st.data_editor(
    st.session_state['base_df'],
    column_config={
        "Role": st.column_config.SelectboxColumn(
            help="Select the user's permission level",
            options=["admin", "user"],
            required=True,
        ),
        "ID": None
    },
    hide_index=True,
    num_rows="dynamic", # This adds a '+' and '-' button to add/delete rows
    key="edited_df"
)

if st.button("Save Changes"):
    changes = st.session_state['edited_df']
    added_users = changes["added_rows"]
    deleted_users = changes["deleted_rows"]
    changed_users = changes["edited_rows"]

    actions = {
        "add": (added_users, handle_add_user),
        "delete": (deleted_users, handle_remove_user),
        "change": (changed_users, handle_edit_user)
    }

    for action_name, (user_group, method) in actions.items():
        for row_id, data in user_group.items():
            method(db_user_functions, row_id, data)