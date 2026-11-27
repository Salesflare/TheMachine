---
title: Microsoft OneDrive
area: connections
summary: Comentarios, menciones y cambios controlados en tus archivos de Word en OneDrive. Los documentos nuevos y los cambios esperan tu visto bueno.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: e931920c74158c98
---
## Qué lee

**Microsoft OneDrive** lee tus archivos de Word en OneDrive, tanto en una Machine alojada como en tu propio ordenador. No hace falta conectar Outlook. Para Google Docs, consulta la sección de abajo. Trae:

- Comentarios y respuestas en tus archivos de Word, incluidos los comentarios que te mencionan.
- Cambios controlados en tus archivos de Word.

La primera sincronización abarca los últimos 7 días. Cada elemento enlaza con las personas y los proyectos de tu [Graph](graph.md). Los comentarios que requieren tu atención se convierten en tareas.

## Archivos que otras personas comparten contigo

Microsoft dejará de mostrarlos en noviembre de 2026. A partir de entonces, los archivos compartidos y las menciones en archivos de otras personas solo llegarán a tu Machine a través de los correos de Microsoft. Conecta también [Outlook](microsoft.md) y mantén esos correos activados. Una tarea creada a partir de uno de esos correos lo abre, y el botón del correo abre el archivo. No se detectan los archivos compartidos ni las menciones que no vienen acompañados de un correo.

## Qué puede hacer

Cuando una tarea necesita el texto de un documento, tu Machine lee solo ese documento y únicamente mientras trabaja en esa tarea. Puede leer archivos de Word, PDF y texto.

También busca archivos de cualquier tipo en tu OneDrive y te da el enlace. No busca en sitios de SharePoint ni en archivos que se hayan compartido contigo. No puede leer el texto de un PDF escaneado.

Puede redactar una respuesta a un comentario. Word no permite publicar respuestas desde fuera, así que tendrás que copiar el borrador en Word.

Nunca acepta una sugerencia, resuelve un comentario, comparte un archivo ni modifica un documento sin tu visto bueno.

Para usarla solo para realizar tareas, desactiva **Trae señales** en **Detalles**. Entonces solo buscará y leerá los archivos que necesiten tus tareas, y creará archivos nuevos.

## Crear y editar documentos

Tu Machine puede crear un documento o modificar uno relacionado con una tarea:

- Puede crear un documento nuevo en el momento si la tarea o una habilidad lo pide. Será privado y estará en tu OneDrive o Google Drive personal. La tarea mostrará **Abrir el documento**. Compartirlo o enviar el enlace esperará a tu visto bueno.
- Los cambios en un documento existente solo se preparan. Pulsa **Revisar cambios** para ver cada párrafo antes y después, y luego **Guardar**. Los cambios que pidas en el chat de la tarea se hacen en el momento.
- Solo escribe en el documento tal como lo viste. Si alguien lo ha modificado mientras tanto, no se escribe nada y la tarea te lo indica. Pide un nuevo borrador.
- En Talk, lee en voz alta todos los cambios y espera un sí claro.
- Si Microsoft o Google no permiten crear un documento, la tarea te explica el motivo y muestra **Revisar y crear** para volver a intentarlo.

Puede reemplazar y añadir texto, párrafos y encabezados. En Google Docs también puede aplicar formato: negrita, cursiva, subrayado, enlaces, encabezados, listas con viñetas y numeradas, y saltos de página. **Revisar cambios** muestra cada cambio. No puede crear tablas. Las imágenes, los cambios controlados y los campos se mantienen tal como están.

Los documentos de una tarea de trabajo van a la cuenta de esa empresa, nunca a una cuenta personal. En tu propio ordenador, una cuenta de Google conectada para Gmail con acceso a Drive también puede crear documentos de Google. Si no hay ninguna cuenta adecuada, la tarea te indica qué conectar para el trabajo: Microsoft OneDrive o Google Docs, si tu Machine puede usarlo.

Si el documento no es el último paso, por ejemplo, si hay que responder con su enlace, la tarea sigue abierta y prepara ese paso para que des tu visto bueno.

La edición está incluida al conectar. Si una conexión antigua solo permite leer, verás **Permitir cambios** en **Conexiones**. Púlsalo una vez y acepta.

## Qué permisos solicita

Microsoft te pide un solo visto bueno para leer y modificar tus archivos, incluidos los que se han compartido contigo. Los cambios siguen esperando tu visto bueno en cada tarea. El acceso al correo y al calendario no cambia.

Si más adelante retiras ese permiso, Microsoft OneDrive mostrará **Esperando tu visto bueno para leer documentos** en **Conexiones**.

## Conectarlo

En una Machine alojada o en tu propio ordenador vinculado a tu cuenta:

