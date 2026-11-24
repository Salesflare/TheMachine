---
title: Historial
area: connections
summary: Aproximadamente un año de correos, reuniones y mensajes antiguos de WhatsApp, Slack y Teams, para buscar, leer y conocer a tus contactos. Nunca genera tareas.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 2b5e84c61892c8e4
---
## Qué conserva

Tu Machine importa aproximadamente un año de correos, reuniones y mensajes antiguos de WhatsApp, Slack y Teams. Puedes encontrarlos con la búsqueda, también por significado; los hilos los muestran y el [Calendario](calendar.md) muestra las reuniones pasadas.

Cada conexión de **Conexiones** indica hasta dónde llega, por ejemplo, **Historial: desde** noviembre de 2025.

## Qué añade a tu Graph

Tu [Graph](graph.md) lo tiene en cuenta: lo cerca que estás de otras personas, cuándo hablaste con ellas por última vez, quién conoce a quién y quiénes son esas personas y organizaciones. También aparece en la cronología de cada persona u organización, para que siempre esté ahí su último contacto. Las respuestas de tu Fleet sobre quién conoce a alguien usan este historial de las cuentas de trabajo, con las mismas [reglas para compartir](sharing-rules.md) que se aplican al correo nuevo.

## Qué no hace nunca

Nunca crea tareas ni promesas, nunca cuenta como contenido nuevo, nunca inicia una comprobación ni se añade a un proyecto. El historial personal sigue siendo personal, igual que el correo personal.

Aparte de la búsqueda por significado, tu modelo de IA solo lo lee en estos tres casos:

- cuando aparece en los resultados de una búsqueda, por ejemplo, al hacer una pregunta o al trabajar en una tarea
- en correos con datos de reservas, para [viajes y eventos](calendar.md#trips-and-events)
- en la [preparación para tus reuniones](calendar.md#ready-for-your-meetings): notas de reuniones anteriores y algunos mensajes antiguos de las personas con las que te reúnes

## Cuándo se ejecuta

Empieza después de revisar tus mensajes por primera vez. Para cada conexión, espera a que haya pasado su primera semana; también lo hace con las conexiones que añades más adelante. Se ejecuta lentamente en segundo plano y se pausa mientras se ejecuta una comprobación o una sincronización, cuando un servicio le pide que vaya más despacio o cuando tu Machine se queda sin espacio. Los mensajes nuevos siempre tienen prioridad.

Cuando termina de importar el historial de un buzón, tu Machine vuelve a leer los correos que conserva para buscar datos de reservas y entradas. Así, las reservas antiguas también aparecen en [viajes y eventos](calendar.md#trips-and-events). Lo hace igual de despacio y se pausa por los mismos motivos.

Usa los permisos que ya tiene cada conexión. No tienes que aprobar nada nuevo.

## Hasta dónde llega

Aproximadamente un año. En tu propio ordenador, puedes cambiarlo con `history_days` en el archivo de configuración (0 lo desactiva y el máximo es 730). Telegram y otras fuentes no importan historial anterior.

Los mensajes de LinkedIn y X abarcan 90 días y se leen muy despacio: unas pocas consultas breves por hora, solo durante el día y, si el sitio limita el acceso, ninguna durante un día para proteger tu cuenta (`social_history_days`; 0 lo desactiva).
