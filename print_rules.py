import pickle
import os

RULES_FILE_PATH = "/home/gustavocunha/project2-pv2/rules.pkl"

def load_rules(file_path):
    """Carrega regras do arquivo pickle."""
    if not os.path.exists(file_path):
        print(f"Arquivo de regras não encontrado em {file_path}")
        return None

    with open(file_path, 'rb') as f:
        rules = pickle.load(f)
    return rules

def inspect_rules(rules):
    """Inspeciona as regras e verifica o formato esperado."""
    if not isinstance(rules, list):
        print("Erro: As regras carregadas não estão no formato de lista.")
        return

    print(f"Total de regras: {len(rules)}")
    valid_rules = 0
    invalid_rules = 0

    for i, rule in enumerate(rules[:60]):  # Mostra apenas as primeiras 10 regras para depuração
        if isinstance(rule, tuple) and len(rule) == 2 and \
           isinstance(rule[0], list) and isinstance(rule[1], list):
            print(f"Regra {i + 1}:")
            print(f"  Condição: {rule[0]}")
            print(f"  Consequência: {rule[1]}")
            valid_rules += 1
        else:
            print(f"Regra {i + 1} está no formato inválido: {rule}")
            invalid_rules += 1

    print("\nResumo:")
    print(f"Regras válidas: {valid_rules}")
    print(f"Regras inválidas: {invalid_rules}")

def main():
    rules = load_rules(RULES_FILE_PATH)
    if rules:
        inspect_rules(rules)

if __name__ == "__main__":
    main()
