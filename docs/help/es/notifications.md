---
title: Notificaciones
area: settings
summary: Qué te llega, dónde y cuándo: solo te avisamos de lo que no puede esperar. El resto se incluye en un resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: febea6f9eb2c331a
---
¿Quieres recibir menos notificaciones o cambiar cuáles recibes? En **Ajustes**, **Notificaciones**, elige dónde quieres recibir cada tipo:

- **Tareas nuevas**: solo lo que no puede esperar, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, un inicio de sesión que necesita una tarea o una pregunta del Fleet.
- **Recordatorios**: tareas pospuestas y respuestas que estás esperando y vuelven a estar pendientes.
- **Resumen matutino**: un resumen breve de tu día. Más abajo tienes más información.
- **Resumen de la tarde**: lo que has hecho hoy y lo que queda pendiente para mañana. Más abajo tienes más información.

Cada tipo tiene un interruptor para **Push** (la app del móvil o del ordenador), **Telegram** cuando lo hayas configurado y **Correo** en una Machine alojada o en una de The Machine Network. Todo está activado, excepto los resúmenes en Telegram.

En la misma pestaña puedes configurar tu **Horario laboral**: los días laborables, cuándo pueden enviarse notificaciones, cuándo vuelven las tareas pospuestas, las horas de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Solo recibirás una notificación push, un aviso de Telegram o un correo electrónico si ocurre algo de esto:

- una tarea vence hoy o está marcada como urgente;
- alguien está esperando una respuesta que ya está redactada y lista para enviar;
- una tarea necesita que inicies sesión;
- una tarea pospuesta vuelve a estar pendiente a la hora que elegiste.

Todo lo demás aparece discretamente en el panel (y en silencio en Telegram) y espera al resumen matutino. En un día libre, solo recibirás avisos de lo urgente o de lo que vence hoy. Recibirás un máximo de 8 notificaciones push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo se envían las notificaciones

Se comprueba si estás usando el panel, no solo si lo tienes abierto:

- Si lo estás usando (está en primer plano y has hecho clic, escrito o desplazado la página en los últimos 10 minutos), no recibirás avisos. Los mensajes de Telegram llegarán en silencio. Abrir o recargar el panel no cuenta.
- Si no estás (está en segundo plano, cerrado o llevas 10 minutos sin actividad), recibirás una notificación push un minuto después de salir, salvo que vuelvas y la veas.
- Si sigue sin verse 15 minutos después y no puede esperar, recibirás un correo electrónico, como máximo uno por hora. No se incluirá lo que ya hayas gestionado y cada tarea aparecerá una sola vez, con su estado actual. La mayoría de los días, el resumen matutino será el único correo electrónico.
- Si un compañero te asigna una tarea y tu Machine no tiene un móvil ni Telegram para avisarte, recibirás un correo electrónico con el título y un enlace 15 minutos después, si todavía no la has visto. Desactiva **Correo** en **Resultados y preguntas** para dejar de recibirlos.
- Fuera de tu horario laboral, no recibirás nada. La tarea se incluirá en el resumen matutino.
- Si recibes una nueva tarea de trabajo en un día libre, esperará hasta la hora del resumen de tu próximo día laborable. La tarea te indicará cuándo recibirás la notificación, por ejemplo: «Notificación: lun, 2 nov · 08:30».

Los avances y las modificaciones no generan notificaciones. Si aparece un resultado nuevo en una tarea que aún no has visto, se actualizará sin enviar otra notificación. Si llegan varias a la vez, recibirás un solo aviso. El icono de la app muestra cuántas tareas necesitan tu atención.

## Botones de las notificaciones

Cada notificación tiene botones para el siguiente paso. En la app móvil:

- Tarea nueva: Hazlo, Posponer, Marcar como hecho.
- Borrador listo: Abrir borrador, Posponer, Marcar como hecho.
- Resultado listo: Abrir, Marcar como hecho, Posponer.
- Pregunta, bloqueo o inicio de sesión: Responder, Abrir o Iniciar sesión, y después Posponer y Marcar como hecho.
- Recordatorio: Marcar como hecho, Posponer, Abrir.
- Resumen matutino: tócalo para abrirlo.

El navegador y Telegram muestran dos de esos botones. Las preguntas del Fleet siempre incluyen las opciones Responder y Rechazar.

No se envía, paga ni presenta nada desde una notificación. Los borradores siempre se abren primero para que puedas revisarlos antes de enviarlos. Abrir borrador muestra la tarea en tu lista con el borrador completo. Hazlo solo inicia el trabajo de una tarea nueva.

