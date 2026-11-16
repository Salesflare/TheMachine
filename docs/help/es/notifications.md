---
title: Notificaciones
area: settings
summary: Qué recibes, dónde y cuándo: solo te avisamos de lo que no puede esperar; lo demás llega en un único resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: ee3ba81a8441704f
---
¿Quieres recibir menos notificaciones o cambiar cuáles recibes? En **Ajustes**, **Notificaciones**, elige dónde quieres recibir cada tipo:

- **Tareas nuevas**: solo lo que no puede esperar, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, un inicio de sesión que necesita una tarea o una pregunta de Fleet.
- **Recordatorios**: tareas pospuestas y respuestas que estás esperando y vuelven a estar pendientes.
- **Resumen matutino**: un resumen breve de tu día. Más abajo encontrarás los detalles.
- **Resumen de la tarde**: lo que hiciste hoy y lo que queda pendiente para mañana. Más abajo encontrarás los detalles.

Cada tipo tiene un interruptor para **Push** (la app en tu teléfono o computadora), **Telegram** cuando lo configures y **Correo** en una Machine alojada o en una de The Machine Network. Todo está activado, excepto los resúmenes en Telegram.

En la misma pestaña encontrarás tu **Horario laboral**: los días laborables, cuándo pueden llegar las notificaciones, cuándo vuelven las tareas pospuestas, los horarios de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Solo recibirás una notificación push, un aviso de Telegram o un correo cuando haya:

- una tarea que vence hoy o está marcada como urgente;
- una respuesta que alguien está esperando, ya redactada y lista para enviar;
- una tarea que necesita que inicies sesión;
- una tarea pospuesta que vuelve en el momento que elegiste.

Todo lo demás aparece sin avisos en el panel (y en silencio en Telegram) y espera al resumen matutino. En un día libre, solo recibirás avisos de lo urgente o de lo que vence hoy. Recibirás un máximo de 8 notificaciones push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo te avisa

Comprueba si estás usando el panel, no solo si está abierto:

- Si lo estás usando (está en primer plano y hiciste clic, escribiste o te desplazaste en los últimos 10 minutos), no recibirás avisos. Los mensajes de Telegram llegarán en silencio.
- Si no estás (está en segundo plano, cerrado o llevas 10 minutos sin actividad), recibirás una notificación push un minuto después de salir, a menos que vuelvas y la veas.
- Si sigue sin verse 15 minutos después y no puede esperar, recibirás un correo. Como máximo, uno por hora. No se incluyen las cosas que ya resolviste. La mayoría de los días, el resumen matutino es el único correo que recibes.
- Si un compañero te asigna una tarea y tu Machine no tiene un teléfono ni Telegram para contactarte, recibirás un correo con el título y un enlace 15 minutos después, si aún no la viste. Desactiva **Correo** en **Resultados y preguntas** para dejar de recibirlos.
- Fuera de tu horario laboral, no recibirás avisos. La tarea aparecerá en el resumen matutino.
- Si te asignan una tarea de trabajo en un día libre, esperará hasta la hora del resumen del siguiente día laborable. La tarea indica cuándo te llegará, por ejemplo: «Notificación lun, 2 nov · 08:30».

Los avances y las ediciones no generan notificaciones. Si aparece un resultado nuevo en una tarea que aún no viste, se actualizará sin enviar otra notificación. Si llegan varios avisos seguidos, recibirás uno solo. El ícono de la app muestra cuántas tareas necesitan tu atención.

## Botones de las notificaciones

Cada notificación tiene botones para el siguiente paso. En la app para teléfono:

- Tarea nueva: **Hazlo**, **Posponer**, **Marcar como hecho**.
- Borrador listo: **Abrir borrador**, **Posponer**, **Marcar como hecho**.
- Resultado listo: **Abrir**, **Marcar como hecho**, **Posponer**.
- Pregunta, problema o inicio de sesión: **Responder**, **Abrir** o **Iniciar sesión**; luego, **Posponer** y **Marcar como hecho**.
- Recordatorio: **Marcar como hecho**, **Posponer**, **Abrir**.
- Resumen matutino: tócalo para abrirlo.

En el navegador y en Telegram aparecen dos de esos botones. En las preguntas de Fleet, siempre aparecen **Responder una vez** y **Rechazar**.

