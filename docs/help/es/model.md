---
title: Modelo
area: settings
summary: Qué modelo de IA responde por ti, cuánto razona y cuánto ha consumido de los límites de tu plan.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 744a27a77ab747ac
---
**Ajustes**, **Modelo** muestra qué modelo de IA realiza el **Trabajo en segundo plano** y cómo has iniciado sesión, por ejemplo, con ChatGPT.

Es posible que un plan personal de ChatGPT o Claude use tus chats para entrenar por defecto. **Desactivar el entrenamiento con tus datos** abre ese ajuste en el proveedor y **Hecho** oculta la línea.

## Modelo y razonamiento para los chats

En **Chats**, elige el modelo y el nivel de razonamiento para tus chats de tareas y Ayuda. Solo verás los modelos y niveles que ofrece el método con el que has iniciado sesión.

Un nivel de razonamiento más alto ayuda a responder mejor las preguntas difíciles, pero es más lento y consume más de tu plan. **Razonamiento ultra** recurre a asistentes para las preguntas más difíciles y es el que más consume. Una Machine nueva empieza con **Razonamiento bajo**: buenos resultados con mucho menos consumo de tu plan. El cambio se aplica a partir del siguiente mensaje.

Para cambiarlo solo en un chat, toca el modelo o el nivel de razonamiento debajo del cuadro de mensaje. Vuelve a elegir **Ajustes** para seguir la configuración de Ajustes.

Las comprobaciones, tu perfil y los borradores preparados de antemano usan su propio modelo.

## Límites

Si tu plan tiene límites de uso, como los límites de 5 horas y semanales de un plan de ChatGPT o Claude, aquí verás cuánto has usado y cuándo se restablece cada límite. Consultar esto nunca consume tu plan.

## Espacio para tus propios chats

El Trabajo en segundo plano deja espacio para tus propios chats. Se pausa cuando se ha usado alrededor del 65 % del límite de 5 horas. Las comprobaciones de mensajes nuevos continúan hasta que se ha usado alrededor del 90 % del límite semanal. El resto del trabajo consume aproximadamente una séptima parte del límite semanal al día. Si inicias sesión sin límites, por ejemplo, con una clave de API, nunca se pausa.

El Trabajo en segundo plano nunca se ejecuta con GPT-6 Astra. En su lugar, usa GPT-6.1 Sol.

## Cuando se alcanza un límite

En la parte superior del panel se indica qué límite se ha alcanzado y cuándo se restablece. El trabajo espera y luego continúa donde se quedó. No se pierde nada. Si tu plan de ChatGPT permite reinicios, **Usar un reinicio** vuelve a iniciar los límites. Si no, **Ver reinicios en ChatGPT** abre la página de ChatGPT.

## Con un modelo alternativo

Si tu Machine tiene un modelo alternativo en otro plan o proveedor, este toma el relevo cuando se alcanza un límite y el trabajo no tiene que esperar. En la parte superior del panel aparece «Se alcanzó el límite de ChatGPT; se está usando el modelo alternativo». Si el modelo alternativo deja de funcionar, vuelven las pausas.

## Cambiar el modelo principal

El modelo principal es el que usa el resto de The Machine. En una Machine alojada, cámbialo en la página de configuración, en Tu IA. Si está en tu propio ordenador, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
