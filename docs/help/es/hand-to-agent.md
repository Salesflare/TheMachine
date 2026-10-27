---
title: Pasar a Claude Code o Codex
area: cards
summary: Envía una tarea de programación a Claude Code o Codex. El resultado vuelve a la tarea.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time
order: 5
---
## Pasa una tarea

1. En la tarea, abre **Más** y elige **Pasar a Codex** o **Pasar a Claude Code**. Aparece cuando esa herramienta está configurada.
2. Revisa el resumen y lo que recibe, añade una nota si quieres y pulsa **Pasar**. **Ver el trabajo completo** muestra todo el encargo.

Luego la tarea muestra que está trabajando, y el resultado cuando termina, con **Mostrar cambios**. **Cambiar** le pide cambios; **Pasar de nuevo** empieza de cero.

Un trabajo nunca envía nada por ti.

## Configúralo

En **Ajustes**, **General**, en **Agentes de código**:

- **Sesión de Claude Code**: la dirección de una sesión de Claude Code.
- **Entorno en la nube de Codex**: el id de su entorno.
- **Se ejecuta en** y, si quieres, una **Rama**.

Claude devuelve su resultado a través del conector de The Machine. Añádelo una vez en claude.ai, Settings, Connectors, Add custom connector, con la dirección que se muestra ahí. Para Codex en una Machine alojada, pulsa primero **Conectar Codex** en tu página de configuración, en **Añade más cuando quieras**. Usa el mismo plan de ChatGPT que tu modelo, y OpenAI pide un código más, para Codex.

En una Machine alojada, Agentes de código aparece en cuanto GitHub o Codex está conectado. También aparece en configuraciones que ejecutan trabajos en otro sitio. Más en la [guía de agentes](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
