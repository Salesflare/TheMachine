---
title: Intercom
area: connections
summary: Conversaciones con clientes en tu espacio de trabajo de Intercom. Responde como tú, solo cuando la envías.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 2cbee87e6d24c0a9
---
## Qué lee

Las conversaciones con clientes de tu espacio de trabajo de Intercom: las de los últimos 7 días cuando conectas la cuenta y, después, las nuevas que vayan llegando. También lee a qué espacio de trabajo y compañero de equipo pertenece la cuenta con la que inicias sesión.

## Qué puede hacer

Con tu propio **Iniciar sesión con Intercom**, puede responder en una conversación como tú, pero solo después de que pulses **Enviar** en ese texto exacto. Nunca asigna, cierra ni etiqueta conversaciones, ni escribe notas. Una cuenta de Intercom compartida contigo a través de tu Fleet solo permite leer.

## Tareas de Intercom

Una tarea de Intercom muestra el cliente, y **Leer mensaje** abre la conversación con un enlace a ella en Intercom. La respuesta se envía en esa conversación, salvo que pidas que se envíe por correo.

Solo se convierten en tareas las conversaciones que tienes asignadas o que aún no tiene asignadas nadie. Cuando un compañero de equipo se hace cargo de una en Intercom, su tarea se cierra automáticamente y aparece **Deshacer**. En una cuenta de Intercom compartida contigo, tus conversaciones son las que están asignadas al compañero de equipo con el que escribes.

Una tarea de Intercom también se cierra automáticamente cuando alguien del equipo cierra la conversación en Intercom o responde y el cliente no vuelve a escribir, si la tarea solo pedía una respuesta. Esto también cuenta si respondiste justo antes de que llegara la tarea, antes de que The Machine leyera tu respuesta. Una nota, una acción de posponer o la respuesta de un bot no cuentan.

Cuando tu Machine no puede responder en Intercom (porque solo tienes acceso de lectura a la cuenta compartida, las respuestas están desactivadas o no está conectada), el borrador se envía por correo en su lugar. La tarea explica el motivo y pregunta **¿Enviar por correo en su lugar?** Para responder en Intercom, pulsa **Conecta tu propio Intercom** en la tarea e inicia sesión. Entonces, la tarea se vuelve a crear como una respuesta en Intercom. No se envía nada hasta que lo envíes.

Si tienes tu propio Intercom y otro compartido contigo para el mismo espacio de trabajo, no leen ambos: el compartido queda inactivo y sus conversaciones pasan al tuyo, una sola vez cada una.

## Conectarlo

1. En el panel: **Conexiones**, **Clientes**, Intercom. O, en la página de configuración de una Machine alojada, en app.themachine.computer/setup: **Más fuentes**, Intercom. En tu propio ordenador, vincula primero la Machine a tu cuenta.
2. Pulsa **Iniciar sesión con Intercom**.
3. Autoriza The Machine (creada por Salesflare) en Intercom. Volverás al lugar donde empezaste.

Si inicias sesión en otro espacio de trabajo, se añadirá una segunda cuenta de Intercom.

Intercom siempre cuenta como trabajo, para la empresa que aparece en el nombre de su espacio de trabajo.

## Quitarla

- En el panel: **Conexiones**, abre Intercom, pulsa **Detalles** y, después, **Desconectar**. Dejará de leer. Lo que ya haya importado se conserva.
- En una Machine alojada, también puedes pulsar **Quitar** junto a Intercom en la página de configuración.

## Desinstalarla en Intercom

En Intercom, abre Ajustes, Aplicaciones y Aplicaciones instaladas, y elimina The Machine.
