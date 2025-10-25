import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fractions import Fraction
import os
import utils

# --- Criar pastas de saída ---
folders = utils.prepare_subfolders("img", "tables", "graphs")  

mass = []
angle = []

with open('data.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line == "":
            continue
        parts = line.split()
        if len(parts) >= 2:
            try:
                m = float(parts[0]) / 1000
                a = np.deg2rad(float(parts[1]))
                mass.append(m)
                angle.append(a)
            except ValueError:
                print(f"Erro ao converter linha: {line}")

mass = np.array(mass)
angle = np.array(angle)

indices = np.where(np.isclose(mass, 0.50405))[0]

mass_groups = []
angle_groups = []
start = 0

for idx in indices:
    m_slice = mass[start:idx+1]
    a_slice = angle[start:idx+1]
    if len(m_slice) > 0:
        mass_groups.append(m_slice)
        angle_groups.append(a_slice)
    start = idx + 1

def angle_to_pi_fraction(rad_value):
    frac = Fraction(rad_value / np.pi).limit_denominator(180)
    num, den = frac.numerator, frac.denominator

    if num == 0:
        return "0"
    elif den == 1:
        return f"{num}π"
    elif num == 1:
        return f"π/{den}"
    else:
        return f"{num}π/{den}"

plt.figure(figsize=(8, 5))
markers = ["o", "s", "d"]

for i in range(len(mass_groups)):
    x = mass_groups[i]
    y = angle_groups[i]
    plt.plot(x, y, marker=markers[i], markersize=8, linewidth=3, label=f'Barra {i+1}')

plt.xlabel("Massa (kg)")
plt.ylabel("Ângulo (rad)")
plt.title("Massa vs Ângulo")
plt.legend()
plt.grid(True)

ax = plt.gca()
y_max = np.pi / 3
yticks = np.linspace(0, y_max, 5)
ax.set_yticks(yticks)
ax.set_yticklabels([angle_to_pi_fraction(r) for r in yticks])

plt.savefig(os.path.join(folders['graphs'], "grafico.png"))  # ✅ alterado para usar pasta 'grafico'
print("✅ Gráfico exibido e salvo como grafico.png")
plt.show()

for i, (m, a) in enumerate(zip(mass_groups, angle_groups), start=1):
    frac_pi = [angle_to_pi_fraction(val) for val in a]

    df = pd.DataFrame({
        "Massa (kg)": np.round(m, 4),
        "Ângulo (π rad)": frac_pi
    })

    fig, ax = plt.subplots(figsize=(4, len(m) * 0.5))
    ax.axis('off')
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.2)

    plt.title(f"Barra {i}")
    plt.savefig(os.path.join(folders['tables'], f"table{i}.png"), bbox_inches='tight', dpi=300)  # ✅ alterado para pasta 'tables'
    plt.close(fig)

print("✅ tabelas salvas como table1.png, table2.png, table3.png ...")

try:
    data2 = pd.read_csv('data2.txt', sep=r'\s+')
    data2.insert(0, "Barra", ["B1", "B2", "B3"])

    data_str = data2.copy()
    numeric_cols = data_str.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        data_str[col] = data_str[col].apply(lambda x: f"{x:.8g}")

    fig, ax = plt.subplots(figsize=(8, 2.5))
    ax.axis('off')

    table = ax.table(
        cellText=data_str.values,
        colLabels=data_str.columns,
        cellLoc='center',
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)

    plt.title("Propriedades das Barras")
    plt.savefig(os.path.join(folders['tables'], "tabela_barras.png"), bbox_inches='tight', dpi=300)  # ✅ alterado para pasta 'tables'
    plt.close(fig)

    print("✅ Tabela das barras salva como tabela_barras.png")

except Exception as e:
    print(f"⚠️ Erro ao ler ou gerar a tabela das barras: {e}")
