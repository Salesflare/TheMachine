---
title: Microsoft OneDrive: archivos de Word en OneDrive y SharePoint
area: connections
summary: Comentarios, menciones, cambios con seguimiento y archivos compartidos en tus archivos de Word en OneDrive y SharePoint, además de documentos nuevos privados, y cambios que apruebas.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## Qué lee

La conexión **Microsoft OneDrive** lee archivos de Word en OneDrive y SharePoint. Inicias sesión con Microsoft para ella, con o sin Outlook conectado. Funciona en una Machine alojada y en tu propio ordenador vinculado a tu cuenta. Para Google Docs, consulta más abajo. Trae:

- Documentos que alguien comparte contigo.
- Comentarios y respuestas en documentos tuyos, y comentarios que te mencionan.
- Control de cambios en archivos de Word tuyos.

La primera sincronización mira 30 días atrás. Cada cosa se convierte en un evento, vinculado a las personas y proyectos de tu [Graph](graph.md). Cuando un comentario te necesita, se convierte en una tarea.

## Qué puede hacer

Cuando una tarea necesita el texto de un documento, tu Machine lee ese documento, y solo mientras trabaja en esa tarea.

Puede redactar una respuesta a un comentario. Los archivos de Word no permiten publicar una respuesta desde fuera de Word, así que la respuesta se queda como borrador para que la copies en Word.

Nunca acepta una sugerencia, resuelve un comentario, comparte un archivo ni cambia un documento sin tu OK.

Una conexión de documentos puede solo hacer cosas: desactiva **Trae señales** en **Detalles**, y solo busca y lee los documentos que tus to-dos necesitan, y crea nuevos. Una de Google sin acceso a todo Drive lee documentos por su enlace, y los que tu Machine creó.

## Crear y editar documentos

Tu Machine puede escribir un documento nuevo o cambiar un documento del que trata una de tus tareas:

- Un documento nuevo lo crea enseguida, cuando la tarea o una habilidad dice que hay que crearlo: un documento privado en tu propio Google Drive o OneDrive, sin compartir con nadie. La tarea lo muestra con **Abrir el documento**. Compartirlo, o enviar su enlace a alguien, espera tu OK.
- Un cambio en un documento existente solo lo prepara, cada párrafo antes y después. Toca **Revisar cambios**, léelo y luego **Guardar**. Un cambio que pides en el chat de la tarea lo hace enseguida.
- Escribe un cambio una sola vez, y solo en el documento tal como lo viste. Si alguien lo cambió entretanto, no se escribe nada y la tarea lo dice. Pide un borrador nuevo.
- En Talk, lee el cambio completo en voz alta y espera un sí claro.
- Si Google o Microsoft rechaza un documento nuevo, la tarea dice qué se rechazó y muestra **Revisar y crear** para volver a intentarlo.

Reemplaza texto, añade texto y añade párrafos y títulos. No toca tablas, imágenes, cambios con seguimiento ni campos. Un documento nuevo queda en tu Google Drive o OneDrive y es privado hasta que lo compartas.

Un documento nuevo va a una cuenta del área de la tarea: el documento de una tarea de Trabajo a la cuenta de esa empresa, la de la conversación cuando se puede, nunca a una personal. En tu propio ordenador, una cuenta de Google conectada para Gmail que ya tiene acceso a Drive también puede recibir un Google Doc nuevo. Si ninguna cuenta encaja, la tarea dice **Conecta Google Docs o Microsoft OneDrive para Trabajo**.

Cuando el documento no es el final de la tarea, como una respuesta con su enlace, la tarea sigue abierta y prepara ese siguiente paso para tu OK.

Conectar Microsoft OneDrive ya lo permite: no hay un paso aparte. Una conexión de Microsoft OneDrive anterior que solo lee muestra **Permitir cambios** en su tarjeta en **Conexiones**. Tócalo una vez y acepta.

## Qué pide

Microsoft OneDrive pide a Microsoft un solo OK, aparte del inicio de sesión de tu correo: leer y cambiar tus archivos, incluidos los que se comparten contigo en OneDrive y SharePoint. Cada cambio sigue esperando tu OK en su tarea. Tu acceso al correo y al calendario se queda como está. Sin Outlook, el inicio de sesión solo cubre tus archivos, nunca tu correo ni tu calendario.

Si más tarde se retira ese OK, la tarjeta de Microsoft OneDrive dice **Esperando tu OK para leer documentos**.

## Conéctalo

No necesitas tener Outlook conectado.

- Machine alojada: en el panel, abre **Conexiones**, **+ Añadir**, elige **Microsoft OneDrive** y pulsa **Iniciar sesión con Microsoft**. Microsoft te pide permitir que lea y edite tus archivos y luego vuelves al panel.
- Tu propio ordenador, vinculado a tu cuenta: abre **Conexiones**, **+ Añadir**, elige **Microsoft OneDrive** y pulsa **Iniciar sesión con Microsoft**.

Comprueba que el inicio de sesión puede leer documentos. Sin ese OK no se añade. Si tocas **Permitir cambios** y Microsoft no permite cambios, lo dice en lugar de mostrar Conectado.

## Google Docs

Google Docs aún no se puede conectar. Leerlos necesita un permiso de Google que The Machine aún no pide. Lo que funciona hoy:

- En tu propio ordenador, tu Machine puede crear un Google Doc nuevo en una cuenta de Gmail iniciada allí que ya tiene acceso a Drive. No lee tus otros Google Docs ni sus comentarios.
- Una Machine alojada aún no puede usar Google Docs.

## Trabajo o personal

Microsoft OneDrive sigue la etiqueta de trabajo o personal de su conexión, como el correo. Los documentos de trabajo pueden llegar al Graph de tu equipo según tus [reglas para compartir](sharing-rules.md). Los personales nunca.

## Quítalo

En el panel: **Conexiones**, abre Microsoft OneDrive, **Detalles** y luego **Desconectar**. Deja de leer. Lo que ya trajo se queda.
