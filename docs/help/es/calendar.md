---
title: Calendario
area: calendar
summary: La semana que tienes por delante en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 93fe9794660b0ab2
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que conectaste,
- tareas que vencen ese día y tareas pospuestas que vuelven ese día,
- seguimientos del trabajo que delegaste,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de los correos de reservas y entradas.

Una reunión que aparece en dos calendarios se muestra una sola vez. Los eventos de un calendario que alguien compartió contigo aparecen atenuados, con el nombre de esa persona; nunca generan una tarea. Los eventos de todo el día y los que duran varios días se muestran como eventos de todo el día en cada uno de los días que abarcan. En **Agenda**, un viaje aparece primero cada uno de sus días. En **Semana** y **Mes**, aparece como una sola franja a lo largo de esos días, por ejemplo, «Viaje a Lisboa».

Un plan acordado entre varias personas cuenta como una sola promesa, marcada «Con» y el nombre de la otra persona. Si una promesa trata sobre una reunión de ese día con esa misma persona, aparece en la fila de la reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea pendiente, se muestra como **Preparación lista**, **Preparando** o **Tarea**. Las tareas que parecen terminadas, porque ya respondiste o porque el proceso detectó que ya se completaron, no aparecen como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día en una lista. Desplázate hacia abajo para ver los días siguientes o hacia arriba, o toca **Mostrar días anteriores**, para ver los anteriores. Retrocede hasta una semana antes de que conectaras tu calendario, y una línea en la parte superior indica desde qué día. Cuando se cargue el [historial](history.md), retrocede aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil, muestra tres días.
- **Mes** muestra el mes completo. En una computadora se muestran hasta tres elementos por día; en el móvil aparecen puntos y, al tocar uno, se muestra la lista de ese día.

**Hoy**, ‹ y ›, en la parte superior, te permiten avanzar y retroceder por las semanas o los meses. La vista que elijas se recuerda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro, y todos se pueden leer. El resto aparece como **+N**. Al tocarlo, se abre ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa, el viaje o el evento, o la reunión. Si no puedes cambiar una reunión desde aquí, por ejemplo, porque es de otra persona o tiene invitados, verás sus detalles: cuándo, dónde y quiénes asisten. Las personas que conoce tu Graph y las organizaciones y proyectos relacionados con la reunión enlazan a sus páginas. **Abrir en Google Calendar** o **Abrir en Outlook**, debajo, abre la reunión en ese servicio. Consultarla no cambia nada.

La sala reservada para una reunión aparece en el campo de ubicación, nunca como persona ni en tu Graph.

El enlace de una reunión aparece con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes en tu correo una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un viaje: la ida, el hotel y la vuelta. El viaje aparece como una sola franja a lo largo de los días que abarca. Ábrelo para ver el código de reserva, el asiento y el billete de cada reserva, en orden cronológico.

Las entradas para un concierto, partido, festival o conferencia crean un evento, uno por cada evento, con su ubicación, el código de reserva, el asiento y la cantidad de entradas. Si haces otro pedido para el mismo evento, se añade al existente. Un evento reservado desde tu correo de trabajo es de Trabajo; de lo contrario, es Personal.

- Cada línea indica quién envió la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si del correo se creó una tarea, por ejemplo, para pagar las entradas, **Abrir la tarea** la muestra.
- Si se modifica una reserva, se actualiza su línea. Si se cancela, desaparece. Cuando se cancelan todas las reservas, también desaparece el viaje o el evento.

Lee los datos que las aerolíneas, los hoteles, los sitios de reservas y los vendedores de entradas incluyen en los correos de confirmación, sin usar IA. Si un correo no incluye esos datos, no se crea nada. Los correos de reservas del año que abarca el [historial](history.md) que conserva tu Machine se leen en segundo plano cuando ese historial está cargado.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** contiene todo lo que se dijo, palabra por palabra. Aparece plegada, junto con su duración; toca **Mostrar** para abrirla.

Si no se cargan, se vuelven a intentar cargar automáticamente durante aproximadamente medio minuto. Después, toca **Reintentar**.

Cada parte tiene su propio botón **Añadir notas** o **Añadir transcripción**, **Subir archivo** para cargar un archivo Markdown o de texto, **Editar** y **Quitar** (toca dos veces). El contenido de una parte no pasa a la otra. En las reuniones que puedes cambiar, **Notas**, debajo del formulario, las abre.

