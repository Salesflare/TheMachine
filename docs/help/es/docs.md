---
title: Microsoft OneDrive
area: connections
summary: Comentarios, menciones y cambios registrados en tus archivos de Word de OneDrive. Los documentos nuevos y las modificaciones esperan tu visto bueno.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: d79388a1c8811d5f
---
## Qué lee

**Microsoft OneDrive** lee tus archivos de Word de OneDrive, tanto en una Machine alojada como en tu ordenador. No hace falta conectar Outlook. Para Google Docs, consulta la sección de abajo. Trae:

- Comentarios y respuestas en tus archivos de Word, y los comentarios que te mencionan.
- Cambios registrados en tus archivos de Word.

La primera sincronización abarca los últimos 7 días. Cada elemento enlaza con las personas y los proyectos de tu [Graph](graph.md). Un comentario que necesita tu atención se convierte en una tarea.

## Archivos que otras personas comparten contigo

Microsoft dejará de mostrar estas comparticiones en noviembre de 2026. A partir de entonces, las comparticiones y las menciones en archivos de otras personas solo llegarán a tu Machine por medio de los correos de Microsoft. Conecta también [Outlook](microsoft.md) y mantén activados esos correos. Una tarea creada a partir de uno de ellos abre el correo, y su botón abre el archivo. No detecta las comparticiones ni las menciones que no lleguen por correo.

## Qué puede hacer

Cuando una tarea necesita el texto de un documento, tu Machine lee ese documento mientras trabaja en la tarea. Puede leer archivos de Word, PDF y texto.

También busca archivos de cualquier tipo en tu propio OneDrive y te da el enlace. No busca en sitios de SharePoint ni en archivos que otras personas hayan compartido contigo. No puede leer el texto de un PDF escaneado.

Puede preparar una respuesta a un comentario. Word no permite publicar respuestas desde fuera, así que tendrás que copiar el borrador en Word.

Nunca acepta una sugerencia, resuelve un comentario, comparte un archivo ni modifica un documento sin tu visto bueno.

Para usarla solo para realizar acciones, desactiva **Trae señales** en **Detalles**. Así solo busca y lee los archivos que necesitan tus tareas, y crea otros nuevos.

## Crear y editar documentos

Tu Machine puede escribir un documento nuevo o modificar uno relacionado con una tarea:

- Crea un documento nuevo de inmediato cuando una tarea o una habilidad lo pide. Es privado y se guarda en tu propio OneDrive o Google Drive. La tarea muestra **Abrir el documento**. Compartirlo o enviar su enlace espera tu visto bueno.
- Los cambios en un documento existente se preparan primero. Pulsa **Revisar cambios** para ver cada párrafo antes y después, y luego **Guardar**. Si pides un cambio en el chat de la tarea, lo hace de inmediato.
- Solo escribe en el documento tal como lo viste. Si alguien lo ha modificado mientras tanto, no escribe nada y te lo indica en la tarea. Pide un borrador nuevo.
- En Talk, lee en voz alta todo el cambio y espera un sí claro.
- Si Microsoft o Google no permite crear un documento, la tarea explica el motivo y muestra **Revisar y crear** para volver a intentarlo.

Puede reemplazar y añadir texto, párrafos y encabezados. Las tablas, las imágenes, los cambios registrados y los campos se mantienen tal como están.

El documento de una tarea de Trabajo se guarda en la cuenta de esa empresa, nunca en una personal. En tu ordenador, una cuenta de Google conectada para Gmail que tenga acceso a Drive también puede crear documentos de Google. Si no hay ninguna cuenta adecuada, la tarea te indica qué conectar para Trabajo: Microsoft OneDrive o Google Docs, si tu Machine puede usarlo.

Si el documento no es el último paso, por ejemplo, si hay que responder con su enlace, la tarea sigue abierta y prepara un borrador de ese paso para que des tu visto bueno.

La edición se incluye al conectar. Una conexión antigua que solo permite leer muestra **Permitir cambios** en **Conexiones**. Pulsa esa opción una vez y acepta.

