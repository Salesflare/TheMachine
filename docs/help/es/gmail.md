---
title: Gmail
area: connections
summary: Lee tus correos y redacta respuestas con tu estilo. Solo envía un correo cuando lo apruebas.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: c1f2362cd496840e
---
## Qué lee

Todos tus correos: los de los últimos 7 días cuando la conectas y, a partir de entonces, todos los nuevos que recibas y envíes. También cuenta los correos que envías, para aprender cómo escribes y qué prometiste.

Primero echa un vistazo rápido a los correos de Promociones, boletines, Notificaciones y Foros: quién los envía, el asunto y unas pocas palabras, muchos a la vez. Si alguno es importante, lo lee entero y puede convertirlo en una tarea. No se salta nada sin revisarlo.

## Qué puede enviar

Puede enviar un correo a partir de una tarea, y solo cuando lo apruebas. **Hazlo** prepara un borrador; **Revisar y enviar** lo abre listo para editar, y no se envía nada hasta que pulses **Enviar ahora**. **Iniciar sesión con Google** también le pide a Google permiso para enviar. Si usas tu propia app en tu propio ordenador, el inicio de sesión solo permite leer, hasta que configures tú el envío.

**De** en la revisión es un selector pequeño que aparece cuando Gmail permite que este buzón envíe como un alias tuyo (uno marcado como **Míos** en Ajustes, [Tus direcciones](settings.md#your-addresses)). Una respuesta a un correo recibido en ese alias se envía desde esa dirección; los correos nuevos se envían desde la dirección de tu buzón. Justo antes de enviar, se vuelve a consultar a Gmail: si no confirma la dirección, no se envía nada.

Las respuestas se añaden al hilo del correo al que responden. Si se envían desde otro de tus buzones y no desde el que recibió ese correo, la tarea te lo indica antes de que la envíes. La respuesta se añade igualmente a ese hilo.

Cuando se envía una respuesta, su hilo sale de la bandeja de entrada y queda bajo la etiqueta Pospuestos durante unos días (3, a menos que la tarea indique otra cosa). Después vuelve a la bandeja, o antes si alguien responde. La revisión te lo indica antes de que envíes la respuesta.

## Conectarla

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup.
2. En **Correo y Calendario**, pulsa **Conectar Google** e inicia sesión. En la pantalla de Google aparece Salesflare, la empresa que creó The Machine.
3. Gmail y Google Calendar se conectan a la vez.

¿Te registraste con Google y diste permiso para Gmail y Calendar en esa pantalla? Se conectan automáticamente. Solo se envía cuando pulsas **Enviar**.

También puedes hacerlo desde el panel: **Conexiones**, **Correo**, elige Gmail y pulsa **Iniciar sesión con Google**. Cuando termines, volverás al panel.

En tu propio ordenador, una vez que esté [vinculada a tu cuenta](friends.md#a-machine-on-your-own-computer):

1. En el panel, abre **Conexiones**, luego **Correo** y elige Gmail.
2. Pulsa **Iniciar sesión con Google** e inicia sesión en la pestaña que se abre. Gmail y Google Calendar se conectan a la vez.

Si no está vinculada, o usas tu propio cliente OAuth de Google, abre **Usar tu propia app** ahí o ejecuta `assistant connect gmail`. Pulsa **Abrir Google**, inicia sesión y pega la dirección a la que te redirige Google. También se conecta Google Calendar con esa misma dirección.

Es posible que un administrador de Google Workspace tenga que permitir primero la app en la consola de administración.

## Desconectarla

- En una Machine alojada: pulsa **Desconectar** junto a la dirección en tu página de configuración. Se desconectan Gmail y Calendar para esa dirección y tu Machine olvida el inicio de sesión. Tus otras Machines conservan el suyo. En el panel, **Desconectar ↗** en Conexiones te lleva a esa página. Allí, **Reconectar** te permite volver a iniciar sesión sin salir del panel.
- En tu propio ordenador: abre **Conexiones**, selecciona Gmail, pulsa **Detalles** y luego **Desconectar**. Deja de leer tus correos. Lo que ya había importado se conserva. Si nada más en ella usa ese inicio de sesión de Google, lo olvida. Tus otras Machines conservan el suyo.

## Desinstalarla en Google

En tu cuenta de Google, abre Seguridad y luego Tus conexiones con aplicaciones y servicios de terceros. Elimina Salesflare (Iniciar sesión con Google o alojada) o tu propia app.
