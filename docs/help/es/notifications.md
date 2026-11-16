---
title: Notificaciones
area: settings
summary: Qué te llega, dónde y cuándo: solo recibirás avisos de lo que no puede esperar. Lo demás se incluye en un resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4f777fac22dba7c0
---
¿Quieres recibir menos notificaciones o de otro tipo? En **Ajustes**, **Notificaciones**, elige dónde quieres recibir cada tipo:

- **Tareas nuevas**: solo lo que no puede esperar, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, una tarea que requiere que inicies sesión o una pregunta de Fleet.
- **Recordatorios**: tareas pospuestas y respuestas que estás esperando cuando vuelven a estar pendientes.
- **Resumen matutino**: un breve resumen de tu día. Más abajo encontrarás más información.
- **Resumen de la tarde**: lo que se hizo hoy y lo que queda pendiente para mañana. Más abajo encontrarás más información.

Cada tipo tiene un interruptor para **Push** (la app en tu teléfono o computadora), **Telegram** una vez configurado y **Correo** si tienes una Machine alojada o una en The Machine Network. Todo está activado, excepto los resúmenes en Telegram.

En la misma pestaña encontrarás tu **Horario laboral**: los días laborables, cuándo pueden enviarse las notificaciones, cuándo vuelven a aparecer las tareas pospuestas, los horarios de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Solo recibirás una notificación push, un aviso de Telegram o un correo electrónico si:

- una tarea vence hoy o está marcada como urgente;
- alguien está esperando una respuesta que ya está redactada y lista para enviar;
- una tarea requiere que inicies sesión;
- una tarea pospuesta vuelve a estar pendiente a la hora que elegiste.

Todo lo demás aparece discretamente en el panel (y en silencio en Telegram) y espera al resumen matutino. En un día libre, solo recibirás avisos de lo que sea urgente o venza hoy. Recibirás un máximo de 8 notificaciones push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo recibirás notificaciones

La app comprueba si estás usando el panel, no solo si está abierto:

- Si lo estás usando (está en primer plano y has hecho clic, escrito o desplazado la página en los últimos 10 minutos), no recibirás avisos. Los mensajes de Telegram llegarán en silencio. Abrir o recargar el panel no cuenta.
- Si no estás (está en segundo plano, cerrado o llevas 10 minutos sin actividad), recibirás una notificación push un minuto después de salir, salvo que vuelvas y la veas.
- Si 15 minutos después sigue sin verse y no puede esperar, recibirás un correo electrónico. Como máximo, uno por hora. No se incluirá lo que ya hayas atendido. La mayoría de los días, el resumen matutino será el único correo electrónico.
- Si un compañero de equipo te asigna una tarea y tu Machine no tiene un teléfono ni Telegram para contactarte, recibirás un correo electrónico con el título y un enlace 15 minutos después, si todavía no la has visto. Desactiva **Correo** en **Resultados y preguntas** para que no ocurra.
- Fuera de tu horario laboral, no recibirás nada. El resumen matutino incluirá la información.
- Si se crea una tarea de trabajo en un día libre, esperará hasta la hora del resumen de tu próximo día laborable. La tarea indicará cuándo recibirás la notificación, por ejemplo: «Notificación: lun., 2 nov. · 08:30».

Los cambios de progreso y las ediciones nunca generan notificaciones. Si aparece un resultado nuevo en una tarea que aún no has visto, se actualizará sin generar otra notificación. Si llegan varias notificaciones seguidas, recibirás un solo aviso. El icono de la app muestra cuántas tareas requieren tu atención.

## Botones de las notificaciones

Cada notificación tiene botones para el siguiente paso. En la app para el teléfono:

- Tarea nueva: **Hazlo**, **Posponer**, **Marcar como hecho**.
- Borrador listo: **Abrir borrador**, **Posponer**, **Marcar como hecho**.
- Resultado listo: **Abrir**, **Marcar como hecho**, **Posponer**.
- Pregunta, problema o solicitud para iniciar sesión: **Responder**, **Abrir** o **Iniciar sesión**; después, **Posponer** y **Marcar como hecho**.
- Recordatorio: **Marcar como hecho**, **Posponer**, **Abrir**.
- Resumen matutino: tócalo para abrirlo.

En el navegador y en Telegram aparecen dos botones. En las preguntas de Fleet, siempre aparecen **Responder** y **Rechazar**.

