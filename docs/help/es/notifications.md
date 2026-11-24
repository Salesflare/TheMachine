---
title: Notificaciones
area: settings
summary: Qué recibes, dónde y cuándo: solo te avisamos de lo que no puede esperar; el resto llega en un único resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: bdb4ecec9446aa5e
---
¿Quieres recibir menos notificaciones o cambiar cuáles recibes? En **Ajustes**, **Notificaciones**, elige dónde quieres recibir cada tipo:

- **Tareas nuevas**: solo las que no pueden esperar, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, un inicio de sesión que necesita una tarea o una pregunta del Fleet.
- **Recordatorios**: tareas pospuestas y respuestas que estás esperando y vuelven a estar pendientes.
- **Resumen matutino**: un resumen breve de tu día. Más abajo tienes los detalles.
- **Resumen de la tarde**: lo que has terminado hoy y lo que queda pendiente para mañana. Más abajo tienes los detalles.

Cada tipo tiene un interruptor para **Push** (la app en tu móvil u ordenador), **Telegram** cuando esté configurado y **Correo** en una Machine alojada o conectada a The Machine Network. Todo está activado, salvo los resúmenes en Telegram.

En la misma pestaña encontrarás tu **Horario laboral**: los días laborables, cuándo pueden llegar las notificaciones, cuándo vuelven las tareas pospuestas, las horas de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Recibirás una notificación Push, un aviso de Telegram o un correo solo si ocurre algo de esto:

- una tarea vence hoy o está marcada como urgente;
- hay una respuesta redactada y lista para enviar que alguien está esperando;
- una tarea necesita que inicies sesión;
- una tarea pospuesta vuelve en el momento que elegiste.

Todo lo demás aparece sin avisar en el panel (y en silencio en Telegram) y espera al resumen matutino. En un día libre, solo recibirás avisos de lo urgente o de lo que vence hoy. Como máximo, recibirás 8 notificaciones Push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo te avisa

La app comprueba si estás usando el panel, no solo si está abierto:

- Si lo estás usando (está en primer plano y has hecho clic, escrito o desplazado la página en los últimos 10 minutos), no recibirás avisos. Los mensajes de Telegram llegarán en silencio. Abrirlo o recargarlo sin más no cuenta.
- Si no estás (está en segundo plano, cerrado o llevas 10 minutos sin actividad), recibirás una notificación Push un minuto después de salir, salvo que hayas vuelto y la hayas visto.
- Si sigue sin verse 15 minutos después y no puede esperar, recibirás un correo. Como máximo, uno por hora. No se incluyen las cosas que ya hayas gestionado, y cada tarea aparece una sola vez, con la información más reciente. La mayoría de los días, el resumen matutino será el único correo.
- Si un compañero te asigna una tarea y tu Machine no tiene un teléfono ni Telegram para avisarte, recibirás un correo con el título y un enlace si sigue sin verse 15 minutos después. Desactiva **Correo** en **Resultados y preguntas** para dejar de recibirlo.
- Fuera de tu horario laboral no recibirás avisos. La tarea aparecerá en el resumen matutino.
- Las tareas de trabajo nuevas que lleguen en un día libre esperarán hasta la hora del resumen del siguiente día laborable. La tarea te indica cuándo te avisará, por ejemplo: Notificación lun, 2 nov · 08:30.

Los avances y las modificaciones no generan notificaciones. Si hay un resultado nuevo para una tarea que aún no has visto, se actualiza sin enviar otra notificación. Si llegan varias a la vez, recibirás un solo aviso. El icono de la app muestra cuántas tareas requieren tu atención.

## Botones de las notificaciones

Cada notificación incluye botones para continuar. En la app para móvil:

- Tarea nueva: **Hazlo**, **Pospón**, **Marcar como hecho**.
- Borrador listo: **Abrir borrador**, **Pospón**, **Marcar como hecho**.
- Resultado listo: **Abrir**, **Marcar como hecho**, **Pospón**.
- Necesita tu respuesta, se ha atascado o requiere que inicies sesión: **Responder**, **Abrir** o **Iniciar sesión**; después, **Pospón** y **Marcar como hecho**.
- Recordatorio: **Marcar como hecho**, **Pospón**, **Abrir**.
- Resumen matutino: tócalo para abrirlo.

El navegador y Telegram muestran dos botones. En las preguntas del Fleet siempre aparecen **Responder** y **Rechazar**.

Las notificaciones no envían, pagan ni presentan nada. Los borradores siempre se abren primero para que los veas antes de enviarlos. **Abrir borrador** muestra la tarea en tu lista y el borrador completo. **Hazlo** solo inicia el trabajo en una tarea nueva.

