import streamlit as st
import datetime
import time

# --- 1. PAGE CONFIG & CINEMATIC STYLING ---
st.set_page_config(page_title="SleepSync AI", page_icon="🌙", layout="centered")

# CSS for Animated Background and Glassmorphism
st.markdown("""
    <style>
    /* Fixed Video/GIF Background */
    .main {
        background: url("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXByeHlod3B6eGZpZzJueHByeHlod3B6eGZpZzJueHByeHlod3B6eGZpZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKVUn7iM8FMEU24/giphy.gif");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Content Container with Glass Blur */
    .block-container {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(15px);
        padding: 3rem;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }

    .score-glow {
        font-size: 5rem;
        font-weight: 900;
        color: #00f2fe;
        text-shadow: 0 0 30px rgba(0, 242, 254, 0.9);
        text-align: center;
        margin: 20px 0;
    }

    .stButton>button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white; border: none; border-radius: 20px; font-weight: bold;
    }
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
    st.write("Your biology meets data science. Let's predict your peak performance.")
    st.info("💡 Pro-Tip: A consistent wake-up time is more important than a consistent bedtime.")
    st.button("Start Bio-Scan ➔", on_click=move_next)

# PAGE 1: PREVIOUS NIGHT (NEW PAGE)
elif st.session_state.step == 1:
    st.header("📉 Step 1: Sleep Debt")
    st.session_state.prev_sleep = st.slider("How many hours did you sleep LAST night?", 0.0, 12.0, 7.0, 0.5)
    st.markdown(f"**Current Sleep Debt:** {max(0.0, 8.0 - st.session_state.prev_sleep)} hours")
    
    col1, col2 = st.columns(2)
    with col1: st.button("⬅ Back", on_click=move_back)
    with col2: st.button("Next: Digital Habits ➔", on_click=move_next)

# PAGE 2: DIGITAL
elif st.session_state.step == 2:
    st.header("📱 Step 2: Digital Sunset")
    st.session_state.stop_t = st.time_input("Phone Stop Time", datetime.time(21, 30))
    st.session_state.bed_t = st.time_input("Planned Bedtime Today", datetime.time(23, 0))
    
    col1, col2 = st.columns(2)
    with col1: st.button("⬅ Back", on_click=move_back)
    with col2: st.button("Next: Caffeine ➔", on_click=move_next)

# PAGE 3: CAFFEINE
elif st.session_state.step == 3:
    st.header("☕ Step 3: Caffeine Pulse")
    st.session_state.cups = st.number_input("Coffee/Tea Cups", 0, 10, 2)
    st.session_state.caf_t = st.time_input("Last Cup Time", datetime.time(15, 0))
    
    col1, col2 = st.columns(2)
    with col1: st.button("⬅ Back", on_click=move_back)
    with col2: st.button("Analyze & Predict ✨", on_click=move_next)

# PAGE 4: RESULTS & PREDICTIONS
elif st.session_state.step == 4:
    st.title("📊 Predictive Analysis")
    
    with st.spinner("Simulating Metabolic Pathways..."):
        time.sleep(2)
        
        # --- CALCULATIONS ---
        # 1. Productivity Prediction Logic
        # Start at 100%, subtract for sleep debt and caffeine crashes
        prod_score = 100
        debt = 8.0 - st.session_state.prev_sleep
        prod_score -= (debt * 10) # 10% drop per hour of debt
        
        # 2. Caffeine Crash Prediction
        # If caffeine is taken late, productivity spikes then crashes tomorrow
        bed_dt = datetime.datetime.combine(datetime.date.today(), st.session_state.bed_t)
        caf_dt = datetime.datetime.combine(datetime.date.today(), st.session_state.caf_t)
        gap_caf = (bed_dt - caf_dt).total_seconds() / 3600
        if gap_caf < 6: prod_score -= 15 # "The Caffeine Hangover"
        
        final_prod = round(max(5, prod_score))

        # --- UI DISPLAY ---
        st.markdown(f"<div class='score-glow'>{final_prod}%</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>PREDICTED TOMORROW'S PRODUCTIVITY</p>", unsafe_allow_html=True)
        
        st.divider()
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.write("### 🧠 Cognitive State")
            if final_prod > 85: st.success("Peak Focus: High neuroplasticity.")
            elif final_prod > 60: st.warning("Moderate: Potential brain fog at 3 PM.")
            else: st.error("Low: High reliance on stimulants expected.")

        with col_res2:
            st.write("### 🔋 Recovery Level")
            st.write(f"Sleep Debt: **{round(debt, 1)} hrs**")
            st.write(f"System Load: **{'High' if st.session_state.cups > 3 else 'Normal'}**")

    if st.button("🔄 New Simulation"):
        st.session_state.step = 0
        st.rerun()