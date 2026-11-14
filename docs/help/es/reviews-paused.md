---
title: No hay tareas nuevas
area: troubleshooting
summary: Las revisiones están desactivadas, en espera o detenidas por el límite de uso de tu modelo. Cómo saber qué ocurre y qué hacer.
covers: 
code: dashboard.html, assistant.py
order: 3
translated: d265e540d9ecef0e
---
Las tareas se generan con las revisiones: tu Machine revisa lo que ha llegado en unos 15 minutos.

## Te acabas de registrar

En una Machine nueva alojada, las revisiones se activan automáticamente cuando conectas tu IA y tu correo. Mientras tu Machine lee el correo, Tareas muestra «Leyendo tu correo. Tus primeras tareas estarán listas en unos minutos». Cuando sabe cuántos mensajes hay, indica más o menos cuánto tardará: «Tus primeras tareas estarán listas en unos 10 min». Si falta algún paso, **Te necesita** te indica cuál, como **Conectar correo**, y te lleva directamente a ese paso.

Mientras lee, Tareas muestra cuánto ha avanzado («Ha leído 20 de 132 mensajes. Leyendo los siguientes 40…»), algunas de las personas y organizaciones que ha encontrado, y tu primera tarea en cuanto está lista. El número cuenta los mensajes que ya terminó de leer; la barra sigue avanzando mientras lee los siguientes. Los nombres provienen de tu correo y solo tú los ves.

Si en la primera revisión no encuentra nada para ti, indica qué leyó y te ofrece los siguientes pasos, como conectar un servicio del que recibes correos con frecuencia o preguntar qué ha cambiado esta semana.

## Las revisiones están desactivadas

En la parte superior de Tareas aparece «Las revisiones están desactivadas, así que aún no recibirás tareas». En una Machine alojada, pulsa **Activar las revisiones**. En tu propio equipo, ejecuta `./install.sh --activate`.

## El límite de tu modelo

Para dejar margen para tus propios chats, las revisiones se pausan al llegar a aproximadamente el 65 % del límite de 5 horas de tu plan de IA y al 90 % del límite semanal. Si tienes un modelo de respaldo en otro plan, las revisiones no esperan. Consulta [Modelo](model.md).

Mientras las revisiones están en espera, en la parte superior del panel se indica hasta cuándo, por ejemplo: «Las revisiones esperan hasta las 07:15 para ahorrar tu límite semanal de ChatGPT». **Revisar ahora** inicia una revisión de todos modos. En **Ajustes**, **Modelo** puedes consultar tus límites.

No se pierde nada: se revisa lo que ha llegado en cuanto sea posible.

## Por la noche

De las 00:00 a las 06:30, las revisiones se pausan y los mensajes nuevos quedan en espera. Se revisan todos juntos a las 06:30, antes del resumen de la mañana. **Revisiones** muestra «En pausa por la noche. Se pondrán al día a las 06:30». Si usas la app, escribes en el chat o tocas una tarea, las revisiones vuelven a ejecutarse hasta que lleves una hora sin actividad. **Revisar ahora** revisa los mensajes de inmediato.

## Error en una ejecución

**Ejecuciones recientes**, en **Conexiones** > **Revisiones**, muestra cada ejecución. Si una falla, se vuelve a intentar automáticamente.

## Apartar mensajes

Cuando una revisión pospone un mensaje dos veces, se aparta. **Conexiones** > **Revisiones** muestra cuántos hay y **Apartados** los enumera. Los mensajes de alguien que te escribe, de alguien que conoces o de un cliente se revisan una vez más unos 3 días después de llegar. Esa revisión crea una tarea o cierra el mensaje. Lo que descartaste o pospusiste sigue así.
