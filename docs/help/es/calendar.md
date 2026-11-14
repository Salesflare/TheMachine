---
title: Calendario
area: calendar
summary: La semana que viene en un solo sitio: reuniones, tareas que vencen, tareas pospuestas y promesas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 0f6b54ba94a7cdcc
---
## Qué muestra

Tus días a partir de hoy, con:

- las reuniones de los calendarios que conectaste,
- las tareas que vencen ese día, y las tareas pospuestas el día en que vuelven,
- los seguimientos del trabajo que pasaste,
- las promesas con fecha.

Una reunión que está en dos calendarios aparece una vez. Un calendario que alguien compartió contigo muestra sus eventos atenuados, con su nombre de pila; esos nunca crean una tarea. Los eventos de todo el día y de varios días aparecen como de todo el día, en cada día que abarcan.

Un plan hecho en común es una sola promesa, marcada "Con" y su nombre. Una promesa sobre una reunión de ese día con la misma persona va en la fila de esa reunión.

**Vencida** sale primero. Una reunión con una tarea abierta la muestra: **Preparación lista**, **Preparando** o **Tarea**. Una tarea que parece hecha (ya respondiste, o su ejecución la encontró hecha) no aparece como **Vence**.

## Agenda, semana o mes

- **Agenda** lista cada día. Desplázate hacia abajo para ver días posteriores, o hacia arriba (o **Mostrar días anteriores**) para los anteriores. Llega hasta una semana antes de que conectaras tu calendario, y una línea arriba dice desde qué día. Cuando llega su [historial](history.md), llega a un año atrás.
- **Semana** muestra una cuadrícula, de lunes a domingo. En un móvil muestra tres días.
- **Mes** muestra el mes entero. Un ordenador muestra hasta tres elementos por día; un móvil muestra puntos, y al tocar un día se lista.

**Hoy**, ‹ y › arriba recorren las semanas o los meses. La vista que eliges se recuerda en ese dispositivo.

En la cuadrícula de la semana, los eventos a la misma hora se colocan uno al lado del otro y cada uno sigue siendo legible. El resto aparecen como **+N**, que abre ese día en la agenda.

## Abre algo

Haz clic en una fila para abrir el chat de su tarea, la promesa o la reunión en su propio calendario. En una reunión, alguien que tu Graph conoce, y las organizaciones y proyectos de los que trata, son enlaces a su página. Mirar no cambia nada.

Una sala de reuniones reservada aparece en el lugar, nunca como persona ni en tu Graph.

Un enlace de reunión aparece como su servicio, como Zoom, Google Meet o Teams, o como **Videollamada**. Abre la reunión para unirte.

## Notas y transcripción de la reunión

Los detalles de una reunión tienen dos partes. **Notas** es el resumen: decisiones y tareas. **Transcripción** es lo que se dijo, palabra por palabra. Empieza plegada, con su duración; **Mostrar** la abre.

Si no cargan (por ejemplo, mientras tu Machine se reinicia), la reunión lo vuelve a intentar sola durante unos treinta segundos, y otra vez cuando vuelves a la ventana. Después lo dice, con **Reintentar**.

Cada una tiene su propio **Añadir notas** o **Añadir transcripción**, **Subir archivo** para un archivo Markdown o de texto, **Editar** y **Quitar** (toca dos veces). Lo que va en una se queda ahí. En una reunión que puedes cambiar, **Notas** debajo de su formulario las abre.

Con [Zoom](zoom.md) o [Google Meet](google-meet.md) conectado, sus notas aparecen en Notas y su transcripción en Transcripción, marcadas **De Zoom** o **De Google Meet**. Nunca reemplazan lo que añadiste: cuando están los dos, se ven los dos.

Las notas también pueden estar en el propio evento del calendario, añadidas después de que empezara, o llegar por correo de Zoom o Gemini. Después de la reunión, The Machine solo crea to-dos con ellas para próximos pasos claros. Las mismas notas que llegan de dos formas crean un solo to-do, con la reunión como origen: **Notas de** la reunión.

Una reunión con transcripción y sin notas tiene **Generar notas**. The Machine las escribe a partir de la transcripción: un resumen corto, las decisiones y las tareas con quién las hace, en el idioma de la reunión.

