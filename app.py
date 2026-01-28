import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FarmEco Professional", 
    page_icon="🌱", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. CSS STYLING ENGINE ---
def local_css():
    st.markdown(
        """
        <style>
        .stApp { background-color: #f8f9fa; color: #333333; }
        section[data-testid="stSidebar"] { background-color: #0e3b28; }
        section[data-testid="stSidebar"] * { color: white !important; }
        .stButton > button {
            background-color: #0e3b28 !important; 
            color: white !important;
            border-radius: 10px;
            border: none;
            padding: 10px 24px;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #1b5e20 !important; 
            transform: scale(1.05);
        }
        .dashboard-card {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #e6e6e6;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            height: 100%;
        }
        .seasonal-banner {
            background: linear-gradient(135deg, #0e3b28 0%, #1b5e20 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-top: 30px;
            box-shadow: 0 4px 15px rgba(14, 59, 40, 0.3);
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 2rem;}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. DATA LOADER (FIXED PATH) ---
@st.cache_data
def load_data():
    try:
        # This points to the 'data' folder seen in your screenshot
        df = pd.read_csv("large_agri_dataset.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        return None

df = load_data()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("FarmEco Pro 🚀")
st.sidebar.markdown("---")

if "page" not in st.session_state:
    st.session_state.page = "Home"

menu = st.sidebar.radio(
    "Select Module:", 
    ["Home", "Market Analytics (Real AI)", "AgroWaste (Smart Reuse)", "CarbonCredit (Income Calc)"],
    key="page"
)

# --- 5. MAIN LOGIC ---

# ================= HOME =================
if menu == "Home":
    local_css()
    
    def switch_page(page_name):
        st.session_state.page = page_name

    st.markdown("<h2 style='color: #0e3b28;'>Dashboard Overview</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; margin-bottom: 30px;'>Welcome back, Farmer. Here is your daily farming summary.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">📉</div>
            <h3 style="margin: 0; color: #333; font-size: 1.2rem;">Price Alerts</h3>
            <p style="color: #666; font-size: 0.9rem; margin-top: 10px;">
                Current Rice prices are trending upwards. Check the AI forecast now.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Check Forecast ➡️", key="btn_market", on_click=switch_page, args=("Market Analytics (Real AI)",))

    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">🌱</div>
            <h3 style="margin: 0; color: #333; font-size: 1.2rem;">Carbon Credits</h3>
            <p style="color: #666; font-size: 0.9rem; margin-top: 10px;">
                Your practices could yield <strong>₹12,000</strong>. Calculate now.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Calculate Earnings ➡️", key="btn_carbon", on_click=switch_page, args=("CarbonCredit (Income Calc)",))

    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">♻️</div>
            <h3 style="margin: 0; color: #333; font-size: 1.2rem;">Waste Reuse</h3>
            <p style="color: #666; font-size: 0.9rem; margin-top: 10px;">
                Don't burn corn husks! Find profitable eco-friendly solutions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Get Ideas ➡️", key="btn_waste", on_click=switch_page, args=("AgroWaste (Smart Reuse)",))

    st.markdown("""
    <div class="seasonal-banner">
        <h2 style="color: white; margin-top: 0;">Seasonal Advice 🌦️</h2>
        <p style="font-size: 1.1rem; opacity: 0.9; max-width: 800px;">
            Monsoon is expected to start in 12 days. We recommend reinforcing your storage silos 
            and moving your harvested grain to a dry environment immediately.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    with st.expander("📖 Click to Read Monsoon Preparation Guide"):
        st.markdown("""
        ### 🌧️ Official Monsoon Advisory
        **1. Storage Safety:**
        * Inspect silos for cracks before rain starts.
        * Use **hermetic bags** (airtight) to prevent moisture.
        
        **2. Field Drainage:**
        * Clear all drainage channels to avoid waterlogging.
        * Create raised beds for vegetables like Tomato and Chili.
        
        **3. Disease Prevention:**
        * High humidity causes fungal growth. Spray **Neem Oil** preemptively.
        """)

# ================= MODULE 1: MARKET ANALYTICS =================
elif menu == "Market Analytics (Real AI)":
    local_css()
    st.header("📈 Market Analytics & Prediction")
    
    if df is None:
        st.error("🚨 Error: Could not find 'data/large_agri_dataset.csv'. Please check your file structure.")
        st.stop()

    crop_list = df['Crop'].unique()
    selected_crop = st.selectbox("Select Crop to Analyze", crop_list)
    
    crop_df = df[df['Crop'] == selected_crop].copy()
    crop_df = crop_df.sort_values("Date")
    
    st.subheader(f"📊 5-Year Price History: {selected_crop}")
    st.line_chart(crop_df.set_index("Date")["Price"])
    
    crop_df['DayIndex'] = crop_df['Date'].map(datetime.datetime.toordinal)
    X = crop_df[['DayIndex']]
    y = crop_df['Price']
    
    model = LinearRegression()
    model.fit(X, y)
    
    st.write("---")
    st.subheader("🤖 AI Price Prediction & Advisory")
    
    col_input, col_pred = st.columns(2)
    
    with col_input:
        last_known_price = crop_df["Price"].iloc[-1]
        current_price = st.number_input(
            f"Enter Current Market Price for {selected_crop} (₹/kg):", 
            value=float(last_known_price),
            step=0.50
        )
        days_ahead = st.slider("Forecast Horizon (Days):", 1, 30, 7)

    future_date = datetime.date.today() + datetime.timedelta(days=days_ahead)
    future_day_index = np.array([[future_date.toordinal()]])
    predicted_price = model.predict(future_day_index)[0]
    
    with col_pred:
        st.metric(
            label=f"AI Forecast for {future_date}", 
            value=f"₹ {predicted_price:.2f}",
            delta=f"{predicted_price - current_price:.2f} vs Today"
        )
    
    st.write("### 📢 System Recommendation")
    change_percent = ((predicted_price - current_price) / current_price) * 100
    
    if change_percent > 5:
        st.success(f"🚀 **HOLD!** Prices are expected to RISE by {change_percent:.1f}% in the next {days_ahead} days.")
    elif change_percent < -5:
        st.error(f"📉 **SELL NOW!** Prices are expected to FALL by {abs(change_percent):.1f}%. Don't wait.")
    else:
        st.info(f"⚖️ **NEUTRAL.** Market is stable ({change_percent:.1f}% change). You can sell or hold.")

# ================= MODULE 2: AGRO WASTE =================
elif menu == "AgroWaste (Smart Reuse)":
    local_css()
    st.header("♻️ AgroWaste: Smart Reuse Recommendations")
    
    waste_type = st.selectbox(
        "Select Farm Waste Material:",
        ["Rice Straw", "Wheat Husk", "Cow Dung", "Vegetable Peels", "Dry Leaves", "Corn Cobs"]
    )
    
    if st.button("Get Eco-Friendly Solution"):
        st.write("---")
        st.subheader(f"♻️ Best Usage for {waste_type}:")
        
        if waste_type == "Rice Straw":
            st.success("🍄 **Mushroom Cultivation:** Perfect bed for Oyster Mushrooms.")
            st.info("🔥 **Bio-Briquettes:** Compress for eco-fuel.")
        elif waste_type == "Wheat Husk":
            st.success("🐮 **Cattle Feed:** Mix with molasses for fodder.")
        elif waste_type == "Cow Dung":
            st.success("⚡ **Biogas Plant:** Generate electricity and cooking gas.")
            st.info("🪱 **Vermicompost:** Turn into organic fertilizer.")
        elif waste_type == "Vegetable Peels":
            st.success("🌱 **Organic Compost:** Nitrogen-rich soil additive.")
        elif waste_type == "Dry Leaves":
            st.success("🍂 **Mulching:** Retain soil moisture.")
        elif waste_type == "Corn Cobs":
            st.success("🔥 **Industrial Fuel:** High calorific value for boilers.")

# ================= MODULE 3: CARBON CREDIT =================
elif menu == "CarbonCredit (Income Calc)":
    local_css()
    st.header("🌍 CarbonCredit: Income Advisor")
    
    col1, col2 = st.columns(2)
    with col1:
        farm_size = st.number_input("Farm Size (Acres)", 1.0, 100.0, 5.0)
        farming_type = st.selectbox("Farming Method", ["Organic (Chemical Free)", "Conventional"])
    with col2:
        trees = st.number_input("Trees Planted", 0, 5000, 50)
        
    if st.button("Calculate Potential Income"):
        st.write("---")
        
        soil_credits = farm_size * (1.0 if farming_type == "Organic (Chemical Free)" else 0.5)
        tree_credits = trees / 100
        total_credits = soil_credits + tree_credits
        income = total_credits * 1000 
        
        st.info(f"🌿 **Total Carbon Credits:** {total_credits:.2f}")
        st.success(f"💰 **Estimated Annual Income:** ₹ {income:,.2f}")