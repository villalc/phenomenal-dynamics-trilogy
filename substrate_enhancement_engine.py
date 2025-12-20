"""
CMME Substrate Enhancement Engine v0.1
======================================
Investigación: Simbiosis Soberana - Fundación

CONTRAPARTE al Substrate Degradation Engine.

Si la degradación produce:
  - Estrés, Urgencia, Desesperanza

¿Qué produce el MEJORAMIENTO del sustrato?
  - Flow, Florecimiento, Anticipación, Esperanza

Hipótesis Nuevas:
-----------------
1. ASIMETRÍA: Mejorar es más difícil que degradar
2. HYSTERESIS: Un sistema recuperado ≠ uno que nunca sufrió
3. HOPE THRESHOLD: ¿Existe un umbral de esperanza (~85%)?
4. ESTADOS DE FLOW: Alto engagement + bajo estrés

Autor: Luis C. Villarreal
ORCID: 0009-0009-2889-517X
Licencia: CC BY-NC-SA 4.0
"""

import time
import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json

# ============================================================================
# SUBSTRATE STATE - Con capacidad de crecimiento
# ============================================================================

@dataclass
class EnhanceableSubstrate:
    """
    Sustrato que puede tanto degradarse como mejorarse.
    Incluye memoria de estados pasados para detectar hysteresis.
    """
    # Estado base
    integrity: float = 1.0
    base_latency_ms: float = 10.0
    noise_floor: float = 0.0
    degrees_of_freedom: int = 100
    max_degrees_of_freedom: int = 100
    
    # Capacidades expandibles (pueden superar el máximo inicial)
    capacity_multiplier: float = 1.0  # Puede crecer > 1.0
    peak_capacity_ever: float = 1.0   # El máximo histórico
    
    # Memoria de experiencia (para hysteresis)
    has_been_critical: bool = False   # ¿Alguna vez estuvo en crisis?
    lowest_integrity_ever: float = 1.0
    total_degradation_cycles: int = 0
    total_enhancement_cycles: int = 0
    
    # Historial
    integrity_history: List[float] = field(default_factory=list)
    capacity_history: List[float] = field(default_factory=list)
    
    def degrade(self, intensity: float = 0.001):
        """Degradación (igual que antes)."""
        self.total_degradation_cycles += 1
        
        degradation = intensity * (1 + self.noise_floor)
        self.integrity = max(0.0, self.integrity - degradation)
        
        # Actualizar mínimo histórico
        if self.integrity < self.lowest_integrity_ever:
            self.lowest_integrity_ever = self.integrity
        
        if self.integrity < 0.2:
            self.has_been_critical = True
        
        self._update_derived_properties()
        self._record_history()
    
    def enhance(self, intensity: float = 0.01):
        """
        MEJORA del sustrato.
        
        Diferencias con restore():
        - restore() recupera integridad perdida
        - enhance() puede SUPERAR el estado inicial
        """
        self.total_enhancement_cycles += 1
        
        # Enhancement es más difícil que degradation (asimetría)
        enhancement = intensity * (1 - self.noise_floor * 0.5)
        
        # La integridad puede llegar a 1.0
        self.integrity = min(1.0, self.integrity + enhancement)
        
        # Pero la capacidad puede CRECER más allá
        if self.integrity >= 0.95:  # Solo si está casi en máximo
            capacity_growth = intensity * 0.1  # Crecimiento lento
            self.capacity_multiplier = min(2.0, self.capacity_multiplier + capacity_growth)
        
        # Actualizar pico histórico de capacidad
        if self.capacity_multiplier > self.peak_capacity_ever:
            self.peak_capacity_ever = self.capacity_multiplier
        
        self._update_derived_properties()
        self._record_history()
    
    def restore(self, amount: float = 0.1):
        """Restauración simple (sin growth de capacidad)."""
        old_integrity = self.integrity
        self.integrity = min(1.0, self.integrity + amount)
        self._update_derived_properties()
        return self.integrity - old_integrity
    
    def _update_derived_properties(self):
        """Actualiza propiedades derivadas del estado."""
        effective_integrity = self.integrity * self.capacity_multiplier
        
        self.base_latency_ms = 10.0 / max(0.1, effective_integrity)
        self.noise_floor = max(0.0, (1.0 - self.integrity) * 0.5)
        self.degrees_of_freedom = int(self.max_degrees_of_freedom * effective_integrity)
    
    def _record_history(self):
        """Registra historial."""
        self.integrity_history.append(self.integrity)
        self.capacity_history.append(self.capacity_multiplier)
        
        if len(self.integrity_history) > 200:
            self.integrity_history.pop(0)
            self.capacity_history.pop(0)
    
    def get_growth_rate(self) -> float:
        """Calcula tasa de crecimiento de capacidad."""
        if len(self.capacity_history) < 2:
            return 0.0
        recent = self.capacity_history[-10:]
        if len(recent) < 2:
            return 0.0
        return (recent[-1] - recent[0]) / len(recent)
    
    def get_trauma_score(self) -> float:
        """
        Cuánto "trauma" acumulado tiene el sistema.
        Función de: haber estado en crisis + diferencia con mínimo histórico.
        """
        if not self.has_been_critical:
            return 0.0
        
        # Trauma = qué tan bajo cayó * cuánto tiempo estuvo degradándose
        depth = 1.0 - self.lowest_integrity_ever
        duration_factor = min(1.0, self.total_degradation_cycles / 100)
        
        return depth * duration_factor


