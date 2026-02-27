import datetime

def analyze_health_impact(total_usage_h, stop_time_str, bed_time_str, wake_time_str):
    # 1. SETUP & CONVERSIONS
    stop_dt = datetime.datetime.strptime(stop_time_str, "%H:%M")
    bed_dt = datetime.datetime.strptime(bed_time_str, "%H:%M")
    wake_dt = datetime.datetime.strptime(wake_time_str, "%H:%M")
    
    # Handle overnight sleep (if wake time is '07:00' and bed is '23:00')
    if wake_dt < bed_dt:
        wake_dt += datetime.timedelta(days=1)
    
    actual_sleep_h = (wake_dt - bed_dt).total_seconds() / 3600
    gap_before_bed_m = (bed_dt - stop_dt).total_seconds() / 60
    
    score = 100
    insights = []

    # 2. FEATURE: TIME BEFORE SLEEP (Melatonin Analysis)
    # Scientific Average: 2 hours of blue light can suppress melatonin by 50%
    if gap_before_bed_m < 0:
        score -= 40
        insights.append("❌ CRITICAL: You used your phone in bed. This tricks your brain into 'Daytime Mode'.")
    elif gap_before_bed_m < 60:
        score -= 20
        insights.append("⚠️ POOR: Only 1 hour gap. Expect difficulty reaching deep 'Stage 3' sleep.")
    elif gap_before_bed_m >= 120:
        insights.append("✅ EXCELLENT: 2+ hour gap allows your natural melatonin surge to peak.")

    # 3. FEATURE: SLEEP SUFFICIENCY (7-9 Hour Adult Target)
    if actual_sleep_h < 7:
        score -= 15
        sufficiency = f"Insufficient ({actual_sleep_h:.1f}h). Most adults need 7-9 hours."
    else:
        sufficiency = f"Sufficient ({actual_sleep_h:.1f}h). Your body has time for cellular repair."

    # 4. FEATURE: NEXT-DAY FORECAST
    forecast = ""
    if score > 85:
        forecast = "🚀 High Alertness: Expect peak focus and stable mood tomorrow."
    elif score > 60:
        forecast = "⚖️ Moderate: You might feel a 'mid-afternoon slump' or slight irritability."
    else:
        forecast = "📉 Impaired: High risk of 'brain fog', slow reaction times, and sugar cravings."

    return {
        "score": max(0, score),
        "insights": insights,
        "sufficiency": sufficiency,
        "forecast": forecast
    }

# --- USER INPUT ---
print("--- Advanced Sleep & Screen Time Analytics ---")
h = int(input("Total Phone Hours today: "))
m = int(input("Total Phone Minutes today: "))
stop_t = input("Time you stopped using your phone (e.g. 21:30): ")
bed_t = input("Time you went to sleep (e.g. 23:00): ")
wake_t = input("Time you plan to wake up (e.g. 07:00): ")

# --- ANALYSIS ---
results = analyze_health_impact(h + (m/60), stop_t, bed_t, wake_t)

print("\n" + "="*40)
print(f"OVERALL SLEEP QUALITY: {results['score']}/100")
print(f"SLEEP DURATION: {results['sufficiency']}")
print("-" * 40)
for note in results['insights']: print(note)
print("-" * 40)
print(f"TOMORROW'S FORECAST:\n{results['forecast']}")
print("="*40)