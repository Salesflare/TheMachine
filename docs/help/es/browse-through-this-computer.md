---
title: Navega desde la app de escritorio
area: troubleshooting
summary: Haz que el navegador de tu Machine alojada salga a Internet a través del ordenador donde se ejecuta la app de escritorio, para que los sitios vean tu conexión a Internet.
code: desktop/src/exit.rs, desktop/src/settings.rs
keywords: desktop app, exit node, home internet, office, ip address, linkedin, sign in, proxy
order: 5
translated: 6da69c78d7e60574
---
Algunos sitios, como LinkedIn, rechazan los inicios de sesión desde navegadores en la nube. Con la [app de escritorio](desktop-app.md) iniciada, el navegador de tu Machine alojada puede salir a Internet a través de ese ordenador. Así, los sitios ven tu conexión de casa o del trabajo, no la de un centro de datos.

## Actívalo

Se activa de forma predeterminada cuando tu Machine tiene esta función. En los Ajustes de la app de escritorio, el interruptor se llama **Dejar que mi Machine navegue a través de este ordenador**. Desactívalo y el navegador de tu Machine volverá a salir directamente, de inmediato.

Mientras el navegador de tu Machine use esta función, el cuadro del robot y el icono de la app en la barra de menús o la barra de tareas mostrarán **Tu Machine está navegando a través de este ordenador**.

## Qué tráfico pasa por aquí

Solo pasa el tráfico del navegador de tu Machine hacia sitios web: los puertos 80 y 443 de direcciones públicas de Internet. La app nunca se conecta a este ordenador, a tu red doméstica o del trabajo ni a otras direcciones privadas, y no abre ningún puerto en tu ordenador. El límite es de 4 MB/s de descarga, 1 MB/s de subida y 2 GB al día.

## Cuando el ordenador está apagado

El navegador de tu Machine sale directamente desde tu Machine y vuelve a hacerlo a través del ordenador en cuanto la app vuelve a ejecutarse.
