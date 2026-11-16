---
title: Personas
area: graph
summary: Todas las personas con las que estás en contacto: su página, resumen y cronología, y cómo añadir, editar, fusionar o eliminar a alguien.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 0eb2dcc70fba84c2
---
Todas las personas con las que estás en contacto, empezando por las más cercanas, según tus mensajes y reuniones. Los boletines, recibos y otros envíos no añaden a nadie hasta que respondes. Aparecen en Remitentes ocultos, debajo de la lista: **Mostrar como persona** añade a alguien. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada lista tiene sus propios filtros: consulta [Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre de una tienda) cuenta como parte de su organización, no como una persona, incluso después de que le escribas.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea sobre cómo estás en contacto con ella («Hablan a diario · último contacto ayer · próxima reunión mar, 27 oct»). El contacto reciente aparece como «ahora mismo», «hace 3 horas», «ayer» o «hace 3 días», y el contacto más antiguo, como una fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo encontrarás:

- **Contacto**: sus teléfonos y direcciones de correo. Toca uno para llamar o escribir, o **Copiar** para copiarlo. Aquí también aparece su **Cumpleaños**, junto con su origen (Contactos de Google, Google Calendar, Facebook, tus notas o tú): consulta [Graph](graph.md#birthday).
- **Contigo**: qué relación tiene contigo, si es un contacto de Trabajo o Personal, y si forma parte de tu familia o Fleet, con la opción **Ver en Fleet**.
- **También en**: otros lugares donde hablas con esa persona. **Slack** la abre en Slack o abre el hilo más reciente que tienes con ella en Slack.
- **Personas** y **Proyectos** de los que forma parte, **Pendiente entre ambos** (promesas en ambos sentidos, con **Marcar como hecha** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se vinculan automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, si aparece un correo de trabajo con su dirección personal en copia.

Si una página muestra **No se ha podido cargar esta página.**, toca **Reintentar**. Si sigue apareciendo el mensaje, toca **¿Algo va mal?** al final de la página.

## Resumen

Unas pocas líneas al principio de la página de una persona: qué se decidió, pidió, planeó o prometió, con los nombres de todos. The Machine lo reescribe cuando hay novedades, solo para las personas con las que realmente estás en contacto, y comprueba cada línea antes de mostrarla. Normalmente, una vez al día; en unas horas si cambia algo relacionado con esa persona, como una nueva fecha límite o una solicitud retirada.

Si una línea es vaga, se omite; si no hay nada concreto que decir, no aparece ningún resumen. Cada línea enlaza con su origen: los mensajes de un mismo día comparten fecha y muestran la cantidad, y se abren juntos.

**Editar** te permite expresarlo a tu manera. Cuando hay novedades, The Machine muestra una **Actualización sugerida** con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** le devuelve la tarea.

La preparación de reuniones usa este resumen, pero solo las líneas de la categoría de esa tarea (Trabajo o Personal). Se queda en tu Machine; tu equipo nunca la ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de lo más reciente a lo más antiguo: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y cambios en proyectos. Los filtros de arriba muestran una fuente a la vez. **Mostrar más** carga los elementos anteriores.

Las reuniones futuras aparecen arriba, en **Lo próximo**, empezando por la más cercana; **Mostrar todos los próximos** muestra las demás. En una reunión aparecen las personas que participaron, una sola vez cada una. Si tiene notas o una transcripción, aparece **Notas** o **Transcripción**; haz clic para leerlas.

Tus cronologías son solo tuyas: el Graph del equipo muestra únicamente lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la Cronología, añade lo que compartieron tus compañeros de equipo; cada elemento indica quién lo compartió. **Míos** muestra solo los tuyos.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran a las personas según su tipo, que aparece en su página. Tu elección (**Editar**) tiene prioridad. De lo contrario, tu familia y tus amigos, y las personas que son familia o amigas tuyas (una esposa, un padre), son de tipo Personal, sin importar desde qué dirección escriban. Tu equipo nunca ve los contactos personales.

## Añadir a alguien

Toca **Nueva persona** en la parte superior de Personas o **+** en la barra superior desde el teléfono. Añade un nombre y, si los tienes, un correo y una organización. Si ya hay alguien parecido en tu Graph, el formulario lo muestra primero para que puedas abrir esa ficha. **Añadir** abre la nueva página.

La persona que añadas se queda en tu lista, aunque todavía no haya mensajes. Su primer mensaje la vincula.

## Editar a alguien

La opción **Editar**, en la parte superior de su página, te permite cambiar su nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, qué relación tiene contigo y si es de tipo Trabajo o Personal. El campo **Notas** sirve para lo que quieras recordar; las notas se conservan al fusionar personas. **Guardar** guarda los cambios y **Cancelar** los descarta.

Tus cambios se conservan aunque vuelvas a buscar sus datos, y también al usar **Fusionar** y **Deshacer**. Borra un campo para volver a usar el valor encontrado. Si borras el nombre, vuelve a aparecer el que figura en sus mensajes.

Para cambiar su foto, haz clic en ella y elige **Subir una imagen**, selecciona una de las imágenes encontradas para esa persona o toca **Quitar imagen**. La foto se queda en tu Machine.

## Fusionar a dos personas

Si dos personas podrían ser la misma, su página te pregunta si se trata de la misma persona y Personas las muestra en **¿Misma persona?**. **Fusionar** las combina, junto con todos sus mensajes, notas, roles y proyectos. **No es la misma** las mantiene separadas definitivamente. Tu respuesta aparece durante un momento en el par, que luego desaparece de la lista. La lista desaparece cuando ya no hay nada que consultar.

Nunca se sugiere que alguien con una dirección que solo se parece a una que conoces, como acme-corp.example y acmecorp.example, sea la misma persona. Solo tú puedes asignarle un rol.

Un nombre por sí solo nunca basta para unir personas de dos dominios, porque cualquiera puede escribirlo. Solo se sugieren dos direcciones de dominios distintos si hay algún otro vínculo, como las mismas personas o un proyecto. Nunca se sugiere a alguien que usa tu mismo nombre con una dirección que no es tuya. En su lugar, añade tus otras direcciones en **Ajustes**, en [Tus direcciones](settings.md#your-addresses).

Si solo coincide el nombre de pila en distintos dominios, como «Sam» y «Sam Lee», solo se sugieren si tienen el mismo número de teléfono o perfil de LinkedIn.

Nunca se vincula una dirección compartida, como info@ o una lista de correo, con las personas que escriben a través de ella. Un contacto de trabajo de fuera de tu empresa y un chat personal que solo comparten un nombre no se vinculan automáticamente: aparecen como una consulta.

**Fusionar todo** combina de una vez todos los pares de la lista, excepto los que marcaste con **No es la misma**. Si tocas **Deshacer** justo después, los separa de nuevo.

Para unir a dos personas por tu cuenta, abre una de ellas, toca **⋯**, **Misma persona que…** y elige a la otra. En la página de la persona unificada, debajo de **Combinada desde**, aparecen los motivos. Toca **Deshacer** para volver a separarlas.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯, elige **Eliminar para siempre…** y luego **Eliminar**. Se elimina a esa persona y todo lo que tu Machine sabe de ella: su ficha, direcciones, datos encontrados, los mensajes que solo intercambiaron entre ustedes y las notas sobre ella.

Las tareas en las que participa se conservan, pero se quita su nombre. No se volverá a añadir, ni siquiera mediante una importación o una tarea de cumpleaños de Facebook que incluya su nombre o dirección. Esta acción no se puede deshacer.

## Correos devueltos

Cuando un correo que envías a alguien se devuelve, su dirección aparece como **Devuelto**, junto con la fecha, y se muestra primero otra dirección suya. Si se conoce otra dirección, los nuevos borradores nunca se envían a la dirección devuelta. Si es la única dirección, la pantalla de envío te avisa, pero puedes enviar el correo igualmente.

Un correo cuenta como devuelto cuando el servidor indica que la dirección no existe o tras 3 fallos temporales en una semana. El aviso desaparece cuando esa persona vuelve a escribir desde esa dirección o cuando se envía un correo correctamente a ella.

## Cargo y foto

A las personas con una dirección de empresa se les busca el cargo, la foto, LinkedIn y la ciudad, como se describe en [los datos de organizaciones](organization-data.md). En una Machine alojada, la búsqueda solo recibe su nombre y el dominio de su empresa. Para obtener una foto, Gravatar recibe un hash de su dirección de trabajo, nunca la dirección en sí. Puedes desactivarlo en **Ajustes**, en Seguridad, con la opción **Buscar contactos de trabajo**.

Si la búsqueda encuentra información sobre esa persona, su página también muestra su descripción, desde cuándo ocupa su cargo actual y los dos cargos anteriores. La preparación de reuniones también la consulta; solo usa la descripción si la persona no tiene una biografía propia.

Tus conexiones se completan con la información que ya consultan: un cargo, teléfono y zona horaria de Slack; una biografía y ubicación de X; un titular y una foto de LinkedIn; cargos de Contactos de Google y Salesflare; y la foto de un contacto de Salesflare si Salesflare tiene una. Pasa el cursor por la línea debajo de su nombre para ver de dónde salió la información.

Outlook añade las fotos de los compañeros de tu organización y de tus contactos de Outlook, además de los cargos y las empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram se obtienen mediante la sincronización de WhatsApp y la conexión de tus chats de Telegram: hasta 50 al día de cada servicio, solo para las personas que ya están en tu Graph. No se les envía nada. Una importación de cumpleaños de Facebook añade la foto de perfil de una persona que no tenga foto cuando la guardes ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Graph del equipo](team-graph.md) de un Fleet de Trabajo, se comparte una copia pequeña de la foto de trabajo con la ficha de esa persona. Nunca se comparten las fotos de Contactos de Google, WhatsApp, Telegram o Facebook, ni las fotos que hayas cambiado o quitado.

## Sobre ti

Tus direcciones y números, incluidos tus alias, siempre son tuyos, nunca de alguien en tu Graph. Si te buscas o añades a alguien con una de tus direcciones, se abre **Sobre ti**; una importación omite tu propia fila.

Sobre ti muestra tus direcciones y de dónde viene cada una. Cámbialas en **Ajustes**, en Cuenta. Para enviar tu contacto a un compañero o amigo, toca **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Los roles que tu Machine detecta en tus mensajes aparecen en la página de esa persona, en **Para ti**, junto con la frase que los identificó. No tienes que confirmarlos. ¿No es correcto? **Editar** en su página lo corrige, o toca **⋯** en la línea correspondiente de **Cambios recientes**. The Machine aprende de tus cambios.

## Lo que sabe de alguien

Los datos sobre esa persona aparecen en su página, en **Información conocida**; en Aprendizaje se guardan los datos generales. Toca **Añadir** para agregar otro con tus propias palabras. Cada dato tiene un menú:

- **Editar** lo cambia ahí mismo.
- **No es sobre esta persona** lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, desplegado justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine cambió o aprendió sobre ese elemento: un rol, dónde trabaja alguien, la relación entre dos personas, un dato o un cambio de proyecto. Cada línea tiene su fecha y su origen; toca el origen para leer el mensaje.

Si una línea es incorrecta, toca **⋯** para corregirla ahí mismo: **Editar**, **Quitar**, **No es sobre esta persona** o **Deshacer** para devolver un proyecto a donde estaba. Se muestran tres líneas; **Mostrar más** muestra las demás.

Una persona cuyos datos haya actualizado tu Machine hoy aparece con un punto pequeño en la lista Personas, y **4 personas actualizadas hoy** aparece en la parte superior de la lista con sus nombres. Consulta [Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea**, en el menú **⋯** de una persona, organización o proyecto, crea una tarea sobre ese elemento.
