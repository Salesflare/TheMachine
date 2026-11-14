---
title: Salesforce
area: connections
summary: Oportunidades, tareas y actividad de Salesforce en tus personas y proyectos. Si lo activas, mantiene al día los datos de contacto allí.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: e2394748e0a676b1
---
## Qué lee

Oportunidades nuevas, y oportunidades que pasan a otra etapa o cambian de importe. Tus tareas abiertas, llamadas y otras tareas registradas como hechas con notas, y reuniones con descripción. Los últimos 7 días al conectar, y luego las nuevas cada 15 minutos.

Cada oportunidad se convierte en un proyecto en tu Graph, y sus contactos aparecen en sus personas, como contacto de Salesforce en su cuenta.

## Qué puede cambiar

Nada, hasta que activas **Actualizar datos de contacto**. Tu inicio de sesión de Salesforce se queda en tu Machine.

## Conéctalo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre Salesforce y pulsa **Conectar Salesforce**.
3. Inicia sesión en Salesforce y permite The Machine (hecha por Salesflare).

O en el panel: **Conexiones**, **Clientes**, elige Salesforce y pulsa **Iniciar sesión con Salesforce**.

Tu usuario de Salesforce necesita acceso a la API, que incluyen la mayoría de las ediciones.

## Actualizar datos de contacto

Cuando tu Machine conoce datos más recientes de uno de tus contactos de Salesforce, puede actualizar ese contacto allí: cargo, teléfono, y el enlace de LinkedIn si tu org tiene un campo de LinkedIn en los contactos.

1. En **Conexiones**, abre Salesforce y pulsa **Ver qué cambiaría**.
2. Revisa la lista y pulsa **Activar** o **Ahora no**.

Lo que respeta:

- Solo datos en las propias palabras de la persona, como su perfil de LinkedIn o Slack, o los que pusiste tú en su página. Nunca una suposición.
- Solo cuando el dato es más reciente que el último cambio del contacto en Salesforce. Un cambio hecho allí gana.
- Solo campos que difieren, y nunca un valor vacío. Nunca cambia la dirección de email ni la cuenta.
- Cada cambio es una línea con fecha en la página de la persona.

Pulsa **Desactivar** para parar. Una conexión que comparte tu Fleet solo lee.

## Quítalo

- En el panel: **Conexiones**, abre Salesforce, **Detalles** y luego **Desconectar**. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Revócalo en Salesforce

En Salesforce, abre tu configuración personal y luego Connected Apps OAuth Usage, o pídeselo a tu admin, y revoca The Machine. Ya no puede leer ni cambiar nada.