Las notificaciones no envían, pagan ni envían nada a nadie. Los borradores siempre se abren primero para que puedas revisarlos antes de enviarlos. **Abrir borrador** muestra la tarea en tu lista con el borrador completo. **Hazlo** solo inicia el trabajo en una tarea nueva.

En la app para el teléfono, **Posponer** y **Marcar como hecho** te piden que desbloquees el teléfono primero. En el navegador, abren el panel, donde se realiza la acción y aparece **Deshacer**. Al posponer una tarea, volverá a aparecer dentro de dos horas o, si es un recordatorio, a la mañana siguiente.

Los correos electrónicos incluyen enlaces para **Abrir** (y **Posponer** si algo está pendiente). Solo abren el panel.

Al tocar una notificación, o **Abrir** en un correo electrónico o en Telegram, verás la tarea resaltada en tu lista, dondequiera que esté en ese momento: **Recién hecho**, **Hecho**, **Vuelve más tarde** u otra vista. Nunca se abre el chat. Si la página todavía no se ha actualizado, seguirá la tarea cuando lo haga.

## El resumen matutino

Llega los días laborables a la hora de **Resumen matutino**, a menos que no haya nada que contar. Si esa hora es anterior a **Lo pospuesto vuelve a las**, esperará hasta 5 minutos después para incluir las tareas que vuelven a estar pendientes esa mañana. **Vista previa** te permite verlo sin enviarlo. De forma predeterminada, se envía como notificación push y por correo electrónico. Es lo bastante breve como para leerlo de un vistazo:

- un saludo con lo más importante del día, como «Buenos días, Sam. Hay 2 respuestas listas para enviar» o, si hay una sola tarea, «Buenos días, Sam. Espera tu aprobación: enviar el formulario del pedido»;
- las tareas que se mencionan en el saludo, cada una con un enlace para abrirla, y lo que vence hoy; si no, como máximo tres tareas;
- hasta cinco tareas que añadiste y que requieren tu atención, sin importar si se mencionan en el saludo;
- cuántas tareas más pueden esperar y cuánto tardarás en hacerlas a tu ritmo, por ejemplo: «Hay 12 tareas más que pueden esperar. Tardarás unos 5 min en resolverlas». Las tareas que esperan tu respuesta no se incluyen en ese tiempo. Si una tarea pospuesta vence hoy, no se cuenta hasta que vuelva a estar pendiente.
- tus reuniones, en una sola línea.

**Abrir** muestra la tarea resaltada en tu lista, incluso si ya está hecha o pospuesta. Si una promesa está vinculada a una tarea, se abre esa tarea; si todavía no tiene ninguna, se abre su propia página.

La notificación push muestra el mismo contenido, sin enlaces. Tócala o usa el enlace al final del correo electrónico para volver a leer este resumen en **Tareas**.

## El resumen de la tarde

Llega una vez en los días laborables, a la hora que aparece en **Horario laboral**. De forma predeterminada, se envía 15 minutos antes de **Hasta**, por los medios que elegiste en la fila de arriba. No recibirás ninguno si ese día no se completó ninguna tarea ni se celebró ninguna reunión. Empieza con un recuento del día, por ejemplo: «Buenas tardes, Sam. Hoy se completaron 4 tareas». Después incluye una sección de **Trabajo** y otra de **Personal**. Si una sección no tiene nada, no aparece. Cada una incluye:

- **Hecho hoy**: hasta tres tareas que tú o tu Machine completaron, seguidas de «+12 más» y las reuniones del día, por ejemplo: «+3 reuniones: llamada sobre precios y 2 más»;
- **Pendiente para mañana** (o para tu próximo día laborable si es viernes): las primeras reuniones y lo que vence.

Al final, indica cuántas tareas todavía requieren tu atención. Toca la notificación push o usa el enlace al final del correo electrónico para volver a leerlo, con **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva su fila.

## Privacidad

La notificación push va directamente desde tu Machine hasta tu dispositivo, cifrada para ese dispositivo. El correo electrónico pasa por el servidor de correo de The Machine y por tu proveedor de correo. Si [Cauteloso](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos electrónicos solo mostrarán recuentos. Desactiva **Correo** en un tipo de notificación para que no se envíe por correo electrónico.

Activa las notificaciones push para un dispositivo en **Este dispositivo** o consulta [Instalar la app](phone-app.md). La [app móvil](mobile-app.md) envía una línea de texto sin formato a través de Apple o Google y luego le pide a tu Machine el título y el siguiente paso.
