---
title: Salesflare CRM
area: connections
summary: Cuentas, contactos y oportunidades para que sepa quién importa. Accede con tu clave de API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 8051c61777603a7e
---
## Qué lee

Tus cuentas, contactos y oportunidades en Salesflare, y la actividad de cada cuenta: correos de compañeros en los que no estabas incluido y reuniones con notas.

## Qué puede cambiar

Nada. (En tu propio ordenador, el ajuste `join_pipelines` puede añadirte a las cuentas de los pipelines que elijas. Está desactivado de forma predeterminada.)

## Conectarlo

1. En Salesflare, abre [Ajustes, Claves de API](https://app.salesflare.com/#/settings/apikeys) y crea una clave.
2. En una Machine alojada: abre tu página de configuración en app.themachine.computer/setup, ve a **Más fuentes**, abre Salesflare CRM, pega la clave y pulsa **Conectar**.
3. En el panel: **Conexiones**, **Clientes**, Salesflare CRM, pega la clave y pulsa **Conectar**. La tarjeta muestra el progreso.

## Detalles de sincronización

En **Conexiones**, **Clientes**, Salesflare muestra el progreso: las cuentas revisadas en esta ronda, las que se han omitido porque Salesflare iba demasiado lento y las que no puedes abrir con tu clave de API (**sin acceso**). Si una ronda dura horas, puede que se haya quedado bloqueada.

Los recuadros indican cuántas cuentas ha leído esta semana y cuántos correos y reuniones ha incorporado.

No hace falta hacer nada si hay unas pocas cuentas sin acceso: el resto se importa como siempre. Si tu clave de API no puede abrir ninguna cuenta, la tarjeta muestra **Necesita tu ayuda**: usa la clave de un usuario que pueda verlas. Una clave nueva empieza desde cero y vuelve a leer la última semana. Si Salesflare sigue agotando el tiempo de espera, pero consigue conectarse en cada reintento, indica que Salesflare va **lenta a veces**.

Si Salesflare no ha activado el acceso al feed para las claves de API de tu equipo, la tarjeta te lo indica: no se importarán correos ni reuniones hasta que el equipo de soporte de Salesflare lo active. Lo comprueba cada 10 minutos durante el primer día y, después, aproximadamente cada hora. Cuando funciona, continúa por sí sola.

- **Detener**: no se importa nada nuevo hasta que pulses **Empieza**. Continúa desde donde lo dejó.
- **Reiniciar sincronización**: vuelve a empezar y lee de nuevo la última semana. No se pierde nada de lo que ya había importado.
- **Claves de API**: abre la página de claves de API de Salesflare para crear una nueva.

## Quitar la conexión

- En el panel: abre **Conexiones**, selecciona Salesflare, pulsa **Detalles** y, después, **Desconectar**. Se conserva lo que ya había importado.
- En una Machine alojada, también puedes pulsar **Quitar** junto a la conexión en tu página de configuración.

## Revocar el acceso en Salesflare

Elimina la clave de API en Salesflare, en Ajustes, Claves de API.
