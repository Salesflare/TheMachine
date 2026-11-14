---
title: Gmail
area: connections
summary: Lee tus correos y redacta respuestas con tu estilo. Solo envía un correo cuando lo apruebas.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: e06946aaa6ad0e1a
---
## Qué lee

Todo tu correo: los últimos 7 días al conectarlo y, a partir de ahí, todo lo nuevo, tanto lo que recibes como lo que envías. También cuenta el correo que envías, para que aprenda cómo escribes y qué prometiste.

Primero echa un vistazo rápido a los correos de Promociones, newsletters, Actualizaciones y Foros: remitente, asunto y unas pocas palabras, muchos a la vez. Cuando uno es importante, lo lee completo y puede convertirse en una tarea. No se salta nada sin revisarlo.

## Qué puede enviar

Un correo a partir de una tarea, y solo después de que lo apruebes. **Hazlo** prepara un borrador; **Revisar y enviar** lo abre para que lo edites, y no se envía nada hasta que pulses **Enviar ahora**. **Iniciar sesión con Google** también solicita a Google permiso para enviar. Si usas tu propia app en tu propio ordenador, el acceso solo permite leer hasta que configures tú el envío.

**De** en la revisión es un selector pequeño que aparece cuando Gmail permite que este buzón envíe como uno de tus alias (uno marcado como **Míos** en **Ajustes**, [Tus direcciones](settings.md#your-addresses)). Si respondes a un correo que llegó a ese alias, la respuesta se envía desde él. Los correos nuevos se envían desde la dirección de tu buzón. Justo antes de enviar, se vuelve a consultar a Gmail: si no confirma la dirección, no se envía nada.

Las respuestas van al hilo del correo al que responden. Si se envían desde otro de tus buzones distinto del que recibió el correo, la tarea lo indica antes de que lo envíes. La respuesta sigue apareciendo en el hilo de esa persona.

## Conéctalo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup.
2. En **Correo y Calendario**, pulsa **Conectar Google** e inicia sesión. En la pantalla de Google aparece Salesflare, la empresa que crea The Machine.
3. Gmail y Google Calendar se conectan a la vez.

¿Te registraste con Google y diste permiso para Gmail y Calendar en esa pantalla? Se conectan automáticamente. Solo se envía algo cuando pulsas Enviar.

También puedes hacerlo desde el panel: **Conexiones**, **Correo**, elige Gmail y pulsa **Iniciar sesión con Google**. Al terminar, volverás al panel.

En tu propio ordenador, una vez que esté [vinculada a tu cuenta](friends.md#a-machine-on-your-own-computer):

1. En el panel, abre **Conexiones**, luego **Correo** y elige Gmail.
2. Pulsa **Iniciar sesión con Google** e inicia sesión en la pestaña que se abre. Gmail y Google Calendar se conectan a la vez.

Si no está vinculada o usas tu propio cliente OAuth de Google, abre **Usar tu propia app** allí o ejecuta `assistant connect gmail`. Pulsa **Abrir Google**, inicia sesión y pega la dirección a la que te redirige Google. También se conecta Google Calendar para esa misma dirección.

Es posible que un administrador de Google Workspace tenga que permitir primero la app en la consola de administración.

## Elimínalo

- En una Machine alojada: pulsa **Desconectar** junto a la dirección en tu página de configuración. Se desconectan Gmail y Calendar para esa dirección, y tu Machine olvida el inicio de sesión. Las demás instancias de Machine conservan el suyo. En el panel, **Desconectar ↗** en **Conexiones** te lleva a esa página. Allí, **Reconectar** te permite volver a iniciar sesión sin salir del panel.
- En tu propio ordenador: abre **Conexiones**, selecciona Gmail, pulsa **Detalles** y luego **Desconectar**. La Machine deja de leer el correo. Lo que ya había importado se conserva. Si ningún otro servicio de la Machine usa ese inicio de sesión de Google, lo olvida. Las demás instancias de Machine conservan el suyo.

## Desinstálalo en Google

En tu cuenta de Google, abre Seguridad y luego Tus conexiones con aplicaciones y servicios de terceros. Quita Salesflare (Iniciar sesión con Google o alojada) o tu propia app.
