def generate_prompt(history, current_data, language="en", summary=False):
    prompt = f"""
You are an espresso expert. Based on the data below, generate a new espresso recipe that matches the desired sensory profile.
Consider that the equipement beeing use is a Gaggia Classi Evo and a 1Zpresso K-Max Grinder
The grinder has adjustments of 22 microns per click, and the espresso range is between the clicks 20 and 35

New coffee:
Process: {current_data['coffee']['process']}
Roast: {current_data['coffee']['roast']}
Desired sensory: {current_data['desired_result']['sensory']}

Suggest:
Dose (g)
Yield (g)
Extraction time (s)
Grind (K-Max)
Pre-infusion time (s)
Language: {language}
"""
    return prompt
