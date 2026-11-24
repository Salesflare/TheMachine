---
title: Calendario
area: calendar
summary: La semana que tienes por delante, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: f3f41306aad03084
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que has conectado,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos del trabajo que has pasado a otras personas,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de las reservas y entradas que recibes por correo.

Si una reunión está en dos calendarios, solo aparece una vez. Los eventos de un calendario que alguien ha compartido contigo aparecen atenuados y con el nombre de pila de esa persona. Nunca generan tareas. Los eventos de todo el día y los que duran varios días aparecen como eventos de todo el día en cada uno de los días que abarcan. En Agenda, un viaje aparece primero cada uno de sus días. En Semana y Mes, aparece como una sola franja que abarca esos días, por ejemplo, «Viaje a Lisboa».

Un plan que hacéis juntos cuenta como una sola promesa, marcada como «Con» y con el nombre de la otra persona. Si una promesa es sobre una reunión de ese día con esa misma persona, aparece en la fila de la reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea pendiente, se muestra: **Preparación lista**, **Preparando** o **Tarea**. Una tarea que parece completada, porque ya has respondido o porque la ejecución la encontró hecha, no aparece como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes o hacia arriba, o pulsa **Mostrar días anteriores**, para ver los anteriores. Llega hasta una semana antes de que conectaras tu calendario e indica arriba desde qué día empieza. Cuando se haya cargado su [historial](history.md), llega aproximadamente hasta un año atrás.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil muestra tres días.
- **Mes** muestra el mes entero. En un ordenador se muestran hasta tres elementos por día; en el móvil aparecen puntos y, al tocarlos, se muestra la lista de ese día.

**Hoy**, ‹ y ›, en la parte superior, te permiten avanzar o retroceder por las semanas o los meses. La vista que elijas se recuerda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en hora aparecen uno al lado del otro y se pueden leer. El resto aparece como **+N**. Al pulsarlo, se abre ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa, el viaje o evento, o la reunión. Si no puedes cambiar una reunión desde aquí, por ejemplo, porque es de otra persona o tiene invitados, verás sus detalles: cuándo, dónde y quiénes asisten. Las personas que conoce tu Graph, así como las organizaciones y los proyectos de la reunión, enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**) debajo de esos datos abre el evento allí. Consultarlo no cambia nada.

Si se ha reservado una sala para la reunión, aparece en el campo del lugar, nunca como persona ni en tu Graph.

El enlace de una reunión aparece con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes por correo una reserva de vuelo, hotel, casa vacacional, tren, autobús, ferry, coche de alquiler, taxi o aparcamiento en el aeropuerto, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un viaje, aunque lleguen a cualquiera de tus buzones: el tren al aeropuerto, los vuelos, el coche, el alojamiento y el trayecto de vuelta. Las reservas se agrupan cuando coinciden en fechas o cuando una empieza al terminar la otra.

El viaje aparece como una sola franja que abarca sus días. Ábrelo para ver cada reserva en orden cronológico, con sus horarios, dirección, código de reserva y asiento.

Las entradas para un concierto, un partido, un festival o una conferencia crean un evento, uno por cada evento, con el lugar, el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade al mismo. Los eventos reservados desde tu buzón de trabajo son de Trabajo. Los demás son personales. Las entradas para algo que ocurre durante un viaje se añaden al viaje.

Si aún falta para el viaje, tu Machine indica qué falta, por ejemplo, **No hay alojamiento reservado para 2 noches** o que no hay nada reservado para ir del aeropuerto al hotel. Esas líneas aparecen atenuadas y marcadas como **Sin reserva**. Si el viaje no incluye ningún alojamiento, no se indica nada sobre las noches.

- Cada línea indica de quién procede la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo ha generado una tarea, como pagar las entradas, **Abrir la tarea** la muestra.
- Si se modifica una reserva, se actualiza su línea. Si se cancela, desaparece. Cuando se cancelan todas las reservas, también desaparece el viaje o el evento.
- Las reservas de otras personas, como el vuelo de un compañero que te han reenviado, no se añaden a tus viajes.

