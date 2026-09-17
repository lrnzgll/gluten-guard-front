import streamlit as st

st.markdown(
     """
     <style>
     /* Main app background */
     .stApp {
        background-color: #EFEDE7;
     }

     /* Main content area */
     .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
     }
     </style>
     """,
     unsafe_allow_html=True,
)


st.set_page_config(
    page_title="GlutenGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

page = st.navigation(
    [
        st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
        st.Page(
            "app_pages/food_categories.py",
            title="Food Categories",
            icon=":material/restaurant_menu:",
        ),
        st.Page(
            "app_pages/how_it_works.py",
            title="How It Works",
            icon=":material/help_outline:",
        ),
    ],
    position="top",
)

st.markdown(
    """
    <style>
    /* Top navigation background */
    [data-testid="stHeader"] {
        background-color: #FFF3D8;
    }

    /* Navigation container */
    [data-testid="stHeader"] [data-testid="stToolbar"] {
        background-color: #FFF3D8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
page.run()
