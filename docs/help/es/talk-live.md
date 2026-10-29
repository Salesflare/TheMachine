---
title: Hablar en vivo
area: cards
summary: Una conversación en voz alta con The Machine sobre una tarea, con la voz de OpenAI. Trabaja en el chat de la tarea, pero nunca envía nada.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Empieza una conversación

En el chat de una tarea, toca la onda junto al micro. Permite el micro si tu navegador lo pide. Cuando la barra diga **En vivo**, habla como en una llamada. The Machine responde en voz alta, y puedes hablar encima para interrumpirla.

Conoce la tarea en la que estás: sus mensajes, su borrador y su chat. También puede consultar tus otras tareas.

La barra tiene **Silenciar** y **Fin**. Una conversación dura hasta 10 minutos. Un minuto antes del final, el temporizador muestra cuánto queda. Vuelve a empezarla para seguir.

## Nada se envía desde una conversación

Cuando pides algo, como "escribe una respuesta diciendo que el jueves me va bien" o "pospón esto hasta el lunes", The Machine se lo pasa al chat de la tarea, como si lo hubieras escrito. El chat sigue sus reglas de siempre: puede cambiar el borrador o posponer la tarea, pero un borrador espera tu **Aprobar**.

Decir "sí" o "envíalo" no hace nada. Solo envía tu toque en **Aprobar**.

## Un registro en el chat

Lo que dicen los dos se escribe en el chat de la tarea, bajo una línea **Habló en vivo**. Puedes releerlo después.

## Qué necesitas

Hablar en vivo usa la voz en tiempo real de OpenAI, así que OpenAI tiene que estar configurado en OpenClaw:

- Un inicio de sesión de ChatGPT: incluido en tu plan, si tu plan tiene acceso.
- Una clave de API de OpenAI: OpenAI cobra a tu clave por minuto de conversación, y la barra lo indica. Si los dos están configurados, OpenClaw usa la clave.

**Ajustes**, **General**, **Entrada de voz** muestra si Hablar en vivo está listo. Sin OpenAI, la onda no aparece. Tu audio va de tu navegador directamente a OpenAI. Tu clave nunca llega al navegador.

## Si no funciona

- **El micro está bloqueado**: permite el micro para este sitio en los ajustes de tu navegador.
- **Hablar en vivo no pudo empezar**: revisa OpenAI en OpenClaw e inténtalo de nuevo.
- **Hablar en vivo perdió la conexión**: vuelve a empezarlo. Lo dicho hasta ahora sigue en el chat.
