---
title: Entrada de voz
area: cards
summary: Habla en vez de escribir. Lo que digas aparecerá en el cuadro de mensaje para que lo revises. No se envía nada.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
translated: f311b21bb4996eb4
---
## Habla en vez de escribir

Toca el micrófono en un cuadro de mensaje: en el chat de una tarea, en **Nueva tarea**, **Ayuda** o en el cuadro para cambiar un borrador. Habla y luego toca la marca de verificación. También puedes mantener pulsado el micrófono mientras hablas y soltarlo cuando termines.

Mientras escucha, el cuadro muestra un temporizador y lo que ha oído hasta el momento. Toca la X para detener la grabación sin guardar nada. La grabación se detiene automáticamente después de 2 minutos.

El texto aparece en el cuadro, donde estaba el cursor. No se envía nada: léelo, haz los cambios que quieras y envíalo tú.

## Adónde va tu voz

Elige una opción en **Ajustes**, **General**, en **Entrada de voz**. Ahí se indica brevemente cuál está en uso.

- **Automático** (la opción predeterminada): OpenAI convierte la grabación en texto cuando tu Machine usa OpenAI (con una clave de OpenAI o un plan de ChatGPT que permite usar audio). De lo contrario, tu Machine lo hace por su cuenta y la grabación no sale de ella.
- **En esta Machine**: siempre en tu Machine, incluso si OpenAI está configurado.
- **Con OpenAI**: siempre con OpenAI.

La grabación se elimina en cuanto el texto está listo.

## Preparación

Para convertir la voz en texto por su cuenta, tu Machine primero descarga un modelo de voz (de 150 a 500 MB) en segundo plano, cuando no está en uso. Mientras tanto, en Ajustes aparece **Preparándose en segundo plano**. Se omite este paso si se usa OpenAI.

Hasta entonces, **Automático** usa el reconocimiento de voz propio del navegador, si lo tiene, y lo indica debajo del cuadro. Algunos navegadores envían la grabación a su fabricante. Si eliges **En esta Machine**, la grabación queda en espera y el cuadro muestra «Preparando la entrada de voz…» junto con el tiempo restante.

## Ajustes

- **Pasado a texto**: **Automático**, **En esta Machine** o **Con OpenAI**.
- **Precisión** (solo en tu Machine): **Más preciso** funciona mejor con la mayoría de los idiomas. **Más rápido** tarda menos, pero comete más errores, y es la opción predeterminada en una Machine Standard.
- **Idioma**: **Detectar** funciona con todos los idiomas de la aplicación. Si eliges el tuyo, será un poco más rápido.

Para hablar en voz alta con The Machine, consulta [Habla en directo](talk-live.md).

## Si no funciona

- **El micrófono está bloqueado**: permite el acceso al micrófono para este sitio en los ajustes del navegador. En la aplicación del teléfono, está en los permisos de la aplicación.
- **No se encontró ningún micrófono**: conecta uno e inténtalo de nuevo.
- **No se puede conectar con tu Machine**: la grabación se conserva y se transcribe cuando tu Machine vuelva a estar disponible. Para intentarlo antes, toca **Probar ahora**.
- **No se entendió nada**: acércate al micrófono o habla un poco más.
