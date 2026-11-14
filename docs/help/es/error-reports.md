---
title: Informes de errores
area: security
summary: Cuando algo falla, tu Machine le cuenta al equipo de The Machine qué falló y dónde en el código. Nunca comparte tus mensajes, nombres ni direcciones.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 03a8649f2f634b59
---
## Qué son

Cuando algo falla en The Machine, tu Machine envía a nuestro equipo una breve nota anónima sobre el error para que podamos corregirlo antes de que alguien lo reporte. Esta opción está activada de forma predeterminada y requiere [The Machine Network](/network).

## Qué se envía

Solo esto, para cada tipo de error:

- el tipo de error, como `KeyError`;
- su mensaje, sin datos específicos: números, identificadores, texto entre comillas, direcciones de correo electrónico, enlaces, rutas de archivos, claves y cualquier palabra que pudiera ser un nombre;
- dónde ocurrió en el código propio de The Machine, nunca en una carpeta de tu equipo;
- la versión de la aplicación, cuántas veces ocurrió y cuándo ocurrió por primera y última vez.

Por ejemplo: `IndexError`, `list index out of range`, en `machine/faults.py:fault_event:246`, versión `05b17ee6ac79`, 1 vez.

## Qué nunca se envía

El contenido de tus mensajes, tareas, borradores o chats. Nombres, direcciones de correo electrónico, números de teléfono, enlaces o contraseñas. De qué cuenta o persona se trataba.

## De dónde vienen los errores

- tareas en segundo plano: comprobaciones de mensajes nuevos, preparación de tareas, chats, conexiones y sincronizaciones;
- el panel, en tu navegador o en la aplicación, incluidos los errores que te mostró;
- solicitudes del panel que fallan o agotan el tiempo de espera: cuál falló, nunca qué envió;
- tareas fallidas de agentes de programación: solo la herramienta y el tipo de fallo.

Los errores repetidos se cuentan, pero no se vuelven a enviar. Como máximo, se envía un lote cada 10 minutos. Los conservamos durante 30 días.

## Ritmo

Las tareas en segundo plano esperan cuando los límites de tu plan de IA están cerca de agotarse, para reservar capacidad para tus propios chats (consulta [Tu modelo de IA](model.md)).

Si los informes de errores están activados, tu Machine también nos cuenta una vez al día con qué frecuencia ocurrió: por cada pausa, la hora, qué límite se alcanzó, cuánto duró y cuántas tareas esperaron. No comparte de qué trataban las tareas.

## Desactivarlos

En **Ajustes**, **Seguridad**, desactiva **Enviar informes de errores**. No se registrará ni se enviará nada más, y se eliminará lo que estuviera pendiente. Los errores seguirán apareciendo en tu Machine, que puede ofrecerte una solución.

Consulta [Seguridad y privacidad](security-and-privacy.md).
