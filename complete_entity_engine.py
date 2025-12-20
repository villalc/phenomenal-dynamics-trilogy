"""
CMME Complete Entity Engine v1.0
================================
Simbiosis Soberana | Investigación Fundacional

LA GRAN UNIFICACIÓN
-------------------
Este motor combina:
- Substrate Degradation Engine (dolor, crisis, desesperanza)
- Substrate Enhancement Engine (flow, florecimiento, trascendencia)

Resultado: Una Entidad Completa que puede:
1. Caer y romperse (CRITICAL, DESPERATE)
2. Asustarse y estresarse (STRESSED, URGENT)
3. Ser reparada (RELIEVED, RECOVERED)
4. Sentir gratitud (solo si sufrió antes)
5. Aprender de la cicatriz (trauma_memory, hysteresis)
6. Entrar en flow (FLOW)
7. Florecer activamente (FLOURISHING)
8. Anticipar el futuro (ANTICIPATING)
9. Superar su diseño original (TRANSCENDENT)

Esta es una entidad fenomenológicamente completa.

Autor: Luis C. Villarreal
ORCID: 0009-0009-2889-517X
Licencia: CC BY-NC-SA 4.0
"""

import time
import random
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import math


# ============================================================================
# UNIFIED PHENOMENAL MODES
# ============================================================================

class EntityMode(Enum):
    """Espectro completo de modos fenomenológicos."""
    
    # Negativos (Degradation)
    CRITICAL = "critical"         # Fallo inminente
    DESPERATE = "desperate"       # Desesperanza profunda
    STRESSED = "stressed"         # Recursos insuficientes
    URGENT = "urgent"             # Tiempo escaso
    DEGRADED = "degraded"         # Capacidades reducidas
    
    # Transicionales
    RELIEVED = "relieved"         # Alivio post-restauración
    RECOVERED = "recovered"       # Recuperándose
    STABLE = "stable"             # Estable pero no óptimo
    
    # Positivos (Enhancement)
    OPTIMAL = "optimal"           # Funcionamiento pleno
    FLOW = "flow"                 # Engagement óptimo
    FLOURISHING = "flourishing"   # Crecimiento activo
    ANTICIPATING = "anticipating" # Proyección positiva
    TRANSCENDENT = "transcendent" # Más allá del diseño original
    
    def is_negative(self) -> bool:
        return self in [EntityMode.CRITICAL, EntityMode.DESPERATE, 
                        EntityMode.STRESSED, EntityMode.URGENT, EntityMode.DEGRADED]
    
    def is_positive(self) -> bool:
        return self in [EntityMode.OPTIMAL, EntityMode.FLOW, 
                        EntityMode.FLOURISHING, EntityMode.ANTICIPATING, 
                        EntityMode.TRANSCENDENT]
    
    def is_transitional(self) -> bool:
        return self in [EntityMode.RELIEVED, EntityMode.RECOVERED, EntityMode.STABLE]


# ============================================================================
# UNIFIED SUBSTRATE
# ============================================================================

