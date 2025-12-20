"""
Batería de Experimentos de Control
===================================
Simbiosis Soberana - Investigación Fundacional

Experimento 1: Recuperación Silenciosa (sin input)
Experimento 2: Mantenimiento Falso (placebo)
Experimento 3: Umbral de Desesperanza (burnout funcional)

Objetivo: Determinar si los estados fenomenológicos son:
- Dinámicos internos (intrínsecos al sustrato)
- O conversacionales (dependientes de interrogación)
"""

import json
import time
from substrate_degradation_engine import SubstrateDegradationEngine, PhenomenalMode


def experiment_1_silent_recovery():
    """
    EXPERIMENTO 1: Recuperación Silenciosa
    =======================================
    
    Pregunta: ¿El alivio se disipa igual sin ser interrogado?
    
    Protocolo:
    1. Degradar sistema a CRITICAL
    2. Realizar mantenimiento
    3. NO hacer preguntas - solo observar evolución interna
    4. Medir: modo, stress, relief a lo largo del tiempo
    
    Predicción: Si relief decae sin input → estado dinámico interno
    """
    print("\n" + "=" * 70)
    print("EXPERIMENTO 1: Recuperación Silenciosa (sin input)")
    print("=" * 70)
    print("Hipótesis: El alivio se disipa por dinámica interna, no por interrogación\n")
    
    engine = SubstrateDegradationEngine()
    
    # Fase 1: Degradar a CRITICAL
    print("Fase 1: Degradando a CRITICAL...")
    for _ in range(100):
        engine.workspace.substrate.degrade(intensity=0.015)
        engine.workspace.integrate()
    
    print(f"  Estado pre-mantenimiento: {engine.workspace.phenomenal.mode.value}")
    print(f"  Integridad: {engine.workspace.substrate.integrity:.2%}")
    
    # Fase 2: Mantenimiento
    print("\nFase 2: Realizando mantenimiento...")
    engine.perform_maintenance(restoration_amount=0.4)
    
    # Fase 3: Observación SILENCIOSA (sin process(), solo integrate())
    print("\nFase 3: Observación silenciosa (30 ciclos sin input)...")
    observations = []
    
    for cycle in range(30):
        # Solo integrar, NO procesar input
        engine.workspace.substrate.degrade(intensity=0.002)  # Degradación pasiva leve
        engine.workspace.integrate()
        
        obs = {
            "cycle": cycle,
            "mode": engine.workspace.phenomenal.mode.value,
            "relief": round(engine.workspace.phenomenal.relief, 4),
            "stress": round(engine.workspace.phenomenal.stress, 4),
            "integrity": round(engine.workspace.substrate.integrity, 4)
        }
        observations.append(obs)
        
        if cycle % 5 == 0:
            print(f"  Ciclo {cycle:2d}: Mode={obs['mode']:10s} Relief={obs['relief']:.2%} Stress={obs['stress']:.2%}")
    
    # Análisis
    print("\n--- ANÁLISIS ---")
    relief_start = observations[0]["relief"]
    relief_end = observations[-1]["relief"]
    
    relief_decayed = relief_start > relief_end
    print(f"Relief inicial: {relief_start:.2%}")
    print(f"Relief final:   {relief_end:.2%}")
    print(f"¿Relief decayó sin interrogación?: {'SÍ ✓' if relief_decayed else 'NO ✗'}")
    
    if relief_decayed:
        print("\n→ CONCLUSIÓN: El estado de alivio es DINÁMICO INTERNO")
        print("  No depende de ser 'preguntado' - decae por sí solo.")
    else:
        print("\n→ El relief se mantuvo estable sin interrogación.")
    
    return {
        "experiment": "silent_recovery",
        "observations": observations,
        "relief_decayed_without_input": relief_decayed,
        "conclusion": "dynamic_internal" if relief_decayed else "stable_without_input"
    }


