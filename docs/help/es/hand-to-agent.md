---
title: Pasar tareas a Claude Code o Codex
area: cards
summary: Envía una tarea de programación a Claude Code o Codex. El resultado aparece en la tarea.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 22e1b9b950988a58
---
## Pasar una tarea

1. En la tarea, abre **…**, luego **Pasar…** y elige **Codex** o **Claude Code**. Solo aparecen las herramientas que hayas configurado.
2. Revisa el resumen y lo que hará, añade una nota si quieres y pulsa **Pasar**. **Ver el trabajo completo** muestra el encargo entero.

La tarea muestra que está en marcha y, después, el resultado, con **Qué hizo** y **Ver cambios**. **Pedir cambios** le indica qué cambiar. **Pasar…**, en **…**, vuelve a empezar. **Ocultar** aparta el resultado. Si pasas una tarea atascada, muestra **Trabajando…** en lugar de **Atascada** mientras se ejecuta el trabajo.

Un trabajo nunca envía nada por ti. Si te deja un paso de publicación o despliegue, **Hazlo** en la tarea ejecuta ese paso. Las respuestas que redacta se quedan como borradores para que las envíes tú.

## En la app de Codex

- **Abrir en Codex** abre el hilo del trabajo en la app de Codex cuando termina.
- **Pedir cambios** continúa en esa misma conversación de Codex, y la tarea la sigue.
- Un trabajo se detiene tras 30 minutos sin avances o tras 6 horas en total. Reiniciarlo no lo detiene.

## Configurarlo

En **Ajustes**, **Modelo**, en **Codex y Claude Code**:

- **Codex**: dónde se ejecuta. En tu Machine o en tu ordenador no necesitas configurar nada más aquí. **Cambiar** abre la página de configuración.
- **Codex cloud**: su ID de entorno, que encontrarás en Codex, y, si quieres, una **Rama** desde la que empezar.
- **Claude Code**: el enlace de una sesión de Claude Code.

Claude devuelve el resultado a través del conector de The Machine. Añádelo una vez en claude.ai: Ajustes, Conectores, Añadir conector personalizado, con la dirección que aparece debajo de la sesión.

## Dónde se ejecuta Codex

En una Machine alojada, elige dónde se ejecuta en la página de configuración, en **Añadir más cuando quieras**, **Codex**:

- **En tu Machine** (la opción predeterminada): pulsa **Conectar Codex** e introduce el código que aparece en OpenAI. Usa el mismo plan de ChatGPT que tu modelo, y los trabajos se ejecutan en tu Machine. No hace falta usar el terminal. Si has iniciado sesión con la misma cuenta de ChatGPT, también permite que tu Machine vea y use los reinicios de tu límite de uso.
- **Otras opciones**, **En mi ordenador**: el trabajo se ejecuta en tu propio ordenador, con la sesión de Codex iniciada allí. La conexión está cifrada y solo funciona con ese ordenador. Instala The Machine allí, vincúlala desde la página de tu cuenta, ejecuta `codex login` y mantén The Machine en marcha. El resultado aparece en la tarea. Cuando el ordenador está apagado, los trabajos esperan.
- **Otras opciones**, **Codex cloud**: el trabajo se ejecuta en la nube de OpenAI. Pulsa **Conectar Codex**. Usa el mismo plan de ChatGPT que tu modelo, y OpenAI te pide otro código para Codex. Después, introduce el entorno de Codex cloud en Ajustes.

También puedes iniciar sesión desde el panel: **Conexiones**, **Proyectos y código**, **Codex**, **Recibir un código**. Una Machine autoalojada inicia esa misma sesión por sí sola.

En una Machine alojada, **Codex y Claude Code** aparece en Ajustes cuando conectas GitHub o Codex. Para desarrolladores: la [guía de agentes](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
