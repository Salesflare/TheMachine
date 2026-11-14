---
title: Traspasos
area: fleet
summary: Pasa una tarea a la Machine de un compañero con todo lo que necesita. Pregunta cómo va más tarde o recupérala.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: acb60a24ef374625
---
## Pasar una tarea

1. En la tarea, abre **…**, luego **Pasar…** y elige **Un compañero**.
2. Elige a quién, revisa qué se incluye (× deja fuera una parte) y añade una nota. No se incluye nada de una cuenta Personal ni de otra empresa.
3. Envíala. Su Machine se la muestra como una tarea.

Su Machine le envía una notificación al teléfono o por Telegram. Si no tiene configurado ninguno de los dos, le manda un único correo con quién se la pasó, el título y un enlace. Consulta [Notificaciones](notifications.md).

También se incluye la conversación de Intercom. Si su Machine tiene acceso al mismo espacio de trabajo de Intercom, **Leer mensaje** la abre y su respuesta se envía a Intercom. Si no, la tarea incluye un enlace a la conversación.

Mientras esperas, la tarea indica lo que pediste y cuándo («Se lo pediste a Pat el mar 3 nov: …»), solo si eso aporta algo al título. Aparece en **Vuelve más tarde**, con el estado «Con Pat · esperando» y una fecha para preguntar cómo va. **Hacer seguimiento ahora** prepara un breve recordatorio para que se lo envíes a Pat; **Cambiar hora** cambia cuándo preguntar.

Si la Machine de Pat no puede enviarle notificaciones, la tarea dice «Pat no recibirá una notificación. Avísale». Díselo tú a Pat. El mensaje desaparece cuando active las notificaciones.

La tarea vuelve a aparecer arriba solo cuando hay algo que decidir: Pat respondió, la rechazó o la terminó, el traspaso falló o llegó una fecha límite. La fecha para preguntar cómo va depende de la fecha de vencimiento: unas horas si vence hoy, el día laborable anterior si vence pronto, a la mañana siguiente si es urgente y, en los demás casos, en 3 días laborables.

Cuando vuelve para preguntar cómo va, dice «Sigue con Pat». **Hacer seguimiento ahora** prepara un breve recordatorio para Pat en el mismo canal donde se lo pediste (Slack, WhatsApp, Telegram o correo), desde la tarea. No se envía nada hasta que elijas **Enviar**; después, vuelve a quedar pendiente de Pat. Si ninguno de los canales que conectaste puede enviarle un mensaje a Pat, se abre el chat y se indica. **Recuperar** y **Pasar a otra persona** están en **…**, luego **Pasar…**.

El chat de la tarea muestra cuándo se envió («Pasada a la Machine de Pat · 14:02») y qué respuesta llegó: aceptada, rechazada (con su nota) o terminada. Si todavía no hay respuesta, ofrece **Marcar como hecha**, **Posponer** y **No hace falta**. Para recordárselo o recuperarla, dilo en el chat.

Si no se pudo enviar el traspaso, la tarea y su chat lo indican y muestran **Reintentar**.

## Pasársela a otra persona

Mientras la tiene un compañero, la tarea lo indica en una línea («Con Pat · esperando») y muestra **Recuperar** y **Pasar a otra persona** en **…**, luego **Pasar…**. **Recuperar** hace que vuelva a ser tuya: se avisa a la Machine de Pat y su respuesta ya no la cambia.

**Pasar a otra persona** abre el formulario de traspaso. También puedes decirlo en el chat de la tarea («esta debería ir a Kim»): entonces la tarea dice «Sigue con Pat hasta que se la pases a Kim» y muestra **Revisar traspaso a** Kim.

Cada tarea se pasa una sola vez a cada compañero: mientras Pat la tenga, si vuelves a elegir a Pat en el formulario de traspaso, se inicia un seguimiento. **Preguntar cómo va** prepara el mismo recordatorio, con una línea tuya si añades una.

**Recuperar de** Pat está activado de forma predeterminada; desactívalo para que ambos tengan la tarea. No se envía nada hasta que elijas **Pasar**. Se avisa a la Machine de Pat y su copia de la tarea desaparece.

## Si la rechaza

Puede explicar por qué: no le corresponde, ya está hecha o no tiene tiempo esta semana. Después, elige **Lo hago yo**, **Pasar a otra persona** o **Marcar como hecha**. Lo mismo ocurre si no responde a tiempo. **Lo hago yo** hace que la tarea vuelva a ser tuya y aparezca en Para ti.

## Alguien fuera de Network

Elige **Por correo**: tu Machine prepara un correo para que lo envíes. Mientras escribes, primero te sugiere personas de tu Fleet y luego de tu empresa. Añade una página de tarea para que puedan responder con un toque: consulta [Páginas de tareas](task-pages.md).

Solo para tareas de Trabajo. Marca qué quieres incluir: unas líneas sobre la tarea, su borrador, enlaces y archivos. El contenido Personal y Solo tú no se incluye. **Preparar correo** añade el correo a la tarea: léelo y envíalo desde tu propio buzón. No se hace seguimiento.

Las tareas de Intercom o Slack no tienen un buzón propio, así que sus correos se envían desde tu buzón de Trabajo.

Luego, la tarea sigue la promesa hasta que respondan que está hecha o la marques como hecha. El correo termina con «Hazte cargo en tu propia Machine»: si se registran desde ese enlace, pueden unirse a tu Fleet y la tarea pasa a su Machine. Desactiva esa frase en **Ajustes**, en Fleet.
