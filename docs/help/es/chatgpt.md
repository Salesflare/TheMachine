---
title: ChatGPT
area: connections
summary: Inicia sesión con ChatGPT para que tu Machine funcione con tu plan de ChatGPT, e importa tus habilidades de ChatGPT.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
---
## Para qué sirve

ChatGPT es el modelo que lee y redacta por ti, con tu propio plan de ChatGPT. The Machine no tiene IA propia. Las peticiones de tu Machine van directamente a OpenAI, con tu cuenta y según sus condiciones.

## Inicia sesión

En una Machine alojada, en tu página de configuración, pulsa **Iniciar sesión con ChatGPT** y escribe en ChatGPT el código que muestra. ¿Se cerró la sesión más tarde? Pulsa **Reconectar ChatGPT**.

¿OpenAI rechaza el código? Abre tus [ajustes de seguridad de ChatGPT](https://chatgpt.com/settings/security), baja hasta el final y activa el interruptor "Enable device code sign-in for Codex, Excel, PowerPoint, and Word". Luego vuelve a introducir el código.

¿No está? En una cuenta de trabajo (Business, Enterprise o Edu), un administrador del espacio de trabajo lo activa en [Permissions & roles](https://chatgpt.com/admin/permissions), en "Codex and Work Local". Un solo interruptor vale para los dos códigos: si el código de tu modelo funcionó, el de Codex también funciona.

En tu propio ordenador, inicia la sesión de OpenClaw en ChatGPT con `openclaw models auth login`.

## Límites de uso

Un plan de ChatGPT tiene un límite de 5 horas y uno semanal. **Ajustes** y luego **Modelo** muestra cuánto se ha usado de cada uno y cuándo se reinicia. El trabajo en segundo plano se para bastante antes de un límite, para dejar margen a tus propios chats. Cuando se alcanza un límite, la parte superior del panel dice cuál y cuándo se reinicia, y el trabajo sigue después. Consulta [Modelo](model.md).

## Importa tus habilidades de ChatGPT

En **Ajustes**, **Habilidades**, pulsa **Importar**, elige **De ChatGPT** y pulsa **Buscar mis habilidades**. Lee las habilidades que creaste, en el navegador de tu Machine. Solo entran las instrucciones. Consulta [Habilidades](skills.md).

## Quítalo

Elige otro modelo en tu página de configuración, o inicia la sesión de OpenClaw con otro proveedor. Para terminar su acceso por parte de OpenAI, cierra la sesión en tus ajustes de seguridad de ChatGPT.
