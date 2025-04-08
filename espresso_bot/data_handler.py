import json
import os

def carregar_historico(db_path):
    try:
        with open(db_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_entrada(data, db_path):
    historico = carregar_historico(db_path)
    historico.append(data)
    with open(db_path, "w") as f:
        json.dump(historico, f, indent=2)
