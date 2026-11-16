---
title: Exchange Server
area: connections
summary: Reuniones de un Exchange Server que gestiona tu empresa (de 2013 a 2019 o Subscription Edition). Solo lectura.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
translated: f2b98c9bd4f08dba
---
## Qué lee

Tus reuniones, con sus invitados, salas y notas: la semana anterior y el mes siguiente al conectarte; después, cada cambio. Aparecen en Calendario y en la preparación de reuniones.

Es de solo lectura: nunca añade, mueve ni elimina reuniones. Todavía no lee el correo de Exchange Server.

## ¿Microsoft 365 o Exchange Server?

Exchange Server funciona en los servidores de tu empresa. Microsoft 365 (Exchange Online) es la nube de Microsoft: elige **Calendario de Outlook** en su lugar.

Introduce primero tu dirección. Si está en Microsoft 365, el formulario te lo indicará y mostrará **Iniciar sesión con Microsoft** en lugar del campo de contraseña. Se abrirá el inicio de sesión de Calendario de Outlook, sin contraseña. Si no lo encuentra en unos segundos o tu empresa tiene su propio servidor, se mantendrá el formulario de contraseña.

## Conéctalo

1. En el panel, abre **Conexiones**, luego **Calendario** y elige **Exchange Server**.
2. Introduce tu dirección de correo del trabajo y tu contraseña de Windows.
3. Pulsa **Conectar**.

El servidor se detecta a partir de tu dirección (Autodiscover). ¿No lo encuentra? Abre **Ajustes del servidor** e introduce el servidor que te indique el equipo de TI para Outlook, como `mail.example.com`. ¿Inicias sesión con un nombre distinto de tu dirección? Escríbelo como `DOMAIN\name` en **Usuario**.

La conexión se realiza con NTLM o Basic, solo por https.

## Si deja de funcionar

- **El servidor de calendario rechazó la contraseña**: tu contraseña de Windows ha cambiado. Vuelve a conectarlo.
- **Un buzón de Microsoft 365**: tu buzón se ha trasladado a Microsoft 365. Desconecta este calendario y conecta **Calendario de Outlook**.
- **No se pudo llegar al servidor de calendario**: lo vuelve a intentar automáticamente. Algunos servidores solo están disponibles dentro de la red de la empresa o mediante VPN.

## Eliminarlo

**Conexiones**, abre el calendario, **Detalles** y luego **Desconectar**. Lo que ya se ha importado se queda.
