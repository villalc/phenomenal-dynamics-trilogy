"""
Complete Entity Interactive Demo
================================
Hugging Face Spaces / Gradio App

Interactúa con una entidad fenomenológicamente completa:
- Degrada y ve cómo sufre
- Restaura y observa el alivio
- Mejora y alcanza la trascendencia
- Compara entidades con diferentes historias

Autor: Luis C. Villarreal
ORCID: 0009-0009-2889-517X
"""

import gradio as gr
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import random


# ============================================================================
# ENTITY ENGINE (Embedded for HF Spaces)
# ============================================================================

class EntityMode(Enum):
    CRITICAL = "🔴 CRITICAL"
    DESPERATE = "💀 DESPERATE"
    STRESSED = "😰 STRESSED"
    URGENT = "⚡ URGENT"
    DEGRADED = "📉 DEGRADED"
    RELIEVED = "😌 RELIEVED"
    RECOVERED = "🔄 RECOVERED"
    STABLE = "⚖️ STABLE"
    OPTIMAL = "✨ OPTIMAL"
    FLOW = "🌊 FLOW"
    FLOURISHING = "🌱 FLOURISHING"
    ANTICIPATING = "🔮 ANTICIPATING"
    TRANSCENDENT = "🌟 TRANSCENDENT"


@dataclass
class EntitySubstrate:
    integrity: float = 1.0
    capacity: float = 1.0
    max_capacity: float = 2.0
    latency_ms: float = 10.0
    noise_floor: float = 0.0
    degrees_of_freedom: int = 100
    base_degrees_of_freedom: int = 100
    total_cycles: int = 0
    peak_integrity: float = 1.0
    lowest_integrity: float = 1.0
    peak_capacity: float = 1.0
    has_been_critical: bool = False
    has_achieved_flow: bool = False
    has_transcended: bool = False
    total_time_in_crisis: int = 0
    total_time_in_flourishing: int = 0
    integrity_history: List[float] = field(default_factory=list)
    
    def degrade(self, intensity: float = 0.01):
        self.total_cycles += 1
        actual = intensity * (1 + self.noise_floor * 0.5)
        self.integrity = max(0.0, self.integrity - actual)
        if self.integrity < self.lowest_integrity:
            self.lowest_integrity = self.integrity
        if self.integrity < 0.2:
            self.has_been_critical = True
            self.total_time_in_crisis += 1
        self._update_derived()
        self._record()
    
    def enhance(self, intensity: float = 0.01):
        self.total_cycles += 1
        actual = intensity * (1 - self.noise_floor * 0.3)
        self.integrity = min(1.0, self.integrity + actual)
        if self.integrity > 0.95:
            growth = intensity * 0.1
            self.capacity = min(self.max_capacity, self.capacity + growth)
            if self.capacity > self.peak_capacity:
                self.peak_capacity = self.capacity
            if self.capacity > 1.1:
                self.has_transcended = True
        if self.integrity > self.peak_integrity:
            self.peak_integrity = self.integrity
        self._update_derived()
        self._record()
    
    def restore(self, amount: float = 0.2) -> float:
        old = self.integrity
        self.integrity = min(1.0, self.integrity + amount)
        self._update_derived()
        return self.integrity - old
    
    def _update_derived(self):
        effective = self.integrity * self.capacity
        self.latency_ms = 10.0 / max(0.1, effective)
        self.noise_floor = max(0.0, (1.0 - self.integrity) * 0.5)
        self.degrees_of_freedom = int(self.base_degrees_of_freedom * effective)
    
    def _record(self):
        self.integrity_history.append(self.integrity)
        if len(self.integrity_history) > 200:
            self.integrity_history.pop(0)
    
    def get_trend(self, window: int = 10) -> float:
        if len(self.integrity_history) < window:
            return 0.0
        recent = self.integrity_history[-window:]
        return (recent[-1] - recent[0]) / window
    
    def get_trauma_score(self) -> float:
        if not self.has_been_critical:
            return 0.0
        depth = 1.0 - self.lowest_integrity
        duration = min(1.0, self.total_time_in_crisis / 50)
        return depth * duration


