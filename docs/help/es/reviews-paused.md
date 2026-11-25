---
title: Sin tareas nuevas
area: troubleshooting
summary: Las revisiones están desactivadas, en espera o se han detenido por el límite de uso de tu modelo. Cómo saber qué pasa y qué hacer.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: f0e9e4dc6c850b25
---
Las tareas se generan con las revisiones: tu Machine comprueba lo que ha llegado en unos 15 minutos.

## Te acabas de registrar

En una Machine alojada nueva, las revisiones se inician automáticamente cuando conectas tu IA y el correo. Mientras tu Machine lee el correo, Tareas muestra «Leyendo tu correo. Tus primeras tareas estarán listas en unos minutos». Cuando sabe cuánto hay que revisar, indica un tiempo aproximado: «Tus primeras tareas estarán listas en unos 10 min». Si falta algún paso, **Te necesita** te lo indica, por ejemplo **Conectar correo**, con un enlace para completarlo.

Mientras lee, Tareas muestra cuánto ha avanzado («Ha leído 20 de 132 mensajes. Leyendo los 40 siguientes…»), algunas de las personas y organizaciones que ha encontrado y tu primera tarea en cuanto esté lista. El número cuenta los mensajes que ha terminado de leer; la barra sigue avanzando mientras lee los siguientes. Los nombres proceden de tu correo y solo tú los ves.

Si en la primera revisión no encuentra nada para ti, indica qué ha leído y propone los siguientes pasos, como conectar un servicio del que recibes muchos correos o preguntar qué ha cambiado esta semana.

## Las revisiones están desactivadas

En la parte superior de Tareas aparece «Las revisiones están desactivadas. Aún no recibirás tareas». En una Machine alojada, pulsa **Activar las revisiones**. En tu propio ordenador, ejecuta `./install.sh --activate`.

## El límite de tu modelo

Para dejar margen para tus propios chats, las revisiones se pausan cuando se alcanza aproximadamente el 65 % del límite de 5 horas de tu plan de IA y el 90 % del límite semanal. Si tienes un modelo de respaldo con otro plan, las revisiones no esperan. Consulta [Modelo](model.md).

Mientras las revisiones están en espera, en la parte superior del panel aparece hasta cuándo, por ejemplo: «Las revisiones esperan hasta las 07:15 para que puedas seguir usando ChatGPT esta semana». **Revisar ahora** inicia una revisión de todos modos. En **Ajustes**, **Modelo** puedes ver tus límites.

No se pierde nada: los mensajes se revisan en cuanto se puede. Si la espera es larga, primero se revisan los mensajes recientes de personas y, en cada revisión, también se avanza con parte de los más antiguos.

## Por la noche

Desde las 00:00 hasta las 06:30, las revisiones se pausan y los mensajes nuevos quedan en espera. Se revisan todos juntos a las 06:30, antes del resumen de la mañana. **Revisiones** muestra «Pausadas por la noche. Se pondrán al día a las 06:30». Si usas la app, escribes en el chat o tocas una tarea, las revisiones vuelven a ejecutarse hasta que lleves una hora sin actividad. **Revisar ahora** revisa los mensajes enseguida.

## Una ejecución ha fallado

**Ejecuciones recientes**, en **Conexiones**, **Revisiones**, muestra cada ejecución. Si una falla, se vuelve a intentar automáticamente.

Si una ejecución se detiene por el límite de uso de tu plan de IA, muestra **Se ha alcanzado el límite de uso de la IA.** e indica cuándo se restablece. Es una pausa, no un fallo: los mensajes quedan en espera y se revisan después del restablecimiento. No se envía nada a los [informes de errores](error-reports.md).

## Apartados

Cuando una revisión pospone un mensaje dos veces, pasa a Apartados. **Conexiones**, **Revisiones** muestra cuántos hay, y **Apartados** los enumera. Si el mensaje es de alguien que te escribe, de alguien que conoces o de un cliente, se revisa una vez más unos 3 días después de haber llegado. Esa revisión crea una tarea o cierra el mensaje. Lo que hayas descartado o pospuesto se mantiene así.
