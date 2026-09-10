import streamlit as st

# Main header for How It Works
st.subheader("How Gluten Guard Works", anchor=False)
st.caption("A quick look inside our AI-powered dish recognition & Celiac risk assessment pipeline.")

st.markdown("---")

# Navigation link back to Home
st.page_link("app_pages/home.py", label="← Back to Home & Try Now", icon=":material/arrow_back:")

st.markdown("##")

# Step 1: CNN & Food-101
col_text1, col_img1 = st.columns([1.1, 0.9], gap="large", vertical_alignment="center")

with col_text1:
    st.markdown("### 1. Fine-tuned CNN Dish Recognition")
    st.write(
        "When you snap or upload a photo of your meal, Gluten Guard feeds the image into a "
        "**fine-tuned Convolutional Neural Network (CNN)** trained on the **Food-101 dataset** "
        "(over 101,000 food images spanning 101 diverse culinary categories)."
    )
    st.info(
        "💡 **Did you know?** Food-101 allows our vision model to identify dishes like *Pasta Carbonara*, "
        "*Pho*, *Ramen*, or *Risotto* in milliseconds—even with complex garnishes and varied lighting.",
        icon=":material/lightbulb:",
    )

with col_img1:
    with st.container(border=True):
        st.caption("📷 **AI Dish Detection Preview**")
        # Visual mock plate representation
        st.markdown(
            """
            <div style="position: relative; background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%); padding: 24px; border-radius: 12px; text-align: center; border: 1px solid #e2e8f0;">
                <div style="font-size: 80px; line-height: 1; margin-bottom: 12px; filter: drop-shadow(0px 8px 12px rgba(0,0,0,0.1));">🍝</div>
                <div style="display: inline-block; background-color: #059669; color: white; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    ✓ Detected: Pasta Carbonara <span style="opacity: 0.85; font-size: 0.8rem; font-weight: 400;">(98.4%)</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("##")

# Step 2: Risk Assessment Engine
col_img2, col_text2 = st.columns([0.9, 1.1], gap="large", vertical_alignment="center")

with col_img2:
    with st.container(border=True):
        st.caption("🛡️ **Ingredient & Risk Matrix**")
        st.markdown(
            """
            <div style="background-color: #fff1f2; border: 1px solid #fecdd3; padding: 18px; border-radius: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 700; color: #9f1239;">Celiac Risk Level</span>
                    <span style="background-color: #e11d48; color: white; font-weight: 700; padding: 2px 10px; border-radius: 12px; font-size: 0.85rem;">88% HIGH</span>
                </div>
                <div style="font-size: 0.85rem; color: #881337; line-height: 1.5;">
                    ⚠️ Contains traditional wheat semolina pasta.<br/>
                    ⚠️ Potential flour thickener in egg mixture.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with col_text2:
    st.markdown("### 2. Ingredient & Risk Assessment")
    st.write(
        "Once the dish is identified, Gluten Guard evaluates its **primary ingredients** and "
        "known culinary preparation methods against a comprehensive **Celiac & Gluten Risk Index**."
    )
    st.write(
        "It flags obvious sources (wheat, barley, rye) as well as **hidden gluten vectors** "
        "(soy sauce, roux thickeners, shared pasta water, and shared fryer oils)."
    )

st.markdown("##")

# Step 3: Precise Restaurant Questions
col_text3, col_img3 = st.columns([1.1, 0.9], gap="large", vertical_alignment="center")

with col_text3:
    st.markdown("### 3. Dish-Specific Restaurant Inquiries")
    st.write(
        "Instead of generic questions, Gluten Guard equips you with **precise, dish-tailored questions** "
        "to ask your server or chef before ordering."
    )
    st.write(
        "This empowers Celiac and gluten-sensitive diners to communicate clearly, "
        "prevent cross-contamination, and enjoy eating out with confidence."
    )

with col_img3:
    with st.container(border=True):
        st.caption("💬 **Actionable Questions for Server**")
        st.markdown(
            """
            <ul style="padding-left: 18px; font-size: 0.9rem; color: #334155; line-height: 1.6;">
                <li>Is gluten-free pasta boiled in a <strong>dedicated clean pot</strong>?</li>
                <li>Is the sauce thickened with flour or cornstarch?</li>
                <li>Are preparation surfaces cleaned between orders?</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# Call to Action at bottom
st.container(border=True).markdown(
    """
    <div style="text-align: center; padding: 12px;">
        <h3 style="margin-top:0;">Ready to test your meal?</h3>
        <p style="color: #64748b;">Upload or capture a dish photo right now on the home page.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.page_link(
        "app_pages/home.py",
        label="Try Gluten Guard Now",
        icon=":material/rocket_launch:",
        width="stretch",
    )
