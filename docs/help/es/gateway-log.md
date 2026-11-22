---
title: Salud de tu Machine
area: connections
summary: El registro de tu propia Machine, para que detecte sus propios problemas. Solo lo lee.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 7d66ff6a6a5d5b1d
---
## Qué lee

El registro de tu propia Machine: ejecuciones fallidas, traspasos rechazados, mensajes de Telegram que no se enviaron y errores de The Machine. Una tarea te avisa cuando hay algo que corregir. En tu propio ordenador, eso incluye **Termina de instalar la última actualización**: una parte de una actualización necesita un reinicio breve por la noche, y hubo varias noches en las que no se pudo hacer. Pídeselo en su chat y The Machine terminará de instalarla. La tarea se cierra sola cuando esa parte está instalada.

## Correcciones que una actualización dejó a un lado

Cuando The Machine se actualiza y una de sus propias correcciones deja de ser compatible con la nueva versión, la actualización la deja a un lado y continúa, para que tu Machine nunca se quede con una versión antigua. Una tarea, **Rehacer una corrección que la actualización dejó a un lado**, indica cuál es la corrección.

Con **Rehacer**, tu Machine vuelve a crearla para la nueva versión, como cualquier corrección propia: ves el cambio y pulsas **Fusionar**. Una vez fusionada, se elimina la copia antigua. También puedes cerrar la tarea.

## Tus archivos que una actualización conservó

Cuando una nueva versión incluye un archivo con el mismo nombre que uno que añadiste, la actualización cambia el nombre del tuyo en lugar de sobrescribirlo y continúa. Una tarea indica cuántos conservó y muestra cada nombre antiguo y nuevo. Ciérrala cuando los hayas comprobado.

## Qué puede hacer

Nada. Solo lee el registro de tu propia Machine.

## Conectarla

- En una Machine alojada, aparece en la página de configuración, en **Más fuentes**, como Salud de tu Machine. Hay una por Machine.
- En tu propio ordenador: **Conexiones**, **Otras**, Salud de tu Machine. O ejecuta `assistant connect gateway`.

## Quitarla

- En el panel: **Conexiones**, ábrela y pulsa **Detalles** y luego **Desconectar**.
- En una Machine alojada, también puedes pulsar **Quitar** junto a ella en la página de configuración.

No hay que desinstalar nada en ningún otro lugar.
