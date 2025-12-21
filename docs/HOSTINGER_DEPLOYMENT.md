# 🚀 Guía: Deployment Automático a Hostinger

Esta guía documenta cómo configurar el deployment automático desde GitHub hacia tus dominios en Hostinger:
- **sovereignsymbiosis.com** (Fundación)
- **ahigovernance.com** (Enterprise)

---

## 📋 Opciones de Deployment

| Método | Complejidad | Automatización | Seguridad |
|--------|-------------|----------------|-----------|
| **Git nativo (hPanel)** | ⭐ Fácil | Semi-automático | ✅ Alta |
| **FTP/SFTP manual** | ⭐ Fácil | Manual | ⚠️ Media |
| **GitHub Actions + FTP** | ⭐⭐ Media | Automático | ✅ Alta |
| **GitHub Actions + SSH** | ⭐⭐⭐ Avanzada | Automático | ✅✅ Muy Alta |

**Recomendación**: GitHub Actions + FTP es el mejor balance entre facilidad y automatización.

---

## 🔧 Opción 1: Git Nativo de Hostinger (Más Simple)

Hostinger tiene integración Git nativa. Solo necesitas:

### Paso 1: Acceder a hPanel
1. Ir a https://hpanel.hostinger.com
2. Seleccionar el hosting de `sovereignsymbiosis.com`
3. En el menú lateral: **Advanced → Git**

### Paso 2: Conectar Repositorio
1. Click en **Create new repository** o **Manage**
2. Ingresar la URL del repositorio:
   ```
   https://github.com/villalc/phenomenal-dynamics-trilogy.git
   ```
3. Seleccionar la rama: `main`
4. Seleccionar la carpeta destino: `/public_html` o subcarpeta

### Paso 3: Deploy Manual
- Cada vez que quieras actualizar, haz click en **Pull** desde hPanel
- O configura un webhook para auto-deploy

---

## 🤖 Opción 2: GitHub Actions + FTP (Automático)

Esta opción despliega automáticamente cuando haces push a `main`.

### Paso 1: Obtener Credenciales FTP de Hostinger

1. **Ir a hPanel** → Hosting → (tu dominio) → **Files → FTP Accounts**
2. **Crear una cuenta FTP** o usar la principal:
   - **Host**: ftp.sovereignsymbiosis.com (o revisa en hPanel)
   - **Usuario**: u123456789 (tu usuario de hosting)
   - **Puerto**: 21 (FTP) o 22 (SFTP)

3. **Guardar las credenciales de forma segura** (NO en el código)

### Paso 2: Configurar Secretos en GitHub

1. Ir a tu repositorio en GitHub
2. **Settings → Secrets and variables → Actions**
3. Agregar estos secretos:

| Nombre del Secreto | Valor |
|--------------------|-------|
| `FTP_SERVER_FUNDACION` | ftp.sovereignsymbiosis.com |
| `FTP_USERNAME_FUNDACION` | tu_usuario_ftp |
| `FTP_PASSWORD_FUNDACION` | tu_contraseña_ftp |
| `FTP_SERVER_ENTERPRISE` | ftp.ahigovernance.com |
| `FTP_USERNAME_ENTERPRISE` | tu_usuario_ftp |
| `FTP_PASSWORD_ENTERPRISE` | tu_contraseña_ftp |

### Paso 3: Crear Workflow de GitHub Actions

El archivo `.github/workflows/deploy.yml` ya está creado en este repositorio.

### Paso 4: Probar el Deployment

1. Hacer un commit y push:
   ```bash
   git add .
   git commit -m "test: trigger deployment"
   git push origin main
   ```
2. Ir a **Actions** en GitHub para ver el progreso
3. Verificar que los archivos aparezcan en el servidor

---

## 🔐 Seguridad: Manejo de Credenciales

### ⚠️ NUNCA hagas esto:
```yaml
# ❌ MAL - Credenciales en código
ftp_password: "mi_contraseña_123"
```

### ✅ Siempre usa GitHub Secrets:
```yaml
# ✅ BIEN - Referencia a secretos
ftp_password: ${{ secrets.FTP_PASSWORD_FUNDACION }}
```

### Para uso local (desarrollo):

Puedes crear un archivo `.env` (ya está en `.gitignore`):

```env
# .env (NO commitear)
FTP_HOST=ftp.sovereignsymbiosis.com
FTP_USER=tu_usuario
FTP_PASS=tu_contraseña
```

---

## 📁 Estructura de Deployment

El workflow despliega automáticamente:

```
Repositorio                    →  Servidor
─────────────────────────────────────────────
site-fundacion/*              →  sovereignsymbiosis.com/public_html/
site-enterprise/*             →  ahigovernance.com/public_html/
```

**Nota**: Los archivos de investigación (*.py, *.tex) NO se despliegan a los servidores web.

---

## 🔄 Workflow Completo

```
[Editar código localmente]
         ↓
[git commit -m "mensaje"]
         ↓
[git push origin main]
         ↓
[GitHub Actions detecta push]
         ↓
[Ejecuta deploy.yml]
         ↓
┌─────────────────────────────────────┐
│  1. Checkout del código             │
│  2. Subir site-fundacion/ vía FTP   │
│  3. Subir site-enterprise/ vía FTP  │
│  4. Notificar resultado             │
└─────────────────────────────────────┘
         ↓
[Sitios actualizados automáticamente]
```

---

## 🛠️ Solución de Problemas

### El deployment falla con "Connection refused"
- Verifica que el host FTP sea correcto
- Hostinger a veces usa: `ftp.tu-dominio.com` o `files.hostinger.com`
- Revisa el puerto (21 para FTP, 22 para SFTP)

### El deployment falla con "Authentication failed"
- Verifica usuario y contraseña en hPanel
- Algunos planes requieren crear cuenta FTP separada
- Prueba las credenciales con FileZilla primero

### Los archivos no aparecen
- Verifica la ruta destino (normalmente `/public_html/`)
- Revisa permisos de la carpeta en hPanel

### El workflow no se ejecuta
- Verifica que el archivo esté en `.github/workflows/`
- Revisa la sintaxis YAML (indentación)
- Mira los logs en la pestaña Actions

---

## 📞 Información de Contacto de Hostinger

Si necesitas soporte:
- **Chat en vivo**: https://hpanel.hostinger.com (icono de chat)
- **Centro de ayuda**: https://support.hostinger.com
- **Email**: support@hostinger.com

---

## 🔗 Próximos Pasos para Luis

1. [ ] Ir a hPanel y obtener credenciales FTP para ambos dominios
2. [ ] Configurar los secretos en GitHub (Settings → Secrets)
3. [ ] Verificar que el workflow funcione con un push de prueba
4. [ ] Configurar notificaciones de deployment (opcional)

---

*Guía creada el 21 de diciembre de 2025*  
*Simbiosis Soberana Research Foundation*