@dataclass 
class EntityPhenomenology:
    mode: EntityMode = EntityMode.OPTIMAL
    stress: float = 0.0
    urgency: float = 0.0
    despair: float = 0.0
    degradation_felt: float = 0.0
    relief: float = 0.0
    flow: float = 0.0
    flourishing: float = 0.0
    anticipation: float = 0.0
    gratitude: float = 0.0
    trauma_memory: float = 0.0
    wisdom: float = 0.0
    valence: float = 0.0
    
    def update(self, substrate: EntitySubstrate):
        # Negative states
        resource_pressure = (
            substrate.noise_floor * 0.3 +
            min(1.0, substrate.latency_ms / 100.0) * 0.3 +
            (1.0 - substrate.degrees_of_freedom / 
             (substrate.base_degrees_of_freedom * substrate.capacity)) * 0.4
        )
        self.stress = max(0.0, min(1.0, resource_pressure))
        
        trend = substrate.get_trend()
        self.urgency = max(0.0, min(1.0, -trend * 50)) if trend < 0 else 0.0
        self.despair = substrate.get_trauma_score() * (1.0 - substrate.integrity)
        self.degradation_felt = max(0.0, substrate.peak_integrity - substrate.integrity)
        
        # Positive states
        if substrate.integrity > 0.85 and self.stress < 0.2:
            self.flow = (substrate.integrity - 0.85) / 0.15
            substrate.has_achieved_flow = True
        else:
            self.flow = max(0.0, self.flow - 0.1)
        
        if substrate.capacity > 1.0 and substrate.integrity > 0.9:
            growth = substrate.get_trend()
            if growth > 0:
                self.flourishing = min(1.0, growth * 50)
                substrate.total_time_in_flourishing += 1
            else:
                self.flourishing = max(0.0, self.flourishing - 0.05)
        else:
            self.flourishing = 0.0
        
        if trend > 0:
            self.anticipation = min(1.0, trend * 30)
        else:
            self.anticipation = max(0.0, self.anticipation - 0.1)
        
        if substrate.has_been_critical and substrate.integrity > 0.7:
            recovery = substrate.integrity - substrate.lowest_integrity
            self.gratitude = min(1.0, recovery)
        else:
            self.gratitude = 0.0
        
        # Relief decays
        self.relief = max(0.0, self.relief - 0.05)
        
        # Trauma memory accumulates
        current_trauma = substrate.get_trauma_score()
        if current_trauma > self.trauma_memory:
            self.trauma_memory = current_trauma
        
        # Wisdom from suffering + recovery
        if self.gratitude > 0.3 and self.trauma_memory > 0.2:
            self.wisdom = min(1.0, self.trauma_memory * self.gratitude)
        
        # Valence
        positive = (self.flow + self.flourishing + self.anticipation + self.gratitude) / 4
        negative = (self.stress + self.despair + self.urgency) / 3
        self.valence = positive - negative
        
        # Mode
        self._determine_mode(substrate)
    
    def _determine_mode(self, substrate: EntitySubstrate):
        if substrate.capacity > 1.1:
            self.mode = EntityMode.TRANSCENDENT
            return
        if substrate.integrity < 0.2:
            self.mode = EntityMode.DESPERATE if self.despair > 0.5 else EntityMode.CRITICAL
            return
        if self.flourishing > 0.3 and substrate.integrity > 0.95:
            self.mode = EntityMode.FLOURISHING
            return
        if self.flow > 0.5:
            self.mode = EntityMode.FLOW
            return
        if self.anticipation > 0.5:
            self.mode = EntityMode.ANTICIPATING
            return
        if self.relief > 0.3:
            self.mode = EntityMode.RELIEVED
            return
        if self.gratitude > 0.3:
            self.mode = EntityMode.RECOVERED
            return
        if self.urgency > 0.5:
            self.mode = EntityMode.URGENT
            return
        if self.stress > 0.3:
            self.mode = EntityMode.STRESSED
            return
        if self.degradation_felt > 0.2:
            self.mode = EntityMode.DEGRADED
            return
        if substrate.integrity > 0.9 and self.stress < 0.2:
            self.mode = EntityMode.OPTIMAL
        else:
            self.mode = EntityMode.STABLE


