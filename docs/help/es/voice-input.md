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

Mientras escucha, el cuadro muestra un temporizador. Toca la cruz para parar sin guardar nada. Una grabación puede durar hasta 2 minutos; a los 2 minutos se detiene sola y escribe lo que dijiste. Lo que ya oyó aparece en la barra mientras hablas, así el texto está listo poco después de parar.

Lo que dijiste aparece en el cuadro, donde estaba tu cursor. No se envía nada: léelo, cambia lo que quieras y envíalo tú.

## Adónde va tu voz

En **Ajustes**, **General**, bajo **Entrada de voz**, una línea corta dice cuál se usa.

- **Automático** (por defecto): cuando OpenAI está configurado en OpenClaw, OpenAI pasa tu grabación a texto. Eso es una clave de API, o un inicio de sesión de ChatGPT si tu plan permite audio. Sin OpenAI, se pasa a texto en tu propia Machine y nunca sale de ella.
- **En esta Machine**: siempre en tu Machine, aunque OpenAI esté configurado.
- **Con OpenAI**: siempre OpenAI.

Una grabación se borra en cuanto vuelve el texto.

## Preparación

Para pasar la voz a texto ella misma, tu Machine necesita un modelo de voz de 150 a 500 MB. Lo descarga en segundo plano, con prioridad baja, cuando ya está configurada, terminó su primera revisión y lleva un rato tranquila. Mientras tanto, Ajustes muestra **Preparándose (en segundo plano)**. Nunca lo hace cuando se usa OpenAI.

Hasta que esté lista, **Automático** usa el reconocimiento de voz de tu navegador si tiene uno, y lo dice bajo el cuadro. Algunos navegadores lo envían a su fabricante. Con **En esta Machine** elegido, tu grabación espera y el cuadro muestra "Preparando la voz…" con el tiempo que falta.

## Ajustes

- **Pasado a texto**: **Automático**, **En esta Machine** o **Con OpenAI**.
- **Precisión** (solo en tu Machine): **Más preciso** funciona mejor para la mayoría de los idiomas. **Más rápido** va más rápido pero se equivoca en más palabras. En una Machine Standard, que tiene menos memoria, **Más rápido** es el valor por defecto.
- **Idioma**: **Detectar** funciona para todos los idiomas de la app. Elegir el tuyo es un poco más rápido.

Para hablar en voz alta con The Machine, mira [Hablar en vivo](talk-live.md).

## Si no funciona

- **El micro está bloqueado**: permite el micro para este sitio en los ajustes de tu navegador. En la app del teléfono, está en los permisos de la app.
- **No se encontró ningún micro**: conecta uno e inténtalo de nuevo.
- **No se puede conectar con tu Machine**: tu grabación se guarda y se escribe cuando tu Machine vuelva. Para intentarlo antes, toca **Probar ahora**.
- **No entendí nada**: habla un poco más cerca del micro, o durante más tiempo.
