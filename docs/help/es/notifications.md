---
title: Notificaciones
area: settings
summary: Qué te llega, dónde y cuándo: solo lo que no puede esperar te avisa; lo demás aparece en un resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 2146426abe3eaa50
---
¿Quieres menos notificaciones o recibir otras? En **Ajustes**, **Notificaciones**, elige dónde recibir cada tipo:

- **Tareas nuevas**: solo lo que no puede esperar, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, un inicio de sesión que necesita una tarea o una pregunta de Fleet.
- **Recordatorios**: tareas pospuestas y respuestas pendientes.
- **Resumen matutino**: un breve resumen del día. Más abajo encontrarás más información.
- **Resumen de la tarde**: lo que hiciste hoy y lo que queda pendiente para mañana. Más abajo encontrarás más información.

Cada tipo tiene una opción para **Push** (la app en tu teléfono o computadora), **Telegram** cuando ya esté configurado y **Correo** en una Machine alojada o una de The Machine Network. Todas están activadas, excepto los resúmenes en Telegram.

En la misma pestaña encontrarás tu **Horario laboral**: los días laborables, cuándo pueden llegar las notificaciones, cuándo vuelven las tareas pospuestas, los horarios de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Recibirás una notificación Push, un aviso de Telegram o un correo solo por:

- una tarea que vence hoy o está marcada como urgente;
- una respuesta que alguien espera, preparada y lista para enviar;
- una tarea que necesita que inicies sesión;
- una tarea pospuesta que vuelve a la hora que elegiste.

Todo lo demás aparece discretamente en el panel (y sin sonido en Telegram) y espera al resumen matutino. En un día libre, solo te avisamos de lo urgente o de lo que vence hoy. Recibirás como máximo 8 notificaciones Push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo te avisa

Comprueba si estás usando el panel, no solo si está abierto:

- Si lo estás usando (está en primer plano y has hecho clic, escrito o desplazado la página en los últimos 10 minutos), no recibirás avisos. Los mensajes de Telegram llegan sin sonido. Abrir o volver a cargar el panel no cuenta por sí solo.
- Si no estás (está en segundo plano, cerrado o llevas 10 minutos sin actividad), recibirás una notificación Push un minuto después de irte, a menos que vuelvas y la veas.
- Si 15 minutos después sigue sin leerse y no puede esperar, recibirás un correo al respecto, como máximo uno por hora. No se incluyen las cosas que ya resolviste. La mayoría de los días, el resumen matutino es el único correo.
- Si un compañero te asigna una tarea y tu Machine no tiene un teléfono ni Telegram para avisarte, recibirás un correo con el título y un enlace 15 minutos después, si aún no la has visto. Desactiva **Correo** en **Resultados y preguntas** para dejar de recibirlo.
- Fuera de tu horario laboral, no recibirás avisos. La tarea aparecerá en el resumen matutino.
- Si te asignan una tarea de trabajo en un día libre, esperará hasta la hora del resumen del próximo día laborable. La tarea indica cuándo te llegará, por ejemplo: «Notificación: lun. 2 nov. · 08:30».

Los avances y las ediciones no generan notificaciones. Si aparece un resultado nuevo en una tarea que aún no has visto, se actualizará sin enviar otra notificación. Si llegan varias a la vez, recibirás un solo aviso. El icono de la app muestra cuántas tareas necesitan tu atención.

## Botones de las notificaciones

Cada notificación incluye botones para el siguiente paso. En la app para teléfono:

- Tarea nueva: **Hazlo**, **Posponer**, **Marcar como hecho**.
- Borrador listo: **Abrir borrador**, **Posponer**, **Marcar como hecho**.
- Resultado listo: **Abrir**, **Marcar como hecho**, **Posponer**.
- Pregunta, problema o inicio de sesión: **Responder**, **Abrir** o **Iniciar sesión**, y después **Posponer** y **Marcar como hecho**.
- Recordatorio: **Marcar como hecho**, **Posponer**, **Abrir**.
- Resumen matutino: tócalo para abrirlo.

En el navegador y en Telegram aparecen dos botones. En las preguntas de Fleet, siempre aparecen **Responder una vez** y **Rechazar**.