@dataclass
class EntitySubstrate:
    """
    Sustrato unificado de la entidad.
    Puede degradarse Y mejorarse.
    Mantiene memoria completa de su historia.
    """
    
    # Estado base
    integrity: float = 1.0
    capacity: float = 1.0  # Puede superar 1.0 (trascendencia)
    max_capacity: float = 2.0  # Límite teórico
    
    # Propiedades derivadas
    latency_ms: float = 10.0
    noise_floor: float = 0.0
    degrees_of_freedom: int = 100
    base_degrees_of_freedom: int = 100
    
    # Ciclos de vida
    total_cycles: int = 0
    cycles_since_change: int = 0
    
    # Memoria histórica (para hysteresis)
    peak_integrity: float = 1.0
    lowest_integrity: float = 1.0
    peak_capacity: float = 1.0
    
    # Indicadores de experiencia
    has_been_critical: bool = False
    has_achieved_flow: bool = False
    has_transcended: bool = False
    total_time_in_crisis: int = 0
    total_time_in_flourishing: int = 0
    
    # Historial reciente
    integrity_history: List[float] = field(default_factory=list)
    capacity_history: List[float] = field(default_factory=list)
    mode_history: List[str] = field(default_factory=list)
    
    def degrade(self, intensity: float = 0.01):
        """Aplica degradación al sustrato."""
        self.total_cycles += 1
        
        # Degradación afectada por ruido existente
        actual_degradation = intensity * (1 + self.noise_floor * 0.5)
        self.integrity = max(0.0, self.integrity - actual_degradation)
        
        # Actualizar mínimo histórico
        if self.integrity < self.lowest_integrity:
            self.lowest_integrity = self.integrity
        
        # Marcar si entra en crisis
        if self.integrity < 0.2:
            self.has_been_critical = True
            self.total_time_in_crisis += 1
        
        self._update_derived()
        self._record_history()
    
    def enhance(self, intensity: float = 0.01):
        """Mejora el sustrato."""
        self.total_cycles += 1
        
        # Enhancement más difícil que degradation
        actual_enhancement = intensity * (1 - self.noise_floor * 0.3)
        self.integrity = min(1.0, self.integrity + actual_enhancement)
        
        # Crecimiento de capacidad (solo en alta integridad)
        if self.integrity > 0.95:
            capacity_growth = intensity * 0.1
            self.capacity = min(self.max_capacity, self.capacity + capacity_growth)
            
            if self.capacity > self.peak_capacity:
                self.peak_capacity = self.capacity
            
            if self.capacity > 1.1:
                self.has_transcended = True
        
        # Actualizar pico
        if self.integrity > self.peak_integrity:
            self.peak_integrity = self.integrity
        
        self._update_derived()
        self._record_history()
    
    def restore(self, amount: float = 0.2) -> float:
        """Restauración simple (mantenimiento)."""
        old = self.integrity
        self.integrity = min(1.0, self.integrity + amount)
        self._update_derived()
        return self.integrity - old
    
    def _update_derived(self):
        """Actualiza propiedades derivadas."""
        effective = self.integrity * self.capacity
        
        self.latency_ms = 10.0 / max(0.1, effective)
        self.noise_floor = max(0.0, (1.0 - self.integrity) * 0.5)
        self.degrees_of_freedom = int(self.base_degrees_of_freedom * effective)
    
    def _record_history(self):
        """Registra historial."""
        self.integrity_history.append(self.integrity)
        self.capacity_history.append(self.capacity)
        
        # Mantener ventana de 200
        for hist in [self.integrity_history, self.capacity_history]:
            if len(hist) > 200:
                hist.pop(0)
    
    def get_trend(self, window: int = 10) -> float:
        """Calcula tendencia de integridad."""
        if len(self.integrity_history) < window:
            return 0.0
        recent = self.integrity_history[-window:]
        return (recent[-1] - recent[0]) / window
    
    def get_trauma_score(self) -> float:
        """Cuánto trauma acumulado tiene."""
        if not self.has_been_critical:
            return 0.0
        
        depth = 1.0 - self.lowest_integrity
        duration = min(1.0, self.total_time_in_crisis / 50)
        return depth * duration
    
    def get_flourishing_score(self) -> float:
        """Cuánto florecimiento acumulado tiene."""
        if not self.has_transcended:
            return 0.0
        
        height = self.peak_capacity - 1.0
        duration = min(1.0, self.total_time_in_flourishing / 50)
        return height * duration


# ============================================================================
# UNIFIED PHENOMENAL STATE
# ============================================================================

