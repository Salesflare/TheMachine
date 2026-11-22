---
title: Ejecútala en tu propio ordenador
area: getting-started
summary: Instala la app de código abierto en Linux, macOS o Windows. Gratis, con tu propio modelo y tus propios datos.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
translated: 73526b82818f009d
---
Ejecuta The Machine gratis en tu propio ordenador. Es de código abierto (AGPL) y tus datos se quedan contigo. Para instalarla necesitas un terminal; para conectar tus cuentas, no.

## Qué necesita

- OpenClaw 2026.11.2 o posterior, el agente de código abierto sobre el que funciona The Machine. El instalador ofrece instalarlo.
- Python 3.12 o posterior, y Node.js 24 (24.22.1 o posterior) o 26.12.1 o posterior, no 25.
- Tailscale, para llegar a tu panel desde el teléfono.
- Una cuenta de usuario normal, no root.

## Instálala

En Linux o macOS (macOS está en beta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

En Windows (beta), se ejecuta dentro de WSL2. En PowerShell, ejecuta `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`. Configura WSL2 con Ubuntu y todo lo que necesita la app, y luego ejecuta `./install.sh`.

El instalador encuentra tus cuentas, las conecta una a una y muestra una vista previa de la semana pasada antes de activar nada.

## Después de instalar

- Conecta tu correo: arriba en **Tareas**, pulsa **Gmail** (o **Outlook**) y luego **Vincular esta Machine** para vincularla con tu cuenta. Sin cuenta, **Usar tu propia app** está justo debajo.
- Luego pulsa **Inicia sesión con Google** (o **Inicia sesión con Microsoft** para Outlook). El correo y el calendario se conectan juntos.
- Otras fuentes: **Conexiones** y luego el tipo de fuente. Tu propio cliente de Google o app de Entra: `assistant connect` en una terminal.
- Revísalo todo con `assistant doctor`. Muestra una solución para cada problema.
- El instalador toma la versión firmada más reciente, y las actualizaciones también llegan como versiones firmadas.
- Vincúlala con tu cuenta y la app del teléfono la abrirá cuando inicies sesión. Al desvincularla, se quita ese enlace.

La guía completa está en el repositorio: [Primeros pasos](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
