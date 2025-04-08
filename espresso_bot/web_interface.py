import streamlit as st
from datetime import datetime
from espresso_bot.ai_client import get_response
from espresso_bot.data_handler import load_history, save_entry
from espresso_bot.prompt_generator import generate_prompt
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

    # Web Interface
    st.title(translations["title"])
    # st.header(translations["input_section_header"])
    process = st.selectbox(translations["process"], translations["process_options"], index=1)
    roast = st.selectbox(translations["roast_profile"], translations["roast_profile_options"], index=0)
    dose = st.number_input(translations["dose"], step=0.1, value=16.0)
    yield_ = st.number_input(translations["yield"], step=0.1, value=32.0)
    grind = st.text_input(translations["grind"], value="25")
    pre_infusion = st.number_input(translations["pre_infusion"], step=1, value=3)
    desired_sensory = st.selectbox(translations["desired_sensory"], translations["desired_sensory_options"])

    if st.button(translations["create_recipe"]):
        data = {
            "timestamp": datetime.now().isoformat(),
            "coffee": {
                "process": process,
                "roast": roast
            },
            "parameters": {
                "dose": dose,
                "yield": yield_,
                "grind": grind,
                "pre_infusion": pre_infusion
            },
            "desired_result": {
                "sensory": desired_sensory
            }
        }
        save_entry(data, DB_PATH)
        prompt = generate_prompt(history, data, language=language, summary=summary)
        response = get_response(prompt, language=language, summary=summary)
        st.subheader(translations["ai_suggested_recipe"])
        st.markdown(response)
