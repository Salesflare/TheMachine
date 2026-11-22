---
title: Pasar a Claude Code o Codex
area: cards
summary: Envía una tarea de programación a Claude Code o Codex. El resultado vuelve a la tarea.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 333d553e80aea529
---
## Pasa una tarea

1. En la tarea, abre **…**, luego **Pasar…**, y elige **Codex** o **Claude Code**. Solo aparecen las herramientas que has configurado.
2. Revisa el resumen y lo que recibe, añade una nota si quieres y pulsa **Pasar**. **Ver el trabajo completo** muestra todo el encargo.

La tarea muestra que está trabajando y luego el resultado, con **Qué hizo** y **Ver cambios**. **Pedir cambios** le envía qué cambiar. **Pasar…** en **…** empieza de cero. **Ocultar** guarda el resultado. Una tarea atascada que pasas muestra **Trabajando…** en lugar de **Atascada** mientras el trabajo sigue.

Un trabajo nunca envía nada por ti. Si te deja un paso de publicar o desplegar, **Hazlo** en la tarea ejecuta ese paso. Una respuesta que escribió queda como borrador que envías tú.

## En la app de Codex

- **Abrir en Codex** abre el hilo del trabajo en la app de Codex, una vez terminado el trabajo.
- **Pedir cambios** sigue en esa misma conversación de Codex, y la tarea la sigue.
- Un trabajo se detiene tras 30 minutos sin avanzar, o tras 6 horas en total. Un reinicio no lo detiene.

## Configúralo

En **Ajustes**, **Modelo**, en **Codex y Claude Code**:

- **Codex**: dónde se ejecuta. En tu Machine o tu ordenador no necesita nada más aquí; **Cambiar** abre tu página de configuración.
- **Codex cloud**: el ID de su entorno, de Codex, y si quieres una **Rama** desde la que empezar.
- **Claude Code**: el enlace de una sesión de Claude Code.

Claude devuelve su resultado a través del conector de The Machine. Añádelo una vez en claude.ai, Settings, Connectors, Add custom connector, con la dirección que se muestra debajo de la sesión.

## Dónde se ejecuta Codex

En una Machine alojada, elígelo en tu página de configuración, en **Añade más cuando quieras**, **Codex**:

- **En tu Machine** (por defecto): pulsa **Conectar Codex** e introduce en OpenAI el código que aparece. Usa el mismo plan de ChatGPT que tu modelo, y los trabajos se ejecutan en tu Machine. Sin terminal.
- **Otras formas**, **En mi ordenador**: el trabajo se ejecuta en tu propio ordenador, con el Codex que tiene la sesión iniciada allí. Viaja cifrado, solo para ese ordenador. Instala allí The Machine, vincúlalo en tu página Cuenta, ejecuta `codex login` y mantén The Machine en marcha. El resultado vuelve a la tarea. Cuando el ordenador está apagado, los trabajos esperan.
- **Otras formas**, **Codex cloud**: el trabajo se ejecuta en la nube de OpenAI. Pulsa **Conectar Codex**. Usa el mismo plan de ChatGPT que tu modelo, y OpenAI pide un código más, para Codex. Luego introduce el entorno de Codex cloud en Ajustes.

O inicia sesión desde tu panel: **Conexiones**, **Proyectos y código**, **Codex**, **Recibir un código**. Una Machine autoalojada hace ese mismo inicio de sesión ella misma.

En una Machine alojada, **Codex y Claude Code** aparece en Ajustes en cuanto GitHub o Codex está conectado. Para desarrolladores: la [guía de agentes](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
