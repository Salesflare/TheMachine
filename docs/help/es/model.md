---
title: Modelo
area: settings
summary: Qué modelo de IA responde, cuánto razona y qué parte de los límites de tu plan ha consumido.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: f34db396a7290252
---
**Ajustes**, **Modelo** muestra qué modelo de IA realiza tu **Trabajo en segundo plano** y cómo has iniciado sesión, por ejemplo, con ChatGPT.

En una Machine alojada con una cuenta de ChatGPT, el modelo principal es GPT-6.2 Sol: responde más rápido que GPT-6.1 Sol al mismo precio.

Es posible que un plan personal de ChatGPT o Claude use tus chats para entrenar modelos de forma predeterminada. **Desactivar el entrenamiento con tus datos** abre ese ajuste en el proveedor, y **Hecho** oculta la línea.

## Modelo y razonamiento para los chats

En **Chats**, elige el modelo y el nivel de razonamiento para tus chats de tareas y para Ayuda. Solo verás los modelos y niveles que ofrece tu cuenta.

Un mayor nivel de razonamiento permite responder mejor a preguntas difíciles, pero tarda más y consume más de tu plan. **Razonamiento ultra** recurre a modelos auxiliares para las preguntas más difíciles y es el que más consume. Una Machine nueva empieza con **Razonamiento bajo**: ofrece buenos resultados y consume mucho menos de tu plan. El cambio se aplica a partir del siguiente mensaje.

Para cambiarlo solo en un chat, toca el modelo o el nivel de razonamiento debajo del cuadro de mensaje. Vuelve a elegir la opción de Ajustes para usar los ajustes generales.

Las comprobaciones, tu perfil y los borradores preparados con antelación mantienen su propio modelo.

## Límites

Si tu plan tiene límites de uso, como los límites de 5 horas y semanales de un plan de ChatGPT o Claude, verás cuánto has consumido y cuándo se reinicia cada límite. Consultar esta información no consume tu plan.

## Espacio para tus chats

El trabajo en segundo plano deja espacio para tus chats. Se pausa cuando se consume alrededor del 65 % del límite de 5 horas. Las comprobaciones de mensajes nuevos continúan hasta que se consume alrededor del 90 % del límite semanal. El resto del trabajo consume aproximadamente una séptima parte del límite semanal al día. Una cuenta sin límites, como una clave de API, nunca se pausa.

El trabajo en segundo plano nunca se ejecuta con GPT-6 Astra. Si has iniciado sesión con ChatGPT y usas una versión de OpenClaw anterior a 2026.11.10, se usa GPT-6.1 Sol, incluso si tu modelo principal es GPT-6.2 Sol. En ese caso, GPT-6.2 no reutiliza las instrucciones guardadas en caché, así que consume más de tu plan. A partir de OpenClaw 2026.11.10, el trabajo en segundo plano vuelve a usar tu modelo principal. Tus chats siguen usando el modelo que elegiste.

Antes de una comprobación, un modelo pequeño (GPT-6 Luna con ChatGPT, Haiku con Claude) aparta los boletines, las promociones y los avisos de aplicaciones que claramente no requieren ninguna acción, para que las comprobaciones consuman menos de tu plan. Seguirán apareciendo en las búsquedas. Siempre se comprueban los mensajes de una persona, una factura, una alerta de seguridad o un código de inicio de sesión.

## Antes de alcanzar un límite

Si a tu plan de ChatGPT le quedan reinicios, Tareas muestra una línea breve cuando el trabajo en segundo plano empieza a ralentizarse: al llegar a alrededor del 65 % del límite de 5 horas o al 90 % del límite semanal. Indica cuánto has consumido y cuántos reinicios quedan. **Usar un reinicio** reinicia los límites cuando lo confirmes. × oculta la línea hasta que se reinicie ese límite. Si no te quedan reinicios, no aparece nada nuevo.

En una Machine alojada, tu Machine detecta y usa los reinicios cuando Codex haya iniciado sesión en la misma cuenta de ChatGPT. Hasta entonces, Tareas y Ajustes muestran **Activar reinicios**. Esta opción abre el paso de Codex en tu página de configuración, donde inicias sesión con un código, igual que al iniciar sesión en ChatGPT.

## Al alcanzar un límite

En la parte superior del panel se indica qué límite se ha alcanzado y cuándo se reinicia. El trabajo espera y después continúa donde se quedó. No se pierde nada. Si tu plan de ChatGPT tiene reinicios, **Usar un reinicio** reinicia los límites. En una Machine alojada sin una sesión iniciada en Codex, **Activar reinicios** abre tu página de configuración. En los demás casos, **Ver reinicios en ChatGPT** abre la página de ChatGPT.

## Con un modelo alternativo

Si tu Machine tiene un modelo alternativo en otro plan o proveedor, este se encarga del trabajo cuando se alcanza un límite, así que nada queda en espera. En la parte superior del panel se indica: «Se ha alcanzado el límite de ChatGPT; se está usando el modelo alternativo». Si el modelo alternativo deja de funcionar, vuelven las pausas.

## Cambiar el modelo principal

El modelo principal es el que usa el resto de The Machine. En una Machine alojada, cámbialo en tu página de configuración, en Tu IA. En tu ordenador, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
