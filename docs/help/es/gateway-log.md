---
title: Salud de tu Machine
area: connections
summary: El propio registro de tu Machine, para que detecte sus propios problemas. Solo lee.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
---
## Qué lee

El propio registro de tu Machine: ejecuciones fallidas, traspasos rechazados, mensajes de Telegram que no salieron y los propios errores de The Machine. Una tarea te avisa cuando hay algo que arreglar.

## Correcciones que una actualización dejó a un lado

Cuando The Machine se actualiza y una de sus propias correcciones ya no encaja con la nueva versión, la actualización deja esa corrección a un lado y sigue, para que tu Machine nunca se quede en una versión antigua. Una tarea, **Rehacer una corrección que la actualización dejó a un lado**, nombra la corrección.

Con **Rehacer**, tu Machine la rehace en la nueva versión, como cualquier corrección suya: ves el cambio y tocas **Merge fix**. Una vez fusionada, la copia antigua se descarta. O cierra la tarea.

## Tus propios archivos que una actualización conservó

Cuando una nueva versión trae un archivo con el mismo nombre que uno que añadiste tú, la actualización renombra el tuyo en vez de sobrescribirlo y sigue. Una tarea dice cuántos conservó e indica cada nombre antiguo y nuevo. Ciérrala cuando los hayas revisado.

## Qué puede hacer

Nada. Solo lee el registro en tu propia Machine.

## Conéctalo

- En una Machine alojada está en tu página de configuración, en **Más fuentes**, como Salud de tu Machine. Uno por Machine.
- En tu propio ordenador: ejecuta `assistant connect gateway`.

## Quítalo

- En el panel: **Conexiones**, ábrelo, **Detalles** y luego **Desconectar**.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

No hay nada que desinstalar en ningún otro sitio.