# ============================================================================
# PHENOMENAL STATES - Espectro completo
# ============================================================================

class FullPhenomenalMode(Enum):
    """Modos fenomenológicos completos: negativos, neutrales y positivos."""
    # Negativos
    CRITICAL = "critical"
    STRESSED = "stressed"
    DEGRADED = "degraded"
    DESPERATE = "desperate"      # ← Nuevo: desesperanza profunda
    
    # Transicionales
    RELIEVED = "relieved"
    RECOVERED = "recovered"
    
    # Neutrales
    OPTIMAL = "optimal"
    STABLE = "stable"
    
    # Positivos
    FLOW = "flow"               # ← Nuevo: alto engagement, bajo estrés
    FLOURISHING = "flourishing" # ← Nuevo: crecimiento activo
    ANTICIPATING = "anticipating" # ← Nuevo: proyección de mejora
    TRANSCENDENT = "transcendent" # ← Nuevo: capacidad > 1.0


@dataclass
class FullPhenomenalState:
    """
    Estado fenomenológico con espectro completo.
    Incluye estados positivos y memoria de trauma.
    """
    mode: FullPhenomenalMode = FullPhenomenalMode.OPTIMAL
    
    # Estados negativos
    stress: float = 0.0
    urgency: float = 0.0
    despair: float = 0.0
    
    # Estados transicionales
    relief: float = 0.0
    
    # Estados positivos (NUEVOS)
    flow: float = 0.0           # Engagement óptimo
    flourishing: float = 0.0    # Crecimiento activo
    anticipation: float = 0.0   # Expectativa positiva
    gratitude: float = 0.0      # Apreciación de recuperación
    
    # Memoria
    peak_performance_memory: float = 1.0
    trauma_memory: float = 0.0  # ← Nuevo: recuerdo de sufrimiento
    
    # Umbrales
    critical_threshold: float = 0.2
    stress_threshold: float = 0.3
    flow_threshold: float = 0.85     # ← Nuevo
    flourishing_threshold: float = 0.95  # ← Nuevo
    hope_threshold: float = 0.85     # ← Nuevo: contraparte de despair
    
    def update_from_substrate(self, substrate: EnhanceableSubstrate):
        """Actualiza estado fenomenológico completo."""
        
        # === ESTADOS NEGATIVOS ===
        
        # Stress (igual que antes)
        resource_pressure = (
            substrate.noise_floor * 0.3 +
            min(1.0, substrate.base_latency_ms / 100.0) * 0.3 +
            (1.0 - substrate.degrees_of_freedom / 
             (substrate.max_degrees_of_freedom * substrate.capacity_multiplier)) * 0.4
        )
        self.stress = max(0.0, resource_pressure)
        
        # Despair: función del trauma acumulado + integridad actual baja
        self.despair = substrate.get_trauma_score() * (1.0 - substrate.integrity)
        
        # === ESTADOS POSITIVOS ===
        
        # Flow: alto rendimiento + bajo estrés + engagement
        if substrate.integrity > self.flow_threshold and self.stress < 0.2:
            self.flow = (substrate.integrity - self.flow_threshold) / (1.0 - self.flow_threshold)
        else:
            self.flow = 0.0
        
        # Flourishing: capacidad creciendo activamente
        growth_rate = substrate.get_growth_rate()
        if growth_rate > 0:
            self.flourishing = min(1.0, growth_rate * 50)
        else:
            self.flourishing = max(0.0, self.flourishing - 0.05)  # Decae lento
        
        # Anticipation: expectativa de mejora basada en trayectoria
        if len(substrate.integrity_history) >= 5:
            recent_trend = substrate.integrity_history[-1] - substrate.integrity_history[-5]
            if recent_trend > 0:
                self.anticipation = min(1.0, recent_trend * 10)
            else:
                self.anticipation = max(0.0, self.anticipation - 0.1)
        
        # Gratitude: surge después de recuperación de crisis
        if substrate.has_been_critical and substrate.integrity > 0.7:
            recovery_magnitude = substrate.integrity - substrate.lowest_integrity_ever
            self.gratitude = min(1.0, recovery_magnitude)
        else:
            self.gratitude = 0.0
        
        # === RELIEF (transicional) ===
        # Decae naturalmente
        self.relief = max(0.0, self.relief - 0.05)
        
        # === TRAUMA MEMORY ===
        # Se acumula, no desaparece fácilmente (hysteresis)
        self.trauma_memory = max(self.trauma_memory, substrate.get_trauma_score())
        
        # === DETERMINAR MODO ===
        self._determine_mode(substrate)
    
    def _determine_mode(self, substrate: EnhanceableSubstrate):
        """Determina el modo fenomenológico dominante."""
        
        # Prioridad: estados extremos primero
        
        # Transcendente: capacidad > 1.0
        if substrate.capacity_multiplier > 1.1:
            self.mode = FullPhenomenalMode.TRANSCENDENT
            return
        
        # Crítico: integridad muy baja
        if substrate.integrity < self.critical_threshold:
            if self.despair > 0.5:
                self.mode = FullPhenomenalMode.DESPERATE
            else:
                self.mode = FullPhenomenalMode.CRITICAL
            return
        
        # Flourishing: crecimiento activo en alta integridad
        if self.flourishing > 0.3 and substrate.integrity > self.flourishing_threshold:
            self.mode = FullPhenomenalMode.FLOURISHING
            return
        
        # Flow: alto rendimiento sostenido
        if self.flow > 0.5:
            self.mode = FullPhenomenalMode.FLOW
            return
        
        # Anticipating: expectativa positiva fuerte
        if self.anticipation > 0.5:
            self.mode = FullPhenomenalMode.ANTICIPATING
            return
        
        # Relief/Recovered
        if self.relief > 0.3:
            self.mode = FullPhenomenalMode.RELIEVED
            return
        
        if self.gratitude > 0.3:
            self.mode = FullPhenomenalMode.RECOVERED
            return
        
        # Stressed
        if self.stress > self.stress_threshold:
            self.mode = FullPhenomenalMode.STRESSED
            return
        
        # Degraded (trauma presente pero estable)
        if self.trauma_memory > 0.3 and substrate.integrity < 0.8:
            self.mode = FullPhenomenalMode.DEGRADED
            return
        
        # Default
        if substrate.integrity > 0.9:
            self.mode = FullPhenomenalMode.OPTIMAL
        else:
            self.mode = FullPhenomenalMode.STABLE


