import streamlit as st
import datetime
import time

# --- 1. PAGE CONFIG & CINEMATIC STYLING ---
st.set_page_config(page_title="SleepSync AI", page_icon="🌙", layout="centered")

st.markdown("""
    <style>
    .main {
        background: url("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXByeHlod3B6eGZpZzJueHByeHlod3B6eGZpZzJueHByeHlod3B6eGZpZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKVUn7iM8FMEU24/giphy.gif");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .block-container {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(20px);
        padding: 3rem;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: white;
    }

    .score-glow {
        font-size: 5rem;
        font-weight: 900;
        color: #00f2fe;
        text-shadow: 0 0 30px rgba(0, 242, 254, 0.9);
        text-align: center;
    }

    /* Modern slider/input styling */
    .stSlider [data-baseweb="slider"] { margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'step' not in st.session_state:
    st.session_state.step = 0

def move_next(): st.session_state.step += 1
def move_back(): st.session_state.step -= 1

# --- 3. THE WIZARD ---

# PAGE 0: LANDING
if st.session_state.step == 0:
    st.title("🌙 SleepSync AI")
    st.subheader("Biological Forecasting Engine")
    st.write("We analyze your sleep debt, caffeine pulse, and metabolic load to predict tomorrow's cognitive performance.")
    st.button("Begin Bio-Scan ➔", on_click=move_next)

# PAGE 1: SLEEP DEBT
elif st.session_state.step == 1:
    st.header("📉 Step 1: Sleep Debt")
    st.session_state.prev_sleep = st.slider("Hours slept last night?", 0.0, 12.0, 7.0, 0.5)
    st.button("Next: Digital Habits ➔", on_click=move_next)

# PAGE 2: DIGITAL
elif st.session_state.step == 2:
    st.header("📱 Step 2: Digital Sunset")
    st.session_state.stop_t = st.time_input("Phone Stop Time", datetime.time(21, 30))
    st.session_state.bed_t = st.time_input("Planned Bedtime", datetime.time(23, 0))
    
    col1, col2 = st.columns(2)
    with col1: st.button("⬅ Back", on_click=move_back)
    with col2: st.button("Next: Caffeine ➔", on_click=move_next)

# PAGE 3: CAFFEINE
elif st.session_state.step == 3:
    st.header("☕ Step 3: Caffeine Pulse")
    st.session_state.cups = st.number_input("Caffeine Servings", 0, 10, 1)
    st.session_state.caf_t = st.time_input("Time of Last Intake", datetime.time(15, 0))
    
    col1, col2 = st.columns(2)
    with col1: st.button("⬅ Back", on_click=move_back)
    with col2: st.button("Next: Metabolic Load ➔", on_click=move_next)

# PAGE 4: NUTRITION (NEW)
elif st.session_state.step == 4:
    st.header("🥗 Step 4: Metabolic Load")
    st.write("Food is information. What did your body process last?")
    st.session_state.meal_t = st.time_input("Time of Last Meal", datetime.time(19, 30))
    
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.session_state.sugar = st.checkbox("High Sugar 🍩")
    with col_b: st.session_state.heavy = st.checkbox("Heavy/Fatty 🍔")
    with col_c: st.session_state.spicy = st.checkbox("Spicy 🌶️")

    col1, col2 = st.columns(2)
    with col1: st.button("⬅ Back", on_click=move_back)
    with col2: st.button("Analyze & Predict ✨", on_click=move_next)

# PAGE 5: FINAL PREDICTION
elif st.session_state.step == 5:
    st.title("📊 Predictive Analysis")
    
    with st.spinner("Decoding Bio-Signals..."):
        time.sleep(2)
        
        # --- CALCULATIONS ---
        prod_score = 100
        
        # 1. Sleep Debt Impact
        debt = 8.0 - st.session_state.prev_sleep
        prod_score -= (debt * 10)
        
        # 2. Nutrition Logic
        bed_dt = datetime.datetime.combine(datetime.date.today(), st.session_state.bed_t)
        meal_dt = datetime.datetime.combine(datetime.date.today(), st.session_state.meal_t)
        meal_gap = (bed_dt - meal_dt).total_seconds() / 3600
        
        if meal_gap < 2: prod_score -= 15 # Heavy digestion during sleep
        if st.session_state.sugar: prod_score -= 10 # Insulin spike
        if st.session_state.heavy: prod_score -= 10 # Core temp rise
        
        final_prod = round(max(5, prod_score))

        # --- DISPLAY ---
        st.markdown(f"<div class='score-glow'>{final_prod}%</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>TOMORROW'S PREDICTED EFFICIENCY</p>", unsafe_allow_html=True)
        
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Metabolic Status", "Resting" if meal_gap > 3 else "Active")
        c2.metric("Focus Potential", f"{final_prod}%")
        c3.metric("Sleep Debt", f"{round(debt, 1)}h")

        st.info(f"🧬 **Insight:** You are finishing your meal **{round(meal_gap, 1)} hours** before bed. " + 
                ("Your body will be too busy digesting to fully enter deep sleep." if meal_gap < 3 else "Perfect metabolic timing!"))

    if st.button("🔄 Restart Simulation"):
        st.session_state.step = 0
        st.rerun()