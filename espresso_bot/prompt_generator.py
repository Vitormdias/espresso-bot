def format_historico(historico):
    ultimos = historico[-3:] if len(historico) >= 3 else historico
    historico_texto = "\n".join([
        f"- Café: {e['cafe']['origem']}, Processo: {e['cafe']['processo']}, Torra: {e['cafe']['torra']}, "
        f"Desejado: A:{e['resultado_desejado']['perfil_sensorial']['acidez']}, D:{e['resultado_desejado']['perfil_sensorial']['dulcor']}, Am:{e['resultado_desejado']['perfil_sensorial']['amargor']} -> "
        f"Real: A:{e['resultado_real']['sensorial_real']['acidez']}, D:{e['resultado_real']['sensorial_real']['dulcor']}, Am:{e['resultado_real']['sensorial_real']['amargor']}"
        for e in ultimos
    ])
    return historico_texto

def gerar_prompt(historico, dados_atuais):
    historico_texto = format_historico(historico)
    prompt = f"""
Você é um especialista em espresso. Com base nos dados abaixo, gere uma nova receita de espresso que se aproxime do perfil sensorial desejado.
Histórico recente:
{historico_texto}
Novo café:
Origem: {dados_atuais['cafe']['origem']}
Processo: {dados_atuais['cafe']['processo']}
Torra: {dados_atuais['cafe']['torra']}
Sensorial desejado: {dados_atuais['resultado_desejado']['sensorial']}
Perfil desejado: Acidez: {dados_atuais['resultado_desejado']['perfil_sensorial']['acidez']}, Dulçor: {dados_atuais['resultado_desejado']['perfil_sensorial']['dulcor']}, Amargor: {dados_atuais['resultado_desejado']['perfil_sensorial']['amargor']}
Sugira:
Dose (g)
Yield (g)
Tempo de extração (s)
Moagem (K-Max)
Tempo de pré-infusão (s)
Sensorial esperado (acidez, dulçor, amargor)
"""
    return prompt
