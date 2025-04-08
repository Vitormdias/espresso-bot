from espresso_bot.web_interface import web_interface
from espresso_bot.ai_client import get_client, obter_resposta
from espresso_bot.data_handler import carregar_historico, salvar_entrada
from espresso_bot.prompt_generator import gerar_prompt
import os

# Caminho do banco de dados local
DB_PATH = "espressos.json"

if __name__ == "__main__":
    web_interface()
