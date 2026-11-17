---
title: Calendario
area: calendar
summary: La semana que tienes por delante, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: c1941aa6ca09b134
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que has conectado,
- tareas que vencen ese día y tareas pospuestas que vuelven ese día,
- seguimientos de trabajos que has delegado,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de los correos de reservas y entradas.

Una reunión que aparece en dos calendarios solo se muestra una vez. Los eventos de un calendario que alguien ha compartido contigo aparecen atenuados y con el nombre de pila de esa persona; nunca generan una tarea. Los eventos de todo el día y de varios días aparecen como eventos de todo el día en cada uno de los días que abarcan. En **Agenda**, un viaje aparece primero en cada uno de sus días. En **Semana** y **Mes**, aparece como una sola franja que abarca esos días, por ejemplo, «Viaje a Lisboa».

Un plan hecho entre varias personas cuenta como una sola promesa, marcada con «Con» y el nombre de la otra persona. Si hay una promesa sobre una reunión de ese día con esa misma persona, aparece en la fila de la reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea pendiente, muestra su estado: **Preparación lista**, **Preparando** o **Tarea**. Las tareas que parecen completadas, porque ya has respondido o porque una ejecución las encontró hechas, no aparecen como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes, o hacia arriba (o toca **Mostrar días anteriores**) para ver los anteriores. Retrocede hasta una semana antes de que conectaras tu calendario y verás una línea en la parte superior que indica desde qué día. Cuando esté disponible tu [historial](history.md), podrás retroceder aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil, muestra tres días.
- **Mes** muestra el mes entero. En un ordenador, muestra hasta tres elementos por día; en el móvil, muestra puntos. Toca un día para ver la lista de ese día.

**Hoy**, ‹ y ›, en la parte superior, te permiten avanzar o retroceder por las semanas o los meses. La vista que elijas se recuerda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en el horario aparecen uno junto al otro, sin perder legibilidad. El resto se muestra como **+N**. Tócalo para abrir ese día en la agenda.

## Abrir algo

Haz clic en una fila para abrir el chat de una tarea, la promesa, el viaje o evento, o la reunión. Si no puedes cambiar una reunión desde aquí, por ejemplo, porque pertenece a otra persona o tiene invitados, verás sus detalles: cuándo, dónde y quiénes asisten. Las personas que conoce tu Graph y las organizaciones y proyectos relacionados con la reunión enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**) abre la reunión en ese servicio. Consultarla no cambia nada.

Si una reunión tiene una sala reservada, aparece en «Dónde», nunca como persona ni en tu Graph.

Los enlaces a reuniones muestran el servicio, como Zoom, Google Meet o Teams, o el texto **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes en tu correo una reserva de vuelo, hotel, casa de vacaciones, tren, autobús, ferry, coche de alquiler, taxi o aparcamiento en el aeropuerto, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un solo viaje, aunque lleguen a cualquiera de tus buzones: el tren al aeropuerto, los vuelos, el coche, el alojamiento y el viaje de vuelta. Las reservas se agrupan cuando coinciden en fechas o cuando una empieza justo al terminar la otra.

El viaje aparece como una sola franja que abarca sus días. Ábrelo para ver cada reserva en orden cronológico, con sus horarios, dirección, código de reserva y asiento.

Las entradas para un concierto, un partido, un festival o una conferencia crean un evento por cada actividad, con el lugar, el código de reserva, el asiento y el número de entradas. Si haces un segundo pedido para el mismo evento, se añade al mismo. Si la entrada se reservó en tu buzón de trabajo, el evento es de Trabajo; de lo contrario, es Personal. Las entradas para algo que ocurre durante un viaje se añaden al viaje.

Si todavía falta para el viaje, tu Machine te indica qué falta, por ejemplo, **No hay alojamiento reservado para 2 noches** o que no has reservado cómo ir del aeropuerto al hotel. Estas líneas aparecen atenuadas y marcadas como **Sin reserva**. Si el viaje no incluye alojamiento, no se muestra información sobre las noches.

- Cada línea indica de quién procede la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo generó una tarea, como pagar las entradas, **Abrir la tarea** la muestra.
- Si cambia una reserva, se actualiza su línea. Si se cancela, desaparece. Cuando se cancelan todas las reservas, también desaparece el viaje o el evento.
- Las reservas de otras personas, como el vuelo de un compañero que te han reenviado, no aparecen en tus viajes.

La mayoría de las confirmaciones incluyen los detalles en un formato que tu Machine puede leer sin IA. Si alguna no está en ese formato, por ejemplo, un correo reenviado o de un sitio de reservas pequeño, tu [modelo](model.md) lee el correo en segundo plano, de unos pocos en pocos, y espera si estás cerca del límite de uso. Cuando tu Machine haya terminado de guardar el [historial](history.md) del año, también leerá en segundo plano los correos de reservas de ese año.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** recoge palabra por palabra lo que se dijo. Al principio aparece plegada y muestra cuánto dura. Toca **Mostrar** para abrirla.

