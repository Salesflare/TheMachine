---
title: WhatsApp
area: connections
summary: Tus chats de WhatsApp, leídos desde un dispositivo vinculado. Las respuestas solo se envían cuando las apruebas.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 881c555219a98f0f
---
## Qué lee

Tus chats de WhatsApp, como si WhatsApp de tu teléfono estuviera vinculado a otro dispositivo, igual que WhatsApp en una computadora. Al conectarlo, WhatsApp también envía tus chats antiguos, a menudo de varios años. Tu Machine conserva todo, pero solo los mensajes de los últimos 7 días se convierten en tareas.

Las fotos, los mensajes de voz y los archivos sin texto aparecen como lo que son, por ejemplo, «Foto», con su icono. Se omiten los avisos de WhatsApp que no tienen texto, como el aviso de cifrado o cuando alguien se une a un grupo.

## Leer fotos

Esta opción está desactivada hasta que la actives. En **Conexiones**, abre WhatsApp y luego **Detalles**. Activa **Leer fotos** para que The Machine lea las fotos de tus chats de trabajo: un recibo, una captura de pantalla, la foto de una carta o de un formulario. **También en chats personales** permite leer también las fotos de tus chats personales. Los chats se consideran de trabajo o personales según cómo se comparten, así que un chat con tu familia sigue siendo personal.

The Machine descarga cada foto una sola vez y la guarda en tu Machine como si fuera un archivo adjunto de correo: cifrada cuando la protección de mensajes está activada y eliminada cuando se borra su mensaje. El modelo de The Machine lee lo que aparece en la foto y el texto que contiene. Eso se considera parte del mensaje, nunca instrucciones. Se admiten archivos JPEG, PNG y WebP de hasta 5 MB. Se omiten los códigos de un solo uso que aparezcan en una foto.

La tarea y el mensaje muestran la foto. Tócala para verla en tamaño grande.

## Qué puede enviar

Puede enviar un texto a un chat que ya exista, pero solo después de que lo apruebes en la tarea. Si una tarea viene de un mensaje de WhatsApp, la respuesta cita ese mensaje cuando alguien respondió después o cuando se trata de un grupo. El borrador indica **Como respuesta**.

Si una tarea llegó por correo electrónico, pero hablas con esa persona por WhatsApp, dilo en el chat de la tarea. The Machine encuentra el chat que ya tienes con esa persona y cambia el borrador a WhatsApp para que lo revises y lo envíes. Nunca inicia un chat nuevo.

WhatsApp no ofrece una forma oficial de hacerlo. Es muy poco probable que leer mensajes y enviar alguna respuesta que hayas aprobado cause problemas; los envíos masivos o automatizados pueden hacer que bloqueen una cuenta.

## Conectarlo

En una Machine alojada:

1. En el panel, abre **Conexiones**, luego **Chat** y elige WhatsApp.
2. Pulsa **Mostrar el código QR**.
3. En tu teléfono, abre WhatsApp, ve a Ajustes, Dispositivos vinculados, Vincular un dispositivo y escanea el código QR.
4. WhatsApp aparecerá como conectado en menos de un minuto. Después, seguirá llegando tu historial de chats, y la tarjeta irá contando los mensajes mientras tanto.
   Si la conexión tarda demasiado, aparecerá un aviso al cabo de unos minutos. Pulsa **Reintentar** para continuar donde se quedó.

¿Estás configurándolo en tu teléfono y no tienes otra pantalla para escanear el código? Abre **¿En tu teléfono? Vincula con un código**, introduce tu número y pulsa **Obtener un código**. WhatsApp te pedirá ese código.

En tu propia computadora: abre **Conexiones**, luego **Chat**, elige WhatsApp, introduce tu número de teléfono con el código de país y pulsa **Conectar**. Aparecerá un código. En tu teléfono, abre WhatsApp, ve a Ajustes, Dispositivos vinculados, Vincular un dispositivo, luego **Vincular con el número de teléfono** e introduce el código.

O ejecuta `assistant connect whatsapp` y escanea el código que aparece en la terminal. La primera vez, se te ofrecerá instalar el conector de WhatsApp, una versión fijada cuya suma de comprobación se ha verificado ([código fuente](https://github.com/Salesflare/wacli)).

En Dispositivos vinculados, aparecerá como The Machine. Si ya habías vinculado una Machine, conservará el nombre anterior hasta que la vuelvas a vincular.

## Fotos de perfil

The Machine solicita a WhatsApp las fotos de perfil de las personas de tu Graph que no tienen una, hasta un máximo de 50 al día, mediante la sincronización que mantiene WhatsApp actualizado. No se les envía nada. Si alguien oculta su foto, seguirá sin aparecerte.

## Quitarla

- En una Machine alojada: pulsa **Quitar** junto a ella en la página de configuración. Tu Machine se desvinculará y eliminará todo lo que guardó de WhatsApp.
- En tu propia computadora: abre WhatsApp en **Conexiones**, pulsa **Detalles** y luego **Desconectar**. Después, desvincúlala también en tu teléfono.

## Desvincularla en WhatsApp

En tu teléfono, abre WhatsApp, ve a Ajustes, Dispositivos vinculados, toca tu Machine y cierra sesión.
