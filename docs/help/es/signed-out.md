---
title: Sesión cerrada en un sitio
area: troubleshooting
summary: LinkedIn o X cerró la sesión de tu Machine. Vuelve a iniciarla, una vez o para siempre.
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
translated: b77b372b9332ca2b
---
Sitios como LinkedIn y X se leen en el navegador propio de tu Machine. A veces un sitio cierra su sesión.

## Vuelve a iniciar sesión

La fuente en **Conexiones**, y la parte superior de tus Tareas, indican que la sesión está cerrada. Pulsa **Volver a iniciar sesión** e inicia sesión en una pequeña ventana del panel.

Marca **Guardar para la próxima vez** al iniciar sesión. La próxima vez que el sitio cierre la sesión de tu Machine, vuelve a entrar con un toque. La contraseña se guarda cifrada en tu Machine; la IA nunca la ve.

## Contraseñas y códigos

Escribe las contraseñas tú. Los códigos de verificación en dos pasos también los introduces tú.

Los inicios de sesión guardados están en **Conexiones**, **Inicios de sesión**. **Olvidar** quita uno.

## Si el sitio lo rechaza o pide una verificación de robot

LinkedIn, X y los sitios detrás de una verificación de Cloudflare suelen rechazar los inicios de sesión desde un navegador en la nube. En una Machine alojada, el inicio de sesión muestra entonces **Inicia sesión desde tu conexión de casa**. Abre tu página de configuración, donde el navegador de tu Machine puede salir por tu internet de casa con Tailscale, o por tu propio proxy. Después, inicia sesión de nuevo.

En tu propio ordenador no lo necesitas: su navegador ya está en casa.