- Abre **Conexiones**, ve a **Documentos y archivos** y elige **Microsoft OneDrive**.
- Pulsa **Iniciar sesión con Microsoft** y permite que lea y edite tus archivos.

Si Microsoft no permite la lectura, no se añadirá. Si pulsas **Permitir cambios** y Microsoft no permite editar, te lo indicará.

## Google Docs

En una Machine alojada, abre **Conexiones**, ve a **Documentos y archivos** y elige **Google Docs**. Google te pide permiso para ver y editar los documentos que le indiques y crear otros nuevos. No hace falta conectar Gmail y el acceso a Gmail no cambia.

Después, tu Machine:

- Lee un documento de Google enlazado en los mensajes de una tarea o pegado en su chat, solo mientras trabaja en esa tarea.
- Prepara cambios en ese documento. Cada uno espera tu visto bueno, como se explica arriba.
- Crea documentos privados en tu Google Drive.

Si hay más de una conexión de Google Docs en el área de una tarea, lee y modifica un archivo a través de una conexión que pueda abrirlo y modificarlo.

No busca en tu Drive. Solo ve los comentarios, archivos compartidos y sugerencias de los documentos que ha creado. Para ver más, necesitaría acceso a todo tu Drive, que no solicita.

## Google Sheets y Slides

Si Google Docs muestra **Permitir el acceso a Sheets y Slides** en **Conexiones**, púlsalo y permite ambos accesos. Google te pide permiso para que tu Machine vea tus archivos de Sheets y Slides. No puede modificarlos.

A partir de entonces, tu Machine también lee un archivo de Google Sheets o Slides enlazado en los mensajes de una tarea o pegado en su chat, solo mientras trabaja en esa tarea:

- En una hoja de cálculo, primero lee la pestaña o las celdas enlazadas y luego las demás pestañas, hasta un máximo de 2.000 celdas. Las fórmulas se muestran como sus valores. Solo lee las pestañas ocultas si se enlazan o se le pide que lo haga.
- En las presentaciones, lee el texto y las notas del orador en orden. No lee las imágenes ni los gráficos.

### Editar Sheets y Slides

Una vez que tu Machine pueda leerlos, Google Docs también puede mostrar **Permitir editar Sheets y Slides**. Púlsalo y permite ambos accesos para que tu Machine pueda modificar un archivo de Sheets o Slides enlazado en una tarea o pegado en su chat. El proceso es el mismo que para modificar un documento: solo prepara el cambio, **Revisar cambios** lo muestra y no se escribe nada hasta que pulses **Guardar**.

- En una hoja de cálculo: puede añadir valores a celdas de una pestaña, filas debajo de la última fila o una pestaña nueva. Cada celda muestra el antes y el después. Los valores se añaden como texto. Las fórmulas solo se añaden como fórmulas si la tarea lo indica.
- En las presentaciones: puede reemplazar texto en una diapositiva, mostrando el antes y el después, o añadir una diapositiva con título y texto.
- Solo escribe en el archivo tal como lo viste. Si alguien ha modificado esas celdas o diapositivas mientras tanto, no se escribe nada y la tarea te lo indica.

El formato, los gráficos, las imágenes y los archivos de Excel o PowerPoint se mantienen tal como están.

Si el archivo es grande, indica en el chat a qué pestaña, celdas o diapositivas te refieres. Si el archivo es privado de otra persona, se ha eliminado o es un archivo de Excel o PowerPoint, la tarea te lo indicará. Un enlace de Google Drive funciona igual si lleva a un archivo de Google Docs, Sheets o Slides.

## Google Docs en tu propio ordenador

En tu propio ordenador, tu Machine puede crear un documento de Google en una cuenta de Gmail que tenga la sesión iniciada y ya tenga acceso a Drive. No lee tus otros documentos de Google ni sus comentarios. **Documentos y archivos** lo muestra como Google Docs en esa cuenta. También puede modificar un documento que haya creado allí para una tarea.

También lee un archivo de Google Sheets o Slides enlazado en una tarea o pegado en su chat, si esa sesión de Google ya tiene acceso a Drive, Sheets o Slides. Nunca pide más permisos a Google y no modifica esos archivos. Si Google no lo permite, activa la API de Google Sheets o Slides en el proyecto de Google de esa cuenta.

## Trabajo o personal

Sigue la etiqueta Trabajo o Personal de la conexión, igual que con el correo. Los documentos de trabajo pueden llegar al Graph de tu equipo según tus [reglas para compartir](sharing-rules.md). Los personales nunca llegan.

## Desconectarlo

Abre **Conexiones**, elige Microsoft OneDrive o Google Docs, pulsa **Detalles** y luego **Desconectar**. Dejará de leer. Lo que ya haya importado se mantiene. En una Machine alojada, **Desconectar ↗** abre la página de configuración, donde se guarda la sesión.