La mayoría de las confirmaciones incluyen los datos en un formato que tu Machine puede leer sin IA. Si no es así, por ejemplo, si se trata de un correo reenviado o de una web de reservas pequeña, tu [modelo](model.md) lee el correo en segundo plano, de unos pocos en unos pocos, y espera cuando estás cerca del límite de uso. Los correos de reservas del año que tu Machine conserva en el [historial](history.md) se leen en segundo plano cuando se ha cargado ese historial.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** es lo que se dijo, palabra por palabra. Al principio aparece plegada junto con su duración. Pulsa **Mostrar** para abrirla.

Si no se carga, vuelve a intentarlo automáticamente durante aproximadamente medio minuto. Después, pulsa **Reintentar**.

Cada parte tiene sus propias opciones **Añadir notas** o **Añadir transcripción**, **Subir archivo** para subir un archivo Markdown o de texto, **Editar** y **Quitar** (pulsa dos veces). El contenido que añadas a una parte se queda ahí. En una reunión que puedes modificar, abre las notas con **Notas**, debajo del formulario.

Si conectas [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), sus notas aparecen en Notas y su transcripción en Transcripción, con las etiquetas **De Zoom**, **De Google Meet** o **De Granola**. Nunca sustituyen lo que has añadido: si están las dos, se muestran las dos.

También pueden añadirse notas al evento de calendario de la propia reunión, después de que empiece, o por correo desde Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de ellas si incluyen pasos siguientes claros. Si las mismas notas llegan por dos vías, se crea una sola tarea y la reunión aparece como origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción pero no notas, aparece la opción **Generar notas**. The Machine las redacta a partir de la transcripción: un breve resumen, las decisiones y las tareas pendientes, con la persona responsable de cada una, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si la reunión es larga, puede tardar unos minutos y se usa tu propio modelo. Las notas indican **Redactado por The Machine** y nunca sustituyen las que hayas añadido.

También puedes pedirle a The Machine que las añada. Por ejemplo, desde una tarea, puedes decirle «añade esta transcripción a la reunión de hoy del equipo». La transcripción se añade a Transcripción y el resumen, a Notas. En el Calendario, las reuniones con notas o transcripción muestran **Notas** o **Transcripción**.

The Machine lee ambas para encontrar los seguimientos de la reunión. Son de Trabajo o personales, igual que la reunión, y solo se comparten con tu equipo si la reunión también se comparte con él.

La reunión se abre con estos detalles desde cualquier lugar donde la encuentres: en una cronología, en una búsqueda de mensajes o como origen de una tarea. **Invitación original**, al final, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes modificar tu propio calendario de Google. Outlook y los demás calendarios solo se pueden consultar. **Nuevo evento** añade uno (en el móvil está en **+**, en la barra superior): elige el calendario, el título y la hora. Haz clic en un evento sin invitados de ese calendario para modificarlo o **Eliminar** (pulsa dos veces).

Al escribir en **Dónde**, se sugieren lugares: primero los que has usado antes y los de tus organizaciones; después, direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlos. Elige una sugerencia o deja el texto que has escrito.

**Invitar** añade personas de tu Graph o cualquier dirección de correo. Esta opción solo está disponible en tu propio calendario. Encima del botón se muestran las personas que recibirán una invitación y el botón indica cuántas son: **Añadir e invitar a 2 personas**. Google envía las invitaciones al pulsar el botón, no antes. Si no hay invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede sugerir un cambio, como añadir una recogida. Muestra exactamente qué cambiaría. Solo se aplica si pulsas **Añadir**, **Guardar** o **Eliminar**.

¿Aún no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre Conexiones, donde puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente de los dos. Puede redactar una nota breve para proponer otro horario o sugerir que lo rechaces. No se envía nada hasta que des el visto bueno.

Los eventos de todo el día, los que indican que estás disponible y los provisionales no cuentan. Cada conflicto se muestra una sola vez. Una tarea de Trabajo solo indica que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú puedes ver con qué coincide.

## Prepárate para tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Prepárate para** la reunión. Es un breve resumen:

