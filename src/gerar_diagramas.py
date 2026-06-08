"""
Gerador de diagramas para os três reconhecedores.
Usa matplotlib para desenhar os autômatos sem depender do Graphviz binário.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diagramas")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_arrow(ax, start, end, label, color='black', curve=0):
    """Desenha seta entre dois pontos com label."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dist = np.sqrt(dx**2 + dy**2)

    # Offset para não sobrepor os círculos (raio ~0.3)
    r = 0.35
    if dist > 0:
        sx = start[0] + r * dx / dist
        sy = start[1] + r * dy / dist
        ex = end[0] - r * dx / dist
        ey = end[1] - r * dy / dist
    else:
        sx, sy = start
        ex, ey = end

    style = f"arc3,rad={curve}"
    arrow = mpatches.FancyArrowPatch(
        (sx, sy), (ex, ey),
        arrowstyle='->', mutation_scale=15,
        connectionstyle=style,
        color=color, linewidth=1.5
    )
    ax.add_patch(arrow)

    # Label position
    mid_x = (sx + ex) / 2 + curve * (ey - sy) * 0.5
    mid_y = (sy + ey) / 2 + curve * (sx - ex) * 0.5
    ax.text(mid_x, mid_y, label, fontsize=8, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow',
                      edgecolor='none', alpha=0.8))


def draw_self_loop(ax, center, label, direction='top'):
    """Desenha loop próprio (transição para o mesmo estado)."""
    x, y = center
    if direction == 'top':
        loop_center = (x, y + 0.55)
        angle = 0
    elif direction == 'bottom':
        loop_center = (x, y - 0.55)
        angle = 180
    elif direction == 'right':
        loop_center = (x + 0.55, y)
        angle = 270
    else:
        loop_center = (x - 0.55, y)
        angle = 90

    loop = mpatches.FancyArrowPatch(
        (x + 0.15, y + 0.33), (x - 0.15, y + 0.33),
        arrowstyle='->', mutation_scale=12,
        connectionstyle="arc3,rad=-1.5",
        color='black', linewidth=1.5
    )
    ax.add_patch(loop)
    ax.text(x, y + 0.75, label, fontsize=8, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow',
                      edgecolor='none', alpha=0.8))


def draw_state(ax, pos, name, is_initial=False, is_final=False):
    """Desenha um estado (círculo) no diagrama."""
    circle = plt.Circle(pos, 0.3, fill=True, facecolor='lightblue',
                        edgecolor='black', linewidth=2)
    ax.add_patch(circle)

    if is_final:
        inner = plt.Circle(pos, 0.24, fill=False,
                           edgecolor='black', linewidth=1.5)
        ax.add_patch(inner)

    if is_initial:
        # Seta de entrada
        arrow_start = (pos[0] - 0.7, pos[1])
        arrow_end = (pos[0] - 0.32, pos[1])
        ax.annotate('', xy=arrow_end, xytext=arrow_start,
                    arrowprops=dict(arrowstyle='->', color='black', lw=2))

    ax.text(pos[0], pos[1], name, fontsize=9, ha='center', va='center',
            fontweight='bold')


# ========================= DIAGRAMA 1: DFA =========================

