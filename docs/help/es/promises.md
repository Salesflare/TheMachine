---
title: Promesas
area: cards
summary: Lo que dijiste que harías y lo que otros te prometieron. Se lleva el seguimiento automáticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Lleva un seguimiento de lo que prometiste y de lo que otros te prometieron. Tu Machine detecta automáticamente las promesas en tus mensajes.

## Dónde están

En **Promesas**, en la página de Tareas:

- Lo que dijiste que harías y para quién: **Tu promesa**.
- Lo que otros dijeron que harían: **Te lo prometieron**.

Cada promesa tiene un menú **⋯**:

- **Hazlo** en las tuyas: se convierte en una tarea al momento y tu Machine la prepara. **Recordar** en las de otras personas: tu Machine prepara un mensaje breve de seguimiento en el mismo lugar donde hicieron la promesa, mientras tú sigues en la lista. Aparece una nota breve que indica que está en camino, junto con **Abrir tarea**, y la promesa muestra «una tarea ahora». No se envía nada hasta que lo envíes. Si ya es una tarea, se abre esa tarea.
- **Marcar como hecho**: la promesa se cumplió.
- **No va a pasar**: no se cumplirá, así que tu Machine deja de hacerle seguimiento y no crea una tarea.

Una promesa abierta también se convierte automáticamente en tarea cerca de la fecha indicada (las tuyas, la mañana anterior, para que tengas un día para hacerla; las de otras personas, la mañana siguiente, si sigue abierta) y aparece ese día en el [calendario](calendar.md). Si ya es una tarea, enlaza con ella, y **Marcar como hecho** o **No va a pasar** también cierra esa tarea. Cuando tu Machine detecta que se ha cumplido, cierra ambas y añade una nota para indicarlo.

Una respuesta que solo promete hacer el trabajo, como «Enviaré los archivos antes del martes», no completa la tarea. La tarea sigue abierta con esa fecha y la promesa enlaza con ella. La revisión del mensaje indica esto antes de que lo envíes.

¿Ya se cumplió, por ejemplo, con una respuesta que enviaste o una reunión en la que se trató el tema? Se cierra automáticamente, sin crear una tarea.

¿Se indica más adelante una fecha nueva, como «mejor la semana que viene»? La misma promesa cambia de fecha, y también su tarea, sin crear otra. Su página muestra la fecha nueva y el mensaje más reciente.

Si no tiene fecha, se le asigna un día de **seguimiento**: tres días después de que la hicieras tú, o una semana después de que la hiciera otra persona. Si para entonces sigue abierta, se convierte en tarea.

Las promesas de Slack muestran el nombre de la persona.

También se registra una promesa recibida por correo de alguien a quien nunca has escrito, marcada como **remitente sin verificar**: solo tienes su palabra. La tarea empieza con «Sin verificar: nunca le has escrito».

## Reembolsos

Cuando una tienda, aerolínea, arrendador o aseguradora te promete devolverte dinero, por ejemplo, un reembolso por un pedido cancelado o una reclamación aprobada, tu Machine registra el importe, quién te lo paga y cuándo debería llegar. Aparece en **Te lo prometieron**. Solo se registra si el mensaje deja claros los tres datos.

Si el dinero llega primero, por ejemplo, con un correo que indica «reembolso procesado», un aviso de un servicio de pago o una notificación de la app del banco en tu móvil, se cierra automáticamente, sin crear una tarea.

¿No ha llegado para ese día? Aparece una tarea discreta: «Reclama el reembolso de €42 a…», con un correo breve para esa persona que incluye el número del pedido o del caso. No se envía nada hasta que lo envíes. Si al final llega el dinero, la tarea se cierra automáticamente. **Deshacer** la vuelve a abrir durante un día.

El [resumen semanal](weekly-recap.md) cuenta las promesas cumplidas y las que siguen abiertas. En tu propio ordenador, `assistant promises` las muestra en un terminal.
