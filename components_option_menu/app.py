# How to Run this App:
# cd components_option_menu
# pipenv run streamlit run app.py

import streamlit as st
from streamlit_option_menu import option_menu

# 1. Sidebar menu
# icons: https://icons.getbootstrap.com/
with st.sidebar:
    selected = option_menu(
        menu_title="Menu Menu",
        options=["Home", "Projects", "Upload", "Task", "Contact", "Settings"],
        icons=["house", "book", "upload", "list-check", "envelope", "gear"],
    )

# 2. Horizontal menu
# selected = option_menu(
#     menu_title="Menu Menu",
#     options=["Home", "Projects", "Upload", "Task", "Contact", "Settings"],
#     icons=["house", "book", "upload", "list-check", "envelope", "gear"],
#     orientation="horizontal",
# )

if selected == "Home":
    st.title(f"You have selected {selected}")
elif selected == "Projects":
    st.title(f"You have selected {selected}")
elif selected == "Upload":
    st.title(f"You have selected {selected}")
elif selected == "Task":
    st.title(f"You have selected {selected}")
elif selected == "Contact":
    st.title(f"You have selected {selected}")
elif selected == "Settings":
    st.title(f"You have selected {selected}")
