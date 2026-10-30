---
title: Microsoft Word: archivos de Word en OneDrive y SharePoint
area: connections
summary: Comentarios, menciones, cambios con seguimiento y archivos compartidos en tus archivos de Word en OneDrive y SharePoint, además de documentos nuevos y cambios que apruebas. Google Docs llegará más adelante.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## Qué lee

La conexión **Microsoft Word** lee archivos de Word en OneDrive y SharePoint. Inicias sesión con Microsoft para ella, con o sin Outlook conectado. Funciona en una Machine alojada y en tu propio ordenador vinculado a tu cuenta. Google Docs llegará más adelante: el inicio de sesión de Google de The Machine aún no puede leer documentos. Trae:

- Documentos que alguien comparte contigo.
- Comentarios y respuestas en documentos tuyos, y comentarios que te mencionan.
- Control de cambios en archivos de Word tuyos.

La primera sincronización mira 30 días atrás. Cada cosa se convierte en un evento, vinculado a las personas y proyectos de tu [Graph](graph.md). Cuando un comentario te necesita, se convierte en una tarea.

## Qué puede hacer

Cuando una tarea necesita el texto de un documento, tu Machine lee ese documento, y solo mientras trabaja en esa tarea.

Puede redactar una respuesta a un comentario. Los archivos de Word no permiten publicar una respuesta desde fuera de Word, así que la respuesta se queda como borrador para que la copies en Word.

Nunca acepta una sugerencia, resuelve un comentario, comparte un archivo ni cambia un documento sin tu OK.

## Crear y editar documentos

Tu Machine puede escribir un documento de Word nuevo o cambiar un documento del que trata una de tus tareas. Nunca escribe por su cuenta:

- Prepara el cambio en la tarea. Un documento nuevo se ve completo. Una edición muestra cada párrafo antes y después.
- Toca **Revisar y crear** o **Revisar cambios**, léelo y luego **Crear** o **Guardar**.
- Escribe una sola vez, y solo en el documento tal como lo viste. Si alguien lo cambió entretanto, no se escribe nada y la tarea lo dice. Pide un borrador nuevo.
- En Talk, lee el cambio completo en voz alta y espera un sí claro.

Reemplaza texto, añade texto y añade párrafos y títulos. No toca tablas, imágenes, cambios con seguimiento ni campos. Un documento nuevo queda en tu OneDrive y es privado hasta que lo compartas.

Conectar Microsoft Word ya lo permite: no hay un paso aparte. Una conexión de Microsoft Word anterior que solo lee muestra **Permitir cambios** en su tarjeta en **Conexiones**. Tócalo una vez y acepta.

## Qué pide

Microsoft Word pide a Microsoft un solo OK, aparte del inicio de sesión de tu correo: leer y cambiar tus archivos, incluidos los que se comparten contigo en OneDrive y SharePoint. Cada cambio sigue esperando tu OK en su tarea. Tu acceso al correo y al calendario se queda como está. Sin Outlook, el inicio de sesión solo cubre tus archivos, nunca tu correo ni tu calendario.

Si más tarde se retira ese OK, la tarjeta de Microsoft Word dice **Esperando tu OK para leer documentos**.

## Conéctalo

No necesitas tener Outlook conectado.

- Machine alojada: en el panel, abre **Conexiones**, **+ Añadir**, elige **Microsoft Word** y pulsa **Iniciar sesión con Microsoft**. Microsoft te pide permitir que lea y edite tus archivos y luego vuelves al panel.
- Tu propio ordenador, vinculado a tu cuenta: abre **Conexiones**, **+ Añadir**, elige **Microsoft Word** y pulsa **Iniciar sesión con Microsoft**.

Comprueba que el inicio de sesión puede leer documentos. Sin ese OK no se añade. Si tocas **Permitir cambios** y Microsoft no permite cambios, lo dice en lugar de mostrar Conectado.

## Trabajo o personal

Microsoft Word sigue la etiqueta de trabajo o personal de su conexión, como el correo. Los documentos de trabajo pueden llegar al Graph de tu equipo según tus [reglas para compartir](sharing-rules.md). Los personales nunca.

## Quítalo

En el panel: **Conexiones**, abre Microsoft Word, **Detalles** y luego **Desconectar**. Deja de leer. Lo que ya trajo se queda.