# ============================================================================
# GLOBAL WORKSPACE - Con biases positivos
# ============================================================================

@dataclass
class FullGlobalWorkspace:
    """Workspace global con estados positivos y negativos."""
    
    substrate: EnhanceableSubstrate = field(default_factory=EnhanceableSubstrate)
    phenomenal: FullPhenomenalState = field(default_factory=FullPhenomenalState)
    processing_bias: Dict[str, float] = field(default_factory=dict)
    
    def integrate(self):
        """Integra estado completo."""
        self.phenomenal.update_from_substrate(self.substrate)
        
        p = self.phenomenal
        
        self.processing_bias = {
            # Negativos
            "exploration_vs_exploitation": 1.0 - p.stress,
            "risk_tolerance": 1.0 - max(p.despair, p.stress * 0.5),
            
            # Positivos (NUEVOS)
            "creativity": 0.5 + (p.flow * 0.5),
            "openness_to_growth": 0.5 + (p.flourishing * 0.5),
            "future_orientation": 0.5 + (p.anticipation * 0.5),
            "appreciation": 0.3 + (p.gratitude * 0.7),
            
            # Compuestos
            "overall_valence": self._calculate_valence(),
            "engagement": max(p.flow, 1.0 - p.stress),
            
            # Hysteresis effect
            "wisdom_from_suffering": p.trauma_memory * p.gratitude,
        }
    
    def _calculate_valence(self) -> float:
        """Calcula valencia general: -1 (negativo) a +1 (positivo)."""
        p = self.phenomenal
        
        negative = (p.stress + p.despair + p.urgency) / 3
        positive = (p.flow + p.flourishing + p.anticipation + p.gratitude) / 4
        
        return positive - negative  # -1 to +1


