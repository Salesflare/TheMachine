---
title: Problemas en tu ordenador
area: troubleshooting
summary: Tu Machine lee los registros de su propio ordenador y te avisa de los problemas reales, con la causa y una solución. Una solución solo se ejecuta cuando tocas **Hazlo**.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: 1a191d8433bfba2a
---
## Qué lee

En Linux con systemd, tu Machine lee el registro de tu propia sesión de usuario: tus propios servicios y los informes de fallos de tus propios programas. En Omarchy también comprueba Hyprland y la barra. Nunca lee el registro de todo el sistema ni pide más acceso.

Lee qué servicio se detuvo, cómo terminó y qué programa falló. Nunca lee el contenido de las líneas del registro, así que no se guarda ni sale de tu ordenador ningún texto de los registros.

## Qué se considera un problema

Un servicio que se reinicia una y otra vez, uno que falla varias veces en un día o permanece detenido, uno que se queda sin memoria y un programa que se bloquea. En Omarchy, también los fallos de Hyprland o de la barra, y los errores en los ajustes de Hyprland.

Un solo reinicio o un solo fallo es normal y no genera avisos. Tampoco los genera un servicio que falla unas cuantas veces y luego vuelve a funcionar bien.

Los navegadores que controlan las pruebas y los agentes (headless, Playwright, Puppeteer, CI) no generan avisos. Tampoco los genera un programa que se detiene mientras se detiene o reinicia su servicio. Lo mismo ocurre con las ejecuciones de desarrollo: lo que ejecuta un agente de programación, las pruebas y los programas que se ejecutan desde una carpeta temporal o de caché. Si un programa se bloquea una y otra vez, se crea una sola tarea que indica cuántas veces y cuándo.

Los scripts aparecen con su propio nombre, como backup.py, no como python3 o node.

## Qué recibes

Una tarea que explica en palabras sencillas qué pasó, por qué importa y qué puedes hacer. Los comandos que muestran la causa aparecen en **Mostrar más**. Pregunta en su chat y The Machine lo investigará. Cualquier cambio que haga esperará tu aprobación, igual que con **Hazlo**.

Si hay una solución segura, la tarea incluye **Hazlo**. Si uno de tus servicios permanece detenido, lo inicia de nuevo; en Omarchy, también vuelve a activar la barra. **Hazlo** solo ejecuta ese comando y el resultado aparece en el chat de la tarea. Nunca afecta a los propios servicios de The Machine ni al OpenClaw Gateway.

El mismo problema genera como máximo una tarea cada dos semanas, y nunca mientras su tarea siga abierta. Se crean como máximo dos tareas nuevas al día. Una tarea sobre un servicio detenido se cierra automáticamente cuando vuelve a funcionar o se resuelve el problema.

## En un terminal

`assistant doctor` muestra los mismos problemas del último día.

## Otros ordenadores

En macOS, Windows y los ordenadores sin systemd, no lee nada y lo indica en `assistant doctor`.

En una Machine alojada, nos encargamos de mantener el servidor en funcionamiento: sus problemas se envían al equipo de The Machine, no a ti como tareas.

## Desactivarlo

Establece `"computer_logs": false` en config.json y reinicia el servicio.
