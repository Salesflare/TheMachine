---
title: Informes de errores
area: security
summary: Cuando algo falla, tu Machine le cuenta al equipo de The Machine qué falló y dónde ocurrió en el código. Nunca comparte tus mensajes, nombres ni direcciones.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 4dc53a854d15f1a3
---
## Qué es

Cuando algo falla en The Machine, tu Machine envía al equipo una nota breve y anónima sobre el error para que podamos corregirlo antes de que alguien lo reporte. La opción está activada de forma predeterminada y requiere [The Machine Network](/network).

## Qué se envía

Solo esto, por cada tipo de error:

- el tipo de error, como `KeyError`;
- el mensaje, sin datos específicos: números, identificadores, texto entre comillas, direcciones de correo, enlaces, rutas de archivos, claves y cualquier palabra que pueda ser un nombre;
- en qué parte del código de The Machine ocurrió, nunca en una carpeta de tu computadora;
- la versión de la app, cuántas veces ocurrió y cuándo ocurrió por primera y última vez.

Por ejemplo: `IndexError`, `list index out of range`, en `machine/faults.py:fault_event:246`, versión `05b17ee6ac79`, 1 vez.

## Qué nunca se envía

El contenido de tus mensajes, tareas, borradores o chats. Nombres, direcciones de correo, números de teléfono, enlaces o contraseñas. Ni de qué cuenta o persona se trataba.

## De dónde vienen los errores

- tareas en segundo plano: revisar mensajes nuevos, preparar tareas, chats, Conexiones y sincronizaciones;
- el panel, en tu navegador o en la app, incluidos los errores que te muestra;
- solicitudes del panel que fallan o agotan el tiempo de espera: cuál fue la solicitud, nunca qué datos envió;
- tareas de agentes de programación que fallan: solo la herramienta y el tipo de fallo;
- la breve prueba de tu IA cuando falla: el error de la IA, sin datos específicos.

Los errores repetidos se cuentan, pero no se vuelven a enviar. Se envía como máximo un lote cada 10 minutos. Los conservamos durante 30 días.

## Frecuencia

Las tareas en segundo plano esperan cuando quedan pocos usos disponibles en los límites de tu plan de IA, para dejar espacio para tus propios chats (consulta [Tu modelo de IA](model.md)).

Si los informes de errores están activados, tu Machine también nos indica una vez al día con qué frecuencia ocurrió: por cada pausa, la hora, qué límite se alcanzó, cuánto duró y cuántas tareas esperaron. No incluye información sobre esas tareas.

## Desactivarlos

En **Ajustes**, **Seguridad**, desactiva **Enviar informes de errores**. No se registra ni se envía nada más, y se elimina lo que estaba pendiente. Los errores siguen apareciendo en tu Machine, que puede ofrecerte una solución.

Consulta [Seguridad y privacidad](security-and-privacy.md).
