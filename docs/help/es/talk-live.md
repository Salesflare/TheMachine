---
title: Hablar en vivo
area: cards
summary: Una conversación hablada con The Machine sobre una tarea, con la voz de OpenAI. Funciona en el chat de la tarea y solo envía un borrador cuando dices que sí.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: f5555cb693a23682
---
## Empieza una conversación

En el chat de una tarea, toca la onda junto al micrófono y permite el acceso al micrófono si te lo pide. Cuando la barra indique **En marcha**, habla como si estuvieras en una llamada. The Machine te responde en voz alta. Habla por encima para interrumpirla.

Conoce esta tarea: sus mensajes, el borrador y el chat. También puede consultar tus otras tareas. Di «marca esto como hecho», «pospónla hasta mañana a las 9» o «no hace falta» y lo hará. Di «no, eso no» justo después para deshacerlo. Las horas siguen la zona horaria de tu [Horario laboral](work-hours.md).

Escucha en el idioma de la app y en los idiomas que aparecen en la lista de tu navegador. No responde a toses, ruidos ni a otros idiomas, y estos no aparecen en la transcripción.

La barra tiene las opciones **Silenciar** y **Finalizar**. Despídete y terminará automáticamente. La conversación dura hasta 10 minutos; durante el último minuto verás una cuenta atrás. Vuelve a empezar para continuar.

## Habla sobre todas tus tareas

Toca **Hablar** en la barra lateral (en el menú, si usas un móvil). The Machine te dice cuántas tareas están pendientes y va revisando las de **Para ti** una por una, en el orden en que aparecen en tu lista. Te avisa cuando una tarea marcada como **Preparando…** está lista.

Hablar tiene su propia página: la tarea que estáis revisando aparece arriba, junto con su borrador y **Abrir el chat**.

Pídele que lea un borrador, lo cambie, lo posponga, lo marque como hecho o pase a la siguiente tarea. Lo que digas sobre una tarea se añade a su chat. Menciona las tareas nuevas cuando hay una pausa. Di «añade una tarea para...» para añadir una sin perder el hilo.

Pregunta por una persona, organización, proyecto, reunión o promesa, y lo buscará y te lo mostrará. También puede descartar, cambiar el nombre o volver a abrir tareas, incluidas las que están en **Hecho / descartado**. Para cualquier otra cosa, pasa la pregunta al chat de una tarea nueva y te dice la respuesta.

Recuerda tus conversaciones anteriores. Pregúntale «¿qué decidí sobre la reunión fuera de la oficina?» y te lo dirá, además de decirte cuándo lo dijiste. Solo Hablar en la barra lateral puede hacerlo.

Mientras tanto, puedes usar otras páginas: la barra se queda abajo y **Hablar** te lleva de vuelta. Esta conversación dura hasta 30 minutos. En ordenadores y Android, continúa en segundo plano. En iPhone, se detiene cuando la app deja de estar en pantalla.

## Pide cosas y envía cuando confirmes

Pide algo, por ejemplo «escribe una respuesta diciendo que el jueves me va bien», y The Machine se lo pasa al chat de la tarea como si lo hubieras escrito tú. El chat sigue sus reglas habituales.

El chat también puede buscar información, como el horario de apertura de una tienda. Muestra **Trabajando en ello…** y puedes seguir hablando. Cuando tiene la respuesta, The Machine te la dice y te cuenta dónde la encontró.

Para enviar un borrador, díselo. The Machine lo lee en voz alta (a quién va dirigido, el asunto y el texto) y te pregunta algo como «¿Envío esta respuesta por correo a Sam?». Puedes tener el móvil en el bolsillo. Di que sí claramente, por ejemplo «sí, envíala», y se enviará el borrador.

- Envía exactamente el borrador que ha leído. Si el borrador cambia, lo vuelve a leer y te lo pregunta otra vez. Si no respondes a una pregunta en 3 minutos, caduca.
- Si no dices claramente que sí, no se envía nada.
- Si ya has visto u oído un borrador, no lo vuelve a leer. Solo pregunta, por ejemplo, «¿Se lo envío a Pat?».
- Di «envía todos los que estén listos» y mencionará a todos en una sola pregunta. Con un sí, los envía todos.
- Después de que digas que sí, Hablar muestra **Deshacer** con una cuenta atrás. Tócalo o di «deshazlo» o «espera».
- Una vez enviado, Hablar dice «Enviado» y la tarea muestra **Enviado a** esa persona, junto con la hora. Si no se ha podido enviar, Hablar te dice por qué. Pregunta «¿se ha enviado?» en cualquier momento: lo comprueba, nunca lo da por hecho.

También puedes tocar **Aprobar**.

Di «hazlo» para que The Machine empiece a trabajar en la tarea, igual que con **Hazlo**. Di «informa de un error» para enviar un informe de errores, como con **Informar de un error** en Ayuda.

## Elige una voz

En **Ajustes**, **General**, dentro de **Entrada de voz**, elige una **Voz** y toca reproducir para escucharla. **Cedar** es la opción predeterminada. La voz Cove de ChatGPT no está disponible.

## Un registro en el chat

Todo lo que dices aparece en el chat de la tarea, debajo de una línea **Habló en vivo**, para que puedas volver a leerlo más tarde.

## Qué necesitas

Hablar en vivo usa la voz de OpenAI, así que tu Machine necesita una de estas opciones:

- Una cuenta de ChatGPT: incluida en los planes que la ofrecen.
- Una clave de API de OpenAI: OpenAI cobra por minuto y la barra te lo indica. Si tienes ambas opciones, tu Machine usa la clave.

En **Ajustes**, **General**, **Entrada de voz** puedes ver si Hablar en vivo está disponible. Si no tienes OpenAI, no aparece la onda. El audio va directamente desde tu navegador a OpenAI.

## Si no funciona

- **El micrófono está bloqueado**: permite el acceso al micrófono para este sitio en los ajustes de tu navegador.
- **No se ha podido iniciar Hablar en vivo**: comprueba tu cuenta de ChatGPT o tu clave de OpenAI e inténtalo de nuevo.
- **Hablar en vivo ha perdido la conexión**: vuelve a empezar. Lo que se haya dicho seguirá en el chat.
- Dice que no entiende lo que has dicho: comprueba el micrófono o escribe en el chat.
