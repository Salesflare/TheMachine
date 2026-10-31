---
title: No hay tareas nuevas
area: troubleshooting
summary: Las revisiones están desactivadas, esperando o paradas por el límite de uso de tu modelo. Cómo saberlo y qué hacer.
covers: 
code: dashboard.html, assistant.py
order: 3
---
Las tareas salen de las revisiones: tu Machine lee lo que ha llegado, en lotes pequeños, en más o menos una hora.

## Las revisiones están desactivadas

La parte superior de Sugerencias dice "Las revisiones están desactivadas, así que aún no llegan sugerencias." En una Machine alojada, pulsa **Activar revisiones**. En tu propio ordenador, ejecuta `./install.sh --activate`.

## El límite de tu modelo

Las revisiones de lo que llegó se pausan hacia el 65% del límite de 5 horas de tu plan y al 90% de su límite semanal, para dejar margen a tus propios chats. Un tablero que recorre tu historial va más despacio, a más o menos un séptimo de la semana al día. Con un modelo de respaldo que funcione, con otro plan o proveedor, las revisiones no esperan. Consulta [Modelo](model.md).

Mientras las revisiones esperan, la parte superior del panel dice hasta cuándo, como "Las revisiones esperan hasta las 07:15 para ahorrar tu semana de ChatGPT." **Revisar ahora** inicia una enseguida. Cuando se alcanza un límite, la parte superior del panel dice cuál y cuándo se reinicia. **Conexiones** y luego **Revisiones** lo muestra junto a la ejecución. **Ajustes**, **Modelo** muestra tus límites. Consulta [Modelo](model.md).

No se pierde nada mientras espera: lo que llegó se revisa en cuanto se pueda.

## Falló una ejecución

**Ejecuciones recientes** en **Revisiones** muestra cada ejecución. Un lote fallido se reintenta solo.
