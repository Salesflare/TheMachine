---
title: Personas
area: graph
summary: Todas las personas con las que estás en contacto: sus páginas, resúmenes y cronologías, y cómo añadirlas, editarlas, fusionarlas o eliminarlas.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: b23d3ebdc4f162f2
---
Todas las personas con las que estás en contacto, empezando por las más cercanas, según tus mensajes y reuniones. Los boletines, recibos y otros correos no añaden a nadie hasta que respondes. Están en Remitentes ocultos, debajo de la lista. **Mostrar como persona** añade a alguien. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada lista tiene sus propios filtros: consulta [Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre de una tienda) se cuenta para su organización, no como persona, incluso después de que escribas a esa dirección.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea sobre cómo estáis en contacto ("Habláis a diario · último contacto ayer · próxima reunión mar., 27 oct."). El contacto reciente aparece como «ahora mismo», «hace 3 horas», «ayer» o «hace 3 días». Si es anterior, aparece la fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo verás:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar**. Aquí también aparece su **Cumpleaños**, junto con el origen de la información (Google Contacts, Google Calendar, Facebook, tus notas o tú): consulta [Graph](graph.md#birthday).
- **Contigo**: quién es para ti, si es un contacto de Trabajo o Personal y si forma parte de tu familia o de tu Fleet, con **Ver en Fleet**.
- **También en**: los otros sitios donde hablas con esa persona. **Slack** la abre en Slack o abre el hilo más reciente que tengáis allí.
- Las **Personas** y los **Proyectos** de los que forma parte, lo **Pendiente entre ambos** (promesas en ambas direcciones, con **Marcar como hecho** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se unen automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, si un correo del trabajo tiene su dirección personal en copia. También se unen cuando alguien con quien chateas reserva una llamada desde el enlace que le enviaste y coincide el nombre de su empresa o su apellido.

Si una página muestra **No se ha podido cargar esta página.**, toca **Reintentar**. Si sigue apareciendo, usa **¿Algo va mal?** en la parte inferior de la página.

## Resumen

Unas líneas breves en la parte superior de la página de una persona: qué se decidió, pidió, planeó o prometió, con los nombres de todas las personas implicadas. The Machine lo reescribe cuando hay novedades, solo para personas con las que estás realmente en contacto, y revisa cada línea antes. Normalmente, una vez al día. Si cambia algo relacionado con esa persona, como un nuevo plazo o una petición que se retira, lo actualiza en unas horas.

Si una línea es imprecisa, se omite. Si no hay nada concreto que decir, no hay resumen. Cada línea enlaza con su origen: los mensajes de un mismo día comparten fecha y muestran su número, y se abren juntos.

**Editar** para expresarlo a tu manera. Cuando haya novedades, The Machine muestra una **Actualización sugerida** con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** se lo devuelve.

La preparación de reuniones también usa el resumen, pero solo las líneas del área de esa tarea, Trabajo o Personal. Se queda en tu Machine. Tu equipo nunca lo ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de más reciente a más antigua: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y cambios de proyectos. Los botones de filtro de arriba muestran una fuente cada vez. **Mostrar más** carga los elementos anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, empezando por la más cercana. **Mostrar todos los próximos** muestra las demás. En cada reunión aparecen las personas que asistieron, una sola vez cada una. Si hay notas o una transcripción, aparece **Notas** o **Transcripción**. Haz clic para leerlas.

Tus cronologías son tuyas: el Graph del equipo solo muestra lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la cronología, añade lo que han compartido tus compañeros. Cada elemento indica quién lo compartió. **Míos** muestra solo lo tuyo.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran a las personas según su tipo, el que aparece en su página. Si eliges uno (**Editar**), tiene prioridad. Si no, tu familia y tus amigos, y quienes son familia o amigos para ti (tu mujer, tu padre), se consideran Personal, independientemente de la dirección desde la que escriban. Tu equipo nunca ve los contactos personales.

## Añadir a alguien

Toca **Nueva persona** en la parte superior de Personas o **+** en la barra superior del móvil. Añade un nombre y, si los tienes, un correo y una organización. Si alguien parecido ya está en tu Graph, aparecerá primero en el formulario para que puedas abrir esa ficha en su lugar. **Añadir** abre la página nueva.

La persona que añadas se queda, incluso si todavía no hay mensajes. Su primer mensaje la vincula.

## Editar a alguien

**Editar**, en la parte superior de su página, permite cambiar su nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, quién es para ti y si es de Trabajo o Personal. El campo **Notas** es para cualquier cosa que quieras recordar. Las notas se conservan al fusionar personas. **Guardar** conserva los cambios y **Cancelar** los descarta.

Tus cambios se conservan, incluso cuando se vuelven a consultar sus datos, y también al **Fusionar** y **Deshacer**. Si dejas un campo vacío, se vuelve a usar el valor consultado. Si borras el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella: **Subir una imagen**, elige una imagen encontrada para esa persona o **Quitar imagen**. La imagen se queda en tu Machine.

## Fusionar a dos personas

Si dos personas podrían ser la misma, su página te pregunta si lo son, y Personas las muestra en **¿Misma persona?**. **Fusionar** las une, junto con todos sus mensajes, notas, funciones y proyectos. **No es la misma** las mantiene separadas definitivamente. Tu respuesta aparece un momento en la pareja, y luego la pareja desaparece de la lista. La lista desaparece cuando ya no queda nada que consultar.

Nunca se propone que alguien con una dirección que solo se parece a otra que conoces, como acme-corp.example y acmecorp.example, sea la misma persona. Solo tú puedes asignarle una función.

Un nombre por sí solo nunca basta para relacionar a dos personas de dominios distintos, porque cualquiera puede escribir un nombre. Solo se propone unir dos direcciones de dominios distintos si hay otra conexión, como las mismas personas o un proyecto. Nunca se propone unir a alguien que usa tu nombre con una dirección que no es tuya. En su lugar, añade tus otras direcciones en Ajustes, [Tus direcciones](settings.md#your-addresses).

Si solo coincide el nombre de pila en dominios distintos, como «Sam» y «Sam Lee», solo se propone unirlos si tienen el mismo número de teléfono o perfil de LinkedIn.

Si solo coincide el nombre de pila con el de una reunión creada a partir de un chat, o la dirección es de alguien que ya conocías y solo esa persona dice en el chat que es suya, se te pregunta. The Machine nunca abre un enlace para averiguarlo.

Nunca se une una dirección compartida, como info@ o una lista de correo, con las personas que escriben a través de ella. Un contacto de trabajo de fuera de tu empresa y un chat personal que solo comparten un nombre tampoco se unen automáticamente. Aparecen como una pregunta.

**Fusionar todo** une de una vez todas las parejas de la lista, excepto las que marcaste como **No es la misma**. **Deshacer** las separa todas de nuevo si lo haces justo después.

Para unir a dos personas, abre una de sus páginas, toca **⋯**, **Misma persona que…** y elige a la otra. En la página de la persona unida se indica el motivo en **Unida desde**, con **Deshacer** para separarlas de nuevo.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯ y elige **Eliminar para siempre…**. Después, toca **Eliminar**. Se eliminarán la persona y todo lo que tu Machine sabe de ella: su ficha, direcciones, datos consultados, los mensajes que solo intercambiasteis entre vosotros y las notas sobre esa persona.

Las tareas relacionadas con esa persona se conservan, pero se elimina su nombre. No se volverá a añadir, tampoco mediante una importación ni una tarea de cumpleaños de Facebook con su nombre o dirección. No se puede deshacer.

## Correo devuelto

Si se devuelve un correo que enviaste a alguien, su dirección aparece como **Devuelto** junto con la fecha, y se muestra primero otra dirección suya. Los borradores nuevos nunca se envían a esa dirección si se conoce otra. Si es la única, la pantalla de envío te avisa, pero puedes enviar el correo igualmente.

Se considera devuelto cuando el servidor de correo indica que la dirección no existe o tras 3 fallos temporales a lo largo de una semana. El aviso desaparece cuando esa persona vuelve a escribir desde esa dirección o cuando se envía correctamente un correo a ella.

## Cargo y foto

Las personas con una dirección de empresa tienen un cargo, una foto, LinkedIn y una ciudad, consultados como se describe en [Datos de la organización](organization-data.md). En una Machine alojada, la consulta solo recibe su nombre y el dominio de la empresa. Para obtener una foto, Gravatar recibe un hash de su dirección de trabajo, nunca la dirección en sí. Puedes desactivar esta opción en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Esa opción también impide consultar la página web antes de una primera reunión y hacer búsquedas web si hay un proveedor de búsqueda configurado (consulta [Lista para tus reuniones](calendar.md#ready-for-your-meetings)).

Si la consulta encuentra información sobre esa persona, su página también muestra su texto «Acerca de», desde cuándo ocupa su puesto actual y sus dos puestos anteriores. La preparación también usa esta información, pero solo el texto «Acerca de» si la persona no tiene una biografía propia.

Tus conexiones se completan con la información que ya han leído: un cargo, teléfono y zona horaria de Slack; una biografía y ubicación de X; un titular y foto de LinkedIn; cargos de Google Contacts y Salesflare; y la foto de un contacto de Salesflare, si Salesflare la conserva. Pasa el cursor por la línea debajo de su nombre para ver de dónde procede.

Outlook añade las fotos de los compañeros de tu organización y de tus contactos de Outlook, además de los cargos y empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram llegan a través de tu sincronización de WhatsApp y la conexión de tus chats de Telegram: hasta 50 al día en cada servicio, solo para personas que ya están en tu Graph. No se les envía nada. Una importación de cumpleaños de Facebook añade la foto de perfil de alguien que no tenga foto cuando la guardas ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Graph del equipo](team-graph.md) de un Fleet de trabajo, se comparte una copia pequeña de la foto de trabajo con el registro compartido de una persona. Nunca se comparten las fotos de Google Contacts, WhatsApp, Telegram o Facebook, ni las fotos que hayas cambiado o quitado.

## Sobre ti

Tus propias direcciones y números, incluidos los alias, siempre son tuyos y nunca pertenecen a alguien de tu Graph. Si te buscas o añades a alguien con una de tus direcciones, se abre **Sobre ti**, y la importación omite tu propia fila.

Sobre ti muestra tus direcciones y el origen de cada una. Puedes cambiarlas en **Ajustes**, en Cuenta. Para enviar tu propio contacto a un compañero o amigo, elige **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Quién es para ti

Las funciones que tu Machine detecta en tus mensajes aparecen en su página, en **Para ti**, junto con las palabras que indican la función, como un cargo. Que alguien diga que es tu contable o tu cliente no basta. También hace falta información de tu parte, como tus propios mensajes o reuniones con esa persona. No hace falta que confirmes nada. ¿No es correcto? **Editar** en su página lo corrige, o toca **⋯** en su línea de **Cambios recientes**. Aprende de tus cambios.

## Lo que sabe de alguien

La información sobre esa persona aparece en su página, en **Información conocida**. Aprendizaje conserva los datos generales. **Añadir** guarda otro dato con tus propias palabras. Cada dato tiene un menú:

- **Editar** permite cambiarlo ahí mismo.
- **No es sobre esta persona** lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, contraído justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido sobre esa persona: una función, dónde trabaja, la relación entre dos personas, un dato o un cambio de proyecto. Cada línea muestra la fecha y el origen. Toca el origen para leer el mensaje.

Si una línea es incorrecta, puedes corregirla ahí mismo con **⋯**: **Editar**, **Quitar**, **No es sobre esta persona** o **Deshacer** para devolver un proyecto a su ubicación anterior. Se muestran tres líneas. **Mostrar más** muestra las demás.

Si tu Machine ha actualizado a alguien hoy, aparece un pequeño punto junto a su nombre en la lista de Personas, y el aviso **4 personas actualizadas hoy** en la parte superior de la lista indica quiénes son. Consulta [Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea**, en el menú **⋯** de una persona, organización o proyecto, crea una tarea sobre esa persona.
