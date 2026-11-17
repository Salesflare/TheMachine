---
title: Calendario
area: calendar
summary: La semana que viene, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 24033419578a8c8f
---
## Qué muestra

Tus días desde hoy, con:

- reuniones de los calendarios que conectaste,
- tareas que vencen ese día y tareas pospuestas el día que vuelven,
- seguimientos de tareas que delegaste,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de las reservas y entradas que recibes por correo.

Una reunión que aparece en dos calendarios solo se muestra una vez. Los eventos de un calendario que alguien compartió contigo aparecen atenuados, con el nombre de pila de esa persona; nunca generan una tarea. Los eventos de todo el día y de varios días aparecen como eventos de todo el día en cada uno de los días que abarcan. En Agenda, un viaje aparece primero en cada uno de sus días; en Semana y Mes, aparece como una sola franja que abarca todos esos días, por ejemplo, «Viaje a Lisboa».

Un plan hecho en conjunto es una sola promesa, marcada como «Con» y el nombre de la otra persona. Si una promesa trata de una reunión de ese día con la misma persona, aparece en la fila de la reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea pendiente, aparece: **Preparación lista**, **Preparando** o **Tarea**. Una tarea que parece hecha (porque ya respondiste o porque al ejecutarse se marcó como hecha) no aparece como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes, o hacia arriba (o toca **Mostrar días anteriores**) para ver los anteriores. Retrocede hasta una semana antes de que conectaras tu calendario; en la parte superior aparece una línea que indica desde qué día. Cuando esté disponible el [historial](history.md), podrás retroceder aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el teléfono se muestran tres días.
- **Mes** muestra el mes entero. En la computadora se muestran hasta tres elementos por día; en el teléfono aparecen puntos y, al tocar uno, se muestra la lista de ese día.

**Hoy**, ‹ y ›, en la parte superior, te permiten moverte entre semanas o meses. La vista que elijas se recordará en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro para que se puedan leer. Los demás aparecen como **+N**; tócalo para abrir ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa, el viaje o evento, o la reunión. Si no puedes cambiar una reunión desde aquí, por ejemplo, porque pertenece a otra persona o tiene invitados, verás sus detalles: cuándo, dónde y quiénes asisten. Las personas que conoce tu Graph, así como las organizaciones y los proyectos relacionados con la reunión, enlazan a sus páginas. Al hacer clic en **Abrir en Google Calendar** (o **Abrir en Outlook**), se abrirá allí. Consultar la reunión no cambia nada.

Si una reunión tiene una sala reservada, esta aparece debajo de dónde, nunca como una persona ni en tu Graph.

El enlace de una reunión muestra el servicio correspondiente, como Zoom, Google Meet o Teams, o aparece como **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes por correo una reserva de vuelo, hotel, alojamiento vacacional, tren, autobús, ferry, coche de alquiler, taxi o aparcamiento en el aeropuerto, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un solo viaje, sin importar en cuál de tus bandejas de correo lleguen: el tren al aeropuerto, los vuelos, el coche, el alojamiento y el viaje de vuelta. Las reservas se agrupan si coinciden en fechas o si una empieza cuando termina la otra.

El viaje aparece como una sola franja que abarca todos sus días. Ábrelo para ver cada reserva en orden cronológico, con sus horarios, dirección, código de reserva y asiento.

Las entradas para un concierto, un partido, un festival o una conferencia crean un evento, uno por cada evento, con el lugar, el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade al que ya existe. Un evento reservado en tu correo de trabajo se marca como Work; de lo contrario, como Personal. Las entradas para eventos durante un viaje se añaden al viaje.

Si aún falta para el viaje, tu Machine te indica qué falta, por ejemplo, **No hay alojamiento reservado para 2 noches**, o que no hay ninguna reserva para ir del aeropuerto al hotel. Esas líneas aparecen atenuadas y marcadas como **Sin reserva**. Si el viaje no tiene ningún alojamiento, no se muestra información sobre las noches.

- Cada línea indica de quién procede la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo generó una tarea, como pagar las entradas, **Abrir la tarea** la muestra.
- Si se modifica una reserva, se actualiza su línea; si se cancela, desaparece. Cuando se cancelan todas las reservas, también desaparece el viaje o evento.
- Las reservas de otras personas, como el vuelo de un compañero que te reenvían, no aparecen en tus viajes.

La mayoría de las confirmaciones incluyen los detalles en un formato que tu Machine puede leer sin IA. Si alguna no lo incluye, como un correo reenviado o de un sitio de reservas pequeño, tu [modelo](model.md) lee el correo en segundo plano, de unos pocos en unos pocos, y espera si estás cerca del límite de uso. Cuando se incorpora el [historial](history.md), tu Machine lee en segundo plano los correos de reservas del año que conserva.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** es lo que se dijo, palabra por palabra. Al principio aparece plegada, junto con su duración; **Mostrar** la despliega.

Si no se cargan, se vuelven a intentar cargar automáticamente durante aproximadamente medio minuto. Después, toca **Reintentar**.

Cada parte tiene sus propias opciones: **Añadir notas** o **Añadir transcripción**, **Subir archivo** para un archivo Markdown o de texto, **Editar** y **Quitar** (toca dos veces). El contenido de una parte se queda en esa parte. En las reuniones que puedes cambiar, **Notas**, debajo del formulario, las abre.

