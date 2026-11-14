---
title: Slack
area: connections
summary: Los canales y mensajes directos en los que estás. Envía un mensaje directo solo después de que lo apruebes.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
translated: 8d275e75083292ba
---
## Qué lee

Las conversaciones de las que eres miembro: canales, canales privados, mensajes directos y mensajes de grupo, los últimos 7 días al conectar y luego todo lo nuevo. Nunca se une a un canal ni abre una conversación por su cuenta. Un canal tranquilo se lee una vez al día más o menos; cuando una tarea necesita sus mensajes más nuevos, The Machine lo lee enseguida.

Cerca de un año de mensajes antiguos llega después, poco a poco, como [historial](history.md).

Las personas aparecen con su nombre y las apps con el suyo, nunca con un ID de Slack. Alguien cuya cuenta de Slack ya no existe aparece como antiguo usuario de Slack.

## Qué puede enviar

Un mensaje directo a una persona, en tu nombre, y solo después de que lo apruebes en la tarea. Una respuesta al mensaje de Slack del que salió una tarea va en el hilo de ese mensaje, en el mensaje directo o en el canal; el borrador dice **En el hilo**. Nunca empieza una publicación nueva en un canal.

## Conéctalo

1. **Conexiones**, **Chat**, **Slack**, luego **Iniciar sesión con Slack**, y permítelo en Slack. En tu propio ordenador, vincúlalo primero con tu cuenta en themachine.computer.
2. Los mensajes nuevos y los mensajes directos llegan primero. Slack deja que las apps lean más o menos una conversación por minuto, así que los mensajes anteriores llegan a lo largo de unas horas.

O usa una clave de API de Maton: inicia sesión en maton.ai, conecta Slack allí y copia tu clave de API de Maton desde Home. Luego abre **O usa una clave de API de Maton** debajo de Slack y pégala, o ejecuta `assistant connect slack` en tu propio ordenador. Un Slack conectado a través de Maton sigue funcionando como está.

## Quítalo

- En el panel: **Conexiones**, abre Slack, **Detalles** y luego **Desconectar**. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Desinstálalo en Slack

Con inicio de sesión de Slack: abre la página Manage apps de tu espacio de trabajo en Slack y quita The Machine. A través de Maton: quita la conexión de Slack en Maton y elimina la clave de API de Maton que diste. Un administrador de Slack también puede quitar cualquiera de las dos apps del espacio de trabajo, en Manage apps.
