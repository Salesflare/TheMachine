---
title: Salesflare CRM
area: connections
summary: Cuentas, contactos y oportunidades para saber quién importa. Lee los datos con tu clave de API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 3d6041d568843d96
---
## Qué datos lee

Tus cuentas, contactos y oportunidades en Salesflare, y la actividad de cada cuenta: correos de compañeros en los que no estabas incluido y reuniones con notas.

## Qué puede cambiar

Nada. (En tu propio ordenador, el ajuste `join_pipelines` puede añadirte a cuentas en los pipelines que elijas. Está desactivado de forma predeterminada.)

## Conectarlo

1. En Salesflare, abre [Ajustes, claves de API](https://app.salesflare.com/#/settings/apikeys) y crea una clave.
2. En una Machine alojada: abre tu página de configuración en app.themachine.computer/setup, ve a **Más fuentes**, abre Salesflare CRM, pega la clave y pulsa **Conectar**.
3. En el panel: **Conexiones**, **Clientes**, Salesflare CRM, pega la clave y pulsa **Conectar**. La tarjeta te mostrará el progreso.

## Detalles de sincronización

En **Conexiones**, **Clientes**, Salesflare muestra el progreso: las cuentas leídas en esta ronda y las que se hayan omitido porque Salesflare iba demasiado lento. Si una ronda tarda horas, aparecerá un aviso de que puede haberse quedado bloqueada.

Los mosaicos cuentan las cuentas que pudo abrir y los correos y reuniones que importó. Si Salesflare no permite que tu clave de API abra ninguna cuenta, la tarjeta mostrará **Necesita tu ayuda**: usa la clave de un usuario que pueda verlas. Si Salesflare agota el tiempo de espera, pero logra conectarse en cada reintento, indicará que a veces **va lento**.

Si Salesflare no ha habilitado el acceso a la actividad mediante claves de API para tu equipo, la tarjeta te lo indicará: no se importarán correos ni reuniones hasta que el equipo de soporte de Salesflare lo habilite. Lo comprobará cada 10 minutos durante el primer día y después aproximadamente cada hora. Cuando funcione, continuará por su cuenta.

- **Detener**: no se importarán datos nuevos hasta que pulses **Empezar**. Continuará desde donde se quedó.
- **Reiniciar sincronización**: empieza de nuevo y vuelve a leer la última semana. No se pierde nada de lo que ya importó.
- **Claves de API**: abre la página de claves de API de Salesflare para crear una nueva.

## Quitarla

- En el panel: **Conexiones**, abre Salesflare, **Detalles** y luego **Desconectar**. Se conservarán los datos que ya importó.
- En una Machine alojada, también puedes pulsar **Quitar** junto a ella en tu página de configuración.

## Revocar el acceso en Salesflare

Elimina la clave de API en Salesflare, en Ajustes, Claves de API.
