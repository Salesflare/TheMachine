---
title: Otro correo (IMAP)
area: connections
summary: Correo de cualquier proveedor con IMAP, como iCloud, Yahoo, Fastmail, Telenet o tu propio dominio.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
---
## Qué lee

Tu bandeja de entrada y tu carpeta Enviados: los últimos 7 días al conectar, y luego todo lo nuevo. El correo que envías también cuenta: así aprende cómo escribes y qué prometiste. Las demás carpetas no se leen.

No cambia nada en tu buzón, salvo una copia de lo que The Machine envía, en tu carpeta Enviados. El correo no se marca como leído.

## Qué puede hacer

Envía correo solo cuando pulsas Enviar, por el servidor de correo de tu proveedor (SMTP) con la misma contraseña. Una copia va a tu carpeta Enviados. Las respuestas siguen en su conversación, y tu firma es la de Ajustes o, si no, la que cierra tu correo enviado.

## Conéctalo

1. En el panel, abre **Conexiones**, luego **+ Añadir**, y elige **Otro correo**.
2. Escribe tu dirección de correo y tu contraseña.
3. Pulsa **Conectar**.

Muchos proveedores piden una contraseña de aplicación para programas de correo, no tu contraseña normal. Crea una en los ajustes de cuenta de tu proveedor:

- iCloud: una contraseña específica de app en account.apple.com.
- Yahoo: Seguridad de la cuenta, Generar contraseña de aplicación.
- Fastmail: Settings, Privacy and security, App passwords.
- Telenet: tu contraseña normal del correo de Telenet.
- Proton Mail: ejecuta Proton Mail Bridge en el mismo ordenador y usa la contraseña que muestra Bridge.

Los ajustes del servidor se rellenan para la mayoría de proveedores. ¿No encuentra el tuyo? Abre **Ajustes del servidor** y escribe lo que tu proveedor indica para programas de correo: los servidores IMAP y SMTP, sus puertos y su seguridad (SSL/TLS o STARTTLS). The Machine nunca se conecta sin TLS.

¿Gmail o correo de Microsoft, también en tu propio dominio? Elige **Gmail** u **Outlook**. Se conectan sin contraseña.

## Si se detiene

- **El servidor de correo rechazó la contraseña**: la cambiaste, o se eliminó la contraseña de aplicación. Vuelve a conectarlo con la nueva.
- **El servidor de correo rechazó la contraseña para enviar**: no se envió nada. Vuelve a conectarlo; si sigue rechazándola, revisa el servidor SMTP en Ajustes del servidor. Hasta entonces solo lee.
- **No se pudo llegar al servidor de correo**: lo vuelve a intentar sola. Si sigue fallando, revisa el nombre del servidor en Ajustes del servidor.

## Quítalo

**Conexiones**, abre la cuenta, **Detalles**, luego **Desconectar**. Deja de leer y lo que ya trajo se queda. Borra también la contraseña de aplicación en tu proveedor.
