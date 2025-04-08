import streamlit as st
from datetime import datetime
from espresso_bot.ai_client import obter_resposta
from espresso_bot.data_handler import carregar_historico, salvar_entrada
from espresso_bot.prompt_generator import gerar_prompt
import os

def web_interface():
    # Caminho do banco de dados local
    DB_PATH = "espressos.json"

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
        salvar_entrada(dados, DB_PATH)
        historico = carregar_historico(DB_PATH)
        prompt = gerar_prompt(historico, dados)
        resposta = obter_resposta(prompt)
        st.subheader("Receita sugerida pela IA:")
        st.markdown(resposta)
