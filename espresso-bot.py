from espresso_bot.web_interface import web_interface
from espresso_bot.ai_client import get_client, get_response
from espresso_bot.data_handler import load_history, save_entry
from espresso_bot.prompt_generator import generate_prompt
import os

# Local database path
DB_PATH = "espressos.json"

if __name__ == "__main__":
    web_interface()
