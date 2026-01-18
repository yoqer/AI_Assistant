# Security & Provider Changes (AI_Assistant)

## Resumen
Este repo usa Docker Compose y Docker Desktop como runtime. No se puede “parchear” una CVE de Docker Compose/ Desktop desde YAML, pero sí se puede:
1) exigir versiones seguras del runtime, y
2) endurecer la configuración del contenedor para reducir impacto en caso de fallo.

## CVEs referenciadas y mitigación

### CVE-2025-62725 (Docker Compose Path Traversal)
- Afecta al runtime de Docker Compose (host).
- Mitigación: actualizar Docker Compose a v2.40.2+.
Referencia: https://nvd.nist.gov/vuln/detail/CVE-2025-62725

### CVE-2025-9074 (Docker Desktop Container Escape)
- Afecta a Docker Desktop en Windows/macOS.
- Mitigación: Docker Desktop 4.44.3+.
Referencia: https://docs.docker.com/security/security-announcements/

### CVE-2025-12735 (Docker Hardened Images)
- Este repo NO usa Docker Hardened Images actualmente (usa python:3.12-slim).
- No aplica directamente al código actual.
Referencia: https://www.docker.com/blog/security-that-strengthens-the-ecosystem-dockers-upstream-approach-to-cve-2025-12735/

## Cambios realizados en docker-compose.yaml

### 1) Eliminación del bind mount por defecto
Antes:
- Se montaba `./:/app`, lo que expone el árbol local al contenedor y facilita modificación accidental/maliciosa del runtime.

Ahora:
- No se monta el repo por defecto.
- Se documenta el uso de un perfil "dev" (recomendación: usar override/ profile para desarrollo).

Beneficio:
- Reduce superficie de ataque y evita exposición de ficheros locales y secretos.

### 2) Endurecimiento del contenedor (hardening)
Se añadieron:
- `read_only: true` + `tmpfs` para rutas temporales
- `security_opt: no-new-privileges:true`
- `cap_drop: [ALL]`
- `pids_limit`

Beneficio:
- Limita escaladas de privilegios dentro del contenedor.
- Reduce impacto si la app o dependencias fueran comprometidas.

## Selección de proveedor/modelo remoto (API compatible OpenAI)
La app ya soporta `REMOTE_BASE_URL` y un API key.
Para usar un proveedor distinto a OpenRouter (por ejemplo un endpoint OpenAI-compatible de otro proyecto):
- Configura:
  - REMOTE_BASE_URL=https://tu-endpoint/v1
  - REMOTE_MODEL_NAME=tu-modelo
  - REMOTE_API_KEY=tu-api-key
- Y usa ese API key en lugar de OPENROUTER_API_KEY.

Nota: la app necesita soportar REMOTE_API_KEY además de OPENROUTER_API_KEY si se quiere desacoplar proveedor. (Recomendado para multi-proveedor).
