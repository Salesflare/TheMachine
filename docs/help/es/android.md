---
title: Notificaciones de Android
area: connections
summary: Las notificaciones de tu teléfono Android, a través de la app OpenClaw. Solo las lee.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 5b08b093662393a1
---
## Qué lee

Las notificaciones de tu teléfono Android, a través de la app OpenClaw. No incluye códigos de un solo uso ni notificaciones de WhatsApp, Telegram, Signal o Discord.

## Qué puede hacer

Nada en tu teléfono. Solo lee las notificaciones.

## Cómo conectarla

En una Machine alojada:

1. Instala OpenClaw desde Google Play en tu teléfono.
2. En el panel de control, abre **Conexiones** y luego **Otras**, selecciona las notificaciones de Android y pulsa **Mostrar un código de configuración**.
3. En la app OpenClaw, añade un Gateway y escanea el código. Después, vuelve al panel de control y pulsa **Aprobar**.
4. Cuando la app te lo pida, permite el acceso a las notificaciones. Luego, activa **Reenviar eventos de notificación** en los ajustes de la app para que las notificaciones lleguen en cuanto aparezcan, y no solo en la comprobación cada 10 minutos.

En tu propio ordenador, vincula el teléfono en la app OpenClaw y luego ejecuta `assistant connect android`.

## Cómo quitarla

- En el panel de control: abre **Conexiones**, selecciona Android, pulsa **Detalles** y luego **Desconectar**.
- En una Machine alojada, también puedes pulsar **Quitar** junto a ella en la página de configuración.

## Cómo quitarla del teléfono

Desactiva el acceso a las notificaciones de la app OpenClaw en los ajustes de Android o desvincula el teléfono en la app OpenClaw.
