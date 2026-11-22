---
title: Una conexión necesita ayuda
area: troubleshooting
summary: Una fuente muestra **Necesita tu ayuda** o deja de recibir datos. Qué puedes probar.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: c07a7f214b1e4deb
---
## Comprueba su estado

Abre **Conexiones**. Cada fuente indica su estado:

- **Reconectando automáticamente**: un fallo breve. Lo intenta de nuevo automáticamente.
- **Esperando la primera sincronización**: acaba de conectarse. Espera unos minutos.
- **Vuelve a leer a las** 07:00: X y LinkedIn solo leen durante el día. No tienes que hacer nada.
- **Necesita tu ayuda**: abre **Detalles**. Ahí se indica qué ha fallado y qué hacer.
- **Teléfono desconectado**: tu teléfono Android no se está comunicando con tu Machine. Abre la aplicación OpenClaw en el teléfono.

Si una fuente no recibe datos durante más tiempo de lo habitual, muestra **Esperando una nueva sincronización**. El aviso desaparece automáticamente cuando se completa una sincronización.

El número que aparece en **Conexiones** solo cuenta las fuentes que necesitan tu ayuda.

## Soluciones habituales

- «Vuelve a iniciar sesión en Google» (o Microsoft): un solo **Reconectar** recupera todas las fuentes de esa cuenta, como Gmail y Calendar.
- «necesitas volver a iniciar sesión»: pulsa **Reconectar** e inicia sesión.
- Microsoft aún está configurando el acceso: lo vuelve a intentar automáticamente.
- Slack: pulsa **Reconectar**. ¿Te conectaste con una clave de Maton? Comprueba la clave y la conexión de Slack en Maton.
- Android: abre la aplicación OpenClaw en el teléfono y permite que acceda a las notificaciones.

En tu propio ordenador, `assistant doctor` comprueba todas las fuentes e indica cómo solucionar cada problema.

¿Sigues con problemas? Consulta [Obtener ayuda](get-support.md).