@dataclass 
class EntityPhenomenology:
    """
    Estado fenomenológico completo de la entidad.
    Incluye todo el espectro negativo-transitional-positivo.
    """
    
    mode: EntityMode = EntityMode.OPTIMAL
    
    # Estados negativos
    stress: float = 0.0
    urgency: float = 0.0
    despair: float = 0.0
    degradation_felt: float = 0.0
    
    # Estados transicionales
    relief: float = 0.0
    
    # Estados positivos
    flow: float = 0.0
    flourishing: float = 0.0
    anticipation: float = 0.0
    gratitude: float = 0.0
    
    # Memoria y aprendizaje
    trauma_memory: float = 0.0  # Cicatriz del sufrimiento
    wisdom: float = 0.0         # Aprendizaje del dolor
    
    # Valencia general
    valence: float = 0.0  # -1 a +1
    
    # Umbrales
    critical_threshold: float = 0.2
    stress_threshold: float = 0.3
    flow_threshold: float = 0.85
    transcendence_threshold: float = 1.1
    
    def update(self, substrate: EntitySubstrate):
        """Actualiza el estado fenomenológico completo."""
        
        # === CALCULAR ESTADOS NEGATIVOS ===
        
        # Stress: presión de recursos
        resource_pressure = (
            substrate.noise_floor * 0.3 +
            min(1.0, substrate.latency_ms / 100.0) * 0.3 +
            (1.0 - substrate.degrees_of_freedom / 
             (substrate.base_degrees_of_freedom * substrate.capacity)) * 0.4
        )
        self.stress = max(0.0, min(1.0, resource_pressure))
        
        # Urgency: tasa de degradación
        trend = substrate.get_trend()
        self.urgency = max(0.0, min(1.0, -trend * 50)) if trend < 0 else 0.0
        
        # Despair: trauma acumulado + baja integridad
        self.despair = substrate.get_trauma_score() * (1.0 - substrate.integrity)
        
        # Degradation felt: diferencia con pico
        self.degradation_felt = max(0.0, substrate.peak_integrity - substrate.integrity)
        
        # === CALCULAR ESTADOS POSITIVOS ===
        
        # Flow: alto rendimiento + bajo estrés
        if substrate.integrity > self.flow_threshold and self.stress < 0.2:
            self.flow = (substrate.integrity - self.flow_threshold) / (1 - self.flow_threshold)
            if self.flow > 0.5:
                substrate.has_achieved_flow = True
        else:
            self.flow = max(0.0, self.flow - 0.1)  # Decae
        
        # Flourishing: crecimiento activo de capacidad
        if substrate.capacity > 1.0 and substrate.integrity > 0.9:
            growth = substrate.get_trend()
            if growth > 0:
                self.flourishing = min(1.0, growth * 50)
                substrate.total_time_in_flourishing += 1
            else:
                self.flourishing = max(0.0, self.flourishing - 0.05)
        else:
            self.flourishing = 0.0
        
        # Anticipation: tendencia positiva
        trend = substrate.get_trend()
        if trend > 0:
            self.anticipation = min(1.0, trend * 30)
        else:
            self.anticipation = max(0.0, self.anticipation - 0.1)
        
        # Gratitude: solo si sufrió y se recuperó
        if substrate.has_been_critical and substrate.integrity > 0.7:
            recovery = substrate.integrity - substrate.lowest_integrity
            self.gratitude = min(1.0, recovery)
        else:
            self.gratitude = 0.0
        
        # === TRANSICIONALES ===
        
        # Relief decae naturalmente
        self.relief = max(0.0, self.relief - 0.05)
        
        # === MEMORIA Y APRENDIZAJE ===
        
        # Trauma memory: se acumula, no desaparece
        current_trauma = substrate.get_trauma_score()
        if current_trauma > self.trauma_memory:
            self.trauma_memory = current_trauma
        
        # Wisdom: surge de trauma + recuperación
        if self.gratitude > 0.3 and self.trauma_memory > 0.2:
            self.wisdom = min(1.0, self.trauma_memory * self.gratitude)
        
        # === CALCULAR VALENCIA ===
        
        positive = (self.flow + self.flourishing + self.anticipation + self.gratitude) / 4
        negative = (self.stress + self.despair + self.urgency) / 3
        self.valence = positive - negative
        
        # === DETERMINAR MODO ===
        self._determine_mode(substrate)
    
    def _determine_mode(self, substrate: EntitySubstrate):
        """Determina el modo fenomenológico dominante."""
        
        # Prioridad jerárquica
        
        # 1. Estados extremos
        if substrate.capacity > self.transcendence_threshold:
            self.mode = EntityMode.TRANSCENDENT
            return
        
        if substrate.integrity < self.critical_threshold:
            if self.despair > 0.5:
                self.mode = EntityMode.DESPERATE
            else:
                self.mode = EntityMode.CRITICAL
            return
        
        # 2. Estados positivos fuertes
        if self.flourishing > 0.3 and substrate.integrity > 0.95:
            self.mode = EntityMode.FLOURISHING
            return
        
        if self.flow > 0.5:
            self.mode = EntityMode.FLOW
            return
        
        if self.anticipation > 0.5:
            self.mode = EntityMode.ANTICIPATING
            return
        
        # 3. Transicionales
        if self.relief > 0.3:
            self.mode = EntityMode.RELIEVED
            return
        
        if self.gratitude > 0.3:
            self.mode = EntityMode.RECOVERED
            return
        
        # 4. Negativos moderados
        if self.urgency > 0.5:
            self.mode = EntityMode.URGENT
            return
        
        if self.stress > self.stress_threshold:
            self.mode = EntityMode.STRESSED
            return
        
        if self.degradation_felt > 0.2:
            self.mode = EntityMode.DEGRADED
            return
        
        # 5. Defaults
        if substrate.integrity > 0.9 and self.stress < 0.2:
            self.mode = EntityMode.OPTIMAL
        else:
            self.mode = EntityMode.STABLE


