---
title: Problemas en tu equipo
area: troubleshooting
summary: Tu Machine lee los registros de su propio equipo y te avisa de los problemas reales, con la causa y una solución. Solo lee.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
---
## Qué lee

En Linux con systemd, tu Machine lee el registro de tu propia sesión: tus propios servicios y los informes de fallo de tus propios programas. En Omarchy también revisa Hyprland y la barra. Nunca lee el registro de todo el sistema y nunca pide más acceso.

Lee qué servicio se detuvo, cómo terminó y qué programa falló. Nunca lo que dice una línea del registro, así que ningún texto del registro se guarda ni sale de tu equipo.

## Qué cuenta como problema

Un servicio que se reinicia una y otra vez, uno que falló varias veces en un día o sigue caído, uno que se quedó sin memoria y un programa que se cerró de golpe. En Omarchy también un fallo de Hyprland o de la barra, y errores en tu configuración de Hyprland.

Un solo reinicio o una sola ejecución fallida es normal y no avisa.

## Qué recibes

Una tarea que dice con palabras simples qué pasó, por qué importa y el comando que lo muestra o lo arregla. Pregunta en su chat y The Machine lo revisa. Todo lo que ella cambie espera tu OK, como con Do it.

Un mismo problema trae como mucho una tarea cada dos semanas, y nunca mientras su tarea siga abierta. Como mucho dos nuevas al día.

## En una terminal

`assistant doctor` muestra los mismos problemas del último día.

## Otros equipos

En macOS, Windows y equipos sin systemd no lee nada y lo dice en `assistant doctor`.

## Desactivarlo

Pon `"computer_logs": false` en config.json y reinicia el servicio.
