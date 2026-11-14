---
title: Personas
area: graph
summary: Todas las personas con las que estás en contacto: su página, resumen y cronología, y cómo añadir, editar, fusionar o eliminar a alguien.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Todas las personas con las que estás en contacto, empezando por las más cercanas, a partir de tus mensajes y reuniones. Los boletines, recibos y otros correos no añaden a nadie hasta que respondes. Aparecen en Remitentes ocultos, debajo de la lista: **Mostrar más** como persona añade a alguien. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada lista tiene sus propios filtros: consulta [The Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre de una tienda) cuenta como parte de su organización, no como una persona, incluso después de que le escribas.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea sobre cómo están en contacto ("Hablan a diario · último contacto ayer · próxima reunión mar., 27 de oct."). El contacto reciente aparece como "ahora mismo", "hace 3 horas", "ayer" o "hace 3 días"; si es más antiguo, aparece la fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar**. Aquí también aparece su **Cumpleaños**, junto con su origen (contactos de Google, Google Calendar, Facebook o tú): consulta [The Graph](graph.md#birthday).
- **Contigo**: qué relación tiene contigo, si es un contacto de Trabajo o Personal, y si forma parte de tu Familia o Fleet, con **Ver en Fleet**.
- **También en**: otros sitios donde hablas con esa persona. **Slack** la abre en Slack o abre el hilo más reciente que tienes con ella en Slack.
- **Personas** y **Proyectos** de los que forma parte, **Pendiente entre ambos** (promesas mutuas, con **Marcar como hecha** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se unen automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, si se trata de un correo de trabajo con su propia dirección en copia.

Si una página muestra **No se pudo cargar esta página.**, toca **Reintentar**. Si sigue apareciendo, usa **¿Algo va mal?** al final de la página.

## Resumen

Unas pocas líneas al principio de la página de una persona: lo que se decidió, pidió, planeó o prometió, con los nombres de todos. The Machine lo reescribe cuando hay novedades, solo para las personas con las que realmente estás en contacto, y revisa cada línea antes. Por lo general, una vez al día; en unas horas si cambia algo relacionado con esa persona, como un nuevo plazo o una solicitud retirada.

Si una línea es imprecisa, se omite. Si no hay nada concreto que decir, no hay resumen. Cada línea enlaza al contenido original: los mensajes de un mismo día comparten una fecha y muestran su cantidad; al abrirlos, aparecen juntos.

**Editar** para expresarlo a tu manera. Cuando hay novedades, The Machine muestra una **Actualización sugerida**, con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** se lo devuelve.

Los preparativos de reuniones usan este resumen, solo las líneas del área de esa tarea (Trabajo o Personal). Se queda en tu Machine; tu equipo nunca lo ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de lo más reciente a lo más antiguo: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y movimientos de proyectos. Los filtros de arriba muestran una fuente a la vez. **Mostrar más** carga elementos anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, empezando por la más cercana. **Mostrar todos los próximos** muestra las demás. En una reunión aparecen las personas que asistieron, cada una una sola vez. Si tiene notas o una transcripción, muestra **Notas** o **Transcripción**; haz clic para leerlas.

Tus cronologías son solo tuyas: el Graph del equipo muestra únicamente lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la cronología, añade lo que han compartido tus compañeros, con el nombre de quien compartió cada elemento; **Míos** muestra solo los tuyos.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran a las personas según su tipo, que aparece en su página. Si eliges uno (**Editar**), prevalece tu elección. De lo contrario, tu Familia y tus Amigos, así como quienes son familia o amigos tuyos (una esposa, un padre), son Personal, sea cual sea la dirección desde la que escriban. Tu equipo nunca ve los contactos personales.

## Añadir a alguien

Usa **Nueva persona** en la parte superior de Personas o **+** en la barra superior de un teléfono. Añade un nombre y, si los tienes, un correo y una organización. Si ya hay alguien parecido en tu Graph, el formulario te lo muestra primero para que puedas abrir esa página. **Añadir** abre la página nueva.

La persona que añadas se queda, aunque todavía no haya mensajes. Su primer mensaje se vincula con ella.

## Editar a alguien

**Editar**, en la parte superior de su página, permite cambiar su nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, qué relación tiene contigo y si es de Trabajo o Personal. El campo **Notas** sirve para guardar lo que quieras recordar; las notas se conservan al fusionar personas. **Guardar** conserva los cambios; **Cancelar** los descarta.

Tus cambios se conservan aunque se vuelvan a consultar sus datos y también al usar **Fusionar** y **Deshacer**. Borra el contenido de un campo para volver a usar el valor consultado. Si borras el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella y selecciona **Subir una imagen**, elige una de las fotos encontradas para esa persona o **Quitar imagen**. La foto se queda en tu Machine.

## Fusionar dos personas

Si dos personas podrían ser la misma, su página te pregunta si son la misma persona, y Personas las muestra en **¿Misma persona?**. **Fusionar** las une, con todos sus mensajes, notas, roles y proyectos. **No es la misma** las mantiene separadas definitivamente. Tu respuesta aparece un momento junto al par y, después, el par desaparece de la lista. La lista desaparece cuando ya no queda nada por revisar.

Nunca se propone como la misma persona a alguien con una dirección que solo se parece a una que conoces, como acme-corp.example en comparación con acmecorp.example. Además, solo tú puedes asignarle un rol.

Una dirección compartida, como info@ o una lista de correo, nunca se une a las personas que escriben desde ella. Un contacto de trabajo ajeno a tu empresa y un chat personal que solo comparte un nombre no se unen automáticamente: aparecen como una pregunta.

**Fusionar todo** une todos los pares de la lista a la vez, excepto los que marcaste como **No es la misma**. Si usas **Deshacer** enseguida, los separa de nuevo.

Para unir a dos personas manualmente, abre una de sus páginas y luego selecciona **⋯**, **Misma persona que…** y elige a la otra. En la página de la persona fusionada aparece el motivo en **Fusionada desde**, con la opción **Deshacer** para volver a separarlas.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯ y selecciona **Eliminar para siempre…**; después, **Eliminar**. Se eliminarán esa persona y todo lo que tu Machine sabe sobre ella: su ficha, direcciones, datos consultados, los mensajes que solo intercambiaron ustedes dos y las notas sobre ella.

Las tareas en las que participa se conservan, pero se quita su nombre. No se volverá a añadir, ni siquiera mediante una importación o una tarea de cumpleaños de Facebook con su nombre o dirección. Esta acción no se puede deshacer.

## Correo rechazado

Cuando un correo que envías a alguien rebota, su dirección aparece como **Rechazado**, junto con la fecha, y se muestra primero otra dirección suya. Los borradores nuevos nunca se envían a esa dirección si se conoce otra. Si es la única, la hoja de envío te avisa, pero puedes enviar el correo.

Se considera que un correo ha rebotado cuando el servidor indica que la dirección no existe o después de 3 fallos temporales durante una semana. El aviso desaparece cuando esa persona vuelve a escribir desde esa dirección o cuando se envía correctamente un correo a ella.

## Cargo y foto

Las personas que tienen una dirección de empresa obtienen un cargo, una foto, LinkedIn y una ciudad, consultados como se explica en [datos de la organización](organization-data.md). En una Machine alojada, la consulta solo recibe su nombre y el dominio de su empresa. Para obtener una foto, Gravatar recibe un hash de su dirección de trabajo, nunca la dirección en sí. Puedes desactivarlo en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Cuando la consulta encuentra sus datos, su página también muestra su texto de presentación, desde cuándo ocupa su puesto actual y sus dos puestos anteriores. Los preparativos también los consultan, y usan el texto de presentación solo si no tiene una biografía propia.

Tus conexiones completan más información con lo que ya han leído: un cargo, teléfono y zona horaria de Slack; una biografía y ubicación de X; un titular y una foto de LinkedIn; cargos de los contactos de Google y Salesflare; y la foto de un contacto de Salesflare, si Salesflare la tiene. Pasa el cursor por encima de la línea debajo del nombre para ver de dónde procede.

Outlook añade las fotos de los compañeros de tu organización y de tus contactos de Outlook, además de los cargos y las empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram se obtienen mediante la sincronización de WhatsApp y la conexión de chats de Telegram: hasta 50 al día en cada caso, solo de personas que ya estén en tu Graph. No se les envía nada. Una importación de cumpleaños de Facebook añade la foto de perfil de una persona que no tenga foto cuando la guardas ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Team Graph](team-graph.md) de una Fleet de Trabajo, se incluye una copia pequeña de la foto de trabajo en el registro compartido de una persona. Nunca se incluyen fotos de contactos de Google, WhatsApp, Telegram o Facebook, ni fotos que hayas cambiado o quitado.

## Sobre ti

Tus propias direcciones y números, incluidos tus alias, siempre son tuyos, nunca de alguien de tu Graph. Si te buscas o añades a alguien con una de tus direcciones, se abre **Sobre ti** y se omite tu propia fila al importar.

Sobre ti muestra tus direcciones y de dónde procede cada una. Cámbialas en **Ajustes**, en Cuenta. Para enviar tu contacto a un compañero o amigo, selecciona **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Los roles que tu Machine detecta en tus mensajes aparecen en su página, en **Para ti**, junto con la línea que leyó. No espera a que se lo confirmes. ¿Está mal? Corrígelo con **Editar** en su página o con **⋯** en la línea correspondiente de **Cambios recientes**. Aprende de tus cambios.

## Lo que sabe sobre alguien

Los datos sobre esa persona aparecen en su página, en **Información conocida**; Aprendizaje guarda los datos generales. **Añadir** permite guardar otro con tus propias palabras. Cada dato tiene un menú:

- **Editar** lo cambia directamente.
- **No es sobre esta persona** lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, desplegado justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido sobre esa entidad: un rol, dónde trabaja alguien, la relación entre dos personas, un dato o un cambio de proyecto. Cada línea incluye la fecha y la fuente; toca la fuente para leer el mensaje.

Si una línea es incorrecta, puedes corregirla directamente desde **⋯**: **Editar**, **Quitar**, **No es sobre esta persona** o **Deshacer** para devolver un proyecto a su estado anterior. Se muestran tres líneas; **Mostrar más** muestra las demás.

Si tu Machine actualizó a alguien hoy, aparece un punto pequeño junto a esa persona en la lista Personas y **4 personas actualizadas hoy** aparece en la parte superior de la lista. Consulta [The Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea** en el menú **⋯** de una persona, organización o proyecto crea una tarea sobre esa entidad.