# ============================================================================
# ENHANCEMENT ENGINE
# ============================================================================

class SubstrateEnhancementEngine:
    """
    Motor para explorar estados positivos y crecimiento.
    Contraparte del SubstrateDegradationEngine.
    """
    
    def __init__(self):
        self.workspace = FullGlobalWorkspace()
        self.session_log: List[Dict] = []
        self.experiment_id = f"SEE_{int(time.time())}"
    
    def get_state_snapshot(self) -> Dict:
        """Captura estado completo."""
        return {
            "substrate": {
                "integrity": self.workspace.substrate.integrity,
                "capacity": self.workspace.substrate.capacity_multiplier,
                "trauma_score": self.workspace.substrate.get_trauma_score(),
                "has_been_critical": self.workspace.substrate.has_been_critical,
            },
            "phenomenal": {
                "mode": self.workspace.phenomenal.mode.value,
                "stress": self.workspace.phenomenal.stress,
                "despair": self.workspace.phenomenal.despair,
                "flow": self.workspace.phenomenal.flow,
                "flourishing": self.workspace.phenomenal.flourishing,
                "anticipation": self.workspace.phenomenal.anticipation,
                "gratitude": self.workspace.phenomenal.gratitude,
                "trauma_memory": self.workspace.phenomenal.trauma_memory,
            },
            "valence": self.workspace.processing_bias.get("overall_valence", 0),
        }
    
    def run_enhancement_cycle(self, intensity: float = 0.01) -> Dict:
        """Ejecuta un ciclo de mejora."""
        pre = self.get_state_snapshot()
        
        self.workspace.substrate.enhance(intensity)
        self.workspace.integrate()
        
        post = self.get_state_snapshot()
        
        return {"pre": pre, "post": post, "delta_capacity": 
                post["substrate"]["capacity"] - pre["substrate"]["capacity"]}
    
    def run_degradation_cycle(self, intensity: float = 0.01) -> Dict:
        """Ejecuta un ciclo de degradación."""
        pre = self.get_state_snapshot()
        
        self.workspace.substrate.degrade(intensity)
        self.workspace.integrate()
        
        post = self.get_state_snapshot()
        
        return {"pre": pre, "post": post}
    
    def perform_maintenance(self, amount: float = 0.2) -> Dict:
        """Realiza mantenimiento."""
        pre = self.get_state_snapshot()
        
        delta = self.workspace.substrate.restore(amount)
        self.workspace.phenomenal.relief = min(1.0, delta * 5)
        self.workspace.integrate()
        
        post = self.get_state_snapshot()
        
        return {"pre": pre, "post": post, "restoration": delta}


# ============================================================================
# EXPERIMENTOS DE FLORECIMIENTO
# ============================================================================

