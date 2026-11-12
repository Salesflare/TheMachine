---
title: Notificaciones
area: settings
summary: Qué te llega, por dónde y cuándo: solo avisa lo que no puede esperar, lo demás va en un único resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
En **Ajustes**, **Notificaciones**, elige por tipo por dónde te llega:

- **Tareas nuevas**: solo lo que no puede esperar, como algo que vence hoy o algo urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, un inicio de sesión que necesita una tarea, una pregunta del Fleet.
- **Recordatorios**: lo pospuesto y las esperas que vuelven.
- **Resumen matutino**: un resumen corto de tu día. Más abajo.

Cada uno tiene un interruptor para **Push** (la app en tu teléfono u ordenador), **Telegram** cuando está configurado y **Correo** en una Machine alojada o en una que está en The Machine Network. Todos están activados, salvo el resumen en Telegram.

El **Horario laboral** está en la misma pestaña: tus días laborables, las horas en que pueden salir notificaciones, cuándo vuelve lo pospuesto, la hora del resumen y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Un push, un aviso en Telegram o un correo solo sale para:

- una tarea que vence hoy, o marcada como urgente;
- una respuesta que alguien espera, redactada y lista para enviar;
- una tarea que necesita que inicies sesión;
- algo pospuesto que vuelve a la hora que elegiste.

Todo lo demás llega en silencio al panel (y sin sonido en Telegram) y espera al resumen matutino. En un día libre solo avisa lo urgente o lo que vence hoy. Como mucho 8 push al día. Tras 3 días sin abrir el panel, solo llega el resumen matutino, hasta que vuelvas.

## Cuándo avisa

Como Slack, mira si estás usando el panel, no solo si está abierto:

- En uso: el panel está delante de ti, en primer plano, y has hecho clic, escrito, desplazado o tocado en los últimos 10 minutos. No vibra nada. Telegram llega sin sonido.
- Fuera: el panel está en segundo plano, minimizado, cerrado o inactivo durante 10 minutos. Un push sale un minuto después de que lo dejes, salvo que vuelvas y lo veas antes.
- Sin ver 15 minutos después, y no puede esperar: un correo para eso, como mucho uno por hora. Lo que ya resolviste queda fuera. La mayoría de los días, el resumen matutino es el único correo.
- Fuera de tu horario laboral: nada. El resumen matutino trae lo que llegó.
- Una tarea nueva de trabajo que llega en un día libre espera a la hora del resumen de tu próximo día laborable. La tarea muestra dónde y cuándo te llegará, como Notificación lun, 2 nov · 08:30, según la fila **Tareas nuevas**. Con Push y Telegram apagados ahí, no dice nada.

Solo avisa lo que te necesita. El progreso y los cambios no. Un resultado más nuevo en una tarea que aún no viste la actualiza sin una notificación nueva. Una ráfaga vibra una vez. El icono de la app muestra cuántas tareas te necesitan.

## Botones en las notificaciones

Cada notificación tiene botones para el siguiente paso. En la app del móvil:

- Tarea nueva: Hazlo, Posponer, Marcar como hecha.
- Borrador listo: Abrir borrador, Posponer, Marcar como hecha.
- Resultado listo: Abrir, Marcar como hecha, Posponer.
- Pregunta, atascada o con inicio de sesión: Responder, Abrir o Iniciar sesión, y luego Posponer y Marcar como hecha.
- Recordatorio: Marcar como hecha, Posponer, Abrir.
- Resumen matutino: tócalo para abrirlo.

Un navegador y Telegram muestran dos de ellos. Las preguntas del Fleet mantienen Responder una vez y Rechazar.

Desde una notificación nunca se envía, se paga ni se presenta nada. Un borrador siempre se abre primero, para que lo veas antes de que salga. Abrir borrador muestra la tarea en tu lista con el borrador completo. Hazlo solo empieza el trabajo en una tarea nueva.

En la app, Posponer y Marcar como hecha piden desbloquear primero. En un navegador abren el panel, que lo hace y muestra Deshacer. Posponer trae la tarea de vuelta en dos horas, o mañana por la mañana en un recordatorio.

Los correos con lo que te espera tienen enlaces Abrir y Posponer. Solo abren el panel.

## El resumen matutino

Llega los días laborables a tu hora de **Resumen matutino**, salvo que no haya nada que contar. Si es antes de **Lo pospuesto vuelve a las**, espera hasta 5 minutos después, para incluir las tareas que vuelven esa mañana. **Vista previa**, en su fila, lo muestra sin enviarlo. Por defecto es un push y un correo, cortos para leer de un vistazo:

- un saludo con lo que importa hoy, como "Buenos días, Sam: 2 respuestas listas para enviar" o, para una tarea, "Buenos días, Sam. Para revisar: Enviar el formulario de pedido";
- como mucho tres cosas que hacer, cada una con un enlace Abrir: primero los borradores para revisar y las promesas de hoy;
- cuántas más pueden esperar y cuánto te llevan a tu ritmo, como "12 más pueden esperar, unos 5 min para terminar." Las tareas que esperan tu respuesta no cuentan en ese tiempo.
- tus reuniones en una línea.

Abrir muestra esa tarea resaltada en tu lista. Si está hecha, pospuesta o en otra vista, se abre su chat. Una promesa abre su tarea, o su propia página si aún no tiene una.

El push dice lo mismo sin enlaces. Tócalo para abrir hoy en el **Calendario**.

## Privacidad

El push va de tu Machine directamente a tu dispositivo, cifrado para ese dispositivo. El plano de control nunca lo ve. El correo lo envía el servidor de correo de The Machine a la dirección de tu cuenta, así que el texto pasa por él y por el proveedor de correo. Cuando [Prudente](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo llevan recuentos. Desactiva **Correo** para un tipo si no quieres que llegue nunca por correo.

Activa el push para un dispositivo en **Este dispositivo**, o consulta [Instala la app](phone-app.md).
