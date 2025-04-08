import streamlit as st
from datetime import datetime
from espresso_bot.ai_client import get_response
from espresso_bot.data_handler import load_history, save_entry
from espresso_bot.prompt_generator import generate_prompt
import os

def web_interface():
    # Local database path
    DB_PATH = "espressos.json"

    # Web Interface
    st.title("Espresso Bot with AI")
    st.header("Input Section")
    process = st.selectbox("Process", ["Natural", "Washed", "Honey", "Other"])
    roast = st.selectbox("Roast Profile", ["Light Medium", "Medium", "Dark"], index=0)
    dose = st.number_input("Dose (g)", step=0.1, value=16.0)
    yield_ = st.number_input("Yield (g)", step=0.1, value=32.0)
    grind = st.text_input("Grind (K-Max)", value="25")
    pre_infusion = st.number_input("Pre-infusion Time (s)", step=1, value=3)
    desired_sensory = st.selectbox("Desired Sensory Profile", ["Balanced Fruity Acidity & Sweetness", "Sweet and syrupy", "Strong body, balanced sweetness and no acidity", "Clear acidity and floral notes (not sour)"])

    if st.button("Generate Recipe with AI"):
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
        st.subheader("AI Suggested Recipe:")
        st.markdown(response)

    st.header("Actual Result (optional)")
    actual_extraction = st.number_input("Actual Extraction Time (s)", step=1)
    actual_yield = st.number_input("Actual Yield (g)", step=0.1)
    actual_sensory = st.selectbox("Actual Sensory Profile", ["On the spot, perfect!", "High sourness", "High bitterness", "Remove a little bit of bitterness", "Remove a little bit of sourness", "Improve sweetness", "Lacks clarity"])

    if st.button("Send Actual Result to Model"):
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
        st.subheader("AI Suggested Adjustments:")
        st.markdown(response)
