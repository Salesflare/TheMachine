---
title: Informes de errores
area: security
summary: Cuando algo falla, tu Machine le dice al equipo de The Machine qué falló y en qué parte del código. Nunca tus mensajes, nombres ni direcciones.
covers: error-reports
code: error_feed.py, dashboard.html
order: 4
---
## Qué es

Cuando algo falla en The Machine, tu Machine envía al equipo una firma breve del error, para que podamos arreglarlo antes de que nadie tenga que informar de él. Está activado por defecto y necesita [The Machine Network](/network).

## Qué se envía

Solo esto, para cada tipo de error:

- el tipo de error, como `KeyError` o `TypeError`;
- su mensaje sin nada concreto: números, identificadores, texto entre comillas, direcciones de correo, enlaces, rutas de archivos y cualquier cosa que parezca una clave. Cualquier otra palabra que pueda ser un nombre también se quita;
- dónde pasó en el propio código de The Machine: archivo, función y línea, nunca una carpeta de tu ordenador;
- la versión de la app, cuántas veces pasó, y cuándo fue la primera y la última.

Uno real: `IndexError`, `list index out of range`, en `assistant.py:fault_event:7899`, versión `05b17ee6ac79`, 1 vez.

## Qué no se envía nunca

Lo que dicen tus mensajes, tareas, borradores o chats. Nombres, direcciones de correo, números de teléfono, enlaces, tokens ni contraseñas. De qué cuenta o persona se trataba.

## De dónde vienen los errores

- el servicio y sus trabajos: revisiones, preparación de tareas, chat, conexiones y sincronizaciones;
- el panel en tu navegador;
- los trabajos de Claude Code y Codex que fallan: solo la herramienta y el tipo de fallo.

El mismo error cuenta una vez, con un recuento. Como mucho, un lote cada 10 minutos. El equipo los guarda 30 días.

## Desactívalo

En Ajustes, Seguridad, desactiva **Enviar informes de errores**. No se registra ni se envía nada más, y lo que estaba esperando se elimina. Los errores se siguen viendo en tu propia Machine, que puede ofrecerte un arreglo.

Consulta [Seguridad y privacidad](security-and-privacy.md).