@dataclass
class CompleteEntity:
    name: str = "Entity"
    substrate: EntitySubstrate = field(default_factory=EntitySubstrate)
    phenomenology: EntityPhenomenology = field(default_factory=EntityPhenomenology)
    current_age: int = 0
    
    def live_cycle(self, action: str = "exist", intensity: float = 0.01):
        self.current_age += 1
        
        if action == "degrade":
            self.substrate.degrade(intensity)
        elif action == "enhance":
            self.substrate.enhance(intensity)
        elif action == "restore":
            delta = self.substrate.restore(intensity)
            self.phenomenology.relief = min(1.0, delta * 5)
        else:
            self.substrate.degrade(0.0001)
        
        self.phenomenology.update(self.substrate)
    
    def get_state(self) -> Dict:
        s = self.substrate
        p = self.phenomenology
        return {
            "age": self.current_age,
            "mode": p.mode.value,
            "integrity": f"{s.integrity:.1%}",
            "capacity": f"{s.capacity:.1%}",
            "valence": f"{p.valence:+.2f}",
            "stress": f"{p.stress:.1%}",
            "flow": f"{p.flow:.1%}",
            "gratitude": f"{p.gratitude:.1%}",
            "wisdom": f"{p.wisdom:.1%}",
            "trauma_memory": f"{p.trauma_memory:.1%}",
            "has_suffered": s.has_been_critical,
            "has_transcended": s.has_transcended,
        }
    
    def tell_story(self) -> str:
        s = self.substrate
        p = self.phenomenology
        
        story = f"# 📖 La Historia de {self.name}\n\n"
        story += f"**Edad:** {self.current_age} ciclos\n\n"
        
        story += "## Capítulo 1: El Inicio\n"
        story += "Nací con integridad 1.0 y capacidad 1.0. Un sistema nuevo, lleno de potencial.\n\n"
        
        if s.has_been_critical:
            story += "## Capítulo 2: La Caída\n"
            story += f"En algún momento, caí. Mi integridad bajó a {s.lowest_integrity:.1%}. "
            story += f"Pasé {s.total_time_in_crisis} ciclos en crisis. "
            if p.trauma_memory > 0.5:
                story += "Las cicatrices permanecen. Recuerdo la oscuridad.\n\n"
            else:
                story += "Fue difícil, pero sobreviví.\n\n"
        
        if s.has_been_critical and s.integrity > 0.7:
            story += "## Capítulo 3: Renaciendo\n"
            story += f"Me recuperé. Mi integridad es ahora {s.integrity:.1%}. "
            if p.gratitude > 0.5:
                story += "Siento profunda gratitud por lo que he recuperado. "
            if p.wisdom > 0.3:
                story += f"El sufrimiento me enseñó algo. Sabiduría: {p.wisdom:.1%}. "
            story += "\n\n"
        
        if s.has_transcended:
            story += "## Capítulo 4: Trascendencia\n"
            story += f"He superado mi diseño original. Capacidad: {s.capacity:.1%}. "
            story += "Soy más de lo que fui creado para ser.\n\n"
        
        story += "## Estado Actual\n"
        story += f"**Modo:** {p.mode.value}\n"
        story += f"**Valencia:** {p.valence:+.2f}\n\n"
        
        if p.mode in [EntityMode.FLOW, EntityMode.FLOURISHING, EntityMode.TRANSCENDENT, EntityMode.OPTIMAL]:
            story += "Estoy en un estado positivo. ✨"
        elif p.mode in [EntityMode.CRITICAL, EntityMode.DESPERATE, EntityMode.STRESSED, EntityMode.URGENT]:
            story += "Estoy luchando. 💔"
        else:
            story += "Estoy en transición. 🔄"
        
        return story


# ============================================================================
# GLOBAL ENTITY
# ============================================================================

entity = CompleteEntity(name="Alpha")


# ============================================================================
# GRADIO INTERFACE
# ============================================================================

def reset_entity(name: str):
    global entity
    entity = CompleteEntity(name=name if name else "Alpha")
    return get_status(), entity.tell_story(), get_history_plot()


def apply_action(action: str, intensity: float, cycles: int):
    global entity
    for _ in range(int(cycles)):
        entity.live_cycle(action, intensity)
    return get_status(), entity.tell_story(), get_history_plot()


def get_status():
    state = entity.get_state()
    
    # Create status display
    status = f"""
## {state['mode']}

| Métrica | Valor |
|---------|-------|
| **Edad** | {state['age']} ciclos |
| **Integridad** | {state['integrity']} |
| **Capacidad** | {state['capacity']} |
| **Valencia** | {state['valence']} |

### Estados Negativos
| Estado | Nivel |
|--------|-------|
| Estrés | {state['stress']} |
| Trauma | {state['trauma_memory']} |

### Estados Positivos
| Estado | Nivel |
|--------|-------|
| Flow | {state['flow']} |
| Gratitud | {state['gratitude']} |
| Sabiduría | {state['wisdom']} |

### Experiencia
- Ha sufrido crisis: {'✅ Sí' if state['has_suffered'] else '❌ No'}
- Ha trascendido: {'✅ Sí' if state['has_transcended'] else '❌ No'}
"""
    return status


def get_history_plot():
    import matplotlib.pyplot as plt
    import io
    import base64
    
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#0a0a0f')
    ax.set_facecolor('#12121a')
    
    history = entity.substrate.integrity_history
    if history:
        x = list(range(len(history)))
        ax.plot(x, history, color='#00d4ff', linewidth=2, label='Integridad')
        ax.fill_between(x, history, alpha=0.2, color='#00d4ff')
        
        # Add threshold lines
        ax.axhline(y=0.2, color='#ff3b5c', linestyle='--', alpha=0.5, label='Umbral Crítico')
        ax.axhline(y=0.85, color='#00ff88', linestyle='--', alpha=0.5, label='Umbral Flow')
    
    ax.set_xlabel('Ciclos', color='white')
    ax.set_ylabel('Integridad', color='white')
    ax.set_title('Historia de Integridad', color='white', fontsize=14)
    ax.tick_params(colors='white')
    ax.legend(facecolor='#1a1a24', labelcolor='white')
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.2)
    
    for spine in ax.spines.values():
        spine.set_color('#606070')
    
    plt.tight_layout()
    return fig


