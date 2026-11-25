---
title: Hablar en vivo
area: cards
summary: Una conversación hablada con The Machine sobre una tarea, con la voz de OpenAI. Funciona en el chat de la tarea y solo envía un borrador cuando dices que sí.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: da63957f0556ff4f
---
## Iniciar una conversación

En el chat de una tarea, toca la onda junto al micrófono y permite el acceso al micrófono si te lo pide. Cuando la barra indique **En marcha**, habla como si estuvieras en una llamada. The Machine responde en voz alta. Interrúmpela hablando por encima.

Conoce esta tarea: sus mensajes, su borrador y su chat. También puede consultar tus otras tareas. Di «marca esto como hecho», «pospónla hasta mañana a las 9» o «no hace falta» y lo hará. Di «no, eso no» justo después para deshacerlo. Las horas siguen la zona horaria de tu [Horario laboral](work-hours.md).

Escucha en el idioma de la app y en los idiomas que aparecen en tu navegador. No responde a toses, ruidos ni a otros idiomas, y estos no aparecen en la transcripción.

La barra tiene las opciones **Silenciar** y **Finalizar**. Despídete y la conversación terminará automáticamente. Cada conversación dura hasta 10 minutos; durante el último minuto aparece una cuenta atrás. Empieza otra para continuar.

## Hablar sobre todas tus tareas

Toca **Hablar** en la barra lateral (en el menú, si usas un móvil). The Machine te dice cuántas tareas hay pendientes y va revisando una por una las que aparecen en **Para ti**, en el orden de la lista. Te avisa cuando está lista una tarea que aparece como **Preparando…**.

Hablar tiene su propia página: la tarea en la que estás aparece arriba, junto con su borrador y **Abrir el chat**.

Pídele que lea un borrador, lo cambie, lo posponga, lo marque como hecho o pase a la siguiente tarea. Lo que digas sobre una tarea se añade a su chat. Menciona las tareas nuevas cuando hay una pausa. Di «añade una tarea para...» para añadir una sin perder el hilo.

Pregunta por una persona, organización, proyecto, reunión o promesa y la buscará y te mostrará la información. También puede descartar, cambiar el nombre o reabrir tareas, incluidas las que están en **Hecho / descartado**. Para cualquier otra cosa, pasa la pregunta al chat de una tarea nueva y te da la respuesta.

Recuerda las conversaciones anteriores que has tenido con ella. Pregunta «¿qué decidí sobre la reunión fuera de la oficina?» y te lo dirá, junto con cuándo lo dijiste. Solo la opción Hablar de la barra lateral puede hacerlo.

Mientras tanto, puedes estar en otras páginas: la barra permanece en la parte inferior y **Hablar** te lleva de vuelta. Esta conversación dura hasta 30 minutos. Continúa en segundo plano en ordenadores y Android. En iPhone, se detiene cuando sales de la app.

## Pide cosas y confirma el envío

Pide algo, como «escribe una respuesta diciendo que el jueves me va bien», y The Machine se lo pasa al chat de la tarea como si lo hubieras escrito tú. El chat sigue sus reglas habituales.

El chat también puede buscar información, como el horario de una tienda. Te indica que está buscando y puedes seguir hablando. Cuando encuentra la respuesta, The Machine te la dice y te cuenta dónde la encontró.

Para enviar un borrador, díselo. The Machine lo lee en voz alta (a quién va dirigido, el asunto y el texto) y pregunta algo como «¿Envío esta respuesta por correo a Sam?». Puedes hacerlo con el móvil en el bolsillo. Di claramente que sí, por ejemplo «sí, envíala», y se enviará el borrador.

- Envía exactamente el borrador que ha leído. Si el borrador cambia, lo vuelve a leer y te pregunta otra vez. Si no respondes en 3 minutos, la pregunta caduca.
- Si no dices claramente que sí, no se envía nada.
- Si ya has visto u oído un borrador, no lo vuelve a leer. Solo pregunta algo como «¿Se lo envío a Pat?».
- Di «envía todos los que estén listos» y nombrará a todas las personas en una sola pregunta. Con un sí, los enviará todos.
- Después de que digas que sí, Hablar muestra **Deshacer** junto con una cuenta atrás. Tócalo o di «deshazlo» o «espera».
- Una vez enviado, Hablar dice «Enviado» y la tarea muestra **Enviado a** esa persona, junto con la hora. Si no se ha podido enviar, Hablar te dice por qué. Pregunta «¿se ha enviado?» en cualquier momento para que lo compruebe. Nunca lo adivina.

También puedes tocar **Aprobar**.

Di «hazlo» para que The Machine empiece a trabajar en la tarea, igual que con **Hazlo**. Di «informa de un error» para enviar un informe de error, igual que con **Informar de un error** en Ayuda.

## Elegir una voz

En **Ajustes**, en **General**, debajo de **Entrada de voz**, elige una **Voz** y toca el botón de reproducción para escucharla. **Cedar** es la voz predeterminada. La voz Cove de ChatGPT no está disponible.

## Un registro en el chat

Todo lo que se dice aparece en el chat de la tarea, debajo de una línea **Habló en vivo**, para que puedas consultarlo más tarde.

## Qué necesitas

Hablar en vivo usa la voz de OpenAI, así que tu Machine necesita una de estas opciones:

- Una sesión iniciada en ChatGPT: está incluida en los planes que la ofrecen.
- Una clave de API de OpenAI: OpenAI cobra por minuto y la barra lo indica. Si tienes ambas opciones, tu Machine usa la clave.

En **Ajustes**, **General**, **Entrada de voz** indica si Hablar en vivo está listo. Si no tienes OpenAI, no aparece la onda. El audio se envía directamente desde el navegador a OpenAI.

## Si no funciona

- **El micrófono está bloqueado**: permite el acceso al micrófono para este sitio en los ajustes del navegador.
- **No se pudo iniciar Hablar en vivo**: comprueba que hayas iniciado sesión en ChatGPT o que la clave de OpenAI sea correcta, e inténtalo de nuevo.
- **Hablar en vivo perdió la conexión**: vuelve a empezar. Lo que se haya dicho seguirá en el chat.
- Si indica que no entiende lo que dices, comprueba el micrófono o escribe en el chat.