No se envía, paga ni presenta nada desde una notificación. Los borradores siempre se abren primero para que puedas verlos antes de enviarlos. **Abrir borrador** muestra la tarea en tu lista con el borrador completo. **Hazlo** solo inicia el trabajo en una tarea nueva.

En la app para teléfono, **Posponer** y **Marcar como hecho** te piden que desbloquees el dispositivo primero. En el navegador, abren el panel, que realiza la acción y muestra **Deshacer**. Al posponer una tarea, volverá en dos horas o, si es un recordatorio, mañana por la mañana.

Los correos incluyen enlaces para **Abrir** (y **Posponer** si hay algo pendiente). Solo abren el panel.

Al tocar una notificación, o **Abrir** en un correo o en Telegram, verás la tarea resaltada en tu lista, esté donde esté ahora: **Recién hecho**, **Hecho**, **Vuelve más tarde** u otra vista. Nunca se abre el chat. Si la página aún no se ha actualizado, seguirá la tarea cuando lo haga.

## El resumen matutino

Llega los días laborables a la hora de **Resumen matutino**, a menos que no haya nada que contar. Si esa hora es anterior a **Lo pospuesto vuelve a las**, espera hasta 5 minutos después, para incluir las tareas que vuelven esa mañana. **Vista previa** te permite verlo sin enviarlo. De forma predeterminada, llega como notificación Push y por correo, y es lo bastante breve para leerlo de un vistazo:

- un saludo con lo más importante del día, como «Buenos días, Sam. Hay 2 respuestas listas para enviar» o, si hay una sola tarea, «Buenos días, Sam. Espera tu aprobación: Envía el formulario de pedido»;
- las tareas que menciona el saludo, cada una con un enlace para abrirla, y lo que vence hoy; si no hay nada que venza hoy, incluye como máximo tres tareas;
- hasta cinco tareas que tú mismo añadiste y que esperan tu atención, además de las que menciona el saludo;
- cuántas tareas más pueden esperar y cuánto tardarías en resolverlas a tu ritmo, por ejemplo: «Pueden esperar 12 más. Te llevará unos 5 min resolverlas». Ese tiempo no incluye las tareas que esperan tu respuesta. Tampoco se cuenta una tarea que vence hoy pero está pospuesta para más tarde, ni una en la que The Machine siga trabajando, hasta que requiera tu atención. El total coincide con las tareas pendientes de tu lista.
- tus reuniones en una sola línea.

**Abrir** muestra la tarea resaltada en tu lista, aunque esté hecha o pospuesta. Una promesa abre su tarea o, si todavía no tiene una, su propia página.

La notificación Push contiene lo mismo, pero sin enlaces. Tócala o usa el enlace al final del correo para volver a leer este resumen en **Tareas**.

## El resumen de la tarde

Llega una vez al día los días laborables, a la hora que hayas elegido en **Horario laboral**. De forma predeterminada, llega 15 minutos antes de **Hasta**, por los medios que elegiste en su fila. Si durante el día no has completado ninguna tarea ni has tenido reuniones, no recibirás el resumen. Empieza con un recuento del día, como «Buenas tardes, Sam. Hoy has completado 4 tareas»; luego incluye una sección de **Trabajo** y otra de **Personal**. Si una sección no tiene nada, no aparece. Cada sección incluye:

- **Hecho hoy**: hasta tres tareas que tú o tu Machine hayan completado, seguidas de «+12 más» y las reuniones del día, por ejemplo, «+3 reuniones: Llamada sobre precios y 2 más»;
- **Pendiente para mañana** (o para el próximo día laborable si es viernes): las primeras reuniones y lo que vence.

Al final, indica cuántas tareas siguen necesitando tu atención. Toca la notificación Push o el enlace al final del correo para volver a leerlo, con **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva su fila.

## Privacidad

Las notificaciones Push van directamente de tu Machine a tu dispositivo, cifradas para él. El correo pasa por el servidor de correo de The Machine y tu proveedor de correo. Cuando [Cuidadoso](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo incluyen recuentos. Desactiva **Correo** para un tipo de notificación si no quieres recibirlo por correo.

Activa las notificaciones Push para un dispositivo en **Este dispositivo** o consulta [Instalar la app](phone-app.md). La [app móvil](mobile-app.md) envía una línea sin cifrar a través de Apple o Google y luego le pide a tu Machine el título y el siguiente paso.
