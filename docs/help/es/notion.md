---
title: Notion
area: connections
summary: Comentarios, menciones y tareas que tienes asignadas en Notion. Las respuestas, páginas nuevas, ediciones y tareas marcadas como hechas esperan tu aprobación.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 8544baf8c60cc40b
---
## Qué lee

Las páginas que puede ver tu conexión de Notion. Incluye:

- Comentarios en tus páginas, respuestas en conversaciones en las que participas y comentarios que te mencionan. Si uno requiere que intervengas, se convierte en una tarea.
- Elementos de bases de datos que tienes asignados, con su fecha de vencimiento y estado. Cada uno se convierte en una tarea, y su fecha de vencimiento aparece en **Calendario**. Cuando el elemento se marca como hecho en Notion, la tarea se cierra automáticamente. **Deshacer** la vuelve a abrir.
- Páginas nuevas que añadan otras personas y que puedas ver.
- Un aviso discreto cuando alguien cambia una página que pediste que modificaran. Nunca te envía una notificación sonora.

La primera sincronización incluye los últimos 7 días. Las personas se vinculan a tu [Graph](graph.md) por su dirección de correo. Si Notion no comparte una, solo se vinculan cuando el nombre completo coincide exactamente con el de una sola persona de tu Graph.

Para usarla solo para hacer cosas, desactiva **Trae señales** en **Detalles**.

## Qué puede hacer

Cuando una tarea o una reunión necesita el texto de una página, tu Machine lee esa página solo mientras trabaja en ella.

Cada una de estas acciones espera tu aprobación en su tarea:

- Responder a un comentario dentro de su conversación.
- Crear una página nueva. Es privada hasta que la compartas.
- Editar una página. Pulsa **Revisar cambios** para ver cada párrafo antes y después, y luego **Guardar**. Solo escribe en la página tal como la viste. Si alguien la cambia mientras tanto, no se escribe nada y la tarea te lo indica.
- Marcar como hecha una tarea que tienes asignada. Solo cambia su estado.

Nunca elimina, comparte ni mueve una página.

## Conectarla

1. En el panel: **Conexiones**, **Documentos y archivos**, Notion. O, en la página de configuración de una Machine alojada en app.themachine.computer/setup: **Más fuentes**, Notion. En tu propio ordenador, primero vincúlala con tu cuenta.
2. Pulsa **Inicia sesión con Notion**, elige tu espacio de trabajo y las páginas que puede ver, y autoriza el acceso.
3. Al volver a The Machine, comprobará el inicio de sesión de inmediato y mostrará el nombre del espacio de trabajo.

Para conectar otro espacio de trabajo, vuelve a añadir Notion.

## Pegar un token en su lugar

En **O pega un token de integración**, pulsa **Consigue tu token**. Notion abrirá su página de integraciones: crea una integración interna, permite leer e insertar contenido y comentarios, y leer información de usuarios con sus direcciones de correo. Copia el token, pégalo y pulsa **Conectar**.

Después, comparte tus páginas con la integración en Notion, en **Conexiones** de cada página. En tu propio ordenador, `assistant connect notion` también te lo pide.

## Quitar la conexión

- En el panel: **Conexiones**, abre Notion y ve a **Detalles**. Luego pulsa **Desconectar**. Lo que ya se haya importado se queda.
- En una Machine alojada, también puedes pulsar **Quitar** junto a Notion en la página de configuración.

## Revocar el acceso en Notion

En Notion, ve a **Configuración**, **Conexiones** y desconecta The Machine. Si usaste un token, elimina la integración en la página de integraciones.
