# Plan por Fases · Adaptacion Shadow Quantum

## Objetivo
Convertir phenomenal-dynamics-trilogy en una copia operativa orientada a Shadow Quantum, manteniendo trazabilidad y frontera limpia para migracion posterior a repositorio privado.

## Principios de trabajo
- Shadow primero: toda integracion nueva nace en esta copia.
- Evidencia obligatoria: toda decision deja artefacto verificable.
- Frontera explicita: lo experimental no se etiqueta como productivo.
- Portabilidad: cada fase deja carpeta exportable.

## Fase 1 (implementada): Base de trazabilidad Shadow
Entregables:
- Modelo de manifiesto de corrida y eventos:
  - src/swarmguard/shadow_models.py
- Persistencia de manifiestos:
  - src/swarmguard/shadow_manifest.py
- Adaptador de metricas fenomenales a metricas Shadow y puente de decision:
  - src/swarmguard/shadow_bridge.py

Criterio de salida:
- Se puede serializar una corrida Shadow y registrar decisiones con audit chain.

## Fase 2: Acople a campañas Frontier (baseline implementado)
Objetivo:
- Consumir salidas de corridas Frontier (v2-v4) y normalizarlas en ShadowRunManifest.

Entregables implementados:
- Ingestor multi-esquema para artifacts Frontier:
  - src/swarmguard/frontier_ingest.py
- CLI de ingestion por lote:
  - ingest_frontier_artifacts.py
- Cobertura de pruebas para esquemas runs/variants/profiles:
  - tests/test_frontier_ingest.py

Comando de ejecucion:
- python ingest_frontier_artifacts.py --artifact-dir ../artifacts

Pendiente para cierre completo de fase:
- Mapping versionado de campos legacy -> shadow schema.
- Reporte comparativo por corrida (deuda, promociones, riesgo).

Criterio de salida:
- Cualquier corrida Frontier produce manifiesto canonico sin edicion manual.

## Fase 3: Politica de decision soberana (baseline implementado)
Objetivo:
- Reemplazar heuristicas fijas por politica configurable y testeable.

Entregables implementados:
- Politicas por perfil:
  - src/swarmguard/shadow_policy.py
- Bridge de decision profile-driven:
  - src/swarmguard/shadow_bridge.py
- Ingestor Frontier con politica conservative por defecto:
  - src/swarmguard/frontier_ingest.py
- Pruebas de consistencia de perfiles:
  - tests/test_shadow_policy.py

Pendiente para cierre completo de fase:
- Umbrales por fase temporal y ventana de promociones.
- Registro de cooldown/limites de canonizacion por run.

Criterio de salida:
- Las decisiones son reproducibles y auditables con perfiles intercambiables.

## Fase 4: Reporte ejecutivo y paquete portable (baseline implementado)
Objetivo:
- Generar paquete para traslado al repo privado con trazabilidad completa.

Entregables implementados:
- Constructor de export pack:
  - src/swarmguard/shadow_export_pack.py
- CLI de build de pack:
  - build_shadow_pack.py
- Salidas de pack:
  - pack_index.json
  - executive_summary.md
  - carpeta manifests copiada para traslado

Pendiente para cierre completo de fase:
- Ninguno en baseline. Fase operativa para traslado.

Criterio de salida:
- Carpeta transferible con evidencia de integridad, comparativas y estado final.

## Fase 5: Hardening para alineacion privada (baseline implementado)
Objetivo:
- Preparar el paquete para acople en entorno privado sin contaminar principal.

Entregables implementados:
- Validacion de esquema de manifiesto:
  - src/swarmguard/shadow_validate.py
- Cobertura de regresion de esquema y pack:
  - tests/test_shadow_validate.py
  - tests/test_shadow_export_pack.py

Pendiente para cierre completo de fase:
- Ninguno en baseline. Queda opcional evolucionar a firma asimetrica en siguiente ciclo.

Criterio de salida:
- Integracion privada predecible, reversible y trazable.
