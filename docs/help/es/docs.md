---
title: Microsoft OneDrive
area: connections
summary: Comentarios, menciones y cambios registrados en tus archivos de Word de OneDrive. Los documentos nuevos y los cambios esperan tu visto bueno.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: c8fca3cf0299e327
---
## Qué lee

**Microsoft OneDrive** lee tus archivos de Word en OneDrive, tanto en una Machine alojada como en tu propio ordenador. No hace falta que conectes Outlook. Para Google Docs, consulta la sección correspondiente más abajo. Trae:

- Comentarios y respuestas en tus archivos de Word, y comentarios en los que te mencionan.
- Cambios registrados en tus archivos de Word.

La primera sincronización incluye los últimos 7 días. Cada elemento enlaza con las personas y los proyectos de tu [Graph](graph.md). Los comentarios que requieren tu atención se convierten en tareas.

## Archivos que otras personas comparten contigo

Microsoft dejará de mostrar estos elementos en noviembre de 2026. A partir de entonces, los archivos compartidos y las menciones en archivos de otras personas solo llegarán a tu Machine como correos de Microsoft. Conecta también [Outlook](microsoft.md) y no desactives esos correos. Una tarea creada a partir de uno de esos correos lo abre, y el botón del correo abre el archivo. No se detectan los archivos compartidos ni las menciones que no vengan en un correo.

## Qué puede hacer

Cuando una tarea necesita el texto de un documento, tu Machine lee ese documento mientras trabaja en la tarea. Puede leer archivos de Word, PDF y texto.

También busca archivos de cualquier tipo en tu propio OneDrive y te da el enlace. No busca en sitios de SharePoint ni en archivos que otras personas hayan compartido contigo. No puede leer el texto de un PDF escaneado.

Puede preparar un borrador de respuesta a un comentario. Word no permite publicar respuestas desde fuera, así que tendrás que copiar el borrador en Word.

Nunca acepta una sugerencia, resuelve un comentario, comparte un archivo ni modifica un documento sin tu visto bueno.

Para usarla solo para realizar acciones, desactiva **Trae señales** en **Detalles**. Así, solo busca y lee los archivos que necesitan tus tareas y crea archivos nuevos.

## Crear y editar documentos

Tu Machine puede crear un documento o modificar uno relacionado con una tarea:

- Puede crear un documento en el momento si la tarea o una habilidad lo pide. Es privado y se guarda en tu propio OneDrive o Google Drive. La tarea muestra **Abrir el documento**. Compartirlo o enviar el enlace espera tu visto bueno.
- Los cambios en un documento existente solo se preparan. Pulsa **Revisar cambios** para ver cada párrafo antes y después, y luego **Guardar**. Los cambios que pidas en el chat de la tarea se aplican de inmediato.
- Solo escribe en el documento tal como lo viste. Si alguien lo ha modificado entretanto, no escribe nada y la tarea te lo indica. Pide un borrador nuevo.
- En Talk, lee en voz alta todos los cambios y espera un sí claro.
- Si Microsoft o Google no permiten crear un documento, la tarea explica por qué y muestra **Revisar y crear** para volver a intentarlo.

Puede sustituir y añadir texto, párrafos y títulos. En Google Docs también puede aplicar formato: negrita, cursiva, subrayado, enlaces, títulos, listas con viñetas y numeradas, y saltos de página. **Revisar cambios** muestra cada cambio. No puede crear tablas, y las imágenes, los cambios registrados y los campos se quedan como están.

El documento de una tarea de trabajo se guarda en la cuenta de esa empresa, nunca en una personal. En tu propio ordenador, una cuenta de Google conectada para Gmail que ya tenga acceso a Drive también puede recibir documentos nuevos de Google Docs. Si no hay ninguna cuenta adecuada, la tarea te indica qué conectar para el trabajo: Microsoft OneDrive o Google Docs, si tu Machine puede usarlo.

Si el documento no es el último paso, por ejemplo, si hay que responder con su enlace, la tarea sigue abierta y prepara un borrador de ese paso para que des tu visto bueno.

La edición se incluye al conectar la cuenta. Si una conexión antigua solo permite leer, verás **Permitir cambios** en **Conexiones**. Púlsalo una vez y acepta.

