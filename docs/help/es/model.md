---
title: Modelo
area: settings
summary: Qué modelo de IA te responde, cuánto razonamiento aplica y qué parte de los límites de tu plan ha usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: a6db52984a6fddeb
---
**Ajustes**, **Modelo** muestra qué modelo de IA realiza el **Trabajo en segundo plano** y cómo has iniciado sesión, por ejemplo, con ChatGPT.

En una Machine alojada con una sesión iniciada en ChatGPT, el modelo principal es GPT-6.2 Sol: responde más rápido que GPT-6.1 Sol por el mismo precio.

Es posible que los planes personales de ChatGPT o Claude usen tus chats para entrenar por defecto. **Desactivar el entrenamiento con tus datos** abre ese ajuste en el proveedor y **Hecho** oculta la opción.

## Modelo y razonamiento en los chats

En **Chats**, elige el modelo y el nivel de razonamiento para tus chats de tareas y para Ayuda. Solo verás los modelos y niveles que ofrece tu método de inicio de sesión.

Un nivel de razonamiento más alto permite responder mejor a preguntas difíciles, pero tarda más y consume más de tu plan. **Razonamiento ultra** recurre a asistentes para las preguntas más difíciles y consume más que cualquier otro nivel. Una Machine nueva empieza con **Razonamiento bajo**: ofrece buenos resultados y consume mucho menos de tu plan. Los cambios se aplican a partir del siguiente mensaje.

Para cambiarlo solo en un chat, toca el modelo o el nivel de razonamiento debajo del cuadro de mensaje. Vuelve a elegir **Ajustes** para usar la opción de Ajustes.

Las comprobaciones, tu perfil y los borradores preparados de antemano mantienen su propio modelo.

## Límites

Si tu plan tiene límites de uso, como los límites de 5 horas y semanales de un plan de ChatGPT o Claude, aquí verás cuánto has usado y cuándo se reinicia cada límite. Consultar esta información no consume tu plan.

## Espacio para tus propios chats

El trabajo en segundo plano deja espacio para tus propios chats. Se pausa cuando se ha usado aproximadamente el 65 % del límite de 5 horas. Las comprobaciones de mensajes nuevos continúan hasta que se ha usado aproximadamente el 90 % del límite semanal. El resto del trabajo consume alrededor de una séptima parte del límite semanal al día. Si inicias sesión con un método sin límites, como una clave de API, el trabajo nunca se pausa.

El trabajo en segundo plano nunca se ejecuta con GPT-6 Astra. Por ahora, si inicias sesión con ChatGPT, usa GPT-6.1 Sol, incluso cuando el modelo principal sea GPT-6.2 Sol. En ese método de inicio de sesión, GPT-6.2 todavía no reutiliza sus instrucciones guardadas en caché, así que consume más de tu plan. Tus chats mantienen el modelo que hayas elegido.

## Cuando se alcanza un límite

En la parte superior del panel se indica qué límite se ha alcanzado y cuándo se reinicia. El trabajo queda en espera y luego continúa donde se había quedado. No se pierde nada. Si tu plan de ChatGPT incluye reinicios, **Usar un reinicio** vuelve a empezar los límites. Si no, **Ver reinicios en ChatGPT** abre la página de ChatGPT.

## Con un modelo alternativo

Si tu Machine tiene un modelo alternativo de otro plan o proveedor, este se activa cuando se alcanza un límite y no hay que esperar. En la parte superior del panel se indica «Se alcanzó el límite de ChatGPT; se está usando el modelo alternativo». Si el modelo alternativo deja de funcionar, vuelven las pausas.

## Cambiar el modelo principal

El modelo principal es el que usa el resto de The Machine. En una Machine alojada, cámbialo en la página de configuración, en Tu IA. En tu propio ordenador, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
