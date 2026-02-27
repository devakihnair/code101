import datetime

def analyze_food_impact(eat_time_str, bed_time_str, salt, sugar, fat):
    eat_dt = datetime.datetime.strptime(eat_time_str, "%H:%M")
    bed_dt = datetime.datetime.strptime(bed_time_str, "%H:%M")
    
    # Calculate gap between last meal and sleep
    digest_gap = (bed_dt - eat_dt).total_seconds() / 3600
    
    food_score = 100
    body_effects = []
    
    # 1. Timing Logic (The 3-Hour Rule)
    if digest_gap < 1:
        food_score -= 40
        body_effects.append("🔴 DIGESTION: Your body is digesting instead of resting. Expect high heart rate.")
    elif digest_gap < 3:
        food_score -= 20
        body_effects.append("🟡 METABOLISM: Active digestion is raising your core temp, delaying deep sleep.")
    else:
        body_effects.append("🟢 TIMING: Your stomach is settled. Perfect for rapid sleep onset.")

    # 2. Nutrient Logic (High/Med/Low Poll)
    # Penalties: High = -15, Med = -5, Low = 0
    weights = {"high": 15, "med": 5, "low": 0}
    
    total_nutrient_penalty = weights[salt] + weights[sugar] + weights[fat]
    food_score -= total_nutrient_penalty

    # Health Factor Explanations
    if salt == "high":
        body_effects.append("💧 SALT: High sodium causes dehydration and 'sleep fragmentation' (waking up thirsty).")
    if sugar == "high":
        body_effects.append("⚡ SUGAR: Causes a glucose spike & crash, leading to night sweats or vivid dreams.")
    if fat == "high":
        body_effects.append("🔥 FAT: High-fat meals slow down stomach emptying, increasing risk of acid reflux.")

    return max(0, food_score), body_effects

# --- USER INTERFACE ---
print("--- 🥗 NUTRITION & SLEEP QUALITY POLL ---")
last_meal = input("When was your last meal/snack? (HH:MM): ")
bed_time = input("When are you going to sleep? (HH:MM): ")

print("\nQuick Poll: Rate your last meal:")
s_salt = input("Salt level (high/med/low): ").lower()
s_sugar = input("Sugar level (high/med/low): ").lower()
s_fat = input("Fat level (high/med/low): ").lower()

f_score, f_effects = analyze_food_impact(last_meal, bed_time, s_salt, s_sugar, s_fat)

print("\n" + "═"*45)
print(f"DIETARY SLEEP SCORE: {f_score}/100")
print("═"*45)
print("BODY IMPACT ANALYSIS:")
for effect in f_effects:
    print(effect)
print("═"*45)