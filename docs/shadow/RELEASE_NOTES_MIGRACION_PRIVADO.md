# Release Notes · Migracion a Privado (Shadow)

## Corte
- Fecha: 2026-03-21
- Alcance: cierre de etapa Shadow en copia phenomenal-dynamics-trilogy

## Cambios funcionales
1. Ingestion Frontier multi-esquema a manifiesto canonico Shadow.
2. Politicas profile-driven para decision soberana (balanced/conservative/frontier/recovery).
3. Control de ventanas y cooldown para promociones canonical/exploratory.
4. Export pack portable con indice y resumen ejecutivo.
5. Validacion de esquema de manifiestos y firma SHA-256 de pack.

## Artefactos principales
- Ingestion:
  - src/swarmguard/frontier_ingest.py
  - ingest_frontier_artifacts.py
- Decision y politicas:
  - src/swarmguard/shadow_bridge.py
  - src/swarmguard/shadow_policy.py
  - src/swarmguard/shadow_window.py
- Pack y validacion:
  - src/swarmguard/shadow_export_pack.py
  - src/swarmguard/shadow_validate.py
  - build_shadow_pack.py
  - src/swarmguard/shadow_signing.py
  - sign_shadow_pack.py

## Resultado de ejecucion real
- Manifiestos generados desde artifacts: 92
- invalid_count en pack: 0
- Pack firmado con SHA-256

## Estado de calidad
- Suite Shadow en verde en el corte.
- Frontera de riesgo preservada: componentes mock siguen etiquetados como no productivos.

## Riesgo residual
- Politicas de ventana/cooldown son baseline; pueden calibrarse por entorno privado.
- Firma actual por hash (SHA-256) lista para trazabilidad; firma asimetrica opcional en siguiente ciclo.
