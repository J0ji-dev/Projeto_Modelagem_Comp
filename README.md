# Validador Formal em Três Níveis

**Tema 2: Validador de Logs e Protocolos**

Projeto prático da disciplina de Modelagem Computacional. Implementação de três reconhecedores formais que demonstram a hierarquia de Chomsky: LR ⊊ LLC ⊊ R.

## Linguagens Implementadas

| Nível | Linguagem | Modelo | Descrição |
|-------|-----------|--------|-----------|
| LR | `LOGIN AUTH REQUEST^n LOGOUT` | DFA (5 estados) | Sequência de eventos de protocolo |
| LLC | `BEGIN^n END^n` (aninhados) | PDA (3 estados) | Blocos de transação balanceados |
| R | `OPEN^n COMMIT^n CLOSE^n` | MT (7 estados) | Trio balanceado de eventos |

## Estrutura do Repositório

```
projeto/
├── README.md
├── requirements.txt
├── src/
│   ├── regular.py          (reconhecedor LR — DFA)
│   ├── livre_contexto.py   (reconhecedor LLC — PDA)
│   ├── recursiva.py        (reconhecedor R — Máquina de Turing)
│   └── testes.py           (bateria de testes completa)
├── testes/
│   ├── testes_regular.txt
│   ├── testes_livre_contexto.txt
│   └── testes_recursiva.txt
├── diagramas/
│   ├── dfa_regular.png
│   ├── pda_livre_contexto.png
│   └── mt_recursiva.png
└── relatorio/
    └── relatorio.pdf
```

## Como Executar

### Pré-requisitos

```bash
pip install -r requirements.txt
Se não rodar o pip acima, use:
python -m pip install -r requirements.txt
```

### Rodar a bateria completa de testes

```bash
python src/testes.py
```

### Executar cada reconhecedor individualmente

```bash
# Linguagem Regular (DFA)
python src/regular.py "LOGIN AUTH REQUEST REQUEST LOGOUT"

# Linguagem Livre de Contexto (PDA)
python src/livre_contexto.py "BEGIN BEGIN END END"

# Linguagem Recursiva (Máquina de Turing)
python src/recursiva.py "OPEN OPEN COMMIT COMMIT CLOSE CLOSE"
```

## Detalhes dos Reconhecedores

### Nível 1 — Linguagem Regular (DFA)

- **Linguagem:** L = { LOGIN AUTH REQUEST^n LOGOUT | n ≥ 0 }
- **Alfabeto:** Σ = {LOGIN, AUTH, REQUEST, LOGOUT}
- **Modelo:** Autômato Finito Determinístico com 5 estados
- **Aceitação:** Estado final q3 atingido após processar toda a entrada

### Nível 2 — Linguagem Livre de Contexto (PDA)

- **Linguagem:** L = { w ∈ {BEGIN, END}* | w tem BEGIN/END balanceados e aninhados }
- **Alfabeto:** Σ = {BEGIN, END}
- **Modelo:** Autômato com Pilha, 3 estados, pilha com {Z0, B}
- **Aceitação:** Estado q0 com pilha contendo apenas Z0 ao final da entrada

### Nível 3 — Linguagem Recursiva (MT)

- **Linguagem:** L = { OPEN^n COMMIT^n CLOSE^n | n ≥ 1 }
- **Alfabeto:** Σ = {OPEN, COMMIT, CLOSE}
- **Modelo:** Máquina de Turing com 7 estados e fita única
- **Algoritmo:** Marcação iterativa — a cada passagem marca um OPEN, um COMMIT e um CLOSE, até que todos estejam marcados

## Equipe

- [Nome 1]
- [Nome 2]
- [Nome 3]