The Machine muestra **Escribiendo notas…** y sigue aunque cierres la reunión; una larga tarda unos minutos. Usa tu propio modelo y espera si llegas a tu límite de uso. Las notas dicen **Escritas por The Machine**, nunca reemplazan las que añadiste, y los seguimientos salen de ellas como de las de Zoom.

The Machine también puede añadirlas. Pídeselo en una tarea, como "añade esta transcripción a la reunión del consejo de hoy". Una transcripción va en Transcripción, un resumen en Notas. Una reunión con ellas muestra **Notas** o **Transcripción** en el calendario.

The Machine lee las dos para los siguientes pasos de la reunión. Son de Trabajo o Personales como la reunión, y solo van a tu equipo cuando la reunión va.

Una reunión se abre con estos detalles dondequiera que la encuentres: en una cronología, en una búsqueda de mensajes o como fuente de una tarea. **Invitación original** abajo muestra la invitación tal como llegó.

## Añade o cambia un evento

Cuando un calendario se puede cambiar desde aquí, **Nuevo evento** añade uno (en un teléfono está en **+**, en la barra superior): elige el calendario, un título y la hora. Haz clic en un evento sin invitados de ese calendario para cambiarlo, o **Eliminar** (toca dos veces).

**Dónde** sugiere lugares mientras escribes: primero los que ya usaste y tus organizaciones, y luego direcciones de [OpenStreetMap](https://www.openstreetmap.org) a través de Photon, un buscador de mapas gratuito. Tu Machine se lo pregunta solo con las palabras que escribiste. Elige uno o deja tu propio texto.

**Invitar** añade personas de tu Graph, o cualquier dirección de correo. Solo está en tu propio calendario. Quién recibe una invitación aparece encima del botón, y el botón dice cuántas: **Añadir e invitar a 2**. Google envía las invitaciones cuando lo tocas, no antes. Sin invitados, nadie recibe una invitación ni una actualización.

Una tarea también puede ofrecer un cambio, como añadir una recogida. Muestra exactamente qué cambia, y solo tu **Añadir**, **Guardar** o **Eliminar** lo hace.

¿Aún no hay reuniones? Sin calendario, **Conecta tu calendario** abre Conexiones: conecta [Google Calendar](google-calendar.md), el [Calendario de Outlook](microsoft.md) u [otro calendario](other-calendars.md).

## Coincidencias con tu otro calendario

Cuando una reunión de trabajo se solapa con algo de tu calendario personal, o al revés, The Machine crea una tarea sobre el más reciente de los dos. Puede preparar un borrador corto para moverlo, u ofrecer rechazarlo. No se envía nada hasta que lo apruebes.

Los eventos de todo el día, libres o provisionales nunca cuentan, y cada coincidencia aparece una sola vez. Una tarea de Trabajo solo dice que hay un conflicto, así que tu equipo nunca ve el evento personal. Solo tú ves con qué coincide.

## Listo para tus reuniones

Antes de una reunión con personas de fuera de tu empresa, The Machine crea una tarea: **Preparar** la reunión. Es un resumen corto:

- **Quién:** quiénes son, según tu Graph.
- **Último contacto:** tu último intercambio con ellos. Ese mensaje es la fuente de la tarea, después de la reunión.
- **Promesas pendientes:** lo que tú o ellos aún deben.
- **Preguntas pendientes:** lo que sigue sin respuesta.
- **Decidir o llevar:** lo que hay que decidir o llevar.

Llega la mañana de un día laborable: el mismo día si la reunión es por la tarde, si no el día laborable anterior. Solo usa lo que ya está en tu Machine. Es solo para leer: **Hecho** cuando la leas. Una promesa o pregunta que pida algo tiene su propia tarea.

Sin historial útil, no hay tarea. Las reuniones recurrentes, internas, personales y rechazadas no tienen. Una reunión que se mueve conserva su única tarea, a la nueva hora. Una descartada no vuelve, y la de una reunión cancelada se cierra sola.

Los detalles de la reunión muestran su tarea en **Tarea**, a un toque del chat.
