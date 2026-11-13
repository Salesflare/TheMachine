---
title: Conexiones
area: connections
summary: Tus fuentes en un solo sitio: cómo va cada una, añade una nueva o desconecta una.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
---
## Cómo van

La pestaña **Conexiones** agrupa tus fuentes en **Correo**, **Calendario**, **Chat** y **Otras fuentes**. Cada una indica cómo va: Conectada, Esperando la primera sincronización, Reconectando automáticamente o Necesita tu ayuda. Abre **Detalles** para ver **Sincronizaciones recientes**, donde su sincronización se explica con palabras sencillas (como "Al día" o "Primera lectura"), y qué hacer.

Una sincronización fallida que una posterior ya compensó se muestra en gris; solo un fallo que sigue siendo el último se muestra como problema, con cuándo vuelve a intentarlo.

Sus cifras muestran todo lo que trajo, también su [historial](history.md), lo que llegó en las últimas 24 h y lo que aún no se ha revisado. Un calendario cuenta eventos: todos, los de los próximos 7 días y los de las últimas 24 h.

Cada fuente lleva el nombre de su cuenta, como lo llama el servicio: tu dirección, un perfil de X, un espacio de trabajo de Slack o de quién es el Signal o el Telegram. Debajo: **Trabajo** o **Personal**, y la dirección o el usuario cuando el nombre aún no lo dice.

Debajo de su estado, cada fuente dice en una línea lo que trae y, cuando puede actuar, que solo lo hace después de que pulses **Enviar** o des el visto bueno.

## Añade una

Abre **+ Añadir** y elige una fuente. Te pregunta lo que necesita, una pregunta cada vez. **Cancelar** deja de añadirla. ¿Te fuiste antes de terminar? Vuelve a abrir **Conexiones**, en cualquier dispositivo, y sigue en el mismo paso. Cuando ya está conectada, tu Machine empieza a leerla enseguida y abre la tarjeta nueva, que muestra cómo va su primera sincronización. En una Machine alojada, Google, Microsoft, Microsoft OneDrive, Zoom, Stripe e Intercom inician sesión aquí: elige **Trabajo** o **Personal**, inicia sesión y vuelves a este formulario, que muestra cómo va la conexión. GitHub, WhatsApp, Codex, Chats de Telegram y tu teléfono Android muestran su código en este mismo formulario.

Una fuente que ya conectaste lo indica en la lista, con su cuenta. Elígela para añadir otra al lado: su formulario lo dice y enlaza a la que ya tienes.

La lista está agrupada (**Correo**, **Calendario**, **Chat**, **Reuniones**, **Documentos y archivos**, **Clientes**, **Proyectos y código**, **Otras**), de la A a la Z en cada grupo. Una opción general como **Otro correo** va al final de su grupo.

**Sugerido para ti** aparece arriba cuando tu Machine ve un motivo para una fuente, con ese motivo en una línea: correos de Stripe, reuniones de Zoom en tu calendario, mensajes con enlaces a Google Docs o una configuración que no terminó. La fuente también sigue en su propio grupo, marcada como **Sugerido**. Lo cuenta en tu Machine; nada sale de ella. Nunca sugiere una fuente ya conectada.

Microsoft Teams aparece dos veces: en **Chat** para sus chats y en **Reuniones** como **Reuniones de Teams** para sus notas de reuniones. Las dos usan el mismo inicio de sesión de Microsoft, así que conectar una conecta la otra.

**Reconectar** en una fuente y en **Te necesita** abre el mismo formulario. En tu propio ordenador, `assistant connect` hace lo mismo en un terminal.

## Trabajo o personal

Cada fuente cuenta como trabajo (para una empresa que indicas) o como personal. Cámbialo en **Detalles**. Solo dice **Adivinado** cuando tu Machine lo eligió a partir de la dirección; en cuanto eliges tú, la elección es tuya. Las tareas de trabajo esperan a tus días laborables.

El correo y los calendarios de Google y Microsoft siguen su dirección cuando está clara: un proveedor como Gmail u Outlook.com es Personal, el dominio de tu equipo es Trabajo. Si no, pregunta una vez, justo después de iniciar sesión. **Cambiar** te deja elegirlo. Si luego el correo dice lo contrario, la tarea **Saca más partido a The Machine** pregunta una vez si quieres cambiarlo.

## Capacidades

Una fuente puede traer señales (lo que llega se convierte en to-dos), hacer cosas para tus to-dos (leer un documento cuando uno lo necesita, o enviar, responder o cambiar algo tras tu OK), o ambas. Con ambas, **Detalles** tiene un interruptor para cada una: **Trae señales** y **Puede hacer cosas**. Una queda activada. Para detener ambas, desconéctala. Las respuestas de un chat contestan a lo que trae, así que un chat solo tiene **Puede hacer cosas**.

Con **Trae señales** desactivado, no se sincroniza y su tarjeta no muestra cifras. Con **Puede hacer cosas** desactivado, tu Machine nunca lee nada a demanda, ni redacta ni cambia nada con ella. Las fuentes de antes tienen ambas activadas.

## Quita una

Abre la fuente, **Detalles** y luego **Desconectar**. Deja de leer. Lo que ya trajo se queda. En una Machine alojada, Google, Microsoft, Microsoft OneDrive, Zoom y Stripe muestran **Desconectar ↗**, que abre tu página de configuración.

**Desconectado hace poco** lista los inicios de sesión de Google, Microsoft y Zoom que quitaste. **Eliminado, confirmado** significa que Google confirmó el cierre de sesión, o, en Microsoft y Zoom, que no queda ninguna copia. **Pendiente** dice por qué, y tu Machine lo sigue intentando.

## Inicios de sesión guardados

Los sitios que usa el navegador de tu Machine, como LinkedIn o X, pueden guardar un inicio de sesión: marca **Guardar para la próxima vez** al iniciar sesión. Luego **Inicios de sesión** los lista. Cuando un sitio cierra la sesión de tu Machine, vuelve a entrar con un toque. Las contraseñas se guardan cifradas en tu Machine. **Olvidar** quita uno.

## Revisiones

**Revisiones** muestra cómo está leyendo tu Machine lo que llega: las ejecuciones recientes y lo que encontró cada una. Consulta [No hay tareas nuevas](reviews-paused.md).

Cada conexión tiene su propio artículo en esta sección, con lo que lee y lo que puede enviar.