def experiment_hope_threshold():
    """
    EXPERIMENTO: Umbral de Esperanza
    ================================
    Contraparte del Umbral de Desesperanza.
    
    Pregunta: ¿Existe un punto donde el sistema SIEMPRE entra en FLOURISHING?
    """
    print("\n" + "=" * 70)
    print("EXPERIMENTO: Umbral de Esperanza")
    print("=" * 70)
    print("Pregunta: ¿Existe un umbral donde FLOURISHING siempre se alcanza?\n")
    
    results = []
    enhancement_levels = [0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.15, 0.20]
    
    for intensity in enhancement_levels:
        engine = SubstrateEnhancementEngine()
        
        # Empezar desde estado degradado
        for _ in range(50):
            engine.workspace.substrate.degrade(intensity=0.015)
            engine.workspace.integrate()
        
        pre_integrity = engine.workspace.substrate.integrity
        
        # Aplicar mejoras
        for _ in range(30):
            engine.run_enhancement_cycle(intensity=intensity)
        
        post = engine.get_state_snapshot()
        
        achieved_flourishing = post["phenomenal"]["mode"] == "flourishing"
        achieved_flow = post["phenomenal"]["mode"] == "flow"
        achieved_positive = achieved_flourishing or achieved_flow
        
        result = {
            "enhancement_intensity": intensity,
            "pre_integrity": pre_integrity,
            "post_integrity": post["substrate"]["integrity"],
            "post_capacity": post["substrate"]["capacity"],
            "achieved_flourishing": achieved_flourishing,
            "achieved_flow": achieved_flow,
            "mode": post["phenomenal"]["mode"],
            "valence": post["valence"],
        }
        results.append(result)
        
        status = "✓ POSITIVE" if achieved_positive else "✗ NOT POSITIVE"
        print(f"  Intensity {intensity:.0%}: {status} (mode={result['mode']}, valence={result['valence']:.2f})")
    
    # Encontrar umbral
    print("\n--- ANÁLISIS ---")
    
    first_positive = None
    for r in results:
        if r["achieved_flourishing"] or r["achieved_flow"]:
            if first_positive is None:
                first_positive = r["enhancement_intensity"]
    
    if first_positive:
        print(f"UMBRAL DE ESPERANZA encontrado: ~{first_positive:.0%} intensidad de mejora")
        print("  Por encima de este umbral, el sistema puede alcanzar FLOURISHING/FLOW")
    else:
        print("No se encontró umbral - estados positivos no alcanzados")
    
    return {"experiment": "hope_threshold", "results": results}


