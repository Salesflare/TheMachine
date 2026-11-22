---
title: Promesas
area: cards
summary: Lo que dijiste que harías y lo que otros te prometieron. Se registra automáticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: ba0e2190e1b8b791
---
Lleva un seguimiento de lo que prometiste y de lo que otros te prometieron. Tu Machine detecta automáticamente las promesas en tus mensajes.

## Dónde están

En **Promesas**, en la página de Tareas:

- Lo que dijiste que harías y para quién: **Tu promesa**.
- Lo que otros dijeron que harían: **Te lo prometieron**.

Cada una tiene un menú **⋯**:

- **Hazlo** en las tuyas: se convierte en una tarea al momento y tu Machine la prepara. **Recordar** en las de otros: tu Machine redacta un breve seguimiento en el mismo sitio donde te lo prometieron, y tú sigues en la lista. Aparece una nota breve que indica que está en camino, junto con **Abrir tarea**, y la promesa muestra «ahora es una tarea». No se envía nada hasta que lo envíes. Si ya es una tarea, se abre esa tarea.
- **Marcar como hecho**: se cumplió.
- **No va a pasar**: no se cumplirá, así que tu Machine deja de hacerle seguimiento y no crea ninguna tarea.

Una promesa abierta también se convierte automáticamente en tarea cerca de su fecha (las tuyas, la mañana anterior, para que tengas un día para hacerla; las de otros, la mañana siguiente, si sigue abierta) y aparece ese día en el [Calendario](calendar.md). Si ya es una tarea, enlaza con ella, y **Marcar como hecho** o **No va a pasar** también cierra esa tarea. Cuando tu Machine detecta que está hecha, se cierran ambas y aparece una nota que lo indica.

Una respuesta que solo promete hacer el trabajo, como «Te enviaré los archivos antes del martes», no completa la tarea. La tarea sigue abierta con esa fecha y la promesa enlaza con ella. La revisión del envío te lo indica antes de que lo envíes.

¿Ya se cumplió, por ejemplo, con una respuesta que enviaste o una reunión en la que se trató el tema? Se cierra automáticamente, sin crear ninguna tarea.

Cuando alguien responde a una promesa que hizo, esta sigue abierta hasta que la respuesta indique que se cumplió. Un «Claro», una respuesta automática o una respuesta que solo cubre parte de la promesa no la cumplen. Si había un recordatorio pendiente de envío, se cancela y la tarea sigue abierta con «Han vuelto a escribir».

¿Te dieron una nueva fecha posterior, como «mejor, la semana que viene»? La misma promesa cambia de fecha, y también su tarea, sin crear una segunda. Su página muestra la nueva fecha y el mensaje más reciente.

Si no tiene fecha, se le asigna un día de **seguimiento**: tres días después de que la hicieras tú, o una semana después de que la hiciera otra persona. ¿Sigue abierta para entonces? Se convierte en tarea.

Las promesas de Slack muestran el nombre de la persona.

También se registra una promesa por correo de alguien a quien nunca has escrito, marcada como **remitente sin verificar**: solo tienes su palabra. La tarea empieza con «Sin verificar: nunca le has escrito».

## Reembolsos

Cuando una tienda, aerolínea, arrendador o aseguradora te promete devolverte dinero, por ejemplo, un reembolso por un pedido cancelado o una reclamación aprobada, tu Machine registra el importe, quién te lo paga y el día en que debería llegar. Aparece en **Te lo prometieron**. Solo si el mensaje deja claros los tres datos.

Si el dinero llega antes, por ejemplo, mediante un correo que dice «reembolso procesado», un aviso de un servicio de pago o una notificación de la app del banco en tu móvil, se cierra automáticamente, sin crear ninguna tarea.

¿No ha llegado para ese día? Se crea una única tarea discreta: «Reclamar el reembolso de 42 € a …», con un breve correo para esa persona que indica el número del pedido o del caso. No se envía nada hasta que lo envíes. Si al final llega el dinero, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

El [resumen semanal](weekly-recap.md) cuenta las promesas cumplidas y las que siguen abiertas. En tu propio ordenador, `assistant promises` las muestra en un terminal.
