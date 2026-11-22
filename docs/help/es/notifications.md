---
title: Notificaciones
area: settings
summary: Qué te llega, dónde y cuándo: solo te avisamos de lo que no puede esperar; el resto llega en un único resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4a782ad03270e7b0
---
¿Quieres menos notificaciones o recibir otras? En **Ajustes**, **Notificaciones**, elige dónde quieres recibir cada tipo:

- **Tareas nuevas**: solo lo que no puede esperar, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, una tarea que necesita que inicies sesión o una pregunta de Fleet.
- **Recordatorios**: tareas pospuestas y respuestas que estás esperando y vuelven a aparecer.
- **Resumen matutino**: un breve resumen de tu día. Más abajo tienes los detalles.
- **Resumen de la tarde**: lo que has hecho hoy y lo que queda pendiente para mañana. Más abajo tienes los detalles.

Cada tipo tiene un interruptor para **Push** (la app en tu móvil u ordenador), **Telegram** cuando lo hayas configurado y **Correo** si usas una Machine alojada o una de The Machine Network. Todo está activado, excepto los resúmenes en Telegram.

En la misma pestaña están tus **Horario laboral**: los días laborables, cuándo pueden llegarte notificaciones, cuándo vuelven a aparecer las tareas pospuestas, las horas de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Solo recibirás una notificación push, un aviso de Telegram o un correo por estos motivos:

- una tarea que vence hoy o está marcada como urgente;
- una respuesta que alguien está esperando, ya redactada y lista para enviar;
- una tarea que necesita que inicies sesión;
- una tarea pospuesta que vuelve a aparecer a la hora que elegiste.

Todo lo demás aparece discretamente en el panel (y en silencio en Telegram) y espera al resumen matutino. En un día libre, solo recibirás avisos de lo urgente o de lo que vence hoy. Como máximo, recibirás 8 notificaciones push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo llegan las notificaciones

La app comprueba si estás usando el panel, no solo si está abierto:

- Si lo estás usando (está en primer plano y has hecho clic, escrito o desplazado la página en los últimos 10 minutos), no recibirás avisos. Telegram llegará en silencio. Abrirlo o recargarlo no cuenta.
- Si no estás (está en segundo plano, cerrado o llevas 10 minutos sin usarlo), recibirás una notificación push un minuto después de salir, salvo que vuelvas y la veas.
- Si 15 minutos después aún no la has visto y no puede esperar, recibirás un correo sobre ello, como máximo uno por hora. No se incluyen las cosas que ya has atendido. La mayoría de los días, el resumen matutino será el único correo.
- Si un compañero te asigna una tarea y tu Machine no tiene un teléfono o Telegram para avisarte, recibirás un correo con el título y un enlace, 15 minutos después si aún no la has visto. Desactiva **Correo** en **Resultados y preguntas** para que no te llegue.
- Fuera de tu horario laboral no recibirás nada. Se incluirá en el resumen matutino.
- Una tarea nueva de trabajo en un día libre esperará hasta la hora del resumen del siguiente día laborable. La tarea indica cuándo te llegará, por ejemplo: Notificación lun, 2 nov · 08:30.

Los cambios de progreso y las ediciones no generan notificaciones. Si aparece un resultado nuevo en una tarea que aún no has visto, se actualizará sin enviarte otra notificación. Si llegan varias a la vez, recibirás un solo aviso. El icono de la app muestra cuántas tareas requieren tu atención.

## Botones de las notificaciones

Cada notificación tiene botones para dar el siguiente paso. En la app para móvil:

- Tarea nueva: **Hazlo**, **Pospón**, **Marcar como hecho**.
- Borrador listo: **Abrir borrador**, **Pospón**, **Marcar como hecho**.
- Resultado listo: **Abrir**, **Marcar como hecho**, **Pospón**.
- Pregunta, tarea bloqueada o solicitud para iniciar sesión: **Responder**, **Abrir** o **Iniciar sesión**; después, **Pospón** y **Marcar como hecho**.
- Recordatorio: **Marcar como hecho**, **Pospón**, **Abrir**.
- Resumen matutino: tócalo para abrirlo.

En el navegador y en Telegram aparecen dos de esos botones. En las preguntas de Fleet, también están **Responder una vez** y **Rechazar**.

No se envía, paga ni presenta nada desde una notificación. Los borradores siempre se abren primero para que los veas antes de que se envíen. **Abrir borrador** muestra la tarea en tu lista con el borrador completo. **Hazlo** solo inicia el trabajo en una tarea nueva.

