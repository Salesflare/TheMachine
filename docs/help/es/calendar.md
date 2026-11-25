---
title: Calendario
area: calendar
summary: La semana que tienes por delante, en un solo lugar: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9b7475608bb04e5c
---
## Qué muestra

Tus días a partir de hoy, con:

- reuniones de los calendarios que has conectado,
- tareas que vencen ese día y tareas pospuestas para el día en que vuelven,
- seguimientos del trabajo que has pasado a otras personas,
- promesas con fecha,
- [viajes y eventos](calendar.md#trips-and-events) de las reservas y entradas que recibes por correo.

Una reunión que aparece en dos calendarios solo se muestra una vez. Los eventos de un calendario que alguien haya compartido contigo aparecen atenuados, con el nombre de pila de esa persona. Nunca generan una tarea. Los eventos de todo el día y los que duran varios días aparecen como eventos de todo el día en cada uno de los días que abarcan. En Agenda, un viaje aparece primero en cada uno de sus días; en Semana y Mes, se muestra como una sola franja que los abarca, por ejemplo, «Viaje a Lisboa».

Un plan acordado entre varias personas es una sola promesa, marcada como «Con» y el nombre de la otra persona. Si una promesa está relacionada con una reunión de ese día con la misma persona, aparece en la fila de esa reunión.

**Vencida** aparece primero. Si una reunión tiene una tarea pendiente, se muestra con el estado **Preparación lista**, **Preparando** o **Tarea**. Una tarea que parece hecha, porque ya has respondido o porque la ejecución ha comprobado que está hecha, no aparece como **Vence**.

## Agenda, semana o mes

- **Agenda** muestra cada día. Desplázate hacia abajo para ver los días siguientes, o hacia arriba, o pulsa **Mostrar días anteriores**, para ver los días previos. Retrocede hasta una semana antes de que conectaras el calendario y muestra una línea en la parte superior que indica desde qué día. Cuando se haya cargado el [historial](history.md), retrocede aproximadamente un año.
- **Semana** muestra una cuadrícula de lunes a domingo. En el móvil, muestra tres días.
- **Mes** muestra el mes entero. En un ordenador se ven hasta tres elementos por día; en el móvil aparecen puntos y, al tocar uno, se muestra la lista de ese día.

**Hoy**, ‹ y ›, en la parte superior, sirven para avanzar o retroceder por las semanas o los meses. La vista que elijas se recuerda en ese dispositivo.

En la cuadrícula semanal, los eventos que coinciden en horario aparecen uno al lado del otro y siguen siendo fáciles de leer. El resto se agrupa como **+N**. Al pulsarlo, se abre ese día en la agenda.

## Abrir un elemento

Haz clic en una fila para abrir el chat de su tarea, la promesa, el viaje o evento, o la reunión. Si no puedes modificar una reunión desde aquí, por ejemplo, porque pertenece a otra persona o tiene invitados, se muestran sus detalles: cuándo es, dónde y quién participa. Las personas que conoce tu Graph, y las organizaciones y los proyectos de la reunión, enlazan a sus páginas. **Abrir en Google Calendar** (o **Abrir en Outlook**) aparece debajo y abre la reunión en ese servicio. Consultarla no cambia nada.

Si una reunión tiene reservada una sala, se muestra debajo de dónde es, nunca como persona ni en tu Graph.

El enlace de una reunión muestra el servicio correspondiente, como Zoom, Google Meet o Teams, o aparece como **Videollamada**. Abre la reunión para unirte.

## Viajes y eventos

Cuando recibes por correo una reserva de vuelo, hotel, casa de vacaciones, tren, autobús, ferry, coche de alquiler, taxi o aparcamiento en el aeropuerto, tu Machine la añade a un viaje. Las reservas de un mismo trayecto se agrupan en un solo viaje, aunque lleguen a cualquiera de tus buzones: el tren al aeropuerto, los vuelos, el coche, el alojamiento y el viaje de vuelta. Las reservas se agrupan cuando sus fechas coinciden o cuando una empieza el día en que termina la otra.

El viaje aparece como una sola franja que abarca sus días. Ábrelo para ver cada reserva en orden cronológico, con sus horarios, dirección, código de reserva y asiento.

Las entradas para un concierto, un partido, un festival o una conferencia crean un evento, uno por cada evento, con el lugar, el código de reserva, el asiento y el número de entradas. Si haces un segundo pedido para el mismo evento, se añade al mismo. Si reservas las entradas desde tu buzón de trabajo, el evento es de Trabajo; si no, es Personal. Las entradas para algo que ocurre durante un viaje se añaden al viaje.

Si aún no ha llegado la fecha del viaje, tu Machine indica lo que falta, por ejemplo, **Sin alojamiento reservado para 2 noches**, o que no hay ningún transporte reservado entre el aeropuerto y el hotel. Esas líneas aparecen atenuadas y con la etiqueta **Sin reserva**. Si el viaje no tiene ningún alojamiento, no se indica nada sobre las noches.

- Cada línea indica de quién procede la reserva, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo generó una tarea, por ejemplo, para pagar las entradas, **Abrir la tarea** la muestra.
- Si se modifica una reserva, se actualiza su línea; si se cancela, desaparece. Cuando se cancelan todas las reservas, también desaparece el viaje o el evento.
- Las reservas de otras personas, como el vuelo de un compañero que te han reenviado, no aparecen en tus viajes.

La mayoría de las confirmaciones incluyen sus datos en un formato que tu Machine puede leer sin IA. Si no es así, por ejemplo, si te han reenviado el correo o procede de un sitio de reservas pequeño, tu [modelo](model.md) lo lee en segundo plano, de unos pocos correos a la vez, y espera si estás cerca de tu límite de uso. Los correos de reservas del año que tu Machine conserva como [historial](history.md) se leen en segundo plano cuando se carga ese historial.

## Notas y transcripción de reuniones

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas. **Transcripción** recoge, palabra por palabra, lo que se dijo. Al principio aparece plegada junto con su duración; **Mostrar** la despliega.

Si no se carga, vuelve a intentarlo automáticamente durante aproximadamente medio minuto. Después, pulsa **Reintentar**.

Cada parte tiene sus propias opciones: **Añadir notas** o **Añadir transcripción**, **Subir archivo** para cargar un archivo Markdown o de texto, **Editar** y **Quitar** (pulsa dos veces). El contenido de una parte no se mezcla con el de la otra. En las reuniones que puedes modificar, la opción **Notas**, debajo del formulario, las abre.

Si has conectado [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), sus notas aparecen en Notas y su transcripción en Transcripción, con la etiqueta **De Zoom**, **De Google Meet** o **De Granola**. Nunca sustituyen lo que has añadido. Si están las dos versiones, se muestran ambas.

También puedes añadir notas al evento de calendario de la propia reunión, después de que haya empezado, o recibirlas por correo de Zoom o Gemini. Cuando termina la reunión, The Machine solo crea tareas a partir de esas notas si indican pasos siguientes claros. Si las mismas notas llegan por dos vías, se crea una sola tarea y la reunión aparece como su origen: «Origen: notas de» la reunión.

Si una reunión tiene transcripción pero no notas, aparece la opción **Generar notas**. The Machine las redacta a partir de la transcripción: un breve resumen, las decisiones y las tareas con la persona responsable, en el idioma de la reunión.

Aparece **Escribiendo notas…** y el proceso continúa aunque cierres la reunión. Si la reunión es larga, puede tardar unos minutos y se usa tu propio modelo. Las notas indican **Redactado por The Machine** y nunca sustituyen las que hayas añadido.

También puedes pedirle a The Machine que las añada. Por ejemplo, en una tarea puedes pedirle «añade esta transcripción a la reunión de hoy de la junta». La transcripción se guarda en Transcripción y el resumen, en Notas. En el Calendario, las reuniones que las tienen muestran **Notas** o **Transcripción**.

The Machine lee ambas para encontrar tareas de seguimiento de la reunión. Son de Trabajo o Personales, igual que la reunión, y solo se comparten con tu equipo si la reunión también se comparte.

La reunión muestra estos detalles estés donde estés: en una cronología, en una búsqueda de mensajes o como origen de una tarea. **Invitación original**, al final, muestra la invitación tal como llegó.

## Añadir o cambiar un evento

Desde aquí puedes modificar tu propio calendario de Google. Outlook y los demás calendarios solo se pueden consultar. **Nuevo evento** añade uno (en el móvil, está bajo **+** en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento sin invitados de ese calendario para modificarlo o **Eliminar** (pulsa dos veces).

Al escribir en **Dónde**, se sugieren lugares: primero los que ya has usado y tus organizaciones, y después direcciones de [OpenStreetMap](https://www.openstreetmap.org), un mapa gratuito. Solo se envían las palabras que escribes para buscar el lugar. Elige una sugerencia o conserva tu propio texto.

**Invitar** añade a personas de tu Graph o cualquier dirección de correo. Esta opción solo aparece en tu propio calendario. Encima del botón se muestra quién recibirá una invitación, y el botón indica cuántas personas son: **Añadir e invitar a 2 personas**. Google envía las invitaciones cuando pulsas el botón, no antes. Si no hay invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede sugerir un cambio, como añadir una recogida. Se muestra exactamente qué cambiaría y solo se hace si pulsas **Añadir**, **Guardar** o **Eliminar**.

¿Aún no tienes reuniones? Si no tienes un calendario conectado, **Conecta tu calendario** abre Conexiones, donde puedes conectar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) u [otro calendario](other-calendars.md).

## Conflictos con tu otro calendario

Si una reunión de trabajo coincide con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el evento más reciente. Puede redactar una nota breve para cambiarlo de horario u ofrecerse a rechazarlo. No se envía nada hasta que lo apruebes.

Si un evento coincide con varios, se crea una sola tarea sobre ese evento. Si hay otra coincidencia mientras sigue pendiente, se añade a la misma tarea. Cuando la completas o la descartas, solo vuelve a aparecer si más adelante creas o cambias una reunión.

Los eventos de todo el día, los que muestran disponibilidad y los provisionales no cuentan, y cada conflicto solo se muestra una vez. Tampoco cuentan la ubicación de trabajo, el tiempo de concentración ni la ausencia de la oficina de Google. Lo mismo ocurre con un bloque tuyo que incluye otras reuniones, como un día en la oficina: solo pueden entrar en conflicto las reuniones que contiene. Un bloque sin otras personas ni reuniones, como un vuelo, sí puede entrar en conflicto con un evento en el que haya más gente.

Una tarea de Trabajo solo indica que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú ves con qué entra en conflicto: los dos primeros y, después, cuántos más hay. Una tarea en la que no hayas hecho nada se cierra automáticamente si su conflicto aparece en otra tarea o si resulta que no había conflicto.

## Preparación para tus reuniones

Antes de una reunión con personas ajenas a tu empresa, The Machine crea una tarea: **Preparar la reunión**. Es un informe breve:

- **Quién:** quiénes son, según tu Graph, con información de sus antecedentes cuando se conoce.
- **Organización:** a qué se dedica su empresa, para quién y a qué precio, si es importante para la reunión.
- **Hasta ahora:** qué habéis hablado, preguntado y ofrecido, y en qué punto estáis. Después de la reunión, esos mensajes aparecen como fuentes de la tarea.
- **Acordado anteriormente:**, **Cambios desde entonces:** y **Aún pendiente:** lo que surgió en reuniones anteriores con las mismas personas, con la reunión o el mensaje de origen en cada línea.
- **Promesas pendientes:** lo que aún os debéis, según las promesas de tu Machine.
- **Preguntas pendientes:** lo que aún no tiene respuesta.
- **Decidir o llevar:** qué hay que resolver o llevar, y qué les puede interesar.

Se crea la mañana de un día laborable: el mismo día de la reunión si es por la tarde; si no, el día laborable anterior. Solo sirve para consultar la información: márcala como **Hecho** cuando la hayas leído. Si contiene una promesa o una pregunta que requiere una acción, tiene su propia tarea.

Se tienen en cuenta las reuniones anteriores en las que haya participado alguien de fuera, sean cuales sean el nombre de la reunión y la dirección que haya usado esa persona. Lee las notas que tiene tu Machine: las tuyas, las de la aplicación de reuniones o las que te haya enviado por correo; si no hay, lee la transcripción o las notas del evento del calendario. Da más importancia a las más recientes y no muestra como pendiente un asunto que se haya resuelto después.

También se tienen en cuenta las notas y los mensajes del [Historial](history.md), para que el informe incluya las reuniones anteriores a tu primer día.

Los informes de trabajo no leen notas personales ni información de la Machine de otra persona. Su contenido es solo para ti: no se incluye al pasar una tarea a otra persona y no se puede enviar para que la revisen. Si no hay notas, no aparecen esas secciones.

Usa la información que ya está en tu Machine. Si es tu primera reunión con alguien de una empresa, también lee la página principal del sitio web de la empresa.

Si la búsqueda web está configurada en tu Machine, también busca brevemente en la web el nombre de la persona y el de su empresa. Las Machine alojadas no incluyen esta función; si usas tu propio ordenador, puedes configurarla en OpenClaw. Los resultados incluyen un enlace. La búsqueda solo recibe el nombre público de la persona, el nombre de la empresa y su sitio web, nunca tus mensajes. Los resultados se reutilizan durante 30 días.

Así, puedes recibir un informe antes de haber intercambiado una palabra, incluso para una primera reunión a la que hayas aceptado asistir: qué hace la empresa, qué significa para ti y, si se sabe, quién es la otra persona. Si solo tienes su nombre de pila, conserva los resultados únicamente si apuntan a una sola persona. Si **Buscar contactos de trabajo** está desactivado en Ajustes, en Seguridad, no se realiza ninguna búsqueda.

Si una reunión es recurrente, solo se crea un informe cuando hay novedades desde la última vez: un mensaje, notas o una promesa. Indica lo nuevo, no lo que ya decía el informe anterior. Se crea cuando termina la reunión anterior y, como máximo, para dos reuniones recurrentes al día.

Si no hay nada útil que decir, no se crea ninguna tarea. Las reuniones internas, personales y rechazadas no generan tareas. Si se cambia la hora de una reunión, su tarea se mantiene con la nueva hora. Si descartas la tarea, no vuelve a aparecer; si se cancela la reunión, la tarea se cierra automáticamente.

Si una actualización cambia el contenido de un informe, se vuelve a redactar una sola vez el de las reuniones que aún no han empezado. Se mantienen el título, las fuentes y el lugar en la lista. Los informes que hayas modificado, pospuesto o cerrado no cambian. Tampoco cambia el de una reunión que vaya a empezar en los próximos minutos.

Los detalles de la reunión muestran su tarea en **Tarea**, a un toque de su chat.
