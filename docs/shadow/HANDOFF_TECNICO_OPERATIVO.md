# Handoff Tecnico Operativo · Shadow Copy

## Estado al corte
- Fase 1: completada.
- Fase 2: baseline operativa + ingestion real ejecutada.
- Fase 3: baseline profile-driven activa.
- Fase 4: pack portable generado y validado.
- Fase 5: baseline de hardening con validacion de esquema y firma SHA-256.

## Comandos operativos
1. Ingestar artifacts Frontier:
- python ingest_frontier_artifacts.py --artifact-dir ../artifacts

2. Construir pack portable:
- python build_shadow_pack.py --manifest-dir data/shadow_exports/frontier_ingest --pack-name shadow_pack_phase4

3. Firmar pack:
- python sign_shadow_pack.py --pack-dir data/shadow_exports/packs/shadow_pack_phase4

## Artefactos de salida esperados
- data/shadow_exports/frontier_ingest/*.json
- data/shadow_exports/packs/<pack>/pack_index.json
- data/shadow_exports/packs/<pack>/executive_summary.md
- data/shadow_exports/packs/<pack>/pack_signatures.json
- data/shadow_exports/packs/<pack>/manifests/*.json

## Criterio de aceptacion para traslado al privado
- Tests shadow en verde.
- invalid_count = 0 en pack.
- pack_signatures.json presente.
- Checklist de handoff verificado.

## Notas de frontera
- Mecanismos ZK actuales siguen en modo mock para demo/investigacion.
- La decision policy por perfil se considera baseline y puede endurecerse por entorno privado.
