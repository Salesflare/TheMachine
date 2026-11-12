---
title: Proton Calendar y enlaces de calendario (ICS)
area: connections
summary: Reuniones del enlace para compartir de un calendario: Proton Calendar, calendarios publicados, escolares o deportivos. Solo lectura.
covers: connector:proton_calendar, connector:ics
code: ics_feed.py, ical.py, machine/sources/calendar_setup.py
order: 15
---
## Qué lee

Los eventos del calendario detrás del enlace, con eventos periódicos y zonas horarias: la semana pasada y el mes siguiente, y luego cada cambio. Aparecen en Calendario y en la preparación de reuniones.

Un enlace solo se puede leer, así que nunca cambia una reunión. Revisa el enlace como mucho cada 15 minutos. Proton dice que los cambios pueden tardar unas horas en llegar a un enlace.

## Conecta Proton Calendar

Proton Calendar no tiene otro acceso para apps, así que usa un enlace para compartir.

1. Abre Proton Calendar en la web, en calendar.proton.me. En sus apps del móvil no se pueden crear enlaces para compartir.
2. Ve a "Ajustes", "Todos los ajustes", "Calendarios", y elige el calendario.
3. En "Share with anyone", pulsa "Create link" y elige "Full view". Limited view solo muestra cuándo estás ocupado.
4. Pulsa "Copy link".
5. En el panel, abre **Conexiones**, luego **+ Añadir**, elige **Proton Calendar**, pega el enlace y pulsa **Conectar**.

## Conecta cualquier otro enlace de calendario

Elige **Enlace de calendario (ICS)** y pega el enlace: una dirección https o webcal que termina en .ics, como un calendario público de iCloud, un calendario publicado de Outlook o el calendario escolar de tu hijo.

## Mantén el enlace privado

Cualquiera con el enlace puede leer el calendario. The Machine lo guarda como una contraseña: nunca en un registro ni en pantalla. Para pararlo, borra el enlace donde lo creaste y pulsa aquí **Desconectar**.

## Si se detiene

- **El enlace del calendario dejó de funcionar**: el enlace se borró o cambió. Crea uno nuevo y vuelve a conectarlo.
- **No se pudo llegar al servidor de calendario**: lo reintenta solo.
