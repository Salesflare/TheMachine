---
title: Promesas
area: cards
summary: Lo que prometiste hacer y lo que otros te prometieron. Se registran automáticamente.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: 8e5ce7b371ab7fd0
---
Lleva un registro de lo que prometiste y de lo que otros te prometieron. Tu Machine detecta automáticamente las promesas en tus mensajes.

## Dónde encontrarlas

En **Promesas**, en la página de Tareas:

- Lo que dijiste que harías y para quién: **Tu promesa**.
- Lo que otros dijeron que harían: **Te lo prometieron**.

Cada una tiene un menú **⋯**:

- **Hazlo**, en las tuyas: se convierte en una tarea y tu Machine la prepara. **Recordar**, en las de otros: tu Machine redacta un breve seguimiento en el lugar donde hicieron la promesa, mientras tú sigues en la lista. Aparece una nota breve que indica que está en camino, con **Abrir tarea**, y la promesa muestra «ahora es una tarea». No se envía nada hasta que tú lo envíes. Si ya es una tarea, se abre esa tarea.
- **Marcar como hecha**: se cumplió.
- **No va a pasar**: no se cumplirá, así que tu Machine deja de hacerle seguimiento y no crea una tarea.

Una promesa abierta también se convierte automáticamente en tarea cerca de la fecha acordada (las tuyas, la mañana anterior, para que tengas un día para hacerla; las de otros, la mañana siguiente, si sigue abierta) y aparece ese día en el [Calendario](calendar.md). Si ya es una tarea, la promesa enlaza a ella, y **Marcar como hecha** o **No va a pasar** también cierra esa tarea. Cuando tu Machine detecta que se cumplió, cierra ambas y lo indica con una nota.

¿Ya se cumplió, por ejemplo, con una respuesta que enviaste o una reunión en la que se trató el tema? Se cierra automáticamente, sin crear una tarea.

¿Se acordó una fecha posterior, como «mejor la semana que viene»? La misma promesa cambia de fecha, y también su tarea, sin crear una segunda. Su página muestra la nueva fecha y el mensaje más reciente.

Si no tiene fecha, se le asigna un día de **seguimiento**: tres días después de que la hiciste tú, o una semana después de que la hizo otra persona. ¿Sigue abierta para entonces? Se convierte en una tarea.

Las promesas de Slack muestran el nombre de la persona.

También se registran las promesas por correo electrónico de alguien a quien nunca le has escrito. Se marcan como **remitente sin verificar**: solo cuentan con la palabra de esa persona. La tarea empieza con «No verificado: nunca le has escrito».

El [resumen semanal](weekly-recap.md) cuenta las promesas cumplidas y las abiertas. En tu propio ordenador, `assistant promises` las muestra en un terminal.
