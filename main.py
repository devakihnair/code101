import streamlit as st
import usercaff
import screentime
import food
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="SleepSync AI", page_icon="🌙", layout="wide")

# --- 2. DYNAMIC STYLING (Lively & Attractive) ---
st.markdown("""
    <style>
    /* Animated Gradient Background */
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
    
    /* Glassmorphism Design */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00f2fe;
    }

    /* Pulsing Score Animation */
    .score-glow {
        font-size: 5rem;
        font-weight: 900;
        color: #00f2fe;
        text-shadow: 0 0 25px rgba(0, 242, 254, 0.8);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 4em;
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        color: white;
        font-weight: bold;
        border: none;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. NAVIGATION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- 4. PAGE 1: LANDING PAGE ---
if st.session_state.page == 'landing':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 4rem;'>🌙 SleepSync</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.5rem; opacity: 0.8;'>Synchronize your habits. Optimize your rest.</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Let's Start"):
            st.session_state.page = 'dashboard'
            st.rerun()

# --- 5. PAGE 2: DASHBOARD ---
else:
    st.title("📊 SleepSync Analyzer")
    
    # Input Sidebar
    with st.sidebar:
        st.header("📋 Daily Log")
        with st.expander("☕ Caffeine & Time", expanded=True):
            cups = st.number_input("Cups of coffee today?", 0, 10, 2)
            intake_t = st.text_input("Time of last cup (HH:MM)", "16:15")
            bed_t = st.text_input("Planned bedtime (HH:MM)", "23:15")
        
        with st.expander("📱 Digital & Food"):
            usage_h = st.number_input("Phone usage (Hours)", 0, 24, 4)
            stop_t = st.text_input("Phone stop time (HH:MM)", "21:30")
            wake_t = st.text_input("Wakeup time (HH:MM)", "07:00")
            meal_t = st.text_input("Last meal time (HH:MM)", "20:45")
            salt = st.selectbox("Salt level", ["low", "med", "high"])
            sugar = st.selectbox("Sugar level", ["low", "med", "high"])
            fat = st.selectbox("Fat level", ["low", "med", "high"])

        if st.button("Analyze Quality"):
            st.session_state.analyzed = True

    # Analysis Results
    if st.session_state.get('analyzed'):
        with st.spinner("Calculating Bio-metrics..."):
            time.sleep(1) # Visual effect
            
            # Logic Execution from your files
            caf = usercaff.assess_sleep_quality(cups, intake_t, bed_t)
            scr = screentime.analyze_health_impact(usage_h, stop_t, bed_t, wake_t)
            nut_score, nut_effects = food.analyze_food_impact(meal_t, bed_t, salt, sugar, fat)
            
            # Final Composite Score
            final_score = (caf['score'] + scr['score'] + nut_score) / 3

            # Score Display
            st.markdown(f"<div style='text-align: center;'><h1 class='score-glow'>{round(final_score)}%</h1><p>Projected Sleep Quality</p></div>", unsafe_allow_html=True)
            
            # Metric Card Grid
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<div class='metric-card'><h3>☕ Caffeine</h3><h2>{caf['score']}%</h2><p>{caf['residual_mg']} mg at bedtime</p></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='metric-card'><h3>📱 Screen</h3><h2>{scr['score']}%</h2><p>{scr['sufficiency']}</p></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='metric-card'><h3>🥗 Nutrition</h3><h2>{nut_score}%</h2><p>{len(nut_effects)} impacts noted</p></div>", unsafe_allow_html=True)

            # Insights
            st.divider()
            st.subheader("🔊 Expected Breathing Pattern & Expert Advice")
            st.info(caf['feedback'])
            for note in scr['insights']: st.write(f"- {note}")
            for effect in nut_effects: st.write(f"- {effect}")
    else:
        st.info("Fill out your log in the sidebar and click 'Analyze Quality' to begin.")

    if st.button("Return Home"):
        st.session_state.page = 'landing'
        st.rerun()