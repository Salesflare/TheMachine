---
title: Personas
area: graph
summary: Todas las personas con las que estás en contacto: su página, resumen y cronología, y cómo añadirlas, editarlas, fusionarlas o eliminarlas.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e671ff84b143e74
---
Todas las personas con las que estás en contacto, empezando por las más cercanas, a partir de tus mensajes y reuniones. Los boletines, recibos y otros envíos no añaden a nadie hasta que respondes. Aparecen en Remitentes ocultos, debajo de la lista: **Mostrar como persona** añade a alguien. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada lista tiene sus propios filtros: consulta [Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre propio de una tienda) cuenta para su organización, no como una persona, incluso después de escribirle.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea sobre cómo estáis en contacto ("Habláis a diario · último contacto ayer · próxima reunión: mar, 27 oct"). El contacto reciente aparece como "justo ahora", "hace 3 horas", "ayer" o "hace 3 días"; el contacto anterior aparece como una fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar**. Aquí también aparece su **Cumpleaños**, junto con su origen (Contactos de Google, Google Calendar, Facebook, tus notas o tú): consulta [Graph](graph.md#birthday).
- **Contigo**: qué relación tiene contigo, si es un contacto de Trabajo o Personal, y si pertenece a tu familia o a tu Fleet, con **Ver en Fleet**.
- **También en**: otros lugares donde habláis. **Slack** abre su perfil en Slack o el hilo más reciente que tengas con esa persona.
- Las **Personas** y los **Proyectos** de los que forma parte, lo **Pendiente entre ambos** (promesas en ambas direcciones, con **Marcar como hecho** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se unen automáticamente cuando está claro que corresponden a la misma persona, por ejemplo, si un correo de trabajo aparece con su dirección personal en copia. También se unen cuando alguien con quien chateas reserva una llamada desde el enlace que le enviaste y coincide su empresa o apellido.

Si aparece **No se ha podido cargar esta página.**, toca **Reintentar**. Si el mensaje sigue apareciendo, usa **¿Algo va mal?** al final de la página.

## Resumen

Unas pocas líneas breves en la parte superior de la página de una persona: lo que se decidió, pidió, planeó o prometió, con los nombres de todos. The Machine lo reescribe cuando hay novedades, solo para las personas con las que realmente estás en contacto, y revisa cada línea antes. Normalmente, una vez al día; en unas horas si cambia algo relacionado con esa persona, como una nueva fecha límite o una petición que se retira.

Si una línea es imprecisa, se omite. Si no hay nada concreto que decir, no hay resumen. Cada línea enlaza con su origen: los mensajes de un mismo día aparecen juntos con una fecha y el número de mensajes, y se abren a la vez.

**Editar** para escribirlo a tu manera. Cuando hay novedades, The Machine muestra una **Actualización sugerida** con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** se lo devuelve.

La preparación de reuniones usa este resumen, pero solo las líneas del tipo de tarea correspondiente (Trabajo o Personal). Se queda en tu Machine; tu equipo no la ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de más reciente a más antigua: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y movimientos de proyectos. Los filtros de arriba muestran un origen cada vez. **Mostrar más** carga los anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, empezando por la más cercana. **Mostrar todos los próximos** muestra el resto. En cada reunión aparecen las personas que asistieron, una sola vez cada una. Las reuniones con notas o transcripción indican **Notas** o **Transcripción**; haz clic para leerlas.

Tus cronologías son tuyas: el Graph del equipo solo muestra lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la cronología, añade lo que han compartido tus compañeros, y cada elemento indica quién lo compartió. **Míos** muestra solo lo tuyo.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran a las personas según su tipo, que aparece en su página. Si eliges uno (**Editar**), prevalece tu elección. Si no, tu familia y amigos, así como los familiares o amigos tuyos (una esposa, un padre), son Personal, sea cual sea la dirección desde la que escriban. Tu equipo nunca ve los contactos personales.

## Añadir a alguien

**Nueva persona** en la parte superior de Personas, o **+** en la barra superior desde el móvil. Añade un nombre y, si los tienes, un correo y una organización. Si ya hay alguien parecido en tu Graph, el formulario te lo muestra primero para que puedas abrir esa ficha en su lugar. **Añadir** abre la página nueva.

La persona que añadas se queda, aunque todavía no haya mensajes. Su primer mensaje se unirá a su ficha.

## Editar a alguien

**Editar**, en la parte superior de su página, permite cambiar su nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, su relación contigo y si es Trabajo o Personal. El campo **Notas** sirve para apuntar lo que quieras recordar; las notas se conservan al fusionar fichas. **Guardar** conserva los cambios y **Cancelar** los descarta.

Tus cambios se conservan aunque se vuelvan a consultar sus datos, y también después de **Fusionar** y **Deshacer**. Borra un campo para volver a usar el valor consultado. Si borras el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella: **Subir una imagen**, elige una de las fotos que se hayan encontrado o **Quitar imagen**. Se queda en tu Machine.

## Fusionar dos personas

Si dos personas podrían ser la misma, sus páginas preguntan si lo son y Personas las muestra en **¿Misma persona?**. **Fusionar** las une con todos sus mensajes, notas, roles y proyectos. **No es la misma** las mantiene separadas definitivamente. Tu respuesta aparece un momento en el par y luego desaparece de la lista. La lista desaparece cuando ya no queda nada que preguntar.

Una persona con una dirección que solo se parece a otra que conoces, como acme-corp.example y acmecorp.example, nunca se ofrece como la misma persona. Solo tú puedes asignarle un rol.

Un nombre por sí solo nunca basta para unir a alguien de otro dominio, porque cualquiera puede escribirlo: dos direcciones de dominios distintos solo se ofrecen cuando hay otro vínculo, como las mismas personas o un proyecto. Nunca se ofrece a alguien que use tu nombre en una dirección que no sea tuya. Añade tus otras direcciones en Ajustes, [Tus direcciones](settings.md#your-addresses).

Si solo coincide el nombre de pila en dominios distintos, como «Sam» y «Sam Lee», solo se ofrecen si tienen el mismo número de teléfono o perfil de LinkedIn.

Si solo coincide el nombre de pila con el de una reunión creada desde un chat, o si la dirección pertenece a alguien que ya conocías y solo esa persona dice en el chat que es suya, se te pregunta. The Machine nunca abre un enlace para averiguarlo.

Una dirección compartida, como info@ o una lista de correo, nunca se une a las personas que escriben a través de ella. Un contacto de trabajo de fuera de tu empresa y un chat personal que solo comparten un nombre no se unen automáticamente: aparecen como una pregunta.

**Fusionar todo** une de una vez todos los pares de la lista, salvo los que marcaste como **No es la misma**. Si usas **Deshacer** justo después, se separan todos de nuevo.

Para unir dos personas tú mismo, abre una de sus páginas y elige **⋯**, **Misma persona que…** y la otra persona. En la página de la persona fusionada se indica el motivo en **Fusionada desde**, con **Deshacer** para volver a separarlas.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯ y elige **Eliminar para siempre…**; después, **Eliminar**. Se eliminarán la persona y todo lo que tu Machine sabe de ella: su ficha, direcciones, datos consultados, los mensajes que solo intercambiasteis entre los dos y las notas sobre ella.

Las tareas en las que aparece se conservan, pero se quita su nombre. No se volverá a añadir, tampoco mediante una importación ni una tarea de cumpleaños de Facebook con su nombre o dirección. No se puede deshacer.

## Correo rechazado

Cuando se rechaza un correo enviado a alguien, su dirección aparece como **Rebotado**, con la fecha, y otra de sus direcciones pasa a ocupar el primer lugar. Si se conoce otra dirección, los borradores nuevos nunca se envían a la que ha rebotado. Si es la única, la pantalla de envío te avisa, pero puedes enviar el correo igualmente.

Se considera que un correo ha rebotado cuando el servidor de correo indica que la dirección no existe o tras 3 errores temporales en una semana. El aviso desaparece cuando esa persona vuelve a escribir desde esa dirección o cuando se envía un correo a ella correctamente.

## Cargo y foto

Las personas con una dirección de empresa tienen un cargo, una foto, LinkedIn y una ciudad, que se consultan igual que los [datos de la organización](organization-data.md). En una Machine alojada, la consulta solo obtiene su nombre y el dominio de su empresa. Para buscar una foto, Gravatar recibe un hash de su dirección de trabajo, nunca la dirección en sí. Desactiva esta función en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Ese ajuste también impide que se consulte el sitio web antes de una primera reunión y que se haga una búsqueda web cuando esté configurada (consulta [Preparación para tus reuniones](calendar.md#ready-for-your-meetings)).

Si la consulta encuentra información, su página también muestra su descripción, desde cuándo tiene su cargo actual y los dos cargos anteriores. La preparación también usa esos datos, pero solo muestra la descripción si la persona no tiene una propia.

Tus conexiones se completan con información que ya se ha consultado: un cargo, teléfono y zona horaria de Slack; una descripción y ubicación de X; un titular y una foto de LinkedIn; cargos de Contactos de Google y Salesflare; y la foto de un contacto de Salesflare, si Salesflare tiene una. Pasa el cursor por encima de la línea bajo su nombre para ver de dónde procede la información.

Outlook añade las fotos de los compañeros de tu organización y de tus contactos de Outlook, además de los cargos y las empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram se obtienen mediante la sincronización de WhatsApp y la conexión con tus chats de Telegram: hasta 50 al día de cada servicio, solo para personas que ya estén en tu Graph. No se les envía nada. Al importar cumpleaños de Facebook, se añade la foto de perfil de las personas que no tengan foto cuando guardes la importación ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Graph del equipo](team-graph.md) de un Fleet de trabajo, se incluye una copia pequeña de la foto de trabajo en el registro compartido de la persona. Nunca se incluyen fotos de Contactos de Google, WhatsApp, Telegram o Facebook, ni fotos que hayas cambiado o quitado.

## Sobre ti

Tus direcciones y números, también los alias, siempre son tuyos, nunca de alguien de tu Graph. Si te buscas o añades a alguien con una de tus direcciones, se abre **Sobre ti**, y la importación omite tu propia fila.

Sobre ti muestra tus direcciones y de dónde procede cada una. Cámbialas en **Ajustes**, en Cuenta. Para enviar tu propio contacto a un compañero o amigo, elige **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Los roles que tu Machine detecta en tus mensajes aparecen en la página de la persona, en **Para ti**, con las palabras que indican el rol, como un cargo. Que alguien diga que es tu contable o cliente no basta: también hace falta información de tu parte, como tus propios mensajes o reuniones con esa persona. No espera a que confirmes nada. ¿Hay un error? **Editar** en su página permite corregirlo, o puedes usar **⋯** en la línea correspondiente de **Cambios recientes**. Aprende de tus cambios.

## Lo que sabe de alguien

Los datos sobre esa persona aparecen en su página, en **Datos conocidos**; los más generales están en Aprendizaje. **Añadir** guarda otro dato con tus propias palabras. Cada dato tiene un menú:

- **Editar** permite cambiarlo ahí mismo.
- **No es sobre** esa persona lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, desplegado justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido sobre ellos: un rol, dónde trabaja alguien, la relación entre dos personas, un dato o un cambio de proyecto. Cada línea incluye la fecha y el origen; toca el origen para leer el mensaje.

Si una línea es incorrecta, puedes corregirla desde su menú **⋯**: **Editar**, **Quitar**, **No es sobre** esa persona o **Deshacer** para devolver un proyecto a su estado anterior. Se muestran tres líneas; **Mostrar más** enseña el resto.

Si tu Machine ha actualizado a alguien hoy, aparece un punto junto a su nombre en la lista de Personas, y el mensaje **4 personas actualizadas hoy** en la parte superior de la lista indica quiénes son. Consulta [Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea** en el menú **⋯** de una persona, organización o proyecto crea una tarea sobre esa persona.
