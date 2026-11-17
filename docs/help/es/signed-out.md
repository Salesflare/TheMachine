---
title: Se cerró tu sesión en un sitio
area: troubleshooting
summary: LinkedIn o X cerraron la sesión de tu Machine. Vuelve a iniciarla una vez o guarda el inicio de sesión para la próxima vez.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js
order: 2
translated: 060f7ca4f870ad0a
---
En tu Machine, los sitios como LinkedIn y X se consultan desde su propio navegador. A veces, un sitio cierra la sesión.

## Vuelve a iniciar sesión

**Conexiones** y la parte superior de tus tareas indican que cerraste la sesión. Pulsa **Inicia sesión aquí** e inicia sesión en una ventana pequeña del panel.

Marca **Guardar para la próxima vez** para volver a iniciar sesión con un solo toque si vuelve a pasar. La contraseña se mantiene cifrada en tu Machine y la IA nunca la ve. Si tienes varias cuentas en un mismo sitio, **Guardar como** le asigna un nombre a esta cuenta (Trabajo, Personal). Si la tarea no especifica cuál usar, el cuadro de diálogo te lo pregunta.

## Contraseñas y códigos

Escribe las contraseñas tú. También tienes que introducir los códigos de verificación en dos pasos.

Los inicios de sesión guardados están en **Conexiones**, **Inicios de sesión**. **Olvidar** elimina uno. **Importar** los añade desde un gestor de contraseñas.

## Si el sitio rechaza el inicio de sesión o te pide verificar que no eres un robot

LinkedIn, X y los sitios con una verificación de Cloudflare suelen rechazar los inicios de sesión desde un navegador en la nube. En una Machine alojada, aparece **Inicia sesión desde tu conexión de casa**. Esta opción abre la página de configuración, donde el navegador de tu Machine puede conectarse a través de internet de tu casa con Tailscale o de tu propio proxy. Después, vuelve a iniciar sesión.

En tu propio equipo no hace falta: su navegador ya está en casa.
