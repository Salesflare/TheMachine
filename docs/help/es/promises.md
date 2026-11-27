---
title: Promesas
area: cards
summary: Lo que dijiste que harías y lo que otros te prometieron. Se registra automáticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: b624394de7ff77b1
---
Lleva un registro de lo que prometiste y de lo que otros te prometieron. Tu Machine detecta automáticamente las promesas en tus mensajes.

## Dónde encontrarlas

En **Promesas**, en la página de Tareas:

- Lo que dijiste que harías y para quién: **Tu promesa**.
- Lo que otros dijeron que harían: **Te lo prometieron**.

Cada una tiene un menú **⋯**:

- **Hazlo** en las tuyas: se convierte en una tarea y tu Machine la prepara. **Recordar** en las de otros: tu Machine redacta un breve mensaje de seguimiento en el lugar donde hicieron la promesa, mientras tú sigues en la lista. Aparece una nota breve que indica que está en camino, junto con **Abrir tarea**, y la promesa muestra «ahora es una tarea». No se envía nada hasta que lo envíes. Si ya es una tarea, se abre esa tarea.
- **Hecho**: se cumplió.
- **No va a pasar**: no se cumplirá, así que tu Machine deja de hacerle seguimiento y no crea una tarea.

Una promesa abierta también se convierte automáticamente en una tarea cerca de la fecha indicada: las tuyas, la mañana anterior, para que tengas un día para hacerla; las de otros, la mañana siguiente, si sigue abierta. También aparece en el día correspondiente del [Calendario](calendar.md). Si ya es una tarea, enlaza con ella, y **Hecho** o **No va a pasar** también la cierra. Cuando tu Machine detecta que se ha cumplido, cierra ambas y añade una nota para indicarlo.

Una respuesta que solo promete hacer el trabajo, como «Te enviaré los archivos antes del martes», no completa la tarea. La tarea sigue abierta con esa fecha, y la promesa enlaza con ella. La revisión antes de enviar te lo indica. Si primero cambias el texto, se eliminan la promesa anterior y su fecha: la tarea sigue abierta hasta que tu Machine detecte que se ha hecho el trabajo, y la promesa incluida en lo que enviaste se añade a ella.

¿Ya se cumplió, por ejemplo, con una respuesta que enviaste o en una reunión? Se cierra automáticamente, sin crear una tarea.

Cuando alguien responde a una promesa que hizo, esta sigue abierta hasta que la respuesta indique que la cumplió. Un «Claro» o una respuesta parcial no cumple nada. Si había un recordatorio pendiente de envío, se cancela y la tarea sigue abierta con la nota «Volvió a escribir». Una respuesta automática de ausencia no cambia nada.

Si más adelante se indica una nueva fecha, como «mejor la semana que viene», se cambia la fecha de la misma promesa y también la de su tarea, sin crear otra. Su página muestra la nueva fecha y el mensaje más reciente.

Las promesas sin fecha tienen un día de **seguimiento**: tres días después de que la hicieras tú, o una semana después de que la hiciera otra persona. ¿Sigue abierta para entonces? Se convierte en una tarea.

Las promesas de Slack muestran el nombre de la persona.

También se registra una promesa por correo de alguien a quien nunca le has escrito, marcada como **remitente sin verificar**: solo depende de su palabra. La tarea empieza con «Sin verificar: nunca le has escrito».

## Reembolsos

Cuando una tienda, una aerolínea, un casero o una aseguradora te promete que te devolverá dinero, por ejemplo, por un pedido cancelado o una reclamación aprobada, tu Machine registra el importe, quién lo pagará y para qué día debería llegar. Aparece en **Te lo prometieron**. Solo si el mensaje deja claros los tres datos.

Si el dinero llega antes, por ejemplo, mediante un correo que dice «reembolso procesado», una notificación de un servicio de pago o una notificación de la app del banco en tu móvil, se cierra automáticamente, sin crear una tarea.

¿No ha llegado para esa fecha? Se crea una sola tarea discreta: «Reclama el reembolso de 42 € a …», con un breve correo para esa persona que incluye el número de pedido o de expediente. No se envía nada hasta que lo envíes. Si al final llega el dinero, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

El [resumen semanal](weekly-recap.md) cuenta las promesas cumplidas y las que siguen abiertas. En tu propio ordenador, `assistant promises` las muestra en un terminal.
