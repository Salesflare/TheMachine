---
title: Intercom
area: connections
summary: Conversaciones con clientes en tu espacio de trabajo de Intercom. Solo responde después de que envíes, en tu nombre.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, Or paste an access token, Connect, More sources, Remove
---
## Qué lee

Las conversaciones con clientes de tu espacio de trabajo de Intercom: los últimos 7 días al conectar, y luego las nuevas según llegan. También lee a qué espacio de trabajo y a qué administrador pertenece el inicio de sesión.

## Qué puede hacer

Lee conversaciones. Con tu propio **Iniciar sesión con Intercom**, también puede responder en una conversación en tu nombre, solo después de que pulses **Enviar** en ese texto exacto. Nunca asigna, cierra, etiqueta ni escribe notas. Un Intercom compartido contigo a través de tu Fleet solo lee.

## Tareas desde Intercom

Una tarea de una conversación de Intercom muestra de dónde viene: **Leer mensaje** abre la conversación, con un enlace a ella en Intercom, y el cliente aparece en la tarea. Su respuesta es una respuesta de Intercom en esa conversación, salvo que pidas un correo.

Cuando Intercom no puede responder desde tu Machine (compartido contigo solo para leer, respuestas sin activar o sin conectar), el borrador va por correo. La tarea dice por qué y su revisión pregunta **¿Enviar por correo en su lugar?** Para responder tú en Intercom, toca **Conecta tu propio Intercom** en la tarea e inicia sesión. No sale nada antes de que lo envíes.

## Conéctalo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre Intercom y pulsa **Iniciar sesión con Intercom**.
3. Aprueba The Machine en Intercom. La hace Salesflare.

Si el inicio de sesión no encaja con tu espacio de trabajo, abre **O pega un token de acceso**, pega un token del Developer Hub de Intercom y pulsa **Conectar**.

En tu propio ordenador:

1. En el Developer Hub de Intercom, abre tu app, luego Authentication, y copia su token de acceso.
2. En el panel, abre **Conexiones**, luego **+ Añadir**, y elige Intercom. O ejecuta `assistant connect intercom`.
3. Pega el token. Un token de otro espacio de trabajo se convierte en una segunda cuenta de Intercom.

Intercom siempre cuenta como trabajo, para la empresa que indica su espacio de trabajo.

## Quítalo

- En el panel: **Conexiones**, abre Intercom, **Detalles** y luego **Desconectar**. Deja de leer. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Desinstálalo en Intercom

- Con inicio de sesión de Intercom: en Intercom, abre Settings, Apps, Installed apps, y quita The Machine.
- Con un token pegado: elimínalo o rótalo en el Developer Hub, o elimina la app en la que lo creaste.
