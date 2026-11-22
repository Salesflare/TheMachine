---
title: Modelo
area: settings
summary: Qué modelo de IA te responde, cuánto razona y qué parte de los límites de tu plan ha usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: d63ec55d8d0339e6
---
**Ajustes**, **Modelo** muestra qué modelo de IA se encarga del **Trabajo en segundo plano** y cómo has iniciado sesión, por ejemplo, con ChatGPT.

En una Machine alojada con una sesión iniciada en ChatGPT, el modelo principal es GPT-6.2 Sol: responde más rápido que GPT-6.1 Sol por el mismo precio.

De forma predeterminada, los planes personales de ChatGPT o Claude pueden usar tus chats para entrenar sus modelos. **Desactivar el entrenamiento con tus datos** abre ese ajuste en el proveedor y **Hecho** oculta la línea.

## Modelo y razonamiento en los chats

En **Chats**, elige el modelo y el nivel de razonamiento para tus chats de tareas y Ayuda. Solo verás los modelos y niveles disponibles con tu inicio de sesión.

Un mayor razonamiento permite responder mejor a preguntas difíciles, pero es más lento y consume más de tu plan. **Razonamiento ultra** recurre a asistentes para las preguntas más difíciles y consume más que ningún otro nivel. Las nuevas Machine empiezan con **Razonamiento bajo**: ofrece buenos resultados y consume mucho menos de tu plan. Los cambios se aplican a partir del siguiente mensaje.

Para cambiarlo solo en un chat, toca el modelo o el nivel de razonamiento debajo del cuadro de mensaje. Vuelve a elegir la opción de Ajustes para usar la configuración de Ajustes.

Las comprobaciones, tu perfil y los borradores preparados de antemano usan su propio modelo.

## Límites

Si tu plan tiene límites de uso, como los límites de 5 horas y semanales de un plan de ChatGPT o Claude, verás cuánto has usado y cuándo se reinicia cada límite. Consultarlo no consume tu plan.

## Espacio para tus propios chats

El trabajo en segundo plano deja espacio para tus propios chats. Se pausa cuando se alcanza aproximadamente el 65 % del límite de 5 horas. Las comprobaciones de mensajes nuevos continúan hasta aproximadamente el 90 % del límite semanal. El resto del trabajo consume cada día aproximadamente una séptima parte del límite semanal. Los inicios de sesión sin límites, como con una clave de API, nunca se pausan.

El trabajo en segundo plano nunca se ejecuta con GPT-6 Astra. Por ahora, si has iniciado sesión con ChatGPT, usa GPT-6.1 Sol, aunque el modelo principal sea GPT-6.2 Sol: con ese inicio de sesión, la versión 6.2 aún no reutiliza las instrucciones almacenadas en caché, así que consume más de tu plan. Tus chats siguen usando el modelo que elegiste.

## Antes de alcanzar un límite

Si a tu plan de ChatGPT le quedan reinicios, Tareas muestra una línea breve cuando el trabajo en segundo plano empieza a ralentizarse: al alcanzar aproximadamente el 65 % del límite de 5 horas o el 90 % del límite semanal. Indica cuánto se ha usado y cuántos reinicios quedan. **Usar un reinicio** vuelve a iniciar los límites, después de que lo confirmes. × oculta la línea hasta que se reinicie ese límite. Si no quedan reinicios, no aparecerá nada nuevo.

## Al alcanzar un límite

En la parte superior del panel se indica qué límite se ha alcanzado y cuándo se reinicia. El trabajo espera y luego continúa donde se quedó. No se pierde nada. Si a tu plan de ChatGPT le quedan reinicios, **Usar un reinicio** vuelve a iniciar los límites. Si no, **Ver reinicios en ChatGPT** abre la página de ChatGPT.

## Con un modelo alternativo

Si tu Machine tiene un modelo alternativo de otro plan o proveedor, este toma el relevo al alcanzar un límite y no hay que esperar. En la parte superior del panel se indica: «Se ha alcanzado el límite de ChatGPT. Se está usando tu modelo alternativo». Si el modelo alternativo deja de funcionar, vuelven las pausas.

## Cambiar el modelo principal

El modelo principal es el que usa el resto de The Machine. En una Machine alojada, cámbialo en la página de configuración, en Tu IA. Si usas tu propio ordenador, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
