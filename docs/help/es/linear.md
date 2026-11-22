---
title: Linear
area: connections
summary: Tus incidencias, menciones, comentarios, revisiones y fechas de vencimiento de Linear. Los comentarios, los cambios de estado y de responsable, y las incidencias nuevas esperan tu visto bueno.
covers: connector:linear
code: connectors/linear.py, linear_writes.py
site: Sign in with Linear, Connect, More sources, Remove
translated: 1e16b6abdf4fefad
---
## Qué lee

Tu bandeja de entrada de Linear y las incidencias que tienes asignadas. Incluye:

- Las incidencias que tienes asignadas: las nuevas y las que hayan cambiado de estado, fecha de vencimiento o título. Cuando una incidencia se completa o se cancela en Linear, su tarea se cierra automáticamente. **Deshacer** la vuelve a abrir.
- Las menciones que te hacen, y los comentarios y respuestas en las incidencias que sigues.
- Las solicitudes de revisión y las incidencias añadidas al triaje.
- Los recordatorios de fechas de vencimiento.

Cada elemento se convierte en una tarea solo cuando requiere tu atención, según lo que dice. Tus propios cambios no se importan. La primera sincronización incluye los últimos 7 días. Las personas se vinculan a tu [Graph](graph.md) mediante la dirección de correo que Linear muestra para cada una.

Si quieres usarlo solo para ejecutar acciones, desactiva **Trae señales** en **Detalles**.

## Qué puede hacer

Cada una de estas acciones espera tu visto bueno en su tarea:

- Comentar en la incidencia de la tarea o responder en un hilo de comentarios. Se publica en tu nombre.
- Cambiar el estado de esa incidencia a otro de los estados de su equipo.
- Asignársela a alguien de su equipo o a ti.
- Crear una incidencia nueva en uno de tus equipos.

Nunca elimina ni archiva incidencias, ni las mueve a otro equipo.

## Conectarla

1. En el panel: **Conexiones**, **+ Añadir**, Linear. O desde la página de configuración de una Machine alojada, en app.themachine.computer/setup: **Más fuentes**, Linear. En tu propio ordenador, primero vincúlala a tu cuenta.
2. Pulsa **Iniciar sesión con Linear**, elige tu espacio de trabajo y autoriza el acceso.
3. Al volver a The Machine, comprueba el inicio de sesión de inmediato y muestra el nombre del espacio de trabajo.

Para conectar otro espacio de trabajo, añade Linear de nuevo. Elige **Trabajo** o **Personal**, como con cualquier otra conexión.

## Pegar una clave de API

En **O pega una clave de API**, pulsa **Consigue tu token**. Linear abre **Ajustes**, **Seguridad y acceso**: crea una clave de API personal, cópiala, pégala y pulsa **Conectar**. En tu propio ordenador, `assistant connect linear` también te la pide.

## Quitarla

- En el panel: **Conexiones**, abre Linear, **Detalles** y luego **Desconectar**. Lo que ya se haya importado se queda.
- En una Machine alojada, también puedes pulsar **Quitar** junto a Linear en la página de configuración.

## Revocar el acceso en Linear

En Linear: **Ajustes**, **Seguridad y acceso** y, en aplicaciones autorizadas, revoca el acceso de The Machine. Si pegaste una clave, revócala en la misma página.
