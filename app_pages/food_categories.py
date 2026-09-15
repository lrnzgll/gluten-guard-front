import os
import streamlit as st
from utils.celiac_db import food101_celiac_db

# Build a sorted list of display labels mapped to key entries
DISPLAY_TO_KEY = {data["label"]: key for key, data in food101_celiac_db.items()}
LABEL_OPTIONS = sorted(list(DISPLAY_TO_KEY.keys()))

# Page Header
st.subheader("Food Categories", anchor=False)
st.caption("Browse all 101 food categories and inspect their Celiac risk assessment, ingredients notes, and server questions.")

st.page_link("app_pages/home.py", label="Back to Home", icon=":material/arrow_back:")

st.space("small")

# Category Selector
st.markdown("### 🔍 Select a Food Category")
selected_label = st.selectbox(
    "Choose a food category from Food-101:",
    options=LABEL_OPTIONS,
    index=None,
    placeholder="Type or select a food category (e.g. Spaghetti carbonara, Pizza...)",
    label_visibility="collapsed",
)

if selected_label:
    key = DISPLAY_TO_KEY[selected_label]
    category_info = food101_celiac_db[key]

    label = category_info.get("label", selected_label)
    celiac_risk = category_info.get("celiac_risk", "Unknown")
    contains_gluten = category_info.get("contains_gluten")
    notes = category_info.get("notes", "")
    questions = category_info.get("server_questions", [])

    gluten_text = "Yes" if contains_gluten is True else ("No" if contains_gluten is False else "Uncertain")

    st.markdown("---")

    col1, col2 = st.columns([1, 1.25], gap="large")

    with col1:
        # 1. Dish and risk score header card
        with st.container(border=True):
            head_col1, head_col2 = st.columns([0.55, 0.45], vertical_alignment="center")
            with head_col1:
                st.caption("SELECTED DISH")
                st.subheader(label)
                st.caption("📚 Food-101 Database Entry")

            with head_col2:
                risk_images = {
                    "High": "assets/risk_score/high.png",
                    "Medium": "assets/risk_score/mid.png",
                    "Mid": "assets/risk_score/mid.png",
                    "Low": "assets/risk_score/low.png",
                }
                risk_img_path = risk_images.get(celiac_risk, None)
                if risk_img_path and os.path.exists(risk_img_path):
                    st.image(risk_img_path, width="stretch")
                else:
                    st.caption(f"Risk score: {celiac_risk}")

    with col2:
        # 2. Celiac Risk & Contains Gluten
        m1, m2 = st.columns(2)
        with m1:
            with st.container(border=True):
                risk_icons = {
                    "High": ":material/warning:",
                    "Medium": ":material/info:",
                    "Mid": ":material/info:",
                    "Low": ":material/check_circle:",
                }
                icon = risk_icons.get(celiac_risk, ":material/help_outline:")
                st.metric(
                    label="Celiac risk",
                    value=f"{icon} {celiac_risk}" if icon else celiac_risk,
                )

        with m2:
            with st.container(border=True):
                gluten_icons = {
                    "Yes": ":material/cancel:",
                    "No": ":material/check_circle:",
                    "Uncertain": ":material/help_outline:",
                }
                g_icon = gluten_icons.get(gluten_text, "")
                st.metric(
                    label="Contains gluten",
                    value=f"{g_icon} {gluten_text}" if g_icon else gluten_text,
                )

        # 3. Risk Analysis
        with st.container(border=True):
            st.markdown("##### :material/analytics: Risk analysis")
            st.write(notes if notes else "No additional analysis details available.")

        # 4. Questions for the restaurant staff
        with st.container(border=True):
            st.markdown("##### :material/quiz: Questions for the restaurant staff")
            if questions:
                for i, q in enumerate(questions, 1):
                    st.markdown(f"**{i}.** {q}")
            else:
                st.caption("No specific questions required for this meal.")

st.divider()

# List of all Food-101 classes
st.markdown("### 📋 All 101 Food Categories")
st.caption("Explore all food classes in our database.")

search_query = st.text_input(
    "Search categories",
    placeholder="Filter categories (e.g. salad, pasta, soup, cake)...",
    icon=":material/search:",
)

filtered_labels = [l for l in LABEL_OPTIONS if search_query.lower() in l.lower()] if search_query else LABEL_OPTIONS

st.caption(f"Showing {len(filtered_labels)} of {len(LABEL_OPTIONS)} categories")

cols = st.columns(3)
for idx, item_label in enumerate(filtered_labels):
    item_key = DISPLAY_TO_KEY[item_label]
    item_data = food101_celiac_db[item_key]
    risk = item_data.get("celiac_risk", "Unknown")

    col = cols[idx % 3]
    with col:
        with st.container(border=True):
            st.write(f"**{idx + 1}. {item_label}**")
            badge_color = ":red[High Risk]" if risk == "High" else (":orange[Medium Risk]" if risk == "Medium" else ":green[Low Risk]")
            st.caption(f"Risk level: {badge_color}")
