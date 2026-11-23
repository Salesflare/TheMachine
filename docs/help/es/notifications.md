---
title: Notificaciones
area: settings
summary: Qué te llega, dónde y cuándo: solo lo urgente te avisa al momento; lo demás va en un único resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3faac166e8f9fa3d
---
¿Quieres menos notificaciones o recibir otras? En **Ajustes**, **Notificaciones**, elige dónde quieres recibir cada tipo:

- **Tareas nuevas**: solo lo urgente, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, un inicio de sesión que necesita una tarea o una pregunta del Fleet.
- **Recordatorios**: tareas pospuestas y respuestas que estás esperando y vuelven a aparecer.
- **Resumen matutino**: un breve resumen del día. Más abajo tienes más información.
- **Resumen de la tarde**: lo que has hecho hoy y lo que queda pendiente para mañana. Más abajo tienes más información.

Cada tipo tiene una opción para **Push** (la app en tu móvil o tu ordenador), **Telegram** cuando lo configures y **Correo** en una Machine alojada o en una de The Machine Network. Todas están activadas, excepto los resúmenes en Telegram.

En la misma pestaña puedes configurar tu **Horario laboral**: los días laborables, cuándo pueden llegar las notificaciones, cuándo vuelven a aparecer las tareas pospuestas, las horas de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo urgente

Recibirás una notificación push, un aviso de Telegram o un correo solo en estos casos:

- una tarea vence hoy o está marcada como urgente;
- alguien está esperando una respuesta que ya está redactada y lista para enviar;
- una tarea necesita que inicies sesión;
- una tarea pospuesta vuelve a aparecer a la hora que elegiste.

Todo lo demás aparece discretamente en el panel (y en silencio en Telegram) y espera al resumen matutino. En un día libre, solo te avisamos de lo urgente o de lo que vence hoy. Recibirás un máximo de 8 notificaciones push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo te avisa

Comprueba si estás usando el panel, no solo si está abierto:

- Si lo estás usando (está en primer plano y has hecho clic, escrito o desplazado la página en los últimos 10 minutos), no recibirás avisos. Los mensajes de Telegram llegarán en silencio. Abrir o recargar el panel no cuenta por sí solo.
- Si no estás (está en segundo plano, cerrado o llevas 10 minutos sin actividad), recibirás una notificación push un minuto después de salir, a menos que hayas vuelto y la hayas visto.
- Si sigue sin verse 15 minutos después y es urgente, recibirás un correo al respecto, como máximo uno por hora. Se excluye lo que ya hayas resuelto y cada tarea aparece una sola vez, tal como está en ese momento. La mayoría de los días, el resumen matutino será el único correo.
- Si un compañero te asigna una tarea y tu Machine no tiene un móvil ni Telegram para avisarte, recibirás un correo con el título y un enlace, 15 minutos después si aún no la has visto. Desactiva **Correo** en **Resultados y preguntas** para evitarlo.
- Fuera de tu horario laboral, no recibirás avisos. Aparecerá en el resumen matutino.
- Una tarea de trabajo nueva que llegue en un día libre esperará hasta la hora del resumen del siguiente día laborable. La tarea indica cuándo te llegará, por ejemplo: Notificación lun. 2 nov · 08:30.

El progreso y las ediciones nunca generan notificaciones. Si aparece un resultado nuevo en una tarea que aún no has visto, se actualiza sin enviar una notificación nueva. Si llegan varias a la vez, recibirás un solo aviso. El icono de la app muestra cuántas tareas requieren tu atención.

## Botones de las notificaciones

Cada notificación tiene botones para dar el siguiente paso. En la app para móvil:

- Tarea nueva: **Hazlo**, **Posponer**, **Marcar como hecha**.
- Borrador listo: **Abrir borrador**, **Posponer**, **Marcar como hecha**.
- Resultado listo: **Abrir**, **Marcar como hecha**, **Posponer**.
- Necesita tu respuesta, está bloqueada o requiere que inicies sesión: **Responder**, **Abrir** o **Iniciar sesión**; después, **Posponer** y **Marcar como hecha**.
- Recordatorio: **Marcar como hecha**, **Posponer**, **Abrir**.
- Resumen matutino: tócalo para abrirlo.

El navegador y Telegram muestran dos de esos botones. En las preguntas del Fleet, siempre están las opciones **Responder una vez** y **Rechazar**.

No se envía, paga ni presenta nada desde una notificación. Los borradores siempre se abren primero para que los veas antes de enviarlos. **Abrir borrador** muestra la tarea en tu lista con el borrador completo. **Hazlo** solo inicia el trabajo en una tarea nueva.

