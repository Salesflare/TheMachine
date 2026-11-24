---
title: Calendario
area: calendar
summary: La semana que tienes por delante, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9f38e3718f3e8639
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que has conectado,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos del trabajo que has delegado,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de las reservas y entradas que recibes por correo.

Una reunión que aparece en dos calendarios solo se muestra una vez. Los eventos de un calendario que alguien ha compartido contigo aparecen atenuados y con el nombre de pila de esa persona; nunca generan una tarea. Los eventos de todo el día y los que duran varios días aparecen como eventos de todo el día en cada uno de los días que abarcan. En Agenda, un viaje aparece primero en cada uno de sus días; en Semana y Mes, aparece como una sola franja que los abarca, por ejemplo, «Viaje a Lisboa».

Un plan que hacéis juntos cuenta como una sola promesa, marcada «Con» y el nombre de la otra persona. Si una promesa es sobre una reunión de ese día con esa misma persona, aparece en la fila de la reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea abierta, se muestra como **Preparación lista**, **Preparando** o **Tarea**. Las tareas que parecen hechas, porque ya has respondido o porque una ejecución las ha marcado como hechas, no aparecen como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes o hacia arriba, o pulsa **Mostrar días anteriores**, para ver los anteriores. Retrocede hasta una semana antes de que conectaras el calendario y muestra arriba una línea que indica desde qué día. Cuando se haya cargado el [historial](history.md), retrocede aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil, muestra tres días.
- **Mes** muestra el mes entero. En el ordenador se muestran hasta tres elementos por día; en el móvil aparecen puntos y, al tocar uno, se muestra la lista de ese día.

**Hoy**, ‹ y ›, en la parte superior, te permiten avanzar o retroceder por las semanas o los meses. La vista que elijas se recuerda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro, sin perder legibilidad. Los demás se muestran como **+N**; al pulsarlo, se abre ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa, el viaje o evento, o la reunión. Si no puedes modificar una reunión desde aquí, por ejemplo, porque pertenece a otra persona o tiene invitados, se muestran sus detalles: cuándo, dónde y quiénes asisten. Las personas que conoce tu Graph y las organizaciones y proyectos a los que pertenece la reunión enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**) te lleva al evento correspondiente. Consultarlo no cambia nada.

Si hay una sala reservada para una reunión, aparece en el apartado «Dónde», nunca como persona ni en tu Graph.

Los enlaces a reuniones aparecen con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes por correo una reserva de vuelo, hotel, casa de vacaciones, tren, autobús, ferry, coche de alquiler, taxi o aparcamiento en el aeropuerto, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un solo viaje, sin importar en cuál de tus buzones lleguen: el tren al aeropuerto, los vuelos, el coche, el alojamiento y el viaje de vuelta. Las reservas se agrupan cuando sus fechas coinciden o cuando una empieza justo al terminar la otra.

El viaje aparece como una sola franja que abarca todos sus días. Ábrelo para ver cada reserva en orden cronológico, con sus horarios, dirección, código de reserva y asiento.

Las entradas para un concierto, un partido, un festival o una conferencia crean un evento, uno por cada evento, con el lugar, el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade al mismo. Si reservas las entradas desde tu buzón de trabajo, el evento es de trabajo; de lo contrario, es personal. Las entradas para algo que ocurre durante un viaje se añaden al viaje.

Si un viaje aún no ha empezado, tu Machine te indica qué falta, por ejemplo, **No hay alojamiento reservado para 2 noches** o que no hay ningún transporte reservado del aeropuerto al hotel. Esas líneas aparecen atenuadas y marcadas como **Sin reserva**. Si el viaje no tiene ningún alojamiento, no se indica nada sobre las noches.

- Cada línea indica de quién procede la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si del correo se ha creado una tarea, por ejemplo, para pagar las entradas, **Abrir la tarea** la muestra.
- Si se modifica una reserva, se actualiza su línea; si se cancela, desaparece. Cuando se cancelan todas las reservas, también desaparece el viaje o el evento.
- Las reservas de otras personas, como el vuelo de un compañero que te han reenviado, no aparecen en tus viajes.

La mayoría de las confirmaciones incluyen los datos en un formato que tu Machine puede leer sin IA. Si alguna no está en ese formato, como un correo reenviado o de una web de reservas pequeña, tu [modelo](model.md) lee el correo en segundo plano, de unos pocos en unos pocos, y espera si estás cerca del límite de uso. Los correos de reservas del año que tu Machine conserva en el [historial](history.md) se leen en segundo plano cuando el historial ya está cargado.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** recoge palabra por palabra lo que se dijo. Al principio está contraída y muestra su duración; pulsa **Mostrar** para abrirla.

Si no se carga, vuelve a intentarlo automáticamente durante aproximadamente medio minuto. Después, pulsa **Reintentar**.

Cada parte tiene sus propias opciones: **Añadir notas** o **Añadir transcripción**, **Subir archivo** para subir un archivo Markdown o de texto, **Editar** y **Quitar** (toca dos veces). Lo que añadas a una parte se queda ahí. En las reuniones que puedes modificar, **Notas**, debajo del formulario, las abre.

