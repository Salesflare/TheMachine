---
title: Calendario
area: calendar
summary: La semana que tienes por delante, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 479aa9c3fadda8bd
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que has conectado,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos de tareas que has delegado,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de las reservas y entradas que recibes por correo.

Una reunión que aparece en dos calendarios solo se muestra una vez. Los eventos de un calendario que alguien ha compartido contigo aparecen atenuados, con el nombre de pila de esa persona; nunca generan una tarea. Los eventos de todo el día y los que duran varios días aparecen como eventos de todo el día en cada uno de los días que ocupan. En Agenda, un viaje aparece primero cada uno de sus días; en Semana y Mes aparece como una única franja que abarca esos días, por ejemplo, «Viaje a Lisboa».

Un plan acordado con otra persona cuenta como una sola promesa, marcada con «Con» y su nombre. Si una promesa trata sobre una reunión de ese día con esa misma persona, aparece en la fila de la reunión.

**Vencida** aparece primero. Una reunión con una tarea pendiente muestra su estado: **Preparación lista**, **Preparando** o **Tarea**. Las tareas que parecen completadas, porque ya has respondido o porque una ejecución ha detectado que están hechas, no aparecen como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes o hacia arriba, o pulsa **Mostrar días anteriores**, para ver los anteriores. Se remonta a la semana anterior a la conexión de tu calendario y una línea en la parte superior indica desde qué día. Cuando se cargue el [historial](history.md), se remontará aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil muestra tres días.
- **Mes** muestra el mes completo. En un ordenador se muestran hasta tres elementos por día; en el móvil aparecen puntos y, al tocar uno, se muestra la lista de ese día.

**Hoy**, ‹ y ›, en la parte superior, te permiten avanzar o retroceder por las semanas o los meses. La vista que elijas se recuerda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro y se pueden leer. El resto se muestran como **+N**; al pulsarlo, se abre ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa, el viaje o evento, o la reunión. Si no puedes cambiar una reunión desde aquí, por ejemplo, porque es de otra persona o tiene invitados, se muestran sus detalles: cuándo, dónde y quién. Las personas que conoce Graph y las organizaciones y proyectos de la reunión enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**), debajo de esos datos, abre la reunión allí. Consultarla no cambia nada.

La sala reservada para una reunión aparece debajo de dónde se celebra, nunca como persona ni en tu Graph.

El enlace de una reunión aparece con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes por correo una reserva de vuelo, hotel, casa de vacaciones, tren, autobús, ferry, coche de alquiler, taxi o aparcamiento en el aeropuerto, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un viaje, aunque procedan de cualquiera de tus buzones: el tren al aeropuerto, los vuelos, el coche, la estancia y el trayecto de vuelta. Las reservas se agrupan si sus fechas coinciden o si una empieza cuando termina la otra.

El viaje aparece como una sola franja que abarca sus días. Ábrelo para ver cada reserva en orden cronológico, con sus horarios, dirección, código de reserva y asiento.

Las entradas para conciertos, partidos, festivales o conferencias crean un evento por cada ocasión, con el lugar, el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade al mismo. Si has reservado las entradas desde tu buzón de trabajo, el evento es de Trabajo; si no, es Personal. Las entradas para algo que ocurre durante un viaje se añaden al viaje.

Si todavía no ha llegado la fecha del viaje, tu Machine indica lo que falta, como **No hay alojamiento reservado para 2 noches** o que no hay ningún transporte reservado del aeropuerto al hotel. Esas líneas aparecen atenuadas y marcadas como **Sin reserva**. Si un viaje no tiene alojamiento, no se indica nada sobre las noches.

- Cada línea indica quién ha enviado la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo ha generado una tarea, por ejemplo, para pagar las entradas, **Abrir la tarea** la muestra.
- Si se modifica una reserva, se actualiza su línea; si se cancela, desaparece. Cuando se cancelan todas las reservas, también desaparece el viaje o el evento.
- Las reservas de otra persona, como el vuelo de un compañero que te han reenviado, no se añaden a tus viajes.

La mayoría de las confirmaciones incluyen los detalles en un formato que tu Machine puede leer sin IA. Si no es así, por ejemplo, porque es un correo reenviado o de un sitio de reservas pequeño, tu [modelo](model.md) lee el correo en segundo plano, de unos pocos en unos pocos, y espera si estás cerca de tu límite de uso. Cuando se carga el [historial](history.md), tu Machine lee en segundo plano los correos de reservas del año que conserva.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** recoge lo que se ha dicho palabra por palabra. Al principio está plegada y muestra su duración; **Mostrar** la abre.

