"""
Reconhecedor de Linguagem Livre de Contexto (LLC) — Tema 2: Validador de Logs e Protocolos

Linguagem: L = { w ∈ {BEGIN, END}* | w tem blocos BEGIN/END balanceados e aninhados }
Descrição: Blocos aninhados de transação onde cada BEGIN precisa de um END
           correspondente, podendo aninhar.
Alfabeto: Σ = {BEGIN, END}
Alfabeto da pilha: Γ = {Z0, B}  (Z0 = marcador de fundo, B = marcador de BEGIN)
Modelo: Autômato com Pilha (PDA)

Estados: {q0, q1, DEAD}
Estado inicial: q0
Estados finais: {q1}
Símbolo inicial da pilha: Z0

Transições do PDA:
    δ(q0, BEGIN, Z0) = (q0, BZ0)    — empilha B sobre Z0
    δ(q0, BEGIN, B)  = (q0, BB)     — empilha B sobre B
    δ(q0, END, B)    = (q0, ε)      — desempilha B (pop)
    δ(q0, END, Z0)   = (DEAD, Z0)   — END sem BEGIN correspondente → rejeita
    δ(q0, ε, Z0)     = (q1, Z0)     — fim da entrada com pilha só com Z0 → aceita

Aceitação: por estado final (q1) quando a entrada termina e a pilha contém apenas Z0.
"""

import sys


# ========================= DEFINIÇÃO FORMAL DO PDA =========================

# Conjunto de estados
STATES = {"q0", "q1", "DEAD"}

# Alfabeto de entrada
ALPHABET = {"BEGIN", "END"}

# Alfabeto da pilha
STACK_ALPHABET = {"Z0", "B"}

# Estado inicial
INITIAL_STATE = "q0"

# Símbolo inicial da pilha
INITIAL_STACK_SYMBOL = "Z0"

# Estados finais (de aceitação)
FINAL_STATES = {"q1"}

# Função de transição δ: (estado, símbolo_entrada, topo_pilha) -> (novo_estado, operação_pilha)
# Operação da pilha: lista de símbolos a empilhar (vazia = pop sem push)
TRANSITION = {
    ("q0", "BEGIN", "Z0"): ("q0", ["B", "Z0"]),   # push B, mantém Z0
    ("q0", "BEGIN", "B"):  ("q0", ["B", "B"]),     # push B sobre B
    ("q0", "END", "B"):    ("q0", []),              # pop B (desempilha)
    ("q0", "END", "Z0"):   ("DEAD", ["Z0"]),       # END sem BEGIN → erro
}


# ========================= SIMULADOR DO PDA =========================

def run_pda(input_string, verbose=False):
    """
    Simula o PDA sobre a cadeia de entrada.

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
    stack = [INITIAL_STACK_SYMBOL]  # pilha (topo = último elemento)
    steps = 0
    history = [{
        "state": current_state,
        "stack": list(stack),
        "remaining": list(tokens)
    }]

    for i, token in enumerate(tokens):
        # Verificar se o símbolo pertence ao alfabeto
        if token not in ALPHABET:
            if verbose:
                print(f"  Passo {steps + 1}: Estado {current_state}, "
                      f"símbolo '{token}' não pertence ao alfabeto → REJEITA")
            return False, steps, history

        # Topo da pilha
        top = stack[-1] if stack else None

        if top is None:
            # Pilha vazia inesperadamente
            if verbose:
                print(f"  Passo {steps + 1}: Pilha vazia, "
                      f"símbolo '{token}' → REJEITA")
            return False, steps, history

        # Buscar transição
        key = (current_state, token, top)
        if key not in TRANSITION:
            if verbose:
                print(f"  Passo {steps + 1}: Sem transição para "
                      f"δ({current_state}, {token}, {top}) → REJEITA")
            return False, steps, history

        next_state, push_symbols = TRANSITION[key]
        steps += 1  # Cada transição (leitura + operação na pilha) = 1 passo

        # Desempilhar o topo
        stack.pop()

        # Empilhar os novos símbolos (em ordem reversa, para que o
        # primeiro da lista fique no topo)
        for symbol in reversed(push_symbols):
            stack.append(symbol)

        if verbose:
            stack_str = "".join(reversed(stack)) if stack else "∅"
            print(f"  Passo {steps}: δ({current_state}, {token}, {top}) = "
                  f"({next_state}, {''.join(push_symbols) if push_symbols else 'ε'}) "
                  f"| Pilha: [{stack_str}]")

        history.append({
            "state": next_state,
            "symbol_read": token,
            "stack": list(stack),
            "remaining": tokens[i + 1:]
        })

        current_state = next_state

        # Se entrou em estado morto, rejeitar imediatamente
        if current_state == "DEAD":
            if verbose:
                print(f"  → Estado DEAD atingido → REJEITA")
            return False, steps, history

    # Verificar aceitação: estado final + pilha contém apenas Z0
    accepted = (current_state == "q0" and
                len(stack) == 1 and
                stack[0] == INITIAL_STACK_SYMBOL)

    if verbose:
        stack_str = "".join(reversed(stack)) if stack else "∅"
        print(f"  Fim da entrada: estado={current_state}, pilha=[{stack_str}]")
        print(f"  → {'ACEITA' if accepted else 'REJEITA'}")

    return accepted, steps, history


# ========================= EXECUÇÃO AUTÔNOMA =========================

def main():
    if len(sys.argv) < 2:
        print("Uso: python livre_contexto.py \"<cadeia>\"")
        print("Exemplo: python livre_contexto.py \"BEGIN BEGIN END END\"")
        sys.exit(1)

    input_string = sys.argv[1]
    print(f"Entrada: \"{input_string}\"")
    print(f"Linguagem: L = {{ w ∈ {{BEGIN, END}}* | BEGIN/END balanceados }}")
    print(f"Modelo: PDA com {len(STATES)} estados")
    print("-" * 50)
    print("Execução passo a passo:")

    accepted, steps, history = run_pda(input_string, verbose=True)

    print("-" * 50)
    print(f"Resultado: {'ACEITA' if accepted else 'REJEITA'}")
    print(f"Número de passos: {steps}")


if __name__ == "__main__":
    main()
