---
title: Google Docs y Word
area: connections
summary: Comentarios, menciones, sugerencias de edición y archivos compartidos en tus documentos de Google Docs o Word. Lee, y publica una respuesta a un comentario solo cuando das el OK.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
---
## Qué lee

Docs usa el inicio de sesión de Google o Microsoft que ya tienes para esa dirección. Trae:

- Documentos que alguien comparte contigo.
- Comentarios y respuestas en documentos tuyos, y comentarios que te mencionan.
- Sugerencias de edición en documentos de Google Docs tuyos, y control de cambios en archivos de Word tuyos.

La primera sincronización mira 30 días atrás. Cada cosa se convierte en un evento, vinculado a las personas y proyectos de tu [Graph](graph.md). Cuando un comentario te necesita, se convierte en una tarea.

## Qué puede hacer

Cuando una tarea necesita el texto de un documento, tu Machine lee ese documento, y solo mientras trabaja en esa tarea.

Puede redactar una respuesta a un comentario. En Google Docs, la respuesta espera en la tarea: pulsa **Revisar y publicar**, revísala y luego **Publicar ahora**. No se publica nada hasta que lo hagas. Los archivos de Word no permiten publicar una respuesta desde fuera de Word, así que esas respuestas se quedan como borradores para que las copies en Word.

Nunca edita un documento, acepta una sugerencia, resuelve un comentario ni comparte un archivo.

## Qué pide

Leer documentos necesita su propio OK, aparte del inicio de sesión de tu correo. Tu acceso a Gmail y al calendario se queda como está.

- Google: acceso de solo lectura a tus archivos y comentarios de Drive. Publicar respuestas necesita un OK más, que puedes omitir.
- Microsoft: acceso de lectura a tus archivos, incluidos los que se comparten contigo en OneDrive y SharePoint.

Si más tarde se retira ese OK, la tarjeta de Docs dice **Esperando tu OK para leer documentos**.

## Conéctalo

En una Machine alojada, Docs aparece en **+ Añadir** en cuanto tu página de configuración lo ofrezca.

En tu propio ordenador:

1. Conecta primero Gmail u Outlook para esa dirección.
2. Abre **Conexiones**, luego **+ Añadir**, elige Docs e introduce esa dirección. O ejecuta `assistant connect docs`.
3. Comprueba que tu inicio de sesión puede leer documentos. Sin ese OK no se añade.

## Trabajo o personal

Docs sigue la etiqueta de trabajo o personal de su conexión, como el correo. Los documentos de trabajo pueden llegar al Graph de tu equipo según tus [reglas para compartir](sharing-rules.md). Los personales nunca.

## Quítalo

En el panel: **Conexiones**, abre Docs, **Detalles** y luego **Desconectar**. Deja de leer. Lo que ya trajo se queda.
