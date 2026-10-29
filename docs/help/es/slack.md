---
title: Slack
area: connections
summary: Los canales y mensajes directos en los que estás. Envía un mensaje directo solo después de que lo apruebes.
covers: connector:slack
code: assistant.py, slack_api.py, next_actions.py, onboarding.py
site: Sign in with Slack, Connect, More sources, Remove
---
## Qué lee

Las conversaciones de las que eres miembro: canales, canales privados, mensajes directos y mensajes de grupo, los últimos 7 días al conectar y luego todo lo nuevo. Nunca se une a un canal ni abre una conversación por su cuenta.

## Qué puede enviar

Un mensaje directo a una persona, en tu nombre, y solo después de que lo apruebes en la tarea. Nunca publica en un canal.

## Conéctalo

Inicia sesión con Slack, la forma fácil:

1. En el panel: **Conexiones**, **+ Añadir**, Slack. O en la página de configuración de una Machine alojada en app.themachine.computer/setup: **Más fuentes**, Slack. En tu propio ordenador, vincúlalo antes con tu cuenta.
2. Pulsa **Iniciar sesión con Slack**. Slack pregunta qué espacio de trabajo y muestra lo que The Machine puede leer y enviar.
3. Pulsa **Allow**. Vuelves a donde empezaste y Slack queda conectado.

En algunos espacios de trabajo solo los administradores aprueban apps nuevas. Slack se lo pide primero a un administrador; cuando lo apruebe, vuelve a iniciar sesión.

O usa Maton:

1. Inicia sesión en maton.ai, conecta Slack allí y copia tu clave de API de Maton desde Home.
2. Abre Slack como arriba (o ejecuta `assistant connect slack`), abre **O usa una clave de API de Maton**, pega la clave y pulsa **Conectar**.

¿Ya conectaste Slack con Maton? Sigue funcionando. Conexiones muestra **Reconectar Slack**: púlsalo e inicia sesión con Slack para dejar de usar Maton. Lo que Slack ya trajo se queda.

## Quítalo

- En el panel: **Conexiones**, abre Slack, **Detalles** y luego **Desconectar**. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Desinstálalo en Slack

- Con inicio de sesión de Slack: en Slack, abre la página Manage apps de tu espacio de trabajo (o Ajustes, Apps), busca The Machine y quítala. Un administrador de Slack también puede quitarla para todo el espacio de trabajo.
- Con Maton: quita la conexión de Slack en Maton y borra la clave de API de Maton que diste.
