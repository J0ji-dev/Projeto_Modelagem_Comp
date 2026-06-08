"""
Reconhecedor de Linguagem Regular (LR) — Tema 2: Validador de Logs e Protocolos

Linguagem: L = { LOGIN AUTH REQUEST^n LOGOUT | n >= 0 }
Descrição: Sequência de eventos que começa com LOGIN, seguido de AUTH,
           seguido de zero ou mais REQUEST, terminando com LOGOUT.
Alfabeto: Σ = {LOGIN, AUTH, REQUEST, LOGOUT}
Modelo: Autômato Finito Determinístico (DFA)

Estados: {q0, q1, q2, q3, DEAD}
Estado inicial: q0
Estados finais: {q3}

Tabela de transição:
    +---------+---------+-------+-----------+---------+
    | Estado  | LOGIN   | AUTH  | REQUEST   | LOGOUT  |
    +---------+---------+-------+-----------+---------+
    | q0      | q1      | DEAD  | DEAD      | DEAD    |
    | q1      | DEAD    | q2    | DEAD      | DEAD    |
    | q2      | DEAD    | DEAD  | q2        | q3      |
    | q3      | DEAD    | DEAD  | DEAD      | DEAD    |
    | DEAD    | DEAD    | DEAD  | DEAD      | DEAD    |
    +---------+---------+-------+-----------+---------+
"""

import sys


# ========================= DEFINIÇÃO FORMAL DO DFA =========================

# Conjunto de estados
STATES = {"q0", "q1", "q2", "q3", "DEAD"}

# Alfabeto
ALPHABET = {"LOGIN", "AUTH", "REQUEST", "LOGOUT"}

# Estado inicial
INITIAL_STATE = "q0"

# Estados finais (de aceitação)
FINAL_STATES = {"q3"}

# Função de transição δ: (estado, símbolo) -> estado
TRANSITION = {
    ("q0", "LOGIN"):   "q1",
    ("q0", "AUTH"):    "DEAD",
    ("q0", "REQUEST"): "DEAD",
    ("q0", "LOGOUT"):  "DEAD",

    ("q1", "LOGIN"):   "DEAD",
    ("q1", "AUTH"):    "q2",
    ("q1", "REQUEST"): "DEAD",
    ("q1", "LOGOUT"):  "DEAD",

    ("q2", "LOGIN"):   "DEAD",
    ("q2", "AUTH"):    "DEAD",
    ("q2", "REQUEST"): "q2",
    ("q2", "LOGOUT"):  "q3",

    ("q3", "LOGIN"):   "DEAD",
    ("q3", "AUTH"):    "DEAD",
    ("q3", "REQUEST"): "DEAD",
    ("q3", "LOGOUT"):  "DEAD",

    ("DEAD", "LOGIN"):   "DEAD",
    ("DEAD", "AUTH"):    "DEAD",
    ("DEAD", "REQUEST"): "DEAD",
    ("DEAD", "LOGOUT"):  "DEAD",
}


# ========================= SIMULADOR DO DFA =========================

def run_dfa(input_string, verbose=False):
    """
    Simula o DFA sobre a cadeia de entrada.

    Args:
        input_string: string com tokens separados por espaço.
        verbose: se True, imprime execução passo a passo.

    Returns:
        tuple: (aceita: bool, passos: int, historico: list)
    """
    # Tokenizar a entrada
    if input_string.strip() == "":
        tokens = []
    else:
        tokens = input_string.strip().split()

    current_state = INITIAL_STATE
    steps = 0
    history = [{"state": current_state, "remaining": list(tokens)}]

    for i, token in enumerate(tokens):
        # Verificar se o símbolo pertence ao alfabeto
        if token not in ALPHABET:
            if verbose:
                print(f"  Passo {steps + 1}: Estado {current_state}, "
                      f"símbolo '{token}' não pertence ao alfabeto → REJEITA")
            history.append({
                "state": "DEAD",
                "symbol_read": token,
                "note": "símbolo fora do alfabeto"
            })
            return False, steps, history

        # Aplicar a função de transição (1 passo = 1 leitura de símbolo)
        next_state = TRANSITION[(current_state, token)]
        steps += 1

        if verbose:
            print(f"  Passo {steps}: δ({current_state}, {token}) = {next_state}")

        history.append({
            "state": next_state,
            "symbol_read": token,
            "remaining": tokens[i + 1:]
        })

        current_state = next_state

    accepted = current_state in FINAL_STATES

    if verbose:
        print(f"  Estado final: {current_state} → "
              f"{'ACEITA' if accepted else 'REJEITA'}")

    return accepted, steps, history


# ========================= EXECUÇÃO AUTÔNOMA =========================

def main():
    if len(sys.argv) < 2:
        print("Uso: python regular.py \"<cadeia>\"")
        print("Exemplo: python regular.py \"LOGIN AUTH REQUEST LOGOUT\"")
        sys.exit(1)

    input_string = sys.argv[1]
    print(f"Entrada: \"{input_string}\"")
    print(f"Linguagem: L = {{ LOGIN AUTH REQUEST^n LOGOUT | n >= 0 }}")
    print(f"Modelo: DFA com {len(STATES)} estados")
    print("-" * 50)
    print("Execução passo a passo:")

    accepted, steps, history = run_dfa(input_string, verbose=True)

    print("-" * 50)
    print(f"Resultado: {'ACEITA' if accepted else 'REJEITA'}")
    print(f"Número de passos: {steps}")


if __name__ == "__main__":
    main()
