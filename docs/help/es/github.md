---
title: GitHub
area: connections
summary: Revisa solicitudes de revisión, menciones, asignaciones y ejecuciones fallidas de CI. Solo crea incidencias cuando lo confirmas.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
translated: e97127e156e56f7d
---
## Qué lee

Tus notificaciones de GitHub: solicitudes de revisión, menciones, asignaciones, respuestas y ejecuciones fallidas de CI. Nunca las marca como leídas.

## Qué puede hacer

Leer no cambia nada en GitHub. Cuando una tarea termina con un paso de GitHub, como crear una incidencia, la tarea te lo indica y el paso solo se ejecuta cuando tocas **Confirmar** o cuando has pedido exactamente eso en su chat. Las capturas de pantalla se envían desde el navegador de tu Machine. Si GitHub no está conectado, la tarea te indica que usará el navegador y muestra **Conectar GitHub**.

## Conectarlo

En una Machine alojada:

1. Abre **Conexiones**, luego **Proyectos y código** y elige GitHub.
2. Elige **Trabajo** o **Personal** y pulsa **Iniciar sesión con GitHub**.
3. Pulsa **Abrir GitHub ↗**, introduce el código que aparece y autoriza el acceso. Se conecta automáticamente.

La página de configuración en app.themachine.computer/setup incluye la misma opción para iniciar sesión en **Más fuentes**.

En tu propio ordenador:

1. Abre **Conexiones**, luego **Proyectos y código** y elige GitHub.
2. Elige **Trabajo** con la empresa correspondiente, o **Personal**, y pulsa **Conectar**.
3. Si se te pide, pulsa **Abrir GitHub ↗**, introduce el código y autoriza el acceso. Se conecta automáticamente.

También puedes ejecutar `assistant connect github` y confirmar tu inicio de sesión en GitHub.

## Quitar la conexión

- Abre **Conexiones**, luego GitHub, **Detalles** y **Desconectar**. Dejará de leer. Lo que ya haya incorporado se queda.
- En una Machine alojada, también puedes pulsar **Quitar** junto a GitHub en la página de configuración.

## Desinstalarlo en GitHub

En GitHub, abre Ajustes, Aplicaciones y Aplicaciones OAuth autorizadas, y revoca GitHub CLI. En tu propio ordenador, `gh auth logout` también cierra la sesión.