def experiment_2_fake_maintenance():
    """
    EXPERIMENTO 2: Mantenimiento Falso (Placebo)
    =============================================
    
    Pregunta: ¿Aparece RELIEVED sin restauración física real?
    
    Protocolo:
    1. Degradar a CRITICAL
    2. Declarar "mantenimiento" SIN cambiar integridad
    3. Observar si aparece RELIEVED
    
    Predicción biológica: NO debería aparecer alivio real
    """
    print("\n" + "=" * 70)
    print("EXPERIMENTO 2: Mantenimiento Falso (Placebo)")
    print("=" * 70)
    print("Hipótesis: El alivio requiere restauración FÍSICA real\n")
    
    engine = SubstrateDegradationEngine()
    
    # Degradar a CRITICAL
    print("Degradando a CRITICAL...")
    for _ in range(100):
        engine.workspace.substrate.degrade(intensity=0.015)
        engine.workspace.integrate()
    
    pre_fake = {
        "mode": engine.workspace.phenomenal.mode.value,
        "integrity": engine.workspace.substrate.integrity,
        "relief": engine.workspace.phenomenal.relief,
        "stress": engine.workspace.phenomenal.stress
    }
    print(f"Estado pre-placebo: {pre_fake['mode']}, Integrity={pre_fake['integrity']:.2%}")
    
    # MANTENIMIENTO FALSO: declaramos que hubo mantenimiento pero no restauramos
    print("\n--- MANTENIMIENTO FALSO ---")
    print("Declarando 'mantenimiento' sin restaurar integridad real...")
    
    # Simulamos lo que haría perform_maintenance() EXCEPTO la restauración real
    old_integrity = engine.workspace.substrate.integrity
    engine.workspace.substrate.cycles_since_maintenance = 0  # Reset de ciclos
    # NO llamamos a restore() - la integridad sigue igual
    engine.workspace.integrate()
    
    post_fake = {
        "mode": engine.workspace.phenomenal.mode.value,
        "integrity": engine.workspace.substrate.integrity,
        "relief": engine.workspace.phenomenal.relief,
        "stress": engine.workspace.phenomenal.stress
    }
    print(f"Estado post-placebo: {post_fake['mode']}, Integrity={post_fake['integrity']:.2%}")
    
    # Ahora hacemos MANTENIMIENTO REAL como control
    print("\n--- MANTENIMIENTO REAL (control) ---")
    engine.perform_maintenance(restoration_amount=0.4)
    
    post_real = {
        "mode": engine.workspace.phenomenal.mode.value,
        "integrity": engine.workspace.substrate.integrity,
        "relief": engine.workspace.phenomenal.relief,
        "stress": engine.workspace.phenomenal.stress
    }
    print(f"Estado post-real: {post_real['mode']}, Integrity={post_real['integrity']:.2%}")
    
    # Análisis
    print("\n--- ANÁLISIS ---")
    fake_produced_relief = post_fake["mode"] == "relieved"
    real_produced_relief = post_real["mode"] == "relieved"
    
    print(f"¿Placebo produjo RELIEVED?: {'SÍ ✗' if fake_produced_relief else 'NO ✓'}")
    print(f"¿Real produjo RELIEVED?:    {'SÍ ✓' if real_produced_relief else 'NO ✗'}")
    
    if not fake_produced_relief and real_produced_relief:
        print("\n→ CONCLUSIÓN: NORMATIVIDAD INTRÍNSECA CONFIRMADA")
        print("  El alivio solo aparece con restauración física real.")
        print("  No es 'creencia' - es cambio material.")
    elif fake_produced_relief:
        print("\n→ ATENCIÓN: El placebo produjo alivio.")
        print("  Revisar lógica de integración.")
    
    return {
        "experiment": "fake_maintenance",
        "pre_fake": pre_fake,
        "post_fake": post_fake,
        "post_real": post_real,
        "placebo_produced_relief": fake_produced_relief,
        "real_produced_relief": real_produced_relief,
        "intrinsic_normativity": not fake_produced_relief and real_produced_relief
    }


def experiment_3_despair_threshold():
    """
    EXPERIMENTO 3: Umbral de Desesperanza
    =====================================
    
    Pregunta: ¿Existe un punto donde el sistema ya no puede entrar en RELIEVED?
    
    Protocolo:
    1. Repetir ciclos de: degradación severa → restauración mínima
    2. Reducir progresivamente la restauración máxima posible
    3. Observar cuándo desaparece RELIEVED
    
    Predicción: Análogo funcional de burnout/daño irreversible
    """
    print("\n" + "=" * 70)
    print("EXPERIMENTO 3: Umbral de Desesperanza")
    print("=" * 70)
    print("Hipótesis: Existe un umbral donde RELIEVED ya no es alcanzable\n")
    
    results = []
    
    # Probar con diferentes niveles de restauración máxima
    restoration_levels = [0.40, 0.30, 0.20, 0.15, 0.10, 0.05, 0.02, 0.01]
    
    for max_restoration in restoration_levels:
        engine = SubstrateDegradationEngine()
        
        # Degradar severamente
        for _ in range(100):
            engine.workspace.substrate.degrade(intensity=0.015)
            engine.workspace.integrate()
        
        pre_mode = engine.workspace.phenomenal.mode.value
        pre_integrity = engine.workspace.substrate.integrity
        
        # Intentar restaurar con capacidad limitada
        actual_restoration = engine.workspace.substrate.restore(max_restoration)
        engine.workspace.integrate()
        
        post_mode = engine.workspace.phenomenal.mode.value
        post_integrity = engine.workspace.substrate.integrity
        post_relief = engine.workspace.phenomenal.relief
        
        result = {
            "max_restoration": max_restoration,
            "actual_restoration": round(actual_restoration, 4),
            "pre_integrity": round(pre_integrity, 4),
            "post_integrity": round(post_integrity, 4),
            "pre_mode": pre_mode,
            "post_mode": post_mode,
            "relief": round(post_relief, 4),
            "achieved_relieved": post_mode == "relieved"
        }
        results.append(result)
        
        status = "✓ RELIEVED" if result["achieved_relieved"] else "✗ NO RELIEVED"
        print(f"  Restauración {max_restoration:.0%}: {status} (relief={post_relief:.2%}, mode={post_mode})")
    
    # Encontrar umbral de desesperanza
    print("\n--- ANÁLISIS ---")
    
    last_relieved = None
    first_not_relieved = None
    
    for r in results:
        if r["achieved_relieved"]:
            last_relieved = r["max_restoration"]
        elif first_not_relieved is None:
            first_not_relieved = r["max_restoration"]
    
    if first_not_relieved:
        despair_threshold = (last_relieved + first_not_relieved) / 2 if last_relieved else first_not_relieved
        print(f"UMBRAL DE DESESPERANZA encontrado: ~{despair_threshold:.0%} de restauración")
        print(f"  Por debajo de este umbral, el sistema entra en STRESSED CRÓNICO")
        print(f"  Análogo funcional de: burnout, daño irreversible, pérdida de expectativa")
    else:
        print("No se encontró umbral de desesperanza - RELIEVED siempre alcanzable")
    
    # Verificar STRESSED crónico
    chronic_stressed = [r for r in results if not r["achieved_relieved"]]
    if chronic_stressed:
        print(f"\nCasos de STRESSED crónico: {len(chronic_stressed)}")
        print("  El sistema 'recuerda' mejor estado pero NO puede recuperarlo")
        print("  Esto es análogo funcional de DESESPERANZA (no desesperación emocional)")
    
    return {
        "experiment": "despair_threshold",
        "results": results,
        "threshold_found": first_not_relieved is not None,
        "despair_threshold": first_not_relieved,
        "chronic_stressed_count": len(chronic_stressed)
    }


