---
title: Problemas en tu ordenador
area: troubleshooting
summary: Tu Machine lee los registros del propio ordenador y te avisa de problemas reales, con la causa y una solución. La solución solo se aplica cuando pulsas **Hazlo**.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: b18e5f4989d6baff
---
## Qué lee

En Linux con systemd, tu Machine lee el registro de tu propia sesión de usuario: tus propios servicios y los informes de fallos de tus propios programas. En Omarchy también comprueba Hyprland y la barra. Nunca lee el registro de todo el sistema ni pide más permisos.

Lee qué servicio se detuvo, cómo terminó y qué programa falló. Nunca lee el contenido de las líneas del registro, así que no se guarda ni sale de tu ordenador ningún texto de esos registros.

## Qué cuenta como problema

Un servicio que se reinicia continuamente, uno que falla varias veces en un día o permanece detenido, uno que se queda sin memoria y un programa que falla. En Omarchy, también los fallos de Hyprland o de la barra y los errores en los ajustes de Hyprland.

Un solo reinicio o un solo intento fallido es normal y no genera avisos. Tampoco los genera un servicio que falla unas cuantas veces y luego vuelve a funcionar bien, ni un servicio que falla y que nadie intenta iniciar: uno que no está habilitado y que ningún otro servicio o temporizador inicia.

Los navegadores controlados por pruebas y agentes (headless, Playwright, Puppeteer, CI) no generan avisos. Tampoco los genera un programa que se detiene mientras su servicio se está deteniendo o reiniciando. Lo mismo ocurre con las ejecuciones de desarrollo: lo que ejecuta un agente de programación, las pruebas y los programas que se ejecutan desde una carpeta temporal o de caché. Si un programa falla una y otra vez, se crea una sola tarea que indica cuántas veces y cuándo.

Los scripts aparecen con su propio nombre, como backup.py, no como python3 o node.

## Qué recibes

Una tarea que explica con palabras sencillas qué ocurrió, por qué importa y qué puedes hacer. Los comandos que muestran el motivo están en **Mostrar más**. Pregunta en su chat y The Machine lo investigará. Todo lo que cambie esperará a que des tu aprobación, igual que con **Hazlo**.

Si hay una solución segura, la tarea incluye **Hazlo**. Si uno de tus servicios permanece detenido, lo vuelve a iniciar y, en Omarchy, restaura la barra. **Hazlo** ejecuta únicamente ese comando y el resultado aparece en el chat de la tarea. Nunca modifica los servicios propios de The Machine ni OpenClaw Gateway.

El mismo problema genera como máximo una tarea cada dos semanas, y nunca mientras su tarea siga abierta. Se crean como máximo dos tareas nuevas al día. Una tarea sobre un servicio detenido se cierra automáticamente cuando vuelve a funcionar o se resuelve el problema.

## En una terminal

`assistant doctor` muestra los mismos problemas del último día.

## Otros ordenadores

En macOS, Windows y ordenadores sin systemd, no lee nada y lo indica en `assistant doctor`.

En una Machine alojada, el servidor está a nuestro cargo: sus problemas se envían al equipo de The Machine, no a ti como tareas.

## Desactivarlo

Configura `"computer_logs": false` en config.json y reinicia el servicio.
