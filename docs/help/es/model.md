---
title: Modelo
area: settings
summary: Qué modelo de IA responde por ti, cuánto razona y qué parte de los límites de tu plan ha consumido.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 9a0777c555ab5637
---
**Ajustes**, **Modelo** muestra qué modelo de IA hace el **Trabajo en segundo plano** y cómo has iniciado sesión, por ejemplo, con ChatGPT.

En una Machine alojada con una sesión iniciada en ChatGPT, el modelo principal es GPT-6.2 Sol: responde más rápido que GPT-6.1 Sol por el mismo precio.

El acceso con Claude caduca unas cuatro semanas después de iniciar sesión. **Te necesita** te avisa con tres días de antelación y, cuando caduca, recibes una notificación. **Volver a iniciar sesión** lo soluciona en un paso.

Los planes personales de ChatGPT o Claude pueden usar tus chats para entrenar por defecto. **Desactivar el entrenamiento con tus datos** abre ese ajuste en el proveedor y **Hecho** oculta el aviso.

## Modelo y razonamiento para los chats

En **Chats**, elige el modelo y el nivel de razonamiento para tus chats de tareas y para Ayuda. Solo verás los modelos y niveles que ofrece tu método de inicio de sesión.

Un nivel de razonamiento más alto responde mejor a preguntas difíciles, pero es más lento y consume más de tu plan. **Razonamiento ultra** recurre a modelos auxiliares para las preguntas más difíciles y es el que más consume. Las nuevas Machine empiezan con **Razonamiento bajo**: ofrece buenos resultados y consume mucho menos de tu plan. Los cambios se aplican a partir del siguiente mensaje.

Para cambiarlo solo en un chat, toca el modelo o el nivel de razonamiento debajo del cuadro de mensaje. Vuelve a elegir la opción de Ajustes para seguir la configuración de Ajustes.

Las comprobaciones, tu perfil y los borradores preparados con antelación conservan su propio modelo.

## Límites

Si tu plan tiene límites de uso, como los límites de 5 horas y semanales de un plan de ChatGPT o Claude, aquí verás cuánto has usado y cuándo se restablece cada uno. Consultarlo no consume tu plan.

## Espacio para tus propios chats

El trabajo en segundo plano deja espacio para tus propios chats. Se pausa cuando se alcanza aproximadamente el 65 % del límite de 5 horas. Las comprobaciones de mensajes nuevos continúan hasta alcanzar aproximadamente el 90 % del límite semanal; el resto del trabajo consume alrededor de una séptima parte del límite semanal al día. Si inicias sesión con una opción sin límites, como una clave de API, nunca se pausa.

El trabajo en segundo plano nunca se ejecuta con GPT-6 Astra. Si inicias sesión con ChatGPT y tienes una versión de OpenClaw anterior a 2026.11.10, usa GPT-6.1 Sol, incluso si tu modelo principal es GPT-6.2 Sol: en esa versión, 6.2 no reutiliza las instrucciones almacenadas en caché, así que consume más de tu plan. A partir de OpenClaw 2026.11.10, el trabajo en segundo plano vuelve a usar tu modelo principal. Tus chats conservan el modelo que elegiste.

Antes de una comprobación, un modelo pequeño (GPT-6 Luna con ChatGPT, Haiku con Claude) aparta boletines, promociones y avisos de apps que claramente no requieren atención, para que las comprobaciones consuman menos de tu plan. Aun así, puedes buscarlos. Los mensajes de personas, las facturas, las alertas de seguridad y los códigos de inicio de sesión siempre se comprueban.

## Antes de alcanzar un límite

Si a tu plan de ChatGPT le quedan reinicios, Tareas muestra una breve línea cuando el trabajo en segundo plano se ralentiza: al alcanzar aproximadamente el 65 % del límite de 5 horas o el 90 % del límite semanal. Indica cuánto has usado y cuántos reinicios quedan. **Usar un reinicio** vuelve a iniciar los límites, después de que lo confirmes. × oculta la línea hasta que se restablezca ese límite. Si no te quedan reinicios, no aparece nada nuevo.

En una Machine alojada, tu Machine detecta y usa los reinicios cuando hayas iniciado sesión en Codex en tu Machine con la misma cuenta de ChatGPT. Hasta entonces, Tareas y Ajustes muestran **Activar reinicios**. Esta opción abre el paso de Codex en la página de configuración, donde inicias sesión con un código, igual que con ChatGPT.

## Al alcanzar un límite

En la parte superior del panel se indica qué límite se ha alcanzado y cuándo se restablece. El trabajo espera y luego continúa donde se quedó. No se pierde nada. Si a tu plan de ChatGPT le quedan reinicios, **Usar un reinicio** vuelve a iniciar los límites. En una Machine alojada sin una sesión iniciada en Codex, **Activar reinicios** abre la página de configuración. En los demás casos, **Ver reinicios en ChatGPT** abre la página de ChatGPT.

## Con un modelo alternativo

Si tu Machine tiene un modelo alternativo asociado a otro plan o proveedor, lo usa cuando se alcanza un límite y el trabajo no se queda en espera. En la parte superior del panel aparece «Se ha alcanzado el límite de ChatGPT. Se está usando el modelo alternativo». Si el modelo alternativo deja de funcionar, se vuelven a aplicar las pausas.

## Cambiar el modelo principal

El modelo principal es el que usa el resto de The Machine. En una Machine alojada, puedes cambiarlo en la página de configuración, en Tu IA. En tu propio ordenador, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