Las notificaciones no envían, pagan ni presentan nada. Los borradores siempre se abren primero para que puedas revisarlos antes de enviarlos. **Abrir borrador** muestra la tarea en tu lista con el borrador completo. **Hazlo** solo empieza a trabajar en una tarea nueva.

En la app para teléfono, **Posponer** y **Marcar como hecho** te piden que desbloquees el teléfono primero. En el navegador, abren el panel, donde se realiza la acción y aparece la opción **Deshacer**. Al posponer una tarea, volverá en dos horas o, si es un recordatorio, a la mañana siguiente.

Los correos incluyen enlaces para **Abrir** (y **Posponer** las tareas que están esperando). Solo abren el panel.

Al tocar una notificación o **Abrir** en un correo o en Telegram, verás la tarea destacada en tu lista, dondequiera que esté ahora: **Recién hecho**, **Hecho**, **Vuelve más tarde** u otra vista. Nunca se abre el chat. Si la página aún no se había actualizado, seguirá la tarea cuando lo haga.

## El resumen matutino

Llega los días laborables a la hora de **Resumen matutino**, a menos que no haya nada que contarte. Si esa hora es anterior a **Lo pospuesto vuelve a las**, esperará hasta 5 minutos después para incluir las tareas que vuelven esa mañana. **Vista previa** te permite verlo sin enviarlo. De forma predeterminada, llega como notificación push y correo, y es lo bastante breve como para leerlo de un vistazo:

- un saludo con lo importante del día, como «Buenos días, Sam. Hay 2 respuestas listas para enviar» o, si solo hay una tarea, «Buenos días, Sam. Está listo para que lo apruebes: enviar el formulario del pedido»;
- las tareas que cuenta el saludo, cada una con un enlace para abrirla, y lo que vence hoy; si no hay nada que vence hoy, hasta tres cosas por hacer;
- hasta cinco tareas que añadiste tú y que siguen esperando que te ocupes de ellas, independientemente de lo que cuente el saludo;
- cuántas tareas más pueden esperar y cuánto tardarás en resolverlas a tu ritmo, por ejemplo: «Pueden esperar 12 más. Tardarás unos 5 min en resolverlas». Las tareas que esperan tu respuesta no se incluyen en ese tiempo, y las tareas pospuestas que vencen hoy no se cuentan hasta que vuelven a estar pendientes.
- tus reuniones, en una sola línea.

**Abrir** muestra la tarea destacada en tu lista, también si ya está hecha o pospuesta. Una promesa abre su tarea o, si todavía no tiene una, su propia página.

La notificación push muestra lo mismo, pero sin enlaces. Tócala o usa el enlace al final del correo para volver a leer este resumen en **Tareas**.

## El resumen de la tarde

Llega una vez en los días laborables, a la hora indicada en **Horario laboral**. De forma predeterminada, llega 15 minutos antes de **Hasta**, por los medios que elegiste en su fila de arriba. Si en un día no se completó ninguna tarea ni se celebró ninguna reunión, no recibirás el resumen. Empieza con un recuento del día, como «Buenas tardes, Sam. Hoy completaste 4 tareas», y después incluye una sección de **Trabajo** y otra de **Personal**. Si una sección no tiene nada, se omite. Cada una incluye:

- **Hecho hoy**: hasta tres tareas que completaste tú o tu Machine, seguidas de «+12 más» y las reuniones del día, como «+3 reuniones: llamada sobre precios y 2 más»;
- **Pendiente para mañana** (el próximo día laborable si es viernes): las primeras reuniones y lo que vence.

Al final indica cuántas tareas siguen necesitando tu atención. Toca la notificación push o el enlace al final del correo para volver a leerlo, con **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva su fila.

## Privacidad

Las notificaciones push van directamente de tu Machine a tu dispositivo y se cifran para este. El correo pasa por el servidor de correo de The Machine y tu proveedor de correo. Si [Con cautela](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo muestran recuentos. Desactiva **Correo** para un tipo de notificación para que no llegue por correo.

Activa las notificaciones push para un dispositivo en **Este dispositivo** o consulta [Instalar la app](phone-app.md). La [app móvil](mobile-app.md) recibe una línea de texto sin formato a través de Apple o Google y luego le pide a tu Machine el título y el siguiente paso.
