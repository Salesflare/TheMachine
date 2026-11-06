---
title: Registro de la Machine
area: connections
summary: El propio registro de tu Machine, para que detecte sus propios problemas. Solo lee.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
---
## Qué lee

El registro de tu OpenClaw Gateway: ejecuciones fallidas, traspasos rechazados, mensajes de Telegram que no salieron y los propios errores de The Machine. Una tarea te avisa cuando hay algo que arreglar.

## Correcciones que una actualización dejó a un lado

Cuando The Machine se actualiza y una de sus propias correcciones ya no encaja con la nueva versión, la actualización deja esa corrección a un lado y sigue, para que tu Machine nunca se quede en una versión antigua. Una tarea, **Rehacer una corrección que la actualización dejó a un lado**, nombra la corrección. Pide que la rehaga en la nueva versión, o cierra la tarea.

## Qué puede hacer

Nada. Solo lee el registro en tu propia Machine.

## Conéctalo

- En una Machine alojada está en tu página de configuración, en **Más fuentes**, como registro de OpenClaw Gateway. Uno por Machine.
- En tu propio ordenador: ejecuta `assistant connect gateway`.

## Quítalo

- En el panel: **Conexiones**, ábrelo, **Detalles** y luego **Desconectar**.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

No hay nada que desinstalar en ningún otro sitio.
