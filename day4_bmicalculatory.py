import streamlit as st
from dataclasses import dataclass

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="PyVeeran – Day 4: Advanced BMI Calculator",
    page_icon="🏋",
    layout="centered"
)

# ---------- Dataclass to store result ----------
@dataclass
class BMIResult:
    bmi: float
    category: str
    advice: str

# ---------- Helper Function with match-case ----------
def get_bmi_category(bmi: float) -> BMIResult:
    match bmi:
        case x if x < 18.5:
            return BMIResult(bmi, "Underweight", "Consider a nutrient-rich diet to gain weight.")
        case x if 18.5 <= x < 25:
            return BMIResult(bmi, "Normal", "Great! Maintain your healthy lifestyle.")
        case x if 25 <= x < 30:
            return BMIResult(bmi, "Overweight", "Regular exercise and balanced diet recommended.")
        case _:
            return BMIResult(bmi, "Obese", "Consult a healthcare professional for guidance.")

# ---------- CSS for gradient background (fixed) ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#f5f7fa 0%,#c3cfe2 100%);
}
</style>
""", unsafe_allow_html=True)

# ---------- Tabs for Calculator / Info ----------
tab1, tab2 = st.tabs(["🧮 Calculator", "ℹ️ About BMI"])

with tab1:
    st.title("🏋 Day 4: Advanced BMI Calculator")
    st.write("Enter your height and weight to check your Body Mass Index and get advice.")

    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.1)
    with col2:
        weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1)

    if st.button("💡 Calculate BMI", type="primary"):
        height_m = height / 100
        bmi_value = round(weight / (height_m ** 2), 2)
        result = get_bmi_category(bmi_value)

        st.subheader("📊 Your Results")
        if result.category == "Underweight":
            st.warning(f"**BMI:** {result.bmi} – **{result.category}**")
        elif result.category == "Normal":
            st.success(f"**BMI:** {result.bmi} – **{result.category}**")
        else:
            st.error(f"**BMI:** {result.bmi} – **{result.category}**")

        st.info(result.advice)

        # --- Progress bar representation ---
        st.caption(f"BMI scale (0–40) → Your BMI: {bmi_value}")
        st.progress(min(bmi_value / 40, 1.0))

        # --- Download your result as text file ---
        summary = f"Your BMI: {result.bmi}\nCategory: {result.category}\nAdvice: {result.advice}"
        st.download_button("⬇️ Download Result", summary, file_name="bmi_result.txt")

with tab2:
    st.header("What is BMI?")
    st.write("""
    **Body Mass Index (BMI)** is a simple index of weight-for-height
    that is commonly used to classify underweight, normal weight,
    overweight and obesity in adults.

    **Categories:**
    - Underweight: < 18.5
    - Normal: 18.5 – 24.9
    - Overweight: 25 – 29.9
    - Obese: ≥ 30
    """)
    st.caption("Source: World Health Organization")
