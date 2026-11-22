---
title: Informes de errores
area: security
summary: Cuando algo falla, tu Machine le cuenta al equipo de The Machine qué ha fallado y en qué parte del código. Nunca comparte tus mensajes, nombres ni direcciones.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: e1d4d602255cde39
---
## Qué es

Cuando algo falla en The Machine, tu Machine envía a nuestro equipo una nota breve y anónima sobre el error para que podamos corregirlo antes de que alguien nos lo comunique. Está activado de forma predeterminada y necesita [The Machine Network](/network).

## Qué se envía

Solo esto, para cada tipo de error:

- el tipo de error, como `KeyError`;
- el mensaje, sin ningún dato concreto: números, identificadores, texto entrecomillado, direcciones de correo, enlaces, rutas de archivos, claves y cualquier palabra que pueda ser un nombre;
- en qué parte del código de The Machine ocurrió, nunca en una carpeta de tu ordenador;
- la versión de la aplicación, cuántas veces ocurrió y cuándo ocurrió por primera y última vez.

Por ejemplo: `IndexError`, `list index out of range`, en `machine/faults.py:fault_event:246`, versión `05b17ee6ac79`, 1 vez.

## Qué nunca se envía

El contenido de tus mensajes, tareas, borradores o chats. Nombres, direcciones de correo, números de teléfono, enlaces o contraseñas. A qué cuenta o persona se refería.

## De dónde vienen los errores

- el trabajo en segundo plano: comprobaciones de mensajes nuevos, preparación de tareas, chats, conexiones y sincronizaciones;
- el panel, en el navegador o en la aplicación, incluidos los errores que te muestra;
- solicitudes del panel que fallan o agotan el tiempo de espera: cuál, nunca qué enviaron;
- tareas de agentes de programación que fallan: solo la herramienta y el tipo de fallo;
- la prueba breve de tu IA cuando falla: el error de la IA, sin ningún dato concreto.

Una comprobación que se detiene al alcanzar el límite de uso de tu plan de IA no es un error y no se envía: espera a que se restablezca el límite.

Un conector que hayas añadido tú (tu propio archivo en `connectors/`) solo envía el nombre de su servicio y la etiqueta del error, como `notes` y `notes_http: HTTP unauthorized`, para que podamos ayudarte a corregirlo. No envía nada más de su código. La tarjeta de conexión muestra el error completo.

Los errores repetidos se cuentan, pero no se vuelven a enviar. Se envía como máximo un lote cada 10 minutos. Los conservamos durante 30 días.

## Control del ritmo

El trabajo en segundo plano se pausa cuando quedan pocos usos dentro de los límites de tu plan de IA, para dejar espacio a tus chats (consulta [Tu modelo de IA](model.md)).

Si los informes de errores están activados, tu Machine también nos indica una vez al día con qué frecuencia ocurrió: por cada pausa, la hora, el límite alcanzado, cuánto duró y cuántas tareas quedaron en espera. No indica de qué tareas se trataba.

## Desactivarlo

En **Ajustes**, **Seguridad**, desactiva **Enviar informes de errores**. No se registra ni se envía nada más, y se elimina lo que estaba en espera. Los errores siguen apareciendo en tu propia Machine, que puede ofrecerte una solución.

Consulta [Seguridad y privacidad](security-and-privacy.md).
