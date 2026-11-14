---
title: No hay tareas nuevas
area: troubleshooting
summary: Las revisiones están desactivadas, esperando o paradas por el límite de uso de tu modelo. Cómo saberlo y qué hacer.
covers: 
code: dashboard.html, assistant.py
order: 3
translated: 39b4aa749445dfba
---
Las tareas salen de las revisiones: tu Machine lee lo que ha llegado, en lotes pequeños, en unos 15 minutos.

## Recién registrado

En una Machine alojada nueva, las revisiones empiezan solas en cuanto tu IA y tu correo están conectados. Mientras tu Machine lee tu correo, Tareas dice "Leyendo tu correo, tus primeras tareas llegan en unos minutos". En cuanto sabe cuánto hay, dice más o menos cuánto tarda: "Primeras tareas en unos 10 min." Si falta un paso, **Te necesita** lo nombra, como **Conectar correo**, con un enlace a ese paso.

Mientras lee, Tareas muestra cuánto lleva, algunas de las personas y organizaciones que encontró y tu primera tarea en cuanto llega. Los nombres salen de tu propio correo y solo tú los ves.

Si en el primer vistazo no encuentra nada para ti, dice lo que leyó y ofrece próximos pasos, como conectar un servicio que te escribe a menudo o preguntar qué cambió esta semana.

## Las revisiones están desactivadas

La parte superior de Tareas dice "Las revisiones están desactivadas, así que aún no llegan tareas." En una Machine alojada, pulsa **Activar las revisiones**. En tu propio ordenador, ejecuta `./install.sh --activate`.

## El límite de tu modelo

Las revisiones de lo que llegó se pausan hacia el 65% del límite de 5 horas de tu plan y al 90% de su límite semanal, para dejar margen a tus propios chats. Un tablero que recorre tu historial va más despacio, a más o menos un séptimo de la semana al día. Con un modelo de respaldo que funcione, con otro plan o proveedor, las revisiones no esperan. Consulta [Modelo](model.md).

Mientras las revisiones esperan, la parte superior del panel dice hasta cuándo, como "Las revisiones esperan hasta las 07:15 para ahorrar tu semana de ChatGPT." **Revisar ahora** inicia una enseguida. Cuando se alcanza un límite, la parte superior del panel dice cuál y cuándo se reinicia. **Conexiones** y luego **Revisiones** lo muestra junto a la ejecución. **Ajustes**, **Modelo** muestra tus límites. Consulta [Modelo](model.md).

No se pierde nada mientras espera: lo que llegó se revisa en cuanto se pueda.

## De noche

De 00:00 a 06:30, las revisiones se pausan y los mensajes nuevos esperan. Se revisan juntos a las 06:30, antes de tu resumen de la mañana. **Revisiones** dice entonces "En pausa por la noche, se pone al día a las 06:30". Si usas la app, escribes en el chat o tocas una tarea, las revisiones vuelven hasta que lleves una hora sin usarla. **Revisar ahora** revisa al momento.

## Falló una ejecución

**Ejecuciones recientes** en **Revisiones** muestra cada ejecución. Un lote fallido se reintenta solo.

## Apartados

Cuando una revisión aplaza un mensaje dos veces, queda apartado. **Conexiones**, **Revisiones** muestra cuántos, y **Apartados** los enumera. Uno de una persona que te escribe directamente, de alguien que conoces o de un cliente recibe una última mirada unos 3 días después de llegar. Esa mirada crea una tarea o lo cierra. Lo que descartaste o pospusiste se queda así.