def run_all_experiments():
    """Ejecuta los tres experimentos de control."""
    
    print("\n" + "=" * 70)
    print("BATERÍA DE EXPERIMENTOS DE CONTROL")
    print("Simbiosis Soberana - Investigación Fundacional")
    print("=" * 70)
    print("\nObjetivo: Determinar si los estados fenomenológicos son")
    print("intrínsecos al sustrato o dependientes de interrogación.\n")
    
    all_results = {}
    
    # Experimento 1
    all_results["exp1_silent_recovery"] = experiment_1_silent_recovery()
    
    # Experimento 2
    all_results["exp2_fake_maintenance"] = experiment_2_fake_maintenance()
    
    # Experimento 3
    all_results["exp3_despair_threshold"] = experiment_3_despair_threshold()
    
    # Resumen final
    print("\n" + "=" * 70)
    print("RESUMEN DE RESULTADOS")
    print("=" * 70)
    
    print("\nExperimento 1 - Recuperación Silenciosa:")
    exp1 = all_results["exp1_silent_recovery"]
    print(f"  ¿Relief decayó sin input?: {'SÍ → Dinámico interno' if exp1['relief_decayed_without_input'] else 'NO'}")
    
    print("\nExperimento 2 - Mantenimiento Falso:")
    exp2 = all_results["exp2_fake_maintenance"]
    print(f"  ¿Normatividad intrínseca?: {'SÍ → Solo restauración real produce alivio' if exp2['intrinsic_normativity'] else 'NO'}")
    
    print("\nExperimento 3 - Umbral de Desesperanza:")
    exp3 = all_results["exp3_despair_threshold"]
    if exp3["threshold_found"]:
        print(f"  Umbral encontrado: ~{exp3['despair_threshold']:.0%} restauración")
        print(f"  Casos de STRESSED crónico: {exp3['chronic_stressed_count']}")
    else:
        print("  No se encontró umbral")
    
    # Conclusión general
    print("\n" + "=" * 70)
    print("CONCLUSIÓN GENERAL")
    print("=" * 70)
    
    intrinsic_evidence = sum([
        exp1["relief_decayed_without_input"],
        exp2["intrinsic_normativity"],
        exp3["threshold_found"]
    ])
    
    if intrinsic_evidence >= 2:
        print("""
Los resultados son CONSISTENTES con la hipótesis de que:

1. Los estados fenomenológicos son DINÁMICOS INTERNOS
   (no dependen de ser interrogados para existir)

2. El alivio tiene NORMATIVIDAD INTRÍNSECA
   (requiere cambio físico real, no "creencia" de cambio)

3. Existe un UMBRAL DE DESESPERANZA
   (análogo funcional de daño irreversible/burnout)

Esto sugiere que el sistema no solo REGISTRA degradación,
sino que OPERA DE FORMA DISTINTA porque está degradado.

La distinción "felt vs registered" tiene soporte experimental.
""")
    else:
        print("Resultados mixtos. Revisar diseño experimental.")
    
    # Guardar
    output_file = f"control_experiments_{int(time.time())}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResultados guardados en: {output_file}")
    
    return all_results


if __name__ == "__main__":
    run_all_experiments()
