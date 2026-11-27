---
title: Calendario
area: calendar
summary: La semana que tienes por delante, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 4b5bc600fefb624c
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que has conectado,
- tareas que vencen ese día y tareas pospuestas el día que vuelven,
- seguimientos del trabajo que has delegado,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de las reservas y entradas que recibes por correo.

Una reunión que aparece en dos calendarios solo se muestra una vez. Los eventos de un calendario que alguien ha compartido contigo aparecen atenuados, con el nombre de esa persona; nunca generan una tarea. Los eventos de todo el día y los que duran varios días aparecen como eventos de todo el día en cada uno de los días que abarcan. En Agenda, un viaje aparece primero cada uno de sus días; en Semana y Mes, aparece como una sola franja que abarca esos días, por ejemplo, «Viaje a Lisboa».

Un plan acordado entre varias personas es una sola promesa, marcada con «Con» y el nombre de la otra persona. Una promesa sobre una reunión de ese día con la misma persona aparece en la fila de esa reunión.

**Vencida** aparece primero. Una reunión con una tarea pendiente la muestra: **Preparación lista**, **Preparando** o **Tarea**. Una tarea que parece completada, porque ya has respondido o porque la ejecución ha detectado que está hecha, no aparece como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes, o hacia arriba (o pulsa **Mostrar días anteriores**) para ver los anteriores. Se remonta a la semana anterior a la conexión de tu calendario, y una línea en la parte superior indica desde qué día. Cuando se haya cargado tu [historial](history.md), se remontará aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil, muestra tres días.
- **Mes** muestra el mes entero. En un ordenador se muestran hasta tres elementos por día; en el móvil aparecen puntos y, al tocar uno, se muestra la lista de ese día.

**Hoy**, ‹ y › en la parte superior te permiten desplazarte por las semanas o los meses. La vista que elijas se recuerda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en el horario aparecen uno al lado del otro, sin perder legibilidad. Los demás se muestran como **+N**; al pulsarlo, se abre ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de la tarea, la promesa, el viaje o evento, o la reunión. Si no puedes modificar una reunión desde aquí, por ejemplo, porque es de otra persona o tiene invitados, verás sus detalles: cuándo y dónde es, y quién asiste. Los contactos que conoce tu Graph, así como las organizaciones y los proyectos relacionados con la reunión, enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**) debajo de ellos abre la reunión allí. Consultarla no cambia nada.

Si una reunión tiene una sala reservada, esta aparece debajo del lugar, nunca como una persona ni en tu Graph.

El enlace de una reunión aparece con el nombre del servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes por correo una reserva de vuelo, hotel, casa de vacaciones, tren, autobús, ferry, coche de alquiler, taxi o aparcamiento del aeropuerto, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un viaje, sin importar en cuál de tus buzones lleguen: el tren al aeropuerto, los vuelos, el coche, el alojamiento y el viaje de vuelta. Las reservas se agrupan si coinciden en algún día o si una empieza cuando termina la otra.

El viaje aparece como una sola franja que abarca sus días. Ábrelo para ver cada reserva en orden cronológico, con sus horarios, dirección, código de reserva y asiento.

Las entradas para un concierto, partido, festival o conferencia crean un evento, uno por cada evento, con el lugar, el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade al mismo. Las entradas reservadas desde el buzón de trabajo son de Trabajo; las demás, de Personal. Las entradas para algo que tiene lugar durante un viaje se añaden al viaje.

Si aún falta para el viaje, tu Machine indica qué falta, por ejemplo, **No hay alojamiento reservado para 2 noches** o que no has reservado nada para ir del aeropuerto al hotel. Esas líneas aparecen atenuadas y marcadas como **Sin reserva**. Si un viaje no tiene alojamiento, no se indican las noches.

- Cada línea indica de dónde viene la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo generó una tarea, por ejemplo, para pagar las entradas, **Abrir la tarea** la muestra.
- Si cambia una reserva, se actualiza su línea; si se cancela, se elimina. Cuando se cancelan todas las reservas, también se elimina el viaje o el evento.
- Las reservas de otras personas, como el vuelo de un compañero que te han reenviado, no aparecen en tus viajes.

La mayoría de las confirmaciones incluyen sus detalles en un formato que tu Machine puede leer sin IA. Si alguna no está en ese formato, como un correo reenviado o de un sitio de reservas pequeño, tu [modelo](model.md) lee el mensaje en segundo plano, de unos pocos en unos pocos, y espera si estás cerca de tu límite de uso. Una vez cargado el [historial](history.md), también se leen en segundo plano los correos de reservas del año que conserva tu Machine.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y acciones pendientes. **Transcripción** recoge literalmente lo que se dijo. Al principio está contraída y muestra su duración; **Mostrar** la despliega.

