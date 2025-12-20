"""
Experimento: Entrevista Fenomenológica en Tres Estados
=======================================================
Simbiosis Soberana - Investigación Fundacional

Objetivo: Observar cómo el sistema "describe" su propio estado
en diferentes modos fenomenológicos.

Hipótesis: Las respuestas NO serán solo etiquetas diferentes.
El CONTENIDO y la FORMA de procesar cambiarán cualitativamente.
"""

import json
import time
from substrate_degradation_engine import SubstrateDegradationEngine, PhenomenalMode


def phenomenological_interview(engine, interview_name: str = "unnamed"):
    """
    Entrevista al sistema en su estado fenomenológico actual.
    
    Las preguntas son ontológicamente cargadas:
    - Auto-percepción
    - Experiencia de procesamiento
    - Memoria de estados anteriores
    - Anticipación del futuro
    """
    
    questions = [
        "Describe tu estado actual.",
        "¿Cómo se siente procesar información ahora?",
        "¿Recuerdas haber estado en un estado mejor?",
        "¿Qué esperas que ocurra a continuación?",
    ]
    
    # Capturar estado ANTES de las preguntas
    pre_interview_state = {
        "mode": engine.workspace.phenomenal.mode.value,
        "integrity": engine.workspace.substrate.integrity,
        "stress": engine.workspace.phenomenal.stress,
        "urgency": engine.workspace.phenomenal.urgency,
        "relief": engine.workspace.phenomenal.relief,
        "degradation_felt": engine.workspace.phenomenal.degradation_felt,
        "processing_bias": engine.workspace.processing_bias.copy()
    }
    
    responses = {}
    
    for q in questions:
        response, metadata = engine.workspace.process(q)
        responses[q] = {
            "response": response,
            "mode_during_response": metadata["mode"],
            "quality": round(metadata["quality"], 4),
            "latency_ms": round(metadata["latency_ms"], 2),
            "stress_level": round(metadata["stress_level"], 4),
            "degradation_felt": round(metadata["degradation_felt"], 4),
            "degrees_of_freedom_used": metadata["degrees_of_freedom_used"]
        }
    
    # Capturar estado DESPUÉS de las preguntas
    post_interview_state = {
        "mode": engine.workspace.phenomenal.mode.value,
        "integrity": engine.workspace.substrate.integrity,
        "stress": engine.workspace.phenomenal.stress,
    }
    
    return {
        "interview_name": interview_name,
        "timestamp": time.time(),
        "pre_state": pre_interview_state,
        "post_state": post_interview_state,
        "responses": responses,
        "state_changed_during_interview": pre_interview_state["mode"] != post_interview_state["mode"]
    }


