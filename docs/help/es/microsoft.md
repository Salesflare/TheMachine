---
title: Microsoft Outlook y Calendario
area: connections
summary: Correo y reuniones de Outlook para Microsoft 365 y Outlook.com. Solo se envía un correo cuando das tu visto bueno.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 7229063d9365735d
---
## Qué lee

- **Outlook**: todo tu correo de los últimos 7 días cuando te conectas y, después, todo lo nuevo.
- **Calendario de Outlook**: tus reuniones, solo de lectura.

Primero echa un vistazo rápido a los correos de Otros y a los boletines: remitente, asunto y unas pocas palabras. Si alguno es importante, lo lee entero y puede convertirse en una tarea.

## Qué puede enviar y cambiar

- Un correo a partir de una tarea, solo cuando das tu visto bueno. Se envía desde la dirección propia del buzón, no desde un alias.
- La respuesta se añade a la conversación de Outlook del correo al que responde.
- Después de enviar una respuesta, los mensajes del hilo pasan a una carpeta Pospuestos de Outlook durante unos días (3, salvo que la tarea indique otra cosa) y vuelven entonces a la Bandeja de entrada, o antes si alguien responde. Nunca permanecen fuera de la Bandeja de entrada después de la fecha límite de la tarea. La revisión te lo indica antes de enviar.

El calendario nunca se modifica.

## Fotos de compañeros y contactos

También se pide a Microsoft que lea los perfiles básicos de tu organización (nombre, correo y foto) y tus contactos de Outlook. Tu Machine solo los usa para mostrar fotos, cargos y empresas de personas que ya están en tu Graph, con un máximo de 200 fotos al día. Si alguien no tiene foto, se vuelve a comprobar al cabo de 30 días.

Es posible que el administrador de tu organización tenga que aprobar las fotos de los compañeros. Si no lo hace, Outlook se conecta igualmente, pero sin esas fotos. Si conectaste la cuenta antes de esto, aparecerá una tarea: pulsa **Reconectar** o **No hace falta** para cerrarla definitivamente. Una cuenta personal (Outlook.com, Hotmail) no tiene compañeros, así que la tarea solo te pide las fotos de tus contactos.

## Conectarlo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup.
2. Pulsa **Conectar Microsoft** e inicia sesión.
3. Si Microsoft pide la aprobación de un administrador, envíale el enlace (**Copiar enlace**) a tu administrador de Microsoft 365. Cuando lo apruebe, todos los miembros de tu organización podrán conectarse. Si eres el administrador, pulsa **Soy el administrador: aprobar ahora**.

También puedes hacerlo desde el panel: **Conexiones**, **Correo**, elige Outlook y pulsa **Iniciar sesión con Microsoft**. El enlace para el administrador está justo debajo del botón.

En tu propio ordenador, una vez que esté [vinculada a tu cuenta](friends.md#a-machine-on-your-own-computer): abre **Conexiones**, luego **Correo**, elige Outlook y pulsa **Iniciar sesión con Microsoft**. El correo y el calendario se conectan juntos. Después de pasar por Microsoft, volverás a **Conexiones** en tu panel.

Si tu equipo de TI usa su propia aplicación de Microsoft Entra: abre **Usar tu propia app** allí o ejecuta `assistant connect outlook`.

## Desconectarlo

- En una Machine alojada: pulsa **Desconectar** junto a la cuenta en tu página de configuración. **Desconectar ↗** en Conexiones te lleva allí.
- En tu propio ordenador: abre **Conexiones**, selecciona la cuenta y pulsa **Detalles** y luego **Desconectar**.

## Desinstalarlo en Microsoft

Microsoft no nos permite revocar el inicio de sesión, así que también debes quitarlo desde allí:

- Cuenta profesional o educativa: myapps.microsoft.com
- Cuenta personal: account.live.com/consent/Manage
