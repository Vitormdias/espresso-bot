import streamlit as st
from datetime import datetime
from espresso_bot.ai_client import get_response
from espresso_bot.data_handler import load_history, save_entry
from espresso_bot.prompt_generator import generate_espresso_prompt, generate_brewers_prompt

def web_interface(summary=True):
    # Local database path
    DB_PATH = "espressos.json"

    # Arrays for dropdown options
    process_options = ["Lavado", "Natural", "Honey", "Fermentado"]
    roast_profile_options = ["Clara", "Média", "Escura"]
    desired_sensory_options = [
        "Acidez suave e dulçor frutado",
        "Doce e encorpado",
        "Acidez clara e floral"
    ]
    brew_method_options = ["V-60", "Koar", "Clever", "Kalita", "Melitta", "Aeropress"]
    brew_amount_options = ["200ml", "300ml", "500ml"]
    brew_process_options = ["Natural", "Lavado", "Honey", "Fermentado"]

    # Import external CSS
    with open("espresso_bot/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # State to toggle between espresso and coado sections
    if "show_coado" not in st.session_state:
        st.session_state.show_coado = False

    # Toggle sections based on state
    if not st.session_state.show_coado:
        # Espresso Section
        st.title("☕ Bora regular um espresso!")
        st.markdown("### Ajuste os parâmetros para criar a receita perfeita de espresso.")
        process = st.selectbox("Processo", process_options, index=1)
        roast = st.selectbox("Perfil de Torra", roast_profile_options, index=0)
        taste_notes = st.text_input("Notas sensoriais")
        desired_sensory = st.selectbox("Perfil Sensorial Desejado", desired_sensory_options)
        dose = st.number_input("Dose (g)", step=0.1, value=16.0)
        yield_ = st.number_input("Rendimento (g)", step=0.1, value=32.0)
        grind = st.text_input("Moagem (K-Max)", value="25")
        pre_infusion = st.number_input("Tempo de pré-infusão (s)", step=1, value=3)
        feedback = st.text_input("Feedback")

        if st.button("☕ Criar receita"):
            data = {
                "timestamp": datetime.now().isoformat(),
                "coffee": {
                    "process": process,
                    "roast": roast,
                    "taste_notes": taste_notes
                },
                "parameters": {
                    "dose": dose,
                    "yield": yield_,
                    "grind": grind,
                    "pre_infusion": pre_infusion,
                    "desired_sensory": desired_sensory,
                    "feedback": feedback
                }
            }
            save_entry(data, DB_PATH)
            history = load_history(DB_PATH)
            prompt = generate_espresso_prompt(history, data, summary=summary)
            response = get_response(prompt, summary=summary)
            st.subheader("☕ Tente começar com essa receita:")
            st.markdown(response)

        # Button to switch to coado section
        if st.button("🌱 Que tal regular um coado agora?"):
            st.session_state.show_coado = True

    else:
        # Coado Section
        st.title("🌿 Bora fazer um café coado!")
        st.markdown("### Ajuste os parâmetros para criar a receita perfeita de café coado.")
        brew_process = st.selectbox("Processo", brew_process_options)
        brew_taste_notes = st.text_input("Notas sensoriais")
        brew_roast_profile = st.selectbox("Perfil de Torra", roast_profile_options)
        brew_method = st.selectbox("Método de Preparo", brew_method_options)
        brew_amount = st.selectbox("Quanto de café quer fazer?", brew_amount_options)
        brew_feedback = st.text_area("Feedback do preparo")

        if st.button("🌿 Gerar receita"):
            brew_data = {
                "timestamp": datetime.now().isoformat(),
                "brew": {
                    "process": brew_process,
                    "taste_notes": brew_taste_notes,
                    "roast_profile": brew_roast_profile,
                    "method": brew_method,
                    "amount": brew_amount,
                    "feedback": brew_feedback
                }
            }
            save_entry(brew_data, DB_PATH)
            history = load_history(DB_PATH)
            prompt = generate_brewers_prompt(history, brew_data, summary=summary)
            response = get_response(prompt, summary=summary)
            st.subheader("🌿 Tente começar com essa receita:")
            st.markdown(response)

        # Button to go back to espresso section
        if st.button("☕ Quero tomar um espresso mesmo"):
            st.session_state.show_coado = False
