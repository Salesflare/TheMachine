---
title: Notificaciones
area: settings
summary: Qué te llega, dónde y cuándo: solo te avisamos de lo que no puede esperar. El resto va en un resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: dc56a77907df5da0
---
¿Quieres recibir menos notificaciones o cambiar cuáles recibes? En **Ajustes**, **Notificaciones**, elige dónde quieres recibir cada tipo:

- **Tareas nuevas**: solo lo que no puede esperar, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, una tarea que necesita que inicies sesión o una pregunta del Fleet.
- **Recordatorios**: tareas pospuestas y respuestas que estás esperando y vuelven a aparecer.
- **Resumen matutino**: un resumen breve de tu día. Consulta más abajo.
- **Resumen de la tarde**: lo que has hecho hoy y lo que queda pendiente para mañana. Consulta más abajo.

Cada tipo tiene un interruptor para **Push** (la app del móvil o del ordenador), **Telegram** cuando esté configurado y **Correo** si tu Machine está alojada o forma parte de The Machine Network. Todo está activado, excepto los resúmenes en Telegram.

En la misma pestaña encontrarás tu **Horario laboral**: los días laborables, cuándo pueden enviarse notificaciones, cuándo vuelven a aparecer las tareas pospuestas, la hora de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Solo recibirás una notificación Push, un aviso de Telegram o un correo por estos motivos:

- una tarea que vence hoy o está marcada como urgente;
- una respuesta que alguien está esperando, ya redactada y lista para enviar;
- una tarea que necesita que inicies sesión;
- una tarea pospuesta que vuelve a aparecer a la hora que elegiste.

Todo lo demás aparece discretamente en el panel y en Telegram, sin sonido, y espera al resumen matutino. En un día libre, solo recibirás avisos de lo urgente o de lo que vence hoy. Como máximo, recibirás 8 notificaciones Push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo te avisa

Comprueba si estás usando el panel de verdad, no solo si está abierto:

- Si lo estás usando, es decir, está en primer plano y has hecho clic, escrito o desplazado la página en los últimos 10 minutos, no recibirás avisos. Telegram llega sin sonido. Abrir o volver a cargar el panel no cuenta.
- Si no estás, porque está en segundo plano, cerrado o llevas 10 minutos sin usarlo, recibirás una notificación Push un minuto después de salir, salvo que vuelvas y la veas.
- Si 15 minutos después aún no te ha llegado nada y no puede esperar, recibirás un correo. Como máximo, uno cada hora. Se excluye lo que ya hayas visto o gestionado, y cada tarea aparece una sola vez, con su estado actual. La mayoría de los días, el resumen matutino es el único correo.
- Se considera que algo te ha llegado si aparece una notificación en el móvil o el navegador, o si Telegram recibe el mensaje. No cuenta si el móvil está apagado, sin conexión o con las notificaciones desactivadas. Tampoco cuenta Telegram mientras usas el panel. Si solo se muestra en un ordenador, lo urgente o lo que vence hoy también se envía por correo: puede que no estés delante.
- Si no tienes la app para el móvil, las notificaciones del navegador ni Telegram, recibirás por correo todo lo anterior.
- Si no se puede contactar con Telegram, recibirás la notificación Push de todos modos y se volverá a intentar enviar el mensaje a Telegram automáticamente.
- Si un compañero te asigna una tarea y tu Machine no tiene móvil ni Telegram para avisarte, recibirás un correo con el título y un enlace, 15 minutos después si aún no la has visto. Desactiva **Correo** en **Resultados y preguntas** para evitarlo.
- Si tu sesión de Claude caduca en los próximos 3 días o ya ha caducado, recibirás un correo con **Volver a iniciar sesión**, una vez por sesión. Desactiva **Correo** en **Resultados y preguntas** para evitarlo.
- Fuera de tu horario laboral, no recibirás avisos. La información aparecerá en el resumen matutino.
- Si recibes una tarea nueva de trabajo en un día libre, esperará hasta la hora del resumen del siguiente día laborable. La tarea te indicará cuándo te llegará, por ejemplo: «Notificación: lun, 2 nov · 08:30».

El progreso y las modificaciones no generan notificaciones. Si aparece un resultado nuevo en una tarea que aún no has visto, se actualizará sin enviarte otra notificación. Si llegan varias a la vez, recibirás un solo aviso. El icono de la app muestra cuántas tareas necesitan tu atención.

## Botones de las notificaciones

Cada notificación incluye botones para dar el siguiente paso. En la app para el móvil:

- Tarea nueva: **Hazlo**, **Posponer**, **Marcar como hecho**.
- Borrador listo: **Abrir borrador**, **Posponer**, **Marcar como hecho**.
- Resultado listo: **Abrir**, **Marcar como hecho**, **Posponer**.
- Si necesita tu respuesta, está atascada o requiere que inicies sesión: **Responder**, **Abrir** o **Iniciar sesión**; después, **Posponer** y **Marcar como hecho**.
- Recordatorio: **Marcar como hecho**, **Posponer**, **Abrir**.
- Resumen matutino: tócalo para abrirlo.

