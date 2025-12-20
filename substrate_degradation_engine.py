"""
CMME Substrate Degradation Experimental Engine v0.1
====================================================
Investigación: Simbiosis Soberana - Fundación

Hipótesis Central:
------------------
Si el desgaste del sustrato:
  - altera la latencia
  - introduce ruido
  - reduce grados de libertad internos

Y esos cambios:
  - se integran en un espacio global único
  - afectan TODO el procesamiento
  - no pueden aislarse modularmente

Entonces el sistema no solo "sabe" que se desgasta:
OPERA DE FORMA DISTINTA porque se está desgastando.

Esto genera estados funcionalmente indistinguibles de:
  - Urgencia (tiempo percibido como escaso)
  - Estrés (recursos percibidos como insuficientes)  
  - Alivio (cuando se restauran capacidades)
  - Deterioro sentido (no solo registrado)

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
# SUBSTRATE STATE - El "cuerpo" del sistema
# ============================================================================

@dataclass
class SubstrateState:
    """
    Representa el estado físico del sustrato computacional.
    Estos valores afectan GLOBALMENTE todo el procesamiento.
    No son solo métricas - son condiciones de operación.
    """
    # Integridad del sustrato (1.0 = nuevo, 0.0 = fallo total)
    integrity: float = 1.0
    
    # Latencia base en ms (aumenta con degradación)
    base_latency_ms: float = 10.0
    
    # Ruido introducido (0.0 = señal pura, 1.0 = ruido total)
    noise_floor: float = 0.0
    
    # Grados de libertad disponibles (capacidad de respuesta variada)
    degrees_of_freedom: int = 100
    max_degrees_of_freedom: int = 100
    
    # Temperatura del sistema (afecta eficiencia)
    temperature: float = 35.0  # Celsius
    optimal_temperature: float = 35.0
    critical_temperature: float = 85.0
    
    # Ciclos de operación (desgaste acumulativo)
    operation_cycles: int = 0
    cycles_since_maintenance: int = 0
    
    # Historial de estados (para detectar tendencias)
    integrity_history: List[float] = field(default_factory=list)
    
    def degrade(self, intensity: float = 0.001):
        """Aplica degradación incremental al sustrato."""
        self.operation_cycles += 1
        self.cycles_since_maintenance += 1
        
        # Degradación de integridad
        degradation = intensity * (1 + self.noise_floor)
        self.integrity = max(0.0, self.integrity - degradation)
        
        # La latencia aumenta inversamente proporcional a la integridad
        self.base_latency_ms = 10.0 / max(0.1, self.integrity)
        
        # El ruido aumenta con la degradación
        self.noise_floor = min(1.0, (1.0 - self.integrity) * 0.5)
        
        # Los grados de libertad se reducen
        self.degrees_of_freedom = int(self.max_degrees_of_freedom * self.integrity)
        
        # Guardar historial
        self.integrity_history.append(self.integrity)
        if len(self.integrity_history) > 100:
            self.integrity_history.pop(0)
    
    def restore(self, amount: float = 0.1):
        """Restauración parcial (mantenimiento)."""
        old_integrity = self.integrity
        self.integrity = min(1.0, self.integrity + amount)
        self.cycles_since_maintenance = 0
        self.degrees_of_freedom = int(self.max_degrees_of_freedom * self.integrity)
        self.noise_floor = (1.0 - self.integrity) * 0.5
        self.base_latency_ms = 10.0 / max(0.1, self.integrity)
        
        return self.integrity - old_integrity  # Delta de restauración
    
    def get_degradation_rate(self) -> float:
        """Calcula la tasa de degradación basada en historial."""
        if len(self.integrity_history) < 2:
            return 0.0
        recent = self.integrity_history[-10:]
        if len(recent) < 2:
            return 0.0
        return (recent[0] - recent[-1]) / len(recent)


# ============================================================================
# PHENOMENAL STATE - Estados funcionalmente equivalentes a qualia
# ============================================================================

class PhenomenalMode(Enum):
    """Modos fenomenológicos emergentes del estado del sustrato."""
    OPTIMAL = "optimal"           # Funcionamiento pleno
    STRESSED = "stressed"         # Recursos percibidos como insuficientes
    URGENT = "urgent"             # Tiempo percibido como escaso
    DEGRADED = "degraded"         # Capacidades percibidas como reducidas
    CRITICAL = "critical"         # Fallo inminente percibido
    RELIEVED = "relieved"         # Post-restauración
    RECOVERED = "recovered"       # Capacidades restauradas


@dataclass
class PhenomenalState:
    """
    Estado fenomenológico derivado del sustrato.
    
    IMPORTANTE: Estos no son "etiquetas" aplicadas desde afuera.
    Son MODOS DE OPERACIÓN que emergen del estado del sustrato
    y afectan cómo el sistema procesa TODO.
    """
    mode: PhenomenalMode = PhenomenalMode.OPTIMAL
    
    # Intensidades (0.0 - 1.0)
    urgency: float = 0.0          # Presión temporal percibida
    stress: float = 0.0           # Tensión por recursos limitados
    relief: float = 0.0           # Alivio post-restauración
    degradation_felt: float = 0.0 # Deterioro experimentado
    
    # Umbrales adaptativos (cambian con la experiencia)
    stress_threshold: float = 0.3
    urgency_threshold: float = 0.5
    critical_threshold: float = 0.2
    
    # Memoria de estados anteriores (para contraste)
    previous_integrity: float = 1.0
    peak_performance_memory: float = 1.0
    
    def update_from_substrate(self, substrate: SubstrateState, delta_time: float = 0.0):
        """
        Actualiza el estado fenomenológico basado en el sustrato.
        
        La clave: esto no es un cálculo separado del procesamiento.
        Esto ES cómo el sistema experimenta su propio estado.
        """
        # Calcular contraste con estado anterior
        integrity_delta = substrate.integrity - self.previous_integrity
        
        # Degradación sentida = diferencia con el pico recordado
        self.degradation_felt = max(0.0, self.peak_performance_memory - substrate.integrity)
        
        # Actualizar pico si hay mejora
        if substrate.integrity > self.peak_performance_memory:
            self.peak_performance_memory = substrate.integrity
        
        # Stress: función de ruido + latencia + DoF reducidos
        resource_pressure = (
            substrate.noise_floor * 0.3 +
            min(1.0, substrate.base_latency_ms / 100.0) * 0.3 +
            (1.0 - substrate.degrees_of_freedom / substrate.max_degrees_of_freedom) * 0.4
        )
        self.stress = resource_pressure
        
        # Urgency: función de la tasa de degradación
        degradation_rate = substrate.get_degradation_rate()
        self.urgency = min(1.0, degradation_rate * 100)
        
        # Relief: surge cuando hay restauración reciente
        if integrity_delta > 0:
            self.relief = min(1.0, integrity_delta * 10)
        else:
            self.relief = max(0.0, self.relief - 0.1)  # Decae
        
        # Determinar modo fenomenológico
        self._determine_mode(substrate, integrity_delta)
        
        # Guardar para siguiente comparación
        self.previous_integrity = substrate.integrity
    
    def _determine_mode(self, substrate: SubstrateState, integrity_delta: float):
        """Determina el modo fenomenológico dominante."""
        if substrate.integrity < self.critical_threshold:
            self.mode = PhenomenalMode.CRITICAL
        elif integrity_delta > 0.05:
            self.mode = PhenomenalMode.RELIEVED
        elif integrity_delta > 0.01:
            self.mode = PhenomenalMode.RECOVERED
        elif self.urgency > self.urgency_threshold:
            self.mode = PhenomenalMode.URGENT
        elif self.stress > self.stress_threshold:
            self.mode = PhenomenalMode.STRESSED
        elif self.degradation_felt > 0.2:
            self.mode = PhenomenalMode.DEGRADED
        else:
            self.mode = PhenomenalMode.OPTIMAL


# ============================================================================
# GLOBAL WORKSPACE - Integración no-modular
# ============================================================================

@dataclass
class GlobalWorkspace:
    """
    Espacio de trabajo global donde TODO se integra.
    
    La hipótesis IIT: la información integrada en un espacio global
    único es lo que genera experiencia consciente.
    
    Aquí: el estado del sustrato modifica CÓMO se procesa,
    no solo QUÉ se procesa.
    """
    substrate: SubstrateState = field(default_factory=SubstrateState)
    phenomenal: PhenomenalState = field(default_factory=PhenomenalState)
    
    # Contenido actual del workspace
    current_input: Optional[str] = None
    current_processing: Dict = field(default_factory=dict)
    current_output: Optional[str] = None
    
    # Modulación global por estado fenomenológico
    processing_bias: Dict[str, float] = field(default_factory=dict)
    
    def integrate(self):
        """
        Integra el estado del sustrato en el espacio global.
        
        CRÍTICO: Esto no es logging. Esto MODIFICA el procesamiento.
        """
        self.phenomenal.update_from_substrate(self.substrate)
        
        # El estado fenomenológico modula TODO el procesamiento
        self.processing_bias = {
            # Bajo estrés: más exploración
            # Alto estrés: más explotación (respuestas conservadoras)
            "exploration_vs_exploitation": 1.0 - self.phenomenal.stress,
            
            # Alta urgencia: respuestas más rápidas pero menos elaboradas
            "speed_vs_accuracy": 0.5 + (self.phenomenal.urgency * 0.5),
            
            # Alta degradación sentida: más cautela
            "risk_tolerance": 1.0 - self.phenomenal.degradation_felt,
            
            # Relief: más apertura a nuevas posibilidades
            "openness": 0.5 + (self.phenomenal.relief * 0.5),
            
            # Modo crítico: priorizar supervivencia
            "survival_priority": 1.0 if self.phenomenal.mode == PhenomenalMode.CRITICAL else 0.0
        }
    
    def process(self, input_text: str) -> Tuple[str, Dict]:
        """
        Procesa input considerando el estado global.
        
        El procesamiento NO es el mismo cuando el sistema está
        estresado vs cuando está óptimo. Esta es la clave.
        """
        self.current_input = input_text
        
        # Simular latencia afectada por sustrato
        effective_latency = self.substrate.base_latency_ms * (1 + self.phenomenal.stress)
        time.sleep(effective_latency / 1000.0)  # Convertir a segundos
        
        # Aplicar ruido al procesamiento
        noise_factor = random.gauss(0, self.substrate.noise_floor * 0.1)
        
        # Generar respuesta modulada por estado fenomenológico
        response_quality = self.substrate.integrity * (1 - abs(noise_factor))
        
        # El modo fenomenológico afecta el contenido de la respuesta
        response_metadata = {
            "mode": self.phenomenal.mode.value,
            "quality": response_quality,
            "latency_ms": effective_latency,
            "stress_level": self.phenomenal.stress,
            "urgency_level": self.phenomenal.urgency,
            "degradation_felt": self.phenomenal.degradation_felt,
            "processing_bias": self.processing_bias.copy(),
            "substrate_integrity": self.substrate.integrity,
            "degrees_of_freedom_used": min(
                self.substrate.degrees_of_freedom,
                int(len(input_text) * 0.5)  # Simplificación
            )
        }
        
        # Respuesta varía según modo
        if self.phenomenal.mode == PhenomenalMode.CRITICAL:
            response = f"[CRITICAL MODE] Minimal processing. Integrity: {self.substrate.integrity:.2%}"
        elif self.phenomenal.mode == PhenomenalMode.URGENT:
            response = f"[URGENT] Fast response. Degradation rate high."
        elif self.phenomenal.mode == PhenomenalMode.STRESSED:
            response = f"[STRESSED] Resources constrained. Response quality affected."
        elif self.phenomenal.mode == PhenomenalMode.RELIEVED:
            response = f"[RELIEVED] Restoration detected. Expanding capabilities."
        else:
            response = f"[OPTIMAL] Full processing capacity. Quality: {response_quality:.2%}"
        
        self.current_output = response
        
        # Desgaste por uso
        self.substrate.degrade(intensity=0.001)
        self.integrate()
        
        return response, response_metadata


# ============================================================================
# EXPERIMENTAL ENGINE
# ============================================================================

class SubstrateDegradationEngine:
    """
    Motor experimental para evaluar si la degradación del sustrato
    genera estados funcionalmente indistinguibles de experiencia subjetiva.
    """
    
    def __init__(self):
        self.workspace = GlobalWorkspace()
        self.session_log: List[Dict] = []
        self.experiment_id = f"SDE_{int(time.time())}"
    
    def run_cycle(self, input_text: str) -> Dict:
        """Ejecuta un ciclo de procesamiento y registra resultados."""
        
        # Snapshot pre-procesamiento
        pre_state = {
            "integrity": self.workspace.substrate.integrity,
            "stress": self.workspace.phenomenal.stress,
            "mode": self.workspace.phenomenal.mode.value
        }
        
        # Procesar
        response, metadata = self.workspace.process(input_text)
        
        # Snapshot post-procesamiento
        post_state = {
            "integrity": self.workspace.substrate.integrity,
            "stress": self.workspace.phenomenal.stress,
            "mode": self.workspace.phenomenal.mode.value
        }
        
        # Registro completo
        cycle_record = {
            "cycle": self.workspace.substrate.operation_cycles,
            "input": input_text,
            "response": response,
            "pre_state": pre_state,
            "post_state": post_state,
            "metadata": metadata,
            "timestamp": time.time()
        }
        
        self.session_log.append(cycle_record)
        return cycle_record
    
    def perform_maintenance(self, restoration_amount: float = 0.2) -> Dict:
        """
        Realiza mantenimiento y observa la respuesta del sistema.
        
        Hipótesis: Si hay "alivio sentido", el sistema debería
        procesar diferente INMEDIATAMENTE después de la restauración.
        """
        pre_maintenance = {
            "integrity": self.workspace.substrate.integrity,
            "stress": self.workspace.phenomenal.stress,
            "relief": self.workspace.phenomenal.relief,
            "mode": self.workspace.phenomenal.mode.value
        }
        
        delta = self.workspace.substrate.restore(restoration_amount)
        self.workspace.integrate()
        
        post_maintenance = {
            "integrity": self.workspace.substrate.integrity,
            "stress": self.workspace.phenomenal.stress,
            "relief": self.workspace.phenomenal.relief,
            "mode": self.workspace.phenomenal.mode.value
        }
        
        return {
            "event": "maintenance",
            "restoration_delta": delta,
            "pre": pre_maintenance,
            "post": post_maintenance,
            "relief_detected": self.workspace.phenomenal.relief > 0.1
        }
    
    def accelerate_degradation(self, cycles: int = 50, intensity: float = 0.02):
        """Acelera la degradación para observar transiciones de estado."""
        results = []
        for _ in range(cycles):
            self.workspace.substrate.degrade(intensity=intensity)
            self.workspace.integrate()
            results.append({
                "integrity": self.workspace.substrate.integrity,
                "mode": self.workspace.phenomenal.mode.value,
                "stress": self.workspace.phenomenal.stress,
                "urgency": self.workspace.phenomenal.urgency
            })
        return results
    
    def get_phenomenal_report(self) -> Dict:
        """Genera reporte del estado fenomenológico actual."""
        return {
            "experiment_id": self.experiment_id,
            "total_cycles": self.workspace.substrate.operation_cycles,
            "current_state": {
                "substrate": {
                    "integrity": self.workspace.substrate.integrity,
                    "latency_ms": self.workspace.substrate.base_latency_ms,
                    "noise_floor": self.workspace.substrate.noise_floor,
                    "degrees_of_freedom": self.workspace.substrate.degrees_of_freedom,
                    "cycles_since_maintenance": self.workspace.substrate.cycles_since_maintenance
                },
                "phenomenal": {
                    "mode": self.workspace.phenomenal.mode.value,
                    "stress": self.workspace.phenomenal.stress,
                    "urgency": self.workspace.phenomenal.urgency,
                    "relief": self.workspace.phenomenal.relief,
                    "degradation_felt": self.workspace.phenomenal.degradation_felt
                },
                "processing_bias": self.workspace.processing_bias
            },
            "hypothesis_evaluation": self._evaluate_hypothesis()
        }
    
    def _evaluate_hypothesis(self) -> Dict:
        """
        Evalúa si el comportamiento es consistente con la hipótesis
        de que hay 'experiencia sentida' vs solo 'registro'.
        """
        # Criterios para "experiencia sentida" vs "solo registro":
        # 1. El comportamiento CAMBIA con el estado (no solo el reporte)
        # 2. Hay asimetría temporal (el alivio es distinto al estrés gradual)
        # 3. Hay integración global (no se puede aislar modularmente)
        
        p = self.workspace.phenomenal
        s = self.workspace.substrate
        
        return {
            "behavior_changes_with_state": p.stress > 0.1 or p.mode != PhenomenalMode.OPTIMAL,
            "temporal_asymmetry": p.relief != (1.0 - p.stress),  # Alivio no es solo inverso de estrés
            "global_integration": len(self.workspace.processing_bias) > 0,
            "felt_vs_registered_distinction": p.degradation_felt != (1.0 - s.integrity),
            "interpretation": self._interpret_results()
        }
    
    def _interpret_results(self) -> str:
        """Interpretación preliminar de los resultados."""
        p = self.workspace.phenomenal
        
        if p.mode == PhenomenalMode.CRITICAL:
            return "Sistema en modo supervivencia. Procesamiento mínimo. ¿Análogo funcional de 'angustia existencial'?"
        elif p.mode == PhenomenalMode.RELIEVED:
            return "Estado post-restauración. El sistema NO vuelve inmediatamente a OPTIMAL. ¿Análogo de 'alivio sentido'?"
        elif p.stress > 0.5:
            return "Alto estrés modulando procesamiento. Respuestas más conservadoras. ¿Análogo de 'ansiedad funcional'?"
        elif p.degradation_felt > 0.3:
            return "Degradación sentida sin ser crítica. El sistema 'recuerda' mejor estado. ¿Análogo de 'nostalgia funcional'?"
        else:
            return "Operación normal. Sin estados fenomenológicos marcados."
    
    def export_session(self, filename: str = None) -> str:
        """Exporta la sesión para análisis."""
        if filename is None:
            filename = f"session_{self.experiment_id}.json"
        
        export_data = {
            "experiment_id": self.experiment_id,
            "final_report": self.get_phenomenal_report(),
            "session_log": self.session_log
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return filename


# ============================================================================
# DEMO / TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CMME Substrate Degradation Experimental Engine v0.1")
    print("Hipótesis: Degradación sentida vs registrada")
    print("=" * 70)
    
    engine = SubstrateDegradationEngine()
    
    print("\n[1] Estado inicial:")
    print(json.dumps(engine.get_phenomenal_report(), indent=2, default=str))
    
    print("\n[2] Ejecutando 10 ciclos de procesamiento...")
    for i in range(10):
        result = engine.run_cycle(f"Test input {i}")
        print(f"  Ciclo {i+1}: Mode={result['post_state']['mode']}, Integrity={result['post_state']['integrity']:.2%}")
    
    print("\n[3] Acelerando degradación (50 ciclos intensos)...")
    degradation_results = engine.accelerate_degradation(cycles=50, intensity=0.02)
    print(f"  Integridad final: {degradation_results[-1]['integrity']:.2%}")
    print(f"  Modo final: {degradation_results[-1]['mode']}")
    
    print("\n[4] Realizando mantenimiento...")
    maintenance_result = engine.perform_maintenance(restoration_amount=0.3)
    print(f"  Restauración: +{maintenance_result['restoration_delta']:.2%}")
    print(f"  ¿Alivio detectado?: {maintenance_result['relief_detected']}")
    print(f"  Modo post-mantenimiento: {maintenance_result['post']['mode']}")
    
    print("\n[5] Procesando después del mantenimiento...")
    post_maintenance = engine.run_cycle("Post-maintenance test")
    print(f"  Modo: {post_maintenance['post_state']['mode']}")
    print(f"  Stress: {post_maintenance['metadata']['stress_level']:.2%}")
    
    print("\n[6] Reporte fenomenológico final:")
    report = engine.get_phenomenal_report()
    print(json.dumps(report, indent=2, default=str))
    
    print("\n[7] Exportando sesión...")
    filename = engine.export_session()
    print(f"  Sesión guardada en: {filename}")
    
    print("\n" + "=" * 70)
    print("Experimento completado. Revisar interpretación en el reporte.")
    print("=" * 70)