def generate_dfa_diagram():
    """Gera diagrama do DFA para a linguagem regular."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 4))
    ax.set_xlim(-1.5, 11)
    ax.set_ylim(-2, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Posições dos estados
    positions = {
        'q0': (0, 0),
        'q1': (2.5, 0),
        'q2': (5, 0),
        'q3': (7.5, 0),
        'DEAD': (5, -1.5),
    }

    # Desenhar estados
    draw_state(ax, positions['q0'], 'q0', is_initial=True)
    draw_state(ax, positions['q1'], 'q1')
    draw_state(ax, positions['q2'], 'q2')
    draw_state(ax, positions['q3'], 'q3', is_final=True)
    draw_state(ax, positions['DEAD'], 'DEAD')

    # Transições
    draw_arrow(ax, positions['q0'], positions['q1'], 'LOGIN')
    draw_arrow(ax, positions['q1'], positions['q2'], 'AUTH')
    draw_arrow(ax, positions['q2'], positions['q3'], 'LOGOUT')

    # Self-loop em q2
    draw_self_loop(ax, positions['q2'], 'REQUEST')

    # Transições para DEAD (mostrar apenas algumas representativas)
    draw_arrow(ax, positions['q0'], positions['DEAD'], 'outros', color='red', curve=0.2)
    draw_arrow(ax, positions['q1'], positions['DEAD'], 'outros', color='red', curve=0.0)
    draw_arrow(ax, positions['q3'], positions['DEAD'], 'qualquer', color='red', curve=-0.2)

    # Título
    ax.set_title('DFA — Linguagem Regular\n'
                 r'$L = \{ \mathrm{LOGIN\ AUTH\ REQUEST}^n\ \mathrm{LOGOUT}\ |\ n \geq 0 \}$',
                 fontsize=12, fontweight='bold', pad=10)

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "dfa_regular.png")
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Gerado: {filepath}")


# ========================= DIAGRAMA 2: PDA =========================

def generate_pda_diagram():
    """Gera diagrama do PDA para a linguagem livre de contexto."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.set_xlim(-1.5, 9)
    ax.set_ylim(-2.5, 3)
    ax.set_aspect('equal')
    ax.axis('off')

    # Posições dos estados
    positions = {
        'q0': (2, 0),
        'q1': (6, 0),
        'DEAD': (4, -2),
    }

    # Desenhar estados
    draw_state(ax, positions['q0'], 'q0', is_initial=True)
    draw_state(ax, positions['q1'], 'q1', is_final=True)
    draw_state(ax, positions['DEAD'], 'DEAD')

    # Transição q0 → q1 (aceitação: ε, Z0/Z0)
    draw_arrow(ax, positions['q0'], positions['q1'], 'ε, Z0/Z0', curve=0.0)

    # Self-loops em q0
    # BEGIN empilha
    loop1 = mpatches.FancyArrowPatch(
        (2.15, 0.33), (1.85, 0.33),
        arrowstyle='->', mutation_scale=12,
        connectionstyle="arc3,rad=-1.5",
        color='blue', linewidth=1.5
    )
    ax.add_patch(loop1)
    ax.text(2, 1.0, 'BEGIN, Z0 → BZ0\nBEGIN, B → BB',
            fontsize=7.5, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                      edgecolor='blue', alpha=0.9))

    # END desempilha
    loop2 = mpatches.FancyArrowPatch(
        (1.85, -0.33), (2.15, -0.33),
        arrowstyle='->', mutation_scale=12,
        connectionstyle="arc3,rad=-1.5",
        color='green', linewidth=1.5
    )
    ax.add_patch(loop2)
    ax.text(2, -1.0, 'END, B → ε',
            fontsize=7.5, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                      edgecolor='green', alpha=0.9))

    # Transição para DEAD
    draw_arrow(ax, positions['q0'], positions['DEAD'], 'END, Z0 → Z0', color='red', curve=0.0)

    # Título
    ax.set_title('PDA — Linguagem Livre de Contexto\n'
                 r'$L = \{ w \in \{\mathrm{BEGIN, END}\}^* \ |\ \mathrm{BEGIN/END\ balanceados} \}$',
                 fontsize=12, fontweight='bold', pad=10)

    # Legenda da pilha
    ax.text(7, -1.5, 'Pilha: Γ = {Z0, B}\n'
            'Z0 = marcador de fundo\n'
            'B = marcador de BEGIN',
            fontsize=8, ha='left', va='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                      edgecolor='gray', alpha=0.9))

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "pda_livre_contexto.png")
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Gerado: {filepath}")


# ========================= DIAGRAMA 3: MT =========================