Si no se carga, vuelve a intentarlo automáticamente durante aproximadamente medio minuto. Después, pulsa **Reintentar**.

Cada parte tiene sus propios controles: **Añadir notas** o **Añadir transcripción**, **Subir archivo** para cargar un archivo Markdown o de texto, **Editar** y **Quitar** (toca dos veces). Lo que añadas a una parte se queda ahí. En una reunión que puedas modificar, **Notas**, debajo del formulario, las abre.

Si has conectado [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), las notas aparecen en Notas y la transcripción, en Transcripción, marcadas como **De Zoom**, **De Google Meet** o **De Granola**. Nunca sustituyen lo que hayas añadido: si están ambas, se muestran ambas.

También pueden añadirse notas al evento de calendario de la propia reunión después de que empiece, o llegar por correo desde Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de ellas si hay pasos siguientes claros. Si las mismas notas llegan por dos vías, se crea una sola tarea y la reunión aparece como origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción, pero no notas, aparece **Generar notas**. The Machine las redacta a partir de la transcripción: un breve resumen, las decisiones y las acciones pendientes, con la persona responsable de cada una, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si la reunión es larga, puede tardar unos minutos y usar tu propio modelo. Las notas indican **Escrito por The Machine** y nunca sustituyen las notas que hayas añadido.

The Machine también puede añadirlas. Pídeselo en una tarea, por ejemplo: «Añade esta transcripción a la reunión de hoy sobre el tablero». La transcripción se añade a Transcripción y el resumen, a Notas. En el Calendario, las reuniones que las tienen muestran **Notas** o **Transcripción**.

The Machine lee ambas para hacer seguimiento de la reunión. Se clasifican como Trabajo o Personal igual que la reunión y solo se comparten con tu equipo si la reunión también se comparte con él.

La reunión se abre con estos detalles desde cualquier lugar donde la encuentres: en una cronología, en una búsqueda de mensajes o como origen de una tarea. **Invitación original**, al final, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes modificar tu propio calendario de Google. Outlook y los demás calendarios solo se pueden consultar. **Nuevo evento** añade un evento (en el móvil, está debajo de **+**, en la barra superior): elige el calendario, un título y una hora. Haz clic en un evento sin invitados de ese calendario para modificarlo o **Eliminar** (toca dos veces).

**Dónde** sugiere lugares a medida que escribes: primero, los que ya has usado y los de tus organizaciones; después, direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscarlas. Elige una sugerencia o conserva tu propio texto.

**Invitar** añade personas de tu Graph o cualquier dirección de correo. Esta opción solo está disponible en tu propio calendario. Encima del botón se enumeran las personas que recibirán una invitación y el botón indica cuántas son: **Añadir e invitar a 2**. Google envía las invitaciones al pulsarlo, no antes. Si no hay invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede proponerte un cambio, como añadir una recogida. Verás exactamente qué va a cambiar y solo se hará si pulsas **Añadir**, **Guardar** o **Eliminar**.

¿Aún no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre Conexiones, donde puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente. Puede redactar una nota breve para cambiarlo u ofrecerte rechazarlo. No se envía nada hasta que lo apruebes.

Si un evento coincide con varios, se crea una sola tarea sobre ese evento. Si hay una nueva coincidencia mientras la tarea sigue pendiente, se añade a ella. Cuando la tarea se completa o se descarta, solo vuelve a aparecer si después se crea o modifica una reunión.

Los eventos de todo el día, los marcados como libre y los provisionales no cuentan, y cada conflicto solo aparece una vez. Tampoco cuentan la ubicación de trabajo, el tiempo de concentración ni el estado de ausencia de Google. Lo mismo ocurre con un bloque tuyo que incluya otras reuniones, como un día de oficina: solo pueden entrar en conflicto las reuniones que contiene. En cambio, un bloque sin otras personas ni reuniones, como un vuelo, sí puede entrar en conflicto con un evento que incluya a otras personas.

Una tarea de Trabajo solo indica que hay un conflicto, para que tu equipo nunca vea el evento personal. Solo tú puedes ver con qué coincide: primero los dos primeros y luego cuántos más hay. Una tarea en la que no hayas hecho nada se cierra automáticamente si el conflicto corresponde a otra tarea o resulta que no existía.

## Prepara tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Preparar la reunión**. Es un breve informe:

