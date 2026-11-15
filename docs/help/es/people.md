---
title: Personas
area: graph
summary: Todas las personas con las que tienes contacto: su página, resumen y cronología, y cómo añadir, editar, fusionar o eliminar a alguien.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 907cec019dc70184
---
Todas las personas con las que tienes contacto, empezando por las más cercanas, a partir de tus mensajes y reuniones. Los boletines, recibos y otros envíos no añaden a nadie hasta que respondes. Aparecen en **Remitentes ocultos**, debajo de la lista: **Mostrar como persona** añade a alguien. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada lista tiene sus propios filtros: consulta [The Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre de una tienda) se asocia a su organización, no a una persona, incluso después de que le escribas.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea sobre el tipo de contacto que tienen ("Hablan a diario · último contacto ayer · próxima reunión mar., 27 oct."). El contacto reciente se indica como "ahora mismo", "hace 3 horas", "ayer" o "hace 3 días"; los contactos anteriores muestran una fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar**. Aquí también aparece su **Cumpleaños**, junto con la fuente (Contactos de Google, Google Calendar, Facebook, tus notas o tú): consulta [The Graph](graph.md#birthday).
- **Contigo**: qué relación tiene contigo, si es un contacto de Trabajo o Personal, y si forma parte de tu Familia o Fleet, con **Ver en Fleet**.
- **También en**: otros lugares donde hablas con esa persona. **Slack** la abre en Slack o abre el hilo más reciente que tienes con ella en Slack.
- **Personas** y **Proyectos** de los que forma parte, **Pendiente entre ambos** (promesas de ambas partes, con **Marcar como hecha** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se asocian automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, si un correo de trabajo tiene su dirección personal en copia.

Si aparece **No se ha podido cargar esta página.**, toca **Reintentar**. Si sigue apareciendo, usa **¿Algo va mal?** al final de la página.

## Resumen

Unas líneas breves al principio de la página de una persona: qué se decidió, pidió, planeó o prometió, y quién participó. The Machine lo reescribe cuando hay novedades, solo para las personas con las que tienes contacto de verdad, y comprueba cada línea antes de mostrarla. Normalmente, una vez al día; en unas horas si cambia algo relacionado con esa persona, como una nueva fecha límite o una petición retirada.

Si una línea es imprecisa, se omite; si no hay nada concreto que decir, no se muestra ningún resumen. Cada línea enlaza a su fuente: los mensajes de un mismo día comparten una fecha con el número de mensajes y se pueden abrir juntos.

**Editar** te permite expresarlo a tu manera. Cuando hay novedades, The Machine muestra una **Actualización sugerida**, con **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** le devuelve el control.

Las preparaciones de reuniones usan este resumen, solo las líneas del área de esa tarea (Trabajo o Personal). Se queda en tu Machine; tu equipo nunca lo ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de la más reciente a la más antigua: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y cambios en proyectos. Los botones de la parte superior muestran una fuente a la vez. **Mostrar más** carga los anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, empezando por la más cercana; **Mostrar todos los próximos** muestra las demás. En cada reunión aparecen las personas que asistieron, una sola vez cada una. Si tiene notas o una transcripción, aparece **Notas** o **Transcripción**; haz clic para leerlas.

Tus cronologías son tuyas: el Graph del equipo solo muestra lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la Cronología, añade lo que han compartido tus compañeros de equipo, e indica quién compartió cada elemento; **Míos** muestra solo los tuyos.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran las personas según el tipo que aparece en su página. Se prioriza el tipo que elijas (**Editar**). Si no, tu Familia y tus Amigos, y las personas que son familia o amigas tuyas (una esposa, un padre), se consideran Personal, sin importar desde qué dirección escriban. Tu equipo nunca ve los contactos personales.

## Añadir a alguien

Usa **Nueva persona** en la parte superior de Personas o **+** en la barra superior del teléfono. Añade un nombre y, si los tienes, un correo y una organización. Si ya hay alguien parecido en tu Graph, el formulario lo muestra primero para que puedas abrir esa ficha. **Añadir** abre la página nueva.

La persona que añadas se queda, aunque todavía no haya mensajes. Su primer mensaje se asociará con ella.

## Editar a alguien

**Editar**, en la parte superior de su página, te permite cambiar su nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, qué relación tiene contigo y si es de Trabajo o Personal. El campo **Notas** sirve para lo que quieras recordar; las notas se conservan al fusionar personas. **Guardar** aplica los cambios y **Cancelar** los descarta.

Los cambios que hagas se conservan aunque se vuelvan a consultar sus datos, y también al usar **Fusionar** y **Deshacer**. Si vacías un campo, se vuelve a usar el valor consultado. Si borras el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella: **Subir una imagen**, elige una imagen encontrada para esa persona o **Quitar imagen**. Se queda en tu Machine.

## Fusionar dos personas

Si dos personas podrían ser la misma, en su página se pregunta si lo son y Personas las muestra en **¿Misma persona?**. **Fusionar** las une, junto con todos sus mensajes, notas, roles y proyectos. **No es la misma** las mantiene separadas para siempre. Tu respuesta aparece un momento junto a la pareja y después desaparece de la lista. La lista desaparece cuando ya no queda nada que preguntar.

Nunca se propone como la misma persona a alguien cuya dirección solo se parece a una que conoces, como acme-corp.example y acmecorp.example. Además, solo tú puedes asignarle un rol.

Un nombre por sí solo nunca basta para relacionar a alguien entre dos dominios, porque cualquiera puede escribirlo: solo se proponen dos direcciones de dominios distintos si hay algún otro vínculo, como las mismas personas o un proyecto. Nunca se propone a alguien que use tu nombre con una dirección que no sea tuya. Añade tus otras direcciones en Ajustes, [Tus direcciones](settings.md#your-addresses).

Nunca se fusiona una dirección compartida, como info@ o una lista de correo, con las personas que escriben a través de ella. Un contacto de trabajo de fuera de tu empresa y un chat personal que solo comparten un nombre tampoco se fusionan automáticamente: aparecen como una pregunta.

**Fusionar todo** fusiona de una vez todas las parejas de la lista, excepto las que marcaste como **No es la misma**. Si usas **Deshacer** justo después, se separan todas de nuevo.

Para unir a dos personas por tu cuenta, abre una de ellas y luego selecciona **⋯**, **Misma persona que…** y elige la otra. En la página de una persona fusionada, **Fusionada desde** explica el motivo, y **Deshacer** permite volver a separarlas.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯ y elige **Eliminar para siempre…**; después, pulsa **Eliminar**. Se eliminarán esa persona y lo que tu Machine sabe de ella: su ficha, direcciones, datos consultados, los mensajes que solo intercambiaron ustedes dos y las notas sobre ella.

Las tareas en las que participa se conservan, pero se elimina su nombre. No volverá a añadirse, tampoco mediante una importación ni con una tarea de cumpleaños de Facebook que incluya su nombre o dirección. Esta acción no se puede deshacer.

## Correos rechazados

Cuando se rechaza un correo enviado a alguien, su dirección aparece como **Rechazada**, con la fecha, y se muestra primero otra dirección suya. Los borradores nuevos nunca se envían a esa dirección si se conoce otra. Si es la única que tiene, la pantalla de envío te avisa, pero puedes enviar el correo igualmente.

Un rechazo cuenta cuando el servidor de correo indica que la dirección no existe o después de 3 fallos temporales en una semana. Se borra cuando esa persona vuelve a escribir desde esa dirección o cuando se entrega un correo enviado a ella.

## Cargo y foto

Las personas con una dirección de empresa tienen un cargo, una foto, LinkedIn y una ciudad, consultados como los [datos de la organización](organization-data.md). En una Machine alojada, la consulta solo obtiene su nombre y el dominio de la empresa. Para buscar una foto, Gravatar recibe un hash de su dirección de trabajo, nunca la dirección en sí. Puedes desactivarlo en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Cuando la consulta encuentra esos datos, su página también muestra su texto de presentación, desde cuándo ocupa su cargo actual y sus dos cargos anteriores. Las preparaciones también los consultan; el texto de presentación solo se usa si no tiene una biografía propia.

Tus conexiones se completan con datos que ya han leído: un cargo, teléfono y zona horaria de Slack; una biografía y ubicación de X; un titular y una foto de LinkedIn; cargos de Contactos de Google y Salesflare; y la foto de un contacto de Salesflare, si Salesflare la guarda. Pasa el cursor por encima de la línea bajo su nombre para ver de dónde viene.

Outlook añade las fotos de tus compañeros de organización y de tus contactos de Outlook, además de los cargos y las empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram se obtienen mediante la sincronización de WhatsApp y la conexión de chats de Telegram: hasta 50 al día de cada servicio, solo para personas que ya están en tu Graph. No se les envía nada. Una importación de cumpleaños de Facebook añade la foto de perfil de alguien que no tenga foto cuando la guardas ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Team Graph](team-graph.md) de una Fleet de trabajo, se incluye una copia pequeña de la foto de trabajo en el registro compartido de una persona. Nunca se incluyen fotos de Contactos de Google, WhatsApp, Telegram o Facebook, ni fotos que hayas cambiado o quitado.

## Sobre ti

Tus propias direcciones y números, incluidos los alias, siempre son tuyos, nunca de alguien de tu Graph. Si te buscas o añades a alguien con una de tus direcciones, se abre **Sobre ti**, y una importación omite tu propia fila.

Sobre ti muestra tus direcciones y de dónde viene cada una. Puedes cambiarlas en **Ajustes**, en Cuenta. Para enviar tu contacto a un compañero de equipo o amigo, selecciona **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Los roles que tu Machine detecta en tus mensajes aparecen en su página, en **Para ti**, junto con la frase que ha leído. No tienes que esperar a que te pregunte. ¿Hay algún error? **Editar** en su página lo corrige, o puedes usar **⋯** en la línea correspondiente de **Cambios recientes**. Aprende de los cambios que haces.

## Lo que sabe de alguien

Los datos sobre esa persona aparecen en su página, en **Información conocida**; Aprendizaje guarda los datos generales. **Añadir** permite guardar otro dato con tus propias palabras. Cada dato tiene un menú:

- **Editar** permite cambiarlo directamente.
- **No es sobre esta persona** lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, desplegado justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido sobre ellos: un rol, dónde trabaja alguien, cómo se relacionan dos personas, un dato o un cambio de proyecto. Cada línea muestra la fecha y la fuente; toca la fuente para leer el mensaje.

Si una línea es incorrecta, puedes corregirla directamente con **⋯**: **Editar**, **Quitar**, **No es sobre esta persona** o **Deshacer** para devolver un proyecto a su estado anterior. Se muestran tres líneas; **Mostrar más** muestra las demás.

Si tu Machine ha actualizado a alguien hoy, aparece un punto pequeño junto a su nombre en la lista Personas, y **4 personas actualizadas hoy** las menciona al principio de la lista. Consulta [The Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea**, en el menú **⋯** de una persona, organización o proyecto, crea una tarea sobre esa persona, organización o proyecto.
