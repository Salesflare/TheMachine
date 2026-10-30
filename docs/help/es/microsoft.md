---
title: Microsoft Outlook y Calendar
area: connections
summary: Correo y reuniones de Outlook, para Microsoft 365 y Outlook.com. Solo envía un correo después de que lo apruebes.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
---
## Qué lee

- **Outlook**: todo tu correo, los últimos 7 días al conectar y luego todo lo nuevo.
- **Calendario de Outlook**: tus reuniones, solo lectura.

El correo de Otros y los boletines reciben primero un vistazo rápido: remitente, asunto y unas palabras, muchos a la vez. Cuando uno importa, se lee entero y puede convertirse en una tarea. No se salta nada sin verlo.

## Qué puede enviar y cambiar

- Un correo desde una tarea, solo después de que lo apruebes en la vista previa.
- Una respuesta va en la conversación de Outlook del correo al que responde.
- Cuando pospones una tarea sobre un correo, los mensajes del hilo pasan a una carpeta Snoozed en Outlook y vuelven cuando vuelve la tarea.

El calendario nunca se cambia.

## Conéctalo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup.
2. Pulsa **Conectar Microsoft** e inicia sesión.
3. Si Microsoft pide la aprobación de un administrador, envía este enlace al administrador de tu Microsoft 365: themachine.computer/m365-admin-consent. **Copiar enlace** lo copia. En cuanto lo apruebe, todas las personas de tu organización pueden conectarse. Si eres tú, pulsa **Soy el administrador: aprobar ahora**.

O en el panel: **Conexiones**, **+ Añadir**, elige Outlook y pulsa **Iniciar sesión con Microsoft**. Cuando termines, vuelves al panel. ¿Necesitas la aprobación de tu administrador? El mismo enlace está debajo del botón, con **Copiar enlace**.

En tu propio ordenador, una vez [vinculado con tu cuenta](fleet.md): abre **Conexiones**, luego **+ Añadir**, elige Outlook y pulsa **Iniciar sesión con Microsoft**. El correo y el calendario se conectan juntos.

Con tu propia app: abre ahí **Usar tu propia app**, o ejecuta `assistant connect outlook` o `assistant connect outlook_calendar`. Usa tu propio registro de app en Microsoft Entra y un código de inicio de sesión. Te pregunta si también debe enviar lo que apruebes.

## Quítalo

- En una Machine alojada: pulsa **Desconectar** junto a la cuenta en tu página de configuración. En el panel, **Desconectar ↗** en Conexiones te lleva ahí. **Reconectar** ahí vuelve a iniciar sesión sin salir del panel.
- En tu propio ordenador: **Conexiones**, abre la cuenta, **Detalles** y luego **Desconectar**.

## Desinstálalo en Microsoft

Microsoft no nos ofrece forma de revocar un inicio de sesión, así que quítalo también ahí:

- Cuenta profesional o educativa: myapps.microsoft.com
- Cuenta personal: account.live.com/consent/Manage
