---
title: Modelo
area: settings
summary: Qué modelo de IA te responde, cuánto razona y qué parte de los límites de tu plan ha usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: c7a96914e4deb3d4
---
**Ajustes**, **Modelo** muestra qué modelo de IA hace el **Trabajo en segundo plano** y cómo has iniciado sesión, por ejemplo, con ChatGPT.

Los planes personales de ChatGPT o Claude pueden usar tus chats para entrenar sus modelos de forma predeterminada. **Desactivar el entrenamiento con tus datos** abre ese ajuste en el proveedor y **Hecho** oculta la línea.

## Modelo y razonamiento en los chats

En **Chats**, elige el modelo y el nivel de razonamiento para tus chats de tareas y Ayuda. Solo verás los modelos y niveles disponibles con tu inicio de sesión.

Con más razonamiento, las respuestas a preguntas difíciles son mejores, pero tardan más y consumen más de tu plan. **Razonamiento ultra** incorpora asistentes para las preguntas más difíciles y es el que más consume. Una Machine nueva empieza con **Razonamiento bajo**: buenos resultados por mucho menos de tu plan. Los cambios se aplican a partir del siguiente mensaje.

Para cambiarlo solo en un chat, toca el modelo o el nivel de razonamiento debajo del cuadro de mensaje. Vuelve a elegir la opción de **Ajustes** para seguir la configuración de Ajustes.

Las comprobaciones, tu perfil y los borradores preparados con antelación usan su propio modelo.

## Límites

Si tu plan tiene límites de uso, como los límites de 5 horas y semanales de un plan de ChatGPT o Claude, aquí verás cuánto has usado y cuándo se restablece cada límite. Consultarlo no consume tu plan.

## Espacio para tus propios chats

El trabajo en segundo plano deja espacio para tus propios chats. Se pausa cuando se alcanza aproximadamente el 65 % del límite de 5 horas. Las comprobaciones de mensajes nuevos continúan hasta alcanzar aproximadamente el 90 % del límite semanal. El resto del trabajo consume cada día alrededor de una séptima parte del límite semanal. Los inicios de sesión sin límites, como con una clave de API, nunca se pausan.

El trabajo en segundo plano nunca se ejecuta en GPT-6 Astra. En su lugar, usa GPT-6.2 Sol o GPT-6.1 Sol si 6.2 no está configurado.

## Cuando se alcanza un límite

En la parte superior del panel se indica qué límite se ha alcanzado y cuándo se restablece. El trabajo queda en espera y luego continúa donde se quedó. No se pierde nada. Si tu plan de ChatGPT permite reiniciar los límites, **Usar un reinicio** los restablece. Si no, **Ver reinicios en ChatGPT** abre la página de ChatGPT.

## Con un modelo de respaldo

Si tu Machine tiene un modelo de respaldo de otro plan o proveedor, este se activa al alcanzar un límite y el trabajo no queda en espera. En la parte superior del panel aparece «Se alcanzó el límite de ChatGPT, se está usando el modelo de respaldo». Si el modelo de respaldo deja de funcionar, vuelven las pausas.

## Cambiar el modelo principal

El modelo principal es el que usa el resto de The Machine. Si tienes una Machine alojada, cámbialo en la página de configuración, en «Tu IA». Si usas tu propio ordenador, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) y la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
