---
title: Notificaciones
area: settings
summary: Qué te llega, por dónde y cuándo: push, Telegram o correo según el tipo, tu horario laboral y el resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
En **Ajustes**, **Notificaciones**, elige por tipo por dónde te llega:

- **Tareas nuevas**: una respuesta que alguien espera, una petición, cualquier cosa urgente.
- **Resultados y preguntas**: un borrador listo para aprobar o enviar, una tarea atascada o que necesita iniciar sesión, una pregunta del Fleet.
- **Recordatorios**: lo pospuesto y las esperas que vuelven.
- **Resumen matutino**: las reuniones de hoy, lo que vence, lo que llegó durante la noche y las primeras tareas que esperan, en el orden de tu lista de tareas.

Cada uno tiene un interruptor para **Push** (la app en tu teléfono u ordenador), **Telegram** cuando está configurado y **Correo** en una Machine alojada o en una que está en The Machine Network. Todos están activados, salvo el resumen en Telegram.

El **Horario laboral** está en la misma pestaña: tus días laborables, las horas en que pueden salir notificaciones, cuándo vuelve lo pospuesto, la hora del resumen y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Cuándo avisa

Como Slack, mira si estás usando el panel, no solo si está abierto:

- En uso: el panel está delante de ti, en primer plano, y has hecho clic, escrito, desplazado o tocado en los últimos 10 minutos. No vibra nada. Telegram llega sin sonido.
- Fuera: el panel está en segundo plano, minimizado, cerrado o inactivo durante 10 minutos. Un push sale un minuto después de que lo dejes, salvo que vuelvas y lo veas antes.
- Sin ver 15 minutos después: un solo correo con todo lo que aún te espera. Como mucho uno por hora. Lo que hayas resuelto mientras tanto, en Telegram o en otro sitio, queda fuera. Usar el panel después de que algo llegó cuenta como haberlo visto, así que un día en el panel puede no traer ningún correo.
- Fuera de tu horario laboral: nada. El resumen matutino trae lo que llegó.
- Una tarea nueva de trabajo que llega en un día libre espera a la hora del resumen de tu próximo día laborable. La tarea muestra dónde y cuándo te llegará, como Notificación lun, 2 nov · 08:30, según la fila **Tareas nuevas**. Con Push y Telegram apagados ahí, no dice nada.

Solo avisa lo que te necesita. El progreso y los cambios no. Una ráfaga vibra una vez. El icono de la app muestra cuántas tareas te necesitan.

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

Llega los días laborables a tu hora de **Resumen matutino**, y solo se omite cuando no hay nada que contar: ni reuniones, ni nada que venza o nuevo, ni tareas esperando. **Vista previa**, en su fila, lo muestra en la página sin enviarlo. Por defecto es un push y un correo. El push dice cuántas tareas esperan, las dos primeras y la hora de tu primera reunión. Al tocar el push se abre hoy en el **Calendario**.

## Privacidad

El push va de tu Machine directamente a tu dispositivo, cifrado para ese dispositivo. El plano de control nunca lo ve. El correo lo envía el servidor de correo de The Machine a la dirección de tu cuenta, así que el texto pasa por él y por el proveedor de correo. Cuando [Prudente](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo llevan recuentos. Desactiva **Correo** para un tipo si no quieres que llegue nunca por correo. También dice cuánto te llevan las tareas pendientes, como "4 para revisar · unos 2 min".

Activa el push para un dispositivo en **Este dispositivo**, o consulta [Instala la app](phone-app.md).
