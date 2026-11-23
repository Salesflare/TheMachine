---
title: Notion
area: connections
summary: Comentarios, menciones y tareas de Notion asignadas a ti. Las respuestas, las páginas nuevas, las ediciones y marcar tareas como hechas requieren tu visto bueno.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 2e93c261cc09e401
---
## Qué lee

Las páginas que puede ver tu conexión de Notion. Incluye:

- Comentarios en tus páginas, respuestas en conversaciones en las que participas y comentarios que te mencionan. Si uno requiere que intervengas, se convierte en una tarea.
- Elementos de bases de datos asignados a ti, con su fecha de vencimiento y estado. Cada uno se convierte en una tarea y su fecha de vencimiento aparece en **Calendario**. Cuando el elemento se marca como hecho en Notion, la tarea se cierra automáticamente. **Deshacer** la vuelve a abrir.
- Páginas nuevas que añade otra persona y que puedes ver.
- Un aviso discreto cuando alguien cambia una página que pediste que modificaran. No emite ningún sonido.

La primera sincronización incluye los últimos 7 días. Las personas se vinculan a tu [Graph](graph.md) por su dirección de correo. Si Notion no comparte una, se vinculan por su nombre completo, siempre que haya una sola persona con ese nombre en tu Graph.

Para usarlo solo para hacer cosas, desactiva **Trae señales** en **Detalles**.

## Qué puede hacer

Cuando una tarea o una reunión necesita el texto de una página, tu Machine lee esa página mientras trabaja en ella. De los archivos de la página, solo ve el nombre. Busca páginas por su título, no por los archivos que contienen.

Necesitas dar el visto bueno a cada una de estas acciones desde su tarea:

- Responder a un comentario en su conversación.
- Crear una página nueva. Es privada hasta que la compartas.
- Editar una página. Pulsa **Revisar cambios** para ver cada párrafo antes y después y, luego, **Guardar**. Solo escribe en la página tal como la viste. Si alguien la ha cambiado entretanto, no escribe nada y la tarea te lo indica.
- Marcar como hecha una tarea que tienes asignada. Solo cambia su estado.

Nunca elimina, comparte ni mueve páginas.

## Conectarlo

1. En el panel: **Conexiones**, **Documentos y archivos**, Notion. O, en la página de configuración de una Machine alojada, en app.themachine.computer/setup: **Más fuentes**, Notion. Si usas tu propio ordenador, primero vincula Notion con tu cuenta.
2. Pulsa **Iniciar sesión con Notion**, elige tu espacio de trabajo y las páginas que puede ver, y permite el acceso.
3. Al volver a The Machine, comprueba la conexión de inmediato y muestra el nombre del espacio de trabajo.

Para conectar otro espacio de trabajo, añade Notion de nuevo.

## Pegar un token

En **O pega un token de integración**, pulsa **Consigue tu token**. Notion abre su página de integraciones: crea una integración interna, permite leer e insertar contenido y comentarios, y leer información de usuarios con sus direcciones de correo. Copia el token, pégalo y pulsa **Conectar**.

Después, comparte tus páginas con la integración en Notion, en **Conexiones** dentro de cada página. Si usas tu propio ordenador, `assistant connect notion` también te lo pide.

## Quitar la conexión

- En el panel: **Conexiones**, abre Notion, pulsa **Detalles** y luego **Desconectar**. Lo que ya se ha importado se conserva.
- Si usas una Machine alojada, también puedes pulsar **Quitar** junto a Notion en la página de configuración.

## Revocar el acceso en Notion

En Notion: **Ajustes**, **Conexiones** y desconecta The Machine. Si usas un token, elimina la integración en la página de integraciones.
