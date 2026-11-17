---
title: Calendario
area: calendar
summary: La semana que viene, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: ae462ef9e7316cb6
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que conectaste,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos del trabajo que delegaste,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de las reservas y entradas que recibes por correo.

Si una reunión está en dos calendarios, solo aparece una vez. Los eventos de un calendario que alguien compartió contigo aparecen atenuados y con el nombre de esa persona; nunca generan una tarea. Los eventos que duran todo el día o varios días aparecen como eventos de todo el día en cada día que abarcan. En Agenda, un viaje aparece primero en cada uno de sus días. En Semana y Mes, aparece como una sola franja que abarca esos días, por ejemplo, «Viaje a Lisboa».

Un plan hecho en conjunto cuenta como una sola promesa, marcada «Con» y el nombre de la otra persona. Si una promesa está relacionada con una reunión de ese día con la misma persona, aparece en la fila de esa reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea abierta, se muestra su estado: **Preparación lista**, **Preparando** o **Tarea**. Las tareas que parecen estar hechas, porque ya respondiste o porque al ejecutarlas se detectó que ya estaban resueltas, no aparecen como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes o hacia arriba, o pulsa **Mostrar días anteriores**, para ver los anteriores. Retrocede hasta una semana antes de que conectaras tu calendario y muestra arriba una línea que indica desde qué día. Cuando se incorpore el [historial](history.md), podrás retroceder aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil, muestra tres días.
- **Mes** muestra el mes completo. En el ordenador, muestra hasta tres elementos por día. En el móvil, muestra puntos y, al tocar uno, aparecen los elementos de ese día.

**Hoy**, ‹ y ›, en la parte superior, te permiten avanzar y retroceder por las semanas o los meses. La vista que elijas se guarda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro y se pueden leer. El resto se muestra como **+N**; al pulsarlo, se abre ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa, el viaje o el evento, o la reunión. Si no puedes cambiar una reunión desde aquí, por ejemplo, porque es de otra persona o tiene invitados, verás sus detalles: cuándo, dónde y quiénes asisten. Las personas que conoce tu Graph, y las organizaciones y los proyectos relacionados con la reunión, enlazan a sus páginas. **Abrir en Google Calendar** o **Abrir en Outlook**, debajo, abre la reunión en ese calendario. Consultarla no cambia nada.

Si una reunión tiene una sala reservada, esta aparece en «Dónde», nunca como persona ni en tu Graph.

El enlace de una reunión muestra el nombre del servicio, como Zoom, Google Meet o Teams, o **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes por correo una reserva de vuelo, hotel, alojamiento vacacional, tren, autobús, ferry, coche de alquiler, taxi o aparcamiento en el aeropuerto, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un viaje, aunque lleguen a distintos buzones: el tren al aeropuerto, los vuelos, el coche, la estancia y el regreso. Las reservas se agrupan si sus fechas coinciden o si una empieza cuando termina la otra.

El viaje aparece como una sola franja que abarca sus días. Ábrelo para ver cada reserva en orden cronológico, con sus horarios, dirección, código de reserva y asiento.

Las entradas para conciertos, partidos, festivales o conferencias crean un evento por cada ocasión, con el lugar, el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade al que ya existe. Los eventos reservados desde tu buzón de trabajo se clasifican como Trabajo; los demás, como Personal. Las entradas para algo que ocurre durante un viaje se añaden al viaje.

Si un viaje aún no ha empezado, tu Machine indica qué falta, por ejemplo, **No hay alojamiento reservado para 2 noches** o que no hay ningún trayecto reservado del aeropuerto al hotel. Esas líneas aparecen atenuadas y marcadas como **Sin reserva**. Si un viaje no tiene ninguna estancia, no se muestran avisos sobre las noches.

- Cada línea indica de quién viene la reserva, como **De Example Tickets**, y abre ese correo.
- Si del correo se creó una tarea, por ejemplo, pagar las entradas, **Abrir la tarea** la muestra.
- Si cambia una reserva, se actualiza su línea; si se cancela, desaparece. Cuando se cancelan todas las reservas, también desaparece el viaje o el evento.
- Las reservas de otras personas, como el vuelo de un compañero que te reenviaron, no se añaden a tus viajes.

La mayoría de las confirmaciones incluyen los detalles en un formato que tu Machine puede leer sin IA. Si no es así, por ejemplo, porque se trata de un correo reenviado o de una web de reservas pequeña, tu [modelo](model.md) lee el correo en segundo plano, de unos pocos en unos pocos, y espera si estás cerca del límite de uso. Cuando se incorpora el [historial](history.md), tu Machine también lee en segundo plano los correos de reservas del año que conserva ese historial.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** recoge palabra por palabra lo que se dijo. Aparece contraída e indica cuánto dura; **Mostrar** la despliega.

Si no se cargan, la aplicación vuelve a intentarlo automáticamente durante aproximadamente medio minuto. Después, pulsa **Reintentar**.

