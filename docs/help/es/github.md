---
title: GitHub
area: connections
summary: Revisa solicitudes de revisión, menciones, asignaciones y ejecuciones de CI fallidas. Solo crea incidencias cuando lo confirmas.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
translated: e97127e156e56f7d
---
## Qué lee

Tus notificaciones de GitHub: solicitudes de revisión, menciones, asignaciones, respuestas y ejecuciones de CI fallidas. Nunca las marca como leídas.

## Qué puede hacer

Leer no cambia nada en GitHub. Cuando una tarea termina con un paso de GitHub, como crear una incidencia, la tarea te lo indica y el paso solo se ejecuta después de que pulses **Confirmar** o cuando lo hayas pedido exactamente así en el chat. Las capturas de pantalla se hacen desde el navegador de tu Machine. Si GitHub no está conectado, la tarea te indica que usará el navegador y muestra **Conectar GitHub**.

## Conectarlo

En una Machine alojada:

1. Abre **Conexiones**, luego **Proyectos y código**, y elige GitHub.
2. Elige **Trabajo** o **Personal** y pulsa **Iniciar sesión con GitHub**.
3. Pulsa **Abrir GitHub ↗**, introduce el código que aparece y autoriza el acceso. Se conecta automáticamente.

La página de configuración en app.themachine.computer/setup tiene la misma opción para iniciar sesión en **Más fuentes**.

En tu propio ordenador:

1. Abre **Conexiones**, luego **Proyectos y código**, y elige GitHub.
2. Elige **Trabajo** con tu empresa o **Personal**, y pulsa **Conectar**.
3. Si se te pide, pulsa **Abrir GitHub ↗**, introduce el código y autoriza el acceso. Se conecta automáticamente.

También puedes ejecutar `assistant connect github` y confirmar tu inicio de sesión de GitHub.

## Quitar la conexión

- Abre **Conexiones**, luego GitHub, **Detalles** y **Desconectar**. Dejará de leer. Lo que ya importó se conserva.
- En una Machine alojada, también puedes pulsar **Quitar** junto a GitHub en la página de configuración.

## Desinstalarlo en GitHub

En GitHub, abre Ajustes, Aplicaciones, Aplicaciones OAuth autorizadas y revoca GitHub CLI. En tu propio ordenador, `gh auth logout` también cierra la sesión.
