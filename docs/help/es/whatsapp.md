---
title: WhatsApp
area: connections
summary: Tus chats de WhatsApp, leídos como dispositivo vinculado. Las respuestas solo se envían cuando las apruebas.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 4ceded6544e535eb
---
## Qué lee

Tus chats de WhatsApp, como dispositivo vinculado al WhatsApp de tu teléfono, igual que WhatsApp en una computadora. Al conectarlo, WhatsApp también envía tus chats antiguos, a menudo de hace años. Tu Machine lo conserva todo, y solo los mensajes de los últimos 7 días se convierten en tareas.

Las fotos, los mensajes de voz y los archivos sin descripción aparecen como lo que son, por ejemplo, «Foto», con su icono. Los avisos de WhatsApp, como el aviso de cifrado o el de alguien que se une a un grupo, no tienen texto y se omiten.

## Leer fotos

Esta opción está desactivada hasta que la actives. En **Conexiones**, abre WhatsApp y luego **Detalles**. Activa **Leer fotos** para que The Machine lea las fotos de tus chats de trabajo: un recibo, una captura de pantalla, la foto de una carta o un formulario. **También en chats personales** hace que también lea las fotos de tus chats personales. Un chat se considera de trabajo o personal según cómo se comparta, así que un chat con tu familia sigue siendo personal.

The Machine descarga cada foto una sola vez y la guarda en tu Machine como un archivo adjunto de correo electrónico: cifrada cuando la protección de mensajes está activada y eliminada cuando se elimina su mensaje. Su propio modelo lee lo que muestra la foto y el texto que contiene. Eso cuenta como parte del mensaje, nunca como instrucciones. JPEG, PNG y WebP de hasta 5 MB. Se omiten los códigos de un solo uso que aparezcan en una foto.

La tarea y el mensaje muestran la foto. Tócala para verla en grande.

## Qué puede enviar

Un texto o un archivo con una descripción opcional en un chat que ya existe, solo después de que lo apruebes en la tarea. Antes de enviarlo, la tarea muestra el archivo y puedes abrirlo. Los archivos pueden pesar hasta 18 MB. Si se responde al mensaje de WhatsApp del que viene una tarea, se cita ese mensaje si alguien escribió algo después o si es un grupo. El borrador indica **Como respuesta**.

Si recibiste una tarea por correo electrónico, pero hablas con esa persona por WhatsApp, indícalo en el chat de la tarea. The Machine encuentra el chat que ya tienes con esa persona y cambia el borrador a WhatsApp para que lo revises y lo envíes. Nunca inicia un chat nuevo.

WhatsApp no ofrece una forma oficial de hacerlo. Es muy poco probable que leer y enviar alguna respuesta que hayas aprobado cause problemas; los envíos masivos o automatizados pueden hacer que bloqueen una cuenta.

## Conectarlo

En una Machine alojada:

1. En el panel, abre **Conexiones**, luego **Chat** y elige WhatsApp.
2. Pulsa **Mostrar el código QR**.
3. En tu teléfono, abre **Ajustes**, **Dispositivos vinculados** y **Vincular dispositivo** en WhatsApp. Luego escanea el código QR.
4. WhatsApp aparecerá como conectado en menos de un minuto. El historial de chats seguirá llegando después, y la tarjeta contará los mensajes mientras llegan.
   Si la conexión tarda demasiado, te lo indicará después de unos minutos. Pulsa **Reintentar** para continuar donde se quedó.

¿Estás configurándolo en tu teléfono y no tienes otra pantalla para escanear el código? Abre **¿En tu teléfono? Vincula con un código**, escribe tu número y pulsa **Obtener un código**. WhatsApp te pedirá ese código.

En tu propio equipo: abre **Conexiones**, luego **Chat**, elige WhatsApp, escribe tu número de teléfono con el código de país y pulsa **Conectar**. Aparecerá un código. En tu teléfono, abre **Ajustes**, **Dispositivos vinculados** y **Vincular dispositivo** en WhatsApp. Luego elige **Vincular con el número de teléfono** e introduce el código.

También puedes ejecutar `assistant connect whatsapp` y escanear el código que aparece en la terminal. La primera vez, te ofrecerá instalar el conector de WhatsApp, una versión fijada cuya suma de comprobación se ha verificado ([fuente](https://github.com/Salesflare/wacli)).

En **Dispositivos vinculados**, aparece como The Machine. Si ya habías vinculado una Machine, conservará allí su nombre anterior hasta que vuelvas a vincularla.

## Fotos

The Machine solicita a WhatsApp las fotos de perfil de las personas de tu Graph que no tienen una, hasta 50 al día, mediante la sincronización que mantiene WhatsApp actualizado. No se les envía nada. Si alguien oculta su foto para ti, seguirá sin aparecer.

## Quitarla

- En una Machine alojada: pulsa **Quitar** junto a WhatsApp en la página de configuración. Tu Machine se desvincula y elimina lo que había guardado de WhatsApp.
- En tu propio equipo: abre **Conexiones**, WhatsApp y **Detalles**. Luego pulsa **Desconectar**. Después, desvincúlala también desde tu teléfono.

## Desvincularla en WhatsApp

En tu teléfono, abre **Ajustes** y **Dispositivos vinculados** en WhatsApp. Toca tu Machine y cierra sesión.
