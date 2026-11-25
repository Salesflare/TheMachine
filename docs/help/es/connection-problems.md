---
title: Una conexión necesita ayuda
area: troubleshooting
summary: Una fuente indica «Necesita tu ayuda» o deja de importar datos. Qué puedes probar.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: cc4b227abd053022
---
## Comprueba el estado

Abre **Conexiones**. Cada fuente indica cómo está:

- **Reconectando automáticamente**: un fallo momentáneo. Lo intenta de nuevo por su cuenta.
- **Esperando la primera sincronización**: acaba de conectarse. Espera unos minutos.
- **Vuelve a leer a las** 07:00: X y LinkedIn solo leen durante el día. No tienes que hacer nada.
- **Aún no está configurado**: nadie ha iniciado sesión aquí todavía. Pulsa **Conectar**. Se pondrá en marcha en menos de un minuto.
- **Necesita tu ayuda**: abre **Detalles**. Ahí se indica qué ha fallado y qué tienes que hacer.
- **Teléfono desconectado**: tu teléfono Android no logra conectarse a tu Machine. Abre la app de OpenClaw en el teléfono.

Si una fuente lleva más tiempo de lo habitual sin importar nada, indica **Esperando una nueva sincronización**. Se quitará automáticamente cuando se complete una sincronización.

El número de **Conexiones** solo cuenta las fuentes que necesitan tu ayuda.

## Soluciones habituales

- «Inicia sesión en Google de nuevo» (o en Microsoft): con una sola **Reconectar** se recuperan todas las fuentes de esa cuenta, como Gmail y Calendario.
- «necesitas volver a iniciar sesión»: pulsa **Reconectar** e inicia sesión.
- «necesitas un programa que no está en este ordenador»: ejecuta el comando de su tarjeta en un terminal de ese ordenador. Te indica qué instalar o encuentra un programa que se ha movido.
- Microsoft sigue configurando el acceso: lo vuelve a intentar automáticamente.
- Slack: pulsa **Reconectar**. ¿Te has conectado con una clave de Maton? Comprueba la clave y la conexión de Slack en Maton.
- Android: abre la app de OpenClaw en el teléfono y permite que acceda a las notificaciones.

En tu propio ordenador, `assistant doctor` comprueba todas las fuentes e indica cómo solucionar cada problema.

¿Sigues sin poder resolverlo? Consulta [Contactar con soporte](get-support.md).
