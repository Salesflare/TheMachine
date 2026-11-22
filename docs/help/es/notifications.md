---
title: Notificaciones
area: settings
summary: Qué te llega, dónde y cuándo: solo te avisamos de lo que no puede esperar; el resto va en un resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: aab523e3a774400b
---
¿Quieres menos notificaciones o recibirlas de otra forma? En **Ajustes**, **Notificaciones**, elige dónde recibir cada tipo:

- **Tareas nuevas**: solo las que no pueden esperar, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, un inicio de sesión que necesita una tarea o una pregunta de Fleet.
- **Recordatorios**: tareas pospuestas y respuestas que estás esperando y vuelven a aparecer.
- **Resumen matutino**: un resumen breve de tu día. Consulta más abajo.
- **Resumen de la tarde**: lo que has hecho hoy y lo que queda pendiente para mañana. Consulta más abajo.

Cada tipo tiene un interruptor para **Push** (la app del teléfono o del ordenador), **Telegram** cuando esté configurado y **Correo** si tienes una Machine alojada o una en The Machine Network. Todas las opciones están activadas, excepto los resúmenes en Telegram.

Tu **Horario laboral** está en la misma pestaña: los días laborables, cuándo pueden enviarse las notificaciones, cuándo vuelven a aparecer las tareas pospuestas, las horas de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Recibirás una notificación push, un aviso de Telegram o un correo solo si:

- una tarea vence hoy o está marcada como urgente;
- alguien espera una respuesta que ya está redactada y lista para enviar;
- una tarea necesita que inicies sesión;
- una tarea pospuesta vuelve a aparecer a la hora que elegiste.

Todo lo demás aparece discretamente en el panel (y sin sonido en Telegram) y espera al resumen matutino. En un día libre, solo recibirás avisos de lo urgente o de lo que vence hoy. Como máximo, recibirás 8 notificaciones push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo te avisa

Comprueba si estás usando el panel, no solo si está abierto:

- Si lo estás usando (está en primer plano y has hecho clic, escrito o desplazado la página en los últimos 10 minutos), no recibirás avisos. Los mensajes de Telegram llegan sin sonido. Abrir o recargar el panel no cuenta.
- Si no estás (el panel está en segundo plano, cerrado o lleva 10 minutos inactivo), recibirás una notificación push un minuto después de irte, a menos que vuelvas y la veas.
- Si sigue sin verse 15 minutos después y no puede esperar, recibirás un correo, como máximo uno por hora. Se omite lo que ya hayas gestionado. La mayoría de los días, el resumen matutino es el único correo.
- Si un compañero te asigna una tarea y tu Machine no tiene un teléfono ni Telegram para avisarte, recibirás un correo con el título y un enlace 15 minutos después, si aún no la has visto. Desactiva **Correo** en **Resultados y preguntas** para que no ocurra.
- Fuera de tu horario laboral, no recibirás avisos. La tarea aparecerá en el resumen matutino.
- Una tarea nueva de trabajo en un día libre espera hasta la hora del resumen de tu próximo día laborable. La tarea muestra cuándo te llegará, por ejemplo: Notificación lun, 2 nov · 08:30.

Los cambios y el progreso nunca generan avisos. Si aparece un resultado nuevo para una tarea que aún no has visto, se actualizará sin generar otra notificación. Si llegan varios avisos seguidos, recibirás uno solo. El icono de la app muestra cuántas tareas requieren tu atención.

## Botones de las notificaciones

Cada notificación tiene botones para el siguiente paso. En la app para el teléfono:

- Tarea nueva: **Hazlo**, **Posponer**, **Marcar como hecha**.
- Borrador listo: **Abrir borrador**, **Posponer**, **Marcar como hecha**.
- Resultado listo: **Abrir**, **Marcar como hecha**, **Posponer**.
- Pregunta, problema o inicio de sesión: **Responder**, **Abrir** o **Iniciar sesión**, y después **Posponer** y **Marcar como hecha**.
- Recordatorio: **Marcar como hecha**, **Posponer**, **Abrir**.
- Resumen matutino: tócalo para abrirlo.

El navegador y Telegram muestran dos de esos botones. En las preguntas de Fleet siempre aparecen **Responder** y **Rechazar**.

No se envía, paga ni presenta nada desde una notificación. Los borradores siempre se abren primero para que los veas antes de enviarlos. **Abrir borrador** muestra la tarea en tu lista con el borrador completo. **Hazlo** solo inicia el trabajo de una tarea nueva.

