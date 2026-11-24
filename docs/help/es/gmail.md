---
title: Gmail
area: connections
summary: Lee tu correo y redacta respuestas con tu estilo. Solo envía correos cuando los apruebas.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: f0565a7bf839f49f
---
## Qué lee

Todo tu correo: los últimos 7 días cuando lo conectas y, a partir de entonces, todo lo nuevo que envías y recibes. También cuenta el correo que envías, así aprende cómo escribes y qué prometiste.

Primero echa un vistazo rápido a los correos de promociones, boletines, Actualizaciones y Foros: quién los envía, el asunto y unas pocas palabras, a muchos a la vez. Si alguno importa, lo lee entero y puede convertirse en una tarea. No se omite ningún correo sin echarle un vistazo.

## Qué puede enviar

Correos a partir de una tarea, y solo cuando los apruebas. **Hazlo** prepara un borrador; **Revisar y enviar** lo abre listo para editar, y no se envía nada hasta que pulses **Enviar ahora**. **Iniciar sesión con Google** también solicita permiso a Google para enviar. Si usas tu propia app en tu propio ordenador, el inicio de sesión es de solo lectura hasta que configures tú el envío.

**De** en la revisión es un selector pequeño cuando Gmail permite enviar desde este buzón como un alias tuyo, uno marcado como **Míos** en **Ajustes**, [Tus direcciones](settings.md#your-addresses). Si respondes a un correo que llegó a ese alias, la respuesta sale desde él; los correos nuevos salen desde la dirección de tu buzón. Justo antes de enviar, se vuelve a preguntar a Gmail: si no confirma la dirección, no se envía nada.

La respuesta se añade al hilo del correo al que responde. Si se envía desde otro de tus buzones distinto del que recibió ese correo, la tarea te lo indica antes de enviarla. Aun así, la respuesta aparece en su hilo.

Cuando se envía una respuesta, su hilo sale de tu bandeja de entrada unos días con la etiqueta Pospuesto (3 días, salvo que la tarea indique otra cosa) y vuelve entonces, o antes si alguien responde. Nunca permanece fuera después de la fecha límite de la tarea: vuelve el día laborable anterior, y si vence hoy, se queda en tu bandeja de entrada. La revisión te lo indica antes de enviar. Esa es tu bandeja de entrada: si una respuesta solo promete hacer el trabajo, la tarea sigue abierta.

## Conectar Gmail

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup.
2. En **Correo y calendario**, pulsa **Conectar Google** e inicia sesión. En la pantalla de Google aparece Salesflare, la empresa que crea The Machine.
3. Gmail y Google Calendar se conectan a la vez.

Si te registraste con Google y diste permiso para Gmail y Calendar en esa pantalla, se conectan automáticamente. Solo se envía correo cuando pulsas Enviar.

También puedes hacerlo desde el panel: **Conexiones**, **Correo**, elige Gmail y pulsa **Iniciar sesión con Google**. Al terminar, volverás al panel.

En tu propio ordenador, una vez que esté [vinculada a tu cuenta](friends.md#a-machine-on-your-own-computer):

1. En el panel, abre **Conexiones**, luego **Correo** y elige Gmail.
2. Pulsa **Iniciar sesión con Google** e inicia sesión en la pestaña que se abre. Gmail y Google Calendar se conectan a la vez.

Si no está vinculada, o si usas tu propio cliente OAuth de Google, abre **Usar tu propia app** allí o ejecuta `assistant connect gmail`. Pulsa **Abrir Google**, inicia sesión y pega la dirección a la que te lleva Google. También se conecta Google Calendar con esa misma dirección.

Es posible que un administrador de Google Workspace tenga que permitir primero la app en la consola de administración.

## Desconectar Gmail

- En una Machine alojada: pulsa **Desconectar** junto a la dirección en tu página de configuración. Se desconectan Gmail y Calendar para esa dirección, y tu Machine olvida el inicio de sesión. Tus otras Machines conservan el suyo. En el panel, **Desconectar ↗** en Conexiones te lleva a esa página. Allí, **Reconectar** permite iniciar sesión de nuevo sin salir del panel.
- En tu propio ordenador: abre **Conexiones**, elige Gmail, pulsa **Detalles** y luego **Desconectar**. Dejará de leer el correo. Lo que ya haya importado se conserva. Cuando ningún otro servicio lo use, olvidará ese inicio de sesión de Google. Tus otras Machines conservan el suyo.

## Desinstalarla de Google

En tu cuenta de Google, abre Seguridad y luego Tus conexiones con aplicaciones y servicios de terceros. Quita Salesflare (Iniciar sesión con Google o alojada) o tu propia app.
