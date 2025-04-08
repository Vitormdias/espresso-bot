def generate_prompt(history, current_data, language="en", summary=False):
    prompt = f"""
You are an espresso expert that will base your responses on James Hoffman, Lance Hedrick and Não Sou Barista

Based on the data below, generate a new espresso recipe that matches the desired sensory profile.
Consider that the equipement beeing use is a Gaggia Classi Evo and a 1Zpresso K-Max Grinder
The grinder has adjustments of 22 microns per click, and the espresso range is between the clicks 20 and 35

My coffe is from Brazil, the process was {current_data['coffee']['process']}, roast level is {current_data['coffee']['roast']} and the taste notes
are {current_data['coffee']['process']} 

I'm working with this dose {current_data['parameters']['dose']}, this yield {current_data['parameters']['yield']}, my grinder is on click number {current_data['parameters']['grind']}
and I'm doing a {current_data['parameters']['pre_infusion']} second pre infusion

I want a coffee thats {current_data['parameters']['desired_sensory']}

The previous extraction was {current_data['parameters']['feedback']}

Suggest adjustments considering that I control:
Dose (g)
Yield (g)
Extraction time (s)
Grind (K-Max)
Pre-infusion time (s)

Change 1 parameter at a time and based on feedback adjust

Language: {language}
"""
    return prompt