## Qué permisos solicita

Microsoft te pide un único visto bueno para leer y modificar tus archivos, incluidos los que otras personas han compartido contigo. Cada cambio sigue esperando tu visto bueno en la tarea correspondiente. El acceso al correo y al calendario no cambia.

Si más adelante retiras ese permiso, Microsoft OneDrive muestra **Esperando tu visto bueno para leer documentos** en **Conexiones**.

## Conectarlo

En una Machine alojada o en tu ordenador vinculado a tu cuenta:

- Abre **Conexiones**, luego **Documentos y archivos**, y elige **Microsoft OneDrive**.
- Pulsa **Iniciar sesión con Microsoft** y permite que lea y modifique tus archivos.

Si Microsoft no permite la lectura, no se añade. Si pulsas **Permitir cambios** y Microsoft no permite las modificaciones, te lo indica.

## Google Docs

En una Machine alojada, abre **Conexiones**, luego **Documentos y archivos**, y elige **Google Docs**. Google te pide permiso para ver y modificar los documentos que le indiques, y crear otros nuevos. No hace falta conectar Gmail y el acceso a Gmail no cambia.

A partir de ahí, tu Machine:

- Lee un documento de Google enlazado en los mensajes de una tarea o pegado en su chat, solo mientras trabaja en esa tarea.
- Prepara cambios en ese documento. Cada uno espera tu visto bueno, como se explica arriba.
- Crea documentos privados en tu Google Drive.

No busca en tu Drive. Solo ve los comentarios, las comparticiones y las sugerencias de los documentos que ha creado. Para acceder a más documentos tendría que tener acceso a todo tu Drive, pero no lo solicita.

## Google Sheets y Slides

Si Google Docs muestra **Permitir el acceso a Sheets y Slides** en **Conexiones**, pulsa esa opción y permite el acceso a ambos. Google te pide permiso para que tu Machine vea tus archivos de Sheets y Slides. No puede modificarlos.

A partir de ahí, tu Machine también lee un archivo de Google Sheets o Slides enlazado en los mensajes de una tarea o pegado en su chat, solo mientras trabaja en esa tarea:

- De una hoja de cálculo, lee primero la pestaña o las celdas enlazadas y luego las demás pestañas, hasta 2.000 celdas. Las fórmulas aparecen como sus valores. Solo lee las pestañas ocultas si están enlazadas o se lo pides.
- De una presentación, lee el texto y las notas del presentador en orden. No lee las imágenes ni los gráficos.

Si el archivo es grande, pide en el chat la pestaña, las celdas o las diapositivas que quieres. Si el archivo es privado de otra persona, se ha eliminado o es un archivo de Excel o PowerPoint, la tarea te lo indica. Un enlace de Google Drive funciona igual si lleva a un documento, una hoja de cálculo o una presentación de Google.

## Google Docs en tu ordenador

En tu ordenador, tu Machine puede crear un documento de Google en una cuenta de Gmail con la sesión iniciada que ya tenga acceso a Drive. No lee tus otros documentos de Google ni sus comentarios. **Documentos y archivos** lo muestra como Google Docs en esa cuenta. También puede modificar allí un documento que haya creado para una tarea.

También lee un archivo de Google Sheets o Slides enlazado en una tarea o pegado en su chat si esa sesión de Google ya tiene acceso a Drive, Sheets o Slides. Nunca pide más permisos a Google. Si Google no da acceso, activa la API de Google Sheets o Slides en el propio proyecto de Google de esa cuenta.

## Trabajo o personal

Sigue la etiqueta Trabajo o Personal de su conexión, igual que el correo. Los documentos de Trabajo pueden llegar al Graph de tu equipo según tus [reglas para compartir](sharing-rules.md). Los personales nunca llegan.

## Desconectarlo

Abre **Conexiones**, luego Microsoft OneDrive o Google Docs, **Detalles** y **Desconectar**. Dejará de leer. Lo que ya haya incorporado se conserva. En una Machine alojada, **Desconectar ↗** abre la página de configuración que guarda la sesión.
