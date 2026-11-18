---
title: Informes de errores
area: security
summary: Cuando algo falla, tu Machine le indica al equipo de The Machine qué falló y dónde, en el código. Nunca incluye tus mensajes, nombres ni direcciones.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: f67d18a44999cfce
---
## Qué son

Cuando algo falla en The Machine, tu Machine envía a nuestro equipo una nota breve y anónima sobre el error, para que podamos solucionarlo antes de que alguien lo reporte. La opción está activada de forma predeterminada y necesita [The Machine Network](/network).

## Qué se envía

Solo estos datos por cada tipo de error:

- el tipo de error, como `KeyError`;
- el mensaje, sin datos específicos: números, identificadores, texto entre comillas, direcciones de correo electrónico, enlaces, rutas de archivos, claves y cualquier palabra que pueda ser un nombre;
- dónde ocurrió en el código de The Machine, nunca en una carpeta de tu ordenador;
- la versión de la app, cuántas veces ocurrió y cuándo ocurrió por primera y última vez.

Por ejemplo: `IndexError`, `list index out of range`, en `machine/faults.py:fault_event:246`, versión `05b17ee6ac79`, 1 vez.

## Qué nunca se envía

El contenido de tus mensajes, tareas, borradores o chats. Nombres, direcciones de correo electrónico, números de teléfono, enlaces o contraseñas. A qué cuenta o persona se refería.

## De dónde vienen los errores

- el trabajo en segundo plano: revisar mensajes nuevos, preparar tareas, chats, conexiones y sincronizaciones;
- el panel, en tu navegador o en la app, incluidos los errores que te mostró;
- las solicitudes del panel que fallan o agotan el tiempo de espera: cuál fue la solicitud, nunca lo que envió;
- las tareas del agente de programación que fallan: solo la herramienta y el tipo de error;
- la prueba breve de tu IA cuando falla: el error de la IA, sin datos específicos.

Un conector que hayas añadido tú (tu propio archivo en `connectors/`) nunca envía sus errores. Puedes verlos en su tarjeta de conexión.

Los errores repetidos se cuentan, pero no se vuelven a enviar. Como máximo, se envía un lote cada 10 minutos. Los conservamos durante 30 días.

## Ritmo de actividad

El trabajo en segundo plano se pausa cuando quedan pocos recursos en los límites de tu plan de IA, para dejar espacio para tus propios chats (consulta [Tu modelo de IA](model.md)).

Si los informes de errores están activados, tu Machine también nos indica una vez al día con qué frecuencia ocurrió: la hora de cada pausa, qué límite la provocó, cuánto duró y cuántas tareas quedaron en espera. No informa de qué trataban las tareas.

## Desactivar los informes

En **Ajustes**, **Seguridad**, desactiva **Enviar informes de errores**. No se registra ni se envía nada más, y se elimina lo que estaba pendiente. Los errores seguirán apareciendo en tu Machine, que puede sugerirte una solución.

Consulta [Seguridad y privacidad](security-and-privacy.md).