Si no se cargan, se vuelven a cargar automáticamente durante aproximadamente medio minuto. Después, pulsa **Reintentar**.

Cada parte tiene sus propias opciones **Añadir notas** o **Añadir transcripción**, **Subir archivo** para subir un archivo Markdown o de texto, **Editar** y **Quitar** (pulsa dos veces). El contenido de una parte no se mezcla con la otra. Si puedes cambiar la reunión, la opción **Notas**, debajo del formulario, las abre.

Si has conectado [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), las notas aparecen en Notas y la transcripción en Transcripción, marcadas como **De Zoom**, **De Google Meet** o **De Granola**. Nunca sustituyen lo que has añadido: si están las dos versiones, se muestran ambas.

También pueden llegar notas en el evento de calendario de la propia reunión, añadirse después de que haya empezado o enviarse por correo desde Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de ellas si indican próximos pasos claros. Si las mismas notas llegan por dos vías, se crea una sola tarea cuya fuente es la reunión: «Fuente: notas de» la reunión.

Si una reunión tiene transcripción, pero no notas, aparece la opción **Generar notas**. The Machine las redacta a partir de la transcripción: un resumen breve, decisiones y tareas pendientes con la persona responsable, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Una reunión larga puede tardar unos minutos; para redactar las notas se usa tu propio modelo. Las notas indican **Redactado por The Machine** y nunca sustituyen las que hayas añadido.

The Machine también puede añadirlas. Pídeselo en una tarea, por ejemplo: «Añade esta transcripción a la reunión de hoy del tablero». La transcripción se añade a Transcripción y el resumen, a Notas. En el Calendario, las reuniones con notas o transcripción muestran **Notas** o **Transcripción**.

The Machine lee ambas para detectar tareas de seguimiento de la reunión. Son de Trabajo o Personales, como la reunión, y solo llegan a tu equipo si la reunión también es de Trabajo.

