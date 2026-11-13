---
title: iCloud y otros calendarios (CalDAV)
area: connections
summary: Reuniones del Calendario de iCloud o de cualquier calendario CalDAV, como Fastmail, Nextcloud o Zoho. Solo lectura.
covers: connector:icloud_calendar, connector:caldav
code: caldav_calendar.py, ical.py, machine/sources/calendar_setup.py
order: 14
---
## Qué lee

Tus reuniones, con sus invitados, salas y notas: la semana pasada y el mes siguiente al conectar, y luego cada cambio. Aparecen en Calendario y en la preparación de reuniones, como las reuniones de Google u Outlook. Se lee cada calendario de la cuenta, o solo el que indiques.

Es de solo lectura: nunca añade, mueve ni quita una reunión.

## Conecta el Calendario de iCloud

1. Crea una contraseña específica de app en [appleid.apple.com](https://appleid.apple.com), en **Inicio de sesión y seguridad**. También sirve la que creaste para iCloud Mail.
2. En el panel, abre **Conexiones**, luego **Calendario**, y elige **Calendario de iCloud**.
3. Escribe tu Apple ID y la contraseña específica de app, y pulsa **Conectar**.

## Conecta otro calendario

1. Abre **Conexiones**, luego **Calendario**, y elige **Otro calendario**.
2. Escribe tu dirección de correo y tu contraseña. Muchos proveedores piden aquí una contraseña de aplicación, que creas en los ajustes de tu cuenta.
3. Pulsa **Conectar**.

El servidor se encuentra para Fastmail, Yahoo, Zoho y los servidores que lo anuncian. ¿No se encuentra el tuyo? Abre **Ajustes del servidor** y escribe su dirección CalDAV, como `nextcloud.example.com/remote.php/dav`. **Solo este calendario** lee un único calendario por su nombre.

¿Calendarios de Google o Microsoft? Elige mejor **Google Calendar** o **Calendario de Outlook**.

## Si se detiene

- **El servidor de calendario rechazó la contraseña**: la cambiaste, o se quitó la contraseña de aplicación. Vuelve a conectarlo con una nueva.
- **No se pudo llegar al servidor de calendario**: lo reintenta solo. Si sigue fallando, revisa la dirección en Ajustes del servidor.

## Quítalo

**Conexiones**, abre el calendario, **Detalles**, luego **Desconectar**. Lo que ya trajo se queda. Quita también la contraseña de aplicación en tu proveedor.
