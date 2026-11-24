---
title: Calendario
area: calendar
summary: La semana que viene, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: d6f800709c378338
---
## Qué muestra

Tus días desde hoy, con:

- reuniones de los calendarios que has conectado,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos del trabajo que has pasado a otras personas,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de las reservas y entradas que recibes por correo.

Si una reunión aparece en dos calendarios, solo se muestra una vez. Los eventos de un calendario que alguien ha compartido contigo aparecen atenuados, con su nombre; nunca generan una tarea. Los eventos de todo el día y los que duran varios días aparecen como eventos de todo el día, en cada día que abarcan. En Agenda, un viaje aparece primero en cada uno de sus días. En Semana y Mes, aparece como una sola franja que ocupa todos esos días, como «Viaje a Lisboa».

Un plan acordado entre varias personas cuenta como una sola promesa, marcada con «Con» y el nombre de la otra persona. Si una promesa trata sobre una reunión de ese día con esa misma persona, aparece en la fila de la reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea pendiente, se muestra: **Preparación lista**, **Preparando** o **Tarea**. Las tareas que parecen estar hechas, porque ya has respondido o porque al ejecutarse se ha comprobado que ya estaban hechas, no aparecen como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes o hacia arriba, o pulsa **Mostrar días anteriores**, para ver los anteriores. Retrocede hasta una semana antes de que conectaras tu calendario; una línea en la parte superior indica desde qué día. Cuando se haya cargado el [historial](history.md), podrás retroceder aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil, muestra tres días.
- **Mes** muestra el mes completo. En un ordenador se muestran hasta tres elementos por día; en el móvil, puntos. Toca un día para ver su lista.

**Hoy**, ‹ y ›, en la parte superior, te permiten cambiar de semana o de mes. La vista que elijas se guarda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro y se pueden leer. Los demás se muestran como **+N**. Al pulsarlo, se abre ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa, el viaje o evento, o la reunión. Si no puedes modificar una reunión desde aquí, por ejemplo, porque pertenece a otra persona o tiene invitados, se muestran sus detalles: cuándo y dónde es, y quién asiste. Las personas que tu Graph conoce, y las organizaciones y proyectos de la reunión, enlazan a sus páginas. **Abrir en Google Calendar** o **Abrir en Outlook** abre la reunión en ese servicio. Consultarla no cambia nada.

Si una reunión tiene reservada una sala, aparece junto a la ubicación, nunca como persona ni en tu Graph.

El enlace de una reunión aparece con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes por correo una reserva de vuelo, hotel, alojamiento vacacional, tren, autobús, ferry, coche de alquiler, taxi o aparcamiento del aeropuerto, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un viaje, aunque estén en distintos buzones: el tren al aeropuerto, los vuelos, el coche, el alojamiento y el viaje de vuelta. Las reservas se agrupan cuando sus fechas coinciden o cuando una empieza justo al terminar la otra.

El viaje aparece como una franja que ocupa todos sus días. Ábrelo para ver cada reserva en orden, con sus horarios, dirección, código de reserva y asiento.

Las entradas para un concierto, partido, festival o congreso crean un evento, uno por cada evento, con su ubicación, código de reserva, asiento y número de entradas. Si haces un segundo pedido para el mismo evento, se añade al mismo. Si reservas el evento desde tu buzón de trabajo, es de trabajo; si no, es personal. Las entradas para algo que tiene lugar durante un viaje se añaden al viaje.

Si aún no has hecho un viaje, tu Machine indica qué falta, por ejemplo, **No hay alojamiento reservado para 2 noches** o que no tienes ningún transporte reservado del aeropuerto al hotel. Esos elementos aparecen atenuados y con la etiqueta **Sin reserva**. Si no hay ningún alojamiento reservado para el viaje, no se indica nada sobre las noches.

- Cada elemento indica de quién procede la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo ha generado una tarea, como pagar las entradas, **Abrir la tarea** la muestra.
- Si se modifica una reserva, se actualiza el elemento correspondiente; si se cancela, se elimina. Cuando se cancelan todas las reservas, también desaparece el viaje o evento.
- Las reservas de otras personas, como el vuelo de un compañero que te han reenviado, no aparecen en tus viajes.

