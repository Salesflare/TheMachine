---
title: Shortcut
area: connections
summary: Historias que cambian de estado, con sus responsables y fechas límite. Solo lee.
covers: connector:shortcut
code: connectors/shortcut.py
site: Sign in with Shortcut, Connect, More sources, Remove
translated: 68419e11fabc157c
---
## Qué lee

Historias de tu espacio de trabajo de Shortcut que cambian de estado, con sus responsables y fechas límite.

## Qué puede hacer

Nada en Shortcut. Solo lee.

## Conectar Shortcut

1. En el panel: **Conexiones**, **Proyectos y código**, Shortcut. O en la página de configuración de una Machine alojada, en app.themachine.computer/setup: **Más fuentes**, Shortcut. En tu propio ordenador, primero vincúlala a tu cuenta.
2. Pulsa **Iniciar sesión con Shortcut** y permite el acceso de lectura. Solo solicita a Shortcut acceso de lectura.
3. Al volver a The Machine, verifica el inicio de sesión de inmediato y muestra con qué cuenta y en qué espacio de trabajo se conectó.

¿Tienes más de un espacio de trabajo de Shortcut? Primero cambia a ese espacio en Shortcut. Para otro espacio de trabajo, añade Shortcut de nuevo.

## Pegar un token en su lugar

Debajo de **O pega un token de API**, pulsa **Consigue tu token**. Shortcut abre su página API Tokens en una pestaña nueva: crea un token, cópialo, pégalo y pulsa **Conectar**. En tu propio ordenador, `assistant connect shortcut` también te lo pide. Un token tiene acceso completo a tu cuenta, pero The Machine solo lo usa para leer.

## Quitarla

- En el panel: **Conexiones**, abre Shortcut, **Detalles** y luego **Desconectar**. Lo que ya importó se conserva.
- En una Machine alojada, también puedes pulsar **Quitar** junto a Shortcut en su página de configuración.

## Revocarlo en Shortcut

Si pegaste un token, elimínalo en la página API Tokens. Si iniciaste sesión, desconectarlo aquí detiene toda lectura.
