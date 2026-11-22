---
title: No hay tareas nuevas
area: troubleshooting
summary: Las revisiones están desactivadas, en espera o detenidas por el límite de uso de tu modelo. Descubre cómo saber qué ocurre y qué hacer.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: 07aca53acc41694d
---
Las tareas se crean a partir de las revisiones: tu Machine comprueba lo que ha llegado en los últimos 15 minutos, aproximadamente.

## Te acabas de registrar

En una Machine alojada nueva, las revisiones empiezan automáticamente cuando conectas la IA y el correo. Mientras tu Machine lee el correo, Tareas muestra «Leyendo tu correo. Tus primeras tareas llegarán en unos minutos». Cuando sabe cuánto correo hay, indica cuánto tardará, aproximadamente: «Tus primeras tareas llegarán en unos 10 min». Si falta algún paso, **Te necesita** indica cuál, como **Conectar correo**, con un enlace a ese paso.

Mientras lee, Tareas muestra cuánto ha avanzado («Ha leído 20 de 132 mensajes. Leyendo los siguientes 40…»), algunas de las personas y organizaciones que ha encontrado y tu primera tarea en cuanto esté lista. El número cuenta los mensajes que ha terminado de leer. La barra sigue avanzando mientras lee los siguientes. Los nombres proceden de tu correo y solo tú puedes verlos.

Si la primera revisión no encuentra nada para ti, indica qué ha leído y te propone los siguientes pasos, como conectar un servicio del que recibes correos a menudo o preguntar qué ha cambiado esta semana.

## Las revisiones están desactivadas

En la parte superior de Tareas aparece «Las revisiones están desactivadas, así que todavía no llegan tareas». En una Machine alojada, pulsa **Activar las revisiones**. En tu propio ordenador, ejecuta `./install.sh --activate`.

## El límite de tu modelo

Para dejar margen para tus propios chats, las revisiones se pausan cuando alcanzan aproximadamente el 65 % del límite de 5 horas de tu plan de IA y el 90 % del límite semanal. Si tienes un modelo de respaldo en otro plan, las revisiones no esperan. Consulta [Modelo](model.md).

Mientras las revisiones están en espera, la parte superior del panel indica hasta cuándo, por ejemplo: «Las revisiones esperan hasta las 07:15 para reservar tu límite semanal de ChatGPT». **Revisar ahora** inicia una revisión igualmente. En **Ajustes**, **Modelo** puedes consultar tus límites.

No se pierde nada: se revisa lo que ha llegado en cuanto es posible.

## Por la noche

De las 00:00 a las 06:30, las revisiones se pausan y los mensajes nuevos quedan en espera. Se revisan todos juntos a las 06:30, antes del resumen de la mañana. **Revisiones** muestra «En pausa por la noche. Se pondrá al día a las 06:30». Si usas la app, escribes en el chat o tocas una tarea, las revisiones vuelven a ejecutarse hasta que lleves una hora sin actividad. **Revisar ahora** inicia una revisión de inmediato.

## Una ejecución ha fallado

En **Conexiones**, **Revisiones**, **Ejecuciones recientes** muestra cada ejecución. Si una falla, se vuelve a intentar automáticamente.

Si una ejecución se detiene al alcanzar el límite de uso de tu plan de IA, muestra **Se ha alcanzado el límite de uso de la IA.** e indica cuándo se restablece. Es una pausa, no un error: los mensajes quedan en espera y se revisan después del restablecimiento. No se envía nada a [informes de errores](error-reports.md).

## Apartados

Cuando una revisión aparta un mensaje dos veces, queda apartado. **Conexiones**, **Revisiones** muestra cuántos hay y **Apartados** los incluye en una lista. Los mensajes de alguien que te escribe, de una persona conocida o de un cliente se vuelven a revisar unos 3 días después de haber llegado. Esa revisión crea una tarea o cierra el mensaje. Lo que hayas descartado o pospuesto se queda así.