La mayoría de las confirmaciones incluyen los detalles en un formato que tu Machine puede leer sin IA. Si no es así, como ocurre con un correo reenviado o una página de reservas pequeña, tu [modelo](model.md) lee el correo en segundo plano, de pocos en pocos, y espera si estás cerca del límite de uso. Cuando se carga el [historial](history.md), tu Machine lee en segundo plano los correos de reserva del año que conserva.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** recoge palabra por palabra lo que se dijo. Al principio aparece plegada y se indica su duración; **Mostrar** la abre.

Si no se carga, vuelve a intentarlo automáticamente durante aproximadamente medio minuto. Después, pulsa **Reintentar**.

Cada parte tiene su propio botón **Añadir notas** o **Añadir transcripción**, **Subir archivo** para subir un archivo Markdown o de texto, **Editar** y **Quitar** (pulsa dos veces). El contenido de una parte no se mezcla con el de la otra. En las reuniones que puedes modificar, **Notas**, debajo del formulario, las abre.

Si tienes conectado [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), sus notas aparecen en Notas y su transcripción en Transcripción, con la etiqueta **De Zoom**, **De Google Meet** o **De Granola**. Nunca reemplazan lo que has añadido: si están las dos, se muestran las dos.

También se pueden añadir notas al evento de calendario de la propia reunión, una vez que haya empezado, o recibirlas por correo de Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de ellas si contienen pasos siguientes claros. Si recibes las mismas notas de dos formas, se crea una sola tarea, con la reunión como origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción, pero no notas, aparece **Generar notas**. The Machine las redacta a partir de la transcripción: un resumen breve, decisiones y tareas pendientes con quién se encargará, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si es larga, puede tardar unos minutos y se usa tu propio modelo. Las notas indican **Escrito por The Machine** y nunca reemplazan las que has añadido.

También puedes pedirle a The Machine que las añada. Por ejemplo, en una tarea puedes pedirle «añade esta transcripción a la reunión de hoy del tablero». La transcripción va en Transcripción y el resumen, en Notas. En el Calendario, las reuniones que tienen contenido muestran **Notas** o **Transcripción**.

The Machine lee las dos partes para buscar seguimientos de la reunión. Se clasifican como de trabajo o personales, igual que la reunión, y solo se comparten con tu equipo si la reunión también se comparte con él.

Puedes abrir los detalles de una reunión desde cualquier lugar donde aparezca: en una cronología, en una búsqueda de mensajes o como origen de una tarea. **Invitación original**, en la parte inferior, muestra la invitación tal como la recibiste.

## Añadir o modificar un evento

