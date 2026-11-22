---
title: Microsoft OneDrive
area: connections
summary: Comentarios, menciones, cambios registrados y archivos compartidos en tus documentos de Word en OneDrive y SharePoint. Los documentos nuevos y los cambios esperan tu visto bueno.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: b06d8ca4f35e5a38
---
## Qué lee

**Microsoft OneDrive** lee tus documentos de Word en OneDrive y SharePoint, tanto en una Machine alojada como en tu propio ordenador. No hace falta conectar Outlook. Para Google Docs, consulta la sección de abajo. Trae:

- Documentos que alguien comparte contigo.
- Comentarios y respuestas en tus documentos, y comentarios que te mencionan.
- Cambios controlados en tus documentos de Word.

La primera sincronización incluye los últimos 7 días. Cada elemento enlaza con las personas y los proyectos de tu [Graph](graph.md). Un comentario que requiere tu atención se convierte en una tarea.

## Qué puede hacer

Cuando una tarea necesita el texto de un documento, tu Machine lee ese documento, solo mientras trabaja en esa tarea.

Puede preparar un borrador de respuesta a un comentario. Word no permite publicar respuestas desde fuera, así que tienes que copiar el borrador en Word.

Nunca acepta una sugerencia, resuelve un comentario, comparte un archivo ni modifica un documento sin tu visto bueno.

Para usarlo solo para hacer cosas, desactiva **Trae señales** en **Detalles**. Así solo busca y lee los documentos que necesitan tus tareas, y crea documentos nuevos.

## Crear y editar documentos

Tu Machine puede crear un documento nuevo o modificar uno relacionado con una tarea:

- Crea un documento nuevo de inmediato cuando la tarea o una habilidad lo solicita. Es privado y se guarda en tu OneDrive o Google Drive. La tarea muestra **Abrir el documento**. Compartirlo o enviar su enlace espera tu visto bueno.
- Solo prepara los cambios en un documento existente. Pulsa **Revisar cambios** para ver cada párrafo antes y después, y luego **Guardar**. Si pides un cambio en el chat de la tarea, lo hace de inmediato.
- Solo escribe en el documento tal como lo viste. Si alguien lo modificó mientras tanto, no escribe nada y la tarea te lo indica. Pide un borrador nuevo.
- En Talk, lee en voz alta todo el cambio y espera un sí claro.
- Si Microsoft o Google no permite crear un documento, la tarea explica por qué y muestra **Revisar y crear** para volver a intentarlo.

Puede reemplazar y añadir texto, párrafos y encabezados. Las tablas, imágenes, cambios controlados y campos se mantienen tal como están.

El documento de una tarea de Trabajo se guarda en la cuenta de esa empresa, nunca en una cuenta personal. En tu propio ordenador, una cuenta de Google conectada para Gmail con acceso a Drive también puede crear documentos nuevos de Google Docs. Si no hay ninguna cuenta adecuada, la tarea te indica qué conectar para Trabajo: Microsoft OneDrive o Google Docs, si tu Machine puede usarlo.

Si el documento no es el último paso, por ejemplo, si hay que responder con su enlace, la tarea sigue abierta y prepara ese paso para que des el visto bueno.

La edición se incluye al conectar. Una conexión antigua que solo permite leer muestra **Permitir cambios** en **Conexiones**. Pulsa esa opción una vez y acepta.

## Qué permisos solicita

Microsoft te pide una sola autorización para leer y modificar tus archivos, incluidos los que se comparten contigo. Cada cambio sigue esperando tu visto bueno en la tarea correspondiente. El acceso al correo y al calendario no cambia.

Si más adelante retiras esa autorización, Microsoft OneDrive muestra **Esperando tu visto bueno para leer documentos** en **Conexiones**.

## Conectarlo

En una Machine alojada o en tu propio ordenador vinculado a tu cuenta:

- Abre **Conexiones**, luego **Documentos y archivos** y elige **Microsoft OneDrive**.
- Pulsa **Iniciar sesión con Microsoft** y permite que lea y edite tus archivos.

Si Microsoft no permite la lectura, no se añade. Si pulsas **Permitir cambios** y Microsoft no permite la edición, te lo indica.

## Google Docs

En una Machine alojada, abre **Conexiones**, luego **Documentos y archivos** y elige **Google Docs**. Google te pide permiso para ver y editar los documentos que le indiques y crear documentos nuevos. No hace falta conectar Gmail y el acceso a Gmail no cambia.

Entonces tu Machine:

- Lee un documento de Google Docs enlazado en los mensajes de una tarea, solo mientras trabaja en esa tarea.
- Prepara cambios en ese documento. Cada cambio espera tu visto bueno, como se explicó arriba.
- Crea documentos nuevos y privados en tu Google Drive.

No busca en tu Drive. Solo ve comentarios, archivos compartidos y sugerencias en los documentos que creó. Para acceder a más documentos necesitaría acceso a todo tu Drive, y no lo solicita.

En tu propio ordenador, tu Machine puede crear un documento nuevo de Google Docs en una cuenta de Gmail que tenga la sesión iniciada allí y ya tenga acceso a Drive. No lee tus otros documentos de Google Docs ni sus comentarios. **Documentos y archivos** la muestra como Google Docs, en esa cuenta. También puede modificar allí un documento que haya creado para una tarea.

## Trabajo o personal

Sigue la etiqueta Trabajo o Personal de su conexión, igual que con el correo. Los documentos de Trabajo pueden llegar al Graph de tu equipo según tus [reglas para compartir](sharing-rules.md). Los documentos personales nunca llegan.

## Desconectarlo

Abre **Conexiones**, luego Microsoft OneDrive o Google Docs, **Detalles** y **Desconectar**. Deja de leer documentos. Lo que ya había incorporado se conserva. En una Machine alojada, **Desconectar ↗** abre la página de configuración, donde se guarda el inicio de sesión.
