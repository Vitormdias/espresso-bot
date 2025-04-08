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

def web_interface():
    # Local database path
    DB_PATH = "espressos.json"

    # Load translations
    language = "pt-BR"
    translations = load_translations(language)

    # Web Interface
    st.title(translations["title"])
    st.header(translations["input_section_header"])
    process = st.selectbox(translations["process"], translations["process_options"])
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
                "sensory": desired_sensory,
                "sensory_profile": {
                    "acidity": None,
                    "sweetness": None,
                    "bitterness": None
                }
            },
            "actual_result": {
                "extraction_time": None,
                "yield": None,
                "actual_sensory": {
                    "acidity": None,
                    "sweetness": None,
                    "bitterness": None
                }
            }
        }
        save_entry(data, DB_PATH)
        history = load_history(DB_PATH)
        prompt = generate_prompt(history, data)
        response = get_response(prompt)
        st.subheader(translations["ai_suggested_recipe"])
        st.markdown(response)

    st.header(translations["actual_result_header"])
    actual_extraction = st.number_input(translations["actual_extraction"], step=1)
    actual_yield = st.number_input(translations["actual_yield"], step=0.1)
    actual_sensory = st.selectbox(translations["actual_sensory"], translations["actual_sensory_options"])

    if st.button(translations["send_actual_result"]):
        actual_data = {
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
                "sensory": desired_sensory,
                "sensory_profile": {
                    "acidity": None,
                    "sweetness": None,
                    "bitterness": None
                }
            },
            "actual_result": {
                "extraction_time": actual_extraction,
                "yield": actual_yield,
                "actual_sensory": {
                    "acidity": None,
                    "sweetness": None,
                    "bitterness": None
                }
            }
        }
        save_entry(actual_data, DB_PATH)
        history = load_history(DB_PATH)
        prompt = generate_prompt(history, actual_data)
        response = get_response(prompt)
        st.subheader(translations["ai_suggested_adjustments"])
        st.markdown(response)
