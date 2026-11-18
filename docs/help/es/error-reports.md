---
title: Informes de errores
area: security
summary: Cuando algo falla, tu Machine le cuenta al equipo de The Machine qué falló y en qué parte del código. Nunca comparte tus mensajes, nombres ni direcciones.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 2253a0d695fe898c
---
## Qué es

Cuando algo falla en The Machine, tu Machine envía a nuestro equipo una nota breve y anónima sobre el error, para que podamos solucionarlo antes de que alguien lo reporte. Está activada por defecto y requiere [The Machine Network](/network).

## Qué se envía

Solo esto, para cada tipo de error:

- el tipo de error, como `KeyError`;
- su mensaje, sin ningún dato específico: números, identificadores, texto entre comillas, direcciones de correo electrónico, enlaces, rutas de archivos, claves y cualquier palabra que pueda ser un nombre;
- dónde ocurrió en el código de The Machine, nunca en una carpeta de tu ordenador;
- la versión de la app, cuántas veces ocurrió y cuándo fue la primera y la última vez.

Por ejemplo: `IndexError`, `list index out of range`, en `machine/faults.py:fault_event:246`, versión `05b17ee6ac79`, 1 vez.

## Qué nunca se envía

El contenido de tus mensajes, tareas, borradores o chats. Nombres, direcciones de correo electrónico, números de teléfono, enlaces o contraseñas. De qué cuenta o persona se trataba.

## De dónde vienen los errores

- tareas en segundo plano: comprobaciones de mensajes nuevos, preparación de tareas, chat, conexiones y sincronizaciones;
- el panel, en tu navegador o en la app, incluidos los errores que te muestra;
- solicitudes del panel que fallan o agotan el tiempo de espera: cuál fue la solicitud, nunca lo que envió;
- tareas fallidas de agentes de programación: solo la herramienta y el tipo de fallo;
- la breve prueba de tu IA cuando falla: el error de la IA, sin ningún dato específico.

Un conector que hayas añadido tú (tu propio archivo en `connectors/`) solo envía el nombre de su servicio y la etiqueta de su error, como `notes` y `notes_http: HTTP unauthorized`, para que podamos ayudarte a solucionarlo. No envía nada más de su código. La tarjeta de conexión muestra el error completo.

Los errores repetidos se cuentan, pero no se vuelven a enviar. Se envía como máximo un lote cada 10 minutos. Los conservamos durante 30 días.

## Ritmo

Las tareas en segundo plano esperan cuando los límites de tu plan de IA están a punto de agotarse, para dejar espacio para tus propios chats (consulta [Tu modelo de IA](model.md)).

Si los informes de errores están activados, tu Machine también nos dice una vez al día con qué frecuencia ocurrió: para cada pausa, la hora, qué límite se alcanzó, cuánto duró y cuántas tareas esperaron. No nos dice de qué trataban las tareas.

## Desactivarlos

En **Ajustes**, **Seguridad**, desactiva **Enviar informes de errores**. No se registra ni se envía nada más, y se elimina lo que estaba en espera. Los errores seguirán apareciendo en tu Machine, que puede ofrecerte una solución.

Consulta [Seguridad y privacidad](security-and-privacy.md).
