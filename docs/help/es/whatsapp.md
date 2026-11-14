---
title: WhatsApp
area: connections
summary: Tus chats de WhatsApp, leídos como dispositivo vinculado. Solo responde después de que lo apruebes.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 881c555219a98f0f
---
## Qué lee

Tus chats de WhatsApp, como dispositivo vinculado al WhatsApp de tu teléfono, igual que WhatsApp en un ordenador. Al conectar, WhatsApp también envía tus chats antiguos, a menudo de años. Tu Machine lo guarda todo, y solo los mensajes de los últimos 7 días se convierten en tareas.

Una foto, un mensaje de voz o un archivo sin texto aparece como lo que es, por ejemplo "Foto", con su icono. Los avisos propios de WhatsApp, como el aviso de cifrado o que alguien se une a un grupo, no tienen texto y se dejan fuera.

## Leer fotos

Desactivado hasta que lo actives. En **Conexiones**, abre WhatsApp, luego **Detalles**, y activa **Leer fotos** y The Machine lee las fotos de tus chats de trabajo: un recibo, una captura, la foto de una carta o de un formulario. **También en chats personales** lee también las de tus chats personales. Un chat es de trabajo o personal según lo ve el uso compartido, así que un chat con la familia sigue siendo personal.

The Machine descarga cada foto una vez y la guarda en tu Machine como un adjunto de correo: cifrada cuando la protección de mensajes está activa, y borrada cuando su mensaje desaparece. Su propio modelo lee lo que muestra la foto y el texto que tiene. Eso cuenta como parte del mensaje, nunca como instrucciones. JPEG, PNG y WebP de hasta 5 MB. Un código de un solo uso en una foto se omite.

La tarea y el mensaje muestran la foto. Tócala para verla en grande.

## Qué puede enviar

Un texto en un chat que ya existe, solo después de que lo apruebes en la tarea. Una respuesta al mensaje de WhatsApp del que salió una tarea cita ese mensaje cuando se escribió más después, o en un grupo; el borrador dice **Como respuesta**.

Si una tarea llegó por correo pero con esa persona hablas por WhatsApp, dilo en el chat de la tarea. The Machine encuentra tu chat con ella y pasa el borrador a WhatsApp, para que lo revises y lo envíes. Nunca empieza un chat nuevo.

WhatsApp no ofrece una forma oficial de hacerlo. Leer y enviar de vez en cuando una respuesta que aprobaste casi nunca da problemas; enviar en masa o de forma automática puede hacer que bloqueen una cuenta.

## Conéctalo

En una Machine alojada:

1. En el panel, abre **Conexiones**, luego **Chat**, y elige WhatsApp.
2. Pulsa **Mostrar el código QR**.
3. En tu teléfono, en WhatsApp, abre Ajustes, Dispositivos vinculados, Vincular un dispositivo, y escanea el código QR.
4. WhatsApp aparece como conectado en menos de un minuto. Tu historial de chats sigue llegando después, y su tarjeta cuenta los mensajes mientras llegan.
   Si la conexión tarda demasiado, lo dice después de unos minutos. Pulsa **Reintentar** para seguir donde se quedó.

¿Lo configuras en el teléfono, sin una segunda pantalla desde la que escanear? Abre **¿En tu teléfono? Vincula con un código**, introduce tu número y pulsa **Obtener un código**. WhatsApp te pide entonces ese código.

En tu propio ordenador, ejecuta `assistant connect whatsapp` y escanea el código que muestra en el terminal. La primera vez, ofrece instalar el conector de WhatsApp, una versión fijada comprobada con su checksum ([código](https://github.com/Salesflare/wacli)).

En Dispositivos vinculados aparece como The Machine. Una Machine vinculada antes conserva allí su nombre anterior hasta que la vuelvas a vincular.

## Fotos

The Machine pide a WhatsApp las fotos de perfil de las personas de tu Graph que no tienen, como mucho 50 al día, a través de la sincronización que mantiene WhatsApp al día. No se les envía nada. Alguien que te oculta su foto se queda sin ella.

## Quítalo

- En una Machine alojada: pulsa **Quitar** junto a él en tu página de configuración. Tu Machine se desvincula y elimina lo que guardaba para WhatsApp.
- En tu propio ordenador: **Conexiones**, abre WhatsApp, **Detalles** y luego **Desconectar**. Después desvincúlalo también en tu teléfono.

## Desvincúlalo en WhatsApp

En tu teléfono, en WhatsApp, abre Ajustes, Dispositivos vinculados, toca tu Machine y cierra la sesión.