En la app móvil, Posponer y Marcar como hecho te pedirán que desbloquees el dispositivo. En un navegador, abrirán el panel, donde se realizará la acción y aparecerá la opción para deshacerla. Al posponer una tarea, volverá a estar pendiente en dos horas o, si es un recordatorio, mañana por la mañana.

Los correos electrónicos incluyen enlaces para abrir las tareas y, si están pendientes, para posponerlas. Solo abren el panel.

Si tocas una notificación o eliges Abrir en un correo electrónico o en Telegram, la tarea aparecerá resaltada en tu lista, dondequiera que esté en ese momento: **Recién hecho**, **Hecho**, **Vuelve más tarde** u otra vista. Nunca se abrirá el chat. Si la página aún no se ha actualizado, seguirá la tarea cuando lo haga.

## El resumen matutino

Lo recibirás los días laborables a la hora de **Resumen matutino**, salvo que no haya nada que contarte. Si esa hora es anterior a **Lo pospuesto vuelve a las**, el resumen esperará hasta 5 minutos después para incluir las tareas que vuelven a estar pendientes esa mañana. **Vista previa** te permite verlo sin enviarlo. De forma predeterminada, recibirás una notificación push y un correo electrónico. Será breve, para que puedas leerlo de un vistazo:

- un saludo con lo más importante del día, como «Buenos días, Sam. Tienes 2 respuestas listas para enviar» o, si solo hay una tarea, «Buenos días, Sam. Falta tu visto bueno: enviar el formulario del pedido». Solo cuentan como listas las tareas con un borrador o resultado que tengas que aprobar. Las que necesitan primero una respuesta tuya no cuentan;
- las tareas que se mencionan en el saludo, cada una con un enlace para abrirla, y lo que vence hoy; si no hay nada que venza hoy, se incluyen como máximo tres tareas;
- hasta cinco tareas que hayas añadido tú y que estén pendientes de ti, independientemente de lo que cuente el saludo;
- cuántas tareas más pueden esperar y cuánto tardarás en gestionarlas a tu ritmo, por ejemplo: «Puedes dejar 12 tareas para más tarde. Tardarás unos 5 min en resolverlas». Las tareas pendientes de tu respuesta no se incluyen en ese tiempo. Tampoco se cuentan hasta que vuelvan a estar pendientes de ti las que vencen hoy pero has pospuesto para más tarde, ni las tareas en las que The Machine sigue trabajando. El número coincide con las tareas pendientes de tu lista;
- tus reuniones, en una sola línea.

Abrir muestra la tarea resaltada en tu lista, aunque esté hecha o pospuesta. Una promesa abre su tarea o, si todavía no tiene ninguna, su propia página.

La notificación push muestra lo mismo, sin enlaces. Tócala o usa el enlace al final del correo electrónico para volver a leer este resumen en **Tareas**.

## El resumen de la tarde

Lo recibirás una vez cada día laborable, a la hora indicada en **Horario laboral**. De forma predeterminada, se envía 15 minutos antes de **Hasta** y por los medios que hayas elegido en su fila. Solo lo recibirás los días que hayas estado presente: si has usado el panel o has elegido qué hacer con una tarea allí, en Telegram, en el chat o por voz. No recibirás ningún resumen los días en que no hayas completado ninguna tarea ni tenido reuniones.

Empieza con un recuento del día, por ejemplo: «Buenas tardes, Sam. Hoy has completado 4 tareas». Después incluye una sección de **Trabajo** y otra de **Personal**. Si una sección no tiene nada, no aparece. Cada una incluye:

- **Hecho hoy**: hasta tres tareas que hayas completado tú o tu Machine, seguidas de «+12 más» y las reuniones del día, por ejemplo: «+3 reuniones: llamada sobre precios y 2 más»;
- **Pendiente para mañana** (o para el próximo día laborable si es viernes): las primeras reuniones y lo que vence.

Al final indica cuántas tareas siguen pendientes de ti. Toca la notificación push o el enlace al final del correo electrónico para volver a leerlo, con las opciones **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva la opción de su fila.

## Privacidad

Las notificaciones push van directamente desde tu Machine hasta tu dispositivo y están cifradas para este. El correo electrónico pasa por el servidor de correo de The Machine y por tu proveedor de correo. Si [Con cuidado](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos electrónicos solo muestran recuentos. Desactiva **Correo** para un tipo de notificación para que no se envíe por correo electrónico.

Activa las notificaciones push de un dispositivo en **Este dispositivo** o consulta [Instalar la app](phone-app.md). La [app móvil](mobile-app.md) envía una línea de texto sin formato a través de Apple o Google y luego le pide a tu Machine el título y el siguiente paso.
