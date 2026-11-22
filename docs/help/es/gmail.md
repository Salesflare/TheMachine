---
title: Gmail
area: connections
summary: Lee tu correo y prepara respuestas con tu estilo. Solo envía correos cuando los apruebas.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## Qué lee

Todo tu correo: los últimos 7 días cuando conectas la cuenta y, después, todos los mensajes nuevos que recibas y envíes. También cuenta el correo que envías, así aprende cómo escribes y qué prometiste.

Primero echa un vistazo rápido a los mensajes de Promociones, boletines, Actualizaciones y Foros: remitente, asunto y unas pocas palabras, muchos a la vez. Si uno es importante, lo lee entero y puede convertirlo en una tarea. No se salta nada sin verlo.

## Qué puede enviar

Un correo a partir de una tarea, y solo después de que lo apruebes. **Hazlo** prepara un borrador; **Revisar y enviar** lo abre listo para editar, y no se envía nada hasta que pulses **Enviar ahora**. **Iniciar sesión con Google** también solicita permiso a Google para enviar. Si usas tu propia app en tu propio ordenador, el inicio de sesión es de solo lectura hasta que configures tú el envío.

**De** en la revisión es un pequeño selector que aparece cuando Gmail permite que este buzón envíe como uno de tus alias, uno marcado como **Míos** en **Ajustes**, [Tus direcciones](settings.md#your-addresses). Si respondes a un correo que llegó a ese alias, la respuesta se envía desde ahí; los correos nuevos se envían desde la dirección de tu buzón. Justo antes de enviar, se vuelve a consultar a Gmail: si no confirma la dirección, no se envía nada.

La respuesta se añade al hilo del correo al que responde. Si se envía desde uno de tus otros buzones, en lugar del buzón al que llegó el correo, la tarea te lo indica antes de enviarla. Aun así, se añade a ese hilo.

Después de enviar una respuesta, el hilo sale de la bandeja de entrada y queda unos días bajo la etiqueta Pospuesto (3, salvo que la tarea indique otro plazo). Entonces vuelve a aparecer, o antes si alguien responde. La revisión te lo indica antes de enviar. Así funciona tu buzón: si una respuesta solo promete hacer el trabajo, la tarea sigue abierta.

## Conéctalo

En una Machine alojada:

1. Abre la página de configuración en app.themachine.computer/setup.
2. En **Correo y Calendario**, pulsa **Conectar Google** e inicia sesión. En la pantalla de Google aparece Salesflare, la empresa que crea The Machine.
3. Gmail y Google Calendar se conectan a la vez.

¿Te registraste con Google y diste permiso para usar Gmail y Calendar en esa pantalla? Se conectan automáticamente. Solo se envía correo cuando pulsas Enviar.

También puedes hacerlo desde el panel: **Conexiones**, **Correo**, elige Gmail y pulsa **Iniciar sesión con Google**. Al terminar, volverás al panel.

En tu propio ordenador, una vez que esté [vinculado a tu cuenta](friends.md#a-machine-on-your-own-computer):

1. En el panel, abre **Conexiones** y luego **Correo**, y elige Gmail.
2. Pulsa **Iniciar sesión con Google** e inicia sesión en la pestaña que se abre. Gmail y Google Calendar se conectan a la vez.

Si no está vinculado o usas tu propio cliente OAuth de Google, abre **Usar tu propia app** allí o ejecuta `assistant connect gmail`. Pulsa **Abrir Google**, inicia sesión y pega la dirección a la que te envía Google. También se conecta Google Calendar para esa misma dirección.

Es posible que el administrador de Google Workspace tenga que permitir primero la app desde la consola de administración.

## Desconéctalo

- En una Machine alojada: pulsa **Desconectar** junto a la dirección en la página de configuración. Se desconectan Gmail y Calendar para esa dirección y tu Machine olvida el inicio de sesión. Las demás Machines lo conservan. En el panel, **Desconectar ↗** en Conexiones te lleva a esa página. **Reconectar** te permite volver a iniciar sesión desde allí sin salir del panel.
- En tu propio ordenador: abre **Conexiones**, selecciona Gmail y pulsa **Detalles** y luego **Desconectar**. Dejará de leer el correo. Lo que ya haya importado se queda. Si ningún otro servicio usa ese inicio de sesión de Google, lo olvida. Las demás Machines lo conservan.

## Desinstálalo en Google

En tu cuenta de Google, abre Seguridad y luego Tus conexiones con aplicaciones y servicios de terceros. Quita Salesflare (Iniciar sesión con Google o alojamiento) o tu propia app.
