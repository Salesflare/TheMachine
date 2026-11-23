---
title: Microsoft OneDrive
area: connections
summary: Comentarios, menciones y cambios controlados en tus archivos de Word de OneDrive. Los documentos nuevos y los cambios esperan tu visto bueno.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 41e5651f29782588
---
## Qué lee

**Microsoft OneDrive** lee tus archivos de Word de OneDrive, tanto en una Machine alojada como en tu propio ordenador. No hace falta conectar Outlook. Para Google Docs, consulta la sección de abajo. Trae:

- Comentarios y respuestas en tus archivos de Word, y comentarios en los que te mencionan.
- Cambios controlados en tus archivos de Word.

La primera sincronización incluye los 7 días anteriores. Cada elemento enlaza con las personas y los proyectos de tu [Graph](graph.md). Los comentarios que requieren tu atención se convierten en tareas.

## Archivos que otras personas comparten contigo

Microsoft dejará de mostrar estos archivos en noviembre de 2026. A partir de entonces, los archivos compartidos y las menciones en archivos de otras personas solo llegarán a tu Machine como correos de Microsoft. Conecta también [Outlook](microsoft.md) y mantén esos correos activados. Una tarea creada a partir de uno de esos correos lo abre, y su botón abre el archivo. No se detectan los archivos compartidos ni las menciones que no vengan con un correo.

## Qué puede hacer

Cuando una tarea necesita el texto de un documento, tu Machine lee ese documento, solo mientras trabaja en esa tarea. Puede leer archivos de Word, PDF y texto.

También busca archivos de cualquier tipo en tu propio OneDrive y te da el enlace. No busca en sitios de SharePoint ni en archivos que se han compartido contigo. No puede leer el texto de un PDF escaneado.

Puede redactar una respuesta a un comentario. Word no permite publicar respuestas desde fuera, así que tendrás que copiar el borrador en Word.

Nunca acepta una sugerencia, resuelve un comentario, comparte un archivo ni cambia un documento sin tu visto bueno.

Para usarla solo para hacer cosas, desactiva **Trae señales** en **Detalles**. Entonces solo busca y lee los archivos que necesitan tus tareas, y crea otros nuevos.

## Crear y editar documentos

Tu Machine puede crear un documento nuevo o modificar uno relacionado con una tarea:

- Crea un documento nuevo de inmediato cuando la tarea o una habilidad lo pide. Es privado y se guarda en tu propio OneDrive o Google Drive. La tarea muestra **Abrir el documento**. Compartirlo o enviar su enlace espera tu visto bueno.
- Los cambios en un documento existente solo los prepara. Pulsa **Revisar cambios** para ver cada párrafo antes y después, y luego **Guardar**. Si pides un cambio en el chat de la tarea, lo hace de inmediato.
- Solo escribe en el documento tal como lo viste. Si alguien lo ha cambiado entretanto, no escribe nada y la tarea te lo indica. Pide un nuevo borrador.
- En Talk, lee en voz alta todos los cambios y espera un sí claro.
- Si Microsoft o Google no permite crear un documento, la tarea explica el motivo y muestra **Revisar y crear** para volver a intentarlo.

Puede reemplazar y añadir texto, párrafos y encabezados. Las tablas, imágenes, cambios controlados y campos se mantienen tal como están.

El documento de una tarea de trabajo se guarda en la cuenta de esa empresa, nunca en una cuenta personal. En tu propio ordenador, una cuenta de Google conectada para Gmail que ya tenga acceso a Drive también puede crear documentos de Google. Si no hay ninguna cuenta adecuada, la tarea te indica qué conectar para el trabajo: Microsoft OneDrive o Google Docs, si tu Machine puede usarlo.

Si el documento no es el último paso, por ejemplo, si hay que responder con su enlace, la tarea sigue abierta y prepara ese paso para que des tu visto bueno.

La conexión incluye la posibilidad de editar. Si una conexión anterior solo permite leer, aparece **Permitir cambios** en **Conexiones**. Pulsa esa opción una vez y acepta.

## Qué permisos solicita

Microsoft te pide un único visto bueno: leer y modificar tus archivos, incluidos los que se han compartido contigo. Cada cambio sigue esperando tu visto bueno en su tarea. El acceso al correo y al calendario no cambia.

Si más adelante retiras ese visto bueno, Microsoft OneDrive muestra **Esperando tu visto bueno para leer documentos** en **Conexiones**.

## Conectarlo

En una Machine alojada o en tu propio ordenador, emparejado con tu cuenta:

- Abre **Conexiones**, luego **Documentos y archivos**, y elige **Microsoft OneDrive**.
- Pulsa **Iniciar sesión con Microsoft** y permite que lea y edite tus archivos.

Si Microsoft no permite la lectura, no se añade. Si pulsas **Permitir cambios** y Microsoft no permite editar, te lo indica.

## Google Docs

En una Machine alojada, abre **Conexiones**, luego **Documentos y archivos**, y elige **Google Docs**. Google te pide permiso para ver y editar los documentos que le indiques y crear otros nuevos. No hace falta conectar Gmail, y el acceso a tu Gmail no cambia.

Después, tu Machine:

- Lee los documentos de Google enlazados en los mensajes de una tarea, solo mientras trabaja en ella.
- Prepara cambios en esos documentos. Cada cambio espera tu visto bueno, como se explica arriba.
- Crea documentos privados en tu Google Drive.

No busca en tu Drive. Solo ve los comentarios, los archivos compartidos y las sugerencias de los documentos que ha creado. Para acceder a más contenido tendría que acceder a todo tu Drive, y no lo solicita.

En tu propio ordenador, tu Machine puede crear un documento de Google en una cuenta de Gmail que tenga la sesión iniciada y ya tenga acceso a Drive. No lee tus otros documentos de Google ni sus comentarios. **Documentos y archivos** la muestra como Google Docs en esa cuenta. También puede modificar un documento que haya creado allí para una tarea.

## Trabajo o personal

Sigue la etiqueta Trabajo o Personal de su conexión, igual que con el correo. Los documentos de trabajo pueden llegar al Graph de tu equipo según tus [reglas para compartir](sharing-rules.md). Los personales no llegan nunca.

## Desconectarlo

Abre **Conexiones**, luego Microsoft OneDrive o Google Docs, **Detalles** y **Desconectar**. Deja de leer. Lo que ya haya incorporado se mantiene. En una Machine alojada, **Desconectar ↗** abre la página de configuración, donde se guarda la sesión iniciada.
