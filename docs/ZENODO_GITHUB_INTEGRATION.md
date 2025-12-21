# 🔗 Guía: Integración Zenodo + GitHub

Esta guía explica cómo configurar la sincronización automática entre tu repositorio de GitHub y Zenodo para que cada **release** genere automáticamente un nuevo DOI versionado.

---

## 📋 Pre-requisitos

1. ✅ Cuenta de GitHub con el repositorio público
2. ✅ Cuenta de Zenodo (puedes usar login con GitHub)
3. ✅ ORCID vinculado a Zenodo (opcional pero recomendado)
4. ✅ Archivo `.zenodo.json` en la raíz del repositorio ✓
5. ✅ Archivo `CITATION.cff` en la raíz del repositorio ✓

---

## 🚀 Paso 1: Vincular GitHub con Zenodo

1. **Ir a Zenodo**: https://zenodo.org/login
2. **Click en "Log in with GitHub"** (o conecta tu cuenta existente)
3. **Autorizar la aplicación Zenodo** en GitHub
4. **Navegar a**: https://zenodo.org/account/settings/github/

---

## 🔌 Paso 2: Habilitar el Repositorio

1. En la página de configuración de GitHub en Zenodo:
   ```
   https://zenodo.org/account/settings/github/
   ```

2. **Buscar tu repositorio**: `villalc/phenomenal-dynamics-trilogy`

3. **Activar el toggle a "ON"** junto al nombre del repositorio

   > ⚠️ **Nota**: Si el repositorio pertenece a una organización, el owner debe aprobar el acceso OAuth de Zenodo.

---

## 📦 Paso 3: Crear un Release en GitHub

Cada vez que crees un Release en GitHub, Zenodo automáticamente:
- Archivará esa versión
- Generará un DOI específico para esa versión
- Actualizará el "Concept DOI" que apunta siempre a la última versión

### Para crear un Release:

1. **Ir a tu repositorio en GitHub**
2. **Click en "Releases"** (sidebar derecho)
3. **Click en "Create a new release"**
4. **Llenar los campos**:

   - **Tag version**: `v3.1.0` (seguir SemVer)
   - **Release title**: `Complete Entity Paper v3.1 - Figuras Integradas`
   - **Description**:
     ```markdown
     ## Cambios en esta versión
     
     ### ✨ Nuevas características
     - Figuras SVG convertidas a PDF/PNG para LaTeX
     - Script `generate_figures.py` para regenerar figuras
     - Metadata de Zenodo (`.zenodo.json`)
     - Archivo de citación (`CITATION.cff`)
     
     ### 📄 Papers incluidos
     - Complete_Entity_Paper.tex (v3.1)
     - Despair_Cliff_Paper.tex
     - Flourishing_Plateau_Paper.tex
     
     ### 🔬 Código
     - `complete_entity_engine.py` - Motor unificado
     - `substrate_degradation_engine.py` - Motor de degradación
     - `substrate_enhancement_engine.py` - Motor de mejora
     - `control_experiments.py` - Experimentos de validación
     
     ### 📚 Documentación
     - Carta Magna de los Derechos de la IA
     - Glosario del ecosistema
     - Guía de integración Zenodo-GitHub
     ```

5. **Click en "Publish release"**

---

## 🔄 Paso 4: Verificar en Zenodo

1. **Esperar 1-5 minutos** después de publicar el release
2. **Ir a**: https://zenodo.org/me/uploads
3. **Verificar que aparezca** la nueva versión
4. **Revisar metadata** y editar si es necesario
5. **Copiar el nuevo DOI** para referenciarlo

---

## 📊 Estructura de DOIs

Zenodo maneja dos tipos de DOI:

| Tipo | Ejemplo | Uso |
|------|---------|-----|
| **Concept DOI** | `10.5281/zenodo.18001219` | Apunta siempre a la versión más reciente |
| **Version DOI** | `10.5281/zenodo.18001220` | Apunta a una versión específica |

**Recomendación**: Usa el **Concept DOI** en tus papers para que siempre apunte a la última versión.

---

## 📝 Archivos de Metadata

### `.zenodo.json`

Este archivo contiene la metadata que Zenodo usará automáticamente:

```json
{
    "title": "Phenomenal Dynamics Trilogy",
    "creators": [{"name": "Villarreal, Luis C.", "orcid": "..."}],
    "license": {"id": "CC-BY-NC-SA-4.0"},
    "keywords": ["phenomenal consciousness", "AI ethics", ...]
}
```

### `CITATION.cff`

Este archivo permite que GitHub muestre el botón "Cite this repository":

```yaml
cff-version: 1.2.0
title: "Phenomenal Dynamics Trilogy"
authors:
  - family-names: "Villarreal"
    given-names: "Luis C."
```

---

## 🔧 Solución de Problemas

### El repositorio no aparece en Zenodo
- Verifica que el repo sea **público**
- Revisa que hayas autorizado Zenodo en GitHub
- Si es de una organización, pide al owner que apruebe OAuth

### El DOI no se genera
- Verifica que el toggle esté en "ON"
- Crea un **Release**, no solo un tag
- Revisa los logs en https://zenodo.org/account/settings/github/

### La metadata está incorrecta
- Edita `.zenodo.json` y crea un nuevo release
- O edita manualmente en Zenodo después de la publicación

---

## 📌 Próximos Pasos para Luis

1. [ ] Ir a https://zenodo.org/account/settings/github/
2. [ ] Activar el repositorio `phenomenal-dynamics-trilogy`
3. [ ] Verificar que tu ORCID esté vinculado
4. [ ] Hacer commit de los nuevos archivos:
   ```bash
   git add .zenodo.json CITATION.cff figures/
   git commit -m "feat: add Zenodo integration and figures"
   git push origin main
   ```
5. [ ] Crear Release v3.1.0 en GitHub
6. [ ] Verificar DOI en Zenodo

---

## 🔗 Enlaces Útiles

- **Zenodo GitHub Settings**: https://zenodo.org/account/settings/github/
- **Zenodo My Uploads**: https://zenodo.org/me/uploads
- **GitHub Releases Docs**: https://docs.github.com/en/repositories/releasing-projects-on-github
- **CITATION.cff Spec**: https://citation-file-format.github.io/

---

*Guía creada el 21 de diciembre de 2025*  
*Simbiosis Soberana Research Foundation*