Si no se cargan, se vuelven a cargar automáticamente durante aproximadamente medio minuto. Después, toca **Reintentar**.

Cada parte tiene sus propias opciones **Añadir notas** o **Añadir transcripción**, **Subir archivo** para subir un archivo Markdown o de texto, **Editar** y **Quitar** (toca dos veces). Lo que añadas a una parte se queda ahí. Si puedes cambiar la reunión, **Notas**, debajo del formulario, las abre.

Si has conectado [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), sus notas aparecen en **Notas** y su transcripción en **Transcripción**, marcadas como **De Zoom**, **De Google Meet** o **De Granola**. Nunca sustituyen lo que has añadido: si están las dos, se muestran las dos.

También pueden añadirse notas al evento de calendario de la propia reunión, una vez que haya empezado, o llegar por correo desde Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de ellas si indican claramente los siguientes pasos. Si llegan las mismas notas por dos medios, se crea una sola tarea y la reunión aparece como origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción, pero no notas, aparece la opción **Generar notas**. The Machine las redacta a partir de la transcripción: un breve resumen, decisiones y tareas pendientes con quién se encargará de ellas, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si la transcripción es larga, puede tardar unos minutos y se usa tu propio modelo. Las notas indican **Redactadas por The Machine** y nunca sustituyen las que hayas añadido.

También puedes pedirle a The Machine que las añada. Por ejemplo, en una tarea puedes decirle «añade esta transcripción a la reunión de equipo de hoy». La transcripción se añade a **Transcripción** y el resumen a **Notas**. En el **Calendario**, las reuniones que las tienen muestran **Notas** o **Transcripción**.

The Machine lee ambas para identificar tareas de seguimiento de la reunión. Son de Trabajo o Personales, igual que la reunión, y solo se comparten con tu equipo si la reunión también se comparte.

La reunión se abre con estos detalles estés donde estés: en una cronología, en una búsqueda de mensajes o como origen de una tarea. **Invitación original**, al final, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes cambiar tu propio calendario de Google. Outlook y otros calendarios solo se pueden consultar. **Nuevo evento** añade uno (en el móvil, está en **+**, en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento sin invitados de ese calendario para cambiarlo o para **Eliminarlo** (toca dos veces).

**Dónde** sugiere lugares a medida que escribes: primero los que has usado antes y tus organizaciones, y después direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige un lugar o deja el texto que has escrito.

**Invitar** te permite añadir personas de tu Graph o cualquier dirección de correo. Esta opción solo está disponible en tu propio calendario. Los invitados aparecen encima del botón, que indica cuántos hay: **Añadir e invitar a 2 personas**. Google envía las invitaciones cuando lo tocas, no antes. Si no hay invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede sugerir un cambio, como añadir una recogida. Verás exactamente qué cambiará. Solo se hará si tocas **Añadir**, **Guardar** o **Eliminar**.

¿Todavía no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre **Conexiones**. Desde ahí puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente. Puede redactar una nota breve para cambiarlo u ofrecerte la opción de rechazarlo. No se envía nada hasta que lo apruebes.

Los eventos de todo el día, los marcados como libre y los provisionales no cuentan. Cada conflicto aparece una sola vez. Las tareas de Trabajo solo indican que hay un conflicto, así que tu equipo nunca verá el evento personal. Solo tú puedes ver con qué entra en conflicto.

## Prepárate para tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Prepararte para** la reunión. Es un breve resumen:

- **Quién:** quiénes son, según tu Graph.
- **Último contacto:** tu último intercambio con esas personas. Ese mensaje aparece como origen de la tarea, después de la reunión.
- **Promesas pendientes:** lo que tú o esas personas aún tienen pendiente.
- **Preguntas pendientes:** lo que aún no tiene respuesta.
- **Decidir o llevar:** qué hay que decidir o llevar.

La tarea aparece la mañana de un día laborable: el mismo día de la reunión si es por la tarde, o el día laborable anterior si no. Solo usa información que ya está en tu Machine. Es solo para consultar: toca **Hecho** cuando la hayas leído. Si hay una promesa o pregunta que requiere hacer algo, tendrá su propia tarea.

Si no hay información útil en tu historial, no se crea ninguna tarea. Las reuniones recurrentes, internas, personales y rechazadas no generan tareas. Si cambia la hora de una reunión, su tarea se mantiene y se actualiza con la nueva hora. Si descartas una tarea, no vuelve a aparecer. La tarea de una reunión cancelada se cierra automáticamente.

Los detalles de la reunión muestran su tarea debajo de **Tarea**, a un solo toque de su chat.
