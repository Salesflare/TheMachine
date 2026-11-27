---
title: Informes de errores
area: security
summary: Cuando algo falla, tu Machine le cuenta al equipo de The Machine qué ha fallado y en qué parte del código. Nunca incluye tus mensajes, nombres ni direcciones.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: d474cfa6bcefd25a
---
## Qué es

Cuando algo falla en The Machine, tu Machine envía al equipo una nota breve y anónima sobre el error para que podamos corregirlo antes de que alguien lo notifique. Está activado de forma predeterminada y necesita [The Machine Network](/network).

## Qué se envía

Solo estos datos, según el tipo de error:

- el tipo de error, como `KeyError`;
- el mensaje, después de eliminar cualquier dato específico: números, identificadores, texto entrecomillado, direcciones de correo, enlaces, rutas de archivos, claves y cualquier palabra que pueda ser un nombre;
- en qué parte del código propio de The Machine ocurrió, nunca en qué carpeta de tu ordenador;
- la versión de la app, cuántas veces ocurrió y cuándo ocurrió por primera y última vez.

Por ejemplo: `IndexError`, `list index out of range`, en `machine/faults.py:fault_event:246`, versión `05b17ee6ac79`, 1 vez.

## Qué no se envía nunca

Lo que dicen tus mensajes, tareas, borradores o chats. Nombres, direcciones de correo, números de teléfono, enlaces o contraseñas. Tampoco se envía información sobre la cuenta o la persona a la que se refería.

## De dónde vienen los errores

- tareas en segundo plano: comprobaciones de mensajes nuevos, preparación de tareas, chats, conexiones y sincronizaciones;
- el panel, en el navegador o en la app, incluidos los errores que te muestra;
- solicitudes del panel que fallan o agotan el tiempo de espera: cuál ha fallado, nunca lo que se envió;
- tareas del agente de programación que fallan: solo la herramienta y el tipo de fallo;
- la breve prueba de tu IA cuando falla: el error de la IA, después de eliminar cualquier dato específico.

Una comprobación que se detiene al alcanzar el límite de uso de tu plan de IA no es un error y no se envía: espera hasta que se restablezca el límite. Tampoco se envía una comprobación que falla porque has cerrado la sesión de tu IA: **Te necesita** te pide que vuelvas a iniciar sesión.

Un conector que hayas añadido tú (tu propio archivo en `connectors/`) solo envía el nombre del servicio y la etiqueta del error, como `notes` y `notes_http: HTTP unauthorized`, para que podamos ayudarte a solucionarlo. No envía nada más de su código. La tarjeta de conexión muestra el error completo.

Los errores repetidos se cuentan, pero no se vuelven a enviar. Como máximo, se envía un lote cada 10 minutos. Los conservamos durante 30 días.

## Límites de uso

Las tareas en segundo plano esperan cuando se agotan los límites de tu plan de IA, para dejar espacio a tus propios chats (consulta [Tu modelo de IA](model.md)).

Si los informes de errores están activados, tu Machine también nos indica una vez al día con qué frecuencia ha ocurrido: por cada pausa, la hora, qué límite se ha alcanzado, cuánto ha durado y cuántas tareas han esperado. No incluye información sobre esas tareas.

## Desactivarlo

En **Ajustes**, dentro de **Seguridad**, desactiva **Enviar informes de errores**. No se registra ni se envía nada más, y se elimina lo que estaba pendiente. Los errores siguen apareciendo en tu Machine, que puede ofrecerte una solución.

Consulta [Seguridad y privacidad](security-and-privacy.md).
