---
title: Microsoft OneDrive
area: connections
summary: Comentarios, menciones y cambios controlados en tus archivos de Word de OneDrive. Los documentos nuevos y los cambios esperan tu visto bueno.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 057429e4c3b6408c
---
## Qué lee

**Microsoft OneDrive** lee tus archivos de Word en OneDrive, tanto en una Machine alojada como en tu propio ordenador. No hace falta conectar Outlook. Para Google Docs, consulta la sección correspondiente más abajo. Trae:

- Comentarios y respuestas en tus archivos de Word, incluidos los comentarios en los que te mencionan.
- Cambios controlados en tus archivos de Word.

La primera sincronización abarca los últimos 7 días. Cada elemento enlaza con las personas y los proyectos de tu [Graph](graph.md). Los comentarios que requieren tu atención se convierten en tareas.

## Archivos que otras personas comparten contigo

Microsoft dejará de mostrar estos archivos en noviembre de 2026. A partir de entonces, los archivos compartidos y las menciones en archivos de otras personas solo llegarán a tu Machine a través de los correos de Microsoft. Conecta también [Outlook](microsoft.md) y mantén activados esos correos. Una tarea creada a partir de uno de ellos abre el correo y su botón abre el archivo. No se detectan los archivos compartidos ni las menciones que no vengan acompañados de un correo.

## Qué puede hacer

Cuando una tarea necesita el texto de un documento, tu Machine lee solo ese documento y únicamente mientras trabaja en esa tarea. Puede leer archivos de Word, PDF y texto.

También busca archivos de cualquier tipo en tu propio OneDrive y te da el enlace. No busca en sitios de SharePoint ni en archivos que hayan compartido contigo. No puede leer el texto de un PDF escaneado.

Puede preparar un borrador de respuesta a un comentario. Word no permite publicar respuestas desde fuera, así que tendrás que copiar el borrador en Word.

Nunca acepta sugerencias, resuelve comentarios, comparte archivos ni cambia documentos sin tu visto bueno.

Si solo quieres que realice acciones, desactiva **Trae señales** en **Detalles**. Entonces solo buscará y leerá los archivos que necesiten tus tareas, y creará otros nuevos.

## Crear y editar documentos

Tu Machine puede crear un documento o modificar uno relacionado con una tarea:

- Puede crear un documento nuevo en el momento si la tarea o una habilidad lo pide. Será privado y estará en tu propio OneDrive o Google Drive. La tarea mostrará **Abrir el documento**. Compartirlo o enviar el enlace esperará tu visto bueno.
- Los cambios en un documento existente solo se preparan. Pulsa **Revisar cambios** para ver cada párrafo antes y después y, luego, **Guardar**. Los cambios que pidas en el chat de la tarea se aplican en el momento.
- Solo escribe en el documento tal como lo viste. Si alguien lo ha cambiado entretanto, no se escribe nada y la tarea te lo indica. Pide un borrador nuevo.
- En Talk, lee en voz alta todos los cambios y espera un sí claro.
- Si Microsoft o Google no permite crear un documento, la tarea indica el motivo y muestra **Revisar y crear** para volver a intentarlo.

Puede reemplazar y añadir texto, párrafos y encabezados. En Google Docs también puede aplicar formato: negrita, cursiva, subrayado, enlaces, encabezados, listas con viñetas y numeradas, y saltos de página. **Revisar cambios** muestra cada cambio. No puede crear tablas, y las imágenes, los cambios controlados y los campos se quedan como están.

El documento de una tarea de trabajo se guarda en la cuenta de esa empresa, nunca en una cuenta personal. En tu propio ordenador, también se pueden crear documentos de Google en una cuenta de Google conectada para Gmail que ya tenga acceso a Drive. Si no hay ninguna cuenta adecuada, la tarea te indica qué conectar para trabajar: Microsoft OneDrive o Google Docs, si tu Machine puede usarlo.

Si el documento no es el último paso, por ejemplo, si hay que responder con un enlace al documento, la tarea sigue abierta y prepara ese paso para que des tu visto bueno.

La conexión incluye la posibilidad de editar. Si una conexión anterior solo permite leer, verás **Permitir cambios** en **Conexiones**. Púlsalo una vez y acepta.

## Qué permisos solicita

Microsoft te pide un único visto bueno para leer y modificar tus archivos, incluidos los que hayan compartido contigo. Cada cambio sigue esperando tu visto bueno en la tarea correspondiente. El acceso al correo y al calendario no cambia.

Si más adelante retiras ese visto bueno, Microsoft OneDrive mostrará **Esperando tu visto bueno para leer documentos** en **Conexiones**.

## Conectarlo

En una Machine alojada o en tu propio ordenador, vinculado a tu cuenta:

- Abre **Conexiones**, luego **Documentos y archivos** y elige **Microsoft OneDrive**.
- Pulsa **Iniciar sesión con Microsoft** y permite leer y editar tus archivos.

Si Microsoft no permite la lectura, no se añade. Si pulsas **Permitir cambios** y Microsoft no permite editar, te lo indicará.

## Google Docs

En una Machine alojada, abre **Conexiones**, luego **Documentos y archivos** y elige **Google Docs**. Google te pide permiso para ver y editar los documentos que le indiques, y crear otros nuevos. No hace falta conectar Gmail y el acceso a Gmail no cambia.

Entonces, tu Machine:

- Lee un documento de Google enlazado en los mensajes de una tarea o pegado en su chat, únicamente mientras trabaja en esa tarea.
- Prepara cambios en ese documento. Cada cambio espera tu visto bueno, como se ha explicado arriba.
- Crea documentos privados en tu Google Drive.

No busca en tu Drive. Solo ve los comentarios, archivos compartidos y sugerencias de los documentos que ha creado. Para acceder a más, necesitaría acceso a todo tu Drive, algo que no solicita.

## Google Sheets y Slides

Si Google Docs muestra **Permitir el acceso a Sheets y Slides** en **Conexiones**, púlsalo y permite el acceso a ambos. Google te pide permiso para que tu Machine vea tus archivos de Sheets y Slides. No puede modificarlos.

Entonces, tu Machine también lee una hoja de cálculo de Google o un archivo de Slides enlazado en los mensajes de una tarea o pegado en su chat, únicamente mientras trabaja en esa tarea:

- De una hoja de cálculo, lee primero la pestaña o las celdas enlazadas y, después, las demás pestañas, hasta un máximo de 2.000 celdas. Las fórmulas se muestran como sus valores. Solo lee las pestañas ocultas si se enlazan o se pide expresamente.
- De las diapositivas, lee el texto y las notas del orador en orden. No lee imágenes ni gráficos.

### Editar Sheets y Slides

Cuando tu Machine ya puede leerlos, Google Docs también puede mostrar **Permitir editar Sheets y Slides**. Púlsalo y permite el acceso a ambos. Así, tu Machine podrá modificar una hoja de cálculo de Sheets o un archivo de Slides enlazado del mismo modo que modifica un documento: solo prepara el cambio, **Revisar cambios** lo muestra y no se escribe nada hasta que pulses **Guardar**.

- En una hoja de cálculo: puede añadir valores nuevos a celdas de una pestaña, filas debajo de la última fila o una pestaña nueva. Se muestra cada celda antes y después. Los valores se añaden como texto; solo se añade una fórmula como fórmula si la tarea lo indica.
- En las diapositivas: puede reemplazar texto en una diapositiva, mostrando el antes y el después, o crear una diapositiva nueva con título y texto.
- Solo escribe en el archivo tal como lo viste. Si alguien ha cambiado entretanto esas celdas o las diapositivas, no se escribe nada y la tarea te lo indica.

El formato, los gráficos, las imágenes y los archivos de Excel o PowerPoint se quedan como están.

Si el archivo es grande, indica en el chat qué pestaña, celdas o diapositivas quieres. Si el archivo es privado de otra persona, se ha eliminado o es un archivo de Excel o PowerPoint, la tarea te lo indica. Un enlace de Google Drive funciona igual si lleva a un documento, una hoja de cálculo o un archivo de Slides de Google.

## Google Docs en tu propio ordenador

En tu propio ordenador, tu Machine puede crear un documento de Google en una cuenta de Gmail con la sesión iniciada que ya tenga acceso a Drive. No lee tus otros documentos de Google ni sus comentarios. **Documentos y archivos** lo muestra como Google Docs en esa cuenta. También puede modificar allí un documento que haya creado para una tarea.

También lee una hoja de cálculo de Google o un archivo de Slides enlazado en una tarea o pegado en su chat, si esa cuenta de Google ya tiene acceso a Drive, Sheets o Slides. Nunca solicita más permisos a Google y no los modifica desde allí. Si Google no lo permite, activa la API de Google Sheets o Slides en el propio proyecto de Google de esa cuenta.

## Trabajo o uso personal

Sigue la etiqueta Trabajo o Personal de su conexión, igual que el correo. Los documentos de trabajo pueden llegar al Graph de tu equipo según tus [reglas para compartir](sharing-rules.md). Los personales nunca llegan.

## Desconectarlo

Abre **Conexiones**, luego Microsoft OneDrive o Google Docs, **Detalles** y **Desconectar**. Dejará de leer. Lo que ya haya incorporado se queda. En una Machine alojada, **Desconectar ↗** abre la página de configuración donde se guarda la sesión.
