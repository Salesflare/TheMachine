---
title: Calendario
area: calendar
summary: La semana que viene en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 7187a83e373922b3
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que conectaste,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos de trabajos que delegaste,
- promesas con fecha.

Una reunión que aparece en dos calendarios se muestra una sola vez. Los eventos de un calendario que alguien compartió contigo aparecen atenuados y con el nombre de pila de esa persona; nunca generan una tarea. Los eventos de todo el día y los que duran varios días aparecen como eventos de todo el día, en cada día que abarcan.

Un plan acordado entre dos personas cuenta como una sola promesa, marcada como «Con» y el nombre de la otra persona. Si una promesa trata sobre una reunión de ese día con la misma persona, aparece en la fila de esa reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea pendiente, se muestra su estado: **Preparación lista**, **Preparando** o **Tarea**. Una tarea que parece terminada (porque ya respondiste o porque al ejecutarse se completó) no aparece como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver días posteriores o hacia arriba (o toca **Mostrar días anteriores**) para ver los anteriores. Muestra desde una semana antes de que conectaras tu calendario, con una línea arriba que indica desde qué día. Cuando esté disponible tu [historial](history.md), llegará hasta aproximadamente un año atrás.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil muestra tres días.
- **Mes** muestra todo el mes. En una computadora aparecen hasta tres eventos por día; en el móvil aparecen puntos y, al tocar uno, se muestran los eventos de ese día.

**Hoy**, ‹ y › en la parte superior te permiten avanzar o retroceder por las semanas o los meses. Se recuerda la vista que elijas en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro y se pueden leer. Los demás aparecen como **+N**. Tócalo para abrir ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa o la reunión. Si no puedes modificar una reunión desde aquí, por ejemplo, porque es de otra persona o tiene invitados, verás sus detalles: cuándo, dónde y quiénes asisten. Las personas que The Machine reconoce en tu Graph, y las organizaciones y los proyectos relacionados con la reunión, enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**) debajo de ellos abre la reunión allí. Consultarla no cambia nada.

Si una reunión tiene una sala reservada, aparece en «Dónde», nunca como persona ni en tu Graph.

El enlace de una reunión aparece con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Notas y transcripción de la reunión

Los detalles de una reunión tienen dos secciones. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** recoge palabra por palabra lo que se dijo. Al principio está contraída y muestra cuánto dura; **Mostrar** la abre.

Si no se cargan, se vuelven a cargar automáticamente durante aproximadamente medio minuto. Después, toca **Reintentar**.

Cada sección tiene sus propias opciones **Añadir notas** o **Añadir transcripción**, **Subir archivo** para subir un archivo Markdown o de texto, **Editar** y **Quitar** (toca dos veces). El contenido de una sección no se mezcla con el de la otra. Si puedes modificar la reunión, **Notas** debajo del formulario las abre.

Si conectaste [Zoom](zoom.md) o [Google Meet](google-meet.md), las notas aparecen en Notas y la transcripción en Transcripción, marcadas como **De Zoom** o **De Google Meet**. Nunca reemplazan lo que añadiste: si están ambas, se muestran ambas.

También puedes recibir notas en el propio evento de calendario de la reunión, añadidas después de que empiece, o por correo de Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de ellas si hay próximos pasos claros. Si recibes las mismas notas por dos vías, se crea una sola tarea, con la reunión como origen: **Notas de** la reunión.

Si una reunión tiene transcripción, pero no notas, aparece **Generar notas**. The Machine las redacta a partir de la transcripción: un resumen breve, decisiones y tareas pendientes con las personas responsables, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si es larga, puede tardar unos minutos y se usa tu propio modelo. Las notas indican **Escritas por The Machine** y nunca reemplazan las que añadiste.

The Machine también puede añadirlas. Pídeselo en una tarea, por ejemplo: «añade esta transcripción a la reunión de hoy del tablero». La transcripción se guarda en Transcripción y el resumen, en Notas. Si una reunión tiene estas notas, en el Calendario aparece **Notas** o **Transcripción**.

The Machine lee ambas para encontrar los seguimientos de la reunión. Son de Trabajo o Personales, como la reunión, y solo se comparten con tu equipo si la reunión también se comparte con él.

La reunión se abre con estos detalles dondequiera que la encuentres: en una cronología, en una búsqueda de mensajes o como origen de una tarea. **Invitación original**, al final, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes modificar tu propio calendario de Google. Outlook y otros calendarios solo se pueden consultar. **Nuevo evento** añade uno (en el móvil, está bajo **+** en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento de ese calendario que no tenga invitados para modificarlo o **Eliminarlo** (toca dos veces).

**Dónde** sugiere lugares mientras escribes: primero los que ya usaste y tus organizaciones; luego, direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige una sugerencia o deja tu propio texto.

**Invitar** añade personas de tu Graph o cualquier dirección de correo electrónico. Esta opción solo aparece en tu propio calendario. Los invitados aparecen encima del botón, que indica cuántos son: **Añadir e invitar a 2**. Google envía las invitaciones cuando lo tocas, no antes. Si no hay invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede ofrecerte un cambio, como añadir una recogida. Verás exactamente qué va a cambiar y solo se hará si tocas **Añadir**, **Guardar** o **Eliminar**.

¿Todavía no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre Conexiones, donde puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Cuando una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente. Puede redactar una nota breve para cambiarlo de hora u ofrecerte rechazarlo. No se envía nada hasta que lo apruebes.

Los eventos de todo el día, los marcados como libre y los provisionales no cuentan. Cada conflicto aparece una sola vez. Una tarea de Trabajo solo indica que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú puedes ver con qué evento coincide.

## Preparación para tus reuniones

Antes de una reunión con personas de fuera de tu empresa, The Machine crea una tarea: **Preparar** la reunión. Es un informe breve con:

- **Quién:** quiénes son, según tu Graph.
- **Último contacto:** tu último intercambio con esas personas. Después de la reunión, ese mensaje es el origen de la tarea.
- **Promesas pendientes:** lo que tú o esas personas aún tienen pendiente.
- **Preguntas pendientes:** lo que aún no tiene respuesta.
- **Decidir o llevar:** lo que hay que resolver o llevar.

La tarea aparece la mañana de un día laborable: el mismo día de la reunión si es por la tarde; si no, el día laborable anterior. Solo usa lo que ya está en tu Machine. Es solo para leer: toca **Hecho** cuando la hayas leído. Si incluye una promesa o una pregunta que requiere una acción, tendrá su propia tarea.

Si no hay información previa útil, no se crea ninguna tarea. Las reuniones recurrentes, internas, personales o rechazadas no generan tareas. Si cambia la hora de una reunión, conserva su tarea, que aparece a la nueva hora. Una tarea descartada no vuelve a aparecer y la de una reunión cancelada se cierra automáticamente.

En los detalles de la reunión, la tarea aparece bajo **Tarea**. Tócala para abrir su chat.
