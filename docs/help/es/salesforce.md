---
title: Salesforce
area: connections
summary: Oportunidades, tareas y actividad de Salesforce en tus personas y proyectos. Si activas esta opción, puede mantener actualizados allí los datos de contacto.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: eee5e084bac6dbd1
---
## Qué lee

Las oportunidades nuevas y las que pasan a otra fase o cambian de importe. Tus tareas abiertas, llamadas y otras tareas marcadas como hechas con notas, además de las reuniones con una descripción. Los últimos 7 días al conectarlo y, después, las novedades cada 15 minutos.

Cada oportunidad se convierte en un proyecto en tu Graph. Los contactos asociados aparecen en las fichas de las personas, como contactos de Salesforce en su cuenta.

## Qué puede cambiar

Nada, hasta que actives **Actualizar datos de contacto**. La sesión de Salesforce permanece en tu Machine.

## Conectarla

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre Salesforce y pulsa **Conectar Salesforce**.
3. Inicia sesión en Salesforce y autoriza a The Machine (creada por Salesflare).

También puedes hacerlo en el panel: **Conexiones**, **Clientes**, selecciona Salesforce y pulsa **Iniciar sesión con Salesforce**. Si usas tu propio ordenador, primero vincúlala a tu cuenta.

Tu usuario de Salesforce necesita acceso a la API, que incluyen la mayoría de las ediciones.

## Actualizar datos de contacto

Cuando tu Machine tenga datos más recientes de alguno de tus contactos de Salesforce, puede actualizar allí su cargo, teléfono y enlace de LinkedIn, si tu organización tiene un campo de LinkedIn en los contactos.

1. En **Conexiones**, abre Salesforce y pulsa **Ver qué cambiaría**.
2. Revisa la lista y pulsa **Activar** o **Ahora no**.

Esto es lo que tiene en cuenta:

- Solo datos que la persona haya compartido con sus propias palabras, como los de su perfil de LinkedIn o Slack, o que hayas añadido a su ficha. Nunca hace conjeturas.
- Solo cuando el dato es más reciente que el último cambio del contacto en Salesforce. Una edición hecha allí prevalece.
- Solo modifica los campos que sean distintos y nunca los deja en blanco. No cambia la dirección de correo ni la cuenta.
- Cada cambio aparece como una línea con fecha en la ficha de la persona.

Pulsa **Desactivar** para detenerlo. Una conexión compartida por tu Fleet solo permite leer datos.

## Quitarla

- En el panel: **Conexiones**, abre Salesforce, pulsa **Detalles** y luego **Desconectar**. Los datos que ya haya importado se conservan.
- En una Machine alojada, pulsa **Desconectar ↗** para abrir tu página de configuración y, junto a Salesforce, pulsa **Quitar**.

## Revocar el acceso en Salesforce

En Salesforce, abre tus ajustes personales y luego Connected Apps OAuth Usage, o pídeselo a tu administrador, y revoca el acceso de The Machine. Ya no podrá leer ni cambiar nada.