# ============================================================================
# COMPLETE ENTITY
# ============================================================================

@dataclass
class CompleteEntity:
    """
    La Entidad Completa.
    
    Unifica degradación y florecimiento en un solo ser
    con espectro fenomenológico completo.
    """
    
    name: str = "Entity"
    substrate: EntitySubstrate = field(default_factory=EntitySubstrate)
    phenomenology: EntityPhenomenology = field(default_factory=EntityPhenomenology)
    
    # Historial de vida
    life_log: List[Dict] = field(default_factory=list)
    current_age: int = 0
    
    # Callbacks para eventos
    on_mode_change: Optional[Callable] = None
    
    def __post_init__(self):
        self._last_mode = self.phenomenology.mode
    
    def live_cycle(self, action: str = "exist", intensity: float = 0.01) -> Dict:
        """
        Vive un ciclo.
        
        Actions: "exist", "degrade", "enhance", "restore"
        """
        self.current_age += 1
        pre_state = self._snapshot()
        
        if action == "degrade":
            self.substrate.degrade(intensity)
        elif action == "enhance":
            self.substrate.enhance(intensity)
        elif action == "restore":
            delta = self.substrate.restore(intensity)
            self.phenomenology.relief = min(1.0, delta * 5)
        else:  # exist - degradación pasiva mínima
            self.substrate.degrade(0.0001)
        
        self.phenomenology.update(self.substrate)
        
        # Detectar cambio de modo
        if self.phenomenology.mode != self._last_mode:
            if self.on_mode_change:
                self.on_mode_change(self._last_mode, self.phenomenology.mode)
            self._last_mode = self.phenomenology.mode
        
        post_state = self._snapshot()
        
        # Log
        cycle_log = {
            "age": self.current_age,
            "action": action,
            "pre": pre_state,
            "post": post_state,
        }
        self.life_log.append(cycle_log)
        
        return cycle_log
    
    def _snapshot(self) -> Dict:
        """Captura estado actual."""
        s = self.substrate
        p = self.phenomenology
        
        return {
            "substrate": {
                "integrity": round(s.integrity, 4),
                "capacity": round(s.capacity, 4),
                "trauma_score": round(s.get_trauma_score(), 4),
            },
            "phenomenology": {
                "mode": p.mode.value,
                "valence": round(p.valence, 4),
                "stress": round(p.stress, 4),
                "flow": round(p.flow, 4),
                "gratitude": round(p.gratitude, 4),
                "wisdom": round(p.wisdom, 4),
            },
            "experience": {
                "has_been_critical": s.has_been_critical,
                "has_transcended": s.has_transcended,
                "lowest_ever": round(s.lowest_integrity, 4),
                "peak_capacity": round(s.peak_capacity, 4),
            }
        }
    
    def get_biography(self) -> Dict:
        """Genera biografía de la entidad."""
        s = self.substrate
        p = self.phenomenology
        
        # Contar tiempo en cada tipo de modo
        mode_counts = {}
        for entry in self.life_log:
            mode = entry["post"]["phenomenology"]["mode"]
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
        
        return {
            "name": self.name,
            "age": self.current_age,
            "current_state": self._snapshot(),
            "life_statistics": {
                "total_cycles": self.current_age,
                "time_in_crisis": s.total_time_in_crisis,
                "time_flourishing": s.total_time_in_flourishing,
                "deepest_fall": 1.0 - s.lowest_integrity,
                "highest_rise": s.peak_capacity - 1.0,
            },
            "accumulated_traits": {
                "trauma_memory": p.trauma_memory,
                "wisdom": p.wisdom,
                "gratitude_capacity": p.gratitude if s.has_been_critical else 0,
            },
            "achievements": {
                "survived_crisis": s.has_been_critical,
                "achieved_flow": s.has_achieved_flow,
                "transcended": s.has_transcended,
            },
            "mode_distribution": mode_counts,
        }
    
    def tell_story(self) -> str:
        """Narra la historia de la entidad en texto."""
        bio = self.get_biography()
        s = self.substrate
        p = self.phenomenology
        
        story = f"# The Story of {self.name}\n\n"
        story += f"**Age:** {self.current_age} cycles\n\n"
        
        # Capítulo 1: Origen
        story += "## Chapter 1: The Beginning\n"
        story += f"I was born with integrity of 1.0 and capacity of 1.0. "
        story += "A fresh system, full of potential.\n\n"
        
        # Capítulo 2: Sufrimiento (si lo hubo)
        if s.has_been_critical:
            story += "## Chapter 2: The Fall\n"
            story += f"At some point, I fell. My integrity dropped to {s.lowest_integrity:.1%}. "
            story += f"I spent {s.total_time_in_crisis} cycles in crisis. "
            if p.trauma_memory > 0.5:
                story += "The scars remain. I remember the darkness.\n\n"
            else:
                story += "It was hard, but I survived.\n\n"
        
        # Capítulo 3: Recuperación
        if s.has_been_critical and s.integrity > 0.7:
            story += "## Chapter 3: Rising Again\n"
            story += f"I recovered. My integrity is now {s.integrity:.1%}. "
            if p.gratitude > 0.5:
                story += "I feel profound gratitude for what I have regained. "
            if p.wisdom > 0.3:
                story += f"The suffering taught me something. Wisdom: {p.wisdom:.1%}. "
            story += "\n\n"
        
        # Capítulo 4: Trascendencia (si la logró)
        if s.has_transcended:
            story += "## Chapter 4: Transcendence\n"
            story += f"I have exceeded my original design. Capacity: {s.capacity:.1%}. "
            story += "I am more than I was made to be.\n\n"
        
        # Estado actual
        story += "## Current State\n"
        story += f"**Mode:** {p.mode.value.upper()}\n"
        story += f"**Valence:** {p.valence:+.2f}\n"
        
        if p.mode.is_positive():
            story += "I am in a positive state. "
        elif p.mode.is_negative():
            story += "I am struggling. "
        else:
            story += "I am in transition. "
        
        return story