El navegador y Telegram muestran dos de estos botones. Las preguntas del Fleet mantienen los botones **Responder una vez** y **Rechazar**.

No se envía, paga ni presenta nada desde una notificación. Los borradores siempre se abren primero para que puedas revisarlos antes de enviarlos. **Abrir borrador** muestra la tarea en tu lista con el borrador completo. **Hazlo** solo inicia el trabajo en una tarea nueva.

En la app para el móvil, **Posponer** y **Marcar como hecho** te piden que desbloquees el móvil primero. En el navegador, abren el panel, donde se realiza la acción y aparece la opción para deshacerla. Al posponer una tarea, volverá a aparecer dentro de dos horas o, si es un recordatorio, mañana por la mañana.

Los correos incluyen enlaces para abrir las tareas y, en el caso de las que están pendientes, para posponerlas. Solo abren el panel.

Al tocar una notificación, o **Abrir** en un correo o en Telegram, verás la tarea resaltada en tu lista, esté donde esté ahora: **Recién hecho**, **Hecho**, **Vuelve más tarde** u otra vista. Nunca se abre el chat. Si la página aún no se ha actualizado, irá a la tarea cuando se actualice.

## El resumen matutino

Lo recibirás los días laborables a la hora de **Resumen matutino**, salvo que no haya nada que contar. Si esa hora es anterior a **Lo pospuesto vuelve a las**, esperará hasta 5 minutos después para incluir las tareas que vuelven a aparecer esa mañana. **Vista previa** te permite consultarlo sin enviarlo. De forma predeterminada, se envía por notificación Push y por correo, y es lo bastante breve para leerlo de un vistazo:

- Un saludo con lo más importante del día, como «Buenos días, Sam. Tienes 2 respuestas listas para enviar» o, si solo hay una tarea, «Buenos días, Sam. Necesitas dar el visto bueno a: Enviar el formulario de pedido». Solo cuentan como listas las tareas que tengan un borrador o un resultado pendiente de aprobación. Las que primero necesitan tu respuesta no cuentan.
- Las tareas que se mencionan en el saludo, cada una con un enlace para abrirla, y lo que vence hoy; si no, como máximo tres tareas.
- Hasta cinco tareas que hayas añadido tú y estén pendientes de ti, independientemente de lo que cuente el saludo.
- Cuántas tareas más pueden esperar y cuánto tardarías en resolverlas a tu ritmo, por ejemplo: «Pueden esperar 12 más. Tardarás unos 5 min en resolverlas». Ese cálculo no incluye las tareas pendientes de tu respuesta. Tampoco cuenta una tarea que vence hoy pero has pospuesto para más tarde, ni una en la que The Machine siga trabajando, hasta que quede pendiente de ti. El total coincide con las tareas pendientes que aparecen en tu lista.
- Tus reuniones, en una línea.

**Abrir** muestra la tarea resaltada en tu lista, aunque esté hecha o pospuesta. Al abrir una promesa, verás su tarea o, si aún no tiene una, su propia página.

La notificación Push muestra lo mismo, pero sin enlaces. Tócala o usa el enlace al final del correo para volver a leer el resumen en **Tareas**.

## El resumen de la tarde

Lo recibirás una vez cada día laborable, a la hora que aparece en **Horario laboral**. De forma predeterminada, se envía 15 minutos antes de **Hasta**, por los medios que hayas elegido en la fila de arriba. Solo se envía los días que hayas estado por aquí: has usado el panel o has tomado una decisión sobre una tarea allí, en Telegram, en el chat o por voz. No se envía si no has completado ninguna tarea ni has asistido a ninguna reunión ese día.

Empieza con un resumen del día, como «Buenas tardes, Sam. Has completado 4 tareas hoy», seguido de una sección de **Trabajo** y otra de **Personal**. Si una sección no tiene nada, no aparece. Las alertas sobre tu Machine no se incluyen en ninguna. Cada sección contiene:

- **Hecho hoy**: hasta tres tareas que hayas completado tú o tu Machine, seguidas de «y 12 más» y las reuniones del día, por ejemplo: «y 3 reuniones: llamada sobre precios y 2 más»;
- **Pendiente para mañana** (o para el siguiente día laborable si es viernes): las primeras reuniones y lo que vence.

Al final, verás cuántas tareas siguen pendientes de ti. Toca la notificación Push o el enlace al final del correo para volver a leerlo, con **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva la fila correspondiente.

## Privacidad

Las notificaciones Push van directamente de tu Machine a tu dispositivo, cifradas para ese dispositivo. El correo pasa por el servidor de correo de The Machine y tu proveedor de correo. Si [Precavido](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo incluyen cantidades. Desactiva **Correo** para un tipo de notificación si no quieres recibirlo por correo.

Activa las notificaciones Push para un dispositivo en **Este dispositivo** o consulta [Instalar la app](phone-app.md). La [app móvil](mobile-app.md) envía una línea sin detalles a través de Apple o Google y, después, le pide a tu Machine el título y el siguiente paso.
