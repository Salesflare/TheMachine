---
title: Notificaciones
area: settings
summary: Qué te llega, dónde y cuándo: solo lo que no puede esperar te avisa al momento; lo demás va en un único resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 334224e0b479ef47
---
¿Quieres recibir menos notificaciones o recibir otras? En **Ajustes**, **Notificaciones**, elige dónde quieres recibir cada tipo:

- **Tareas nuevas**: solo lo que no puede esperar, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, una tarea que requiere iniciar sesión o una pregunta de Fleet.
- **Recordatorios**: tareas pospuestas y respuestas que estás esperando cuando vuelven a aparecer.
- **Resumen matutino**: un breve resumen de tu día. Consulta más abajo.
- **Resumen de la tarde**: lo que has hecho hoy y lo que queda pendiente para mañana. Consulta más abajo.

Cada tipo tiene un interruptor para **Push** (la app en tu teléfono u ordenador), **Telegram** cuando esté configurado y **Correo** en una Machine alojada o en una Machine de The Machine Network. Todas las opciones están activadas, excepto los resúmenes en Telegram.

En la misma pestaña encontrarás tu **Horario laboral**: los días laborables, cuándo pueden enviarse las notificaciones, cuándo vuelven a aparecer las tareas pospuestas, las horas de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Solo recibirás una notificación push, un aviso de Telegram o un correo por:

- una tarea que vence hoy o está marcada como urgente;
- una respuesta que alguien está esperando, ya redactada y lista para enviar;
- una tarea que requiere que inicies sesión;
- una tarea pospuesta que vuelve a aparecer a la hora que elegiste.

Todo lo demás aparece discretamente en el panel (y sin sonido en Telegram) y espera al resumen matutino. En un día libre, solo te avisamos de lo urgente o de lo que vence hoy. Recibirás como máximo 8 notificaciones push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo te avisa

La app comprueba si estás usando el panel de verdad, no solo si está abierto:

- Si lo estás usando (está en primer plano y has hecho clic, escrito o desplazado la página en los últimos 10 minutos), no suena nada. Telegram llega sin sonido.
- Si no estás (está en segundo plano, cerrado o inactivo durante 10 minutos), recibirás una notificación push un minuto después de salir, a menos que vuelvas y la veas.
- Si sigue sin verse 15 minutos después y no puede esperar, recibirás un correo. Como máximo, uno por hora. No se incluyen las cosas que ya hayas resuelto. La mayoría de los días, el resumen matutino es el único correo que recibes.
- Si un compañero te asigna una tarea y tu Machine no tiene un teléfono ni Telegram para contactarte, recibirás un correo con el título y un enlace 15 minutos después, si aún no la has visto. Desactiva **Correo** en **Resultados y preguntas** para evitarlo.
- Fuera de tu horario laboral, no se envía nada. La tarea aparecerá en el resumen matutino.
- Si recibes una tarea nueva de trabajo en un día libre, esperará hasta la hora del resumen de tu próximo día laborable. La tarea indica cuándo te llegará, por ejemplo: «Notificación: lun., 2 nov. · 08:30».

Los avances y las ediciones no generan notificaciones. Si aparece un resultado nuevo en una tarea que aún no has visto, se actualiza sin enviar otra notificación. Si llegan varias a la vez, recibirás un solo aviso. El icono de la app muestra cuántas tareas requieren tu atención.

## Botones de las notificaciones

Cada notificación tiene botones para que puedas dar el siguiente paso. En la app para el teléfono:

- Tarea nueva: **Hazlo**, **Posponer**, **Marcar como hecho**.
- Borrador listo: **Abrir borrador**, **Posponer**, **Marcar como hecho**.
- Resultado listo: **Abrir**, **Marcar como hecho**, **Posponer**.
- Pregunta, bloqueo o solicitud para iniciar sesión: **Responder**, **Abrir** o **Iniciar sesión**; también **Posponer** y **Marcar como hecho**.
- Recordatorio: **Marcar como hecho**, **Posponer**, **Abrir**.
- Resumen matutino: tócalo para abrirlo.

