import streamlit as st
import datetime
import time

# --- 1. PAGE CONFIG & LIVELY STYLING ---
st.set_page_config(page_title="SleepSync AI", page_icon="🌙", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #2e1065, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .cloud {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 20px;
        margin: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        text-align: center;
        transition: 0.5s;
    }
    .cloud:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.15);
    }

    .score-glow {
        font-size: 6rem;
        font-weight: 900;
        color: #00f2fe;
        text-shadow: 0 0 30px rgba(0, 242, 254, 0.8);
        animation: pulse 2s infinite;
        text-align: center;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.08); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }

    .stButton>button {
        width: 100%;
        border-radius: 30px;
        height: 3.5em;
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
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
    st.markdown("<h1 style='text-align: center; color: white;'>🌙 SleepSync AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8;'>Advanced Circadian Analysis</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='cloud'>☕ <b>Bio-Fact:</b> Caffeine has a half-life of 5-6 hours. That 4PM coffee is still 50% there at 10PM!</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='cloud'>📱 <b>Bio-Fact:</b> Blue light blocks melatonin, the 'vampire hormone' that needs darkness.</div>", unsafe_allow_html=True)
    
    st.button("Start Bio-Analysis ➔", on_click=move_next)

# PAGE 1: DIGITAL
elif st.session_state.step == 1:
    st.markdown("### 📱 Step 1: Digital Sunset")
    st.session_state.stop_t = st.time_input("When did you last use your phone?", datetime.time(21, 30))
    st.session_state.bed_t = st.time_input("Planned Bedtime", datetime.time(23, 0))
    st.session_state.wake_t = st.time_input("Wakeup Time", datetime.time(7, 0))
    
    st.button("Next: Caffeine Intake ➔", on_click=move_next)

# NEW PAGE 2: CAFFEINE
elif st.session_state.step == 2:
    st.markdown("### ☕ Step 2: Caffeine Levels")
    st.session_state.cups = st.slider("Cups of Coffee/Energy Drinks today", 0, 8, 1)
    st.session_state.caf_t = st.time_input("Time of your LAST caffeine intake", datetime.time(15, 0))
    
    col_a, col_b = st.columns(2)
    with col_a: st.button("⬅ Back", on_click=move_back)
    with col_b: st.button("Next: Nutrition ➔", on_click=move_next)

# PAGE 3: NUTRITION
elif st.session_state.step == 3:
    st.markdown("### 🥗 Step 3: Nutrition Poll")
    st.session_state.sugar = st.select_slider("Sugar Intake", ["low", "med", "high"])
    st.session_state.salt = st.select_slider("Salt Intake", ["low", "med", "high"])
    st.session_state.fat = st.select_slider("Fat Intake", ["low", "med", "high"])
    
    col_a, col_b = st.columns(2)
    with col_a: st.button("⬅ Back", on_click=move_back)
    with col_b: st.button("Generate My Report ✨", on_click=move_next)

# PAGE 4: RESULTS
elif st.session_state.step == 4:
    st.markdown("<h1 style='text-align: center;'>📊 Bio-Sync Report</h1>", unsafe_allow_html=True)
    
    with st.spinner("Calculating Caffeine Decay..."):
        time.sleep(1.5)
        
        # --- LOGIC ---
        bed_dt = datetime.datetime.combine(datetime.date.today(), st.session_state.bed_t)
        stop_dt = datetime.datetime.combine(datetime.date.today(), st.session_state.stop_t)
        caf_dt = datetime.datetime.combine(datetime.date.today(), st.session_state.caf_t)
        
        # 1. Screen Gap
        gap_h = (bed_dt - stop_dt).total_seconds() / 3600
        
        # 2. Caffeine Decay (Half-life)
        # Residual = (Cups * 95mg) * 0.5 ^ (HoursSinceLastCup / 5.5)
        hours_since_caf = (bed_dt - caf_dt).total_seconds() / 3600
        if hours_since_caf < 0: hours_since_caf += 24
        residual_mg = (st.session_state.cups * 95) * (0.5 ** (hours_since_caf / 5.5))
        
        # 3. Nutrition
        weights = {"high": 12, "med": 5, "low": 0}
        nut_penalty = weights[st.session_state.sugar] + weights[st.session_state.salt] + weights[st.session_state.fat]

        # Scoring Logic
        score = 100
        if gap_h < 1: score -= 25
        if residual_mg > 50: score -= 20
        elif residual_mg > 100: score -= 40
        score -= nut_penalty
        final_score = round(max(0, score))

        # --- UI ---
        st.markdown(f"<div class='score-glow'>{final_score}%</div>", unsafe_allow_html=True)
        
        st.write(f"### ☕ Caffeine Analysis")
        st.progress(min(residual_mg/200, 1.0))
        st.write(f"Estimated **{round(residual_mg)}mg** of caffeine still in your blood at bedtime.")
        
        st.write("### 🧬 Biological Insight")
        if residual_mg > 80:
            st.error("Caffeine levels are high. It blocks **Adenosine**, the chemical that signals sleepiness to your brain.")
        else:
            st.success("Caffeine levels are low enough for natural sleep onset.")

    if st.button("🔄 Restart"):
        st.session_state.step = 0
        st.rerun()