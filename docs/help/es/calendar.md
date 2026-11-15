---
title: Calendario
area: calendar
summary: La semana que viene, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: d85b3eff63ea503d
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que conectaste,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos del trabajo que delegaste,
- promesas con fecha,
- [notas](notes.md) con fechas, como un viaje.

Una reunión que aparece en dos calendarios se muestra una sola vez. Los eventos de un calendario que alguien compartió contigo aparecen atenuados y con su nombre, y nunca generan una tarea. Los eventos de todo el día y de varios días se muestran como eventos de todo el día en cada uno de los días que abarcan. En **Agenda**, un viaje aparece primero en cada uno de sus días. En **Semana** y **Mes**, aparece como una sola franja a lo largo de esos días, por ejemplo, «Viaje a Lisboa».

Un plan que acuerdan juntos es una sola promesa, marcada con «Con» y el nombre de la otra persona. Si haces una promesa sobre una reunión de ese día con esa misma persona, aparece en la fila de la reunión.

**Vencida** aparece primero. Una reunión con una tarea pendiente muestra su estado: **Preparación lista**, **Preparando** o **Tarea**. Una tarea que parece completada, porque ya respondiste o porque su ejecución detectó que estaba hecha, no aparece en **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes, o hacia arriba (o toca **Mostrar días anteriores**) para ver los anteriores. Muestra hasta una semana antes de que conectaras tu calendario, y una línea en la parte superior indica desde qué día. Cuando se cargue su [historial](history.md), mostrará hasta aproximadamente un año atrás.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil, muestra tres días.
- **Mes** muestra el mes entero. En un ordenador se muestran hasta tres elementos por día; en el móvil aparecen puntos y, al tocar uno, se muestra la lista de ese día.

**Hoy**, ‹ y › en la parte superior te permiten avanzar o retroceder por las semanas o los meses. La vista que elijas se guarda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro, sin perder legibilidad. Los demás se agrupan como **+N**. Toca ahí para abrir ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa, la nota o la reunión. Si no puedes editar una reunión desde aquí, por ejemplo, porque es de otra persona o tiene invitados, se muestran sus detalles: cuándo es, dónde y quién asiste. Las personas que conoce tu Graph y las organizaciones y los proyectos asociados a la reunión enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**) debajo de ellos abre la reunión allí. Consultarla no cambia nada.

Si una reunión tiene reservada una sala, esta aparece debajo de dónde, nunca como persona ni en tu Graph.

El enlace de una reunión aparece con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Notas y transcripción de la reunión

Los detalles de una reunión tienen dos partes. **Notas** contiene el resumen: decisiones y tareas pendientes. **Transcripción** muestra lo que se dijo, palabra por palabra. Al principio está contraída y muestra cuánto dura. Toca **Mostrar** para abrirla.

Si no se carga, vuelve a intentarlo automáticamente durante aproximadamente medio minuto. Después, toca **Reintentar**.

Cada sección tiene sus propias opciones **Añadir notas** o **Añadir transcripción**, **Subir archivo** para subir un archivo Markdown o de texto, **Editar** y **Quitar** (toca dos veces). El contenido de una sección no se mezcla con el de la otra. En las reuniones que puedes editar, **Notas**, debajo del formulario, te permite abrirlas.

Si tienes [Zoom](zoom.md) o [Google Meet](google-meet.md) conectado, sus notas aparecen en Notas y su transcripción en Transcripción, marcadas como **De Zoom** o **De Google Meet**. Nunca reemplazan lo que hayas añadido: si están las dos, se muestran las dos.

También pueden llegar notas en el evento de calendario de la propia reunión, añadirse después de que empiece o enviarse por correo desde Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de ellas si hay próximos pasos claros. Si las mismas notas llegan por dos vías, se crea una sola tarea, con la reunión como origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción pero no notas, aparece la opción **Generar notas**. The Machine las redacta a partir de la transcripción: un resumen breve, las decisiones y las tareas pendientes, con la persona responsable de cada una, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Una reunión larga puede tardar unos minutos, ya que se usa tu propio modelo. Las notas indican **Redactadas por The Machine** y nunca reemplazan las notas que hayas añadido.

The Machine también puede añadirlas. Pídeselo en una tarea, por ejemplo: «Añade esta transcripción a la reunión de hoy del tablero». La transcripción se añade a Transcripción y el resumen, a Notas. En Calendar, las reuniones con notas o transcripción muestran **Notas** o **Transcripción**.

The Machine lee ambas para preparar el seguimiento de la reunión. Se clasifican como Trabajo o Personal, igual que la reunión, y solo se comparten con tu equipo si la reunión también se comparte con él.

Los detalles de una reunión se muestran siempre al abrirla, tanto si llegas a ella desde una cronología, una búsqueda de mensajes o el origen de una tarea. **Invitación original**, en la parte inferior, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes cambiar tu propio calendario de Google. Outlook y los demás calendarios solo se pueden consultar. **Nuevo evento** añade un evento (en el móvil, toca **+** en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento de ese calendario que no tenga invitados para cambiarlo o **Eliminarlo** (toca dos veces).

**Dónde** sugiere lugares a medida que escribes: primero, los que ya usaste y los de tus organizaciones; después, direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige una sugerencia o deja el texto que escribiste.

**Invitar** te permite añadir personas de tu Graph o cualquier dirección de correo. Esta opción solo está disponible en tu propio calendario. Las personas invitadas aparecen encima del botón, que indica cuántas son: **Añadir e invitar a 2**. Google envía las invitaciones al tocar el botón, no antes. Si no hay invitados, no se invita a nadie ni se envía ninguna actualización.

Una tarea también puede sugerir un cambio, como añadir una recogida. Muestra exactamente qué cambiará, y solo se aplica si tocas **Añadir**, **Guardar** o **Eliminar**.

¿Todavía no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre Conexiones, donde puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una sola tarea sobre el evento más reciente. Puede redactar una nota breve para cambiarlo de hora u ofrecerte cancelarlo. No se envía nada hasta que lo apruebes.

Los eventos de todo el día, los que indican que estás disponible y los provisionales no cuentan. Cada conflicto aparece una sola vez. Una tarea de Trabajo solo indica que hay un conflicto, así que tu equipo nunca verá el evento personal. Solo tú puedes ver con qué coincide.

## Prepárate para tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Prepararte para** la reunión. Es un resumen breve con:

- **Quién:** quiénes son, según tu Graph.
- **Último contacto:** el último intercambio que tuviste con esas personas. Después de la reunión, ese mensaje aparece como origen de la tarea.
- **Promesas pendientes:** lo que aún se deben tú o esas personas.
- **Preguntas pendientes:** lo que aún no tiene respuesta.
- **Decidir o llevar:** lo que tienes que resolver o llevar contigo.

La tarea llega por la mañana de un día laborable: el mismo día de la reunión si es por la tarde; si no, el día laborable anterior. Solo usa información que ya está en tu Machine. Es solo para leer: toca **Hecho** cuando la hayas leído. Las promesas o preguntas que requieran una acción tienen su propia tarea.

Si no hay historial útil, no se crea ninguna tarea. Las reuniones recurrentes, internas, personales y rechazadas no generan tareas. Si se cambia la hora de una reunión, conserva su tarea y la actualiza con la nueva hora. Si descartas una tarea, no vuelve a aparecer. La tarea de una reunión cancelada se cierra automáticamente.

Los detalles de la reunión muestran la tarea debajo de **Tarea**, a un toque de su chat.
