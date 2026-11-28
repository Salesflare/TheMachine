---
title: Calendario
area: calendar
summary: Toda la semana en un mismo sitio: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 7f9f9d9e9a502b7d
---
## Qué muestra

Tus días desde hoy, con:

- reuniones de los calendarios que has conectado,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos del trabajo que has pasado a otras personas,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de las reservas y entradas que recibes por correo.

Si una reunión está en dos calendarios, solo aparece una vez. Los eventos de un calendario que alguien haya compartido contigo aparecen atenuados y con el nombre de pila de esa persona; nunca generan una tarea. Los eventos de todo el día y los que duran varios días aparecen como eventos de todo el día, en cada uno de los días que abarcan. En Agenda, un viaje aparece primero en cada uno de sus días; en Semana y Mes, como una sola franja a lo largo de todos esos días, por ejemplo, «Viaje a Lisboa».

Un plan que habéis hecho juntos es una sola promesa, marcada como «Con» y el nombre de esa persona. Una promesa sobre una reunión de ese día con la misma persona aparece en la fila de esa reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea pendiente, se indica: **Preparación lista**, **Preparando** o **Tarea**. Una tarea que parece hecha, porque ya has respondido o porque la ejecución ha detectado que ya está hecha, no aparece como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes, o hacia arriba (o toca **Mostrar días anteriores**) para ver los anteriores. Retrocede hasta una semana antes de que conectaras tu calendario; una línea en la parte superior indica desde qué día. Cuando se haya cargado tu [historial](history.md), podrás retroceder aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil muestra tres días.
- **Mes** muestra el mes entero. En un ordenador aparecen hasta tres elementos por día; en un móvil, puntos. Toca un día para ver su lista.

**Hoy**, ‹ y › en la parte superior te permiten avanzar o retroceder por las semanas o los meses. La vista que elijas se recuerda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro y siguen siendo legibles. El resto se muestra como **+N**; tócalo para abrir ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa, el viaje o el evento, o la reunión. Si no puedes cambiar una reunión desde aquí, por ejemplo, porque es de otra persona o tiene invitados, verás sus detalles: cuándo, dónde y quiénes asisten. Las personas que conoce tu Graph, y las organizaciones y los proyectos asociados a la reunión, enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**) aparece debajo y abre la reunión en ese servicio. Consultar una reunión no cambia nada.

La sala reservada para una reunión aparece debajo de dónde, nunca como persona ni en tu Graph.

El enlace de una reunión aparece con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes por correo una reserva de vuelo, hotel, casa de vacaciones, tren, autobús, ferry, coche de alquiler, taxi o aparcamiento en el aeropuerto, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un solo viaje, aunque lleguen a cualquiera de tus buzones: el tren al aeropuerto, los vuelos, el coche, el alojamiento y el trayecto de vuelta. Las reservas se agrupan cuando coinciden en fechas o cuando una empieza al terminar la otra.

El viaje aparece como una franja que abarca todos sus días. Ábrelo para ver cada reserva en orden cronológico, con sus horarios, dirección, código de reserva y asiento.

Las entradas para un concierto, un partido, un festival o una conferencia crean un evento, uno por cada evento, con el lugar, el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade al mismo. Si las entradas se han reservado desde tu buzón de trabajo, el evento es de trabajo; si no, es personal. Las entradas para algo que ocurre durante un viaje se añaden al viaje.

Si tienes un viaje próximo, tu Machine te indica qué falta, por ejemplo, **No hay alojamiento reservado para 2 noches** o que no tienes nada reservado para ir del aeropuerto al hotel. Estas líneas aparecen atenuadas y marcadas como **Sin reserva**. Si el viaje no incluye ninguna estancia, no se indica nada sobre las noches.

- Cada línea indica de quién procede la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo ha generado una tarea, por ejemplo, para pagar las entradas, **Abrir la tarea** la muestra.
- Si cambia una reserva, se actualiza su línea; si se cancela, desaparece. Cuando se cancelan todas las reservas, también desaparece el viaje o el evento.
- Las reservas de otras personas, como el vuelo de un compañero que te han reenviado, no aparecen en tus viajes.

La mayoría de las confirmaciones incluyen los detalles en un formato que tu Machine puede leer sin IA. Si no es así, por ejemplo, si es un correo reenviado o de un sitio de reservas pequeño, tu [modelo](model.md) lee el correo en segundo plano, de unos pocos en unos pocos, y espera si estás cerca del límite de uso. Cuando se haya cargado tu [historial](history.md), tu Machine leerá en segundo plano los correos de reservas del año que conserva.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas pendientes. **Transcripción** recoge palabra por palabra lo que se dijo. Al principio aparece plegada junto con su duración; **Mostrar** la despliega.

