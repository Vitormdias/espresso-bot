def format_history(history):
    last_entries = history[-3:] if len(history) >= 3 else history
    history_text = "\n".join([
        f"- Coffee: {e['coffee']['process']}, Roast: {e['coffee']['roast']}, "
        f"Desired: A:{e['desired_result']['sensory_profile']['acidity']}, S:{e['desired_result']['sensory_profile']['sweetness']}, B:{e['desired_result']['sensory_profile']['bitterness']} -> "
        f"Actual: A:{e['actual_result']['actual_sensory']['acidity']}, S:{e['actual_result']['actual_sensory']['sweetness']}, B:{e['actual_result']['actual_sensory']['bitterness']}"
        for e in last_entries
    ])
    return history_text

def generate_prompt(history, current_data):
    history_text = format_history(history)
    prompt = f"""
You are an espresso expert. Based on the data below, generate a new espresso recipe that matches the desired sensory profile.
Recent history:
{history_text}
New coffee:
Process: {current_data['coffee']['process']}
Roast: {current_data['coffee']['roast']}
Desired sensory: {current_data['desired_result']['sensory']}
Desired profile: Acidity: {current_data['desired_result']['sensory_profile']['acidity']}, Sweetness: {current_data['desired_result']['sensory_profile']['sweetness']}, Bitterness: {current_data['desired_result']['sensory_profile']['bitterness']}
Suggest:
Dose (g)
Yield (g)
Extraction time (s)
Grind (K-Max)
Pre-infusion time (s)
Expected sensory (acidity, sweetness, bitterness)
"""
    return prompt