En la app para móvil, **Pospón** y **Marcar como hecho** te pedirán que desbloquees el móvil. En un navegador, abrirán el panel, donde se completará la acción y podrás deshacerla. Al posponer una tarea, volverá a aparecer dentro de dos horas o, si es un recordatorio, mañana por la mañana.

Los correos incluyen enlaces para abrir las tareas y posponer las que estén pendientes. Esos enlaces solo abren el panel.

Si tocas una notificación o **Abrir** en un correo o en Telegram, verás la tarea resaltada en tu lista, dondequiera que esté ahora: **Recién hecho**, **Hecho**, **Vuelve más tarde** u otra vista. Nunca se abre el chat. Si la página aún no se ha actualizado, seguirá la tarea cuando lo haga.

## El resumen matutino

Lo recibirás los días laborables a la hora indicada en **Resumen matutino**, salvo que no haya nada que contar. Si esa hora es anterior a **Lo pospuesto vuelve a las**, esperará hasta 5 minutos después para incluir las tareas que vuelvan a estar pendientes esa mañana. **Vista previa** te permite verlo sin enviarlo. De forma predeterminada, llega como notificación Push y por correo, y es lo bastante breve para leerlo de un vistazo:

- un saludo con lo más importante del día, como «Buenos días, Sam. Hay 2 respuestas listas para enviar» o, si solo hay una tarea, «Buenos días, Sam. Lista para tu visto bueno: Enviar el formulario del pedido». Solo cuentan como listas las tareas con un borrador o un resultado que aprobar. Las que primero necesitan tu respuesta no cuentan;
- las tareas que se mencionan en el saludo, cada una con un enlace para abrirla, y lo que vence hoy; si no, como máximo tres cosas por hacer;
- hasta cinco tareas que hayas añadido tú y que estén pendientes de ti, independientemente de lo que cuente el saludo;
- cuántas tareas más pueden esperar y cuánto tardarías en resolverlas a tu ritmo, por ejemplo: «Pueden esperar 12 más. Tardarás unos 5 min en resolverlas». Las tareas que esperan tu respuesta no cuentan en ese tiempo. Tampoco se cuentan hasta que requieran tu atención las que vencen hoy pero están pospuestas para más tarde, ni las que The Machine sigue gestionando. El recuento coincide con las tareas pendientes de tu lista;
- tus reuniones en una línea.

**Abrir** muestra la tarea resaltada en tu lista, aunque esté hecha o pospuesta. Si una promesa tiene una tarea, se abre esa tarea. Si aún no tiene ninguna, se abre su propia página.

La notificación Push muestra lo mismo, sin enlaces. Tócala o usa el enlace al final del correo para volver a leer el resumen en **Tareas**.

## El resumen de la tarde

Lo recibirás una vez cada día laborable, a la hora indicada en **Horario laboral**. De forma predeterminada, llega 15 minutos antes de **Hasta**, por los medios que hayas elegido en su fila. Solo lo recibirás los días que hayas estado presente: has usado el panel o has elegido qué hacer con una tarea en el panel, en Telegram, en el chat o por voz. No recibirás uno si ese día no has terminado ninguna tarea ni has tenido reuniones.

Empieza con un recuento del día, por ejemplo: «Buenas tardes, Sam. Hoy has terminado 4 tareas». Después muestra una sección de **Trabajo** y otra de **Personal**. Si una sección está vacía, no aparece. Los avisos sobre tu Machine no aparecen en ninguna de las dos. Cada sección incluye:

- **Hecho hoy**: hasta tres tareas que hayas terminado tú o tu Machine, seguidas de «+12 más» y las reuniones del día, como «+3 reuniones: llamada sobre precios y 2 más»;
- **Pendiente para mañana** (o para el siguiente día laborable si es viernes): las primeras reuniones y lo que vence.

Termina indicando cuántas tareas siguen requiriendo tu atención. Toca la notificación Push o el enlace al final del correo para volver a leerlo, con **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva la opción de esa fila.

## Privacidad

Las notificaciones Push van directamente de tu Machine a tu dispositivo y están cifradas para ese dispositivo. El correo pasa por el servidor de correo de The Machine y tu proveedor de correo. Si [Cuidadoso](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo muestran recuentos. Desactiva **Correo** en un tipo de notificación para que no llegue por correo.

Activa las notificaciones Push para un dispositivo en **Este dispositivo** o consulta [Instala la app](phone-app.md). La [app para móvil](mobile-app.md) envía una línea de texto a través de Apple o Google y, después, le pide a tu Machine el título y el siguiente paso.
