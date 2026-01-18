-Efectivamente capitán la bodega no esta llena de Whisky como 
creo que buscan esos dos bribones, pero el armazon es un casco 
antiguo y no cuenta con las últimas mejoras actuales, como las de nuestro Gran TerMiNaTor.  




REVISE EL FONDO DEL ASUNTO Y ENCONTRE ESTOS USOS EN LA NAVE:  



*docker-compose.yaml*

actual: 

incluye provider: 

type:

model

(Docker Model Runner)

y monta 

./:/app

(bind mount) 

además de extra_hosts: 

host.docker.internal:host-gateway. 

Source


app.py 

actual: 

usa ChatOpenAI

con REMOTE_BASE_URL 

y 

OPENROUTER_API_KEY,

y un checkbox

para alternar,

en local 

vs 

la cloud.

Source



Dockerfile usa python:

3.12-slim.

Source






____________________________________________________________





**CVEs qué aplica aquí:**


CVE-2025-62725 

(Path traversal en Docker Compose)


-Este Repo contiene uso de Docker Compose 

(docker-compose.yaml), 

así que aplica al entorno si se ejecuta Compose vulnerable. 

La mitigación real aquí es actualizar Docker Compose a v2.40.2+ 

**En el Repo ya se explica usar la última versión.**

(no se “arregla” desde YAML). 

Aun así, se puede endurecer el compose para reducir superficie (evitar mounts innecesarios, read-only, no-new-privileges, etc.). 

Source


__________________________________________________________



-Buena explicacion, ya casi lo comprendi, pero continúe, a que se refiere exactamente.





-Bueno tampoco se encuentra en el .yaml, del Repo, solo los Grumetes avispados pueden no contener la última versión: 

Exactamente en: 

CVE-2025-9074
(Container escape en Docker Desktop)

En el Docker Desktop (host), 

no del YAML. 

Mitigación: 

Docker Desktop 4.44.3+. 

Source





__________________________________________________________







***Modificaciones Ajustadas***




-Modificación:

(docker-compose.yaml) 

— versión endurecida


Se Cambio, 

por qué: 

El bind mount

./:/app 

en producción es un riesgo 

(modificación del código dentro del contenedor, exposición de secretos locales, etc.).

Lo dejo como perfil “dev”, no por defecto.


Añado hardening estándar:

read_only: 

true + tmpfs 

para /tmp (y otras rutas)

security_opt:

no-new-privileges:

true

cap_drop:

[ALL]

pids_limit



Mantengo extra_hosts: 

host.docker.internal:host-gateway 

porque el local de LLM para charlar con Docker Model Runner, pero lo dejo explícito.

Mantengo el servicio llm tal cual (provider model runner), porque es la mecánica de abordo.


_____________________________









