---
title: Calendario
area: calendar
summary: La semana que tienes por delante, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 970b39054ae39543
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que has conectado,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos del trabajo que delegaste,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de los correos de reservas y entradas.

Una reunión que aparece en dos calendarios se muestra una sola vez. Los eventos de un calendario que alguien compartió contigo aparecen atenuados y con el nombre de pila de esa persona. Nunca generan una tarea. Los eventos de todo el día y los que duran varios días aparecen como eventos de todo el día, en cada uno de los días que abarcan. En Agenda, cada día de un viaje aparece primero. En Semana y Mes, el viaje aparece como una sola franja que abarca esos días, por ejemplo, «Viaje a Lisboa».

Un plan hecho en conjunto es una sola promesa, marcada como «Con» y el nombre de la otra persona. Si una promesa está relacionada con una reunión de ese día con la misma persona, aparece en la fila de esa reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea pendiente, se muestra su estado: **Preparación lista**, **Preparando** o **Tarea**. Las tareas que parecen estar hechas, porque ya respondiste o porque su ejecución confirmó que estaban hechas, no aparecen como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver días posteriores o hacia arriba, o toca **Mostrar días anteriores**, para ver los anteriores. Retrocede hasta una semana antes de que conectaras tu calendario; una línea en la parte superior indica desde qué día. Cuando se cargue el [historial](history.md), podrás retroceder alrededor de un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil, muestra tres días.
- **Mes** muestra el mes completo. En una computadora se muestran hasta tres elementos por día. En el móvil aparecen puntos; tócalos para ver la lista de ese día.

**Hoy**, ‹ y › en la parte superior te permiten avanzar o retroceder por las semanas o los meses. La vista que elijas se recuerda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro y se pueden leer. El resto se indica como **+N**. Tócalo para abrir ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de su tarea, la promesa, el viaje o evento, o la reunión. Si no puedes cambiar una reunión desde aquí, por ejemplo, porque pertenece a otra persona o tiene invitados, verás sus detalles: cuándo, dónde y quiénes participan. Las personas que conoce tu Graph y las organizaciones y proyectos asociados a la reunión enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**) debajo de esos datos la abre en ese servicio. Consultarla no cambia nada.

Si una reunión tiene reservada una sala, aparece en el campo de ubicación, nunca como persona ni en tu Graph.

El enlace de una reunión aparece con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando llega a tu correo una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje. Las reservas de un mismo recorrido se agrupan en un viaje: la ida, el hotel y la vuelta. El viaje aparece como una sola franja que abarca los días correspondientes. Ábrelo para ver el código de reserva, el asiento y el billete de cada reserva, en orden cronológico.

Las entradas para conciertos, partidos, festivales o conferencias crean un evento, uno por cada evento, con su ubicación, el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade al mismo. Los eventos reservados desde tu correo de trabajo son de Trabajo; los demás, de Personal.

- Cada línea indica quién envió la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo generó una tarea, como pagar las entradas, **Abrir la tarea** la muestra.
- Si se modifica una reserva, se actualiza su línea. Si se cancela, desaparece. Cuando se cancelan todas las reservas, también desaparece el viaje o evento.

La información se extrae, sin IA, de los detalles que las aerolíneas, los hoteles, los sitios de reservas y los vendedores de entradas incluyen en sus correos de confirmación. Si el correo no incluye esos detalles, no se crea nada. Los correos de reservas del año de [historial](history.md) que tu Machine conserva se leen en segundo plano cuando se carga ese historial.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos secciones. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** reproduce palabra por palabra lo que se dijo. Al principio aparece contraída y muestra su duración. Toca **Mostrar** para abrirla.

Si no se carga, vuelve a intentarlo automáticamente durante aproximadamente medio minuto. Después, toca **Reintentar**.

Cada sección tiene sus propias opciones: **Añadir notas** o **Añadir transcripción**, **Subir archivo** para añadir un archivo Markdown o de texto, **Editar** y **Quitar** (toca dos veces). El contenido añadido a una sección se queda ahí. En una reunión que puedes cambiar, toca **Notas** debajo del formulario para abrirlas.

