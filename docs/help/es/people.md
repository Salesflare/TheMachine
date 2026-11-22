---
title: Personas
area: graph
summary: Todas las personas con las que estás en contacto: su página, resumen y cronología, y cómo añadir, editar, fusionar o eliminar a alguien.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e808343918f7f47
---
Todas las personas con las que estás en contacto, empezando por las más cercanas, a partir de tus mensajes y reuniones. Los boletines, recibos y otros envíos no añaden a nadie hasta que respondes. Aparecen en Remitentes ocultos, debajo de la lista: **Mostrar como persona** añade a alguien. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada una tiene sus propios filtros: consulta [Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre de una tienda) cuenta para su organización, no como una persona, incluso después de que le escribas.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea sobre cómo estáis en contacto ("Habláis a diario · último contacto ayer · próxima reunión mar., 27 oct."). El contacto reciente aparece como «ahora mismo», «hace 3 horas», «ayer» o «hace 3 días», y el contacto más antiguo, como una fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo encontrarás:

- **Contacto**: sus teléfonos y correos electrónicos. Toca uno para llamar o escribir, o **Copiar** para copiarlo. Aquí también aparece su **Cumpleaños**, junto con la fuente (Contactos de Google, Google Calendar, Facebook, tus notas o tú): consulta [Graph](graph.md#birthday).
- **Contigo**: qué relación tiene contigo, si es un contacto de Trabajo o Personal y si pertenece a tu familia o a tu Fleet, con la opción **Ver en Fleet**.
- **También en**: los otros lugares donde habláis. **Slack** abre su perfil en Slack o el chat más reciente que tienes con esa persona en Slack.
- **Personas** y **Proyectos** de los que forma parte, **Pendiente entre ambos** (promesas en ambos sentidos, con las opciones **Marcar como hecha** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se unen automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, si un correo del trabajo incluye en CC su dirección personal.

Si una página muestra **No se pudo cargar esta página.**, toca **Reintentar**. Si el mensaje sigue apareciendo, usa **¿Algo va mal?** al final de la página.

## Resumen

Unas pocas líneas al principio de la página de una persona: qué se decidió, pidió, planeó o prometió, con los nombres de todos los involucrados. The Machine lo reescribe cuando hay novedades, solo para las personas con las que realmente estás en contacto, y comprueba cada línea antes de mostrarla. Normalmente, una vez al día; en unas horas si cambia algo relacionado con esa persona, como un nuevo plazo o una solicitud que se retira.

Si una línea es imprecisa, se omite. Si no hay nada concreto que decir, no aparece ningún resumen. Cada línea enlaza con su fuente: los mensajes de un mismo día comparten una fecha y muestran su cantidad, y se abren juntos.

**Editar** te permite expresarlo a tu manera. Cuando hay novedades, The Machine muestra una **Actualización sugerida** con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** vuelve a dejarlo en sus manos.

La preparación de reuniones también usa el resumen, pero solo las líneas correspondientes al tipo de tarea, Trabajo o Personal. Se queda en tu Machine; tu equipo nunca lo ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de más reciente a más antigua: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y cambios de proyectos. Los filtros de arriba muestran una fuente cada vez. **Mostrar más** carga los elementos anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, ordenadas de la más cercana a la más lejana. **Mostrar todos los próximos** muestra las demás. En cada reunión aparecen las personas que asistieron, una vez cada una. Las reuniones con notas o transcripción indican **Notas** o **Transcripción**. Haz clic para leerlas.

Tus cronologías son privadas: el Graph del equipo solo muestra lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la Cronología, añade lo que han compartido tus compañeros; cada elemento indica quién lo compartió. **Míos** muestra solo lo tuyo.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran a las personas según su tipo, que aparece en su página. Si eliges uno (**Editar**), prevalece tu selección. Si no, tu familia y amigos, y quienes son familia o amigos para ti (tu esposa, tu padre), son contactos personales, sea cual sea la dirección desde la que escriban. Tu equipo nunca ve los contactos personales.

## Añadir a alguien

Pulsa **Nueva persona** en la parte superior de Personas, o **+** en la barra superior del teléfono. Añade un nombre y, si los tienes, un correo y una organización. Si ya hay alguien parecido en tu Graph, el formulario lo muestra primero para que puedas abrir esa ficha. **Añadir** abre la página nueva.

La persona que añadas se queda, aunque todavía no haya mensajes. Su primer mensaje se asociará a su ficha.

## Editar a alguien

**Editar**, en la parte superior de su página, te permite cambiar su nombre, cargo, organización, ubicación, perfil de LinkedIn, teléfonos y correos electrónicos, la relación que tiene contigo y si es de Trabajo o Personal. El campo **Notas** sirve para apuntar lo que quieras recordar; las notas se conservan al fusionar fichas. **Guardar** conserva los cambios y **Cancelar** los descarta.

Tus cambios se conservan aunque se vuelvan a buscar sus datos, y también al usar **Fusionar** y **Deshacer**. Vacía un campo para volver a usar el valor encontrado. Si borras el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella: **Subir una imagen**, elige una de las fotos encontradas o **Quitar imagen**. La foto se queda en tu Machine.

## Fusionar a dos personas

Si dos fichas podrían ser de la misma persona, su página te pregunta si se trata de la misma persona, y Personas las muestra en **¿Misma persona?**. **Fusionar** las une con todos sus mensajes, notas, roles y proyectos. **No es la misma** las mantiene separadas definitivamente. Tu respuesta aparece un momento en el par y luego este desaparece de la lista. La lista desaparece cuando ya no queda nada por preguntar.

Nunca se sugiere que una persona con una dirección que solo se parece a otra que conoces, como acme-corp.example y acmecorp.example, sea la misma. Además, solo tú puedes asignarle un rol.

Un nombre por sí solo nunca basta para relacionar a dos personas de dominios distintos, porque cualquiera puede escribirlo. Solo se sugiere unir dos direcciones de dominios distintos si hay algún otro vínculo, como las mismas personas o un proyecto. Nunca se sugiere que una persona que usa tu nombre en una dirección que no es tuya sea la misma que tú. Añade tus otras direcciones en Ajustes, [Tus direcciones](settings.md#your-addresses).

Si solo coincide el nombre de pila en dominios distintos, como «Sam» y «Sam Lee», solo se sugiere que sean la misma persona si tienen el mismo número de teléfono o perfil de LinkedIn.

Nunca se une una dirección compartida, como info@ o una lista de correo, a las personas que escriben a través de ella. Un contacto del trabajo ajeno a tu empresa y un chat personal que solo tienen un nombre en común no se unen automáticamente: aparecen como una pregunta.

**Fusionar todo** une todos los pares de la lista a la vez, excepto los que marcaste como **No es la misma**. Si usas **Deshacer** justo después, los separas de nuevo.

Para unir a dos personas por tu cuenta, abre una de sus páginas y elige **⋯**, **Misma persona que…** y la otra persona. La página de la persona fusionada indica el motivo en **Unido a partir de**, con **Deshacer** para volver a separar las fichas.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯ y elige **Eliminar para siempre…** y, después, **Eliminar**. Se eliminarán la persona y todo lo que tu Machine sabe de ella: su ficha, direcciones, datos encontrados, los mensajes que solo os habéis intercambiado entre vosotros dos y las notas sobre esa persona.

Las tareas que la incluyen se conservan, pero se elimina su nombre. No se volverá a añadir, tampoco mediante una importación o una tarea de cumpleaños de Facebook con su nombre o dirección. Esta acción no se puede deshacer.

## Correo devuelto

Si un correo que envías a alguien se devuelve, su dirección muestra **Rebotó el** y la fecha, y se muestra primero otra de sus direcciones. Si se conoce otra dirección, los borradores nuevos no se envían a la que se devolvió. Si es la única que tiene, la pantalla de envío te avisa, pero aún puedes enviar el mensaje.

Un correo cuenta como devuelto cuando el servidor de correo indica que la dirección no existe, o después de 3 errores temporales en una semana. El aviso desaparece cuando esa persona vuelve a escribir desde esa dirección o cuando se envía correctamente un correo a ella.

## Cargo y foto

Las personas con una dirección de empresa tienen un cargo, una foto, un perfil de LinkedIn y una ciudad, que se buscan como se explica en [datos de organizaciones](organization-data.md). En una Machine alojada, la búsqueda solo recibe su nombre y el dominio de la empresa. Para obtener una foto, Gravatar recibe un hash de su dirección de trabajo, nunca la dirección en sí. Puedes desactivar esta opción en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Este ajuste también desactiva la búsqueda breve en la web antes de una primera reunión (consulta [Prepárate para tus reuniones](calendar.md#ready-for-your-meetings)).

Cuando la búsqueda encuentra información, su página también muestra su descripción, desde cuándo ocupa su cargo actual y sus dos cargos anteriores. La preparación también los consulta, pero solo usa la descripción si la persona no tiene una biografía propia.

Tus contactos se completan con información que ya han leído: un cargo, teléfono y zona horaria de Slack; una biografía y ubicación de X; un titular y una foto de LinkedIn; cargos de Contactos de Google y Salesflare; y la foto de un contacto de Salesflare, si la guarda allí. Pasa el cursor por encima de la línea bajo su nombre para ver de dónde procede la información.

Outlook añade las fotos de los compañeros de tu organización y de tus contactos de Outlook, además de los cargos y empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram llegan a través de la sincronización de WhatsApp y la conexión de chats de Telegram: hasta 50 al día de cada servicio, solo para personas que ya están en tu Graph. No se les envía nada. Una importación de cumpleaños de Facebook añade la foto de perfil de una persona que no tenga foto cuando la guardas ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Graph del equipo](team-graph.md) de un Fleet de trabajo, se incluye una copia pequeña de la foto de trabajo en el registro compartido de una persona. Nunca se incluyen fotos de Contactos de Google, WhatsApp, Telegram o Facebook, ni las fotos que hayas cambiado o quitado.

## Sobre ti

Tus propias direcciones y números, incluidos los alias, siempre son tuyos, nunca de alguien de tu Graph. Si te buscas o añades a alguien con una de tus direcciones, se abre **Sobre ti**. Las importaciones omiten tus propios datos.

Sobre ti muestra tus direcciones y de dónde viene cada una. Puedes cambiarlas en **Ajustes**, en Cuenta. Para enviar tu propio contacto a un compañero o amigo, elige **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Los roles que tu Machine detecta en tus mensajes aparecen en la página de esa persona, en **Para ti**, junto con las palabras que indican el rol, como un cargo. Que alguien diga que es tu contable o cliente no basta: también tiene que haber algo por tu parte, como tus propios mensajes o reuniones con esa persona. No se espera a que lo confirmes. ¿No es correcto? **Editar** en su página lo corrige, o puedes usar **⋯** en la línea correspondiente de **Cambios recientes**. Aprende de tus cambios.

## Lo que sabe sobre alguien

Los datos sobre una persona aparecen en su página, en **Lo que se sabe de** esa persona. Aprendizaje conserva los datos generales. **Añadir** permite guardar otro dato con tus propias palabras. Cada dato tiene un menú:

- **Editar** lo cambia ahí mismo.
- **No trata de** esa persona: lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, plegado justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido sobre esa persona, organización o proyecto: un rol, dónde trabaja alguien, la relación entre dos personas, un dato o un cambio de proyecto. Cada línea muestra la fecha y la fuente. Toca la fuente para leer el mensaje.

Si una línea es incorrecta, usa **⋯** para corregirla ahí mismo: **Editar**, **Quitar**, **No trata de** esa persona o **Deshacer** para devolver un proyecto a su ubicación anterior. Se muestran tres líneas; **Mostrar más** muestra el resto.

Una persona cuya información haya actualizado tu Machine hoy tiene un punto pequeño en la lista de Personas, y **4 personas actualizadas hoy** aparece en la parte superior de la lista con sus nombres. Consulta [Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea** en el menú **⋯** de una persona, organización o proyecto inicia una tarea sobre esa persona, organización o proyecto.
