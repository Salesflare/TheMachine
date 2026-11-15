---
title: Historial
area: connections
summary: Cerca de un año de correos, reuniones y mensajes antiguos de WhatsApp, Slack y Teams, para buscar, leer y conocer a tu gente. Nunca crea tareas.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: c10fe5fb8d7b2d8b
---
## Qué conserva

Tu Machine incorpora cerca de un año de correos, reuniones y mensajes antiguos de WhatsApp, Slack y Teams. Puedes encontrarlos con la búsqueda, también por significado. Los hilos los muestran y el [Calendario](calendar.md) muestra las reuniones pasadas.

En **Conexiones**, cada conexión indica hasta dónde llega, por ejemplo, **Historial: desde** noviembre de 2025.

## Qué aporta a tu Graph

Tu [Graph](graph.md) cuenta con esta información para mostrar lo cerca que estás de otras personas, cuándo hablaste con ellas por última vez, quién conoce a quién y quiénes son esas personas y organizaciones. También aparece en la cronología de cada persona u organización, así que siempre puedes ver el último contacto. Las respuestas de tu Fleet a «quién conoce a quién» usan esta información de las cuentas de trabajo, con las mismas [reglas para compartir](sharing-rules.md) que el correo nuevo.

## Qué nunca hace

Nunca crea una tarea ni una promesa, nunca cuenta como algo nuevo, nunca inicia una revisión ni se añade a un proyecto. El historial personal sigue siendo personal, como el correo personal. Salvo para las búsquedas por significado, ningún modelo de IA lo lee.

## Cuándo se ejecuta

Empieza después de la primera revisión de tus mensajes. En cada conexión, solo empieza cuando ya ha pasado su primera semana, también en las que añadas más adelante. Se ejecuta despacio en segundo plano y se pausa mientras se ejecuta una revisión o una sincronización, cuando un servicio le pide que vaya más despacio o cuando tu Machine se queda sin espacio. Los mensajes nuevos siempre tienen prioridad.

Cuando ya ha incorporado el historial de un buzón, tu Machine vuelve a leer una vez el correo que conserva para detectar datos de reservas y entradas, así que las reservas antiguas también aparecen en [Viajes y eventos](notes.md). Lo hace igual de despacio y se pausa por los mismos motivos.

Usa los permisos que ya tiene cada conexión. No tienes que aprobar nada más.

## Hasta dónde llega

Cerca de un año. En tu propio ordenador, `history_days` en el archivo de ajustes cambia el periodo (0 lo desactiva, hasta 730 días). Telegram y otras fuentes no incorporan el historial antiguo.

Los mensajes de LinkedIn y X se remontan a 90 días y se consultan muy despacio: unas pocas consultas pequeñas por hora, solo durante el día y ninguna durante un día si el sitio pone límites, para mantener tu cuenta segura (`social_history_days`, 0 lo desactiva).
