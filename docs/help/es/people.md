---
title: Personas
area: graph
summary: Todas las personas con las que estás en contacto: su página, resumen y cronología, y cómo añadir, editar, fusionar o eliminar a alguien.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Todas las personas con las que estás en contacto, empezando por las más cercanas, a partir de tus mensajes y reuniones. Los boletines, recibos y otros correos no añaden a nadie hasta que respondes. Aparecen en Remitentes ocultos, debajo de la lista: **Mostrar como persona** añade a alguien. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada lista tiene sus propios filtros: consulta [The Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre de una tienda) cuenta como parte de su organización, no como una persona, incluso después de que le escribas.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea sobre cómo están en contacto («Hablan a diario · último contacto ayer · próxima reunión mar., 27 oct.»). El contacto reciente aparece como «ahora mismo», «hace 3 horas», «ayer» o «hace 3 días», y el contacto más antiguo aparece con la fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo encontrarás:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar**lo. Aquí también aparece su **Cumpleaños**, junto con su origen (Contactos de Google, Google Calendar, Facebook o tú): consulta [The Graph](graph.md#birthday).
- **Contigo**: qué relación tiene contigo, si es un contacto de Trabajo o Personal, y tu Familia o Fleet, con **Ver en Fleet**.
- **También en**: otros lugares donde hablan. **Slack** abre su perfil en Slack o el hilo más reciente que tengas con esa persona.
- Las **Personas** y **Proyectos** de los que forma parte, lo **Pendiente entre ambos** (promesas en ambos sentidos, con **Marcar como hecha** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se unen automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, un correo del trabajo con su dirección personal en copia.

Si aparece el mensaje **No se ha podido cargar esta página.**, toca **Reintentar**. Si sigue apareciendo, usa **¿Algo va mal?** al final de la página.

## Resumen

Unas pocas líneas al principio de la página de una persona: lo que se decidió, pidió, planeó o prometió, con los nombres de todos. The Machine lo reescribe cuando hay novedades, solo para las personas con las que realmente estás en contacto, y comprueba cada línea primero. Normalmente, una vez al día; en unas horas si cambia algo relacionado con esa persona, como un nuevo plazo o una solicitud que se retira.

Si una línea es ambigua, se omite. Si no hay nada concreto que decir, no hay resumen. Cada línea enlaza con su origen: los mensajes de un mismo día comparten una fecha con el número de mensajes y se pueden desplegar juntos.

**Editar** para decirlo a tu manera. Cuando hay novedades, The Machine muestra una **Actualización sugerida** con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** se lo devuelve.

La preparación de reuniones usa este resumen, solo las líneas de la parte correspondiente a esa tarea (Trabajo o Personal). Se queda en tu Machine; tu equipo nunca la ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de más reciente a más antigua: correo, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y cambios en proyectos. Los filtros de arriba muestran un origen a la vez. **Mostrar más** carga los anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, empezando por la más cercana. **Mostrar todos los próximos** muestra el resto. En cada reunión aparecen sus asistentes, una sola vez por persona. Si hay notas o una transcripción, aparece **Notas** o **Transcripción**; haz clic para leerlas.

Tus cronologías son tuyas: el Graph del equipo solo muestra lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la Cronología, añade lo que han compartido tus compañeros; cada elemento indica quién lo compartió. **Míos** muestra solo lo tuyo.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran a las personas según su Tipo, que aparece en su página. Si eliges uno (**Editar**), tiene prioridad. Si no, Familia y Amigos, así como las personas que son familia o amigas tuyas (una esposa, un padre), se consideran Personal, sin importar desde qué dirección escriban. Tu equipo nunca tiene acceso a los contactos personales.

## Añadir a alguien

Usa **Nueva persona** en la parte superior de Personas o **+** en la barra superior desde el móvil. Añade un nombre y, si los tienes, un correo y una organización. Si en tu Graph ya hay alguien que podría ser esa persona, el formulario lo muestra primero para que puedas abrir ese perfil. **Añadir** abre la página nueva.

La persona que añadas se queda, aunque todavía no haya mensajes. Su primer mensaje se vincula a su perfil.

## Editar a alguien

**Editar**, en la parte superior de su página, permite cambiar su nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, qué relación tiene contigo y si es de Trabajo o Personal. El campo **Notas** sirve para apuntar lo que quieras recordar; las notas se conservan al fusionar perfiles. **Guardar** guarda los cambios y **Cancelar** los descarta.

Tus cambios se conservan aunque se vuelvan a consultar sus datos, y también al usar **Fusionar** y **Deshacer**. Si dejas un campo vacío, se volverá a usar el valor consultado. Si dejas vacío el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella: **Subir una imagen**, elige una de las que se hayan encontrado para esa persona o **Quitar imagen**. La foto se queda en tu Machine.

## Fusionar a dos personas

Si dos personas podrían ser la misma, en su página se pregunta si son la misma persona y en Personas aparecen bajo **¿Misma persona?**. **Fusionar** las une, con todos sus mensajes, notas, roles y proyectos. **No es la misma** las mantiene separadas definitivamente. Tu respuesta aparece un momento en la pareja y, después, esta desaparece de la lista. La lista desaparece cuando ya no queda nada por resolver.

Nunca se propone que alguien con una dirección que solo se parece a otra que conoces, como acme-corp.example y acmecorp.example, sea la misma persona. Además, solo tú puedes asignarle un rol.

Una dirección compartida, como info@ o una lista de correo, nunca se une a las personas que escriben a través de ella. Un contacto de trabajo de fuera de tu empresa y un chat personal que solo comparte un nombre con él tampoco se unen automáticamente: aparecen como una pregunta.

**Fusionar todo** une de una vez todas las parejas de la lista, salvo las que hayas marcado como **No es la misma**. Si usas **Deshacer** justo después, las vuelve a separar.

Para unir a dos personas por tu cuenta, abre una de ellas y luego elige **⋯**, **Misma persona que…** y la otra. En la página de la persona resultante se muestran los motivos en **Unido desde**, con la opción **Deshacer** para volver a separarlas.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯, elige **Eliminar para siempre…** y después **Eliminar**. Se eliminan la persona y todo lo que tu Machine sabe de ella: su ficha, direcciones, datos consultados, los mensajes que solo intercambiaron ustedes dos y las notas sobre ella.

Las tareas en las que participa se conservan, pero se quita su nombre. No volverá a añadirse, tampoco mediante una importación o una tarea de cumpleaños de Facebook que incluya su nombre o dirección. Esta acción no se puede deshacer.

## Correo rechazado

Cuando se rechaza un correo enviado a alguien, su dirección aparece como **Rechazada**, junto con la fecha, y se muestra primero otra dirección suya. Los borradores nuevos nunca se envían a esa dirección si se conoce otra. Si es la única, la ventana de envío te avisa, pero puedes enviar el correo de todos modos.

Se considera que un correo ha sido rechazado cuando el servidor de correo indica que la dirección no existe o después de 3 fallos temporales en una semana. El aviso desaparece cuando esa persona vuelve a escribir desde esa dirección o cuando se envía un correo correctamente a ella.

## Cargo y foto

Las personas con una dirección de empresa reciben un cargo, una foto, LinkedIn y una ciudad, consultados como los [datos de la organización](organization-data.md). En una Machine alojada, la consulta solo recibe su nombre y el dominio de la empresa. Para encontrar una foto, Gravatar recibe un hash de su dirección de trabajo, nunca la dirección en sí. Desactiva esta opción en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Cuando la consulta encuentra información, su página también muestra su descripción, desde cuándo ocupa el cargo actual y los dos cargos anteriores. La preparación también utiliza estos datos, pero solo muestra la descripción si la persona no tiene una biografía propia.

Tus conexiones se completan con la información que ya han leído: un cargo, teléfono y zona horaria de Slack; una biografía y ubicación de X; un titular y una foto de LinkedIn; cargos de Contactos de Google y Salesflare; y la foto de un contacto de Salesflare cuando la tiene guardada. Pasa el cursor por encima de la línea bajo su nombre para ver de dónde procede la información.

Outlook añade las fotos de tus compañeros de organización y de tus contactos de Outlook, además de los cargos y las empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram llegan mediante la sincronización de WhatsApp y la conexión con tus chats de Telegram: hasta 50 al día de cada servicio, solo para personas que ya están en tu Graph. No se les envía nada. Una importación de cumpleaños de Facebook añade la foto de perfil de alguien que no tenga foto cuando la guardas ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Team Graph](team-graph.md) de una Fleet de Trabajo, se incluye una copia pequeña de la foto de trabajo en el registro compartido de la persona. Nunca se comparten las fotos de Contactos de Google, WhatsApp, Telegram o Facebook, ni las fotos que hayas cambiado o quitado.

## Sobre ti

Tus propias direcciones y números, incluidos los alias, siempre son tuyos, nunca de alguien de tu Graph. Si te buscas o añades a una persona con una de tus direcciones, se abre **Sobre ti**. Al importar, se omite tu propia fila.

Sobre ti muestra tus direcciones y de dónde viene cada una. Puedes cambiarlas en **Ajustes**, en Cuenta. Para enviar tu propio contacto a un compañero o amigo, elige **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Los roles que tu Machine detecta en tus mensajes aparecen en su página, en **Para ti**, junto con la frase que ha leído. No hace falta esperar a que te lo pregunte. ¿Está mal? Corrígelo con **Editar** en su página o con **⋯** en la línea correspondiente de **Cambios recientes**. Aprende de tus cambios.

## Lo que sabe sobre alguien

Los datos sobre esa persona aparecen en su página, en **Información conocida**. Aprendizaje guarda los datos generales. **Añadir** permite guardar otro con tus propias palabras. Cada dato tiene un menú:

- **Editar** lo cambia ahí mismo.
- **No es sobre esta persona** lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, que aparece plegado justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido: un rol, dónde trabaja alguien, la relación entre dos personas, un dato o un cambio de proyecto. Cada línea indica la fecha y el origen; toca el origen para leer el mensaje.

Si una línea está mal, puedes corregirla desde su **⋯**: **Editar**, **Quitar**, **No es sobre esta persona** o **Deshacer** para devolver un proyecto a su estado anterior. Se muestran tres líneas; **Mostrar más** muestra el resto.

Si tu Machine ha actualizado a alguien hoy, aparece un punto pequeño junto a su nombre en la lista Personas y **4 personas actualizadas hoy** en la parte superior de la lista indica quiénes son. Consulta [The Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea** en el menú **⋯** de una persona, organización o proyecto crea una tarea sobre esa persona, organización o proyecto.
