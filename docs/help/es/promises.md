---
title: Promesas
area: cards
summary: Lo que dijiste que harías y lo que otros te prometieron. Se lleva el seguimiento automáticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Lleva un seguimiento de lo que prometiste y de lo que otros te prometieron. Tu Machine detecta las promesas en tus mensajes automáticamente.

## Dónde encontrarlas

En **Promesas**, en la página de Tareas:

- Lo que dijiste que harías y para quién: **Tu promesa**.
- Lo que otros dijeron que harían: **Te lo prometieron**.

Cada promesa tiene un menú **⋯**:

- **Hazlo** en las tuyas: se convierte en una tarea y tu Machine la prepara. **Recordar** en las de otros: tu Machine redacta un breve mensaje de seguimiento en el mismo sitio donde hicieron la promesa y tú sigues en la lista. Aparece un breve aviso de que está en camino, con **Abrir tarea**, y la promesa muestra «ahora es una tarea». No se envía nada hasta que lo envíes. Si ya es una tarea, se abre esa tarea.
- **Marcar como hecho**: se cumplió.
- **No va a pasar**: no se cumplirá, así que tu Machine deja de hacerle seguimiento y no crea ninguna tarea.

Una promesa abierta también se convierte automáticamente en tarea cerca de la fecha prevista (las tuyas, la mañana anterior, para que tengas un día para hacerla; las de otros, la mañana siguiente, si siguen abiertas) y aparece en el día correspondiente del [Calendario](calendar.md). Si ya es una tarea, incluye un enlace a ella, y **Marcar como hecho** o **No va a pasar** también cierra esa tarea. Cuando tu Machine detecta que se ha completado, cierra ambas y muestra un mensaje que lo indica.

Una respuesta que solo promete hacer el trabajo, como «Te enviaré los archivos el martes», no completa la tarea. La tarea sigue abierta con esa fecha y la promesa incluye un enlace a ella. La revisión del envío lo indica antes de que lo envíes.

¿Ya se cumplió, por ejemplo, con una respuesta que enviaste o en una reunión? Se cierra automáticamente, sin crear ninguna tarea.

¿Te dieron una fecha posterior, como «mejor, la semana que viene»? La misma promesa cambia de fecha, y su tarea también, sin crear una segunda tarea. Su página muestra la nueva fecha y el mensaje más reciente.

Si no tiene fecha, se le asigna un día de **seguimiento**: tres días después de que la hicieras tú, o una semana después de que la hicieran ellos. ¿Sigue abierta para entonces? Se convierte en tarea.

Las promesas de Slack muestran el nombre de la persona.

También se guarda una promesa que llega por correo de alguien a quien nunca has escrito, marcada como **remitente sin verificar**: solo tienes su palabra. La tarea empieza con «Sin verificar: nunca le has escrito».

## Reembolsos

Cuando una tienda, aerolínea, casero o aseguradora te promete devolver dinero, por ejemplo, el reembolso de un pedido cancelado o una reclamación aprobada, tu Machine guarda el importe, quién te lo paga y la fecha en que debería llegar. Aparece en **Te lo prometieron**. Solo si el mensaje deja claros los tres datos.

Si el dinero llega antes, por ejemplo, con un correo que dice «reembolso procesado», un aviso de un servicio de pago o una notificación de la app de tu banco en el móvil, se cierra automáticamente, sin crear ninguna tarea.

¿No ha llegado para ese día? Aparece una sola tarea discreta: «Reclama el reembolso de 42 € a …», con un breve correo para esa persona que incluye el número del pedido o del caso. No se envía nada hasta que lo envíes. Si al final llega el dinero, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

El [Resumen semanal](weekly-recap.md) cuenta las promesas cumplidas y las que siguen abiertas. En tu propio ordenador, `assistant promises` las muestra en un terminal.
