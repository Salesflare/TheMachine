---
title: Notificaciones de Android
area: connections
summary: Las notificaciones de tu teléfono Android, a través de la app OpenClaw. Solo lee.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, More sources, Remove
---
## Qué lee

Las notificaciones que llegan a tu teléfono Android, a través de la app OpenClaw. Se dejan fuera los códigos de un solo uso, y también las notificaciones de WhatsApp, Telegram, Signal y Discord.

## Qué puede hacer

Nada en tu teléfono. Solo lee notificaciones.

## Conéctalo

En una Machine alojada:

1. Instala la app OpenClaw en tu teléfono.
2. En tu página de configuración, ve a **Más fuentes**, abre Notificaciones de Android y pulsa **Mostrar un código de configuración**.
3. Escanéalo en la app OpenClaw y luego pulsa **Aprobar** para la vinculación.
4. En la app OpenClaw, activa Forward Notification Events y permite el acceso a las notificaciones cuando Android lo pida.

En tu propio ordenador, vincula el teléfono con tu OpenClaw Gateway y luego ejecuta `assistant connect android`.

## Quítalo

- En el panel: **Conexiones**, abre Android, **Detalles** y luego **Desconectar**.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Quítalo en el teléfono

Desactiva el acceso a las notificaciones de la app OpenClaw en los ajustes de Android, o desvincula el teléfono en la app OpenClaw.
