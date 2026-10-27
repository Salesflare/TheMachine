---
title: Una conexión necesita ayuda
area: troubleshooting
summary: Una fuente dice Necesita tu ayuda, o deja de traer cosas. Qué probar.
covers: 
code: onboarding.py, dashboard.html
order: 1
---
## Mira su estado

Abre **Conexiones**. Cada fuente indica cómo va:

- **Reconectando automáticamente**: un fallo breve. Lo reintenta sola.
- **Esperando la primera sincronización**: recién conectada. Dale unos minutos.
- **Necesita tu ayuda**: abre **Detalles**. Dice qué falló y qué hacer.

## Soluciones habituales

- "necesita que vuelvas a iniciar sesión": pulsa **Reconectar** e inicia sesión. En una Machine alojada, Google y Microsoft se reconectan desde tu página de configuración.
- Microsoft aún configurando el acceso: lo vuelve a intentar sola.
- Slack: revisa tu clave de API de Maton y la conexión de Slack en Maton.
- Android: abre la app OpenClaw en el teléfono y dale acceso a las notificaciones.

En tu propio ordenador, `assistant doctor` revisa cada fuente y muestra la solución de cada problema.

¿Sigues atascado? Consulta [Obtener ayuda](get-support.md).
