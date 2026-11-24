---
title: Enviar más tarde
area: cards
summary: Pulsa **Enviar más tarde** junto a **Enviar ahora** para programar un correo o mensaje. Lo apruebas ahora y eliges cuándo se envía. Si la otra persona escribe primero, el mensaje vuelve a quedar pendiente de tu aprobación.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, schedule an email, send at a time, delay, tomorrow morning, unsend, take back
translated: 6fa6af155c337981
---
## Programar un mensaje

En la ventana donde revisas un mensaje, pulsa **Enviar más tarde** junto a **Enviar ahora**. Elige **Dentro de 2 horas**, **Mañana**, **lunes** o **Elegir fecha**, y pulsa **Guardar hora**. Se envía tal como lo viste, a esa hora en tu zona horaria.

Funciona con correo, Slack, WhatsApp, Telegram, Signal, Teams e Intercom. No funciona con LinkedIn ni X, porque tu Machine no puede comprobar si hay un mensaje nuevo justo antes de enviarlo, ni con las respuestas en documentos.

También está en **Nuevo correo**. Si revisas varios mensajes a la vez, todos se envían a la hora que elijas.

## Mientras espera

La tarea aparece en **Vuelve más tarde** y en el día correspondiente del [Calendario](calendar.md), con el mensaje y la hora de envío: «Se envía jue., 26 nov., 09:30». **Enviar ahora** lo envía de inmediato, **Cambiar hora** permite elegir otra hora y **Cancelar** lo convierte de nuevo en borrador. En el chat también aparece lo mismo.

Si editas el borrador, completas o descartas la tarea, o la vuelves a activar, el mensaje no se envía: necesitas aprobarlo de nuevo.

## Si la otra persona escribe primero

Si la otra persona escribe antes de que se envíe el mensaje, tu Machine no lo envía. La tarea vuelve a aparecer con su mensaje, por ejemplo: «No se envió: Sam Lee escribió primero». También recibes el aviso que recibirías con una tarea pospuesta. En el caso del correo, cuenta cualquier dirección que tu Machine tenga asociada a esa persona, en cualquier buzón que hayas conectado. También cuenta si responde otra persona de la conversación.

Una respuesta automática, como un mensaje de ausencia, no lo detiene. Tampoco lo detiene un mensaje tuyo.

Justo antes de enviarlo, tu Machine vuelve a leer la conversación. Si no puede, la tarea indica «Aún no se pudo comprobar si hay un mensaje nuevo» y vuelve a intentarlo durante una hora. Después, te pregunta en vez de enviarlo.

En WhatsApp, comprueba los mensajes recibidos hasta ese momento en tu propia cuenta de WhatsApp vinculada.

## Si The Machine está apagada

Si tu Machine está apagada, en reposo o has cerrado sesión a esa hora, el mensaje se envía cuando vuelva a estar disponible, con un retraso máximo de una hora. Después, la tarea vuelve a aparecer con el mensaje «No se envió: se retrasó más de una hora» y tú decides.

Si cambias de ordenador, tendrás que aprobar de nuevo los mensajes programados allí. Consulta [Cambiar de ordenador](moving.md).

## Quién puede programar mensajes

Solo tú, desde el panel de control o la app. Tu Machine, su chat, una IA que hayas conectado y otras Machines no pueden programar mensajes. En [Actividad](activity.md) puedes ver cuándo se programó, cambió, canceló, envió o no se envió un mensaje.
