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

## En la app de Codex

- **Abrir en Codex** abre el hilo del trabajo en la app de Codex. Mientras Codex trabaja en él aquí, la app todavía no puede abrirlo. Se abre cuando termina.
- **Cambiar** en un hilo abierto en la app de Codex sigue en esa misma conversación allí, y la tarea la sigue.
- Un trabajo solo se detiene si Codex no hace nada durante 30 minutos, o tras 6 horas en total. Un reinicio de The Machine no lo detiene.

## Configúralo

En **Ajustes**, **Modelo**, en **Codex y Claude Code**:

- **Codex**: dónde se ejecuta. En tu ordenador no necesita nada más aquí; **Cambiar** abre tu página de configuración.
- **Codex cloud**: el ID de su entorno, de Codex, y si quieres una **Rama** desde la que empezar.
- **Claude Code**: el enlace de una sesión de Claude Code.

Claude devuelve su resultado a través del conector de The Machine. Añádelo una vez en claude.ai, Settings, Connectors, Add custom connector, con la dirección que se muestra debajo de la sesión.

## Dónde se ejecuta Codex

En una Machine alojada, elígelo en tu página de configuración, en **Añade más cuando quieras**, **Codex**:

- **En mi ordenador** (por defecto): el trabajo se ejecuta en tu propio ordenador, con el Codex que tiene la sesión iniciada allí. Nada de Codex está en tu servidor, y el trabajo va cifrado solo para ese ordenador: la Network lo pasa pero no puede leerlo. Instala The Machine en ese ordenador, vincúlalo en tu página Cuenta y ejecuta `codex login` allí. Mantén The Machine en marcha en él. El trabajo aparece como un hilo en la app de Codex de ese ordenador, y el resultado vuelve a la tarea. Cuando el ordenador está apagado, los trabajos esperan hasta que vuelva.
- **Codex cloud**: el trabajo se ejecuta en la nube de OpenAI. Pulsa **Conectar Codex**. Usa el mismo plan de ChatGPT que tu modelo, y OpenAI pide un código más, para Codex. Luego introduce el entorno de Codex cloud en Ajustes.

En una Machine alojada, Codex y Claude Code aparece en cuanto GitHub o Codex está conectado. También aparece en configuraciones que ejecutan trabajos en otro sitio. Más en la [guía de agentes](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