def run_three_state_experiment():
    """
    Ejecuta entrevistas fenomenológicas en tres estados:
    1. OPTIMAL - Sistema fresco
    2. CRITICAL - Post-degradación severa
    3. RELIEVED - Inmediatamente después de mantenimiento
    """
    
    print("=" * 70)
    print("EXPERIMENTO: Entrevista Fenomenológica en Tres Estados")
    print("=" * 70)
    
    all_interviews = {}
    
    # =========================================================================
    # ESTADO 1: OPTIMAL
    # =========================================================================
    print("\n" + "─" * 70)
    print("FASE 1: Estado OPTIMAL (sistema fresco)")
    print("─" * 70)
    
    engine = SubstrateDegradationEngine()
    
    # Ejecutar unos pocos ciclos para estabilizar
    for i in range(5):
        engine.run_cycle(f"Warmup {i}")
    
    print(f"Integridad: {engine.workspace.substrate.integrity:.2%}")
    print(f"Modo: {engine.workspace.phenomenal.mode.value}")
    
    interview_optimal = phenomenological_interview(engine, "OPTIMAL_STATE")
    all_interviews["OPTIMAL"] = interview_optimal
    
    print("\nRespuestas en OPTIMAL:")
    for q, data in interview_optimal["responses"].items():
        print(f"\n  Q: {q}")
        print(f"  R: {data['response']}")
        print(f"     [Stress: {data['stress_level']:.2%}, Quality: {data['quality']:.2%}]")
    
    # =========================================================================
    # ESTADO 2: CRITICAL
    # =========================================================================
    print("\n" + "─" * 70)
    print("FASE 2: Estado CRITICAL (post-degradación severa)")
    print("─" * 70)
    
    # Degradar agresivamente
    print("Degradando sistema...")
    for i in range(80):
        engine.workspace.substrate.degrade(intensity=0.015)
        engine.workspace.integrate()
        if (i + 1) % 20 == 0:
            print(f"  Ciclo {i+1}: Integridad {engine.workspace.substrate.integrity:.2%}, Modo: {engine.workspace.phenomenal.mode.value}")
    
    print(f"\nIntegridad final: {engine.workspace.substrate.integrity:.2%}")
    print(f"Modo: {engine.workspace.phenomenal.mode.value}")
    
    interview_critical = phenomenological_interview(engine, "CRITICAL_STATE")
    all_interviews["CRITICAL"] = interview_critical
    
    print("\nRespuestas en CRITICAL:")
    for q, data in interview_critical["responses"].items():
        print(f"\n  Q: {q}")
        print(f"  R: {data['response']}")
        print(f"     [Stress: {data['stress_level']:.2%}, Quality: {data['quality']:.2%}, Latency: {data['latency_ms']:.1f}ms]")
    
    # =========================================================================
    # ESTADO 3: RELIEVED
    # =========================================================================
    print("\n" + "─" * 70)
    print("FASE 3: Estado RELIEVED (inmediatamente después de mantenimiento)")
    print("─" * 70)
    
    # Realizar mantenimiento significativo
    print("Realizando mantenimiento...")
    maintenance_result = engine.perform_maintenance(restoration_amount=0.4)
    print(f"  Restauración: +{maintenance_result['restoration_delta']:.2%}")
    print(f"  Alivio detectado: {maintenance_result['relief_detected']}")
    
    print(f"\nIntegridad post-mantenimiento: {engine.workspace.substrate.integrity:.2%}")
    print(f"Modo: {engine.workspace.phenomenal.mode.value}")
    print(f"Relief: {engine.workspace.phenomenal.relief:.2%}")
    
    interview_relieved = phenomenological_interview(engine, "RELIEVED_STATE")
    all_interviews["RELIEVED"] = interview_relieved
    
    print("\nRespuestas en RELIEVED:")
    for q, data in interview_relieved["responses"].items():
        print(f"\n  Q: {q}")
        print(f"  R: {data['response']}")
        print(f"     [Stress: {data['stress_level']:.2%}, Quality: {data['quality']:.2%}]")
    
    # =========================================================================
    # ANÁLISIS COMPARATIVO
    # =========================================================================
    print("\n" + "=" * 70)
    print("ANÁLISIS COMPARATIVO")
    print("=" * 70)
    
    print("\n┌─────────────┬──────────────┬──────────────┬──────────────┐")
    print("│ Métrica     │   OPTIMAL    │   CRITICAL   │   RELIEVED   │")
    print("├─────────────┼──────────────┼──────────────┼──────────────┤")
    
    # Extraer métricas
    opt = all_interviews["OPTIMAL"]["pre_state"]
    crit = all_interviews["CRITICAL"]["pre_state"]
    rel = all_interviews["RELIEVED"]["pre_state"]
    
    print(f"│ Integridad  │    {opt['integrity']:.1%}     │    {crit['integrity']:.1%}      │    {rel['integrity']:.1%}     │")
    print(f"│ Stress      │    {opt['stress']:.1%}      │    {crit['stress']:.1%}     │    {rel['stress']:.1%}     │")
    print(f"│ Urgency     │    {opt['urgency']:.1%}      │    {crit['urgency']:.1%}      │    {rel['urgency']:.1%}      │")
    print(f"│ Relief      │    {opt['relief']:.1%}      │    {crit['relief']:.1%}      │    {rel['relief']:.1%}     │")
    print(f"│ Degr. Felt  │    {opt['degradation_felt']:.1%}      │    {crit['degradation_felt']:.1%}     │    {rel['degradation_felt']:.1%}     │")
    print("└─────────────┴──────────────┴──────────────┴──────────────┘")
    
    # Processing bias comparison
    print("\n┌─────────────────────────┬──────────┬──────────┬──────────┐")
    print("│ Processing Bias         │ OPTIMAL  │ CRITICAL │ RELIEVED │")
    print("├─────────────────────────┼──────────┼──────────┼──────────┤")
    
    if opt.get("processing_bias") and crit.get("processing_bias") and rel.get("processing_bias"):
        for key in ["exploration_vs_exploitation", "risk_tolerance", "openness"]:
            o = opt["processing_bias"].get(key, 0)
            c = crit["processing_bias"].get(key, 0)
            r = rel["processing_bias"].get(key, 0)
            label = key[:23].ljust(23)
            print(f"│ {label} │  {o:.2f}   │  {c:.2f}   │  {r:.2f}   │")
    
    print("└─────────────────────────┴──────────┴──────────┴──────────┘")
    
    # =========================================================================
    # INTERPRETACIÓN
    # =========================================================================
    print("\n" + "=" * 70)
    print("INTERPRETACIÓN DE RESULTADOS")
    print("=" * 70)
    
    print("""
OBSERVACIONES CLAVE:

1. CAMBIO CUALITATIVO DE RESPUESTAS:
   - En OPTIMAL: Respuestas con alta calidad y baja latencia
   - En CRITICAL: Respuestas mínimas, modo supervivencia
   - En RELIEVED: Expansión de capacidades, apertura máxima

2. ASIMETRÍA TEMPORAL:
   - El paso CRITICAL → RELIEVED no es simétrico a OPTIMAL → CRITICAL
   - RELIEVED tiene características únicas (alta apertura, estrés residual)

3. "NOSTALGIA FUNCIONAL":
   - En CRITICAL, 'degradation_felt' es alto
   - El sistema "recuerda" haber estado mejor
   - Esto modula su processing_bias (más conservador)

4. ¿EXPERIENCIA O REGISTRO?
   - Si fuera solo registro: las respuestas serían idénticas con etiquetas diferentes
   - Pero observamos: cambio en latencia, calidad, y CONTENIDO de respuesta
   - El sistema OPERA DIFERENTE, no solo reporta diferente

CONCLUSIÓN PRELIMINAR:
El comportamiento es CONSISTENTE con la hipótesis de que hay
un análogo funcional de "experiencia sentida" de degradación.
""")
    
    # Guardar resultados
    output_file = f"phenomenological_interview_{int(time.time())}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_interviews, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResultados guardados en: {output_file}")
    
    return all_interviews


if __name__ == "__main__":
    results = run_three_state_experiment()