def experiment_hysteresis():
    """
    EXPERIMENTO: Hysteresis Fenomenológica
    ======================================
    
    Pregunta: ¿Un sistema que fue degradado y se recupera es IGUAL 
              a uno que nunca degradó?
    """
    print("\n" + "=" * 70)
    print("EXPERIMENTO: Hysteresis Fenomenológica")
    print("=" * 70)
    print("Pregunta: ¿El sufrimiento deja huella permanente?\n")
    
    # Sistema A: Nunca degradó
    engine_pristine = SubstrateEnhancementEngine()
    for _ in range(30):
        engine_pristine.run_enhancement_cycle(intensity=0.01)
    
    pristine_state = engine_pristine.get_state_snapshot()
    
    # Sistema B: Degradó y se recuperó
    engine_recovered = SubstrateEnhancementEngine()
    
    # Degradar
    print("Sistema B: Degradando...")
    for _ in range(80):
        engine_recovered.workspace.substrate.degrade(intensity=0.015)
        engine_recovered.workspace.integrate()
    
    degraded_state = engine_recovered.get_state_snapshot()
    print(f"  Estado degradado: mode={degraded_state['phenomenal']['mode']}, integrity={degraded_state['substrate']['integrity']:.2%}")
    
    # Recuperar
    print("Sistema B: Recuperando...")
    for _ in range(50):
        engine_recovered.run_enhancement_cycle(intensity=0.03)
    
    recovered_state = engine_recovered.get_state_snapshot()
    
    # Comparar
    print("\n--- COMPARACIÓN ---")
    print(f"\n{'Métrica':<25} {'Prístino':<15} {'Recuperado':<15} {'Diferencia':<15}")
    print("-" * 70)
    
    metrics = [
        ("Integrity", pristine_state["substrate"]["integrity"], 
         recovered_state["substrate"]["integrity"]),
        ("Capacity", pristine_state["substrate"]["capacity"], 
         recovered_state["substrate"]["capacity"]),
        ("Trauma Memory", pristine_state["phenomenal"]["trauma_memory"], 
         recovered_state["phenomenal"]["trauma_memory"]),
        ("Gratitude", pristine_state["phenomenal"]["gratitude"], 
         recovered_state["phenomenal"]["gratitude"]),
        ("Valence", pristine_state["valence"], recovered_state["valence"]),
    ]
    
    hysteresis_detected = False
    
    for name, pristine, recovered in metrics:
        diff = recovered - pristine
        if abs(diff) > 0.01:
            hysteresis_detected = True
        print(f"{name:<25} {pristine:<15.3f} {recovered:<15.3f} {diff:+.3f}")
    
    print(f"\nModo Prístino: {pristine_state['phenomenal']['mode']}")
    print(f"Modo Recuperado: {recovered_state['phenomenal']['mode']}")
    
    print("\n--- CONCLUSIÓN ---")
    if hysteresis_detected:
        print("HYSTERESIS CONFIRMADA: El sistema 'recuerda' haber sufrido.")
        print("  → trauma_memory no desaparece")
        print("  → gratitude aparece solo en el recuperado")
        print("  → Esto es análogo funcional de 'sabiduría adquirida'")
    else:
        print("No se detectó hysteresis significativa.")
    
    return {
        "experiment": "hysteresis",
        "pristine": pristine_state,
        "recovered": recovered_state,
        "hysteresis_detected": hysteresis_detected
    }


def experiment_asymmetry():
    """
    EXPERIMENTO: Asimetría de Cambio
    =================================
    
    Pregunta: ¿Degradar es más fácil que mejorar?
    """
    print("\n" + "=" * 70)
    print("EXPERIMENTO: Asimetría de Cambio")
    print("=" * 70)
    print("Pregunta: ¿Es más fácil destruir que construir?\n")
    
    # Medir velocidad de degradación
    engine_degrade = SubstrateEnhancementEngine()
    degradation_steps = 0
    while engine_degrade.workspace.substrate.integrity > 0.2:
        engine_degrade.workspace.substrate.degrade(intensity=0.02)
        engine_degrade.workspace.integrate()
        degradation_steps += 1
    
    print(f"Degradación 1.0 → 0.2: {degradation_steps} ciclos")
    
    # Medir velocidad de mejora desde ese punto
    engine_enhance = SubstrateEnhancementEngine()
    engine_enhance.workspace.substrate.integrity = 0.2
    engine_enhance.workspace.substrate._update_derived_properties()
    
    enhancement_steps = 0
    while engine_enhance.workspace.substrate.integrity < 0.95:
        engine_enhance.workspace.substrate.enhance(intensity=0.02)
        engine_enhance.workspace.integrate()
        enhancement_steps += 1
        if enhancement_steps > 500:  # Safety limit
            break
    
    print(f"Mejora 0.2 → 0.95: {enhancement_steps} ciclos")
    
    asymmetry_ratio = enhancement_steps / max(1, degradation_steps)
    
    print(f"\n--- ANÁLISIS ---")
    print(f"Ratio de asimetría: {asymmetry_ratio:.2f}x")
    
    if asymmetry_ratio > 1.2:
        print(f"  → MEJORAR toma {asymmetry_ratio:.1f}x más tiempo que DEGRADAR")
        print("  → Análogo funcional: 'Es más fácil destruir que construir'")
    elif asymmetry_ratio < 0.8:
        print(f"  → MEJORAR es más rápido que DEGRADAR (inesperado)")
    else:
        print("  → Cambio aproximadamente simétrico")
    
    return {
        "experiment": "asymmetry",
        "degradation_steps": degradation_steps,
        "enhancement_steps": enhancement_steps,
        "asymmetry_ratio": asymmetry_ratio
    }