Si conectas [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), sus notas aparecen en Notas y su transcripción en Transcripción, con la etiqueta **De Zoom**, **De Google Meet** o **De Granola**. Nunca reemplazan lo que añadiste. Si están ambas, se muestran las dos.

También pueden añadirse notas al evento de calendario de la reunión después de que empiece, o llegar por correo de Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de ellas si hay pasos siguientes concretos. Si las mismas notas llegan por dos vías, se crea una sola tarea con la reunión como origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción, pero no notas, aparece la opción **Generar notas**. The Machine las redacta a partir de la transcripción: un resumen breve, las decisiones y las tareas pendientes con quién debe encargarse, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si es una reunión larga, puede tardar unos minutos y usa tu propio modelo. Las notas indican **Redactadas por The Machine** y nunca reemplazan las que añadiste.

The Machine también puede añadirlas. Pídelo en un chat de una tarea, por ejemplo: «añade la transcripción de la reunión de hoy del equipo». La transcripción se añade a Transcripción y el resumen, a Notas. Si una reunión tiene notas o transcripción, aparece **Notas** o **Transcripción** en el Calendario.

The Machine lee ambas para identificar los seguimientos de la reunión. Son de Trabajo o Personal, igual que la reunión, y solo se comparten con tu equipo si la reunión también se comparte con él.

La reunión muestra estos detalles dondequiera que la abras: en una cronología, en una búsqueda de mensajes o como origen de una tarea. **Invitación original**, en la parte inferior, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes cambiar tu propio calendario de Google. Outlook y otros calendarios solo se pueden consultar. **Nuevo evento** añade un evento (en el móvil, está en **+**, en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento de ese calendario sin invitados para cambiarlo o **Eliminarlo** (toca dos veces).

**Dónde** sugiere ubicaciones mientras escribes: primero, las que ya usaste y las de tus organizaciones; después, direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige una sugerencia o deja tu propio texto.

**Invitar** añade personas de tu Graph o cualquier dirección de correo electrónico. Esta opción solo está disponible en tu propio calendario. Los invitados aparecen encima del botón, que indica cuántos hay: **Añadir e invitar a 2**. Google envía las invitaciones cuando lo tocas, no antes. Si no hay invitados, no se invita ni se avisa a nadie.

Una tarea también puede sugerir un cambio, como añadir una recogida. Muestra exactamente qué cambiará y solo se aplica si tocas **Añadir**, **Guardar** o **Eliminar**.

¿Aún no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre Conexiones: conecta [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre la más reciente de las dos. Puede redactar una nota breve para cambiarla o sugerir que la rechaces. No se envía nada hasta que lo apruebes.

Los eventos de todo el día, marcados como libres o provisionales nunca cuentan, y cada conflicto se muestra una sola vez. Una tarea de Trabajo solo indica que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú ves con qué coincide.

## Prepárate para tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Prepararse para** la reunión. Es un resumen breve:

- **Quién:** quiénes son, según tu Graph.
- **Último contacto:** tu último intercambio con ellas. Después de la reunión, ese mensaje aparece como origen de la tarea.
- **Promesas pendientes:** lo que tú o ellas aún tienen pendiente.
- **Preguntas pendientes:** lo que aún no tiene respuesta.
- **Decidir o llevar:** qué hay que resolver o llevar.

La tarea aparece la mañana de un día laborable: el mismo día de la reunión si es por la tarde; si no, el día laborable anterior. Solo usa información que ya está en tu Machine. Es solo para consultar: toca **Hecho** cuando la hayas leído. Si incluye una promesa o pregunta que requiere acción, tendrá su propia tarea.

Si no hay historial útil, no se crea ninguna tarea. Las reuniones periódicas, internas, personales y rechazadas no generan tareas. Si cambia la hora de una reunión, conserva su tarea y la actualiza con la nueva hora. Una tarea descartada no vuelve a aparecer; si se cancela la reunión, la tarea se cierra automáticamente.

Los detalles de la reunión muestran su tarea debajo de **Tarea**, a un toque de distancia de su chat.
