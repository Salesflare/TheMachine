---
title: Modelo
area: settings
summary: Qué modelo de IA responde por ti, cuánto razona y cuánto ha consumido de los límites de tu plan.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: b76f4f927bfd7be1
---
**Ajustes**, **Modelo** muestra qué modelo de IA realiza tu **Trabajo en segundo plano** y cómo has iniciado sesión, por ejemplo, con ChatGPT.

En una Machine alojada con una sesión iniciada en ChatGPT, el modelo principal es GPT-6.2 Sol: responde más rápido que GPT-6.1 Sol al mismo precio.

En una Machine alojada, la sesión de Claude dura aproximadamente un año. Con `claude auth login`, termina unas cuatro semanas después de que inicies sesión. Tres días antes, **Te necesita** te avisa y recibes un correo. Cuando termina, recibes una notificación y, si aún no te había llegado, ese correo. **Volver a iniciar sesión** lo soluciona en un paso.

Es posible que, de forma predeterminada, un plan personal de ChatGPT o Claude use tus chats para entrenar modelos: **Desactivar el entrenamiento con tus datos** abre ese ajuste en el proveedor y **Hecho** oculta el aviso.

## Modelo y razonamiento para los chats

En **Chats**, elige el modelo y el nivel de razonamiento para tus chats de tareas y Ayuda. Solo verás los modelos y niveles que ofrece tu inicio de sesión.

Un mayor nivel de razonamiento permite responder mejor a preguntas difíciles, pero es más lento y consume más de tu plan. **Razonamiento ultra** recurre a asistentes para las preguntas más difíciles y es el nivel que más consume. Las nuevas Machines empiezan con **Razonamiento bajo**: ofrece buenos resultados y consume mucho menos de tu plan. Los cambios se aplican a partir del siguiente mensaje.

Para cambiarlo solo en un chat, pulsa el modelo o el nivel de razonamiento debajo del cuadro de mensaje. Vuelve a elegir la opción de Ajustes para que se apliquen los ajustes generales.

Las comprobaciones, tu perfil y los borradores preparados de antemano usan su propio modelo.

## Límites

Si tu plan tiene límites de uso, como los límites de 5 horas y semanales de un plan de ChatGPT o Claude, se muestra cuánto has usado y cuándo se reinicia cada límite. Consultar esta información no consume tu plan.

## Espacio para tus propios chats

El trabajo en segundo plano deja espacio para tus propios chats. Se pausa cuando se alcanza aproximadamente el 65 % del límite de 5 horas. Las comprobaciones de mensajes nuevos continúan hasta que se alcanza aproximadamente el 90 % del límite semanal; el resto del trabajo ocupa aproximadamente una séptima parte de la semana al día. Los inicios de sesión sin límites, como una clave de API, nunca se pausan.

El trabajo en segundo plano nunca se ejecuta con GPT-6 Astra. Si has iniciado sesión en ChatGPT y tienes una versión de OpenClaw anterior a 2026.11.10, usa GPT-6.1 Sol, incluso si tu modelo principal es GPT-6.2 Sol: en ese caso, 6.2 no reutiliza las instrucciones guardadas en la caché y consume más de tu plan. A partir de OpenClaw 2026.11.10, el trabajo en segundo plano vuelve a usar tu modelo principal. Tus chats conservan el modelo que elegiste.

Antes de una comprobación, un modelo pequeño (GPT-6 Luna con ChatGPT, Haiku con Claude) aparta boletines, promociones y avisos de aplicaciones que claramente no requieren ninguna acción, para que las comprobaciones consuman menos de tu plan. Seguirán apareciendo en las búsquedas. Los mensajes escritos por personas, las facturas, las alertas de seguridad y los códigos de inicio de sesión siempre se comprueban.

## Antes de alcanzar un límite

Si a tu plan de ChatGPT le quedan reinicios, Tareas muestra un breve aviso cuando el trabajo en segundo plano se ralentiza: al llegar aproximadamente al 65 % del límite de 5 horas o al 90 % del límite semanal. Indica cuánto has usado y cuántos reinicios te quedan. **Usar un reinicio** reinicia los límites cuando lo confirmes. × oculta el aviso hasta que se reinicie ese límite. Si no te quedan reinicios, no aparecerá ningún aviso nuevo.

En una Machine alojada, tu Machine ve y usa los reinicios cuando hayas iniciado sesión en Codex en tu Machine con la misma cuenta de ChatGPT. Hasta entonces, Tareas y Ajustes muestran **Activar reinicios**. Se abre el paso de Codex en la página de configuración, donde inicias sesión con un código, igual que con ChatGPT.

## Cuando se alcanza un límite

En la parte superior del panel se indica qué límite se ha alcanzado y cuándo se reinicia. El trabajo espera y luego continúa donde se quedó. No se pierde nada. Si a tu plan de ChatGPT le quedan reinicios, **Usar un reinicio** reinicia los límites. Si tienes una Machine alojada y no has iniciado sesión en Codex, **Activar reinicios** abre la página de configuración. En caso contrario, **Ver reinicios en ChatGPT** abre la página de ChatGPT.

## Con un modelo alternativo

Si tu Machine tiene un modelo alternativo en otro plan o proveedor, lo usa al alcanzar un límite y el trabajo no se detiene. En la parte superior del panel aparece «Se ha alcanzado el límite de ChatGPT. Se está usando el modelo alternativo». Si el modelo alternativo deja de funcionar, vuelven las pausas.

## Cambiar el modelo principal

El modelo principal es el que usa el resto de The Machine. En una Machine alojada, cámbialo en la página de configuración, en Tu IA. En tu ordenador, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