Si no se carga, volverá a intentarlo automáticamente durante aproximadamente medio minuto. Después, toca **Reintentar**.

Cada parte tiene sus propios botones **Añadir notas** o **Añadir transcripción**, **Subir archivo** para subir un archivo Markdown o de texto, **Editar** y **Quitar** (toca dos veces). Lo que añadas a una parte se queda ahí. En una reunión que puedas cambiar, **Notas**, debajo del formulario, las abre.

Si has conectado [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), sus notas aparecen en Notas y su transcripción en Transcripción, marcadas como **De Zoom**, **De Google Meet** o **De Granola**. No sustituyen nunca lo que hayas añadido: si están las dos, se muestran las dos.

También pueden añadirse notas al evento de calendario de la reunión, después de que haya empezado, o enviarse por correo desde Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de ellas si indican claramente los próximos pasos. Si las mismas notas llegan por dos vías, se crea una sola tarea, con la reunión como origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción pero no notas, aparece **Generar notas**. The Machine las redacta a partir de la transcripción: un breve resumen, decisiones y tareas con quién se encargará de cada una, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si es larga, puede tardar unos minutos y usar tu propio modelo. Las notas indican **Escrito por The Machine** y nunca sustituyen las que hayas añadido.

The Machine también puede añadirlas. Pídeselo en una tarea, por ejemplo: «añade esta transcripción a la reunión de hoy sobre el tablero». La transcripción se añade a Transcripción y el resumen, a Notas. En el Calendario, las reuniones que las tienen muestran **Notas** o **Transcripción**.

The Machine lee ambas para buscar tareas pendientes de la reunión. Son de trabajo o personales, como la reunión, y solo llegan a tu equipo si la reunión también es de trabajo.

