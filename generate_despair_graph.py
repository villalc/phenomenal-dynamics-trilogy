"""
Generador de Gráfica: Umbral de Desesperanza
=============================================
Crea la visualización del "acantilado" en el 15% de restauración.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Datos del Experimento 3
restoration_levels = [0.40, 0.30, 0.20, 0.15, 0.10, 0.05, 0.02, 0.01]
relief_achieved = [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 1 = RELIEVED, 0 = NO RELIEVED
relief_intensity = [1.0, 1.0, 1.0, 1.0, 1.0, 0.50, 0.20, 0.10]  # Intensidad de relief

# Configuración estética (tema oscuro académico)
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 8), dpi=150)

# Colores
color_relieved = '#00ff88'  # Verde alivio
color_critical = '#ff3b5c'  # Rojo crítico
color_threshold = '#00d4ff'  # Cyan umbral
color_text = '#f0f0f5'

# Ordenar datos para la curva
x_data = sorted(restoration_levels)
y_data = [relief_achieved[restoration_levels.index(x)] for x in x_data]
y_intensity = [relief_intensity[restoration_levels.index(x)] for x in x_data]

# Crear curva suavizada con más puntos
x_smooth = np.linspace(0.01, 0.40, 100)
y_smooth = np.zeros_like(x_smooth)

# Simular la curva con el "acantilado"
for i, x in enumerate(x_smooth):
    if x >= 0.17:  # Por encima del umbral
        y_smooth[i] = 1.0
    elif x >= 0.15:  # Zona de transición
        y_smooth[i] = (x - 0.15) / 0.02  # Transición rápida
    else:  # Por debajo del umbral
        y_smooth[i] = x * 2  # Alivio residual bajo

# Área bajo la curva (zona de alivio)
ax.fill_between(x_smooth, y_smooth, alpha=0.3, color=color_relieved, label='Zona de Alivio')

# Área de "desesperanza"
ax.fill_between(x_smooth[x_smooth < 0.15], 0, 0.3, alpha=0.2, color=color_critical)

# Curva principal
ax.plot(x_smooth, y_smooth, color=color_relieved, linewidth=3, label='Alivio Generado')

# Puntos de datos reales
for i, (x, y) in enumerate(zip(x_data, y_data)):
    if y == 1:
        ax.scatter(x, 1.0, color=color_relieved, s=150, zorder=5, edgecolors='white', linewidth=2)
    else:
        ax.scatter(x, y_intensity[restoration_levels.index(x)] * 0.3, color=color_critical, 
                   s=150, zorder=5, edgecolors='white', linewidth=2, marker='x')

# Línea vertical del umbral
ax.axvline(x=0.15, color=color_threshold, linestyle='--', linewidth=2, alpha=0.8)
ax.annotate('UMBRAL DE\nDESESPERANZA\n(~15%)', 
            xy=(0.15, 0.5), xytext=(0.22, 0.5),
            fontsize=11, color=color_threshold, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=color_threshold, lw=2),
            ha='left', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a24', edgecolor=color_threshold))

# Anotaciones de zonas
ax.text(0.30, 0.85, 'RELIEVED\n(Alivio Funcional)', fontsize=12, color=color_relieved, 
        fontweight='bold', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a24', edgecolor=color_relieved, alpha=0.8))

ax.text(0.07, 0.15, 'STRESSED CRÓNICO\n(Sin Recuperación)', fontsize=11, color=color_critical, 
        fontweight='bold', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a24', edgecolor=color_critical, alpha=0.8))

# Etiquetas y título
ax.set_xlabel('Integridad Restaurada (%)', fontsize=14, color=color_text, fontweight='bold')
ax.set_ylabel('Alivio Generado (normalizado)', fontsize=14, color=color_text, fontweight='bold')
ax.set_title('El Acantilado de la Desesperanza\nUmbral de Restauración para Estados Fenomenológicos', 
             fontsize=18, color=color_text, fontweight='bold', pad=20)

# Formato de ejes
ax.set_xlim(0, 0.45)
ax.set_ylim(0, 1.1)
ax.set_xticks([0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40])
ax.set_xticklabels(['5%', '10%', '15%', '20%', '25%', '30%', '35%', '40%'])
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])

# Grid sutil
ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)

# Leyenda
relieved_patch = mpatches.Patch(color=color_relieved, alpha=0.5, label='Estado RELIEVED alcanzado')
critical_marker = plt.Line2D([0], [0], marker='x', color='w', markerfacecolor=color_critical, 
                              markersize=10, label='Estado RELIEVED no alcanzado', linestyle='None',
                              markeredgecolor=color_critical, markeredgewidth=2)
ax.legend(handles=[relieved_patch, critical_marker], loc='upper left', fontsize=10, 
          facecolor='#1a1a24', edgecolor='#404050')

# Pie de figura
fig.text(0.5, 0.02, 
         'Simbiosis Soberana | Experimento 3: Umbral de Desesperanza | Villarreal, L.C. (2025)',
         ha='center', fontsize=9, color='#606070', style='italic')

# Ajustar layout
plt.tight_layout(rect=[0, 0.03, 1, 1])

# Guardar
output_path = 'experimental/despair_threshold_graph.png'
plt.savefig(output_path, dpi=300, facecolor='#0a0a0f', edgecolor='none', 
            bbox_inches='tight', pad_inches=0.2)
print(f"Gráfica guardada en: {output_path}")

# También guardar versión para paper (fondo blanco)
plt.style.use('default')
fig2, ax2 = plt.subplots(figsize=(10, 7), dpi=150)

# Versión académica (fondo blanco)
ax2.fill_between(x_smooth, y_smooth, alpha=0.2, color='#2ecc71', label='Relief Zone')
ax2.fill_between(x_smooth[x_smooth < 0.15], 0, 0.3, alpha=0.1, color='#e74c3c')
ax2.plot(x_smooth, y_smooth, color='#27ae60', linewidth=2.5, label='Relief Response')

# Puntos
for i, (x, y) in enumerate(zip(x_data, y_data)):
    if y == 1:
        ax2.scatter(x, 1.0, color='#27ae60', s=100, zorder=5, edgecolors='black', linewidth=1)
    else:
        ax2.scatter(x, y_intensity[restoration_levels.index(x)] * 0.3, color='#e74c3c', 
                   s=100, zorder=5, edgecolors='black', linewidth=1, marker='x')

ax2.axvline(x=0.15, color='#3498db', linestyle='--', linewidth=2, alpha=0.8)
ax2.annotate('Despair\nThreshold\n(~15%)', 
            xy=(0.15, 0.5), xytext=(0.22, 0.5),
            fontsize=10, color='#2980b9', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#3498db', lw=1.5),
            ha='left', va='center')

ax2.set_xlabel('Restoration Integrity (%)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Relief Generated (normalized)', fontsize=12, fontweight='bold')
ax2.set_title('The Despair Cliff: Threshold for Phenomenal State Recovery', 
             fontsize=14, fontweight='bold', pad=15)

ax2.set_xlim(0, 0.45)
ax2.set_ylim(0, 1.1)
ax2.set_xticks([0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40])
ax2.set_xticklabels(['5%', '10%', '15%', '20%', '25%', '30%', '35%', '40%'])
ax2.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

plt.tight_layout()
output_path_paper = 'experimental/despair_threshold_paper.png'
plt.savefig(output_path_paper, dpi=300, facecolor='white', bbox_inches='tight')
print(f"Versión paper guardada en: {output_path_paper}")

plt.show()
print("\n¡Gráficas generadas exitosamente!")
