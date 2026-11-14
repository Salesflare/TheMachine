---
title: Promesas
area: cards
summary: Lo que dijiste que harías y lo que otros te prometieron. Se registra automáticamente.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: dbac0241c54b0ec6
---
Lleva un registro de lo que prometiste y de lo que otros te prometieron. Tu Machine detecta automáticamente las promesas en tus mensajes.

## Dónde encontrarlas

En **Promesas**, en la página Tareas:

- Lo que dijiste que harías y para quién: **Tu promesa**.
- Lo que otros dijeron que harían: **Te lo prometieron**.

Cada promesa tiene un menú **⋯**:

- **Hazlo**, en las tuyas: se convierte en una tarea y tu Machine la prepara. **Recordar**, en las de otros: tu Machine redacta un breve seguimiento en el lugar donde hicieron la promesa, y tú sigues en la lista. Aparece una nota breve que dice que está en camino, con **Abrir tarea**, y la promesa indica «ahora es una tarea». No se envía nada hasta que lo envíes tú. Si ya es una tarea, se abre esa tarea.
- **Marcar como hecha**: se cumplió.
- **No va a pasar**: no se cumplirá, así que tu Machine deja de registrarla y no crea ninguna tarea.

Una promesa abierta también se convierte automáticamente en tarea cuando vence: las tuyas, la mañana anterior, para que tengas un día para hacerla. Además, aparece ese día en el [Calendario](calendar.md). Si ya es una tarea, tiene un enlace a ella, y **Marcar como hecha** o **No va a pasar** también cierra esa tarea. Cuando tu Machine detecta que se cumplió, cierra ambas y lo indica con una nota.

¿Ya se cumplió, por ejemplo, con una respuesta que enviaste o una reunión en la que se trató? Se cierra automáticamente, sin crear una tarea.

¿Se le asignó una nueva fecha más adelante, como «mejor la semana que viene»? Se actualiza la misma promesa y también su tarea, sin crear otra. Su página muestra la nueva fecha y el mensaje más reciente.

Si no tiene fecha, se le asigna un día de **seguimiento**: tres días después de que la hiciste tú o una semana después de que la hicieran ellos. ¿Sigue abierta para entonces? Se convierte en tarea.

Las promesas de Slack muestran el nombre de la persona.

También se registra una promesa por correo de alguien a quien nunca le escribiste, marcada como **remitente sin verificar**: solo tienes su palabra. La tarea empieza con «No verificado: nunca le has escrito antes».

El [resumen semanal](weekly-recap.md) cuenta las promesas cumplidas y las abiertas. En tu propio ordenador, `assistant promises` las muestra en una terminal.
