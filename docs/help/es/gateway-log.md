---
title: Estado de salud de Machine
area: connections
summary: El registro propio de tu Machine, para que detecte sus propios problemas. Solo lo lee.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 3a06400a28396465
---
## Qué lee

El registro propio de tu Machine: ejecuciones fallidas, traspasos rechazados, mensajes de Telegram que no se enviaron y errores de The Machine. Una tarea te avisa cuando hay que arreglar algo. En tu propia computadora, eso incluye **Termina de instalar la última actualización**: una parte de una actualización necesita un breve reinicio por la noche y hubo varias noches en las que no se pudo hacer. Pregúntale en su chat y The Machine lo termina. La tarea se cierra sola cuando esa parte está instalada.

## Rehace las correcciones que dejó a un lado una actualización

Cuando The Machine se actualiza y una de sus propias correcciones ya no encaja con la nueva versión, la actualización la deja a un lado y continúa, para que tu Machine nunca se quede en una versión antigua. Una tarea, **Rehacer una corrección que la actualización dejó a un lado**, indica cuál es la corrección.

Con **Rehacer**, tu Machine vuelve a crearla para la nueva versión, como con cualquier corrección propia: ves el cambio y tocas **Fusionar corrección**. Una vez fusionada, se descarta la copia antigua. También puedes cerrar la tarea.

## Tus archivos propios que conservó una actualización

Cuando una nueva versión incluye un archivo con el mismo nombre que uno que añadiste, la actualización cambia el nombre del tuyo en lugar de sobrescribirlo y continúa. Una tarea indica cuántos archivos conservó y muestra cada nombre antiguo y nuevo. Ciérrala cuando los hayas revisado.

## Qué puede hacer

Nada. Solo lee el registro de tu propia Machine.

## Conectarla

- En una Machine alojada, está en la página de configuración, en **Más fuentes**, con el nombre Machine health. Una por Machine.
- En tu propia computadora: ejecuta `assistant connect gateway`.

## Quitarla

- En el panel: **Conexiones**, ábrela, toca **Detalles** y luego **Desconectar**.
- En una Machine alojada, también puedes tocar **Quitar** junto a ella en la página de configuración.

No hay que desinstalar nada en ningún otro sitio.