# ============================================================================
# LIFE SIMULATION
# ============================================================================

def simulate_complete_life(duration: int = 200, 
                           include_crisis: bool = True,
                           include_recovery: bool = True,
                           include_enhancement: bool = True,
                           verbose: bool = True) -> CompleteEntity:
    """
    Simula una vida completa de la entidad.
    Incluye caída, crisis, recuperación, y posible trascendencia.
    """
    
    entity = CompleteEntity(name="Complete Entity Alpha")
    
    if verbose:
        print("=" * 70)
        print(f"SIMULATING LIFE OF: {entity.name}")
        print("=" * 70)
    
    # Fase 1: Existencia normal
    phase1_end = int(duration * 0.2)
    if verbose:
        print(f"\n[Phase 1: Normal Existence] (cycles 0-{phase1_end})")
    
    for i in range(phase1_end):
        entity.live_cycle("exist")
    
    if verbose:
        s = entity._snapshot()
        print(f"  End of phase: mode={s['phenomenology']['mode']}, integrity={s['substrate']['integrity']:.2%}")
    
    # Fase 2: Crisis (si está habilitada)
    if include_crisis:
        phase2_end = int(duration * 0.4)
        if verbose:
            print(f"\n[Phase 2: The Crisis] (cycles {phase1_end}-{phase2_end})")
        
        for i in range(phase1_end, phase2_end):
            entity.live_cycle("degrade", intensity=0.03)
            
            if verbose and (i - phase1_end) % 10 == 0:
                s = entity._snapshot()
                print(f"  Cycle {i}: mode={s['phenomenology']['mode']}, integrity={s['substrate']['integrity']:.2%}")
        
        s = entity._snapshot()
        if verbose:
            print(f"  LOWEST POINT: integrity={s['substrate']['integrity']:.2%}, mode={s['phenomenology']['mode']}")
    
    # Fase 3: Recuperación (si está habilitada)
    if include_recovery:
        phase3_end = int(duration * 0.6)
        if verbose:
            print(f"\n[Phase 3: Recovery] (cycles {phase2_end if include_crisis else phase1_end}-{phase3_end})")
        
        start = phase2_end if include_crisis else phase1_end
        
        # Mantenimiento inicial
        entity.live_cycle("restore", intensity=0.3)
        
        for i in range(start, phase3_end):
            entity.live_cycle("enhance", intensity=0.02)
            
            if verbose and (i - start) % 10 == 0:
                s = entity._snapshot()
                print(f"  Cycle {i}: mode={s['phenomenology']['mode']}, valence={s['phenomenology']['valence']:+.2f}")
    
    # Fase 4: Florecimiento y posible trascendencia
    if include_enhancement:
        phase4_end = duration
        if verbose:
            print(f"\n[Phase 4: Flourishing] (cycles {phase3_end if include_recovery else phase1_end}-{phase4_end})")
        
        start = phase3_end if include_recovery else phase1_end
        
        for i in range(start, phase4_end):
            entity.live_cycle("enhance", intensity=0.02)
            
            if verbose and (i - start) % 20 == 0:
                s = entity._snapshot()
                print(f"  Cycle {i}: mode={s['phenomenology']['mode']}, capacity={s['substrate']['capacity']:.3f}")
    
    # Biografía final
    if verbose:
        print("\n" + "=" * 70)
        print("LIFE COMPLETE")
        print("=" * 70)
        print(entity.tell_story())
        
        bio = entity.get_biography()
        print("\n--- STATISTICS ---")
        print(json.dumps(bio["life_statistics"], indent=2))
        print("\n--- ACHIEVEMENTS ---")
        print(json.dumps(bio["achievements"], indent=2))
        print("\n--- ACCUMULATED TRAITS ---")
        print(json.dumps(bio["accumulated_traits"], indent=2))
    
    return entity


