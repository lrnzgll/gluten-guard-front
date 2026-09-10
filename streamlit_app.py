import streamlit as st

st.set_page_config(
    page_title="Gluten Guard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

page = st.navigation(
    [
        st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
        st.Page(
            "app_pages/how_it_works.py",
            title="How It Works",
            icon=":material/help_outline:",
        ),
    ],
    position="top",
)

page.run()
