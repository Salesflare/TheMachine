---
title: Una conexión necesita ayuda
area: troubleshooting
summary: Una fuente dice Necesita tu ayuda, o deja de traer cosas. Qué probar.
covers: 
code: onboarding.py, dashboard.html, assistant.py
order: 1
---
## Mira su estado

Abre **Conexiones**. Cada fuente indica cómo va:

- **Reconectando automáticamente**: un fallo breve. Lo reintenta sola.
- **Esperando la primera sincronización**: recién conectada. Dale unos minutos.
- **Vuelve a leer a las** 07:00: X y LinkedIn solo leen de día. No hay nada que hacer.
- **Necesita tu ayuda**: abre **Detalles**. Dice qué falló y qué hacer.
- **Teléfono desconectado**: el teléfono no llega a OpenClaw. Abre la app de OpenClaw en él.

Una fuente que sigue fallando y no trae nada nuevo durante horas, más que su rato tranquilo habitual, no aparece como conectada. Se resuelve sola en cuanto llega algo nuevo.

El número en **Conexiones** solo cuenta las fuentes que necesitan tu ayuda.

## Soluciones habituales

- "Vuelve a iniciar sesión en Google" (o Microsoft): una línea por cuenta. Un solo **Reconectar** recupera todas sus fuentes, como Gmail y Calendar.
- "necesita que vuelvas a iniciar sesión": pulsa **Reconectar** e inicia sesión. En una Machine alojada, inicias sesión ahí mismo y vuelves al panel.
- Microsoft aún configurando el acceso: lo vuelve a intentar sola.
- Slack: revisa tu clave de API de Maton y la conexión de Slack en Maton.
- Android: abre la app OpenClaw en el teléfono y dale acceso a las notificaciones.

En tu propio ordenador, `assistant doctor` revisa cada fuente y muestra la solución de cada problema.

¿Sigues atascado? Consulta [Obtener ayuda](get-support.md).