En la app para el teléfono, **Posponer** y **Marcar como hecha** te piden que desbloquees el dispositivo primero. En el navegador, abren el panel, donde se realiza la acción y se muestra **Deshacer**. **Posponer** hace que la tarea vuelva a aparecer en dos horas o, si es un recordatorio, mañana por la mañana.

Los correos incluyen enlaces para **Abrir** (y **Posponer** si algo está pendiente). Solo abren el panel.

Si tocas una notificación o **Abrir** en un correo o en Telegram, verás la tarea resaltada en tu lista, dondequiera que esté ahora: **Recién hecho**, **Hecho**, **Vuelve más tarde** u otra vista. Nunca se abre el chat. Si la página aún no se ha actualizado, seguirá la tarea cuando lo haga.

## El resumen matutino

Llega los días laborables a la hora de **Resumen matutino**, a menos que no haya nada que contar. Si esa hora es anterior a **Lo pospuesto vuelve a las**, espera hasta 5 minutos después para incluir las tareas que vuelven a aparecer esa mañana. **Vista previa** lo muestra sin enviarlo. De forma predeterminada, se envía como notificación push y por correo, y es lo bastante breve para leerlo de un vistazo:

- un saludo con lo más importante del día, como «Buenos días, Sam. Hay 2 respuestas listas para enviar» o, si hay una sola tarea, «Buenos días, Sam. Falta tu aprobación: enviar el formulario del pedido»;
- las tareas que menciona el saludo, cada una con un enlace **Abrir**, y lo que vence hoy; si no hay nada de eso, como máximo tres tareas;
- hasta cinco tareas que hayas añadido y estén pendientes de ti, independientemente de lo que mencione el saludo;
- cuántas tareas más pueden esperar y cuánto tardarías en resolverlas a tu ritmo, como «Pueden esperar 12 más, que te llevarán unos 5 min». Ese tiempo no incluye las tareas que esperan tu respuesta. Tampoco se cuenta una tarea que vence hoy pero está pospuesta hasta más tarde, ni una en la que The Machine siga trabajando, hasta que requiera tu atención. El total coincide con las tareas pendientes de tu lista.
- tus reuniones en una línea.

**Abrir** muestra la tarea resaltada en tu lista, aunque esté hecha o pospuesta. Una promesa abre su tarea o, si aún no tiene una, su propia página.

La notificación push incluye lo mismo, pero sin enlaces. Tócala o usa el enlace al final del correo para volver a leer el resumen en **Tareas**.

## El resumen de la tarde

Llega una vez en los días laborables, a la hora que hayas elegido en **Horario laboral**. De forma predeterminada, se envía 15 minutos antes de **Hasta** y por los medios que hayas elegido en su fila. Solo llega los días en que hayas estado presente: si has usado el panel o has elegido qué hacer con una tarea en él, en Telegram, en un chat o por voz. Si no has completado ninguna tarea ni has asistido a ninguna reunión, no recibirás el resumen.

Empieza con un recuento del día, como «Buenas tardes, Sam. Has completado 4 tareas hoy», y después incluye una sección de **Trabajo** y otra de **Personal**. Si una sección no tiene contenido, no aparece. Cada una incluye:

- **Hecho hoy**: hasta tres tareas que hayas completado tú o tu Machine, seguidas de «+12 más» y las reuniones del día, como «+3 reuniones: llamada sobre precios y 2 más»;
- **Pendiente para mañana** (o para tu próximo día laborable si es viernes): las primeras reuniones y lo que vence.

Al final indica cuántas tareas siguen necesitando tu atención. Toca la notificación push o el enlace al final del correo para volver a leerlo, con **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva su fila.

## Privacidad

Tu Machine envía las notificaciones push directamente a tu dispositivo, cifradas para ese dispositivo. El correo pasa por el servidor de correo de The Machine y por tu proveedor de correo. Cuando [Cuidadoso](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo incluyen totales. Desactiva **Correo** para un tipo de notificación si no quieres recibirlo por correo.

Activa las notificaciones push de un dispositivo en **Este dispositivo** o consulta [Instalar la app](phone-app.md). La [app para móviles](mobile-app.md) envía una línea sencilla a través de Apple o Google y después le pide a tu Machine el título y el siguiente paso.