En el navegador y en Telegram aparecen dos de esos botones. Las preguntas de Fleet siempre incluyen **Responder una vez** y **Rechazar**.

No se envía, paga ni presenta nada desde una notificación. Los borradores siempre se abren primero para que los revises antes de que se envíen. **Abrir borrador** muestra la tarea en tu lista con el borrador completo. **Hazlo** solo inicia el trabajo de una tarea nueva.

En la app para el teléfono, **Posponer** y **Marcar como hecho** te piden que desbloquees el teléfono primero. En el navegador, abren el panel, donde se realiza la acción y aparece la opción **Deshacer**. Al posponer una tarea, volverá a aparecer dentro de dos horas o, si es un recordatorio, a la mañana siguiente.

Los correos incluyen enlaces para **Abrir** y, en el caso de lo que estés esperando, para **Posponer**. Solo abren el panel.

Al tocar una notificación, o **Abrir** en un correo o en Telegram, verás la tarea resaltada en tu lista. Si ya está hecha, pospuesta o en otra vista, se abrirá su chat.

## El resumen matutino

Lo recibirás los días laborables a la hora de **Resumen matutino**, a menos que no haya nada que contar. Si esa hora es anterior a **Lo pospuesto vuelve a las**, esperará hasta 5 minutos después para incluir las tareas que vuelvan a aparecer esa mañana. **Vista previa** te permite verlo sin enviarlo. De forma predeterminada, se envía como notificación push y por correo, y es lo bastante breve como para leerlo de un vistazo:

- un saludo con lo más importante del día, como «Buenos días, Sam. Hay 2 respuestas listas para enviar» o, si hay una sola tarea, «Buenos días, Sam. En espera de tu visto bueno: enviar el formulario de pedido»;
- las tareas que menciona el saludo, cada una con un enlace **Abrir**, y lo que vence hoy; si no hay nada que venza hoy, como máximo tres tareas;
- cuántas tareas más pueden esperar y cuánto tardarías en resolverlas a tu ritmo, por ejemplo: «Hay 12 más que pueden esperar. Te llevará unos 5 min resolverlas». No se incluye el tiempo de las tareas que esperan tu respuesta.
- tus reuniones, en una sola línea.

**Abrir** muestra la tarea resaltada en tu lista. Si ya está hecha, pospuesta o en otra vista, se abrirá su chat. Una promesa abre su tarea o, si aún no tiene una, su propia página.

La notificación push muestra lo mismo, pero sin enlaces. Tócala o usa el enlace al final del correo para volver a leer este resumen en **Tareas**.

## El resumen de la tarde

Lo recibirás una vez cada día laborable, a la hora indicada en **Horario laboral**. De forma predeterminada, llega 15 minutos antes de **Hasta** y por los medios que hayas elegido en la fila de arriba. Si no has terminado ninguna tarea ni has tenido reuniones ese día, no recibirás el resumen. Empieza con un recuento del día, como «Buenas tardes, Sam. Has completado 4 tareas hoy», y luego incluye una parte de **Trabajo** y otra de **Personal**. Si una parte está vacía, no aparece. Cada una incluye:

- **Hecho hoy**: hasta tres tareas que hayas completado tú o tu Machine, luego «+12 más» y las reuniones del día, como «+3 reuniones: llamada sobre precios y 2 más»;
- **Pendiente para mañana** (o para el próximo día laborable si es viernes): las primeras reuniones y lo que vence.

Al final indica cuántas tareas aún requieren tu atención. Toca la notificación push o el enlace al final del correo para volver a leerlo, con **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva su fila.

## Privacidad

Las notificaciones push van directamente desde tu Machine a tu dispositivo, cifradas para este. El correo pasa por el servidor de correo de The Machine y tu proveedor de correo. Si [Cuidadoso](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo muestran recuentos. Desactiva **Correo** en un tipo de notificación para que no llegue por correo.

Activa las notificaciones push de un dispositivo en **Este dispositivo** o consulta [Instalar la app](phone-app.md). La [app móvil](mobile-app.md) envía una línea de texto simple a través de Apple o Google y luego le pide a tu Machine el título y el siguiente paso.