En la app para móvil, **Posponer** y **Marcar como hecha** te pedirán que desbloquees el móvil primero. En el navegador, abrirán el panel, donde se realizará la acción y aparecerá la opción **Deshacer**. Al posponer una tarea, volverá a aparecer dentro de dos horas o, si es un recordatorio, mañana por la mañana.

Los correos tienen enlaces para abrir las tareas y, si estás esperando algo, para posponerlas. Solo abren el panel.

Al tocar una notificación o **Abrir** en un correo o en Telegram, verás la tarea resaltada en tu lista, esté donde esté: **Recién hecho**, **Hecho**, **Vuelve más tarde** u otra vista. Nunca se abre el chat. Si la página aún no se había actualizado, te llevará a la tarea cuando lo haga.

## El resumen matutino

Lo recibirás los días laborables a la hora de tu **Resumen matutino**, salvo que no haya nada que decir. Si esa hora es anterior a **Lo pospuesto vuelve a las**, esperará hasta 5 minutos después para incluir las tareas que vuelven a aparecer esa mañana. **Vista previa** te permite verlo sin enviarlo. De forma predeterminada, se envía como notificación push y correo, y es lo bastante breve como para leerlo de un vistazo:

- Un saludo con lo más importante del día, como «Buenos días, Sam. Hay 2 respuestas listas para enviar» o, si hay una sola tarea, «Buenos días, Sam. Necesitamos tu visto bueno: Envía el formulario de pedido». Solo cuentan como listas las tareas con un borrador o resultado que aprobar. Las que requieren tu respuesta primero no cuentan.
- Las tareas que se mencionan en el saludo, cada una con un enlace para abrirla, y lo que vence hoy. Si no hay nada de eso, aparecerán como máximo tres tareas.
- Hasta cinco tareas que hayas añadido tú y que estén pendientes de ti, independientemente de lo que se mencione en el saludo.
- Cuántas tareas más pueden esperar y cuánto tardarás en resolverlas a tu ritmo, por ejemplo: «Otras 12 pueden esperar. Tardarás unos 5 min en resolverlas». Las tareas pendientes de tu respuesta no cuentan para ese tiempo. Tampoco se cuenta una tarea que vence hoy pero está pospuesta hasta más tarde, ni una en la que The Machine siga trabajando, hasta que quede pendiente de ti. El número coincide con las tareas pendientes de tu lista.
- Tus reuniones, en una sola línea.

**Abrir** muestra la tarea resaltada en tu lista, también si está hecha o pospuesta. Una promesa abre su tarea o, si aún no tiene una, su propia página.

La notificación push muestra lo mismo, pero sin enlaces. Tócala o toca el enlace al final del correo para volver a leer este resumen en **Tareas**.

## El resumen de la tarde

Lo recibirás una vez los días laborables, a la hora indicada en **Horario laboral**. De forma predeterminada, será 15 minutos antes de **Hasta**, por los medios que hayas elegido en la fila de arriba. Solo lo recibirás los días en que hayas estado: usando el panel o eligiendo qué hacer con una tarea en el panel, en Telegram, en el chat o por voz. No recibirás ninguno si ese día no has completado una tarea ni has tenido una reunión.

Empieza con un recuento del día, como «Buenas tardes, Sam. Hoy has completado 4 tareas». Después incluye una parte de **Trabajo** y otra de **Personal**. Si una parte está vacía, no aparece. Cada una incluye:

- **Hecho hoy**: hasta tres tareas que hayas terminado tú o tu Machine, después «y 12 más» y las reuniones del día, como «y 3 reuniones: Llamada sobre precios y 2 más»;
- **Pendiente para mañana** (o para el siguiente día laborable si es viernes): las primeras reuniones y lo que vence.

Al final, indica cuántas tareas siguen pendientes de ti. Toca la notificación push o el enlace al final del correo para volver a leerlo, con **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva su fila.

## Privacidad

Las notificaciones push van directamente de tu Machine a tu dispositivo y están cifradas para ese dispositivo. El correo pasa por el servidor de correo de The Machine y por tu proveedor de correo. Si el nivel de seguridad [Precavida](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo mostrarán recuentos. Desactiva **Correo** para un tipo de notificación si no quieres recibirlo por correo.

Activa las notificaciones push para un dispositivo en **Este dispositivo** o consulta [Instalar la app](phone-app.md). La [app móvil](mobile-app.md) envía una línea sencilla a través de Apple o Google y luego le pide a tu Machine el título y el siguiente paso.
