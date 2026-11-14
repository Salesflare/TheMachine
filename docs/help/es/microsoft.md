---
title: Microsoft Outlook y Calendario
area: connections
summary: Correo y reuniones de Outlook para Microsoft 365 y Outlook.com. Solo envía correos cuando los apruebas.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: c10bf70a327b8ec0
---
## Qué lee

- **Outlook**: todos tus correos de los últimos 7 días cuando lo conectas y, después, todos los nuevos.
- **Calendario de Outlook**: tus reuniones, solo lectura.

Primero, revisa por encima los correos de Otros y los boletines: quién los envía, el asunto y unas pocas palabras. Si alguno es importante, lo lee completo y puede convertirlo en una tarea.

## Qué puede enviar y cambiar

- Un correo a partir de una tarea, solo cuando lo apruebas. Se envía desde la dirección de correo de la cuenta, no desde un alias.
- Las respuestas aparecen en la conversación de Outlook del correo al que responden.
- Después de enviar una respuesta, los mensajes de la conversación se mueven a la carpeta **Pospuestos** de Outlook durante unos días (3, a menos que la tarea indique otra cosa). Luego vuelven a la bandeja de entrada, o antes si alguien responde. La revisión te lo indica antes de enviar.

El calendario nunca se modifica.

## Fotos de compañeros y contactos

También se le pide a Microsoft que lea los perfiles básicos de tu organización (nombre, correo y foto) y tus contactos de Outlook. Tu Machine solo los usa para mostrar fotos, cargos y empresas de personas que ya están en tu Graph, con un máximo de 200 fotos al día. Si alguien no tiene foto, se vuelve a comprobar después de 30 días.

Es posible que el administrador de tu organización tenga que aprobar las fotos de tus compañeros. Si no las aprueba, Outlook se conectará igualmente, pero sin estas fotos. Si conectaste una cuenta antes de esto, recibirás una tarea: pulsa **Reconectar** o **No hace falta** para cerrarla definitivamente. Las cuentas personales (Outlook.com, Hotmail) no tienen compañeros, así que la tarea solo te pedirá las fotos de tus contactos.

## Conectar

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup.
2. Pulsa **Conectar Microsoft** e inicia sesión.
3. Si Microsoft pide la aprobación de un administrador, envíale el enlace a tu administrador de Microsoft 365 (**Copiar enlace**). Cuando lo apruebe, todos los miembros de tu organización podrán conectarse. Si eres administrador, pulsa **Soy el administrador: aprobar ahora**.

También puedes hacerlo desde el panel: **Conexiones**, **Correo**, elige Outlook y pulsa **Iniciar sesión con Microsoft**. El enlace para el administrador aparece justo debajo del botón.

En tu propio ordenador, una vez que esté [vinculada a tu cuenta](friends.md#a-machine-on-your-own-computer), abre **Conexiones**, luego **Correo**, elige Outlook y pulsa **Iniciar sesión con Microsoft**. El correo y el calendario se conectan a la vez. Después de pasar por Microsoft, volverás a **Conexiones** en el panel.

Si el equipo de TI tiene su propia aplicación de Microsoft Entra: abre **Usar tu propia app** allí o ejecuta `assistant connect outlook`.

## Desconectarla

- En una Machine alojada: pulsa **Desconectar** junto a la cuenta en tu página de configuración. **Desconectar ↗** en Conexiones te lleva a esa página.
- En tu propio ordenador: abre **Conexiones**, selecciona la cuenta, pulsa **Detalles** y luego **Desconectar**.

## Desinstalarla en Microsoft

Microsoft no nos permite revocar un inicio de sesión, así que también debes eliminarlo allí:

- Cuenta profesional o educativa: myapps.microsoft.com
- Cuenta personal: account.live.com/consent/Manage
