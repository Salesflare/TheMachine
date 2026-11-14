---
title: LinkedIn
area: connections
summary: Tus mensajes de LinkedIn, leídos en el navegador de tu Machine con tu sesión iniciada. Solo responde cuando lo apruebas.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: 850b91f79b9e23fc
---
## Qué lee

Tus mensajes de LinkedIn. Los lee de vez en cuando, durante las horas en que estás despierto, en el navegador de tu Machine con tu sesión iniciada. No marca nada como leído. También incluye las respuestas de conversaciones que archivaste y las solicitudes de mensajes; el spam queda fuera.

## Cargos y empresas

También mantiene actualizados los cargos y las empresas de tus contactos de LinkedIn que ya están en tu Graph, a partir de tu lista de Conexiones. No abre sus perfiles ni añade a nuevas personas. Cuando cambia el cargo o la empresa de alguien, lo indica en su cronología, por ejemplo: «Ahora es Head of Sales en Acme; antes era Sales Lead en Acme».

El cargo se obtiene de su titular, por ejemplo, «Head of Sales en Acme» o «VP Sales and Strategy», nunca de un eslogan. Busca a la persona mediante el enlace a su perfil o por su nombre y empresa. Si no hay una empresa con la que comparar, basta con que solo una persona de tu Graph tenga ese nombre completo. Su página también indica desde cuándo estáis conectados.

Lee muy despacio: una página cada vez, con varios minutos de intervalo, unas pocas docenas de páginas al día y solo durante el día. Para unas 3.000 conexiones tarda alrededor de cuatro días. Si LinkedIn pone trabas, se detiene hasta el día siguiente.

## Qué puede enviar

Una respuesta a un mensaje o un mensaje nuevo a un perfil que indiques, y solo cuando lo apruebes en la tarea. Hasta entonces, solo prepara borradores.

LinkedIn no ofrece una forma oficial de hacerlo. Es muy poco probable que leer mensajes y enviar de vez en cuando uno que hayas aprobado cause problemas; el envío masivo o automatizado puede hacer que bloqueen una cuenta.

## Conectarlo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre LinkedIn e inicia sesión en LinkedIn desde el navegador de tu Machine cuando te lo pida. Luego, pulsa **Conectar**.

En tu propio ordenador:

1. En el panel, abre **Conexiones**, luego **Chat** y elige LinkedIn.
2. Elige **Trabajo** (con su empresa) o **Personal**, y pulsa **Conectar**.
3. Pulsa **Iniciar sesión en LinkedIn** e inicia sesión en el navegador de tu Machine. Se conectará automáticamente cuando hayas iniciado sesión.

O ejecuta `assistant connect linkedin`.

Una segunda cuenta de LinkedIn tendrá su propio navegador. Si LinkedIn cierra la sesión de tu Machine, consulta [Se cerró tu sesión en un sitio](signed-out.md).

## Si LinkedIn te pide un código

La primera vez que tu Machine inicia sesión, LinkedIn suele enviarte un código por correo electrónico. Escríbelo en el cuadro de inicio de sesión, en **Código**, y pulsa **Iniciar sesión**. La página no cambia mientras escribes.

Si LinkedIn vuelve al principio o no pasa nada durante dos minutos, espera un minuto y pulsa **Reintentar**. Si LinkedIn muestra una verificación para robots, complétala en el navegador de tu Machine.

## Quitar la conexión

- En el panel: abre **Conexiones**, selecciona LinkedIn, pulsa **Detalles** y luego **Desconectar**. Dejará de leer los mensajes. Lo que ya haya importado se conservará.
- Si tienes una Machine alojada, también puedes pulsar **Quitar** junto a LinkedIn en tu página de configuración.

## Cerrar la sesión en LinkedIn

En LinkedIn, abre Ajustes, Inicio de sesión y seguridad, Dónde has iniciado sesión, y cierra la sesión del navegador de tu Machine.
