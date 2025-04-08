import streamlit as st
from datetime import datetime
from espresso_bot.ai_client import get_response
from espresso_bot.data_handler import load_history, save_entry
from espresso_bot.prompt_generator import generate_espresso_prompt, generate_brewers_prompt
import os
import json

def load_translations(language):
    with open(f"espresso_bot/translations/{language}.json", "r") as f:
        return json.load(f)

def web_interface(language="pt-BR", summary=True):
    # Local database path
    DB_PATH = "espressos.json"

    # Load translations
    translations = load_translations(language)

    # State to toggle between espresso and coado sections
    if "show_coado" not in st.session_state:
        st.session_state.show_coado = False

    # Toggle sections based on state
    if not st.session_state.show_coado:
        # Espresso Section
        st.title(translations["title"])
        process = st.selectbox(translations["process"], translations["process_options"], index=1)
        roast = st.selectbox(translations["roast_profile"], translations["roast_profile_options"], index=0)
        taste_notes = st.text_input(translations["taste_notes"])
        desired_sensory = st.selectbox(translations["desired_sensory"], translations["desired_sensory_options"])
        dose = st.number_input(translations["dose"], step=0.1, value=16.0)
        yield_ = st.number_input(translations["yield"], step=0.1, value=32.0)
        grind = st.text_input(translations["grind"], value="25")
        pre_infusion = st.number_input(translations["pre_infusion"], step=1, value=3)
        feedback = st.text_input(translations["feedback"])

        if st.button(translations["create_recipe"]):
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
            prompt = generate_espresso_prompt(history, data, language=language, summary=summary)
            response = get_response(prompt, language=language, summary=summary)
            st.subheader(translations["ai_suggested_recipe"])
            st.markdown(response)

        # Button to switch to coado section
        if st.button(translations["brew_more_button"]):
            st.session_state.show_coado = True
            # st.experimental_rerun()

    else:
        # Coado Section
        st.subheader("Bora fazer um café coado!")
        brew_process = st.selectbox(translations["brew_process"], translations["brew_process_options"])
        brew_taste_notes = st.text_input(translations["brew_taste_notes"])
        brew_roast_profile = st.selectbox(translations["brew_roast_profile"], translations["brew_roast_profile_options"])
        brew_method = st.selectbox(translations["brew_method"], translations["brew_method_options"])
        brew_amount = st.selectbox(translations["brew_amount"], translations["brew_amount_options"])
        brew_feedback = st.text_area(translations["brew_feedback"])

        if st.button("Gerar receita"):
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
            prompt = generate_brewers_prompt(history, data, language=language, summary=summary)
            response = get_response(prompt, language=language, summary=summary)
            st.subheader(translations["ai_suggested_recipe"])
            st.markdown(response)

        # Button to go back to espresso section
        if st.button("Quero tomar um espresso mesmo"):
            st.session_state.show_coado = False
            # st.experimental_rerun()
