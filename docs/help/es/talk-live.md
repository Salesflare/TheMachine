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

Conoce la tarea en la que estás: sus mensajes, su borrador y su chat. También puede consultar tus otras tareas. Di "márcala como hecha", "posponla" o "no hace falta" y lo hace ella misma. Di "no, eso no" justo después para deshacerlo.

Escucha en tus idiomas: el de la app y los que indica tu navegador. Un ruido, una tos o un sonido en otro idioma no recibe respuesta y no queda en la transcripción.

La barra tiene **Silenciar** y **Fin**. Despídete, o di que ya terminaste, y termina sola. Una conversación dura hasta 10 minutos. Un minuto antes del final, el temporizador muestra cuánto queda. Vuelve a empezarla para seguir.

## Repasa todas tus tareas hablando

Toca **Hablar** en la barra lateral (en el menú en un teléfono) para repasar con la voz todo lo que te espera. The Machine dice cuántas hay y las toma una por una: primero **Lista**, luego **Por decidir**. También ve tus otras tareas, como las que siguen **Preparando**, y te avisa cuando una está lista.

Hablar tiene su propia página: una conversación de principio a fin, con la tarea de la que habla arriba, su borrador y **Abrir el chat**. No te lleva de chat en chat.

Pídele que lea un borrador, lo cambie, lo posponga, lo marque como hecho o pase a la siguiente. Enviar funciona como en el chat de una tarea: un borrador por pregunta, tras un sí claro. Lo que dices sobre una tarea queda en el chat de esa tarea. Si llega una tarea nueva, te la menciona en una pausa. Di "añade una tarea para..." y crea una nueva sin dejar la que tienes abierta.

También llega al resto de The Machine. Pregunta por una persona, una organización, un proyecto, una reunión o una promesa, y lo busca y te lo muestra. Puede posponer una tarea, marcarla como hecha, descartarla, cambiarle el nombre o reabrirla, también una de **Hecho / descartado**. Para todo lo demás, crea una tarea, deja que su chat se encargue y te dice la respuesta.

Mientras tanto puedes ir a otra página: la barra queda abajo, y **Hablar** en la barra lateral te trae de vuelta. Esta conversación dura hasta 30 minutos. Sigue en segundo plano en computadoras y Android. En iPhone, se detiene cuando la app sale de la pantalla.

## Pide cosas y envía con un sí

Cuando pides algo, como "escribe una respuesta diciendo que el jueves me va bien" o "pospón esto hasta el lunes", The Machine se lo pasa al chat de la tarea, como si lo hubieras escrito. El chat sigue sus reglas de siempre: puede cambiar el borrador o posponer la tarea.

El chat también puede buscar cosas, como el horario de una tienda en la web. Mientras tanto muestra **Trabajando en ello…**, y puedes seguir hablando. Cuando la respuesta está lista, The Machine te la dice, y dónde la encontró. Si pides otra cosa mientras tanto, espera su turno.

Para enviar un borrador, dilo. The Machine pregunta primero, diciendo a quién y cómo, por ejemplo "¿Envío esta respuesta a Lotte por correo?". Primero lee el borrador entero en voz alta: a quién va, el asunto y el texto. Así funciona también con el teléfono en el bolsillo. Responde con un sí claro, como "sí, envíalo", y ese borrador se envía.

- Envía exactamente el borrador que leyó. Si cambia después de la pregunta, lo vuelve a leer y vuelve a preguntar. Una pregunta sin respuesta en 3 minutos caduca.
- Si tu respuesta no es un sí claro, no se envía nada y vuelve a preguntar. "No" no envía nada.
- Un borrador que ya viste en pantalla, o que oíste en esta conversación, no se vuelve a leer: solo pregunta, por ejemplo "¿Se lo envío a Nick?".
- Di "envía los dos" o "envía todos los listos" y nombra a todos en una pregunta. Un sí envía cada uno.
- Hablar muestra **Deshacer** con el destinatario y una cuenta atrás unos segundos antes de que salga, y luego **Enviado a** esa persona. Tócalo, o di "deshacer" o "espera".

Siempre puedes tocar **Aprobar** en su lugar.

"Hazlo" pone a The Machine con la tarea, como **Hazlo**, también en el navegador. "Márcala como hecha" la cierra. Di "informa de un error" y envía un informe, como **Informar de un error** en Ayuda, preguntando antes si puede añadir más.

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
- Si dice que no entiende lo que dices, lo que dijiste no llegó dos veces seguidas. Revisa el micrófono o escribe en el chat. Lo dice una vez y luego espera hasta oírte.
