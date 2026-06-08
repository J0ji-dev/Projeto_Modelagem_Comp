"""
Reconhecedor de Linguagem Recursiva (R) — Tema 2: Validador de Logs e Protocolos

Linguagem: L = { OPEN^n COMMIT^n CLOSE^n | n >= 1 }
Descrição: Trio balanceado de eventos — n blocos OPEN seguidos de n blocos COMMIT
           seguidos de n blocos CLOSE. Equivalente estrutural a a^n b^n c^n.
Alfabeto: Σ = {OPEN, COMMIT, CLOSE}
Modelo: Máquina de Turing (MT) com fita única

Esta linguagem NÃO é livre de contexto (demonstrável pelo Lema do Bombeamento para LLCs),
portanto exige o poder computacional de uma Máquina de Turing.

Estados da MT:
    q0  — estado inicial: procura o próximo OPEN não marcado
    q1  — encontrou OPEN, marcou como X_OPEN; busca próximo COMMIT não marcado
    q2  — encontrou COMMIT, marcou como X_COMMIT; busca próximo CLOSE não marcado
    q3  — encontrou CLOSE, marcou como X_CLOSE; volta ao início
    q4  — verificação: todos os símbolos devem estar marcados
    qA  — estado de aceitação
    qR  — estado de rejeição

Alfabeto da fita: Γ = {OPEN, COMMIT, CLOSE, X_OPEN, X_COMMIT, X_CLOSE, BLANK}

Ideia do algoritmo:
    1. A partir do início, encontrar o primeiro OPEN não marcado.
       - Se não encontrar OPEN mas encontrar COMMIT/CLOSE não marcado → rejeita.
       - Se todos estão marcados → aceita.
    2. Marcar esse OPEN como X_OPEN.
    3. Mover para a direita até encontrar o primeiro COMMIT não marcado.
       - Se encontrar CLOSE antes de COMMIT, ou chegar ao BLANK → rejeita.
    4. Marcar esse COMMIT como X_COMMIT.
    5. Mover para a direita até encontrar o primeiro CLOSE não marcado.
       - Se chegar ao BLANK sem encontrar CLOSE → rejeita.
    6. Marcar esse CLOSE como X_CLOSE.
    7. Voltar ao início da fita (mover para a esquerda até o início).
    8. Repetir a partir do passo 1.
"""

import sys


# ========================= DEFINIÇÃO FORMAL DA MT =========================

# Conjunto de estados
STATES = {"q0", "q1", "q2", "q3", "q4", "qA", "qR"}

# Alfabeto de entrada
INPUT_ALPHABET = {"OPEN", "COMMIT", "CLOSE"}

# Alfabeto da fita
TAPE_ALPHABET = {"OPEN", "COMMIT", "CLOSE", "X_OPEN", "X_COMMIT", "X_CLOSE", "BLANK"}

# Estado inicial
INITIAL_STATE = "q0"

# Estado de aceitação
ACCEPT_STATE = "qA"

# Estado de rejeição
REJECT_STATE = "qR"

# Símbolo branco
BLANK = "BLANK"

# Função de transição δ: (estado, símbolo_lido) -> (novo_estado, símbolo_escrito, direção)
# Direção: "R" (direita), "L" (esquerda), "S" (parado)
TRANSITION = {
    # q0: procura próximo OPEN não marcado (início de cada iteração)
    ("q0", "OPEN"):     ("q1", "X_OPEN", "R"),   # marca OPEN, vai buscar COMMIT
    ("q0", "X_OPEN"):   ("q0", "X_OPEN", "R"),   # pula OPENs já marcados
    ("q0", "X_COMMIT"): ("q0", "X_COMMIT", "R"), # pula COMMITs já marcados
    ("q0", "X_CLOSE"):  ("q0", "X_CLOSE", "R"),  # pula CLOSEs já marcados
    ("q0", "COMMIT"):   ("qR", "COMMIT", "S"),   # COMMIT não marcado sem OPEN → rejeita
    ("q0", "CLOSE"):    ("qR", "CLOSE", "S"),    # CLOSE não marcado sem OPEN → rejeita
    ("q0", "BLANK"):    ("q4", "BLANK", "L"),    # fim da fita, verificar se tudo marcado

    # q1: procura próximo COMMIT não marcado (movendo para a direita)
    ("q1", "OPEN"):     ("q1", "OPEN", "R"),     # pula OPENs não marcados restantes
    ("q1", "COMMIT"):   ("q2", "X_COMMIT", "R"), # marca COMMIT, vai buscar CLOSE
    ("q1", "CLOSE"):    ("qR", "CLOSE", "S"),    # CLOSE antes de COMMIT → rejeita
    ("q1", "X_OPEN"):   ("q1", "X_OPEN", "R"),   # pula marcados
    ("q1", "X_COMMIT"): ("q1", "X_COMMIT", "R"), # pula COMMITs já marcados
    ("q1", "X_CLOSE"):  ("q1", "X_CLOSE", "R"),  # pula CLOSEs já marcados
    ("q1", "BLANK"):    ("qR", "BLANK", "S"),    # não encontrou COMMIT → rejeita

    # q2: procura próximo CLOSE não marcado (movendo para a direita)
    ("q2", "OPEN"):     ("qR", "OPEN", "S"),     # OPEN fora de ordem → rejeita
    ("q2", "COMMIT"):   ("q2", "COMMIT", "R"),   # pula COMMITs não marcados restantes
    ("q2", "CLOSE"):    ("q3", "X_CLOSE", "L"),  # marca CLOSE, volta ao início
    ("q2", "X_OPEN"):   ("q2", "X_OPEN", "R"),   # pula marcados
    ("q2", "X_COMMIT"): ("q2", "X_COMMIT", "R"), # pula marcados
    ("q2", "X_CLOSE"):  ("q2", "X_CLOSE", "R"),  # pula marcados
    ("q2", "BLANK"):    ("qR", "BLANK", "S"),    # não encontrou CLOSE → rejeita

    # q3: volta ao início da fita (mover para a esquerda)
    ("q3", "OPEN"):     ("q3", "OPEN", "L"),
    ("q3", "COMMIT"):   ("q3", "COMMIT", "L"),
    ("q3", "CLOSE"):    ("q3", "CLOSE", "L"),
    ("q3", "X_OPEN"):   ("q3", "X_OPEN", "L"),
    ("q3", "X_COMMIT"): ("q3", "X_COMMIT", "L"),
    ("q3", "X_CLOSE"):  ("q3", "X_CLOSE", "L"),
    ("q3", "BLANK"):    ("q0", "BLANK", "R"),    # chegou ao início, recomeça

    # q4: verificação final — voltar verificando se tudo está marcado
    ("q4", "X_OPEN"):   ("q4", "X_OPEN", "L"),
    ("q4", "X_COMMIT"): ("q4", "X_COMMIT", "L"),
    ("q4", "X_CLOSE"):  ("q4", "X_CLOSE", "L"),
    ("q4", "OPEN"):     ("qR", "OPEN", "S"),     # OPEN não marcado restante → rejeita
    ("q4", "COMMIT"):   ("qR", "COMMIT", "S"),   # COMMIT não marcado → rejeita
    ("q4", "CLOSE"):    ("qR", "CLOSE", "S"),    # CLOSE não marcado → rejeita
    ("q4", "BLANK"):    ("qA", "BLANK", "S"),    # tudo verificado → aceita
}


