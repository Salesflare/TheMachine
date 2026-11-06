---
title: Historial
area: connections
summary: Cerca de un año de correos, reuniones y chats de WhatsApp antiguos, para buscar y leer. Nunca una tarea.
covers: history
code: machine/app/history.py, machine/store/history.py
keywords: older messages, backfill, archive, past emails
---
## Qué guarda

Cada cuenta de correo, calendario y WhatsApp guarda cerca de un año de mensajes y reuniones antiguos. La búsqueda los encuentra, un hilo los muestra y el [Calendario](calendar.md) muestra las reuniones pasadas.

Su tarjeta dice hasta dónde llega: **Historial: hasta** un mes, cuando ya está.

## Qué nunca hace

El historial solo sirve para consultar. Nunca crea una tarea ni una promesa, nunca entra en una revisión, nunca cuenta como nuevo y nunca va a tu Graph ni a tu equipo. Ningún modelo de IA lo lee.

Las tareas y promesas siguen saliendo solo de mensajes nuevos, como antes.

## Cuándo se ejecuta

Empieza cuando termina el primer vistazo a tus mensajes y avanza despacio en segundo plano. Espera mientras se ejecuta una revisión o una sincronización, y cuando tu Machine tiene poco espacio en disco o poca memoria. Tras un reinicio sigue donde estaba.

Usa el acceso que ya tiene cada conexión. No se pide nada nuevo.

## Hasta dónde

Cerca de un año por defecto. Las Machines autoalojadas pueden poner `history_days` en la configuración (0 lo apaga, hasta 730). Telegram, Slack y otras fuentes guardan lo que leen hoy.
