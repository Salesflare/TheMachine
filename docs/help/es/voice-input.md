---
title: Entrada de voz
area: cards
summary: Habla en lugar de escribir. Lo que dices aparece en el cuadro de mensaje para que lo revises. No se envía nada.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
---
## Habla en lugar de escribir

Toca el micro en un cuadro de mensaje: el chat de una tarea, **Nueva tarea**, **Ayuda**, o el cuadro para cambiar un borrador. Habla y luego toca la marca de verificación. O mantén pulsado el micro mientras hablas y suéltalo cuando termines.

Mientras escucha, el cuadro muestra un temporizador. Toca la cruz para parar sin guardar nada. Una grabación puede durar hasta 2 minutos; a los 2 minutos se detiene sola y escribe lo que dijiste.

Lo que dijiste aparece en el cuadro, donde estaba tu cursor. No se envía nada: léelo, cambia lo que quieras y envíalo tú.

## La primera vez

La primera vez que tocas el micro, tu Machine prepara la voz. Descarga el modelo de voz una sola vez, unos 600 MB, y muestra "Preparando la voz…" con el progreso. Tarda unos minutos. Tu grabación espera y se escribe en cuanto todo está listo.

## Adónde va tu voz

Por defecto, tu grabación se pasa a texto en tu propia Machine. Nunca sale de ella y se borra en cuanto vuelve el texto. No se usa el reconocimiento de voz de tu navegador, porque algunos navegadores envían tu voz a su fabricante.

En **Ajustes**, **General**, bajo **Entrada de voz**, puedes elegir:

- **Pasado a texto**: **En esta Machine**, o **Con OpenAI**. OpenAI es más rápido en un servidor pequeño, pero tu grabación va a OpenAI, con tu propia clave. Necesita una clave API de OpenAI en OpenClaw. Un inicio de sesión de ChatGPT no la incluye.
- **Precisión**: **Más preciso** funciona mejor para la mayoría de los idiomas y, en un servidor pequeño, tarda más o menos lo que hablaste. **Más rápido** va más deprisa, pero se equivoca en más palabras.
- **Idioma**: **Detectar** funciona con todos los idiomas de la app. Elegir el tuyo es un poco más rápido.

## Si no funciona

- **El micro está bloqueado**: permite el micro para este sitio en los ajustes de tu navegador. En la app del teléfono, está en los permisos de la app.
- **No se encontró ningún micro**: conecta uno e inténtalo de nuevo.
- **No se puede conectar con tu Machine**: tu grabación se guarda. Toca **Reintentar** cuando tu Machine vuelva.
- **No entendí nada**: habla un poco más cerca del micro, o durante más tiempo.
