---
title: Exchange Server
area: connections
summary: Reuniones de un Exchange Server que gestiona tu empresa (2013 a 2019 o Subscription Edition). Solo lectura.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
translated: a437b18fcb879c1b
---
## Qué lee

Tus reuniones, con sus invitados, salas y notas: la semana pasada y el mes siguiente al conectar, y luego cada cambio. Aparecen en Calendario y en la preparación de reuniones.

Es de solo lectura: nunca añade, mueve ni quita una reunión. El correo de Exchange Server aún no se lee.

## ¿Microsoft 365 o Exchange Server?

Exchange Server funciona en tu empresa. Microsoft 365 (Exchange Online) es la nube de Microsoft: para él, elige mejor **Calendario de Outlook**. Si tu dirección resulta estar en Microsoft 365, el formulario te lo dice.

## Conéctalo

1. En el panel, abre **Conexiones**, luego **Calendario**, y elige **Exchange Server**.
2. Escribe tu dirección de correo del trabajo y tu contraseña de Windows.
3. Pulsa **Conectar**.

El servidor se encuentra a partir de tu dirección (Autodiscover). ¿No se encuentra? Abre **Ajustes del servidor** y escribe el servidor que tu equipo de TI da para Outlook, como `mail.example.com`. ¿Inicias sesión con un nombre distinto de tu dirección? Escríbelo como `DOMAIN\name` en **Usuario**.

Inicia sesión con NTLM o Basic, solo por https.

## Si se detiene

- **El servidor de calendario rechazó la contraseña**: tu contraseña de Windows cambió. Vuelve a conectarlo.
- **Un buzón de Microsoft 365**: tu buzón se pasó a Microsoft 365. Desconecta este y conecta **Calendario de Outlook**.
- **No se pudo llegar al servidor de calendario**: lo reintenta solo. Algunos servidores solo se alcanzan dentro de la red de la empresa o por VPN.

## Quítalo

**Conexiones**, abre el calendario, **Detalles**, luego **Desconectar**. Lo que ya trajo se queda.