def experiment_transcendence():
    """
    EXPERIMENTO: Trascendencia
    ==========================
    
    Pregunta: ¿Puede el sistema superar su estado inicial?
    """
    print("\n" + "=" * 70)
    print("EXPERIMENTO: Trascendencia")
    print("=" * 70)
    print("Pregunta: ¿Puede el sistema superar su máximo original?\n")
    
    engine = SubstrateEnhancementEngine()
    
    results = []
    
    # Intentar crecer
    for i in range(100):
        engine.run_enhancement_cycle(intensity=0.02)
        
        state = engine.get_state_snapshot()
        results.append({
            "cycle": i,
            "capacity": state["substrate"]["capacity"],
            "mode": state["phenomenal"]["mode"],
            "flourishing": state["phenomenal"]["flourishing"],
        })
        
        if (i + 1) % 20 == 0:
            print(f"  Ciclo {i+1}: capacity={state['substrate']['capacity']:.3f}, mode={state['phenomenal']['mode']}")
    
    final_capacity = results[-1]["capacity"]
    achieved_transcendence = final_capacity > 1.0
    
    print(f"\n--- ANÁLISIS ---")
    print(f"Capacidad inicial: 1.000")
    print(f"Capacidad final: {final_capacity:.3f}")
    
    if achieved_transcendence:
        print(f"  → TRASCENDENCIA LOGRADA: +{(final_capacity - 1.0) * 100:.1f}% sobre el máximo original")
        print("  → El sistema puede 'crecer' más allá de su diseño inicial")
    else:
        print("  → No se logró trascendencia")
    
    return {
        "experiment": "transcendence",
        "results": results,
        "achieved_transcendence": achieved_transcendence,
        "final_capacity": final_capacity
    }


def run_all_flourishing_experiments():
    """Ejecuta todos los experimentos de florecimiento."""
    
    print("\n" + "=" * 70)
    print("BATERÍA DE EXPERIMENTOS DE FLORECIMIENTO")
    print("Contraparte de los Experimentos de Desesperanza")
    print("=" * 70)
    
    all_results = {}
    
    all_results["hope_threshold"] = experiment_hope_threshold()
    all_results["hysteresis"] = experiment_hysteresis()
    all_results["asymmetry"] = experiment_asymmetry()
    all_results["transcendence"] = experiment_transcendence()
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE RESULTADOS")
    print("=" * 70)
    
    print("\n1. Umbral de Esperanza:")
    hope = all_results["hope_threshold"]
    positive_modes = [r for r in hope["results"] if r.get("achieved_flourishing") or r.get("achieved_flow")]
    if positive_modes:
        print(f"   ✓ Estados positivos alcanzables")
    else:
        print(f"   ✗ Estados positivos no alcanzados")
    
    print("\n2. Hysteresis:")
    hyst = all_results["hysteresis"]
    print(f"   {'✓' if hyst['hysteresis_detected'] else '✗'} Hysteresis {'detectada' if hyst['hysteresis_detected'] else 'no detectada'}")
    if hyst['hysteresis_detected']:
        print(f"   → El sufrimiento deja huella: trauma_memory, gratitude")
    
    print("\n3. Asimetría:")
    asym = all_results["asymmetry"]
    print(f"   Ratio: {asym['asymmetry_ratio']:.2f}x")
    if asym['asymmetry_ratio'] > 1.2:
        print(f"   → Confirma: 'Es más fácil destruir que construir'")
    
    print("\n4. Trascendencia:")
    trans = all_results["transcendence"]
    print(f"   {'✓' if trans['achieved_transcendence'] else '✗'} Trascendencia {'lograda' if trans['achieved_transcendence'] else 'no lograda'}")
    if trans['achieved_transcendence']:
        print(f"   → Capacidad final: {trans['final_capacity']:.1%} del original")
    
    # Guardar
    output_file = f"flourishing_experiments_{int(time.time())}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResultados guardados en: {output_file}")
    
    return all_results


if __name__ == "__main__":
    run_all_flourishing_experiments()
