---
title: Promesas
area: cards
summary: Lo que dijiste que harías y lo que otros te prometieron. Se lleva el control automáticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 22b81ed3f7c4801f
---
Lleva un registro de lo que prometiste y de lo que otros te prometieron. Tu Machine detecta promesas en tus mensajes automáticamente.

## Dónde están

En **Promesas**, en la página Tareas:

- Lo que dijiste que harías y para quién: **Tu promesa**.
- Lo que otros dijeron que harían: **Te lo prometieron**.

Cada una tiene un menú **⋯**:

- **Hazlo** en las tuyas: ahora se convierte en una tarea y tu Machine la prepara. **Recordar** en las de otros: tu Machine redacta un breve mensaje de seguimiento en el lugar donde hicieron la promesa, y tú sigues en la lista. Aparece una nota breve que indica que está en camino, junto con **Abrir tarea**, y la promesa muestra «ahora es una tarea». No se envía nada hasta que lo envíes tú. Si ya es una tarea, se abre esa tarea.
- **Marcar como hecha**: se cumplió.
- **No va a pasar**: no se cumplirá, así que tu Machine deja de hacerle seguimiento y no crea una tarea.

Una promesa abierta también se convierte automáticamente en tarea cerca de la fecha indicada (las tuyas, la mañana anterior, para que tengas un día para hacerla; las de otros, la mañana siguiente, si sigue abierta) y aparece en ese día del [Calendario](calendar.md). Si ya es una tarea, enlaza a ella, y **Marcar como hecha** o **No va a pasar** también cierra esa tarea. Cuando tu Machine detecta que se cumplió, cierra ambas y lo indica con una nota.

¿Ya se cumplió, por ejemplo, con una respuesta que enviaste o una reunión en la que se trató el tema? Se cierra automáticamente, sin crear una tarea.

¿Te dieron una fecha nueva más adelante, como «mejor, la semana que viene»? Se actualiza la misma promesa y también su tarea, sin crear otra. Su página muestra la nueva fecha y el mensaje más reciente.

Si no tiene fecha, se asigna un día de **seguimiento**: tres días después de que hicieras la promesa, o una semana después de que la hicieran. ¿Sigue abierta para entonces? Se convierte en tarea.

Las promesas de Slack muestran el nombre de la persona.

También se registran las promesas por correo de personas a quienes nunca les escribiste, marcadas como **remitente sin verificar**: solo cuentan con su palabra. La tarea empieza con «Sin verificar: nunca les has escrito».

## Reembolsos

Cuando una tienda, aerolínea, casero o aseguradora te promete devolverte dinero, por ejemplo, un reembolso por un pedido cancelado o una reclamación aprobada, tu Machine registra el importe, quién te lo pagará y la fecha en que debería llegar. Aparece en **Te lo prometieron**. Solo se registra si el mensaje deja claros los tres datos.

Si el dinero llega antes, por ejemplo, con un correo que dice «reembolso procesado», un aviso de un servicio de pago o una notificación de la aplicación del banco en tu teléfono, la promesa se cierra automáticamente, sin crear una tarea.

¿No ha llegado para ese día? Se crea una tarea discreta: «Reclama el reembolso de 42 € de …», con un breve correo que menciona el número del pedido o del caso. No se envía nada hasta que lo envíes tú. Si al final recibes el dinero, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

El [resumen semanal](weekly-recap.md) cuenta las promesas cumplidas y las abiertas. En tu propio ordenador, `assistant promises` las muestra en un terminal.
