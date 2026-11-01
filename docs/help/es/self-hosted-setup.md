---
title: Ejecútala en tu propio ordenador
area: getting-started
summary: Instala la app de código abierto en Linux, macOS o Windows. Gratis, con tu propio modelo y tus propios datos.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
---
The Machine es de código abierto (AGPL). En tu propio ordenador es gratis, y tus datos se quedan ahí.

## Qué necesita

- OpenClaw 2026.10.7 o posterior. El instalador ofrece instalarlo.
- Python 3.12 o posterior, y Node.js 24 (24.22.1 o posterior) o 26.12.1 o posterior, no 25.
- Tailscale, para llegar a tu panel desde el teléfono.
- Tu propia cuenta de usuario, no root.

## Instálala

En Linux o macOS (macOS está en beta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

En Windows (beta), se ejecuta dentro de WSL2. En PowerShell, ejecuta `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`. Configura WSL2 con Ubuntu y todo lo que necesita la app, y luego ejecuta `./install.sh`.

El instalador encuentra tus cuentas, las conecta una a una y muestra una vista previa de la semana pasada antes de activar nada.

## Después de instalar

- Añade fuentes con `assistant connect`, o con **Conexiones** y luego **+ Añadir** en el panel.
- Revísalo todo con `assistant doctor`. Muestra una solución para cada problema.
- Las actualizaciones llegan como versiones firmadas.

La guía completa está en el repositorio: [Primeros pasos](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
