---
title: Ejecútala en tu propio ordenador
area: getting-started
summary: Instala la app de código abierto en Linux, macOS o Windows. Gratis, con tu propio modelo y tus propios datos.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
translated: 73526b82818f009d
---
Ejecuta The Machine gratis en tu propio ordenador. Es de código abierto (AGPL) y tus datos se quedan contigo. Para instalarla necesitas usar la terminal. Para conectar tus cuentas, no.

## Requisitos

- OpenClaw 2026.11.2 o posterior, el agente de código abierto que usa The Machine. El instalador te ofrece instalarlo.
- Python 3.12 o posterior y Node.js 24 (24.22.1 o posterior) o 26.12.1 o posterior, pero no la versión 25.
- Tailscale, para acceder al panel desde el móvil.
- Una cuenta de usuario normal, no root.

## Instálala

En Linux o macOS (macOS está en fase beta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

En Windows (beta), funciona dentro de WSL2. En PowerShell, ejecuta `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`. Configura WSL2 con Ubuntu y todo lo que necesita la app, y después ejecuta `./install.sh`.

El instalador encuentra tus cuentas, las conecta una a una y te muestra una vista previa de la semana pasada antes de activar nada.

## Después de instalarla

- Conecta tu correo: en la parte superior de **Tareas**, pulsa **Gmail** (o **Outlook**) y luego **Vincular esta Machine** para vincularla con tu cuenta. Si no tienes una cuenta, encontrarás **Usar tu propia app** justo debajo.
- Después, pulsa **Iniciar sesión con Google** (o **Iniciar sesión con Microsoft** para Outlook). El correo y el calendario se conectan a la vez.
- Otras fuentes: **Conexiones** y luego el tipo de fuente. Para usar tu propio cliente de Google o una app de Entra, ejecuta `assistant connect` en una terminal.
- Comprueba que todo funciona con `assistant doctor`. Muestra cómo solucionar cada problema.
- Instala la versión firmada más reciente; las actualizaciones también llegan como versiones firmadas.
- Vincula la app con tu cuenta y, después de iniciar sesión, se abrirá en el móvil. Si la desvinculas, se elimina esa conexión.

La guía completa está en el repositorio: [Primeros pasos](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
