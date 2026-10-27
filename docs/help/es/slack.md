---
title: Slack
area: connections
summary: Los canales y mensajes directos en los que estás. Envía un mensaje directo solo después de que lo apruebes.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py
site: Connect, More sources, Remove
---
## Qué lee

Las conversaciones de las que eres miembro: canales, canales privados, mensajes directos y mensajes de grupo, los últimos 7 días al conectar y luego todo lo nuevo. Nunca se une a un canal ni abre una conversación por su cuenta.

## Qué puede enviar

Un mensaje directo a una persona, en tu nombre, y solo después de que lo apruebes en la tarea. Nunca publica en un canal.

## Conéctalo

Slack se lee a través de Maton, que guarda el inicio de sesión de Slack.

1. Inicia sesión en maton.ai, conecta Slack allí y copia tu clave de API de Maton desde Home.
2. En una Machine alojada: abre tu página de configuración en app.themachine.computer/setup, ve a **Más fuentes**, abre Slack, pega la clave y pulsa **Conectar**.
3. En tu propio ordenador: ejecuta `assistant connect slack`, o **Conexiones**, **+ Añadir**, Slack.

## Quítalo

- En el panel: **Conexiones**, abre Slack, **Detalles** y luego **Desconectar**. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Desinstálalo en Slack

Quita la conexión de Slack en Maton y elimina la clave de API de Maton que diste. Un administrador de Slack también puede quitar la app del espacio de trabajo, en Manage apps.
