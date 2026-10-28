---
title: Gmail
area: connections
summary: Lee tu correo y redacta respuestas con tu estilo. Solo envía un correo después de que lo apruebes.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
---
## Qué lee

Todo tu correo: los últimos 7 días al conectar y luego todo lo nuevo, recibido y enviado. El correo que envías también cuenta, así aprende cómo escribes y qué prometiste.

El correo de Promociones, los boletines, Notificaciones y Foros reciben primero un vistazo rápido: remitente, asunto y unas palabras, muchos a la vez. Cuando uno importa, se lee entero y puede convertirse en una tarea. No se salta nada sin verlo.

## Qué puede enviar

Un correo desde una tarea, y solo después de que lo apruebes. **Hazlo** prepara un borrador; **Revisar y enviar** lo abre listo para editar, y no sale nada hasta que pulses **Enviar ahora**. **Iniciar sesión con Google** también pide a Google permiso para enviar. Con tu propia app en tu propio ordenador, el inicio de sesión es de solo lectura hasta que añadas tú el envío.

## Conéctalo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup.
2. En **Correo y calendario**, pulsa **Conectar Google** e inicia sesión. La pantalla de Google nombra a Salesflare, que hace The Machine.
3. Gmail y Google Calendar se conectan juntos.

O en el panel: **Conexiones**, **+ Añadir**, elige Gmail y pulsa **Iniciar sesión con Google**. Cuando termines, vuelves al panel.

En tu propio ordenador, una vez [vinculado con tu cuenta](fleet.md):

1. En el panel, abre **Conexiones**, luego **+ Añadir**, y elige Gmail.
2. Pulsa **Iniciar sesión con Google** e inicia sesión en la pestaña que se abre. Gmail y Google Calendar se conectan juntos.

Sin vincular, o con tu propio cliente OAuth de Google: abre ahí **Usar tu propia app**, o ejecuta `assistant connect gmail`. Usa gog. Abre la dirección que muestra e inicia sesión.

Puede que un administrador de Google Workspace tenga que permitir antes la app, en la Consola de administración.

## Quítalo

- En una Machine alojada: pulsa **Desconectar** junto a la dirección en tu página de configuración. Eso quita Gmail y Calendar para esa dirección y revoca el inicio de sesión en Google. En el panel, **Desconectar ↗** en Conexiones te lleva ahí. **Reconectar** ahí vuelve a iniciar sesión sin salir del panel.
- En tu propio ordenador: **Conexiones**, abre Gmail, **Detalles** y luego **Desconectar**. Deja de leer. Lo que ya trajo se queda. Cuando nada más usa ese inicio de sesión de Google, se revoca en Google.

## Desinstálalo en Google

En tu cuenta de Google, abre Seguridad, luego Tus conexiones con aplicaciones y servicios de terceros, y quita Salesflare (Iniciar sesión con Google, o alojada) o tu propia app.
