---
title: Informes de errores
area: security
summary: Cuando algo falla, tu Machine le cuenta al equipo de The Machine qué falló y en qué parte del código. Nunca comparte tus mensajes, nombres ni direcciones.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: fd3e1c2d68b93a35
---
## Qué es

Cuando algo falla en The Machine, tu Machine envía a nuestro equipo una nota breve y anónima sobre el error, para que podamos corregirlo antes de que alguien lo reporte. Está activado de forma predeterminada y requiere [The Machine Network](/network).

## Qué se envía

Solo esto, según el tipo de error:

- el tipo de error, como `KeyError`;
- su mensaje, después de quitar cualquier dato específico: números, identificadores, texto entre comillas, direcciones de correo electrónico, enlaces, rutas de archivos, claves y cualquier palabra que pueda ser un nombre;
- dónde ocurrió en el código propio de The Machine, nunca en una carpeta de tu computadora;
- la versión de la app, cuántas veces ocurrió y cuándo ocurrió la primera y la última vez.

Un ejemplo real: `IndexError`, `list index out of range`, en `assistant.py:fault_event:7899`, versión `05b17ee6ac79`, 1 vez.

## Qué nunca se envía

Lo que dicen tus mensajes, tareas, borradores o chats. Nombres, direcciones de correo electrónico, números de teléfono, enlaces o contraseñas. Ni la cuenta ni la persona de la que se trataba.

## De dónde vienen los errores

- del trabajo en segundo plano: revisiones de mensajes nuevos, preparación de tareas, chats, conexiones y sincronizaciones;
- del panel, en tu navegador o en la app, incluidos los errores que te mostró;
- de solicitudes del panel que fallan o agotan el tiempo de espera: cuál fue la solicitud, nunca lo que envió;
- de trabajos de agentes de programación que fallan: solo la herramienta y el tipo de fallo.

Los errores repetidos se cuentan, pero no se vuelven a enviar. Como máximo, se envía un lote cada 10 minutos. Los conservamos durante 30 días.

## Ritmo de trabajo

El trabajo en segundo plano se pausa cuando estás cerca de alcanzar los límites de tu plan de IA, para dejar espacio para tus propios chats (consulta [Tu modelo de IA](model.md)).

Si los informes de errores están activados, tu Machine también nos indica una vez al día con qué frecuencia ocurrió: por cada pausa, la hora, el límite alcanzado, cuánto duró y cuántos trabajos esperaron. No incluye información sobre lo que hacían los trabajos.

## Desactivarlos

En **Ajustes**, **Seguridad**, desactiva **Enviar informes de errores**. No se registra ni se envía nada más, y se elimina lo que estaba pendiente. Los errores seguirán apareciendo en tu Machine, que puede ofrecerte una solución.

Consulta [Seguridad y privacidad](security-and-privacy.md).
