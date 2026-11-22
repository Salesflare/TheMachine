---
title: Otro correo (IMAP)
area: connections
summary: Correo de cualquier proveedor con IMAP, como iCloud, Yahoo, Fastmail, Telenet o tu propio dominio.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
translated: a21e9d52d723f351
---
## Qué lee

Tu bandeja de entrada y la carpeta Enviados: los últimos 7 días al conectarlo y, a partir de ahí, todo lo nuevo. El correo que envías también cuenta, así aprende cómo escribes y qué prometiste. No lee las demás carpetas.

No se cambia nada en tu buzón, salvo que se guarda una copia de lo que envía The Machine en la carpeta Enviados. El correo no se marca como leído.

## Qué puede hacer

Solo envía correos cuando pulsas **Enviar**, a través del servidor de correo de tu proveedor (SMTP) y con la misma contraseña. Guarda una copia en la carpeta Enviados. Las respuestas conservan el hilo, y tu firma es la de Ajustes o, si no tienes una, la que aparece al final de los correos que envías.

## Conéctalo

1. En el panel, abre **Conexiones**, luego **Correo** y elige **Otro correo**.
2. Escribe tu dirección de correo y tu contraseña.
3. Pulsa **Conectar**.

Muchos proveedores requieren una contraseña de aplicación para usar con apps de correo, no tu contraseña habitual. Crea una en los ajustes de tu cuenta:

- iCloud: una contraseña específica para apps en account.apple.com.
- Yahoo: Seguridad de la cuenta, Generar contraseña de aplicación.
- Fastmail: Ajustes, Privacidad y seguridad, Contraseñas de aplicación.
- Telenet: tu contraseña habitual de correo de Telenet.
- Zoho Mail con la autenticación de dos factores: una contraseña específica para aplicaciones en tu cuenta de Zoho, en Seguridad.
- Proton Mail: ejecuta Proton Mail Bridge en el mismo ordenador y usa la contraseña que muestra Bridge. Solo funciona con The Machine en ese mismo ordenador. The Machine muestra la huella digital del certificado de Bridge y solo confía en ese certificado.

Los ajustes del servidor se rellenan solos para la mayoría de proveedores. ¿No encuentra el tuyo? Abre **Ajustes del servidor** y escribe los datos que proporciona para apps de correo: los servidores IMAP y SMTP, sus puertos y el tipo de seguridad (SSL/TLS o STARTTLS). The Machine nunca se conecta sin TLS.

¿Usas Gmail o correo de Microsoft, también con tu propio dominio? Elige **Gmail** o **Outlook**. Se conectan sin contraseña. Si escribes sus servidores en Ajustes del servidor, también te lleva ahí: Microsoft ya no acepta contraseñas de apps de correo.

¿Escribiste una dirección de Microsoft 365? El formulario lo detecta y muestra **Iniciar sesión con Microsoft** en lugar del campo de contraseña. Se abre el inicio de sesión de Outlook. Si no la detecta en unos segundos, el formulario de contraseña seguirá disponible.

## Si deja de funcionar

- **El servidor de correo rechazó la contraseña**: la cambiaste o se eliminó la contraseña de aplicación. Vuelve a conectar la cuenta con la nueva contraseña.
- **El servidor de correo rechazó la contraseña para enviar**: no se envió nada. Vuelve a conectar la cuenta; si sigue rechazándola, revisa el servidor SMTP en Ajustes del servidor. Mientras tanto, solo leerá el correo.
- **No se pudo llegar al servidor de correo**: lo intentará de nuevo automáticamente. Si sigue sin funcionar, revisa el nombre del servidor en Ajustes del servidor.
- **El certificado del servidor de correo es para** otro nombre: los servicios de alojamiento compartido suelen responder con el nombre de su propio servidor. Escribe el nombre que aparece en Ajustes del servidor. The Machine nunca omite la comprobación del certificado.

## Desconéctalo

Abre **Conexiones**, selecciona la cuenta y pulsa **Detalles** y luego **Desconectar**. Dejará de leer el correo y conservará lo que ya había importado. Elimina también la contraseña de aplicación en el sitio de tu proveedor.
