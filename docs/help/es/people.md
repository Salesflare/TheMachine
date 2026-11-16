---
title: Personas
area: graph
summary: Todas las personas con las que tienes contacto: su página, resumen y cronología, y cómo añadirlas, editarlas, fusionarlas o eliminarlas.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: a16cc66e51a64fd2
---
Todas las personas con las que tienes contacto, primero las más cercanas, a partir de tus mensajes y reuniones. Los boletines, recibos y otros envíos no añaden a nadie hasta que respondas. Aparecen en Remitentes ocultos, debajo de la lista: **Mostrar como persona** añade a alguien a la lista. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada lista tiene sus propios filtros: consulta [The Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre de una tienda) cuenta como organización, no como persona, incluso después de que le escribas.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una frase sobre cómo estás en contacto con esa persona («Hablan a diario · último contacto ayer · próxima reunión mar., 27 oct.»). El contacto reciente aparece como «ahora mismo», «hace 3 horas», «ayer» o «hace 3 días»; los contactos más antiguos aparecen con la fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo encontrarás:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar** para copiarlo. Aquí también aparece su **Cumpleaños**, junto con la fuente (Contactos de Google, Google Calendar, Facebook, tus notas o tú): consulta [The Graph](graph.md#birthday).
- **Contigo**: qué relación tiene contigo, si es un contacto de Trabajo o Personal, y si forma parte de tu familia o de Fleet, con **Ver en Fleet**.
- **También en**: los otros lugares donde hablas con esa persona. **Slack** la abre en Slack o abre el hilo más reciente que tienes con ella en Slack.
- **Personas** y **Proyectos** de los que forma parte, **Pendiente entre ambos** (promesas en ambos sentidos, con **Marcar como hecha** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se unen automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, un correo de trabajo con su dirección personal en copia.

Si aparece el mensaje **No se ha podido cargar esta página.**, toca **Reintentar**. Si sigue apareciendo, usa **¿Algo va mal?** al final de la página.

## Resumen

Unas pocas frases al principio de la página de una persona: lo que se decidió, pidió, planeó o prometió, con los nombres de todas las personas. The Machine lo reescribe cuando hay novedades, solo para las personas con las que realmente tienes contacto, y comprueba cada frase antes. Normalmente, una vez al día; en unas horas si cambia algo relacionado con esa persona, como una nueva fecha límite o una petición que se retira.

Si una frase es imprecisa, se omite. Si no hay nada concreto que decir, no aparece ningún resumen. Cada frase enlaza a su fuente: los mensajes de un mismo día comparten una fecha con el número de mensajes y se abren juntos.

**Editar** el resumen para expresarlo a tu manera. Cuando haya novedades, The Machine muestra una **Actualización sugerida**, con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** permite que The Machine vuelva a redactarlo.

Los preparativos de reuniones usan este resumen, pero solo las frases relacionadas con el tipo de tarea, Trabajo o Personal. Se queda en tu Machine; tu equipo nunca lo ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de más reciente a más antigua: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y cambios en proyectos. Los filtros de arriba muestran una fuente cada vez. **Mostrar más** carga los elementos anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, empezando por la más cercana; **Mostrar todos los próximos** muestra las demás. En cada reunión aparecen las personas que asistieron, cada una una sola vez. Las reuniones con notas o transcripción muestran **Notas** o **Transcripción**; haz clic para leerlas.

Tus cronologías son privadas: el Graph del equipo solo muestra lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la cronología, añade lo que han compartido tus compañeros de equipo; cada elemento indica quién lo compartió. **Míos** muestra solo lo tuyo.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran a las personas según su tipo, que aparece en su página. Si eliges uno (**Editar**), esa elección prevalece. De lo contrario, tus familiares y amigos, y quienes son familiares o amigos tuyos (tu esposa, tu padre), aparecen como Personal, sin importar desde qué dirección escriban. Tu equipo nunca ve los contactos personales.

## Añadir a alguien

Toca **Nueva persona** en la parte superior de Personas o **+** en la barra superior del teléfono. Escribe un nombre y, si los tienes, un correo y una organización. Si ya hay alguien parecido en tu Graph, el formulario lo muestra primero para que puedas abrir esa página. **Añadir** crea la página de la persona.

La persona que añadas seguirá ahí aunque todavía no haya mensajes. Su primer mensaje se asociará a su ficha.

## Editar a una persona

**Editar**, en la parte superior de su página, permite cambiar su nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, qué relación tiene contigo y si es Trabajo o Personal. El campo **Notas** sirve para guardar lo que quieras recordar; las notas se conservan al fusionar personas. **Guardar** conserva los cambios y **Cancelar** los descarta.

Tus cambios se conservan, incluso cuando se vuelven a buscar sus datos y al usar **Fusionar** o **Deshacer**. Borra un campo para volver a usar el valor encontrado. Si borras el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella: **Subir una imagen**, elige una que se haya encontrado para esa persona o **Quitar imagen**. La foto se queda en tu Machine.

## Fusionar a dos personas

Si dos personas podrían ser la misma, su página te pregunta si lo son y Personas las muestra en **¿Misma persona?**. **Fusionar** las une, junto con todos sus mensajes, notas, roles y proyectos. **No es la misma** las mantiene separadas definitivamente. Tu respuesta aparece un momento junto a la pareja y luego desaparece de la lista. La lista desaparece cuando ya no queda nada por preguntar.

Nunca se sugiere que alguien con una dirección que solo se parece a otra que conoces, como acme-corp.example y acmecorp.example, sea la misma persona. Además, solo tú puedes asignarle un rol.

Un nombre por sí solo nunca basta para unir personas de dos dominios, porque cualquiera puede escribirlo. Solo se sugiere unir dos direcciones de dominios distintos si hay algún otro vínculo, como las mismas personas o un proyecto. Nunca se sugiere que alguien que use tu nombre en una dirección que no es tuya seas tú. Añade tus otras direcciones en Ajustes, [Tus direcciones](settings.md#your-addresses).

Si solo coincide el nombre de pila en dominios distintos, como «Sam» y «Sam Lee», solo se sugiere unirlos si tienen el mismo número de teléfono o perfil de LinkedIn.

Una dirección compartida, como info@ o una lista de correo, nunca se une a las personas que escriben a través de ella. Un contacto de trabajo de fuera de tu empresa y un chat personal que solo comparten un nombre no se unen automáticamente: aparecen como una pregunta.

**Fusionar todo** une todas las parejas de la lista a la vez, excepto las que marcaste con **No es la misma**. Si usas **Deshacer** justo después, se separan todas de nuevo.

Para unir a dos personas, abre una de sus páginas y selecciona **⋯**, **Misma persona que…** y la otra persona. La página de una persona fusionada muestra el motivo en **Unida a partir de**, con **Deshacer** para separarlas de nuevo.

## Eliminar a una persona para siempre

En su página, abre el menú ⋯ y selecciona **Eliminar para siempre…**. Luego, toca **Eliminar**. Esto elimina a la persona y todo lo que tu Machine sabe sobre ella: su ficha, direcciones, datos encontrados, los mensajes que solo intercambiaron ustedes dos y las notas sobre esa persona.

Las tareas que la incluyan se conservan, pero se elimina su nombre. No se volverá a añadir, tampoco mediante una importación ni una tarea de cumpleaños de Facebook que incluya su nombre o dirección. Esta acción no se puede deshacer.

## Correos devueltos

Si un correo que envías a alguien se devuelve, su dirección aparece como **Devuelta**, con la fecha, y otra dirección suya pasa a ocupar el primer lugar. Los borradores nuevos nunca se envían a esa dirección si se conoce otra. Si es la única, la pantalla de envío te avisa, pero puedes enviar el correo de todos modos.

Se considera que un correo se ha devuelto cuando el servidor indica que la dirección no existe o después de 3 fallos temporales en una semana. El aviso desaparece cuando la persona vuelve a escribirte desde esa dirección o cuando se envía correctamente un correo a esa dirección.

## Cargo y foto

A las personas con una dirección de empresa se les buscan el cargo, la foto, LinkedIn y la ciudad, igual que [los datos de organizaciones](organization-data.md). En una Machine alojada, la búsqueda solo recibe el nombre y el dominio de la empresa. Para encontrar una foto, Gravatar recibe un hash de la dirección de trabajo, nunca la dirección en sí. Puedes desactivarlo en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Cuando se encuentran esos datos, la página también muestra el texto de presentación, desde cuándo ocupa su puesto actual y sus dos puestos anteriores. Los preparativos también los leen, pero solo usan el texto de presentación si la persona no tiene una biografía propia.

Tus Conexiones se completan con los datos que ya han leído: cargo, teléfono y zona horaria de Slack; biografía y ubicación de X; titular y foto de LinkedIn; cargos de Contactos de Google y Salesflare; y la foto de un contacto de Salesflare, si Salesflare la guarda. Pasa el cursor por encima de la línea bajo su nombre para ver de dónde procede.

Outlook añade fotos de colegas de tu organización y de tus contactos de Outlook, además de los cargos y las empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram llegan mediante la sincronización de WhatsApp y la conexión de tus chats de Telegram: hasta 50 al día de cada servicio, solo para personas que ya están en tu Graph. No se envía nada a esas personas. Una importación de cumpleaños de Facebook añade la foto de perfil de las personas que no tengan foto cuando la guardes ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Graph del equipo](team-graph.md) de un Fleet de Trabajo, se incluye una copia pequeña de la foto de trabajo en el registro compartido de una persona. Nunca se incluyen fotos de Contactos de Google, WhatsApp, Telegram o Facebook, ni fotos que hayas cambiado o quitado.

## Sobre ti

Tus propias direcciones y números, incluidos tus alias, siempre son tuyos, nunca de alguien de tu Graph. Si te buscas o añades a una persona con una de tus direcciones, se abre **Sobre ti**. Las importaciones omiten tu propia fila.

Sobre ti muestra tus direcciones y de dónde procede cada una. Cámbialas en **Ajustes**, en Cuenta. Para enviar tus datos de contacto a un compañero de equipo o amigo, selecciona **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Los roles que tu Machine detecta en tus mensajes aparecen en su página, en **Para ti**, con solo las palabras que indican el rol, como un cargo. Que alguien diga que es tu contable o tu cliente no basta: también hace falta información de tu parte, como tus propios mensajes o reuniones con esa persona. No hace falta que lo confirmes. ¿Está mal? **Editar** en su página permite corregirlo, o puedes usar **⋯** en la línea correspondiente de **Cambios recientes**. The Machine aprende de tus cambios.

## Lo que sabe sobre alguien

Los datos sobre una persona aparecen en su página, en Información conocida; Aprendizaje guarda los datos generales. **Añadir** permite guardar otro dato con tus propias palabras. Cada dato tiene un menú:

- **Editar** lo cambia directamente.
- **No es sobre esta persona** lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, desplegado justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido: un rol, dónde trabaja alguien, la relación entre dos personas, un dato o un cambio de proyecto. Cada línea muestra la fecha y la fuente; toca la fuente para leer el mensaje.

Si una línea no es correcta, puedes corregirla directamente desde **⋯**: **Editar**, **Quitar**, **No es sobre esta persona** o **Deshacer** para devolver un proyecto a su estado anterior. Se muestran tres líneas; **Mostrar más** muestra las demás.

En la lista de Personas, un punto pequeño marca a quien tu Machine haya actualizado hoy. En la parte superior de la lista, **4 personas actualizadas hoy** indica quiénes son. Consulta [The Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea**, en el menú **⋯** de una persona, organización o proyecto, crea una tarea sobre esa persona, organización o proyecto.
