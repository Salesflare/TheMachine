---
title: Calendario
area: calendar
summary: Toda la semana en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 9da7909bce253806
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que conectaste,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos del trabajo que delegaste,
- promesas con fecha.

Si una reunión aparece en dos calendarios, solo se muestra una vez. Los eventos de un calendario que alguien compartió contigo aparecen atenuados y con el nombre de esa persona; nunca generan una tarea. Los eventos de todo el día y los que duran varios días aparecen como eventos de todo el día en cada día que abarcan.

Un plan que hicieron juntos cuenta como una sola promesa, marcada como «Con» y el nombre de esa persona. Si una promesa está relacionada con una reunión de ese día con la misma persona, aparece en la fila de esa reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea pendiente, se muestra su estado: **Preparación lista**, **Preparando** o **Tarea**. Las tareas que parecen estar hechas (porque ya respondiste o porque al ejecutarse se confirmó que estaban hechas) no aparecen como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes o hacia arriba (o pulsa **Mostrar días anteriores**) para ver los anteriores. Retrocede hasta una semana antes de que conectaras tu calendario y muestra una línea en la parte superior que indica desde qué día. Cuando esté disponible tu [historial](history.md), podrás retroceder aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el teléfono, muestra tres días.
- **Mes** muestra el mes completo. En un ordenador, muestra hasta tres elementos al día. En un teléfono, muestra puntos; tócalos para ver la lista de ese día.

**Hoy**, ‹ y › en la parte superior te permiten avanzar o retroceder por las semanas o los meses. La vista que elijas se guarda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro y siguen siendo fáciles de leer. Los demás aparecen como **+N**; al pulsarlo, se abre ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa o la reunión. Si no puedes cambiar una reunión desde aquí, por ejemplo, porque pertenece a otra persona o tiene invitados, verás sus detalles: cuándo, dónde y quiénes asisten. Las personas que conoce tu Graph, así como las organizaciones y los proyectos relacionados con la reunión, enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**) debajo de esos detalles abre el evento en el calendario correspondiente. Consultarlo no cambia nada.

Si una reunión tiene una sala reservada, aparece en «Dónde», nunca como persona ni en tu Graph.

El enlace de una reunión aparece con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Notas y transcripción de la reunión

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** es lo que se dijo, palabra por palabra. Al principio está plegada y muestra cuánto dura; pulsa **Mostrar** para abrirla.

Si no se cargan, se vuelven a intentar cargar automáticamente durante aproximadamente medio minuto. Después, pulsa **Reintentar**.

Cada sección tiene sus propias opciones **Añadir notas** o **Añadir transcripción**, **Subir archivo** para subir un archivo Markdown o de texto, **Editar** y **Quitar** (pulsa dos veces). El contenido de una sección se mantiene en esa sección. En las reuniones que puedes cambiar, **Notas**, debajo del formulario, te permite abrirlas.

Si conectas [Zoom](zoom.md) o [Google Meet](google-meet.md), las notas de la reunión aparecen en Notas y la transcripción en Transcripción, con la etiqueta **De Zoom** o **De Google Meet**. Nunca reemplazan lo que añadiste: si están ambas, se muestran ambas.

También puedes añadir notas en el evento de calendario de la reunión, después de que haya empezado, o recibirlas por correo de Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de las notas si indican claramente qué hay que hacer. Si las mismas notas llegan por dos vías, se crea una sola tarea con la reunión como origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción, pero no notas, aparece la opción **Generar notas**. The Machine las redacta a partir de la transcripción: un resumen breve, decisiones y tareas pendientes con quién debe hacerlas, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si la reunión es larga, puede tardar unos minutos y usa tu propio modelo. Las notas indican **Escritas por The Machine** y nunca reemplazan las que añadiste.

The Machine también puede añadirlas. Pídeselo en una tarea, por ejemplo: «añade esta transcripción a la reunión de hoy del equipo». La transcripción se añade a Transcripción y el resumen, a Notas. En el Calendario, las reuniones que tienen notas o transcripción muestran **Notas** o **Transcripción**.

The Machine usa ambas para identificar los seguimientos de la reunión. Se clasifican como Trabajo o Personal, igual que la reunión, y solo se comparten con tu equipo si la reunión también se comparte.

La reunión se abre con estos detalles desde cualquier lugar donde la encuentres: en una cronología, en los resultados de búsqueda de mensajes o como origen de una tarea. **Invitación original**, en la parte inferior, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes cambiar tu propio calendario de Google. Outlook y los demás calendarios son de solo lectura. **Nuevo evento** añade un evento (en el teléfono, está bajo **+** en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento de ese calendario que no tenga invitados para cambiarlo o **Eliminarlo** (pulsa dos veces).

**Dónde** sugiere lugares mientras escribes: primero, los que ya usaste y tus organizaciones; después, direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige una sugerencia o conserva tu propio texto.

**Invitar** te permite añadir personas de tu Graph o cualquier dirección de correo electrónico. Esta opción solo está disponible en tu propio calendario. Los invitados aparecen encima del botón, que indica cuántos son: **Añadir e invitar a 2**. Google envía las invitaciones cuando pulsas el botón, no antes. Si no hay invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede ofrecerte hacer un cambio, por ejemplo, añadir una recogida. Te muestra exactamente qué cambiará y solo lo hace cuando pulsas **Añadir**, **Guardar** o **Eliminar**.

¿Todavía no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre Conexiones, donde puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente. Puede redactar una nota breve para cambiarlo u ofrecerte rechazarlo. No se envía nada hasta que lo apruebas.

Los eventos de todo el día, con disponibilidad libre o provisional nunca cuentan, y cada conflicto aparece una sola vez. Una tarea de Trabajo solo indica que hay un conflicto, así que tu equipo nunca verá el evento personal. Solo tú puedes ver con qué coincide.

## Prepárate para tus reuniones

Antes de una reunión con personas de fuera de tu empresa, The Machine crea una tarea: **Prepararse para** la reunión. Es un resumen breve:

- **Quién:** quiénes son, según tu Graph.
- **Último contacto:** tu último intercambio con esas personas. Ese mensaje será el origen de la tarea después de la reunión.
- **Promesas pendientes:** lo que tú o esas personas todavía tienen pendiente.
- **Preguntas pendientes:** lo que todavía no tiene respuesta.
- **Decidir o llevar:** lo que hay que decidir o llevar.

La tarea aparece la mañana de un día laborable: el mismo día de la reunión si es por la tarde; de lo contrario, el día laborable anterior. Solo usa información que ya está en tu Machine. Es solo para leer: pulsa **Hecho** cuando la hayas leído. Si incluye una promesa o una pregunta que requiere acción, tendrá su propia tarea.

Si no hay un historial útil, no se crea ninguna tarea. Las reuniones recurrentes, internas, personales y rechazadas no generan tareas. Si una reunión cambia de horario, conserva su tarea y se actualiza la hora. Una tarea descartada no vuelve a aparecer, y la tarea de una reunión cancelada se cierra automáticamente.

Los detalles de la reunión muestran su tarea debajo de **Tarea**; púlsala para abrir su chat.