La reunión se abre con estos detalles desde cualquier lugar donde la encuentres: en una cronología, en una búsqueda de mensajes o como origen de una tarea. **Invitación original**, en la parte inferior, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes cambiar tu propio calendario de Google. Outlook y los demás calendarios solo se pueden consultar. **Nuevo evento** añade uno (en el móvil está bajo **+**, en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento de ese calendario sin invitados para cambiarlo o **Eliminar** (toca dos veces).

Al escribir en **Dónde**, se sugieren lugares: primero los que has usado antes y tus organizaciones, y después direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribas para buscarlas. Elige una sugerencia o deja tu propio texto.

**Invitar** añade personas de tu Graph o cualquier dirección de correo. Esta opción solo está disponible en tu propio calendario. Encima del botón aparecen las personas invitadas y el botón indica cuántas son: **Añadir e invitar a 2**. Google envía las invitaciones cuando lo tocas, no antes. Si no hay invitados, no se invita ni se avisa a nadie.

Una tarea también puede proponerte un cambio, como añadir una recogida. Verás exactamente qué cambia; solo se hará si tocas **Añadir**, **Guardar** o **Eliminar**.

¿Todavía no tienes reuniones? Si no has conectado ningún calendario, **Conecta tu calendario** abre Conexiones, donde puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Cuando una reunión de trabajo se solapa con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente. Puede preparar una nota breve para cambiarlo o proponerte rechazarlo. No se envía nada hasta que des tu visto bueno.

Si un evento se solapa con varios, se crea una sola tarea sobre ese evento. Si se solapa con otro mientras la tarea sigue abierta, se añade a ella. Cuando la tarea se completa o se descarta, solo se vuelve a crear si después se añade o se cambia una reunión.

Los eventos de todo el día, los que aparecen como libre y los provisionales no cuentan, y cada conflicto solo se detecta una vez. Tampoco cuentan la ubicación de trabajo, el tiempo de concentración ni la ausencia de la oficina de Google. Lo mismo ocurre con un bloque tuyo que incluya otras reuniones, como una jornada en la oficina: solo pueden entrar en conflicto las reuniones que contiene. Un bloque sin otras personas ni reuniones, como un vuelo, sí entra en conflicto con un evento que tenga a otras personas.

Una tarea de trabajo solo indica que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú ves con qué entra en conflicto: los dos primeros y cuántos más hay. Si no haces nada con una tarea y el conflicto se incluye en otra tarea o resulta que no existía, la tarea se cierra automáticamente.

## Preparación para tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Preparar** la reunión. Es un resumen breve:

- **Quién:** quiénes son, según tu Graph, con información sobre su trayectoria cuando se conoce.
- **Organización:** a qué se dedica su empresa, para quién y a qué precio, cuando sea relevante para la reunión.
- **Hasta ahora:** qué habéis hablado, preguntado y ofrecido, y en qué punto estáis. Después de la reunión, esos mensajes aparecen como fuentes de la tarea.
- **Acordado anteriormente:**, **Cambios desde entonces:** y **Aún pendiente:** lo que surgió en reuniones anteriores con las mismas personas; cada línea indica la reunión o el mensaje del que procede.
- **Promesas pendientes:** lo que tú o esas personas aún tenéis que hacer, según las promesas de tu Machine.
- **Preguntas pendientes:** lo que aún no tiene respuesta.
- **Decidir o llevar:** qué tenéis que resolver o llevar, y qué es probable que les interese.

La tarea llega por la mañana de un día laborable: el mismo día de la reunión si es por la tarde; si no, el día laborable anterior. Está pensada para leerla: aparece como **Hecho** cuando la has leído. Si incluye una promesa o una pregunta que requiere hacer algo, tiene su propia tarea.

Pregunta sobre la reunión en su chat o añade lo que sabes: The Machine te responde o incorpora tu nota al resumen, por ejemplo, en **Decidir o llevar**, y aprende de ella. No se envía nada desde el resumen.

Se tienen en cuenta las reuniones anteriores en las que haya participado alguien ajeno a tu empresa, sin importar cómo se llamaran ni qué dirección usara esa persona. The Machine lee las notas que tiene tu Machine: las tuyas, las de tu aplicación de reuniones o las que te enviaron por correo; si no hay, lee la transcripción o las notas del evento del calendario. Las más recientes tienen más peso y no se muestran como pendientes los asuntos que se resolvieron después.

También se tienen en cuenta las notas y los mensajes de [Historial](history.md), para que el resumen incluya reuniones anteriores a tu incorporación.

Un resumen de trabajo no lee notas personales ni nada de la Machine de otra persona. El texto es solo para ti: no se incluye al pasar una tarea a otra persona ni se puede enviar para que la revise. Si no hay notas, no aparecen esas líneas.

El resumen usa lo que ya hay en tu Machine. Si es tu primera reunión con alguien de una empresa, también consulta la página principal del sitio web de la empresa.

También busca brevemente en la web el nombre de esa persona y su empresa. Si tu Machine está alojada, la búsqueda se hace con tu cuenta de ChatGPT o Claude y consume una pequeña parte de tu plan. Si usas tu propio ordenador, utiliza el proveedor de búsqueda que hayas configurado en OpenClaw, o tu cuenta cuando lo actives (`meeting_prep_signin_search` en `config.json`). Siempre se da prioridad al proveedor que hayas configurado.

En la búsqueda solo se incluyen el nombre público de la persona, el nombre de la empresa y el sitio web, nunca tus mensajes. Los resultados incluyen un enlace y se reutilizan durante 30 días. En ChatGPT, el modelo elige el enlace y nadie lo verifica: ábrelo antes de fiarte de lo que dice. El chat de la tarea muestra **Buscó en la web**.

Así, una primera reunión que hayas aceptado puede tener un resumen antes de que hayáis intercambiado una sola palabra: a qué se dedica la empresa, qué significa para ti y, si se sabe, quiénes son. Si solo tienes un nombre de pila, solo se conserva lo que encuentre la búsqueda si apunta a una sola persona. Si desactivas **Buscar contactos de trabajo** (Ajustes, Seguridad), no se busca nada.

Las reuniones periódicas solo reciben un resumen si hay novedades desde la última vez: un mensaje, notas o una promesa. El resumen indica qué hay de nuevo, no lo que decía el resumen anterior. Llega cuando termina la reunión anterior, como máximo para dos reuniones periódicas al día.

Las reuniones solo con tu equipo reciben un resumen únicamente si las notas anteriores de la misma serie (o del mismo título, si has participado en alguna) dejan algo pendiente para ti: una tarea tuya, una pregunta para ti, una decisión que aún debes tomar o una promesa que hiciste. Las tareas pendientes de tus compañeros no generan un resumen. No se busca información sobre tus compañeros y, si es posible, el resumen llega la misma mañana de la reunión.

Si no hay nada útil que decir, no se crea ninguna tarea. Las reuniones personales y las que hayas rechazado no generan ninguna. Si se cambia la hora de una reunión, se mantiene la misma tarea y se actualiza la hora. Las tareas descartadas no vuelven a aparecer y la de una reunión cancelada se cierra automáticamente.

Si una actualización cambia el contenido de un resumen, los resúmenes abiertos de las reuniones futuras se redactan de nuevo una vez, con la información actualizada. Conservan el título, las fuentes y el lugar en la lista. Los que hayas cambiado, pospuesto o cerrado no se modifican; tampoco los de reuniones que empiezan en los próximos minutos.

Los detalles de la reunión muestran su tarea bajo **Tarea**. Tócala para abrir el chat.
