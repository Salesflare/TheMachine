---
title: Se cerró la sesión en un sitio
area: troubleshooting
summary: LinkedIn o X cerraron la sesión de tu Machine. Vuelve a iniciarla, una vez o para las próximas veces.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js, dashboard/connections-login-import.js
order: 2
translated: 9a9b91270954c031
---
Sitios como LinkedIn y X se abren en el navegador propio de tu Machine. A veces, un sitio cierra la sesión de tu Machine.

## Vuelve a iniciar sesión

**Conexiones** y la parte superior de tus tareas indican que se cerró la sesión. Pulsa **Inicia sesión aquí** e inicia sesión en una ventana pequeña del panel.

Marca **Guardar para la próxima vez** para volver a iniciar sesión con un solo toque si vuelve a pasar. La contraseña se queda cifrada en tu Machine y la IA nunca la ve. Si tienes varias cuentas en un sitio, **Guardar como** le pone un nombre a esta (Trabajo, Personal), y el cuadro de diálogo te pregunta cuál quieres usar si la tarea no lo especifica.

## Contraseñas y códigos

Escribe las contraseñas tú. También tienes que introducir los códigos de verificación en dos pasos.

Los inicios de sesión guardados están en **Conexiones**, **Inicios de sesión**. **Olvidar** elimina uno. **Importar** permite traerlos desde un gestor de contraseñas, mediante su propia página de exportación en el navegador de tu Machine o desde un archivo de exportación.

## Si el sitio no te deja iniciar sesión o te pide verificar que no eres un robot

LinkedIn, X y los sitios que usan una verificación de Cloudflare suelen rechazar los inicios de sesión desde un navegador en la nube. En una Machine alojada, entonces aparece **Inicia sesión desde tu conexión de casa**. Se abre la página de configuración, donde el navegador de tu Machine puede conectarse a internet a través de tu conexión de casa con Tailscale o de tu propio proxy. Después, vuelve a iniciar sesión.

En tu propio ordenador no hace falta: su navegador ya está en casa.
