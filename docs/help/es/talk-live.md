---
title: Hablar en vivo
area: cards
summary: Una conversación en voz alta con The Machine sobre una tarea, con la voz de OpenAI. Trabaja en el chat de la tarea y solo envía un borrador después de que digas que sí.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Empieza una conversación

En el chat de una tarea, toca la onda junto al micro. Permite el micro si tu navegador lo pide. Cuando la barra diga **En vivo**, habla como en una llamada. The Machine responde en voz alta, y puedes hablar encima para interrumpirla.

Conoce la tarea en la que estás: sus mensajes, su borrador y su chat. También puede consultar tus otras tareas.

La barra tiene **Silenciar** y **Fin**. Una conversación dura hasta 10 minutos. Un minuto antes del final, el temporizador muestra cuánto queda. Vuelve a empezarla para seguir.

## Pide cosas y envía con un sí

Cuando pides algo, como "escribe una respuesta diciendo que el jueves me va bien" o "pospón esto hasta el lunes", The Machine se lo pasa al chat de la tarea, como si lo hubieras escrito. El chat sigue sus reglas de siempre: puede cambiar el borrador o posponer la tarea.

El chat también puede buscar cosas, como el horario de una tienda en la web. Mientras tanto muestra **Trabajando en ello…**, y puedes seguir hablando. Cuando la respuesta está lista, The Machine te la dice, y dónde la encontró. Si pides otra cosa mientras tanto, espera su turno.

Para enviar un borrador, dilo. The Machine pregunta primero, diciendo a quién y cómo, por ejemplo "¿Envío esta respuesta a Lotte por correo?". En un teléfono, lee antes el borrador entero en voz alta. Responde con un sí claro, en cualquier idioma, y ese borrador se envía.

- Solo pregunta por el borrador que se ve en el chat. Si cambia después de la pregunta, vuelve a preguntar.
- Si tu respuesta no es un sí claro, no se envía nada y vuelve a preguntar. "No" no envía nada.
- Un sí envía siempre un solo borrador. Para enviar varios, usa la revisión de seguimientos.
- El chat muestra **Aprobado por voz** con **Deshacer** unos segundos antes de que salga.

Siempre puedes tocar **Aprobar** en su lugar.

## Elige una voz

En **Ajustes**, **General**, en **Entrada de voz**, elige en **Voz** cómo suena The Machine. Toca reproducir para oír una muestra. **Cedar** es la voz por defecto. La voz Cove de ChatGPT no está disponible para hablar en vivo.

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