La reunión muestra estos detalles dondequiera que la encuentres: en una cronología, en una búsqueda de mensajes o como fuente de una tarea. **Invitación original**, en la parte inferior, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes cambiar tu propio calendario de Google. Outlook y los demás calendarios solo se pueden consultar. **Nuevo evento** añade un evento (en el móvil está debajo de **+**, en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento de ese calendario sin invitados para cambiarlo o **Eliminar** (pulsa dos veces).

**Dónde** sugiere lugares mientras escribes: primero, los que has usado antes y los de tus organizaciones; después, direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige una sugerencia o conserva el texto que has escrito.

**Invitar** añade personas de tu Graph o cualquier dirección de correo. Esta opción solo está disponible en tu propio calendario. Las personas que recibirán una invitación aparecen encima del botón, que indica cuántas son: **Añadir e invitar a 2**. Google envía las invitaciones al pulsar el botón, no antes. Si no hay invitados, nadie recibirá una invitación ni una actualización.

Una tarea también puede sugerir un cambio, como añadir una recogida. Se muestra exactamente qué va a cambiar y solo se hace si pulsas **Añadir**, **Guardar** o **Eliminar**.

¿Todavía no tienes reuniones? Si no tienes un calendario, **Conecta tu calendario** abre Conexiones para conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente de los dos. Puede redactar un mensaje breve para cambiarlo o sugerir que lo rechaces. No se envía nada hasta que lo apruebes.

Si un evento coincide con varios, se crea una sola tarea sobre ese evento. Si surge otro conflicto mientras la tarea sigue pendiente, se añade a ella. Cuando se completa o se descarta, solo vuelve a aparecer si más adelante se crea o cambia una reunión.

Los eventos de todo el día, disponibles y provisionales nunca cuentan, y cada conflicto se detecta una sola vez. Tampoco cuentan la ubicación de trabajo, el tiempo de concentración ni el estado de ausencia de Google. Los bloques de tu calendario que incluyen otras reuniones tampoco cuentan, como un día en la oficina: solo las reuniones dentro del bloque pueden entrar en conflicto. Un bloque sin otras personas ni reuniones, como un vuelo, sí entra en conflicto con un evento que incluya a otras personas.

Una tarea de Trabajo solo indica que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú puedes ver con qué coincide: primero los dos primeros y luego cuántos más hay. Si no haces nada con una tarea, se cierra automáticamente cuando el conflicto ya está en otra tarea o resulta que no había conflicto.

## Prepárate para tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Prepárate para** la reunión. Es un resumen breve:

- **Quién:** quiénes son, según tu Graph, y algunos datos sobre su trayectoria si se conocen.
- **Organización:** a qué se dedica su empresa, para quién y a qué precio, si es relevante para la reunión.
- **Hasta ahora:** qué habéis hablado, preguntado y ofrecido, y en qué punto está todo. Esos mensajes pasan a ser las fuentes de la tarea después de la reunión.
- **Acordado anteriormente:**, **Cambios desde entonces:** y **Aún pendiente:** lo que surgió en reuniones anteriores con las mismas personas. Cada línea indica de qué reunión o mensaje procede.
- **Promesas pendientes:** lo que tú o esas personas aún tenéis que cumplir, según las promesas de tu Machine.
- **Preguntas pendientes:** lo que aún no tiene respuesta.
- **Decisiones o preparativos:** qué hay que decidir o llevar, y qué les podría interesar.

La tarea aparece por la mañana de un día laborable: el mismo día de la reunión si es por la tarde; si no, el día laborable anterior. Es solo para leer: indica **Hecho** cuando la hayas leído. Si incluye una promesa o una pregunta que requiere hacer algo, tendrá su propia tarea.

Pregunta sobre la reunión en su chat o añade lo que sabes: The Machine responde o incorpora tu nota al resumen, por ejemplo, en **Decisiones o preparativos**, y aprende de ella. No se envía nada desde el resumen.

Se tienen en cuenta las reuniones anteriores en las que haya participado la misma persona externa, independientemente de cómo se llamara la reunión y de la dirección que usara. Se leen las notas que tu Machine conserva: las tuyas, las de la aplicación de reuniones o las que te hayan enviado por correo. Si no hay ninguna, se usa la transcripción o las notas del evento del calendario. Las notas más recientes tienen más peso y no se muestra como pendiente un tema que ya se haya resuelto después.

También se tienen en cuenta las notas y los mensajes del [Historial](history.md), así que el resumen puede incluir reuniones anteriores a tu incorporación.

Los resúmenes de trabajo no leen notas personales ni nada de la Machine de otra persona. El texto es solo para ti: no se incluye al delegar una tarea y no se puede enviar para que otra persona lo revise. Si no hay notas, no aparecen esas líneas.

Se usa la información que ya está en tu Machine. Para la primera reunión con alguien de una empresa, también se consulta la página de inicio del sitio web de la empresa.

Si has configurado la búsqueda web en tu Machine, también se hace una búsqueda breve en la web sobre su nombre y su empresa. Las Machines alojadas no la incluyen; si usas tu propio ordenador, puedes configurarla en OpenClaw. Los resultados incluyen un enlace. En la búsqueda solo se usan el nombre público, el nombre de la empresa y su sitio web, nunca tus mensajes. Los resultados se reutilizan durante 30 días.

Así, una primera reunión que hayas aceptado puede tener un resumen antes de que hayas intercambiado una palabra: a qué se dedica su empresa, qué significa para ti y, si se sabe, quiénes son. Si solo tienes un nombre de pila, solo se conserva lo que encuentra la búsqueda si apunta a una única persona. Si desactivas **Buscar contactos de trabajo** (Ajustes, Seguridad), no se busca nada.

Las reuniones periódicas solo generan un resumen si hay novedades desde la última vez: un mensaje, notas o una promesa. El resumen indica qué ha cambiado, no repite el anterior. Aparece cuando ha terminado la reunión previa, con un máximo de dos reuniones periódicas al día.

Si no hay nada útil que decir, no se crea ninguna tarea. Las reuniones internas, personales y rechazadas no generan tareas. Si se cambia la hora de una reunión, se conserva la misma tarea, con la nueva hora. Una tarea descartada no vuelve a aparecer y la de una reunión cancelada se cierra automáticamente.

Si una actualización cambia el contenido del resumen, los resúmenes abiertos de reuniones futuras se redactan de nuevo una sola vez, con la información actualizada. Conservan el título, las fuentes y el lugar en la lista. Los que hayas cambiado, pospuesto o cerrado no se modifican; tampoco los de reuniones que empiezan en los próximos minutos.

Los detalles de la reunión muestran la tarea debajo de **Tarea**. Pulsa una vez para abrir su chat.
