---
title: Modelo
area: settings
summary: Qué modelo de IA te responde, cuánto razona y qué parte de los límites de tu plan ha usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: eee77413a4bdbf0b
---
**Ajustes**, **Modelo** muestra qué modelo de IA realiza tu **Trabajo en segundo plano** y cómo has iniciado sesión, por ejemplo, con ChatGPT.

## Modelo y razonamiento en los chats

En **Chats**, elige el modelo y el nivel de razonamiento para tus chats de tareas y Ayuda. Solo verás los modelos y niveles disponibles con tu método de inicio de sesión.

Un mayor razonamiento permite responder mejor a las preguntas difíciles, pero es más lento y consume más de tu plan. **Razonamiento ultra** recurre a asistentes para las preguntas más difíciles y es la opción que más consume. Una Machine nueva empieza con **Razonamiento bajo**: buenos resultados con un consumo mucho menor de tu plan. El cambio se aplica a partir del siguiente mensaje.

Para cambiarlo solo en un chat, toca el modelo o el nivel de razonamiento que aparece debajo del cuadro de mensaje. Vuelve a elegir **Ajustes** para que el chat siga los ajustes generales.

Las comprobaciones, tu perfil y los borradores preparados con antelación mantienen su propio modelo.

## Límites

Si tu plan tiene límites de uso, como los límites de 5 horas y semanales de un plan de ChatGPT o Claude, verás cuánto has usado y cuándo se reinicia cada límite. Consultar esta información no consume tu plan.

## Espacio para tus propios chats

El trabajo en segundo plano deja espacio para tus propios chats. Se pausa cuando se alcanza aproximadamente el 65 % del límite de 5 horas. Las comprobaciones de mensajes nuevos continúan hasta que se alcanza aproximadamente el 90 % del límite semanal. El resto del trabajo consume alrededor de una séptima parte del límite semanal al día. El inicio de sesión no se pausa si no tiene límites, como cuando usas una clave de API.

El trabajo en segundo plano nunca se ejecuta en GPT-6 Astra. En su lugar, usa GPT-6.1 Sol.

## Cuando se alcanza un límite

En la parte superior del panel se indica qué límite se ha alcanzado y cuándo se reinicia. El trabajo queda en espera y luego se reanuda donde se quedó. No se pierde nada. Si tu plan de ChatGPT permite reinicios, **Usar un reinicio** vuelve a empezar los límites. Si no, **Ver reinicios en ChatGPT** abre la página de ChatGPT.

## Con un modelo alternativo

Si tu Machine tiene un modelo alternativo de otro plan o proveedor, este toma el relevo cuando se alcanza un límite y no hay que esperar. En la parte superior del panel aparece «Se alcanzó el límite de ChatGPT. Se está usando el modelo alternativo». Si el modelo alternativo deja de funcionar, se vuelven a aplicar las pausas.

## Cambiar el modelo principal

El modelo principal es el que usa el resto de The Machine. Si tienes una Machine alojada, cámbialo en la página de configuración, en Tu IA. Si usas tu propio ordenador, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
