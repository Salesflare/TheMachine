---
title: LinkedIn
area: connections
summary: Tus mensajes de LinkedIn, leídos en el navegador de tu Machine con tu sesión iniciada. Las respuestas solo se envían cuando las apruebas.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: bc67fbc21c77a97a
---
## Qué lee

Lee tus mensajes de LinkedIn en el navegador de tu Machine, con tu sesión iniciada, de vez en cuando durante el día. No marca nada como leído. También entran las respuestas en conversaciones que archivaste y las solicitudes de mensajes; el spam queda fuera.

## Cargos y empresas

También mantiene actualizados los cargos y las empresas de tus contactos de LinkedIn que ya están en tu Graph, a partir de tu lista de Conexiones. No abre sus perfiles ni añade personas nuevas. Cuando cambia el cargo o la empresa de alguien, su cronología lo indica, por ejemplo: «Ahora es Head of Sales en Acme; antes era Sales Lead en Acme».

El cargo se toma de su titular, como «Head of Sales en Acme» o «VP Sales and Strategy», nunca de un eslogan. Los encuentra por el enlace a su perfil o por su nombre y empresa. Si no hay una empresa con la que comparar, basta con que solo una persona de tu Graph tenga ese nombre completo. Su página también muestra desde cuándo estáis conectados.

Lee muy despacio: una página cada vez, con varios minutos entre una y otra, unas pocas decenas de páginas al día y solo durante el día. Unas 3.000 conexiones tardan unos cuatro días. Si LinkedIn pone trabas, se detiene hasta el día siguiente.

## Qué puede enviar

Puede responder a un mensaje o enviar uno nuevo a un perfil que indiques, pero solo después de que lo apruebes en la tarea. Hasta entonces, solo prepara borradores.

LinkedIn no ofrece una forma oficial de hacer esto. Es muy poco probable que leer y enviar de vez en cuando un mensaje que aprobaste cause problemas; el envío masivo o automatizado puede hacer que bloqueen la cuenta.

## Conectarlo

1. En el panel, abre **Conexiones**, luego **Chat** y elige LinkedIn.
2. Elige **Trabajo** (con su empresa) o **Personal** y pulsa **Conectar**.
3. Pulsa **Iniciar sesión en LinkedIn** e inicia sesión en el navegador de tu Machine. Se conecta automáticamente cuando hayas iniciado sesión.

En una Machine alojada, también puedes usar tu página de configuración en app.themachine.computer/setup: ve a **Más fuentes**, abre LinkedIn, inicia sesión cuando te lo pida y pulsa **Conectar**. En tu propio ordenador, `assistant connect linkedin` hace lo mismo desde un terminal.

Una segunda cuenta de LinkedIn tendrá su propio navegador. Si LinkedIn cierra la sesión de tu Machine, consulta [Se cerró la sesión en un sitio](signed-out.md).

## Si LinkedIn te pide un código

A menudo, LinkedIn envía un código por correo la primera vez que tu Machine inicia sesión. Escríbelo en el cuadro de inicio de sesión, en **Código**, y pulsa **Iniciar sesión**. La página no cambia mientras escribes.

Si LinkedIn vuelve al principio o no pasa nada durante dos minutos, espera un minuto y pulsa **Reintentar**. Si LinkedIn muestra una verificación para saber si eres un robot, complétala en el navegador de tu Machine.

## Quitar la conexión

- En el panel: abre **Conexiones**, selecciona LinkedIn y ve a **Detalles**. Luego pulsa **Desconectar**. Dejará de leer los mensajes. Lo que ya haya importado se conservará.
- En una Machine alojada, también puedes pulsar **Quitar** junto a LinkedIn en tu página de configuración.

## Cerrar la sesión en LinkedIn

En LinkedIn, abre Ajustes, Inicio de sesión y seguridad, Dónde has iniciado sesión y cierra la sesión correspondiente al navegador de tu Machine.
