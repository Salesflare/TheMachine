---
title: WhatsApp
area: connections
summary: Tus chats de WhatsApp, leídos como dispositivo vinculado. Las respuestas solo se envían cuando las apruebas.
covers: connector:whatsapp
code: onboarding.py, whatsapp_setup.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 130c64388a71b7d1
---
## Qué lee

Tus chats de WhatsApp, como dispositivo vinculado al WhatsApp de tu teléfono, igual que WhatsApp en un ordenador. Al conectarlo, WhatsApp también envía tus chats antiguos, a menudo de hace años. Tu Machine lo conserva todo, pero solo los mensajes de los últimos 7 días se convierten en tareas.

Las fotos, los mensajes de voz y los archivos sin texto se muestran como lo que son, por ejemplo, «Foto», con su icono. Los avisos de WhatsApp, como el aviso de cifrado o cuando alguien se une a un grupo, no tienen texto y se omiten.

## Leer fotos

Esta opción está desactivada hasta que la actives. En **Conexiones**, abre WhatsApp y luego **Detalles**. Activa **Leer fotos** para que The Machine lea las fotos de tus chats de trabajo: un recibo, una captura de pantalla, una foto de una carta o un formulario. **También en chats personales** hace que también lea las de tus chats personales. Un chat se considera de trabajo o personal según cómo se comparta, así que un chat con tu familia sigue siendo personal.

The Machine descarga cada foto una vez y la conserva en tu Machine como un archivo adjunto de correo: cifrada cuando está activada la protección de mensajes y eliminada cuando se borra el mensaje. El modelo propio de The Machine lee lo que aparece en la foto y el texto que contiene. Eso se considera parte del mensaje, nunca instrucciones. Se admiten JPEG, PNG y WebP de hasta 5 MB. Se omiten los códigos de un solo uso que aparezcan en una foto.

La tarea y el mensaje muestran la foto. Tócala para verla en grande.

## Qué puede enviar

Un texto o un archivo con un texto opcional, a un chat que ya exista, y solo después de que lo apruebes en la tarea. Antes de enviarlo, la tarea muestra el archivo y puedes abrirlo. El archivo puede tener hasta 18 MB. Si se responde al mensaje de WhatsApp que originó una tarea y después de ese mensaje hubo más mensajes o se envió en un grupo, se incluye una cita del mensaje original. El borrador indica **Como respuesta**.

Si recibes una tarea por correo, pero hablas con esa persona por WhatsApp, díselo en el chat de la tarea. The Machine encuentra el chat que ya tienes con esa persona y cambia el borrador a WhatsApp para que lo revises y lo envíes. Nunca inicia un chat nuevo.

WhatsApp no ofrece una forma oficial de hacerlo. Leer mensajes y enviar de vez en cuando una respuesta que hayas aprobado es muy poco probable que cause problemas. Los envíos masivos o automatizados pueden hacer que bloqueen una cuenta.

## Conectarlo

En una Machine alojada:

1. En el panel, abre **Conexiones**, luego **Chat** y elige WhatsApp.
2. Pulsa **Mostrar el código QR**.
3. En tu teléfono, abre WhatsApp, ve a Configuración y luego a Dispositivos vinculados, pulsa Vincular un dispositivo y escanea el código QR.
4. WhatsApp aparecerá como conectado en menos de un minuto. Después, seguirá llegando tu historial de chats y la tarjeta irá contando los mensajes mientras se sincroniza.
   Si la conexión tarda demasiado, aparecerá un aviso al cabo de unos minutos. Pulsa **Reintentar** para continuar desde donde se quedó.

¿Estás configurándolo en tu teléfono y no tienes otra pantalla para escanear el código? Abre **¿En tu teléfono? Vincula con un código**, introduce tu número y pulsa **Obtener un código**. WhatsApp te pedirá ese código.

En tu propio ordenador: abre **Conexiones**, luego **Chat**, elige WhatsApp, introduce tu número de teléfono con el prefijo del país y pulsa **Conectar**. Aparecerá un código. En tu teléfono, abre WhatsApp, ve a Configuración y luego a Dispositivos vinculados, pulsa Vincular un dispositivo y después Vincular con número de teléfono. Introduce el código.

También puedes ejecutar `assistant connect whatsapp` y escanear el código que aparece en el terminal. La primera vez, se te ofrecerá instalar el conector de WhatsApp, una versión fijada cuya suma de comprobación se ha verificado ([código fuente](https://github.com/Salesflare/wacli)).

En Dispositivos vinculados, aparece como The Machine. Si ya habías vinculado una Machine, conservará allí su nombre anterior hasta que la vuelvas a vincular.

Si WhatsApp cierra la sesión de tu Machine, la tarjeta indicará **WhatsApp desvinculó esta Machine**. Pulsa **Reconectar** y vuelve a vincularla: introduce tu número de teléfono y luego el código que aparece en WhatsApp, en Dispositivos vinculados, en Vincular con número de teléfono. Se vinculará en el mismo lugar que antes, así que conservarás tus chats. Si configuraste tu propio servicio para mantener WhatsApp sincronizado, se pausará mientras la vinculas y se reanudará después.

Si WhatsApp tarda demasiado en responder, aparecerá un aviso durante la configuración. Pulsa **Reintentar** un minuto después para obtener un código nuevo.

## Fotos de perfil

The Machine pide a WhatsApp las fotos de perfil de las personas de tu Graph que no tienen una, hasta 50 al día, mediante la sincronización que mantiene WhatsApp al día. No se les envía nada. Si alguien te oculta su foto, seguirá sin aparecerte.

## Quitar la conexión

- En una Machine alojada: pulsa **Quitar** junto a ella en la página de configuración. Tu Machine se desvinculará y eliminará lo que haya guardado de WhatsApp.
- En tu propio ordenador: abre **Conexiones**, selecciona WhatsApp y pulsa **Detalles**. Luego, pulsa **Desconectar**. Desvincúlala también en tu teléfono.

## Desvincularla en WhatsApp

En tu teléfono, abre WhatsApp, ve a Configuración y luego a Dispositivos vinculados, toca tu Machine y cierra la sesión.