En la app para móvil, tendrás que desbloquear el dispositivo antes de usar **Pospón** o **Marcar como hecho**. En el navegador, se abre el panel, donde se aplica la acción y aparece **Deshacer**. Al posponer una tarea, volverá a aparecer dentro de dos horas o, si es un recordatorio, mañana por la mañana.

Los correos tienen enlaces para abrir la tarea y, si está pendiente, para posponerla. Solo abren el panel.

Al tocar una notificación o seleccionar **Abrir** en un correo o en Telegram, verás la tarea resaltada en tu lista, esté donde esté ahora: **Recién hecho**, **Hecho**, **Vuelve más tarde** u otra vista. Nunca se abre el chat. Si la página aún no se había actualizado, seguirá mostrando la tarea cuando lo haga.

## El resumen matutino

Lo recibirás los días laborables a la hora de **Resumen matutino**, salvo que no haya nada que contar. Si esa hora es anterior a **Lo pospuesto vuelve a las**, el resumen esperará hasta 5 minutos después, para incluir las tareas que vuelven a aparecer esa mañana. **Vista previa** te permite verlo sin enviarlo. De forma predeterminada, llega como notificación push y correo, y es lo bastante breve para leerlo de un vistazo:

- un saludo con lo más importante del día, como «Buenos días, Sam. Hay 2 respuestas listas para enviar» o, si hay una sola tarea, «Buenos días, Sam. Necesitas dar el visto bueno: Enviar el formulario del pedido». Solo cuentan como listas para revisar las tareas que tienen un borrador o un resultado pendiente de aprobación. Las que necesitan primero tu respuesta no cuentan;
- las tareas que se mencionan en el saludo, cada una con un enlace para abrirla, y lo que vence hoy; si no, como máximo tres tareas;
- hasta cinco tareas que hayas añadido y estén pendientes de ti, independientemente de las que se mencionen en el saludo;
- cuántas más pueden esperar y cuánto tardarás en resolverlas a tu ritmo, por ejemplo: «Quedan 12 que pueden esperar. Tardarás unos 5 min en resolverlas». Las tareas pendientes de tu respuesta no se incluyen en ese tiempo. Tampoco se cuenta una tarea que vence hoy pero está pospuesta hasta más tarde, ni una en la que The Machine siga trabajando, hasta que quede pendiente de ti. El total coincide con las tareas pendientes de tu lista.
- tus reuniones, en una sola línea.

**Abrir** muestra la tarea resaltada en tu lista, aunque esté hecha o pospuesta. Una promesa abre su tarea o, si aún no tiene una, su propia página.

La notificación push muestra lo mismo, sin enlaces. Tócala o selecciona el enlace al final del correo para volver a leer el resumen en **Tareas**.

## El resumen de la tarde

Lo recibirás una vez cada día laborable, a la hora indicada en **Horario laboral**. De forma predeterminada, llega 15 minutos antes de **Hasta**, por los medios que hayas elegido en la fila de arriba. Solo llega los días en que hayas estado: si has usado el panel o has tomado una decisión sobre una tarea allí, en Telegram, en el chat o por voz. No recibirás ninguno si ese día no has terminado ninguna tarea ni has tenido reuniones.

Empieza con un recuento del día, como «Buenas tardes, Sam. Has terminado 4 tareas hoy»; después aparecen las secciones **Trabajo** y **Personal**. Si una sección no tiene contenido, no aparece. Cada una incluye:

- **Hecho hoy**: hasta tres tareas que tú o tu Machine hayan terminado, seguido de «+12 más» y las reuniones del día, por ejemplo, «+3 reuniones: llamada sobre precios y 2 más»;
- **Pendiente para mañana** (o para el próximo día laborable si es viernes): las primeras reuniones y lo que vence.

Al final indica cuántas tareas siguen pendientes de ti. Toca la notificación push o el enlace al final del correo para volver a leerlo, con **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva la fila correspondiente.

## Privacidad

Las notificaciones push van directamente de tu Machine a tu dispositivo y están cifradas para él. El correo pasa por el servidor de correo de The Machine y por tu proveedor de correo. Si [Cuidado](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo muestran recuentos. Desactiva **Correo** para un tipo de notificación si no quieres recibirlo por correo.

Activa las notificaciones push para un dispositivo en **Este dispositivo** o consulta [Instalar la app](phone-app.md). La [app para móvil](mobile-app.md) envía una línea sencilla a través de Apple o Google y luego le pide a tu Machine el título y el siguiente paso.