def generate_tm_diagram():
    """Gera diagrama da Máquina de Turing para a linguagem recursiva."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(-2, 12)
    ax.set_ylim(-4, 5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Posições dos estados
    positions = {
        'q0': (2, 2),
        'q1': (6, 2),
        'q2': (10, 2),
        'q3': (6, -1),
        'q4': (2, -1),
        'qA': (0, -3),
        'qR': (10, -1),
    }

    # Desenhar estados
    draw_state(ax, positions['q0'], 'q0', is_initial=True)
    draw_state(ax, positions['q1'], 'q1')
    draw_state(ax, positions['q2'], 'q2')
    draw_state(ax, positions['q3'], 'q3')
    draw_state(ax, positions['q4'], 'q4')
    draw_state(ax, positions['qA'], 'qA', is_final=True)
    draw_state(ax, positions['qR'], 'qR')

    # Transições principais
    draw_arrow(ax, positions['q0'], positions['q1'],
               'OPEN/X_OPEN, R', curve=0.0)
    draw_arrow(ax, positions['q1'], positions['q2'],
               'COMMIT/X_COMMIT, R', curve=0.0)
    draw_arrow(ax, positions['q2'], positions['q3'],
               'CLOSE/X_CLOSE, L', curve=0.2)
    draw_arrow(ax, positions['q3'], positions['q0'],
               'BLANK/BLANK, R', curve=0.2)
    draw_arrow(ax, positions['q0'], positions['q4'],
               'BLANK/BLANK, L', curve=0.0)
    draw_arrow(ax, positions['q4'], positions['qA'],
               'BLANK/BLANK, S', curve=0.0)

    # Transições para rejeição
    draw_arrow(ax, positions['q1'], positions['qR'],
               'BLANK, S', color='red', curve=0.2)
    draw_arrow(ax, positions['q2'], positions['qR'],
               'BLANK, S', color='red', curve=0.0)
    draw_arrow(ax, positions['q0'], positions['qR'],
               'COMMIT|CLOSE, S', color='red', curve=-0.3)

    # Self-loops
    # q0: pula marcados
    ax.text(2, 3.2, 'X_OPEN/R\nX_COMMIT/R\nX_CLOSE/R',
            fontsize=6.5, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow',
                      edgecolor='gray', alpha=0.9))
    loop_q0 = mpatches.FancyArrowPatch(
        (2.15, 2.33), (1.85, 2.33),
        arrowstyle='->', mutation_scale=10,
        connectionstyle="arc3,rad=-1.2",
        color='gray', linewidth=1.2
    )
    ax.add_patch(loop_q0)

    # q1: pula marcados e OPENs
    ax.text(6, 3.2, 'OPEN/R\nX_OPEN/R\nX_COMMIT/R\nX_CLOSE/R',
            fontsize=6.5, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow',
                      edgecolor='gray', alpha=0.9))
    loop_q1 = mpatches.FancyArrowPatch(
        (6.15, 2.33), (5.85, 2.33),
        arrowstyle='->', mutation_scale=10,
        connectionstyle="arc3,rad=-1.2",
        color='gray', linewidth=1.2
    )
    ax.add_patch(loop_q1)

    # q2: pula marcados e COMMITs
    ax.text(10, 3.2, 'COMMIT/R\nX_OPEN/R\nX_COMMIT/R\nX_CLOSE/R',
            fontsize=6.5, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow',
                      edgecolor='gray', alpha=0.9))
    loop_q2 = mpatches.FancyArrowPatch(
        (10.15, 2.33), (9.85, 2.33),
        arrowstyle='->', mutation_scale=10,
        connectionstyle="arc3,rad=-1.2",
        color='gray', linewidth=1.2
    )
    ax.add_patch(loop_q2)

    # q3: volta ao início (qualquer símbolo, L)
    ax.text(6, -2.2, 'qualquer/L',
            fontsize=7, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow',
                      edgecolor='gray', alpha=0.9))
    loop_q3 = mpatches.FancyArrowPatch(
        (5.85, -1.33), (6.15, -1.33),
        arrowstyle='->', mutation_scale=10,
        connectionstyle="arc3,rad=-1.2",
        color='gray', linewidth=1.2
    )
    ax.add_patch(loop_q3)

    # q4: verificação (marcados, L)
    ax.text(2, -2.2, 'X_*/L',
            fontsize=7, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow',
                      edgecolor='gray', alpha=0.9))
    loop_q4 = mpatches.FancyArrowPatch(
        (1.85, -1.33), (2.15, -1.33),
        arrowstyle='->', mutation_scale=10,
        connectionstyle="arc3,rad=-1.2",
        color='gray', linewidth=1.2
    )
    ax.add_patch(loop_q4)

    # Título
    ax.set_title('Máquina de Turing — Linguagem Recursiva\n'
                 r'$L = \{ \mathrm{OPEN}^n\ \mathrm{COMMIT}^n\ \mathrm{CLOSE}^n\ |\ n \geq 1 \}$',
                 fontsize=12, fontweight='bold', pad=10)

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "mt_recursiva.png")
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Gerado: {filepath}")


# ========================= MAIN =========================

if __name__ == "__main__":
    print("Gerando diagramas dos reconhecedores...")
    print()
    generate_dfa_diagram()
    generate_pda_diagram()
    generate_tm_diagram()
    print()
    print("Todos os diagramas gerados na pasta 'diagramas/'")