Si conectaste [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), sus notas aparecen en Notas y su transcripción en Transcripción, marcadas como **De Zoom**, **De Google Meet** o **De Granola**. Nunca reemplazan lo que añadiste: si están las dos, se muestran las dos.

También se pueden añadir notas al evento de calendario de la reunión, una vez que haya empezado, o enviarlas por correo desde Zoom o Gemini. Cuando termina la reunión, The Machine crea tareas a partir de ellas solo si hay pasos siguientes claros. Si las mismas notas llegan por dos vías, se crea una sola tarea, cuya fuente es la reunión: «Fuente: notas de» la reunión.

Si una reunión tiene transcripción, pero no notas, aparece **Generar notas**. The Machine las redacta a partir de la transcripción: un resumen breve, las decisiones y las tareas pendientes con la persona responsable, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si es larga, puede tardar unos minutos y utiliza tu propio modelo. Las notas indican **Redactado por The Machine** y nunca reemplazan las que añadiste.

The Machine también puede añadirlas. Pídeselo en una tarea, por ejemplo: «añade esta transcripción a la reunión de hoy de la junta». La transcripción se añade a Transcripción y el resumen, a Notas. En el Calendario, las reuniones que las incluyen muestran **Notas** o **Transcripción**.

The Machine lee las dos para encontrar las tareas de seguimiento de la reunión. Son Work o Personal, igual que la reunión, y solo se comparten con tu equipo si la reunión también se comparte con él.

La reunión se abre con estos detalles desde cualquier lugar donde la encuentres: en una cronología, en una búsqueda de mensajes o como fuente de una tarea. **Invitación original**, en la parte inferior, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes cambiar tu propio calendario de Google. Outlook y otros calendarios solo se pueden consultar. **Nuevo evento** añade uno (en el teléfono, está bajo **+**, en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento de ese calendario que no tenga invitados para cambiarlo o **Eliminar** (toca dos veces).

**Dónde** sugiere lugares a medida que escribes: primero, los que usaste antes y tus organizaciones; después, direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige una sugerencia o conserva tu propio texto.

**Invitar** añade personas de tu Graph o cualquier dirección de correo electrónico. Esta opción solo aparece en tu propio calendario. Encima del botón se indica quién recibirá una invitación, y el botón muestra cuántas personas son: **Añadir e invitar a 2**. Google envía las invitaciones cuando lo tocas, no antes. Si no hay invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede sugerir un cambio, como añadir una recogida. Te muestra exactamente qué va a cambiar; el cambio solo se aplica si tocas **Añadir**, **Guardar** o **Eliminar**.

¿Todavía no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre Conexiones, donde puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una sola tarea sobre el evento más reciente. Puede redactar una nota breve para cambiarlo u ofrecerte rechazarlo. No se envía nada hasta que lo apruebes.

Los eventos de todo el día, los que aparecen como libre y los provisionales nunca cuentan, y cada conflicto aparece una sola vez. Una tarea de Work solo indica que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú ves con qué coincide.

## Prepárate para tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Preparar la reunión**. Es un resumen breve:

- **Quién:** quiénes son, según tu Graph, con información de su trayectoria si se conoce.
- **Organización:** a qué se dedica su empresa y por qué es relevante para la reunión.
- **Hasta ahora:** qué hablaron, qué preguntaron y qué ofrecieron, y en qué punto está todo. Después de la reunión, esos mensajes aparecen como fuentes de la tarea.
- **Promesas pendientes:** qué os debéis tú y la otra persona.
- **Preguntas pendientes:** qué sigue sin respuesta.
- **Decisiones o cosas que llevar:** qué hay que decidir o llevar, y qué probablemente les interese.

La tarea aparece la mañana de un día laborable: el mismo día de la reunión si es por la tarde; si no, el día laborable anterior. Solo sirve para consultar: toca **Hecho** cuando la hayas leído. Si incluye una promesa o pregunta que requiere una acción, esta tiene su propia tarea.

Usa la información que ya está en tu Machine. Para una primera reunión con alguien de una empresa, también hace una búsqueda breve en la web con el nombre de la persona y el de la empresa, y muestra un enlace junto a lo que encuentre. En la búsqueda solo se usan el nombre público de esa persona, el nombre de la empresa y su sitio web, nunca tus mensajes. Los resultados de la búsqueda se reutilizan durante 30 días. Si desactivas **Buscar contactos de trabajo** (Ajustes, Seguridad), no se hace ninguna búsqueda.

Si no hay información útil del historial, no se crea ninguna tarea. Las reuniones periódicas, internas, personales y rechazadas no generan ninguna. Si se cambia la hora de una reunión, conserva su única tarea, pero con la nueva hora. Una tarea descartada no vuelve a aparecer, y la tarea de una reunión cancelada se cierra automáticamente.

Si una actualización cambia el contenido de un resumen, los resúmenes de las reuniones que aún no han ocurrido se redactan de nuevo una sola vez, con la información actualizada. El título, las fuentes y el lugar que ocupan en tu lista no cambian. Los que hayas modificado, pospuesto o cerrado se mantienen igual, al igual que los de reuniones que empiezan en los próximos minutos.

Los detalles de la reunión muestran su tarea debajo de **Tarea**; tócala una vez para abrir su chat.