Cada parte tiene sus propios controles: **Añadir notas** o **Añadir transcripción**, **Subir archivo** para subir un archivo Markdown o de texto, **Editar** y **Quitar** (pulsa dos veces). Lo que añadas a una parte se queda ahí. En las reuniones que puedes cambiar, abre las notas desde **Notas**, debajo del formulario.

Si conectaste [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), sus notas aparecen en Notas y su transcripción en Transcripción, marcadas como **De Zoom**, **De Google Meet** o **De Granola**. Nunca reemplazan lo que añadiste: si están las dos, se muestran las dos.

También pueden añadirse notas al evento de calendario de la propia reunión después de que empiece, o llegar por correo desde Zoom o Gemini. Cuando termina la reunión, The Machine crea tareas a partir de ellas solo si hay pasos siguientes claros. Si llegan las mismas notas por dos vías, se crea una sola tarea y la reunión figura como su origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción, pero no notas, aparece **Generar notas**. The Machine las redacta a partir de la transcripción: un resumen breve, las decisiones y las tareas pendientes con la persona responsable, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si es larga, puede tardar unos minutos y usa tu propio modelo. Las notas indican **Escrito por The Machine** y nunca reemplazan las que añadiste.

También puedes pedirle a The Machine que las añada. Por ejemplo, en una tarea, dile «añade esta transcripción a la reunión de hoy del equipo». La transcripción se añade a Transcripción y el resumen, a Notas. En Calendar, las reuniones que las tienen muestran **Notas** o **Transcripción**.

The Machine lee ambas para encontrar tareas de seguimiento de la reunión. Se clasifican como Trabajo o Personal, igual que la reunión, y solo se comparten con tu equipo si la reunión también se comparte con él.

La reunión se abre con estos detalles desde cualquier lugar donde la encuentres: en una cronología, en una búsqueda de mensajes o como origen de una tarea. **Invitación original**, al final, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes cambiar tu propio calendario de Google. Outlook y otros calendarios solo se pueden consultar. **Nuevo evento** crea uno (en el móvil, está bajo **+** en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento de ese calendario que no tenga invitados para cambiarlo o **Eliminarlo** (pulsa dos veces).

**Dónde** sugiere lugares mientras escribes: primero, los que ya usaste y tus organizaciones; después, direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían para buscarlas las palabras que escribes. Elige una sugerencia o conserva tu propio texto.

**Invitar** añade personas de tu Graph o cualquier dirección de correo electrónico. Esta opción solo está disponible en tu propio calendario. Sobre el botón aparece quién recibirá una invitación, y el botón indica cuántas personas son: **Añadir e invitar a 2**. Google envía las invitaciones cuando lo pulsas, no antes. Si no hay invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede sugerir un cambio, como añadir una recogida. Muestra exactamente qué cambiará y solo lo hace si pulsas **Añadir**, **Guardar** o **Eliminar**.

¿Todavía no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre Conexiones para conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente. Puede redactar una nota breve para cambiarlo u ofrecerse a rechazarlo. No se envía nada hasta que lo apruebes.

Los eventos de todo el día, los que indican que estás disponible y los provisionales no cuentan. Cada conflicto aparece una sola vez. Una tarea de Trabajo solo indica que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú puedes ver con qué coincide.

## Todo listo para tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Preparar la reunión**. Es un resumen breve:

- **Quién:** quiénes son, según tu Graph, con información sobre sus antecedentes si se conoce.
- **Organización:** a qué se dedica su empresa y qué es relevante para la reunión.
- **Hasta ahora:** qué hablaron, qué preguntaron y qué ofrecieron, y en qué punto están. Después de la reunión, esos mensajes aparecen como fuentes de la tarea.
- **Promesas pendientes:** qué queda por cumplir, de tu parte o de la suya.
- **Preguntas abiertas:** qué preguntas siguen sin respuesta.
- **Decidir o llevar:** qué hay que decidir o llevar, y qué probablemente les interese.

La tarea aparece por la mañana de un día laborable: el mismo día de la reunión si es por la tarde, o el día laborable anterior. Es solo para consultar: pulsa **Hecho** cuando la hayas leído. Si incluye una promesa o pregunta que requiere una acción, tendrá su propia tarea.

Usa la información que ya está en tu Machine. Si es la primera reunión con alguien de una empresa, también hace una búsqueda breve en la web con su nombre y el de la empresa, y muestra un enlace junto a lo que encuentra. Para la búsqueda solo se envían su nombre público, el nombre de la empresa y su sitio web, nunca tus mensajes. Los resultados se reutilizan durante 30 días. Si **Buscar contactos de trabajo** está desactivado en Ajustes, en Seguridad, no se hace ninguna búsqueda.

Si no hay información útil del historial, no se crea ninguna tarea. Las reuniones periódicas, internas o personales, y las reuniones rechazadas, no generan tareas. Si una reunión cambia de hora, conserva su tarea y se actualiza la hora. Si descartas una tarea, no vuelve a aparecer. La tarea de una reunión cancelada se cierra automáticamente.

Los detalles de la reunión muestran su tarea bajo **Tarea**. Puedes abrirla con un solo toque desde el chat de la reunión.
