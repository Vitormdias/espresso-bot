def generate_espresso_prompt(history, current_data, summary=False):
    prompt = f"""
Você é um especialista em espresso que se baseará nas respostas de James Hoffman, Lance Hedrick e Não Sou Barista

Com base nos dados abaixo, gere uma nova receita de espresso que valorize as notas sensoriais de {current_data['coffee']['taste_notes']}
O café que estou usando é do Brasil, o processo foi {current_data['coffee']['process']},
o nível de torra é {current_data['coffee']['roast']} e as notas de sabor são {current_data['coffee']['taste_notes']}
Eu estou usando uma Gaggia Classi Evo e um moedor 1Zpresso K-Max
Eu quero tomar aproximadamente {current_data['parameters']['yield']} de café
Na minha receita anterior eu senti {current_data['parameters']['feedback']}

Quero que você sugira uma receita ajustes considerando que eu controlo:
Dose (g)
Rendimento (g)
Tempo de extração (s)
Moagem (K-Max)
Tempo de pré-infusão (s)
Mude 1 parâmetro por vez e com base no feedback ajuste
A moagem do meu moedor é no clique número {current_data['parameters']['grind']}
Eu estou fazendo uma pré-infusão de {current_data['parameters']['pre_infusion']} segundos
Eu quero um café que seja {current_data['parameters']['desired_sensory']}

Por favor sintetize sua resposta em uma receita de espresso
"""
    return prompt

def generate_brewers_prompt(history, current_data, summary=False):
    prompt = f"""
Você é um especialista em café que se baseará nas respostas de James Hoffman, Lance Hedrick, Tetsu Kasuya e Não Sou Barista
Com base nos dados abaixo, gere uma nova receita de café coado que valorize as notas sensoriais de {current_data['brew']['taste_notes']}

O café que estou usando foi teve o processo {current_data['brew']['process']}, 
o nível de torra é {current_data['brew']['roast_profile']} e o método de preparo que quero usar é {current_data['brew']['method']}

Eu quero tomar aproximadamente {current_data['brew']['amount']} de café

Na minha receita anterior eu senti {current_data['brew']['feedback']}

Quero que você sugira ajustes considerando que eu controlo:
Dose (g)
Temperatura da água (°C)
Quantidade de despejos
Tempo de infusão (caso o método permita)
Moagem 

Sintetize sua resposta em uma receita de café coado
"""
    return prompt