Si conectaste [Zoom](zoom.md) o [Google Meet](google-meet.md), sus notas aparecen en Notas y su transcripción en Transcripción, con la etiqueta **De Zoom** o **De Google Meet**. Nunca reemplazan lo que añadiste. Si están ambas, se muestran ambas.

También se pueden añadir notas al evento de calendario de la propia reunión, una vez que haya empezado, o recibirlas por correo de Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de ellas si indican claramente los próximos pasos. Si llegan las mismas notas por dos vías, se crea una sola tarea y la reunión aparece como origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción, pero no notas, aparece **Generar notas**. The Machine las redacta a partir de la transcripción: un resumen breve, las decisiones y las tareas pendientes con la persona responsable, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si es larga, puede tardar unos minutos y se usa tu propio modelo. Las notas indican **Redactado por The Machine** y nunca reemplazan las notas que añadiste.

The Machine también puede añadirlas. Pídeselo en una tarea, por ejemplo: «añade esta transcripción a la reunión del equipo de hoy». La transcripción se añade a Transcripción y el resumen, a Notas. En el Calendario, las reuniones que las incluyen muestran **Notas** o **Transcripción**.

The Machine lee ambas para hacer el seguimiento de la reunión. Son de Trabajo o Personales, igual que la reunión, y solo se comparten con tu equipo si la reunión también se comparte.

La reunión se abre con estos detalles desde cualquier lugar donde la encuentres: en una cronología, en los resultados de búsqueda de mensajes o como origen de una tarea. **Invitación original**, en la parte inferior, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes cambiar tu propio calendario de Google. Outlook y otros calendarios solo se pueden consultar. **Nuevo evento** añade uno (en el móvil, está debajo de **+** en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento de ese calendario que no tenga invitados para cambiarlo o **Eliminarlo** (toca dos veces).

Al escribir en **Dónde**, se sugieren lugares: primero los que ya usaste y los de tus organizaciones, y después direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige una sugerencia o deja el texto que escribiste.

**Invitar** añade personas de tu Graph o cualquier dirección de correo electrónico. Esta opción solo está disponible en tu propio calendario. Encima del botón se muestran las personas que recibirán una invitación, y el botón indica cuántas son: **Añadir e invitar a 2**. Google envía las invitaciones cuando tocas el botón, no antes. Si no hay invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede ofrecerte un cambio, por ejemplo, añadir una recogida. Verás exactamente qué cambiaría. Solo se hará si tocas **Añadir**, **Guardar** o **Eliminar**.

¿Todavía no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre Conexiones: conecta [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente. Puede redactar una nota breve para cambiarlo u ofrecerte rechazarlo. No se envía nada hasta que lo apruebes.

Los eventos de todo el día, los que indican que estás disponible y los provisionales nunca cuentan, y cada conflicto aparece una sola vez. Una tarea de Trabajo solo indica que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú puedes ver con qué evento coincide.

## Prepárate para tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Prepárate para** la reunión. Es un resumen breve:

- **Quién:** quiénes son, según tu Graph.
- **Último contacto:** tu último intercambio con esas personas. Ese mensaje es el origen de la tarea después de la reunión.
- **Promesas pendientes:** lo que tú o esas personas aún tienen que cumplir.
- **Preguntas pendientes:** lo que aún no tiene respuesta.
- **Decidir o llevar:** qué hay que resolver o llevar.

La tarea llega la mañana de un día laborable: el mismo día de la reunión si es por la tarde; de lo contrario, el día laborable anterior. Solo usa información que ya está en tu Machine. Es solo para consultar: toca **Hecho** cuando la hayas leído. Si una promesa o pregunta requiere una acción, tiene su propia tarea.

Si no hay un historial útil, no se crea ninguna tarea. Las reuniones recurrentes, internas, personales o rechazadas no generan ninguna. Si cambia la hora de una reunión, su tarea se conserva y aparece en el nuevo horario. Si descartas la tarea, no vuelve a aparecer. La tarea de una reunión cancelada se cierra automáticamente.

Los detalles de la reunión muestran su tarea debajo de **Tarea**, a un toque de su chat.
