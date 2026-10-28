---
title: WhatsApp
area: connections
summary: Tus chats de WhatsApp, leídos como dispositivo vinculado. Solo responde después de que lo apruebes.
covers: connector:whatsapp
code: onboarding.py, next_actions.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## Qué lee

Tus chats de WhatsApp, como dispositivo vinculado al WhatsApp de tu teléfono, igual que WhatsApp en un ordenador. Al conectar lee los últimos 7 días.

Una foto, un mensaje de voz o un archivo sin texto aparece como lo que es, por ejemplo "Imagen enviada". Los avisos propios de WhatsApp, como el aviso de cifrado o que alguien se une a un grupo, no tienen texto y se dejan fuera.

## Qué puede enviar

Un texto en un chat que ya existe, solo después de que lo apruebes en la tarea.

Si una tarea llegó por correo pero con esa persona hablas por WhatsApp, dilo en el chat de la tarea. The Machine encuentra tu chat con ella y pasa el borrador a WhatsApp, para que lo revises y lo envíes. Nunca empieza un chat nuevo.

## Conéctalo

En una Machine alojada:

1. En el panel, abre **Conexiones**, luego **+ Añadir**, y elige WhatsApp.
2. Pulsa **Mostrar el código QR**.
3. En tu teléfono, en WhatsApp, abre Ajustes, Dispositivos vinculados, Vincular un dispositivo, y escanea el código QR.

¿Lo configuras en el teléfono, sin una segunda pantalla desde la que escanear? Abre **¿En tu teléfono? Vincula con un código**, introduce tu número y pulsa **Obtener un código**. WhatsApp te pide entonces ese código.

En tu propio ordenador, ejecuta `assistant connect whatsapp` y escanea el código que muestra en el terminal. Sin wacli, ofrece instalar la versión fijada de [Salesflare/wacli](https://github.com/Salesflare/wacli), comprobada con su checksum.

## Fotos

The Machine pide a WhatsApp las fotos de perfil de las personas de tu Graph que no tienen, como mucho 50 al día, a través de la sincronización que mantiene WhatsApp al día. No se les envía nada. Alguien que te oculta su foto se queda sin ella.

## Quítalo

- En una Machine alojada: pulsa **Quitar** junto a él en tu página de configuración. Tu servidor se desvincula y elimina lo que guardaba para WhatsApp.
- En tu propio ordenador: **Conexiones**, abre WhatsApp, **Detalles** y luego **Desconectar**. Después desvincúlalo también en tu teléfono.

## Desvincúlalo en WhatsApp

En tu teléfono, en WhatsApp, abre Ajustes, Dispositivos vinculados, toca tu Machine y cierra la sesión.
