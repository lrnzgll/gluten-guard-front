import os
import streamlit as st
from PIL import Image
from utils.mock_api import call_gluten_guard_api

# Friendly Hero Header
st.title("Gluten Guard", icon=":material/shield_with_heart:")
st.subheader("Intelligent dish recognition & Celiac risk assessment", anchor=False)

# Welcoming Explanation Card
with st.container(border=True):
    col_desc, col_link = st.columns([2.5, 1], vertical_alignment="center")
    with col_desc:
        st.markdown(
            "Welcome! **Gluten Guard** is your friendly, intelligent dining companion. "
            "Simply snap or upload a photo of any dish, and our AI will quickly recognize the meal "
            "and calculate a **Gluten Risk Score** to help you navigate restaurant menus safely and confidently."
        )
    with col_link:
        st.page_link(
            "app_pages/how_it_works.py",
            label="How it works →",
            icon=":material/info:",
            width="stretch",
        )

st.markdown("---")

st.markdown("### 📸 Try It Now")
st.caption("Upload a dish photo or take a picture with your mobile camera to test.")

input_mode = st.segmented_control(
    "Choose photo input method:",
    options=["📁 Upload Image", "📷 Take Photo", "✨ Try Sample Dishes"],
    default="📁 Upload Image",
    label_visibility="collapsed",
)

uploaded_file = None
image_to_process = None

if input_mode == "📁 Upload Image":
    uploaded_file = st.file_uploader(
        "Upload a food image (JPG, PNG, WEBP)",
        type=["jpg", "jpeg", "png", "webp"],
        help="On mobile devices, this opens your photo gallery or camera.",
    )
    if uploaded_file:
        image_to_process = uploaded_file

elif input_mode == "📷 Take Photo":
    camera_file = st.camera_input("Take a photo of your meal")
    if camera_file:
        image_to_process = camera_file

elif input_mode == "✨ Try Sample Dishes":
    st.write("Click a sample dish below to test the AI instantly:")
    sample_cols = st.columns(4)

    sample_choice = None
    if sample_cols[0].button("🍝 Carbonara", width="stretch"):
        sample_choice = "carbonara.jpg"
    if sample_cols[1].button("🍕 Pizza", width="stretch"):
        sample_choice = "pizza.jpg"
    if sample_cols[2].button("🐟 Salmon", width="stretch"):
        sample_choice = "salmon.jpg"
    if sample_cols[3].button("🥗 Salad", width="stretch"):
        sample_choice = "salad.jpg"

    if sample_choice:
        class SampleFile:
            def __init__(self, name):
                self.name = name
                self.path = os.path.join("assets", "samples", name)
        image_to_process = SampleFile(sample_choice)
        st.session_state["sample_active"] = sample_choice

    elif "sample_active" in st.session_state:
        class SampleFile:
            def __init__(self, name):
                self.name = name
                self.path = os.path.join("assets", "samples", name)
        image_to_process = SampleFile(st.session_state["sample_active"])

# Process image if available
if image_to_process is not None:
    st.markdown("##")

    # Layout columns: Left for Image Preview, Right for Assessment Results
    col_img, col_results = st.columns([1, 1.3], gap="large")

    with col_img:
        with st.container(border=True):
            st.markdown("#### 🍽️ Submitted Dish")
            try:
                # If real file bytes uploaded or taken via camera
                if hasattr(image_to_process, "getvalue"):
                    img = Image.open(image_to_process)
                    st.image(img, width="stretch")
                # If sample selected and real image file exists in assets/samples/
                elif hasattr(image_to_process, "path") and os.path.exists(image_to_process.path):
                    st.image(image_to_process.path, width="stretch", caption=f"Sample: {image_to_process.name}")
                else:
                    # Fallback if image file is not added yet
                    st.info(
                        f"Sample Selected: **{image_to_process.name}**\n\n"
                        f"*(To show a real photo, place `{image_to_process.name}` inside `assets/samples/`)*",
                        icon=":material/restaurant:",
                    )
            except Exception:
                st.info("Image loaded successfully.")

    with col_results:
        with st.spinner("🤖 Analyzing dish and assessing Celiac risk..."):
            # Call Mock API -> Returns exactly 2 fields: risk_score and text
            api_response = call_gluten_guard_api(image_to_process)

        risk_score = api_response.get("risk_score", 0)
        text = api_response.get("text", "")

        # Determine risk level and color scheme
        if risk_score >= 67:
            risk_color = "#e11d48"
            risk_bg = "#fff1f2"
            risk_label = "HIGH RISK"
            badge_icon = "🚨"
        elif risk_score >= 34:
            risk_color = "#d97706"
            risk_bg = "#fffbeb"
            risk_label = "MODERATE RISK"
            badge_icon = "⚠️"
        else:
            risk_color = "#059669"
            risk_bg = "#f0fdf4"
            risk_label = "LOW RISK"
            badge_icon = "✅"

        # Risk Score Metric Card
        with st.container(border=True):
            st.caption("CELIAC GLUTEN RISK ASSESSMENT")

            # Big visual score badge
            st.markdown(
                f"""
                <div style="background-color: {risk_bg}; border: 1.5px solid {risk_color}; border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 12px;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: {risk_color}; letter-spacing: 0.05em; margin-bottom: 4px;">
                        {badge_icon} {risk_label}
                    </div>
                    <div style="font-size: 2.8rem; font-weight: 800; color: {risk_color}; line-height: 1;">
                        {risk_score}%
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">
                        Estimated Gluten Probability
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Progress bar matching score
            st.progress(risk_score / 100)

    # Detailed Analysis Text Card (Second returned field)
    st.markdown("##")
    with st.container(border=True):
        st.markdown(text)

else:
    st.info("👆 Please upload an image, take a photo, or choose a sample dish above to start.", icon=":material/touch_app:")
