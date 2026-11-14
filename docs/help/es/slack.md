---
title: Slack
area: connections
summary: Los canales y mensajes directos en los que participas. Solo envía mensajes directos cuando los apruebas.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
translated: 23f9e98f4680d23c
---
## Qué lee

Las conversaciones en las que participas: canales, canales privados, mensajes directos y mensajes grupales. Lee los últimos 7 días al conectarla y, después, todo lo nuevo. Nunca se une a un canal ni abre una conversación por su cuenta. Lee un canal con poca actividad aproximadamente una vez al día. Si una tarea necesita los mensajes más recientes, The Machine los lee de inmediato.

Más adelante, llegan los mensajes de aproximadamente un año de antigüedad como [historial](history.md), poco a poco.

Las personas aparecen con su nombre y las aplicaciones, con el suyo, nunca con un ID de Slack. Si la cuenta de Slack de alguien ya no existe, aparece como antiguo usuario de Slack.

## Qué puede enviar

Un mensaje directo a una persona, en tu nombre y solo después de que lo apruebes en la tarea. Si la tarea viene de un mensaje de Slack, la respuesta se envía en el hilo de ese mensaje, ya sea en el mensaje directo o en el canal. El borrador indica **En el hilo**. Nunca inicia una publicación nueva en un canal.

## Qué conserva

Lo que lee permanece en tu Machine hasta que lo eliminas o eliminas la Machine. El servicio de alojamiento no guarda copias de tus mensajes ni tus datos de inicio de sesión de Slack, y ningún modelo de IA se entrena con tus mensajes de Slack. The Machine usa IA, que puede equivocarse, así que puedes revisar cada mensaje antes de que se envíe.

## Conectarla

1. Ve a **Conexiones**, **Chat**, **Slack** y luego **Iniciar sesión con Slack**. Después, permite el acceso en Slack. Si usas tu propio ordenador, primero vincúlala a tu cuenta en themachine.computer.
2. Primero llegan los mensajes nuevos y los mensajes directos. Slack permite que las aplicaciones lean aproximadamente una conversación por minuto, así que los mensajes antiguos pueden tardar unas horas en cargarse.

O usa una clave de API de Maton: inicia sesión en maton.ai, conecta Slack allí y copia tu clave de API de Maton desde Inicio. Luego, abre **O usa una clave de API de Maton** en Slack y pégala, o ejecuta `assistant connect slack` en tu propio ordenador. Una conexión de Slack hecha a través de Maton sigue funcionando como hasta ahora.

## Quitarla

- En el panel: ve a **Conexiones**, abre Slack, selecciona **Detalles** y luego **Desconectar**. Lo que ya se haya importado se conserva.
- En una Machine alojada, también puedes pulsar **Quitar** a su lado en la página de configuración.

## Desinstalarla en Slack

Si iniciaste sesión con Slack, abre la página Manage apps de tu espacio de trabajo en Slack y quita The Machine. Dejará de leer de inmediato y te pedirá que vuelvas a iniciar sesión. Lo que ya se haya importado se conserva. Si usas Maton, quita la conexión de Slack en Maton y elimina la clave de API de Maton que proporcionaste. Un administrador de Slack también puede quitar cualquiera de las dos aplicaciones del espacio de trabajo desde Manage apps.