Si has conectado [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), sus notas aparecen en Notas y su transcripción en Transcripción, marcadas como **De Zoom**, **De Google Meet** o **De Granola**. Nunca sustituyen lo que has añadido: si están las dos, se muestran las dos.

También puedes recibir notas en el propio evento de calendario de la reunión, añadidas después de que empiece, o por correo desde Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de las notas si incluyen pasos siguientes claros. Si las mismas notas llegan por dos vías, se crea una sola tarea y la reunión aparece como origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción pero no notas, aparece la opción **Generar notas**. The Machine las redacta a partir de la transcripción: un breve resumen, las decisiones y las tareas pendientes, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Una reunión larga puede tardar unos minutos y usa tu propio modelo. Las notas indican **Escrito por The Machine** y nunca sustituyen las que has añadido.

The Machine también puede añadirlas. Pídeselo en una tarea, por ejemplo: «añade esta transcripción a la reunión de hoy del equipo». La transcripción se añade a Transcripción y el resumen, a Notas. En el Calendario, las reuniones que tienen notas o transcripción muestran **Notas** o **Transcripción**.

The Machine lee ambas para encontrar tareas de seguimiento de la reunión. Son de trabajo o personales según la reunión, y solo se comparten con tu equipo si la reunión también se comparte con él.

La reunión se abre con estos detalles desde cualquier lugar donde la encuentres: en una cronología, en una búsqueda de mensajes o como origen de una tarea. **Invitación original**, en la parte inferior, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes modificar tu propio calendario de Google. Outlook y otros calendarios solo se muestran. **Nuevo evento** añade uno (en el móvil, está bajo **+** en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento de ese calendario que no tenga invitados para modificarlo o **Eliminar** (toca dos veces).

**Dónde** sugiere lugares a medida que escribes: primero los que has usado antes y tus organizaciones, y luego direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige una sugerencia o conserva el texto que has escrito.

**Invitar** añade personas de tu Graph o cualquier dirección de correo. Esta opción solo aparece en tu propio calendario. Encima del botón se indica quién recibirá una invitación y el botón muestra cuántas personas son: **Añadir e invitar a 2**. Google envía las invitaciones cuando lo pulsas, no antes. Si no hay invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede ofrecerte un cambio, como añadir una recogida. Te muestra exactamente qué va a cambiar; el cambio solo se aplica si pulsas **Añadir**, **Guardar** o **Eliminar**.

¿Aún no tienes reuniones? Si no tienes ningún calendario conectado, **Conecta tu calendario** abre Conexiones, donde puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre la reunión más reciente de las dos. Puede redactar una nota breve para cambiarla de hora u ofrecerte cancelarla. No se envía nada hasta que lo apruebes.

Los eventos de todo el día, los que aparecen como libre y los provisionales no cuentan. Cada conflicto aparece una sola vez. Las tareas de trabajo solo indican que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú puedes ver con qué coincide.

## Prepárate para tus reuniones

Antes de una reunión con personas de fuera de tu empresa, The Machine crea una tarea: **Prepárate para** la reunión. Es un breve resumen:

- **Quién:** quiénes son, según tu Graph, con información sobre su trayectoria si se conoce.
- **Organización:** a qué se dedica su empresa y qué tiene que ver con la reunión.
- **Hasta ahora:** qué habéis hablado, preguntado y ofrecido, y en qué punto está todo. Esos mensajes pasan a ser el origen de la tarea después de la reunión.
- **Promesas pendientes:** qué os debéis aún tú o esas personas, según las promesas de tu Machine.
- **Preguntas pendientes:** qué sigue sin respuesta.
- **Decidir o llevar:** qué hay que decidir o llevar, y qué les interesará probablemente.

La tarea llega la mañana de un día laborable: el mismo día de la reunión si es por la tarde; de lo contrario, el día laborable anterior. Solo tienes que leerla: cuando la hayas leído, pulsa **Hecho**. Las promesas o preguntas que requieran alguna acción tienen su propia tarea.

Usa la información que ya está en tu Machine. Para una primera reunión con alguien de una empresa, también hace una búsqueda breve en la web con el nombre de esa persona y de su empresa, y muestra un enlace junto a lo que encuentra. La búsqueda solo incluye su nombre público, el nombre de la empresa y su sitio web, nunca tus mensajes. Los resultados de la búsqueda se reutilizan durante 30 días. Si desactivas **Buscar contactos de trabajo** en Ajustes, Seguridad, no se hacen búsquedas.

Si no hay información útil del historial, no se crea ninguna tarea. Las reuniones recurrentes, internas, personales o rechazadas no generan tareas. Si se cambia la hora de una reunión, se conserva la misma tarea y se actualiza la hora. Si descartas una tarea, no vuelve a aparecer; si se cancela la reunión, la tarea se cierra automáticamente.

Si una actualización cambia el contenido del resumen, los resúmenes de las reuniones que aún no han ocurrido se redactan de nuevo una vez, con la información actualizada. Conservan el título, el origen y el lugar que ocupan en la lista. Los resúmenes que hayas modificado, pospuesto o cerrado no cambian. Tampoco cambia el de una reunión que empieza en los próximos minutos.

Los detalles de la reunión muestran su tarea bajo **Tarea**, a un toque de su chat.