Desde aquí puedes modificar tu propio calendario de Google. Outlook y los demás calendarios solo se pueden consultar. **Nuevo evento** añade uno (en el móvil, está bajo **+** en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento sin invitados de ese calendario para modificarlo o **Eliminar** (pulsa dos veces).

**Dónde** sugiere lugares mientras escribes: primero, los que has usado antes y tus organizaciones; después, direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige una sugerencia o conserva el texto que has escrito.

**Invitar** añade personas de tu Graph o cualquier dirección de correo. Esta opción solo aparece en tu propio calendario. Los invitados aparecen encima del botón, que indica cuántos son: **Añadir e invitar a 2 personas**. Google envía las invitaciones al pulsar el botón, no antes. Si no hay invitados, no se invita ni se avisa a nadie.

Una tarea también puede sugerir un cambio, como añadir una recogida. Te muestra exactamente qué va a cambiar, y solo se modifica si pulsas **Añadir**, **Guardar** o **Eliminar**.

¿Aún no tienes reuniones? Si no has conectado ningún calendario, **Conecta tu calendario** abre Conexiones, donde puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente. Puede redactar una nota breve para cambiarlo u ofrecerse a rechazarlo. No se envía nada hasta que lo apruebes.

Los eventos de todo el día, los que indican que estás libre y los provisionales no cuentan. Cada conflicto se muestra una sola vez. Una tarea de trabajo solo indica que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú puedes ver con qué evento coincide.

## Preparación de tus reuniones

Antes de una reunión con personas de fuera de tu empresa, The Machine crea una tarea: **Preparar reunión**. Es un breve resumen:

- **Quién:** quiénes son, según tu Graph, y algún dato de su trayectoria si se conoce.
- **Organización:** a qué se dedica su empresa, para quién y a qué precio, si es relevante para la reunión.
- **Hasta ahora:** qué habéis hablado, preguntado y ofrecido, y en qué punto está todo. Después de la reunión, esos mensajes aparecen como fuentes de la tarea.
- **Acordado antes:**, **Cambios desde entonces:** y **Aún pendiente:** lo que surgió en reuniones anteriores con las mismas personas. Cada elemento incluye la reunión o el mensaje del que procede.
- **Promesas pendientes:** lo que tú o esas personas aún tenéis pendiente, según las promesas de tu Machine.
- **Preguntas pendientes:** lo que aún no tiene respuesta.
- **Decisiones y preparativos:** qué hay que decidir o llevar, y qué les interesará probablemente.

La tarea aparece por la mañana de un día laborable: el mismo día de la reunión si es por la tarde; si no, el día laborable anterior. Solo sirve para consultar: cuando la hayas leído, pulsa **Hecho**. Si incluye una promesa o pregunta que requiere una acción, tendrá su propia tarea.

Se tienen en cuenta las reuniones anteriores en las que haya participado alguien de fuera, independientemente del nombre de la reunión y de la dirección que haya usado. Se leen las notas que tiene tu Machine: las tuyas, las de la aplicación de reuniones o las que te han enviado por correo. Si no hay notas, se usa la transcripción o las notas del evento del calendario. Las más recientes tienen más peso y no se muestran como pendientes los temas que se hayan resuelto después.

También se tienen en cuenta las notas y los mensajes del [Historial](history.md), para que el resumen incluya reuniones anteriores a tu llegada.

El resumen de una reunión de trabajo no lee notas personales ni contenido de la Machine de otra persona. El texto es solo para ti: no se incluye al pasar una tarea a otra persona y no se puede enviar para revisión. Si no hay notas, esos apartados no aparecen.

Se usa lo que ya hay en tu Machine. Para una primera reunión con alguien de una empresa, también se consulta la página de inicio de la web de la empresa.

Si hay un proveedor de búsqueda web configurado en OpenClaw (las Machines alojadas no incluyen uno), también se hace una búsqueda breve en internet sobre el nombre y la empresa de esa persona. Los resultados incluyen un enlace. Solo se envían a la búsqueda su nombre público, el nombre de la empresa y el sitio web, nunca tus mensajes. Los resultados se reutilizan durante 30 días.

Así, puedes recibir un resumen antes de intercambiar una sola palabra con alguien con quien acabas de aceptar una primera reunión: a qué se dedica su empresa, qué implica para ti y, si se sabe, quién es. Si solo se conoce su nombre de pila, los resultados se guardan únicamente si apuntan a una sola persona. Si desactivas **Buscar contactos de trabajo** (Ajustes, Seguridad), no se busca nada.

Si una reunión se repite, solo se crea un resumen cuando hay novedades desde la última vez: un mensaje, notas o una promesa. Indica qué hay de nuevo, no lo que decía el resumen anterior. Se crea cuando termina la reunión anterior, como máximo para dos reuniones recurrentes al día.

Si no hay nada útil que añadir, no se crea ninguna tarea. Las reuniones internas, personales y rechazadas no generan tareas. Si se cambia la hora de una reunión, conserva su tarea, con la nueva hora. Si descartas una tarea, no vuelve a aparecer. Si se cancela una reunión, su tarea se cierra automáticamente.

Si una actualización modifica el contenido de un resumen, los resúmenes de las reuniones que aún no han tenido lugar se vuelven a redactar una vez con la información nueva. Conservan el título, las fuentes y el lugar que ocupan en tu lista. Los que hayas modificado, pospuesto o cerrado no cambian. Tampoco cambia el de una reunión que empieza dentro de unos minutos.

Los detalles de la reunión muestran su tarea bajo **Tarea**. Tócala para abrir su chat.
