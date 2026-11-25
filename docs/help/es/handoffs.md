---
title: Traspasos
area: fleet
summary: Comparte una tarea con un compañero o pásasela a su Machine con **Pasar…**. Haz seguimiento más tarde o recupérala.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: d9b21c04fb0d34a6
---
## Pasar una tarea

1. En la tarea, abre **…**, luego **Pasar…** y elige **Un compañero**.
2. Elige a quién, revisa qué se comparte (× excluye una parte) y añade una nota. No se comparte nada de una cuenta Personal ni de otra empresa.
3. Envíala. Su Machine se la muestra como una tarea.

Su Machine le avisa en el móvil o en Telegram. Si no tiene ninguno configurado, le envía un correo una sola vez con quién se la ha pasado, el título y un enlace. Consulta [Notificaciones](notifications.md).

También se comparte la conversación de Intercom. Si su Machine tiene acceso al mismo espacio de trabajo de Intercom, **Leer mensaje** la abre y su respuesta vuelve a Intercom. Si no, la tarea incluye un enlace.

Mientras esperas, la tarea indica qué pediste y cuándo ("Se lo pediste a Pat el mar 3 nov: …"), solo si aporta algo al título. Aparece en **Vuelve más tarde**, con el estado «Con Pat · esperando» y una fecha para hacer seguimiento. **Hacer seguimiento ahora** prepara un recordatorio breve para Pat que puedes enviar; **Cambiar hora** cambia la fecha del seguimiento.

Si la Machine de Pat no puede avisarle, la tarea indica «Pat no recibirá ningún aviso. Avísale». Díselo tú. El mensaje desaparece cuando active las notificaciones.

La tarea vuelve arriba solo cuando hay algo que decidir: Pat ha respondido, la ha rechazado o terminado, el traspaso ha fallado o ha llegado una fecha límite. La fecha del seguimiento depende de la fecha de vencimiento: unas horas si vence hoy, el día laborable anterior si vence pronto, la mañana siguiente si es urgente y, en los demás casos, dentro de 3 días laborables.

Cuando vuelva para hacer seguimiento, indicará «Sigue con Pat». **Hacer seguimiento ahora** prepara un recordatorio breve para Pat en el canal donde se lo pediste (Slack, WhatsApp, Telegram o correo), desde la tarea. No se envía nada hasta que elijas **Enviar**; después, vuelve a quedar pendiente de Pat. Si ninguno de los servicios conectados permite escribirle a Pat, se abre el chat y se indica. **Recuperar** y **Pasar a otra persona** están en **…**, dentro de **Pasar…**.

El chat de la tarea muestra cuándo se envió («Pasada a la Machine de Pat · 14:02») y qué respuesta llegó: aceptada, rechazada (con su nota) o hecha. Si todavía no hay respuesta, ofrece **Marcar como hecho**, **Posponer** y **No hace falta**. Para recordárselo o recuperarla, díselo en el chat.

Si no se pudo enviar el traspaso, la tarea y su chat lo indican y muestran **Reintentar**.

## Qué ve la otra persona

Solo esa tarea: lo que pides, tu nota, la fecha de vencimiento y el contacto, además de copias de los mensajes que se comparten (hasta tres, sin archivos adjuntos). No ve tu bandeja de correo ni tus otras tareas. Puede elegir **Aceptar** o **Rechazar**.

Cuando la acepta, pasa a ser su tarea. La tuya queda hecha o espera a que la termine si tiene un **Hecho cuando**. No trabajáis los dos en la misma tarea: para que alguien la revise sin dejar de ser tuya, usa [Pedir revisión](ask-to-review.md).

## Pasársela a otra persona

Mientras la tiene un compañero, la tarea lo indica en una línea («Con Pat · esperando»), y muestra **Recuperar** y **Pasar a otra persona** en **…**, dentro de **Pasar…**. **Recuperar** vuelve a asignártela: se avisa a la Machine de Pat y su respuesta deja de cambiar el estado de la tarea.

**Pasar a otra persona** abre el formulario para pasarla. También puedes decirlo en el chat de la tarea («esta tarea debería ser para Kim»): entonces indica «Sigue con Pat hasta que se la pases a Kim» y muestra **Revisar traspaso a** Kim.

Cada tarea se pasa a cada compañero una sola vez: mientras Pat la tenga, si vuelves a elegirlo en el formulario, harás un seguimiento. **Preguntar cómo va** prepara el mismo recordatorio, con una línea tuya si añades una.

**Recuperar de** Pat está activado de forma predeterminada. Desactívalo para que la tarea sea de los dos. No se envía nada hasta que elijas **Pasar**. Se avisa a la Machine de Pat y desaparece su copia de la tarea.

## Si la rechazan

Pueden explicar por qué: no les corresponde, ya está hecha o no tienen tiempo esta semana. Después, elige **Lo hago yo**, **Pasar a otra persona** o **Marcar como hecho**. Lo mismo ocurre si no responden a tiempo. **Lo hago yo** vuelve a convertirla en una tarea tuya, en Para ti.

## Alguien ajeno a la Network

Elige **Por correo**: tu Machine prepara un correo para que lo envíes. Mientras escribes, primero sugiere personas de tu Fleet y luego gente de tu empresa. Añade una página de tarea para que puedan responder con un toque: consulta [Páginas de tarea](task-pages.md).

Solo para tareas de trabajo. Marca lo que quieres incluir: unas líneas sobre la tarea, su borrador, enlaces y archivos. El contenido Personal y Solo tú queda fuera. **Preparar correo** añade el correo a la tarea: léelo y luego envíalo desde tu propia bandeja de correo. No se hace seguimiento.

Las tareas de Intercom o Slack no tienen una bandeja de correo propia, así que el correo se envía desde tu bandeja de correo de trabajo.

Después, la tarea registra una promesa hasta que respondan que está hecha o la marques como hecha. El correo termina con «Hazte cargo de esto en tu propia Machine»: si se registran desde ese enlace, pueden unirse a tu Fleet y la tarea pasa a su Machine. Desactiva esa línea en **Ajustes**, en Fleet.