## Qué permisos solicita

Microsoft te pide un único visto bueno para leer y modificar tus archivos, incluidos los que se han compartido contigo. Cada cambio sigue esperando tu visto bueno en la tarea correspondiente. El acceso al correo y al calendario no cambia.

Si más adelante retiras ese permiso, Microsoft OneDrive mostrará **Esperando tu visto bueno para leer documentos** en **Conexiones**.

## Conectarlo

En una Machine alojada o en tu propio ordenador vinculado a tu cuenta:

- Abre **Conexiones**, luego **Documentos y archivos** y selecciona **Microsoft OneDrive**.
- Pulsa **Iniciar sesión con Microsoft** y permite que lea y edite tus archivos.

Si Microsoft no permite la lectura, la conexión no se añade. Si pulsas **Permitir cambios** y Microsoft no permite editar, te lo indicará.

## Google Docs

En una Machine alojada, abre **Conexiones**, luego **Documentos y archivos** y selecciona **Google Docs**. Google te pide permiso para ver y editar los documentos que le indiques y crear documentos nuevos. No hace falta que conectes Gmail y el acceso a Gmail no cambia.

Entonces, tu Machine:

- Lee un documento de Google Docs enlazado en los mensajes de una tarea o pegado en su chat, solo mientras trabaja en esa tarea.
- Prepara cambios en ese documento. Cada cambio espera tu visto bueno, como se explica más arriba.
- Crea documentos privados en tu Google Drive.

No busca en tu Drive. Solo ve comentarios, archivos compartidos y sugerencias en los documentos que ha creado. Para ver más, necesitaría acceso a todo tu Drive, y no lo solicita.

## Google Sheets y Slides

Si Google Docs muestra **Permitir el acceso a Sheets y Slides** en **Conexiones**, pulsa esa opción y permite el acceso a ambos servicios. Google te pide permiso para que tu Machine vea tus archivos de Sheets y Slides. No puede modificarlos.

Entonces, tu Machine también lee un archivo de Google Sheets o Slides enlazado en los mensajes de una tarea o pegado en su chat, solo mientras trabaja en esa tarea:

- De una hoja de cálculo, primero lee la pestaña o las celdas enlazadas y después las demás pestañas, hasta un máximo de 2,000 celdas. Las fórmulas aparecen como sus valores. Las pestañas ocultas solo se leen si se enlazan o se solicitan.
- De las presentaciones, lee el texto y las notas del orador en orden. No lee las imágenes ni los gráficos.

Si el archivo es grande, indica en el chat a qué pestaña, celdas o diapositivas te refieres. Si el archivo es privado de otra persona, se ha eliminado o es un archivo de Excel o PowerPoint, la tarea te lo indica. Un enlace de Google Drive funciona igual si lleva a un archivo de Google Docs, Sheets o Slides.

## Google Docs en tu propio ordenador

En tu propio ordenador, tu Machine puede crear un documento de Google Docs en una cuenta de Gmail que tenga la sesión iniciada y ya tenga acceso a Drive. No lee tus otros documentos de Google Docs ni sus comentarios. **Documentos y archivos** lo muestra como Google Docs, en esa cuenta. También puede modificar allí un documento que haya creado para una tarea.

También lee archivos de Google Sheets o Slides enlazados en una tarea o pegados en su chat, si esa sesión de Google ya tiene acceso a Drive, Sheets o Slides. Nunca pide más permisos a Google. Si Google no lo permite, activa la API de Google Sheets o Slides en el proyecto de Google de esa cuenta.

## Trabajo o personal

La conexión sigue la etiqueta Trabajo o Personal, como ocurre con el correo. Los documentos de trabajo pueden llegar al Graph de tu equipo según tus [reglas para compartir](sharing-rules.md). Los documentos personales nunca llegan.

## Desconectarlo

Abre **Conexiones**, selecciona Microsoft OneDrive o Google Docs, y luego **Detalles** y **Desconectar**. Dejará de leer, pero conservará lo que ya haya importado. En una Machine alojada, **Desconectar ↗** abre la página de configuración, donde se guarda la sesión.
