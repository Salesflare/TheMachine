---
title: Se cerró la sesión de un sitio
area: troubleshooting
summary: LinkedIn o X cerró la sesión de tu Machine. Vuelve a iniciarla, una vez o para siempre.
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
translated: da165847c9a9d091
---
Los sitios como LinkedIn y X se abren en el navegador propio de tu Machine. A veces, un sitio cierra la sesión.

## Vuelve a iniciar sesión

**Conexiones** y la parte superior de tus tareas indican que la sesión está cerrada. Pulsa **Inicia sesión aquí** e inicia sesión en una ventana pequeña del panel.

Marca **Guardar para la próxima vez** para volver a iniciar sesión con un toque si vuelve a pasar. La contraseña se guarda cifrada en tu Machine y la IA nunca la ve.

## Contraseñas y códigos

Escribe tú las contraseñas. También te corresponde introducir los códigos de verificación en dos pasos.

Los inicios de sesión guardados están en **Conexiones**, **Inicios de sesión**. **Olvidar** elimina uno.

## Si el sitio rechaza el inicio de sesión o te pide verificar que no eres un robot

LinkedIn, X y los sitios que usan una verificación de Cloudflare suelen rechazar los inicios de sesión desde un navegador en la nube. En una Machine alojada, aparece entonces **Inicia sesión desde tu conexión de casa**. Se abre la página de configuración, donde el navegador de tu Machine puede conectarse a través de tu internet de casa con Tailscale o mediante tu propio proxy. Después, vuelve a iniciar sesión.

En tu propio ordenador no hace falta: su navegador ya está en casa.