# ========================= SIMULADOR DA MT =========================

def run_tm(input_string, verbose=False):
    """
    Simula a Máquina de Turing sobre a cadeia de entrada.

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

    # Validar que todos os tokens pertencem ao alfabeto de entrada
    for token in tokens:
        if token not in INPUT_ALPHABET:
            if verbose:
                print(f"  Erro: token '{token}' não pertence ao alfabeto de entrada")
            return False, 0, []

    # Rejeitar cadeia vazia (n >= 1)
    if len(tokens) == 0:
        if verbose:
            print("  Cadeia vazia → REJEITA (n deve ser >= 1)")
        return False, 0, []

    # Inicializar a fita: BLANK + tokens + BLANK
    tape = [BLANK] + list(tokens) + [BLANK]
    head = 1  # posição inicial da cabeça (primeiro símbolo da entrada)
    current_state = INITIAL_STATE
    steps = 0
    history = [{
        "state": current_state,
        "head": head,
        "tape": list(tape)
    }]

    # Limite de segurança para evitar loops infinitos
    MAX_STEPS = 10000

    while current_state not in (ACCEPT_STATE, REJECT_STATE):
        if steps >= MAX_STEPS:
            if verbose:
                print(f"  Limite de {MAX_STEPS} passos atingido → REJEITA")
            return False, steps, history

        # Ler símbolo sob a cabeça
        symbol = tape[head]

        # Buscar transição
        key = (current_state, symbol)
        if key not in TRANSITION:
            if verbose:
                print(f"  Passo {steps + 1}: Sem transição para "
                      f"δ({current_state}, {symbol}) → REJEITA")
            return False, steps, history

        new_state, write_symbol, direction = TRANSITION[key]
        steps += 1  # Cada movimento da cabeça = 1 passo

        if verbose:
            print(f"  Passo {steps}: δ({current_state}, {symbol}) = "
                  f"({new_state}, {write_symbol}, {direction})")

        # Escrever na fita
        tape[head] = write_symbol

        # Mover a cabeça
        if direction == "R":
            head += 1
        elif direction == "L":
            head -= 1
        # "S" = não mover

        # Expandir a fita se necessário
        if head < 0:
            tape.insert(0, BLANK)
            head = 0
        elif head >= len(tape):
            tape.append(BLANK)

        current_state = new_state

        history.append({
            "state": current_state,
            "head": head,
            "tape": list(tape),
            "symbol_read": symbol,
            "symbol_written": write_symbol,
            "direction": direction
        })

    accepted = current_state == ACCEPT_STATE

    if verbose:
        print(f"  Estado final: {current_state} → "
              f"{'ACEITA' if accepted else 'REJEITA'}")

    return accepted, steps, history


# ========================= EXECUÇÃO AUTÔNOMA =========================

def main():
    if len(sys.argv) < 2:
        print("Uso: python recursiva.py \"<cadeia>\"")
        print("Exemplo: python recursiva.py \"OPEN OPEN COMMIT COMMIT CLOSE CLOSE\"")
        sys.exit(1)

    input_string = sys.argv[1]
    print(f"Entrada: \"{input_string}\"")
    print(f"Linguagem: L = {{ OPEN^n COMMIT^n CLOSE^n | n >= 1 }}")
    print(f"Modelo: Máquina de Turing com {len(STATES)} estados")
    print("-" * 60)
    print("Execução passo a passo:")

    accepted, steps, history = run_tm(input_string, verbose=True)

    print("-" * 60)
    print(f"Resultado: {'ACEITA' if accepted else 'REJEITA'}")
    print(f"Número de passos: {steps}")


if __name__ == "__main__":
    main()