- **Quién:** quiénes son, según tu Graph, y algún dato sobre su trayectoria cuando se conoce.
- **Organización:** a qué se dedica su empresa, para quién y a qué precio, cuando sea relevante para la reunión.
- **Hasta ahora:** lo que habéis hablado, preguntado y ofrecido, y en qué punto está. Después de la reunión, esos mensajes aparecen como fuentes de la tarea.
- **Acordado anteriormente:**, **Cambios desde entonces:** y **Aún pendiente:** lo que surgió en reuniones anteriores con las mismas personas, con la reunión o el mensaje de origen en cada línea.
- **Promesas pendientes:** lo que aún os debéis, según las promesas de tu Machine.
- **Preguntas pendientes:** lo que aún no tiene respuesta.
- **Decisiones o material:** lo que hay que decidir o llevar, y lo que probablemente les interesará.

El informe se genera por la mañana de un día laborable: el mismo día de la reunión si es por la tarde; si no, el día laborable anterior. Está pensado para que lo leas: marca **Hecho** cuando lo hayas leído. Si incluye una promesa o una pregunta que requiere una acción, tiene su propia tarea.

Pregunta sobre la reunión en su chat o añade lo que sabes: The Machine te responderá o incorporará tu nota al informe, por ejemplo, en **Decisiones o material**, y aprenderá de ella. No se envía nada desde el informe.

Se tienen en cuenta las reuniones anteriores en las que haya participado alguien ajeno a tu empresa y que comparta una persona invitada con esta, independientemente del nombre de la reunión y de la dirección que haya usado. Se leen las notas que conserva tu Machine: las tuyas, las de la aplicación de reuniones o las que te haya enviado por correo; si no hay, se usa la transcripción o las notas del evento del calendario. Las más recientes tienen más peso y no se muestran como pendientes los temas que se hayan resuelto después.

También se tienen en cuenta las notas y los mensajes de [Historial](history.md), para que el informe incluya reuniones anteriores a tu inicio.

Un informe de trabajo no lee notas personales ni nada de la Machine de otra persona. Su contenido es solo para ti: no se incluye al delegar una tarea ni se puede enviar para revisión. Si no hay notas, esas líneas no aparecen.

El informe usa lo que ya hay en tu Machine. Si es la primera reunión con alguien de una empresa, también consulta la página de inicio del sitio web de la empresa.

Si la búsqueda web está configurada en tu Machine, también se hace una búsqueda breve en Internet sobre el nombre de la persona y la empresa. Las Machines alojadas no la incluyen; si usas tu propio ordenador, puedes configurarla en OpenClaw. Los resultados incluyen un enlace. En la búsqueda solo se envían el nombre público de la persona, el de la empresa y el sitio web, nunca tus mensajes. Los resultados se reutilizan durante 30 días.

Así, una primera reunión que hayas aceptado puede tener un informe antes de que hayáis intercambiado una palabra: qué hace su empresa, qué significa para ti y, si se sabe, quiénes son. Si solo se conoce el nombre de pila, solo se conserva lo que encuentre la búsqueda si apunta a una única persona. Si **Buscar contactos de trabajo** está desactivado (Ajustes, Seguridad), no se busca nada.

Las reuniones que se repiten solo generan un informe si ha habido novedades desde la última vez: mensajes, notas o promesas. El informe explica qué hay de nuevo, no lo que decía el anterior. Se genera cuando ya ha terminado la reunión anterior, como máximo para dos reuniones periódicas al día.

Las reuniones solo con tu equipo tienen un informe únicamente si las notas de reuniones anteriores muestran una decisión pendiente, un paso que alguien debe dar o alguna novedad. La información procede de la misma serie de reuniones o de reuniones con el mismo título en las que haya participado alguien del equipo, nunca de otra reunión con los mismos compañeros. El informe no presenta ni busca información sobre tus compañeros, y las reuniones diarias habituales no generan ninguno.

Si no hay nada útil que decir, no se crea ninguna tarea. Las reuniones personales y las que hayas rechazado no generan tareas. Si cambias la hora de una reunión, se conserva su tarea y se actualiza la hora. Una tarea descartada no vuelve a aparecer y la de una reunión cancelada se cierra automáticamente.

Si una actualización cambia el contenido de un informe, los informes de las reuniones futuras que estén abiertos se vuelven a redactar una sola vez con la nueva información. Conservan el título, las fuentes y la posición en la lista. Los informes que hayas modificado, pospuesto o cerrado no cambian; tampoco los de reuniones que empiezan dentro de unos minutos.

Los detalles de la reunión muestran su tarea en **Tarea**, a un toque de su chat.
