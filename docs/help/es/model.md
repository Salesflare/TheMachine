---
title: Modelo
area: settings
summary: Qué modelo de IA responde por ti, cuánto razona y qué parte de los límites de tu plan ha consumido.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: ee95ad4fa5323e3a
---
**Ajustes**, **Modelo** muestra qué modelo de IA realiza el **Trabajo en segundo plano** y cómo has iniciado sesión, por ejemplo, con ChatGPT.

En una Machine alojada con una cuenta de ChatGPT, el modelo principal es GPT-6.2 Sol: responde más rápido que GPT-6.1 Sol por el mismo precio.

Es posible que un plan personal de ChatGPT o Claude use tus chats para entrenar modelos de forma predeterminada. **Desactivar el entrenamiento con tus datos** abre ese ajuste en el proveedor y **Hecho** oculta la línea.

## Modelo y razonamiento para los chats

En **Chats**, elige el modelo y el nivel de razonamiento para tus chats de tareas y para Ayuda. Solo verás los modelos y niveles disponibles con tu cuenta.

Con más razonamiento, responde mejor a las preguntas difíciles, pero tarda más y consume más de tu plan. **Razonamiento ultra** incorpora asistentes para las preguntas más difíciles y consume más que ningún otro nivel. Una Machine nueva empieza con **Razonamiento bajo**: ofrece buenos resultados y consume mucho menos de tu plan. Los cambios se aplican a partir del siguiente mensaje.

Para cambiarlo solo en un chat, toca el modelo o el nivel de razonamiento debajo del cuadro de mensaje. Vuelve a elegir **Ajustes** para seguir la configuración de Ajustes.

Las comprobaciones, tu perfil y los borradores preparados de antemano usan su propio modelo.

## Límites

Si tu plan tiene límites de uso, como los límites de 5 horas y semanales de un plan de ChatGPT o Claude, aquí verás cuánto has consumido y cuándo se reinicia cada límite. Consultarlo no consume tu plan.

## Espacio para tus propios chats

El trabajo en segundo plano deja espacio para tus propios chats. Se pausa cuando se alcanza aproximadamente el 65 % del límite de 5 horas. Las comprobaciones de mensajes nuevos continúan hasta aproximadamente el 90 % del límite semanal; el resto del trabajo consume alrededor de una séptima parte del límite semanal al día. Si has iniciado sesión con una cuenta sin límites, como una clave de API, nunca se pausa.

El trabajo en segundo plano nunca se ejecuta con GPT-6 Astra. Por ahora, si has iniciado sesión con ChatGPT, usa GPT-6.1 Sol, incluso cuando el modelo principal sea GPT-6.2 Sol. En esa cuenta, la versión 6.2 aún no reutiliza las instrucciones almacenadas en caché, así que consume más de tu plan. Tus chats siguen usando el modelo que elegiste.

Antes de una comprobación, un modelo pequeño (GPT-6 Luna con ChatGPT y Haiku con Claude) aparta los boletines, las promociones y los avisos de aplicaciones que claramente no requieren ninguna acción, para que las comprobaciones consuman menos de tu plan. Seguirán apareciendo en las búsquedas. Siempre se comprueban los mensajes de personas, las facturas, las alertas de seguridad y los códigos de inicio de sesión.

## Antes de alcanzar un límite

Si a tu plan de ChatGPT le quedan reinicios, Tareas muestra una línea breve cuando el trabajo en segundo plano empieza a ralentizarse: al llegar aproximadamente al 65 % del límite de 5 horas o al 90 % del límite semanal. Indica cuánto has consumido y cuántos reinicios te quedan. **Usar un reinicio** reinicia los límites después de que lo confirmes. × oculta la línea hasta que se reinicie ese límite. Si no te quedan reinicios, no aparece nada nuevo.

En una Machine alojada, tu Machine detecta y usa los reinicios cuando hayas iniciado sesión en Codex en tu Machine con la misma cuenta de ChatGPT. Hasta entonces, Tareas y Ajustes muestran **Activar reinicios**. Se abre el paso de Codex en la página de configuración, donde inicias sesión con un código, igual que con tu cuenta de ChatGPT.

## Al alcanzar un límite

En la parte superior del panel se indica qué límite se ha alcanzado y cuándo se reinicia. El trabajo espera y luego continúa donde se quedó. No se pierde nada. Si a tu plan de ChatGPT le quedan reinicios, **Usar un reinicio** reinicia los límites. En una Machine alojada sin sesión iniciada en Codex, **Activar reinicios** abre tu página de configuración. En los demás casos, **Ver reinicios en ChatGPT** abre la página de ChatGPT.

## Con un modelo alternativo

Si tu Machine tiene un modelo alternativo de otro plan o proveedor, lo usa cuando se alcanza un límite y el trabajo no se detiene. En la parte superior del panel aparece «Se ha alcanzado el límite de ChatGPT. Se está usando el modelo alternativo». Si el modelo alternativo deja de funcionar, vuelven las pausas.

## Cambiar el modelo principal

El modelo principal es el que usa el resto de The Machine. En una Machine alojada, cámbialo en tu página de configuración, en Tu IA. Si usas tu propio ordenador, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
