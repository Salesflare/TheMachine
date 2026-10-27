---
title: GitHub
area: connections
summary: Solicitudes de revisión, menciones, asignaciones y ejecuciones de CI fallidas. Solo lee.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
---
## Qué lee

Tus notificaciones de GitHub: solicitudes de revisión, menciones, asignaciones, respuestas y ejecuciones de CI fallidas. Nunca marca una notificación como leída.

## Qué puede hacer

Nada en GitHub. Cada llamada que hace es de lectura.

## Conéctalo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre GitHub y pulsa **Iniciar sesión con GitHub**.
3. Escribe en GitHub el código que muestra, en tu teléfono o tu ordenador.

En tu propio ordenador:

1. Inicia sesión primero en la CLI de GitHub: `gh auth login`.
2. En el panel, abre **Conexiones**, luego **+ Añadir**, y elige GitHub. O ejecuta `assistant connect github`.
3. Confirma tu usuario de GitHub. The Machine comprueba que coincide en cada sincronización.

## Quítalo

- En el panel: **Conexiones**, abre GitHub, **Detalles** y luego **Desconectar**. Deja de leer. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Desinstálalo en GitHub

Revoca el acceso de la CLI de GitHub en GitHub, en Settings, Applications, Authorized OAuth Apps. En tu propio ordenador, `gh auth logout` también cierra la sesión de la CLI.
