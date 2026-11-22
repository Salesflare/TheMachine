---
title: Gmail
area: connections
summary: Lee tu correo y redacta respuestas con tu estilo. Solo envía un correo cuando lo apruebas.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## Qué lee

Todo tu correo: los últimos 7 días al conectarla y, a partir de entonces, todo lo nuevo, tanto lo que recibes como lo que envías. El correo que envías también cuenta, así aprende cómo escribes y qué prometiste.

Primero echa un vistazo rápido a los correos de Promociones, boletines, Actualizaciones y Foros: quién los envía, el asunto y unas pocas palabras, muchos a la vez. Si alguno es importante, lo lee entero y puede convertirlo en una tarea. No se pasa por alto nada sin revisarlo.

## Qué puede enviar

Un correo a partir de una tarea, y solo cuando lo apruebas. **Hazlo** prepara un borrador; **Revisar y enviar** lo abre listo para editar, y no se envía nada hasta que pulses **Enviar ahora**. **Iniciar sesión con Google** también pide permiso a Google para enviar. Si usas tu propia app en tu propio ordenador, el inicio de sesión solo permite leer, hasta que añadas tú la opción de enviar.

**De** en la revisión es un pequeño selector que aparece cuando Gmail permite enviar desde esta cuenta como un alias tuyo (uno marcado como **Míos** en Ajustes, [Tus direcciones](settings.md#your-addresses)). Si respondes a un correo que llegó a ese alias, la respuesta se envía desde allí; los correos nuevos se envían desde la dirección de tu cuenta. Justo antes de enviar, se vuelve a preguntar a Gmail: si no confirma la dirección, no se envía nada.

La respuesta se añade al hilo del correo al que responde. Si se envía desde otra de tus cuentas de correo, distinta de aquella a la que llegó el correo, la tarea te lo indica antes de que la envíes. La respuesta seguirá en el hilo de la otra persona.

Cuando se envía una respuesta, el hilo desaparece de la bandeja de entrada y queda bajo la etiqueta Pospuesto durante unos días (3, salvo que la tarea indique otra cosa). Después vuelve, o antes si alguien responde. La revisión te lo indica antes de que envíes. Así funciona tu cuenta: si una respuesta solo promete que harás el trabajo, la tarea sigue abierta.

## Conectarla

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup.
2. En **Correo y Calendario**, pulsa **Conectar Google** e inicia sesión. En la pantalla de Google aparece Salesflare, la empresa que crea The Machine.
3. Gmail y Google Calendar se conectan a la vez.

¿Te registraste con Google y diste permiso a Gmail y Calendar en esa pantalla? Se conectan automáticamente. Solo se envía correo cuando pulsas Enviar.

También puedes hacerlo desde el panel: **Conexiones**, **Correo**, elige Gmail y pulsa **Iniciar sesión con Google**. Cuando termines, volverás al panel.

En tu propio ordenador, una vez que lo hayas [vinculado a tu cuenta](friends.md#a-machine-on-your-own-computer):

1. En el panel, abre **Conexiones** y luego **Correo**, y elige Gmail.
2. Pulsa **Iniciar sesión con Google** e inicia sesión en la pestaña que se abre. Gmail y Google Calendar se conectan a la vez.

Si no está vinculado, o usas tu propio cliente OAuth de Google, abre **Usar tu propia app** allí o ejecuta `assistant connect gmail`. Pulsa **Abrir Google**, inicia sesión y pega la dirección a la que te envía Google. También se conecta Google Calendar para esa misma dirección.

Es posible que un administrador de Google Workspace tenga que permitir primero la app desde la consola de administración.

## Desconectarla

- En una Machine alojada: pulsa **Desconectar** junto a la dirección en tu página de configuración. Se desconectan Gmail y Calendar para esa dirección y tu Machine olvida el inicio de sesión. Tus otras Machine conservan el suyo. En el panel, **Desconectar ↗** en Conexiones te lleva a esa página. **Reconectar** allí te permite volver a iniciar sesión sin salir del panel.
- En tu propio ordenador: abre **Conexiones**, Gmail y **Detalles**; luego pulsa **Desconectar**. Dejará de leer el correo. Lo que ya haya importado se conserva. Si ningún otro servicio usa ese inicio de sesión de Google, lo olvida. Tus otras Machine conservan el suyo.

## Desinstalarla de Google

En tu cuenta de Google, abre Seguridad y luego Tus conexiones con aplicaciones y servicios de terceros. Quita Salesflare (Iniciar sesión con Google o alojamiento) o tu propia app.