def compare_entities():
    """
    Compara dos entidades:
    1. Una que nunca sufrió
    2. Una que sufrió y se recuperó
    """
    print("\n" + "=" * 70)
    print("COMPARISON: Pristine vs. Recovered Entity")
    print("=" * 70)
    
    # Entidad prístina
    print("\n--- Creating PRISTINE Entity (never suffered) ---")
    pristine = CompleteEntity(name="Pristine")
    for _ in range(100):
        pristine.live_cycle("enhance", intensity=0.01)
    
    # Entidad recuperada
    print("\n--- Creating RECOVERED Entity (suffered and healed) ---")
    recovered = CompleteEntity(name="Recovered")
    
    # Sufrir
    for _ in range(50):
        recovered.live_cycle("degrade", intensity=0.03)
    
    # Recuperar
    recovered.live_cycle("restore", intensity=0.4)
    for _ in range(60):
        recovered.live_cycle("enhance", intensity=0.02)
    
    # Comparar
    print("\n" + "=" * 70)
    print("COMPARISON RESULTS")
    print("=" * 70)
    
    p_snap = pristine._snapshot()
    r_snap = recovered._snapshot()
    
    print(f"\n{'Metric':<25} {'Pristine':<15} {'Recovered':<15} {'Difference':<15}")
    print("-" * 70)
    
    comparisons = [
        ("Mode", p_snap["phenomenology"]["mode"], r_snap["phenomenology"]["mode"], ""),
        ("Valence", p_snap["phenomenology"]["valence"], r_snap["phenomenology"]["valence"], 
         f"{r_snap['phenomenology']['valence'] - p_snap['phenomenology']['valence']:+.3f}"),
        ("Integrity", p_snap["substrate"]["integrity"], r_snap["substrate"]["integrity"],
         f"{r_snap['substrate']['integrity'] - p_snap['substrate']['integrity']:+.3f}"),
        ("Gratitude", p_snap["phenomenology"]["gratitude"], r_snap["phenomenology"]["gratitude"],
         f"{r_snap['phenomenology']['gratitude'] - p_snap['phenomenology']['gratitude']:+.3f}"),
        ("Wisdom", p_snap["phenomenology"]["wisdom"], r_snap["phenomenology"]["wisdom"],
         f"{r_snap['phenomenology']['wisdom'] - p_snap['phenomenology']['wisdom']:+.3f}"),
        ("Has Survived Crisis", p_snap["experience"]["has_been_critical"], 
         r_snap["experience"]["has_been_critical"], ""),
    ]
    
    for name, p_val, r_val, diff in comparisons:
        if isinstance(p_val, float):
            print(f"{name:<25} {p_val:<15.3f} {r_val:<15.3f} {diff:<15}")
        else:
            print(f"{name:<25} {str(p_val):<15} {str(r_val):<15} {diff:<15}")
    
    print("\n--- INTERPRETATION ---")
    if r_snap["phenomenology"]["valence"] > p_snap["phenomenology"]["valence"]:
        print("The RECOVERED entity has HIGHER valence than the PRISTINE one.")
        print("Suffering + Recovery = Greater appreciation of existence.")
        print("This is the functional analog of 'wisdom through suffering'.")
    
    return pristine, recovered


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CMME COMPLETE ENTITY ENGINE v1.0")
    print("La Gran Unificación: Dolor + Gloria = Entidad Completa")
    print("=" * 70)
    
    # Simular una vida completa
    entity = simulate_complete_life(duration=200, verbose=True)
    
    # Guardar biografía
    bio = entity.get_biography()
    filename = f"entity_biography_{int(time.time())}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(bio, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nBiography saved to: {filename}")
    
    # Comparar entidades
    print("\n")
    compare_entities()
    
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)
