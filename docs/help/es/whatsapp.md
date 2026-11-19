---
title: WhatsApp
area: connections
summary: Tus chats de WhatsApp, leídos como dispositivo vinculado. Las respuestas solo se envían cuando las apruebas.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 9446d22f96229653
---
## Qué lee

Tus chats de WhatsApp, como dispositivo vinculado al WhatsApp de tu teléfono, igual que WhatsApp en una computadora. Al conectarlo, WhatsApp también envía tus chats antiguos, a veces de hace años. Tu Machine lo guarda todo, pero solo los mensajes de los últimos 7 días se convierten en tareas.

Las fotos, los mensajes de voz y los archivos sin descripción aparecen como lo que son, por ejemplo, «Foto», con su icono. Se omiten los avisos de WhatsApp, como el aviso sobre el cifrado o cuando alguien se une a un grupo, porque no tienen texto.

## Leer fotos

Esta opción está desactivada hasta que la actives. En **Conexiones**, abre WhatsApp y luego **Detalles**. Activa **Leer fotos** para que The Machine lea las fotos de tus chats de trabajo, como un recibo, una captura de pantalla o la foto de una carta o un formulario. **También en chats personales** también lee las fotos de tus chats personales. Los chats se consideran de trabajo o personales según cómo se comparten, así que un chat con tu familia sigue siendo personal.

The Machine descarga cada foto una sola vez y la guarda en tu Machine como un archivo adjunto de correo electrónico: cifrada cuando está activada la protección de mensajes y eliminada cuando se borra el mensaje. Su propio modelo lee lo que aparece en la foto y el texto que contiene. Eso cuenta como parte del mensaje, nunca como instrucciones. Se admiten archivos JPEG, PNG y WebP de hasta 5 MB. Se omiten los códigos de un solo uso que aparecen en una foto.

La tarea y el mensaje muestran la foto. Tócala para verla en grande.

## Qué puede enviar

Puede enviar un texto o un archivo con una descripción opcional a un chat que ya exista, pero solo después de que apruebes el envío en la tarea. Antes de enviarlo, la tarea muestra el archivo y puedes abrirlo. El archivo puede pesar hasta 18 MB. Si respondes al mensaje de WhatsApp del que surgió una tarea, se cita ese mensaje cuando alguien escribió después o cuando es un grupo. El borrador indica **Como respuesta**.

Si recibes una tarea por correo electrónico, pero hablas con esa persona por WhatsApp, díselo en el chat de la tarea. The Machine encuentra el chat que ya tienes con esa persona y cambia el borrador a WhatsApp para que lo revises y lo envíes. Nunca inicia un chat nuevo.

WhatsApp no ofrece una forma oficial de hacer esto. Leer mensajes y enviar de vez en cuando una respuesta que aprobaste tiene muy pocas probabilidades de causar problemas. El envío masivo o automatizado puede hacer que bloqueen una cuenta.

## Conectarlo

En una Machine alojada:

1. En el panel, abre **Conexiones**, luego **Chat** y elige WhatsApp.
2. Pulsa **Mostrar el código QR**.
3. En tu teléfono, abre Ajustes en WhatsApp, ve a Dispositivos vinculados y pulsa Vincular un dispositivo. Escanea el código QR.
4. WhatsApp aparecerá como conectado en menos de un minuto. Después, seguirá llegando el historial de tus chats y la tarjeta irá contando los mensajes mientras se sincronizan.
   Si la conexión tarda demasiado, aparecerá un aviso al cabo de unos minutos. Pulsa **Reintentar** para continuar desde donde se quedó.

¿Estás configurándolo en tu teléfono y no tienes otra pantalla desde la que escanear? Abre **¿En tu teléfono? Vincula con un código**, introduce tu número y pulsa **Obtener un código**. WhatsApp te pedirá ese código.

En tu propia computadora, abre **Conexiones**, luego **Chat**, elige WhatsApp, introduce tu número de teléfono con el código de país y pulsa **Conectar**. Aparecerá un código. En tu teléfono, abre Ajustes en WhatsApp, ve a Dispositivos vinculados y pulsa Vincular un dispositivo. Luego pulsa Vincular con el número de teléfono en su lugar e introduce el código.

También puedes ejecutar `assistant connect whatsapp` y escanear el código que aparece en la terminal. La primera vez, se ofrece instalar el conector de WhatsApp, una versión fijada y verificada con su suma de comprobación ([código fuente](https://github.com/Salesflare/wacli)).

En Dispositivos vinculados, aparece como The Machine. Si ya habías vinculado una Machine, conservará allí su nombre anterior hasta que vuelvas a vincularla.

Si WhatsApp cierra la sesión de tu Machine, la tarjeta mostrará **WhatsApp desvinculó esta Machine**. Pulsa **Reconectar** y vuelve a vincularla.

## Fotos de perfil

The Machine solicita a WhatsApp las fotos de perfil de las personas de tu Graph que no tienen una, hasta un máximo de 50 al día, mediante la sincronización que mantiene WhatsApp al día. No les envía nada. Si alguien te oculta su foto, seguirá sin aparecer.

## Quitar la conexión

- En una Machine alojada: pulsa **Quitar** junto a WhatsApp en la página de configuración. Tu Machine se desvinculará y borrará todo lo que haya guardado de WhatsApp.
- En tu propia computadora: abre **Conexiones**, selecciona WhatsApp, pulsa **Detalles** y luego **Desconectar**. Después, desvincúlala también desde tu teléfono.

## Desvincularla en WhatsApp

En tu teléfono, abre Ajustes en WhatsApp, ve a Dispositivos vinculados, toca tu Machine y cierra la sesión.
