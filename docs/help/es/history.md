---
title: Historial
area: connections
summary: Aproximadamente un año de correos antiguos, reuniones y mensajes de WhatsApp, Slack y Teams para buscar, leer y conocer a tu gente. Nunca crea tareas.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 93575cd78b3085f7
---
## Qué conserva

Tu Machine importa aproximadamente un año de correos antiguos, reuniones y mensajes de WhatsApp, Slack y Teams. Puedes encontrarlos con la búsqueda, también por significado. Los hilos los muestran y el [Calendario](calendar.md) muestra las reuniones pasadas.

En **Conexiones** puedes ver hasta dónde llega cada conexión, por ejemplo, **Historial: hasta** noviembre de 2025.

## Qué aporta a tu Graph

Tu [Graph](graph.md) tiene en cuenta estos datos: lo cerca que estás de las personas, cuándo hablaste con ellas por última vez, quién conoce a quién y quiénes son esas personas y organizaciones. También aparecen en la cronología de cada persona u organización, así que siempre puedes ver el último contacto. Las respuestas de tu Fleet a «quién conoce a alguien» usan estos datos de las cuentas de trabajo y siguen las mismas [reglas para compartir](sharing-rules.md) que los correos nuevos.

## Lo que nunca hace

Nunca crea tareas ni promesas, nunca cuenta como algo nuevo, nunca inicia una revisión ni se añade a un proyecto. El historial personal sigue siendo personal, igual que el correo personal. Salvo cuando se usa la búsqueda por significado, ningún modelo de IA lo lee.

## Cuándo se ejecuta

Empieza después de revisar tus mensajes por primera vez. Para cada conexión, solo cuando ya ha llegado su primera semana, también para una que añadas más adelante. Se ejecuta lentamente en segundo plano y se pausa mientras se ejecuta una revisión o una sincronización, cuando un servicio le pide que reduzca el ritmo o cuando tu Machine se queda sin espacio. Los mensajes nuevos siempre tienen prioridad.

Cuando termina de importar el historial de un buzón, tu Machine vuelve a leer los correos que conserva para detectar detalles de reservas y entradas. Así, las reservas antiguas también aparecen en [viajes y eventos](calendar.md#trips-and-events). Lo hace igual de despacio y se pausa por los mismos motivos.

Usa los permisos que ya tiene cada conexión. No tienes que aprobar nada nuevo.

## Hasta cuándo llega

Aproximadamente un año. En tu propio ordenador, `history_days` en el archivo de ajustes cambia este periodo (0 lo desactiva; el máximo es 730 días). Telegram y otras fuentes no importan el historial antiguo.

Los mensajes de LinkedIn y X llegan hasta 90 días atrás. Se leen muy lentamente: unas pocas lecturas pequeñas por hora, solo durante el día y, si el sitio pone límites, no se hacen lecturas durante un día para proteger tu cuenta (`social_history_days`; 0 lo desactiva).
