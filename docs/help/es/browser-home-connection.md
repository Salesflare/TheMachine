---
title: La conexión de casa de tu navegador
area: troubleshooting
summary: Haz que el navegador de tu Machine alojada salga por tu internet de casa con Tailscale, para que los sitios acepten sus inicios de sesión.
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
translated: 9935ac3c09fa5c00
---
Algunos sitios, como LinkedIn, X y los que pasan por una comprobación de Cloudflare, rechazan inicios de sesión desde un navegador en la nube. Tu página de configuración puede hacer que el navegador de tu Machine alojada salga por tu internet de casa, con Tailscale. Es gratis, lleva unos 10 minutos y casi todo pasa solo.

## Configurarlo

1. En tu página de configuración, en el navegador de tu Machine, elige **Tailscale** y pulsa **Iniciar sesión en Tailscale**. Inicia sesión o crea allí una cuenta gratis.
2. Instala Tailscale en un ordenador de casa que se quede encendido e inicia sesión allí con la misma cuenta. Un teléfono no: se duerme.
3. Convierte ese ordenador en nodo de salida. La página de configuración muestra el menú para su sistema. En Linux, ejecuta `sudo tailscale set --advertise-exit-node`.
4. Pulsa **Ábrelo en Tailscale** y permítelo: Machine settings, Edit route settings, Use as exit node, Save. En el mismo menú, elige Disable key expiry.

La página de configuración marca cada paso sola. Con un nodo de salida, tu navegador empieza a usarlo enseguida. Con varios, elige uno y pulsa **Usar este nodo de salida**.

## Comprobarlo

Pulsa **Probarlo**. La página muestra dónde ve la web tu navegador: tu ciudad y tu proveedor de internet.

## Cuando el ordenador de casa está apagado

Tu navegador sale entonces directamente desde tu Machine, y vuelve a pasar por tu casa en cuanto el ordenador se enciende. ¿Se cerró la sesión de Tailscale? Pulsa **Volver a iniciar sesión**. Tailscale cierra la sesión de los dispositivos a los 6 meses, salvo que key expiry esté desactivado. La página de configuración muestra la fecha.

## Dejar de usarlo

Pulsa **Dejar de usarlo** para volver a ir directo. **Cerrar también su sesión de Tailscale** cierra también la sesión de Tailscale del navegador de tu Machine. La consola de administración de Tailscale lo muestra entonces como Expired, y puedes quitarlo allí.
