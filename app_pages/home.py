import os
import streamlit as st
from PIL import Image
from utils.api import call_gluten_guard_api
from utils.layout import show_logo

import base64

def get_base64_logo():
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Image resize function(images above 500px)
def resize_image(image, max_size=500):
    # Keep the original image if both dimensions are <= 500
    if image.width <= max_size and image.height <= max_size:
        return image

    # Resize while preserving aspect ratio
    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

    return image

# Header with Logo and Two-Tone Title
logo_b64 = get_base64_logo()
if logo_b64:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 14px; margin-top: 4px; margin-bottom: 6px;">
            <img src="data:image/png;base64,{logo_b64}" style="width: 52px; height: 52px; object-fit: contain;" />
            <h1 style="margin: 0; padding: 0; font-size: 2.3rem; font-weight: 800; line-height: 1.1;">
                <span style="color: #f59e0b;">Gluten</span><span style="color: #2563eb;">Guard</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown("# :orange[Gluten]:blue[Guard]")

st.caption("AI-powered gluten-risk assessment for meals. Snap, assess, eat safely.")
st.space("small")

# Photo Input Selection
input_mode = st.segmented_control(
    "Photo input method",
    options=["📁 Upload image", "📷 Take photo", "✨ Sample dishes"],
    default="📁 Upload image",
    label_visibility="collapsed",
)

uploaded_file = None
image_to_process = None

if input_mode == "📁 Upload image":
    uploaded_file = st.file_uploader(
        "Upload a food photo (JPG, PNG, WEBP)",
        type=["jpg", "jpeg", "png", "webp"],
        help="On mobile devices, this opens your photo gallery or camera.",
    )
    if uploaded_file:
        image_to_process = uploaded_file

elif input_mode == "📷 Take photo":
    camera_file = st.camera_input("Take a photo of your meal")
    if camera_file:
        image_to_process = camera_file

elif input_mode == "✨ Sample dishes":
    st.caption("Select a sample dish to test the AI instantly:")
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

# Resize selected image to a maximum of 500 x 500 pixels
if image_to_process is not None:

    if hasattr(image_to_process, "path"):
        # Sample image
        image = Image.open(image_to_process.path)

    else:
        # Uploaded file or camera input
        image = Image.open(image_to_process)

    image = resize_image(image)

    # Store the resized PIL image
    image_to_process = image

st.divider()

# Process image if available
if image_to_process is not None:
    col_img, col_results = st.columns([1, 1.25], gap="large")

    with col_img:
        with st.container(border=True):
            st.markdown("##### Dish photo")

            st.image(
                image_to_process,
                caption=f"Image: loaded successfully",
                width="stretch",
            )

    with col_results:
        with st.spinner("Analyzing dish and assessing risk level..."):
            try:
                api_response = call_gluten_guard_api(image_to_process)
            except Exception as e:
                api_response = None
                st.error(f"API request failed: {e}")

        if api_response and api_response.get("predictions"):
            top = api_response["predictions"][0]
            celiac_risk = top.get("celiac_risk", "Unknown")
            confidence_pct = round(top.get("confidence", 0) * 100)
            contains_gluten = top.get("contains_gluten")
            notes = top.get("notes", "")
            questions = top.get("server_questions", [])

            # Override all fields if confidence is very low (< 15%)
            if confidence_pct < 20:
                celiac_risk = "Unknown"
                contains_gluten = None
                notes = "Not recognised due to low confidence"
                questions = []
                top["label"] = "Unknown"

            gluten_text = "Yes" if contains_gluten is True else ("No" if contains_gluten is False else "Uncertain")

            # -------------------------------------------------------------
            # 1. Dish and risk score
            # -------------------------------------------------------------
            with st.container(border=True):
                head_col1, head_col2 = st.columns([0.55, 0.45], vertical_alignment="center")
                with head_col1:
                    st.caption("IDENTIFIED DISH")
                    dish_name = top.get("label", "Unknown")
                    st.subheader(dish_name)
                    if confidence_pct > 0:
                        st.caption(f":material/verified: AI Confidence: {confidence_pct}%")

                    st.caption(
                        "⚠️ *This is AI driven. Results might be wrong. "
                        "If incorrect, select the correct food category from the Food Categories page.*"
                    )
                    st.page_link(
                        "app_pages/food_categories.py",
                        label="Select correct food category",
                        icon=":material/restaurant_menu:",
                    )

                with head_col2:
                    risk_images = {
                        "High": "assets/risk_score/high.png",
                        "Medium": "assets/risk_score/mid.png",
                        "Mid": "assets/risk_score/mid.png",
                        "Low": "assets/risk_score/low.png",
                        "Unknown": "assets/risk_score/unknown.png",
                    }
                    risk_img_path = risk_images.get(celiac_risk, None)
                    if risk_img_path and os.path.exists(risk_img_path):
                        st.image(risk_img_path, width="stretch")
                    else:
                        st.caption(f"Risk score: {celiac_risk}")

            # -------------------------------------------------------------
            # 2. Celiac risk and contains gluten
            # -------------------------------------------------------------
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

            # -------------------------------------------------------------
            # 3. Risk analysis
            # -------------------------------------------------------------
            with st.container(border=True):
                st.markdown("##### :material/analytics: Risk analysis")
                if notes:
                    st.write(notes)
                else:
                    st.caption("No additional analysis details available.")

            # -------------------------------------------------------------
            # 4. Questions for the restaurant staff
            # -------------------------------------------------------------
            with st.container(border=True):
                st.markdown("##### :material/quiz: Questions for the restaurant staff")
                if questions:
                    for i, q in enumerate(questions, 1):
                        st.markdown(f"**{i}.** {q}")
                else:
                    st.caption("No specific questions generated for this meal.")

        else:
            st.error("No predictions returned from the API.")

else:
    st.info(
        "Upload an image, take a photo, or select a sample dish above to start your assessment.",
        icon=":material/touch_app:",
    )
