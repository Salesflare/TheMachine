---
title: Sin tareas nuevas
area: troubleshooting
summary: Las revisiones están desactivadas, en espera o detenidas por el límite de uso de tu modelo. Cómo comprobarlo y qué hacer.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: d8a15909ab8164e8
---
Las tareas salen de las revisiones: tu Machine comprueba lo que ha llegado en los últimos 15 minutos, más o menos.

## Te acabas de registrar

En una nueva Machine alojada, las revisiones empiezan automáticamente cuando conectas tu IA y el correo. Mientras tu Machine lee el correo, Tareas muestra «Leyendo tu correo. Tus primeras tareas llegarán en unos minutos». Cuando calcula cuánto correo hay, indica aproximadamente cuánto tardará: «Tus primeras tareas llegarán en unos 10 min». Si falta algún paso, **Te necesita** te indica cuál, como **Conectar correo**, con un enlace para completarlo.

Mientras lee, Tareas muestra por dónde va («Ha leído 20 de 132 mensajes. Leyendo los siguientes 40…»), algunas de las personas y organizaciones que ha encontrado y tu primera tarea en cuanto esté lista. El número cuenta los mensajes que ya ha terminado de leer; la barra sigue avanzando mientras lee los siguientes. Los nombres salen de tu correo y solo tú puedes verlos.

Si en la primera revisión no encuentra nada para ti, te dice qué ha leído y te ofrece los siguientes pasos, como conectar un servicio del que recibes muchos correos o preguntar qué ha cambiado esta semana.

## Las revisiones están desactivadas

En la parte superior de Tareas aparece «Las revisiones están desactivadas, así que todavía no recibirás tareas». En una Machine alojada, pulsa **Activar las revisiones**. En tu propio ordenador, ejecuta `./install.sh --activate`.

## El límite de tu modelo

Para que te quede margen para tus propios chats, las revisiones se pausan cuando alcanzan aproximadamente el 65 % del límite de 5 horas de tu plan de IA y el 90 % del límite semanal. Si tienes un modelo de respaldo en otro plan, las revisiones no esperan. Consulta [Modelo](model.md).

Mientras las revisiones están en espera, en la parte superior del panel aparece hasta cuándo, por ejemplo: «Las revisiones esperan hasta las 07:15 para que puedas seguir usando ChatGPT esta semana». **Revisar ahora** inicia una revisión igualmente. En **Ajustes**, **Modelo** puedes consultar tus límites.

No se pierde nada: se revisa lo que ha llegado en cuanto se puede. Si la espera se alarga, primero se revisan los mensajes recientes de otras personas, y cada revisión también procesa algunos de los más antiguos.

Hasta que se ponga al día, llegan tareas nuevas sin borrador para que tu plan se dedique primero a revisar tus mensajes. Los borradores llegarán después, y las tareas urgentes no esperan. Pulsa **Hazlo** para obtener un borrador ahora.

## Por la noche

De las 00:00 a las 06:30, las revisiones se pausan y los mensajes nuevos esperan. Se revisan todos juntos a las 06:30, antes de tu resumen de la mañana. **Revisiones** muestra «En pausa por la noche. Se pondrá al día a las 06:30». Usa la app, escribe en el chat o pulsa una tarea para que las revisiones vuelvan a ejecutarse. Seguirán hasta que lleves una hora sin usar la app. **Revisar ahora** inicia una revisión al momento.

## Ha fallado una ejecución

**Ejecuciones recientes**, en **Conexiones**, **Revisiones**, muestra cada ejecución. Si una falla, se vuelve a intentar automáticamente. Si tu IA deja de responder, por ejemplo porque ha caducado el inicio de sesión, vuelve a iniciar sesión en **Ajustes**, **Modelo**. Las revisiones se reanudarán enseguida.

Si una ejecución se detiene porque se ha alcanzado el límite de uso de tu plan de IA, muestra **Se ha alcanzado el límite de uso de la IA.** y cuándo se restablece. Es una pausa, no un fallo: los mensajes quedan en espera y se revisan después del restablecimiento. No se envía nada a [informes de errores](error-reports.md).

## Apartados

Si una revisión pospone un mensaje dos veces, se aparta. En **Conexiones**, **Revisiones** puedes ver cuántos hay, y **Apartados** los muestra.

Si un mensaje hace que fallen todas las revisiones aunque tu IA funcione, también se aparta para que se puedan revisar los demás.

Si el mensaje es de alguien que te escribe, alguien que conoces o un cliente, se vuelve a revisar unos 3 días después de que haya llegado. Esa revisión crea una tarea o cierra el mensaje. Lo que hayas descartado o pospuesto se mantiene así.
