---
title: Sin tareas nuevas
area: troubleshooting
summary: Las revisiones están desactivadas, en espera o se han detenido al alcanzar el límite de uso de tu modelo. Descubre cómo saber qué ocurre y qué hacer.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: 40617b8ac692660b
---
Las tareas se generan con las revisiones: tu Machine comprueba lo que ha llegado en los últimos 15 minutos, aproximadamente.

## Te acabas de registrar

En una Machine alojada nueva, las revisiones se inician automáticamente cuando conectas la IA y el correo. Mientras tu Machine lee el correo, Tareas muestra «Leyendo tu correo. Tus primeras tareas llegarán en unos minutos». Cuando calcula cuánto correo hay, indica cuánto tardará, más o menos: «Tus primeras tareas llegarán en unos 10 min». Si falta algún paso, **Te necesita** indica cuál, por ejemplo **Conectar correo**, y muestra un enlace a ese paso.

Mientras lee, muestra cuánto ha avanzado («Ha leído 20 de 132 mensajes. Leyendo los 40 siguientes…»), algunas de las personas y organizaciones que ha encontrado y tu primera tarea en cuanto esté lista. El número cuenta los mensajes que ya ha terminado de leer. La barra sigue avanzando mientras lee los siguientes. Los nombres proceden de tu correo y solo tú puedes verlos.

Si la primera revisión no encuentra nada para ti, indica qué ha leído y ofrece opciones para continuar, como conectar un servicio del que recibes muchos correos o preguntar qué ha cambiado esta semana.

## Las revisiones están desactivadas

En la parte superior de Tareas aparece «Las revisiones están desactivadas, así que todavía no llegan tareas». En una Machine alojada, pulsa **Activar las revisiones**. En tu ordenador, ejecuta `./install.sh --activate`.

## El límite de tu modelo

Para dejar margen para tus propios chats, las revisiones se pausan al alcanzar aproximadamente el 65 % del límite de 5 horas de tu plan de IA y el 90 % del límite semanal. Si tienes un modelo de respaldo en otro plan, las revisiones no esperan. Consulta [Modelo](model.md).

Mientras las revisiones están en espera, en la parte superior del panel se indica hasta cuándo, por ejemplo: «Las revisiones esperan hasta las 07:15 para reservar tu límite semanal de ChatGPT». **Revisar ahora** inicia una revisión de todos modos. En **Ajustes**, **Modelo** puedes consultar tus límites.

No se pierde nada: se revisa lo que ha llegado en cuanto se puede. Si la espera es larga, primero se revisan los mensajes recientes de otras personas y, en cada revisión, también se avanza con los más antiguos.

Hasta que se ponga al día, las nuevas tareas llegan sin borrador para que tu plan se destine primero a revisar tus mensajes. Los borradores llegan más tarde y las tareas urgentes no esperan. Pulsa **Hazlo** para recibir uno ahora.

## Por la noche

Las revisiones se pausan de 00:00 a 06:30 y los mensajes nuevos quedan en espera. Se revisan juntos a las 06:30, antes de tu resumen de la mañana. **Revisiones** indica «En pausa por la noche. Se pondrá al día a las 06:30». Si usas la app, escribes en el chat o tocas una tarea, las revisiones vuelven a ejecutarse hasta que pase una hora sin actividad. **Revisar ahora** inicia una revisión de inmediato.

## Ha fallado una ejecución

**Ejecuciones recientes**, en **Conexiones**, **Revisiones**, muestra cada ejecución. Si alguna falla, se vuelve a intentar automáticamente.

Si una ejecución se detiene al alcanzar el límite de uso de tu plan de IA, aparece **Se ha alcanzado el límite de uso de la IA.** y se indica cuándo se restablece. Es una pausa, no un error: los mensajes quedan en espera y se revisan después del restablecimiento. No se envía nada a los [informes de errores](error-reports.md).

## Apartados

Si una revisión pospone un mensaje dos veces, queda apartado. **Conexiones**, **Revisiones** muestra cuántos hay, y **Apartados** los enumera. Si el mensaje es de una persona que te escribe, alguien que conoces o un cliente, se vuelve a revisar unos 3 días después de su llegada. Esa revisión crea una tarea o cierra el mensaje. Lo que hayas descartado o pospuesto se queda así.
