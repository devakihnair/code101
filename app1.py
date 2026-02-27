import streamlit as st
import datetime
import time

# --- 1. PAGE CONFIG & LIVELY STYLING ---
st.set_page_config(page_title="SleepSync AI", page_icon="🌙", layout="centered")

st.markdown("""
    <style>
    /* Animated Space Background */
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

    /* Floating Cloud Styling */
    .cloud {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 50px;
        padding: 20px;
        margin: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        text-align: center;
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    /* Pulsing Score Glow */
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

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        height: 4em;
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0, 242, 254, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE FOR NAVIGATION ---
if 'step' not in st.session_state:
    st.session_state.step = 0

def move_next(): st.session_state.step += 1
def move_back(): st.session_state.step -= 1

# --- 3. MULTI-PAGE WIZARD ---

# PAGE 0: LANDING PAGE WITH FUN FACT CLOUDS
if st.session_state.step == 0:
    st.markdown("<br><h1 style='text-align: center; color: white; font-size: 4rem;'>🌙 SleepSync</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.3rem; opacity: 0.8;'>Synchronize Habits. Master your Rest.</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='cloud'>☁️ <b>Fun Fact:</b> Humans are the only mammals that willingly delay sleep!</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='cloud' style='animation-delay: 1s;'>☁️ <b>Did you know?</b> Blue light suppresses melatonin for up to 2 hours!</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Let's Start Analysis ➔", on_click=move_next)

# PAGE 1: DIGITAL HABITS & DURATION
elif st.session_state.step == 1:
    st.header("📱 Step 1: Digital Habits")
    st.session_state.usage_h = st.number_input("Total Phone Hours today", 0, 24, 4)
    st.session_state.stop_t = st.time_input("Phone Stop Time", datetime.time(21, 30))
    st.session_state.bed_t = st.time_input("Planned Bedtime", datetime.time(23, 0))
    st.session_state.wake_t = st.time_input("Wakeup Time", datetime.time(7, 0))
    
    st.button("Next: Nutrition Poll ➔", on_click=move_next)

# PAGE 2: NUTRITION POLL
elif st.session_state.step == 2:
    st.header("🥗 Step 2: Nutrition Poll")
    st.session_state.meal_t = st.time_input("Last Meal Time", datetime.time(20, 0))
    st.session_state.sugar = st.select_slider("Sugar Intake Level", ["low", "med", "high"])
    st.session_state.salt = st.select_slider("Salt Intake Level", ["low", "med", "high"])
    st.session_state.fat = st.select_slider("Fat Intake Level", ["low", "med", "high"])
    
    col_a, col_b = st.columns(2)
    with col_a: st.button("⬅ Back", on_click=move_back)
    with col_b: st.button("Generate My Report ✨", on_click=move_next)

# PAGE 3: ATTRACTIVE RESULT PAGE
elif st.session_state.step == 3:
    st.markdown("<h1 style='text-align: center;'>📊 Your Sleep Report</h1>", unsafe_allow_html=True)
    
    with st.spinner("Processing bio-signals..."):
        time.sleep(2)
        
        # --- CALCULATION LOGIC ---
        bed_dt = datetime.datetime.combine(datetime.date.today(), st.session_state.bed_t)
        stop_dt = datetime.datetime.combine(datetime.date.today(), st.session_state.stop_t)
        gap_h = (bed_dt - stop_dt).total_seconds() / 3600
        
        # Nutrition Penalty
        weights = {"high": 15, "med": 5, "low": 0}
        nut_penalty = weights[st.session_state.sugar] + weights[st.session_state.salt] + weights[st.session_state.fat]
        
        # Scoring
        score = 100
        if gap_h < 1: score -= 30
        elif gap_h < 2: score -= 15
        score -= nut_penalty
        final_score = round(max(0, score))

        # --- ANIMATED RESULT UI ---
        st.markdown(f"<div class='score-glow'>{final_score}%</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold; letter-spacing: 2px;'>SLEEP QUALITY SCORE</p>", unsafe_allow_html=True)
        
        st.divider()
        
        if final_score > 80:
            st.balloons()
            st.success("🌟 **REMARK:** Perfect synchronization! Your melatonin surge is optimal.")
        elif final_score > 50:
            st.warning("⚖️ **REMARK:** Average. Your habits are likely fragmenting your sleep stages.")
        else:
            st.error("📉 **REMARK:** Poor. Your body is likely in 'Daytime Mode' due to blue light or heavy digestion.")

        st.write("### 🧬 Biological Insights")
        st.write(f"- Your screen-free gap is **{round(gap_h, 1)} hours**. Humans need ~2 hours to peak melatonin production.")
        st.write("- **Digestion:** Heavy nutrients can raise core temp, delaying the onset of deep REM sleep.")
        
                
    if st.button("🔄 Restart Analysis"):
        st.session_state.step = 0
        st.rerun()