---
title: Intercom
area: connections
summary: Conversaciones con clientes en tu espacio de trabajo de Intercom. Solo responde en tu nombre cuando tú envías el mensaje.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 5a6938dd6c220a43
---
## Qué lee

Las conversaciones con clientes de tu espacio de trabajo de Intercom: las de los últimos 7 días cuando lo conectas y, después, las nuevas a medida que llegan. También lee a qué espacio de trabajo y compañero de equipo pertenece la cuenta con la que inicias sesión.

## Qué puede hacer

Si conectas tu propio Intercom con **Iniciar sesión con Intercom**, puede responder en una conversación en tu nombre, pero solo después de que pulses **Enviar** para enviar ese texto concreto. Nunca asigna conversaciones, las cierra, les añade etiquetas ni escribe notas. Un Intercom que comparten contigo a través de tu Fleet solo puede leer.

## Tareas de Intercom

Una tarea de Intercom muestra al cliente. **Leer mensaje** abre la conversación e incluye un enlace para verla en Intercom. Los mensajes aparecen bajo el nombre de quien los escribió: los del cliente, por un lado, y los de tu equipo y su bot, por el otro. Esto también se aplica cuando un compañero de equipo o una campaña inició la conversación. La respuesta se envía en esa conversación, a menos que pidas enviarla por correo.

Solo se convierten en tareas las conversaciones asignadas a ti o que aún no tienen a nadie asignado. Cuando un compañero de equipo se hace cargo de una en Intercom, la tarea se cierra automáticamente y aparece **Deshacer**. Si comparten contigo un Intercom, tus conversaciones son las asignadas al compañero de equipo con cuya identidad escribes.

Una tarea de Intercom también se cierra automáticamente si alguien del equipo cierra la conversación en Intercom o la responde y el cliente no ha vuelto a escribir, siempre que la tarea solo pidiera responder. También cuenta si respondiste justo antes de que llegara la tarea, antes de que The Machine leyera tu respuesta. Añadir una nota, posponer la conversación o que responda un bot nunca cuenta.

Si tu Machine no puede responder en Intercom (porque solo tienes acceso de lectura, las respuestas no están activadas o no está conectado), el borrador se prepara para enviarlo por correo. La tarea explica el motivo y pregunta **¿Enviar por correo en su lugar?** Para responder en Intercom, toca **Conecta tu propio Intercom** en la tarea e inicia sesión. Entonces, la tarea se vuelve a crear como una respuesta en Intercom. No se envía nada antes de que lo envíes tú.

Si tienes tu propio Intercom y otro compartido contigo para el mismo espacio de trabajo, no leen los dos: el compartido deja de leer y sus conversaciones pasan al tuyo, una sola vez cada una.

## Conectarlo

1. En el panel: **Conexiones**, **Clientes**, Intercom. O, en la página de configuración de una Machine alojada, en app.themachine.computer/setup: **Más fuentes**, Intercom. Si usas tu propio ordenador, primero emparéjalo con tu cuenta.
2. Pulsa **Iniciar sesión con Intercom**.
3. Autoriza a The Machine (creada por Salesflare) en Intercom. Volverás al lugar desde el que empezaste.

Si inicias sesión en otro espacio de trabajo, se añade una segunda cuenta de Intercom.

Intercom siempre cuenta como trabajo, para la empresa que indica el nombre de su espacio de trabajo.

## Quitarla

- En el panel: **Conexiones**, abre Intercom y pulsa **Detalles** y luego **Desconectar**. Dejará de leer. Se conserva lo que ya haya importado.
- En una Machine alojada, también puedes pulsar **Quitar** junto a Intercom en la página de configuración.

## Desinstalarla en Intercom

En Intercom, abre Ajustes, Aplicaciones, Aplicaciones instaladas y elimina The Machine.
