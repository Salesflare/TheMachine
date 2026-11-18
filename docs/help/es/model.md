---
title: Modelo
area: settings
summary: Qué modelo de IA te responde, cuánto razona y cuánto has consumido de los límites de tu plan.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 249d2d7d6c368cfe
---
En **Ajustes**, **Modelo** muestra qué modelo de IA se encarga del **Trabajo en segundo plano** y cómo has iniciado sesión, por ejemplo, con ChatGPT.

En una Machine alojada con una sesión iniciada en ChatGPT, el modelo principal es GPT-6.2 Sol: responde más rápido que GPT-6.1 Sol al mismo precio.

Es posible que un plan personal de ChatGPT o Claude use tus chats para entrenar por defecto. **Desactivar el entrenamiento con tus datos** abre ese ajuste en el proveedor y **Hecho** oculta la opción.

## Modelo y razonamiento para los chats

En **Chats**, elige el modelo y el nivel de razonamiento para tus chats de tareas y Ayuda. Solo verás los modelos y niveles que ofrece tu método de inicio de sesión.

Un mayor nivel de razonamiento ayuda a responder mejor las preguntas difíciles, pero es más lento y consume más de tu plan. **Razonamiento ultra** recurre a asistentes para las preguntas más difíciles y es el que más consume. Una Machine nueva empieza con **Razonamiento bajo**: buenos resultados con mucho menos consumo de tu plan. Los cambios se aplican a partir del siguiente mensaje.

Para cambiarlo solo en un chat, toca el modelo o el nivel de razonamiento debajo del cuadro de mensaje. Vuelve a elegir la opción **Ajustes** para seguir la configuración de Ajustes.

Las comprobaciones, tu perfil y los borradores preparados con antelación usan su propio modelo.

## Límites

Si tu plan tiene límites de uso, como los límites de 5 horas y semanales de un plan de ChatGPT o Claude, verás cuánto has consumido y cuándo se restablece cada límite. Consultar esta información no consume tu plan.

## Espacio para tus propios chats

El trabajo en segundo plano deja espacio para tus propios chats. Se pausa cuando se alcanza aproximadamente el 65 % del límite de 5 horas. Las comprobaciones de mensajes nuevos continúan hasta alcanzar aproximadamente el 90 % del límite semanal. El resto del trabajo consume alrededor de una séptima parte del límite semanal al día. Los métodos de inicio de sesión sin límites, como una clave de API, nunca se pausan.

El trabajo en segundo plano nunca se ejecuta con GPT-6 Astra. En su lugar, usa GPT-6.2 Sol o, si la versión 6.2 no está configurada, GPT-6.1 Sol.

## Cuando se alcanza un límite

En la parte superior del panel se indica qué límite se ha alcanzado y cuándo se restablece. El trabajo espera y luego continúa donde se había quedado. No se pierde nada. Si tu plan de ChatGPT permite reinicios, **Usar un reinicio** vuelve a empezar los límites. Si no, **Ver reinicios en ChatGPT** abre la página de ChatGPT.

## Con un modelo alternativo

Si tu Machine tiene un modelo alternativo de otro plan o proveedor, este toma el relevo cuando se alcanza un límite y el trabajo no se detiene. En la parte superior del panel se muestra «Se alcanzó el límite de ChatGPT. Se está usando el modelo alternativo». Si el modelo alternativo deja de funcionar, se reanudan las pausas.

## Cambiar el modelo principal

El modelo principal es el que usa el resto de The Machine. En una Machine alojada, cámbialo en la página de configuración, en Tu IA. Si usas tu propio equipo, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
