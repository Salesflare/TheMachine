---
title: Habla en vivo
area: cards
summary: Una conversación hablada con The Machine sobre una tarea, con la voz de OpenAI. Funciona en el chat de la tarea y solo envía un borrador cuando das tu aprobación.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: 60168384f08de74e
---
## Empieza una conversación

En el chat de una tarea, toca la onda que aparece junto al micrófono y permite el acceso al micrófono si te lo pide. Cuando la barra indique **En marcha**, habla como si estuvieras en una llamada. The Machine responde en voz alta. Puedes interrumpirla hablando.

Conoce esta tarea: sus mensajes, su borrador y su chat. También puede consultar tus otras tareas. Di «marca esto como hecho», «pospónlo hasta mañana a las 9» o «no hace falta» y lo hará. Di «no, eso no» justo después para deshacerlo. Las horas siguen la zona horaria de tu [Horario laboral](work-hours.md).

Escucha en el idioma de la aplicación y en los idiomas que indica tu navegador. No responde a tos, ruidos ni a otros idiomas, y no los incluye en la transcripción.

La barra tiene las opciones **Silenciar** y **Fin**. Despídete y la conversación terminará automáticamente. Puede durar hasta 10 minutos. Durante el último minuto verás una cuenta atrás. Vuelve a empezar para continuar.

## Habla sobre todas tus tareas

Toca **Hablar** en la barra lateral (en el menú, si usas un móvil). The Machine te dice cuántas tareas tienes pendientes y va revisando una por una las que aparecen en **Para ti**, empezando por las más urgentes. Te avisa cuando una tarea marcada como **Preparando…** está lista.

Hablar tiene su propia página: la tarea que estáis revisando aparece arriba, junto con su borrador y la opción **Abrir el chat**.

Pídele que lea un borrador, lo cambie, posponga la tarea, la marque como hecha o pase a la siguiente. Lo que digas sobre una tarea se añade a su chat. Cuando haya una pausa, te hablará de las tareas nuevas. Di «añade una tarea para...» para añadir una sin perder tu sitio.

Pregunta por una persona, organización, proyecto, reunión o promesa, y lo buscará y te lo mostrará. También puede descartar, cambiar el nombre o volver a abrir tareas, incluidas las que aparecen en **Hecho / descartado**. Para cualquier otra cosa, pasa la pregunta al chat de una tarea nueva y te dice la respuesta.

Recuerda las conversaciones que habéis tenido antes. Pregunta «¿qué decidí sobre la reunión fuera de la oficina?» y te lo dirá, junto con cuándo lo dijiste. Solo Hablar en la barra lateral puede hacerlo.

Mientras tanto, puedes usar otras páginas: la barra seguirá en la parte inferior y **Hablar** te llevará de vuelta. Esta conversación puede durar hasta 30 minutos. En ordenadores y Android, continúa en segundo plano. En iPhone, se detiene cuando sales de la aplicación.

## Pide cosas y confirma antes de enviar

Pide algo, como «escribe una respuesta diciendo que el jueves me va bien», y The Machine lo pasa al chat de la tarea como si lo hubieras escrito tú. El chat sigue sus reglas habituales.

El chat también puede buscar información, como el horario de apertura de una tienda. Muestra **Trabajando en ello…** y puedes seguir hablando. Cuando tenga la respuesta, The Machine te la dice y te cuenta dónde la encontró.

Para enviar un borrador, díselo. The Machine lo lee en voz alta (a quién va dirigido, el asunto y el texto) y te pregunta algo como «¿Envío esta respuesta por correo a Sam?». Puedes hacerlo con el móvil en el bolsillo. Di claramente que sí, por ejemplo, «sí, envíala», y se enviará ese borrador.

- Envía exactamente el borrador que ha leído. Si el borrador cambia, lo vuelve a leer y te lo pregunta de nuevo. Si no respondes en 3 minutos, la pregunta caduca.
- Si no das un sí claro, no se envía nada.
- Si ya has visto u oído un borrador, no lo vuelve a leer. Solo pregunta algo como «¿Se lo envío a Pat?».
- Di «envía todos los que estén listos» y te dirá los nombres en una sola pregunta. Con un sí, los envía todos.
- Cuando dices que sí, Talk muestra **Deshacer** junto con una cuenta atrás. Tócalo o di «deshazlo» o «espera».
- Una vez enviado, Talk dice «Enviado.» y la tarea muestra **Enviado a** esa persona, junto con la hora. Si no se ha podido enviar, Talk te dice por qué. Pregunta «¿se ha enviado?» cuando quieras: lo comprueba, nunca lo adivina.

También puedes tocar **Aprobar**.

Di «hazlo» para que The Machine empiece a trabajar en la tarea, igual que con **Hazlo**. Di «informa de un error» para enviar un informe de error, igual que con **Informar de un error** en Ayuda.

## Elige una voz

En **Ajustes**, **General**, dentro de **Entrada de voz**, elige una **Voz** y toca el botón de reproducción para escucharla. **Cedar** es la opción predeterminada. La voz Cove de ChatGPT no está disponible.

## Un registro en el chat

Todo lo que digas se añade al chat de la tarea, debajo de la línea **Habló en vivo**, para que puedas leerlo más tarde.

## Qué necesitas

Hablar en vivo usa la voz de OpenAI, así que tu Machine necesita una de estas opciones:

- Iniciar sesión en ChatGPT: incluido en los planes que lo ofrecen.
- Una clave de API de OpenAI: OpenAI te cobra por minuto y la barra te lo indica. Si tienes ambas opciones, tu Machine usa la clave.

En **Ajustes**, **General**, **Entrada de voz** puedes ver si Hablar en vivo está listo. Si no tienes OpenAI, no aparecerá la onda. El audio va directamente desde tu navegador a OpenAI.

## Si no funciona

- **El micrófono está bloqueado**: permite el acceso al micrófono para este sitio en los ajustes del navegador.
- **No se ha podido iniciar Hablar en vivo**: comprueba que hayas iniciado sesión en ChatGPT o que la clave de OpenAI sea correcta, e inténtalo de nuevo.
- **Se ha perdido la conexión de Hablar en vivo**: vuelve a empezar. Lo que se haya dicho seguirá en el chat.
- Si dice que no entiende lo que dices, comprueba el micrófono o escribe en el chat.