- **Quién:** quiénes son, según tu Graph, y algunos datos sobre su trayectoria si se conocen.
- **Organización:** a qué se dedica su empresa, para quién y a qué precio, si es relevante para la reunión.
- **Hasta ahora:** qué habéis hablado, preguntado y ofrecido, y en qué punto estáis. Después de la reunión, esos mensajes aparecen como origen de la tarea.
- **Acordado anteriormente:**, **Cambios desde entonces:** y **Aún pendiente:** qué surgió en reuniones anteriores con esas mismas personas, con una referencia a la reunión o el mensaje de donde procede cada elemento.
- **Promesas pendientes:** qué te queda por hacer a ti o a las otras personas, según las promesas de tu Machine.
- **Preguntas pendientes:** qué preguntas siguen sin respuesta.
- **Decidir o llevar:** qué hay que decidir o llevar, y qué les interesará probablemente.

La tarea aparece por la mañana de un día laborable: el mismo día de la reunión si es por la tarde o, si no, el día laborable anterior. Es solo para consultar: pulsa **Hecho** cuando la hayas leído. Si incluye una promesa o una pregunta que requiere una acción, esta tiene su propia tarea.

Se tienen en cuenta las reuniones anteriores en las que participe alguien ajeno a tu empresa y que también esté en la reunión actual, sin importar cómo se llamara la reunión ni qué dirección usara esa persona. The Machine lee las notas que tiene tu Machine: las tuyas, las de la aplicación de reuniones o las que te hayan enviado por correo. Si no hay, lee la transcripción o las notas del evento de calendario. Las más recientes tienen más peso, y los asuntos resueltos más adelante no aparecen como pendientes.

También se tienen en cuenta las notas y los mensajes del [Historial](history.md), para que el resumen incluya reuniones anteriores a tu incorporación.

Un resumen de trabajo no lee notas personales ni nada de la Machine de otra persona. El texto se queda contigo: no se incluye al hacer un traspaso y no se puede enviar para que lo revisen. Si no hay notas, no aparecen esas líneas.

Se usa lo que ya hay en tu Machine. Para una primera reunión con alguien de una empresa, también se consulta la página de inicio del sitio web de la empresa.

Si la búsqueda web está configurada en tu Machine, también se hace una búsqueda breve en la web sobre el nombre de la persona y su empresa. Las Machine alojadas no incluyen esta función. En tu propio ordenador, puedes configurarla en OpenClaw. Los resultados incluyen un enlace. Para la búsqueda solo se envían el nombre público de la persona, el nombre de la empresa y su sitio web, nunca tus mensajes. Los resultados se reutilizan durante 30 días.

Así, puedes obtener un resumen para una primera reunión que hayas aceptado antes de haber intercambiado una sola palabra: a qué se dedica su empresa, qué significa eso para ti y, si se sabe, quiénes son. Si solo tienes el nombre de pila, los resultados se guardan únicamente si apuntan a una sola persona. Si **Buscar contactos de trabajo** está desactivado (Ajustes, Seguridad), no se busca nada.

Las reuniones recurrentes solo generan un resumen si hay novedades desde la última vez: un mensaje, notas o una promesa. El resumen indica las novedades, no repite el anterior. Aparece cuando termina la reunión anterior, como máximo para dos reuniones recurrentes al día.

Si no hay nada útil que decir, no se crea ninguna tarea. Las reuniones internas, personales o rechazadas no generan ninguna. Si una reunión cambia de hora, conserva la misma tarea, pero con la nueva hora. Una tarea descartada no vuelve a aparecer, y la tarea de una reunión cancelada se cierra automáticamente.

Si una actualización cambia el contenido de un resumen, los resúmenes de las reuniones que aún no han tenido lugar se vuelven a redactar una vez con la información nueva. Se mantienen el título, los orígenes y el lugar en la lista. Los resúmenes que hayas modificado, pospuesto o cerrado no cambian. Tampoco cambia el de una reunión que vaya a empezar en los próximos minutos.

Los detalles de la reunión muestran su tarea en **Tarea**, a un toque de su chat.
