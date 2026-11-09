---
title: Historial
area: connections
summary: Cerca de un año de correos, reuniones y mensajes de WhatsApp, Slack y Teams antiguos, para buscar, leer y conocer a tu gente. Nunca una tarea.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
---
## Qué guarda

Cada cuenta de correo, calendario, WhatsApp, Slack y Teams guarda cerca de un año de mensajes y reuniones antiguos. La búsqueda los encuentra, también por significado, un hilo los muestra y el [Calendario](calendar.md) muestra las reuniones pasadas.

Su tarjeta dice hasta dónde llega: **Historial: hasta** un mes, cuando ya está.

## Qué aporta a tu Graph

Tu [Graph](graph.md) lo cuenta: qué tan cerca estás de cada persona, cuándo hablaron por última vez, quién conoce a quién, y las personas y organizaciones mismas. Las respuestas de tu Fleet a "quién conoce a alguien" lo usan desde cuentas de trabajo, con las mismas [reglas para compartir](sharing-rules.md) que el correo nuevo.

## Qué nunca hace

Nunca crea una tarea ni una promesa, nunca cuenta como nuevo, nunca inicia una revisión y nunca entra en un proyecto. El historial personal sigue siendo personal, como el correo personal. Aparte de la búsqueda por significado, ningún modelo de IA lo lee.

## Cuándo se ejecuta

Empieza cuando termina el primer vistazo a tus mensajes, y en cada conexión solo cuando ya está su primera semana, también en una que agregues después. Avanza despacio en segundo plano y espera mientras se ejecuta una revisión o una sincronización, cuando un servicio pide ir más lento o cuando tu Machine tiene poco espacio. Los mensajes nuevos siempre van primero.

Usa el acceso que ya tiene cada conexión. No se pide nada nuevo.

## Hasta dónde

Cerca de un año por defecto. Las Machines autoalojadas pueden poner `history_days` en la configuración (0 lo apaga, hasta 730). Telegram y otras fuentes guardan lo que leen hoy.
