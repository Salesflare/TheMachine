---
title: Resumen semanal
area: weekly
summary: Una vez por semana, cómo le fue a tu Machine: tareas, promesas, personas y proyectos, y lo que notó. Activado por defecto.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
---
## Qué incluye

- Tu semana con The Machine, y cuántas tareas valieron la pena, comparado con la semana anterior.
- Tareas: nuevas, hechas, descartadas y pospuestas, y lo rápido que respondiste.
- Promesas: las tuyas cumplidas y abiertas, las de otros que se cumplieron o siguen pendientes.
- Aprendizajes para compartir con el equipo de The Machine, si hay alguno esperándote. Consulta [Comparte aprendizajes con el equipo](share-learnings.md).
- Personas y proyectos, como quién se ha quedado en silencio.
- Lo que noté: borradores enviados tal cual o editados, tareas descartadas en pocos minutos, tareas pospuestas más de una vez.
- Entre bastidores: cuántas señales revisó esta semana y cuántas siguen en espera.
- Opciones, cada una en su propio mensaje después del resumen: una fuente con mucha actividad sin resultados (**Dejar de revisar** o **Seguir revisando**) y una tarea pospuesta más de una vez (**No hace falta**, **Hazlo** o **Mantener**). No cambia nada hasta que toques.

## Cuándo y dónde

Una vez por semana, por defecto el viernes después de las 16:00 en tu zona horaria. Llega por [Telegram](telegram.md), o como una notificación titulada "Tu semana" desde la [app del teléfono](phone-app.md) y la app del panel. También llega por correo cuando el correo está activado para **Resumen matutino** en Ajustes › Notificaciones. Con [Prudente](security-levels.md) no llega por correo.

## Desactívalo

Está activado por defecto. Desactívalo en Ajustes › Notificaciones con el interruptor **Resumen semanal**. Si lo desactivaste, sigue desactivado. En tu propio ordenador también puedes configurar `weekly_recap` en el config.json: `enabled` en false con `chosen` en true y, si quieres, `weekday` (de 1 a 7, el viernes es 5) y `at` ("16:00"). Consulta la [guía de configuración](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
