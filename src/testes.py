"""
Bateria de testes — Validador Formal em Três Níveis
Tema 2: Validador de Logs e Protocolos

Lê os arquivos testes/*.txt e roda contra os 3 reconhecedores.
Formato de cada linha nos arquivos de teste: <cadeia>,<ACEITA|REJEITA>

Saída: tabela esperado vs obtido + número de passos para cada teste.
"""

import os
import sys

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

from regular import run_dfa
from livre_contexto import run_pda
from recursiva import run_tm


def load_tests(filepath):
    """Carrega casos de teste de um arquivo .txt"""
    tests = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.rsplit(",", 1)
            if len(parts) == 2:
                cadeia = parts[0].strip()
                esperado = parts[1].strip().upper()
                tests.append((cadeia, esperado == "ACEITA"))
    return tests


def run_test_suite(name, runner, tests):
    """Executa uma bateria de testes e imprime resultados em tabela."""
    print(f"\n{'=' * 70}")
    print(f"  {name}")
    print(f"{'=' * 70}")
    print(f"{'Cadeia':<45} {'Esperado':<10} {'Obtido':<10} {'Passos':<7} {'OK?'}")
    print(f"{'-' * 70}")

    passed = 0
    total = len(tests)

    for cadeia, esperado in tests:
        aceita, passos, _ = runner(cadeia)
        obtido_str = "ACEITA" if aceita else "REJEITA"
        esperado_str = "ACEITA" if esperado else "REJEITA"
        ok = "✓" if aceita == esperado else "✗"

        if aceita == esperado:
            passed += 1

        # Truncar cadeia se muito longa
        display = cadeia if len(cadeia) <= 43 else cadeia[:40] + "..."
        print(f"{display:<45} {esperado_str:<10} {obtido_str:<10} {passos:<7} {ok}")

    print(f"{'-' * 70}")
    print(f"  Resultado: {passed}/{total} testes passaram")
    return passed, total


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(os.path.dirname(base_dir), "testes")

    # Se executado de dentro de src/, ajustar caminho
    if not os.path.exists(test_dir):
        test_dir = os.path.join(base_dir, "..", "testes")
    if not os.path.exists(test_dir):
        test_dir = os.path.join(os.getcwd(), "testes")

    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     VALIDADOR FORMAL EM TRÊS NÍVEIS — Bateria de Testes            ║")
    print("║     Tema 2: Validador de Logs e Protocolos                         ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    total_passed = 0
    total_tests = 0

    # Teste 1: Linguagem Regular (DFA)
    test_file = os.path.join(test_dir, "testes_regular.txt")
    if os.path.exists(test_file):
        tests = load_tests(test_file)
        p, t = run_test_suite(
            "NÍVEL 1 — Linguagem Regular (DFA)",
            run_dfa,
            tests
        )
        total_passed += p
        total_tests += t
    else:
        print(f"\n⚠ Arquivo não encontrado: {test_file}")

    # Teste 2: Linguagem Livre de Contexto (PDA)
    test_file = os.path.join(test_dir, "testes_livre_contexto.txt")
    if os.path.exists(test_file):
        tests = load_tests(test_file)
        p, t = run_test_suite(
            "NÍVEL 2 — Linguagem Livre de Contexto (PDA)",
            run_pda,
            tests
        )
        total_passed += p
        total_tests += t
    else:
        print(f"\n⚠ Arquivo não encontrado: {test_file}")

    # Teste 3: Linguagem Recursiva (MT)
    test_file = os.path.join(test_dir, "testes_recursiva.txt")
    if os.path.exists(test_file):
        tests = load_tests(test_file)
        p, t = run_test_suite(
            "NÍVEL 3 — Linguagem Recursiva (Máquina de Turing)",
            run_tm,
            tests
        )
        total_passed += p
        total_tests += t
    else:
        print(f"\n⚠ Arquivo não encontrado: {test_file}")

    # Resumo final
    print(f"\n{'=' * 70}")
    print(f"  RESUMO GERAL: {total_passed}/{total_tests} testes passaram")
    if total_passed == total_tests:
        print("  ✓ Todos os testes passaram!")
    else:
        print(f"  ✗ {total_tests - total_passed} teste(s) falharam")
    print(f"{'=' * 70}")

    return 0 if total_passed == total_tests else 1


if __name__ == "__main__":
    sys.exit(main())
