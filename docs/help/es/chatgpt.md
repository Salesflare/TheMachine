---
title: ChatGPT
area: connections
summary: Inicia sesión con ChatGPT para usar tu Machine con tu plan de ChatGPT e importar tus habilidades de ChatGPT.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
translated: fc97be60c0b68336
---
## Para qué sirve

Inicia sesión con ChatGPT y tu Machine leerá y redactará con ChatGPT usando tu propio plan. The Machine no tiene una IA propia: las solicitudes van directamente a OpenAI, con tu cuenta y según sus condiciones.

## Iniciar sesión

En una Machine alojada, pulsa **Iniciar sesión con ChatGPT** en la página de configuración e introduce en ChatGPT el código que aparece. ¿Se cierra tu sesión más adelante? Pulsa **Volver a conectar ChatGPT**.

¿OpenAI rechaza el código? Abre tus [ajustes de seguridad de ChatGPT](https://chatgpt.com/settings/security), desplázate hasta el final y activa la opción «**Habilitar el inicio de sesión con código de dispositivo para Codex, Excel, PowerPoint y Word**». Después, vuelve a introducir el código.

¿No ves esa opción? Si usas una cuenta de trabajo (Business, Enterprise o Edu), el administrador de ChatGPT puede activarla en [Permisos y roles](https://chatgpt.com/admin/permissions), en «**Codex y Work Local**».

En tu propio ordenador, ejecuta `openclaw models auth login` en una terminal.

## Límites de uso

Los planes de ChatGPT tienen un límite de 5 horas y otro semanal. En **Ajustes**, **Modelo** puedes ver cuánto has usado de cada uno y cuándo se restablece. El trabajo en segundo plano se pausa bastante antes de alcanzar un límite para dejar espacio para tus chats. Cuando alcanzas un límite, la parte superior del panel indica cuándo se restablece. Consulta [Modelo](model.md).

## Importar tus habilidades de ChatGPT

En **Ajustes**, **Habilidades**, pulsa **Importar**, elige **De ChatGPT** y pulsa **Buscar mis habilidades**. Solo se importan las instrucciones. Consulta [Habilidades](skills.md).

## Desconectar ChatGPT

Elige otro modelo en la página de configuración (o, si usas tu propio ordenador, inicia sesión con otro proveedor de la misma manera). Para revocar el acceso desde OpenAI, cierra la sesión en tus ajustes de seguridad de ChatGPT.
