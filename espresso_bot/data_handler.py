import json
import os

DB_PATH = "espressos.json"

def carregar_historico():
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_entrada(data):
    historico = carregar_historico()
    historico.append(data)
    with open(DB_PATH, "w") as f:
        json.dump(historico, f, indent=2)
