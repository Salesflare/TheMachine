---
title: Salesflare CRM
area: connections
summary: Cuentas, contactos y oportunidades, para saber quién importa. Lee con tu clave de API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
---
## Qué lee

Tus cuentas, contactos y oportunidades en Salesflare, y los feeds de las cuentas: correos de compañeros en los que no participas, y reuniones con notas.

## Qué puede cambiar

Nada, a menos que configures `join_pipelines` en el archivo de ajustes de tu Machine. Entonces te añade solo a las cuentas de esos pipelines. Por defecto está vacío.

## Conéctalo

1. En Salesflare, abre [Settings, API keys](https://app.salesflare.com/#/settings/apikeys) y crea una clave.
2. En una Machine alojada: abre tu página de configuración en app.themachine.computer/setup, ve a **Más fuentes**, abre Salesflare CRM, pega la clave y pulsa **Conectar**.
3. En tu propio ordenador: ejecuta `assistant connect crm`, o **Conexiones**, **+ Añadir**, Salesflare CRM. Tras **Conectar**, tu Machine se reinicia y abre la tarjeta de Salesflare, que primero dice que está buscando las cuentas con correos y reuniones recientes, y luego cuántas ha leído.

## Detalles de la sincronización

Su tarjeta en **Conexiones**, **Otras fuentes** muestra cómo va: cuántas cuentas ha leído en esta ronda, y cuántas se saltó porque Salesflare tardó demasiado en responder. Una ronda que dura horas avisa de que puede estar atascada.

- **Detener**: no entra nada nuevo hasta que pulses **Iniciar**. Sigue donde estaba.
- **Reiniciar sincronización**: descarta la ronda en curso, con sus errores, y vuelve a leer la última semana ahora. No se pierde nada de lo que trajo.
- **Claves de API**: abre la página de claves de API de Salesflare, para crear una clave nueva.

## Quítalo

- En el panel: **Conexiones**, abre Salesflare, **Detalles** y luego **Desconectar**. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Revócalo en Salesflare

Elimina la clave de API en Salesflare, en Settings, API keys.