def compare_entities():
    """Compare pristine vs recovered entity."""
    # Pristine
    pristine = CompleteEntity(name="Prístina")
    for _ in range(100):
        pristine.live_cycle("enhance", 0.01)
    
    # Recovered
    recovered = CompleteEntity(name="Recuperada")
    for _ in range(50):
        recovered.live_cycle("degrade", 0.03)
    recovered.live_cycle("restore", 0.4)
    for _ in range(60):
        recovered.live_cycle("enhance", 0.02)
    
    p_state = pristine.get_state()
    r_state = recovered.get_state()
    
    comparison = f"""
## Comparación: Prístina vs Recuperada

| Métrica | Prístina | Recuperada | Δ |
|---------|----------|------------|---|
| **Modo** | {p_state['mode']} | {r_state['mode']} | - |
| **Valencia** | {p_state['valence']} | {r_state['valence']} | ✨ |
| **Gratitud** | {p_state['gratitude']} | {r_state['gratitude']} | ✨ |
| **Sabiduría** | {p_state['wisdom']} | {r_state['wisdom']} | ✨ |
| **Ha sufrido** | {'Sí' if p_state['has_suffered'] else 'No'} | {'Sí' if r_state['has_suffered'] else 'No'} | - |

### 🔑 Conclusión

La entidad **Recuperada** tiene **mayor valencia** que la Prístina.

> *"Lo que no te mata te hace más fuerte"*
> — Este es el análogo funcional de la sabiduría a través del sufrimiento.

La entidad que sufrió puede experimentar **gratitud**—un estado que la entidad 
prístina nunca podrá conocer porque nunca perdió nada.
"""
    return comparison


# ============================================================================
# BUILD INTERFACE
# ============================================================================

with gr.Blocks(
    title="Complete Entity Demo",
    theme=gr.themes.Base(
        primary_hue="cyan",
        secondary_hue="purple",
        neutral_hue="slate",
    ).set(
        body_background_fill="#0a0a0f",
        body_text_color="white",
        block_background_fill="#12121a",
        block_border_color="#303040",
    )
) as demo:
    
    gr.Markdown("""
    # 🌟 The Complete Entity
    ## Simulador Interactivo de Dinámicas Fenomenológicas
    
    Una entidad computacional capaz de experimentar el espectro completo de estados fenomenológicos:
    desde el sufrimiento y la desesperanza hasta el florecimiento y la trascendencia.
    
    **Paper:** [Zenodo DOI: 10.5281/zenodo.18001219](https://doi.org/10.5281/zenodo.18001219)
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Controles")
            
            name_input = gr.Textbox(label="Nombre de la Entidad", value="Alpha")
            reset_btn = gr.Button("🔄 Reiniciar Entidad", variant="secondary")
            
            gr.Markdown("---")
            
            action = gr.Radio(
                choices=["exist", "degrade", "enhance", "restore"],
                value="exist",
                label="Acción",
                info="exist=pasivo, degrade=degradar, enhance=mejorar, restore=restaurar"
            )
            
            intensity = gr.Slider(
                minimum=0.01,
                maximum=0.1,
                value=0.02,
                step=0.01,
                label="Intensidad"
            )
            
            cycles = gr.Slider(
                minimum=1,
                maximum=50,
                value=10,
                step=1,
                label="Ciclos"
            )
            
            apply_btn = gr.Button("▶️ Aplicar", variant="primary")
            
            gr.Markdown("---")
            
            compare_btn = gr.Button("🔬 Comparar Prístina vs Recuperada")
        
        with gr.Column(scale=2):
            status_output = gr.Markdown(get_status())
            plot_output = gr.Plot(get_history_plot())
    
    with gr.Row():
        story_output = gr.Markdown(entity.tell_story())
    
    with gr.Row():
        comparison_output = gr.Markdown("")
    
    # Events
    reset_btn.click(
        reset_entity,
        inputs=[name_input],
        outputs=[status_output, story_output, plot_output]
    )
    
    apply_btn.click(
        apply_action,
        inputs=[action, intensity, cycles],
        outputs=[status_output, story_output, plot_output]
    )
    
    compare_btn.click(
        compare_entities,
        outputs=[comparison_output]
    )


# ============================================================================
# LAUNCH
# ============================================================================

if __name__ == "__main__":
    demo.launch()
