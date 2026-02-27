import math
from datetime import datetime

def assess_sleep_quality(cups_of_coffee, intake_time_str, bedtime_str):
    """
    Assesses sleep quality based on caffeine half-life.
    - cups_of_coffee: Number of standard cups (~95mg each)
    - intake_time_str: Time of last cup (e.g., "15:30")
    - bedtime_str: Intended time to sleep (e.g., "23:00")
    """
    # 1. Configuration
    MG_PER_CUP = 95
    HALF_LIFE = 5.5  # Hours
    
    # 2. Convert string times to datetime objects
    fmt = "%H:%M"
    t_intake = datetime.strptime(intake_time_str, fmt)
    t_bedtime = datetime.strptime(bedtime_str, fmt)
    
    # Calculate time difference in hours
    delta_t = (t_bedtime - t_intake).total_seconds() / 3600
    
    if delta_t < 0:
        # If intake was after bedtime (e.g., intake at 01:00 AM, bedtime at 23:00)
        # We assume it was 24 hours minus the difference
        delta_t += 24

    # 3. Calculate Residual Caffeine at Bedtime
    total_initial_mg = cups_of_coffee * MG_PER_CUP
    residual_mg = total_initial_mg * (0.5 ** (delta_t / HALF_LIFE))
    
    # 4. Sleep Quality Scoring Logic
    # 0mg residual = 100% Quality. Every 10mg reduces quality by roughly 5%
    quality_score = 100 - (residual_mg * 0.5)
    quality_score = max(0, min(100, quality_score)) # Keep between 0-100
    
    # 5. Generate Assessment Feedback
    if quality_score > 85:
        feedback = "Excellent. Caffeine is mostly cleared. Expect deep 'Meditation-style' breathing."
    elif quality_score > 60:
        feedback = "Moderate impact. You might experience lighter sleep cycles and higher heart rate."
    else:
        feedback = "High impact. Caffeine will likely block deep sleep stages (N3)."

    return {
        "residual_mg": round(residual_mg, 2),
        "score": round(quality_score, 1),
        "feedback": feedback
    }

# --- Example Usage ---
cups = int(input("How many cups of coffee did you have? "))
time_last = input("What time was your last cup (HH:MM)? ")
sleep_time = input("What time do you plan to sleep (HH:MM)? ")

result = assess_sleep_quality(cups, time_last, sleep_time)

print(f"\n--- Sleep Quality Report ---")
print(f"Residual Caffeine: {result['residual_mg']} mg")
print(f"Sleep Quality Score: {result['score']}%")
print(f"Expert Advice: {result['feedback']}")
