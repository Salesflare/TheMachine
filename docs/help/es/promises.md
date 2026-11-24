---
title: Promesas
area: cards
summary: Lo que dijiste que harías y lo que otros te prometieron. Se registran automáticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 0bc6594bbd8f4c0b
---
Lleva un seguimiento de lo que prometiste y de lo que otros te prometieron. Tu Machine detecta promesas en tus mensajes automáticamente.

## Dónde encontrarlas

En **Promesas**, en la página Tareas:

- Lo que dijiste que harías y para quién: **Tu promesa**.
- Lo que otros dijeron que harían: **Te lo prometieron**.

Cada una tiene un menú **⋯**:

- **Hazlo** en las tuyas: se convierte en una tarea y tu Machine la prepara. **Recordar** en las de otros: tu Machine prepara un breve mensaje de seguimiento en el mismo lugar donde hicieron la promesa, y tú sigues en la lista. Aparece una nota breve que indica que está en camino, con **Abrir tarea**, y la promesa muestra «ya es una tarea». No se envía nada hasta que lo envíes. Si ya es una tarea, se abre.
- **Marcar como hecho**: se cumplió.
- **No va a pasar**: no se cumplirá, así que tu Machine deja de hacerle seguimiento y no crea ninguna tarea.

Una promesa abierta también se convierte automáticamente en tarea cerca de la fecha indicada: las tuyas, la mañana anterior, para que tengas un día para hacerla; las de otros, la mañana siguiente, si siguen abiertas. Además, aparece ese día en el [Calendario](calendar.md). Si ya es una tarea, enlaza con ella, y **Marcar como hecho** o **No va a pasar** también la cierra. Cuando tu Machine ve que se ha hecho, cierra ambas y añade una nota para indicarlo.

Una respuesta que solo promete hacer el trabajo, como «Te enviaré los archivos el martes», no completa la tarea. La tarea sigue abierta con esa fecha y la promesa enlaza con ella. La pantalla de revisión del envío lo indica antes de que lo envíes.

¿Ya se cumplió, por ejemplo, con una respuesta que enviaste o en una reunión? Se cierra automáticamente, sin crear una tarea.

Cuando alguien responde a una promesa que hizo, sigue abierta hasta que la respuesta confirme que se cumplió. Un «Claro» o cumplir solo una parte no basta. Si había un recordatorio pendiente de enviar, se cancela y la tarea sigue abierta con el aviso «Han vuelto a escribir». Una respuesta automática de ausencia no cambia nada.

¿Se ha aplazado la fecha, por ejemplo, con un «mejor la semana que viene»? Se actualiza la misma promesa y también su tarea, sin crear otra. Su página muestra la nueva fecha y el mensaje más reciente.

Las promesas sin fecha tienen un **día de seguimiento**: tres días después de que la hicieras tú o una semana después de que la hiciera otra persona. ¿Sigue abierta para entonces? Se convierte en tarea.

Las promesas de Slack muestran el nombre de la persona.

También se registran las promesas por correo de alguien a quien nunca has escrito, marcadas como **remitente sin verificar**: solo cuentan con su palabra. La tarea empieza con «Sin verificar: nunca le has escrito».

## Reembolsos

Cuando una tienda, aerolínea, casero o aseguradora te promete devolver dinero, por ejemplo, un reembolso por un pedido cancelado o una reclamación aprobada, tu Machine registra el importe, quién te paga y la fecha prevista. Aparece en **Te lo prometieron**. Solo se registra si el mensaje deja claros los tres datos.

Si el dinero llega antes, por ejemplo, con un correo que diga «reembolso procesado», un aviso de un servicio de pago o una notificación de la app de tu banco en el móvil, la promesa se cierra automáticamente, sin crear una tarea.

¿No ha llegado para esa fecha? Aparece una tarea discreta: «Reclama el reembolso de 42 € de…», con un correo breve que incluye el número del pedido o del caso. No se envía nada hasta que lo envíes. Si al final recibes el dinero, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

El [resumen semanal](weekly-recap.md) cuenta las promesas cumplidas y las que siguen abiertas. En tu propio ordenador, `assistant promises` las muestra en un terminal.
