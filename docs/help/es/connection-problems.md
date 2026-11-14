---
title: Una conexión necesita ayuda
area: troubleshooting
summary: Una fuente muestra **Necesita tu ayuda** o deja de importar contenido. Qué puedes probar.
covers: 
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: 1c530fc2b291d640
---
## Comprueba el estado

Abre **Conexiones**. Cada fuente indica cómo va:

- **Reconectando automáticamente**: un fallo momentáneo. Lo intenta de nuevo por su cuenta.
- **Esperando la primera sincronización**: acaba de conectarse. Espera unos minutos.
- **Vuelve a leer a las** 07:00: X y LinkedIn solo leen durante el día. No tienes que hacer nada.
- **Necesita tu ayuda**: abre **Detalles**. Ahí se explica qué ha fallado y qué hacer.
- **Teléfono desconectado**: tu teléfono Android no se comunica con tu Machine. Abre la aplicación OpenClaw en el teléfono.

Si una fuente no importa nada durante más tiempo de lo habitual, deja de aparecer como conectada. El estado se corrige por sí solo cuando llegan elementos nuevos.

El número de **Conexiones** solo cuenta las fuentes que necesitan tu ayuda.

## Soluciones habituales

- «Vuelve a iniciar sesión en Google» (o Microsoft): pulsa **Reconectar** una vez para recuperar todas las fuentes de esa cuenta, como Gmail y Calendario.
- «Necesitas volver a iniciar sesión»: pulsa **Reconectar** e inicia sesión.
- Microsoft todavía está configurando el acceso: lo vuelve a intentar por su cuenta.
- Slack: pulsa **Reconectar**. ¿Te conectaste con una clave de Maton? Comprueba la clave y la conexión de Slack en Maton.
- Android: abre la aplicación OpenClaw en el teléfono y permite que acceda a las notificaciones.

En tu propio ordenador, `assistant doctor` comprueba todas las fuentes e indica cómo solucionar cada problema.

¿Sigues sin poder resolverlo? Consulta [Contactar con soporte](get-support.md).
