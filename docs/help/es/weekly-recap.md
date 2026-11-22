---
title: Resumen semanal
area: weekly
summary: Una vez a la semana, descubre cómo le fue a tu Machine: tareas, promesas, personas y proyectos, y qué detectó. Está activado de forma predeterminada.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
translated: 223b143a6efd5692
---
## Qué incluye

- Requiere tu atención: promesas que te hicieron y ya vencieron, y promesas tuyas que ya vencieron o vencen en las próximas dos semanas.
- La próxima semana: tus reuniones (con un enlace cuando la preparación esté lista), las tareas que vencen y las promesas que otras personas hicieron para entonces.
- Qué cambió: cuántas tareas valieron la pena en comparación con la semana anterior, con qué frecuencia **Hazlo** acertó a la primera, qué ajustó en tu forma de escribir y en sus filtros, y cuántos borradores se enviaron tal como estaban escritos.
- Para el equipo de The Machine: aprendizajes para compartir, si hay alguno pendiente para ti. Consulta [Compartir aprendizajes con el equipo](share-learnings.md).
- Personas y proyectos: proyectos que cobran o pierden impulso, quién es nuevo y quién lleva tiempo sin actividad.
- Entre bastidores: cuántas señales revisó esta semana y cuántas siguen pendientes.
- En [Telegram](telegram.md), recibirás opciones para elegir, cada una en su propio mensaje: una fuente activa sin resultados (**Dejar de revisar** o **Seguir revisando**) y una tarea pospuesta más de una vez (**No hace falta**, **Hazlo** o **Mantener**). No cambia nada hasta que pulses una opción.

## Cuándo y dónde

Una vez a la semana, los viernes después de las 16:00 en tu zona horaria, de forma predeterminada. Lo recibirás por [Telegram](telegram.md) o como una notificación titulada «Tu semana» desde la [aplicación para teléfono](phone-app.md) y la aplicación del panel. También lo recibirás por correo si el correo está activado para **Resumen matutino** en Ajustes › Notificaciones. Si usas [Prudente](security-levels.md) o tienes desactivado **Texto en las notificaciones**, no lo recibirás por correo electrónico.

## Desactivarlo

Está activado de forma predeterminada. Desactívalo en Ajustes › Notificaciones con el interruptor **Resumen semanal**. Si lo desactivaste, seguirá desactivado. En tu propio ordenador, también puedes configurar `weekly_recap` en config.json: `enabled` false con `chosen` true, y, de forma opcional, `weekday` (del 1 al 7, viernes es 5) y `at` ("16:00"). Consulta la [guía de configuración](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
