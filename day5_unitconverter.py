import streamlit as st
from random import choice

# ---------------- Page Config ----------------
st.set_page_config(page_title="Ultra Unit Converter", page_icon="🔄", layout="wide")

# ----------------- Custom CSS -----------------
st.markdown("""
<style>
.big-title {
    background: linear-gradient(90deg, #ff6a00, #ee0979);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    font-weight: 900;
    text-align:center;
    margin-bottom: 1.5rem;
}
.tab-box {
    padding:20px;
    border-radius:15px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🔄 Ultra Unit Converter</div>', unsafe_allow_html=True)
st.caption("Convert **Currency**, **Temperature**, **Length** and **Weight** — with a touch of fun! 🚀")

# ---------------- Conversion Functions ----------------
def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit": return (value * 9/5) + 32
        elif to_unit == "Kelvin":   return value + 273.15
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":    return (value - 32) * 5/9
        elif to_unit == "Kelvin":   return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":    return value - 273.15
        elif to_unit == "Fahrenheit":return (value - 273.15) * 9/5 + 32
    return value

length_units = {
    "Meters":1,"Kilometers":1000,"Centimeters":0.01,"Millimeters":0.001,
    "Miles":1609.34,"Yards":0.9144,"Feet":0.3048,"Inches":0.0254
}
def convert_length(value, from_unit, to_unit):
    meters = value * length_units[from_unit]
    return meters / length_units[to_unit]

weight_units = {
    "Kilograms":1,"Grams":0.001,"Milligrams":1e-6,"Pounds":0.453592,"Ounces":0.0283495
}
def convert_weight(value, from_unit, to_unit):
    kg = value * weight_units[from_unit]
    return kg / weight_units[to_unit]

currency_rates = {"USD":1,"EUR":0.91,"INR":83.24,"GBP":0.79,"JPY":149.62}
def convert_currency(value, from_currency, to_currency):
    usd_value = value / currency_rates[from_currency]
    return usd_value * currency_rates[to_currency]

# -------------- Fun fact messages ------------------
fun_facts = {
    "Temperature":[
        "🔥 Hot tip: Absolute zero is −273.15 °C. Colder than your ex’s heart!",
        "🌡 Fun fact: The human body’s normal temp is about 37 °C."
    ],
    "Length":[
        "📏 Did you know? One mile equals 1.609 kilometers!",
        "🛤 The Great Wall of China is over 21,000 km long!"
    ],
    "Weight":[
        "⚖ An average adult human brain weighs about 1.4 kg.",
        "🥔 Fun fact: The heaviest potato ever grown weighed 4.98 kg!"
    ],
    "Currency":[
        "💱 Did you know? The first paper money was created in China 1,000 years ago!",
        "🪙 Fun fact: The U.S. once printed a $100,000 bill!"
    ]
}

# ---------------- Helper: Tab UI ----------------
def show_converter(tab_key, bg_color, icon, units, convert_func, fact_key, value_format=".2f"):
    """Reusable converter block with a submit button and friendly output."""
    st.markdown(f'<div class="tab-box" style="background-color:{bg_color}">', unsafe_allow_html=True)
    st.subheader(f"{icon} {fact_key} Conversion")
    c1, c2 = st.columns(2)

    with c1:
        from_unit = st.selectbox("From:", list(units.keys()), key=f"{tab_key}_from")
        value = st.number_input("Value:", value=0.0, key=f"{tab_key}_val")
    with c2:
        to_unit = st.selectbox("To:", list(units.keys()), key=f"{tab_key}_to")
        submitted = st.button("Convert", key=f"{tab_key}_btn")

    if submitted:
        result = convert_func(value, from_unit, to_unit)
        st.success(
            f"You entered **{value} {from_unit}**, which equals "
            f"**{format(result, value_format)} {to_unit}**."
        )
        st.info(choice(fun_facts[fact_key]))
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Tabs ----------------
tabs = st.tabs(["🌡 Temperature", "📏 Length", "⚖ Weight", "💱 Currency"])

with tabs[0]:
    temp_units = {"Celsius":1, "Fahrenheit":1, "Kelvin":1}
    def temp_convert(v,f,t): return convert_temperature(v,f,t)
    show_converter("temp", "#FFE5CC", "🌡", temp_units, temp_convert, "Temperature")

with tabs[1]:
    show_converter("len", "#D0F4DE", "📏", length_units, convert_length, "Length", ".4f")

with tabs[2]:
    show_converter("wt", "#FFF3B0", "⚖", weight_units, convert_weight, "Weight", ".4f")

with tabs[3]:
    show_converter("cur", "#C1E1FF", "💱", currency_rates, convert_currency, "Currency")
