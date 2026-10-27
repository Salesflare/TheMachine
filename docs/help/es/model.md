---
title: Modelo
area: settings
summary: Qué modelo de IA responde por ti, cuánto razona y cuánto ha usado de los límites de tu plan.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
---
En **Ajustes**, **Modelo** muestra el modelo que usa el trabajo en segundo plano (marcado como **Trabajo en segundo plano**) y cómo has iniciado sesión, por ejemplo con ChatGPT.

## Modelo y razonamiento para los chats

En **Chats**, elige el modelo y el nivel de razonamiento que usan los chats de tus tareas y la Ayuda. La lista solo tiene los modelos que ofrece tu inicio de sesión, como los de ChatGPT si iniciaste sesión con ChatGPT, y cada modelo solo los niveles que tiene.

Más razonamiento responde mejor a las preguntas difíciles, pero es más lento y usa más de tu plan. **Razonamiento ultra** suma ayudantes para las preguntas más difíciles: es el más lento y el que más usa. Un cambio se aplica desde el siguiente mensaje.

Un chat puede usar otra cosa: debajo de su cuadro de mensaje, toca el modelo o el nivel de razonamiento. Esa elección es solo para ese chat. Vuelve a elegir lo mismo que en Ajustes para seguir los Ajustes.

Las revisiones, tu perfil y los borradores preparados de antemano mantienen su propio modelo.

## Límites

Si tu plan tiene límites de uso, muestra cuánto se ha usado de cada uno y cuándo se reinicia, por ejemplo el límite de 5 horas y el semanal de un plan de ChatGPT o Claude. Consultar esto nunca gasta tu plan.

## Margen para tus propios chats

El trabajo en segundo plano (revisiones, tu perfil, borradores preparados de antemano) deja margen para tus propios chats. Se pausa hacia el 65% del límite de 5 horas y reparte el límite semanal a razón de más o menos un séptimo al día. Un inicio de sesión sin límites de uso, como una clave de API, nunca se pausa.

El trabajo en segundo plano nunca se ejecuta con GPT-6 Astra. Usa GPT-6.1 Sol en su lugar.

## Cuando se alcanza un límite

La parte superior del panel dice qué límite se alcanzó y cuándo se reinicia. El trabajo espera y luego sigue donde lo dejó. No se pierde nada. Algunos planes de ChatGPT incluyen reinicios: **Usar un reinicio** pone los límites a cero, tras una confirmación. Si no, **Ver reinicios en ChatGPT** abre la propia página de ChatGPT.

## Cambia el modelo principal

El modelo principal es el que usa el resto de The Machine. En una Machine alojada, elige otro en tu página de configuración, en Tu modelo. En tu propio ordenador, cámbialo en OpenClaw. Consulta [ChatGPT](chatgpt.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
