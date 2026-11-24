---
title: Enviar más tarde
area: cards
summary: Da el visto bueno a un mensaje ahora y elige cuándo se envía. Si la otra persona escribe primero, volverá a quedar pendiente de ti.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, send at a time, delay, tomorrow morning, unsend, take back
translated: 29860e4848acce2e
---
## Programar un mensaje

En la ventana donde revisas un mensaje, pulsa **Enviar más tarde** junto a **Enviar ahora**. Elige **Dentro de 2 horas**, **Mañana**, **lunes** o **Elegir fecha**, y pulsa **Guardar hora**. Se envía tal como lo viste, a esa hora en tu zona horaria.

Funciona con correo, Slack, WhatsApp, Telegram, Signal, Teams e Intercom. No funciona con LinkedIn ni X, porque tu Machine no puede comprobar si hay un mensaje nuevo justo antes de enviarlo, ni con respuestas en documentos.

También está disponible en **Nuevo correo**. Si revisas varios mensajes a la vez, todos se envían a la hora que elijas.

## Mientras espera

La tarea aparece en **Vuelve más tarde** y en el día que le corresponde en [Calendario](calendar.md), junto con el mensaje y la hora de envío: «Se envía jue., 26 nov, 09:30». **Enviar ahora** lo envía de inmediato, **Cambiar hora** permite elegir otra hora y **Cancelar** vuelve a convertirlo en borrador. En el chat aparece lo mismo.

Si editas el borrador, completas la tarea, la descartas o la recuperas, no se envía: necesita que vuelvas a dar el visto bueno.

## Si la otra persona escribe primero

Si la otra persona escribe antes de que se envíe, tu Machine no lo envía. La tarea vuelve con su mensaje, por ejemplo: «No se ha enviado: Sam Lee ha escrito primero», y recibes el aviso que recibirías con una tarea pospuesta. En el caso del correo, cuenta cualquier dirección que tu Machine tenga asociada a esa persona, en cualquier bandeja de entrada que hayas conectado. También cuenta si responde otra persona en la conversación.

Una respuesta automática, como un mensaje de fuera de la oficina, no lo detiene. Tampoco lo hace un mensaje tuyo.

Justo antes de enviarlo, tu Machine vuelve a leer la conversación. Si no puede, la tarea muestra «Aún no se ha podido comprobar si hay mensajes nuevos» e intenta comprobarlo durante una hora. Después, te pregunta en lugar de enviarlo.

En WhatsApp, comprueba los mensajes que ha recibido hasta ese momento tu WhatsApp vinculado.

## Si The Machine está apagada

Si tu Machine está apagada, en reposo o con la sesión cerrada a esa hora, el mensaje se envía cuando vuelva a estar disponible, con hasta una hora de retraso. Después de ese plazo, la tarea vuelve con el mensaje «No se ha enviado: lleva más de una hora de retraso» y tú decides.

Si cambias de ordenador, los mensajes programados vuelven a pedirte confirmación allí. Consulta [Cambiar de ordenador](moving.md).

## Quién puede programar mensajes

Solo tú, desde el panel de control o la app. Tu Machine, su chat, una IA que hayas conectado y otras Machines no pueden programar mensajes. [Actividad](activity.md) muestra cuándo se programó, cambió, canceló, envió o no se envió un mensaje.
