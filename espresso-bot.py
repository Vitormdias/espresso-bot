import streamlit as st
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

# Caminho do banco de dados local
DB_PATH = "espressos.json"

# Carrega o histórico
def carregar_historico():
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Salva nova entrada
def salvar_entrada(data):
    historico = carregar_historico()
    historico.append(data)
    with open(DB_PATH, "w") as f:
        json.dump(historico, f, indent=2)

# Gera o prompt com base no histórico
def gerar_prompt(historico, dados_atuais):
    ultimos = historico[-3:] if len(historico) >= 3 else historico
    historico_texto = "\n".join([
        f"- Café: {e['cafe']['origem']}, Processo: {e['cafe']['processo']}, Torra: {e['cafe']['torra']}, "
        f"Desejado: A:{e['resultado_desejado']['perfil_sensorial']['acidez']}, D:{e['resultado_desejado']['perfil_sensorial']['dulcor']}, Am:{e['resultado_desejado']['perfil_sensorial']['amargor']} -> "
        f"Real: A:{e['resultado_real']['sensorial_real']['acidez']}, D:{e['resultado_real']['sensorial_real']['dulcor']}, Am:{e['resultado_real']['sensorial_real']['amargor']}"
        for e in ultimos
    ])
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
# Envia para o modelo
def obter_resposta(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Interface Web
st.title("Espresso Bot com IA")
st.header("1. Informações do Café")
origem = st.text_input("Origem do café")
processo = st.selectbox("Processo", ["Natural", "Lavado", "Honey", "Outro"])
torra = st.selectbox("Perfil de torra", ["Clara", "Média Clara", "Média Escura", "Escura"])
st.header("2. Parâmetros iniciais")
dose = st.number_input("Dose (g)", step=0.1)
yield_ = st.number_input("Yield (g)", step=0.1)
moagem = st.text_input("Moagem (K-Max)")
pre_infusao = st.number_input("Tempo de pré-infusão (s)", step=1)
st.header("3. Perfil sensorial desejado")
sensorial_desejado = st.text_input("Descreva o sensorial desejado")
acidez_d = st.slider("Acidez desejada", 1, 3, 2)
dulcor_d = st.slider("Dulçor desejado", 1, 3, 2)
amargor_d = st.slider("Amargor desejado", 1, 3, 2)
st.header("4. Resultado real (opcional)")
extracao_real = st.number_input("Tempo de extração real (s)", step=1)
yield_real = st.number_input("Yield real (g)", step=0.1)
acidez_r = st.slider("Acidez real", 1, 3, 2)
dulcor_r = st.slider("Dulçor real", 1, 3, 2)
amargor_r = st.slider("Amargor real", 1, 3, 2)

if st.button("Gerar Receita com IA"):
    dados = {
        "timestamp": datetime.now().isoformat(),
        "cafe": {
            "origem": origem,
            "processo": processo,
            "torra": torra
        },
        "parametros": {
            "dose": dose,
            "yield": yield_,
            "moagem": moagem,
            "pre_infusao": pre_infusao
        },
        "resultado_desejado": {
            "sensorial": sensorial_desejado,
            "perfil_sensorial": {
                "acidez": acidez_d,
                "dulcor": dulcor_d,
                "amargor": amargor_d
            }
        },
        "resultado_real": {
            "tempo_extracao": extracao_real,
            "yield": yield_real,
            "sensorial_real": {
                "acidez": acidez_r,
                "dulcor": dulcor_r,
                "amargor": amargor_r
            }
        }
    }
    salvar_entrada(dados)
    historico = carregar_historico()
    prompt = gerar_prompt(historico, dados)
    resposta = obter_resposta(prompt)
    st.subheader("Receita sugerida pela IA:")
    st.markdown(resposta)