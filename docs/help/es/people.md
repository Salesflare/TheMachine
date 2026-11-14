---
title: Personas
area: graph
summary: Todas las personas con las que estás en contacto: su página, resumen y cronología, y cómo añadir, editar, fusionar o eliminar a alguien.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 26845dd199228f90
---
Todas las personas con las que estás en contacto, empezando por las más cercanas, a partir de tus mensajes y reuniones. Los boletines, recibos y otros envíos no añaden a nadie hasta que respondes. Aparecen en Remitentes ocultos, debajo de la lista: Mostrar como persona añade a alguien. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada lista tiene sus propios filtros: consulta [The Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre de una tienda) se cuenta para su organización, no como una persona, incluso después de que le escribas.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea sobre cómo estáis en contacto ("Habláis a diario · último contacto ayer · próxima reunión el martes, 27 de octubre"). El contacto reciente aparece como "justo ahora", "hace 3 horas", "ayer" o "hace 3 días"; el contacto más antiguo aparece como una fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar** para copiarlo. También aparece su **Cumpleaños**, con la fuente de la información (contactos de Google, Google Calendar, Facebook, tus notas o tú): consulta [The Graph](graph.md#birthday).
- **Contigo**: qué relación tienes con esa persona, si es un contacto de trabajo o personal y si pertenece a tu familia o Fleet, con la opción **Ver en Fleet**.
- **También en**: los otros lugares donde habláis. **Slack** abre su perfil en Slack o el hilo más reciente que tengas con esa persona.
- **Personas** y **Proyectos** de los que forma parte, **Pendiente entre ambos** (promesas en ambos sentidos, con **Marcar como hecha** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se vinculan automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, cuando su correo de trabajo aparece con su dirección personal en copia.

Si aparece **No se pudo cargar esta página.**, toca **Reintentar**. Si sigue apareciendo, usa **¿Algo va mal?** al final de la página.

## Resumen

Unas pocas líneas al principio de la página de una persona: lo que se decidió, pidió, planeó o prometió, con los nombres de todos. The Machine lo vuelve a redactar cuando hay novedades, solo para personas con las que realmente estás en contacto, y revisa cada línea antes. Por lo general, una vez al día; en unas horas si cambia algo relacionado con esa persona, como una nueva fecha límite o una solicitud que se retira.

Si una línea es vaga, se omite; si no hay nada concreto que decir, no aparece ningún resumen. Cada línea enlaza con su fuente: los mensajes del mismo día comparten una fecha con el número de mensajes y se abren juntos.

Usa **Editar** para expresarlo a tu manera. Cuando hay novedades, The Machine muestra una **Actualización sugerida** con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** le devuelve la tarea.

La preparación de reuniones también usa el resumen, pero solo las líneas del ámbito de esa tarea (Trabajo o Personal). Se queda en tu Machine; tu equipo nunca la ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una cronología, ordenada de lo más reciente a lo más antiguo: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y cambios de proyectos. Los filtros de arriba muestran una fuente cada vez. **Mostrar más** carga elementos anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, empezando por la más cercana. **Mostrar todos los próximos** muestra las demás. En cada reunión aparecen las personas que asistieron, una sola vez cada una. Las reuniones con notas o transcripción muestran **Notas** o **Transcripción**; haz clic para leerlas.

Tus cronologías son solo tuyas: el Graph del equipo muestra únicamente lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la cronología, añade lo que han compartido tus compañeros, y cada elemento indica quién lo compartió; **Míos** muestra solo lo tuyo.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran las personas según su tipo, que aparece en su página. Siempre prevalece lo que elijas tú (**Editar**). Si no eliges nada, tu familia y tus amigos, y las personas cuya relación contigo es familiar o de amistad (como tu esposa o tu padre), se consideran personales, sin importar desde qué dirección escriban. Tu equipo nunca ve tus contactos personales.

## Añadir a alguien

Pulsa **Nueva persona** en la parte superior de Personas o **+** en la barra superior del teléfono. Añade un nombre y, si los tienes, un correo y una organización. Si ya hay alguien parecido en tu Graph, el formulario te lo muestra primero para que puedas abrir esa ficha. **Añadir** abre la nueva página.

La persona que añades se queda, aunque todavía no haya mensajes. Su primer mensaje la vincula.

## Editar a alguien

**Editar**, en la parte superior de su página, permite cambiar su nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, qué relación tienes con esa persona y si es de Trabajo o Personal. El campo **Notas** sirve para apuntar lo que quieras recordar; las notas se conservan al fusionar personas. **Guardar** conserva los cambios; **Cancelar** los descarta.

Tus cambios se conservan aunque se vuelva a buscar información sobre esa persona, y también al usar **Fusionar** y **Deshacer**. Borra un campo para volver a usar el valor encontrado. Si borras el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella: **Subir una imagen**, elige una de las imágenes encontradas para esa persona o **Quitar imagen**. La foto se queda en tu Machine.

## Fusionar dos personas

Cuando dos personas podrían ser la misma, su página pregunta si son la misma persona y Personas las muestra en **¿Misma persona?**. **Fusionar** las une con todos sus mensajes, notas, roles y proyectos. **No es la misma** las mantiene separadas definitivamente. Tu respuesta aparece un momento en ese par y luego desaparece de la lista. La lista desaparece cuando ya no queda nada por preguntar.

Nunca se sugiere que alguien con una dirección que solo se parece a otra que conoces, como acme-corp.example y acmecorp.example, sea la misma persona. Además, solo tú puedes asignarle un rol.

Una dirección compartida, como info@ o una lista de correo, nunca se vincula a las personas que escriben a través de ella. Un contacto de trabajo ajeno a tu empresa y un chat personal que solo tienen un nombre en común no se vinculan automáticamente: aparecen como una pregunta.

**Fusionar todo** une de una vez todos los pares de la lista, excepto los que marcaste como **No es la misma**. Si pulsas **Deshacer** justo después, los separas de nuevo.

Para unir dos personas por tu cuenta, abre una de sus páginas y elige **⋯**, **Misma persona que…** y la otra persona. En la página de la persona fusionada se muestran los motivos en **Unida desde**, con la opción **Deshacer** para volver a separarlas.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯ y elige **Eliminar para siempre…** y luego **Eliminar**. Se elimina a esa persona y todo lo que tu Machine sabe sobre ella: su ficha, direcciones, datos encontrados, los mensajes que solo habéis intercambiado entre ambos y las notas sobre ella.

Las tareas en las que participa se conservan, pero se quita su nombre. No se volverá a añadir, ni siquiera al importar datos o al crear una tarea de cumpleaños de Facebook con su nombre o dirección. Esta acción no se puede deshacer.

## Correo rechazado

Si se rechaza un correo que envías a alguien, su dirección aparece como **Rechazado**, con la fecha, y otra dirección suya aparece primero. Los borradores nuevos nunca se envían a esa dirección si se conoce otra. Si es la única dirección, la pantalla de envío te avisa, pero puedes enviar el correo.

Una dirección se considera rechazada cuando el servidor de correo indica que no existe o después de 3 errores temporales en una semana. El aviso desaparece cuando esa persona vuelve a escribir desde esa dirección o cuando se consigue enviar un correo a ella.

## Cargo y foto

Las personas con una dirección de empresa tienen un cargo, una foto, LinkedIn y una ciudad, que se buscan como se explica en [los datos de organizaciones](organization-data.md). En una Machine alojada, la búsqueda solo recibe su nombre y el dominio de la empresa. Para la foto, Gravatar recibe un hash de su dirección de trabajo, nunca la dirección en sí. Puedes desactivar esta opción en **Ajustes**, en Seguridad, con **Buscar contactos de trabajo**.

Si se encuentra información sobre esa persona, su página también muestra su descripción, desde cuándo ocupa su cargo actual y los dos cargos anteriores. La preparación también usa esta información; la descripción solo se usa si no tiene una biografía propia.

Tus conexiones se completan con la información que ya han leído: un cargo, teléfono y zona horaria de Slack; una biografía y ubicación de X; un titular y una foto de LinkedIn; cargos de contactos de Google y Salesflare; y la foto de un contacto de Salesflare, si este servicio tiene una. Pasa el cursor por encima de la línea debajo de su nombre para ver de dónde viene la información.

Outlook añade las fotos de los compañeros de tu organización y de tus contactos de Outlook, además de los cargos y las empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram se añaden mediante la sincronización de WhatsApp y la conexión de tus chats de Telegram: hasta 50 al día de cada servicio, solo para personas que ya están en tu Graph. No se les envía nada. Al importar cumpleaños de Facebook se añade la foto de perfil de las personas que no tienen foto cuando guardas la importación ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Graph del equipo](team-graph.md) de una Fleet de trabajo, se comparte una copia pequeña de la foto de trabajo junto con la ficha de la persona. Nunca se comparten las fotos de contactos de Google, WhatsApp, Telegram o Facebook, ni las fotos que hayas cambiado o quitado.

## Sobre ti

Tus propias direcciones y números, incluidos tus alias, siempre son tuyos, nunca de alguien de tu Graph. Si te buscas o añades a alguien con una de tus direcciones, se abre **Sobre ti**. Al importar datos, se omite tu propia fila.

Sobre ti muestra tus direcciones y de dónde viene cada una. Puedes cambiarlas en **Ajustes**, en Cuenta. Para enviar tu contacto a un compañero o amigo, elige **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Los roles que tu Machine detecta en tus mensajes aparecen en su página, en **Para ti**, junto con la línea que leyó. No espera a que los confirmes. ¿Hay algún error? Corrígelo con **Editar** en su página o con **⋯** en la línea correspondiente de **Cambios recientes**. Aprende de tus cambios.

## Qué sabe sobre alguien

Los datos sobre esa persona aparecen en su página, en **Información conocida**. Aprendizaje conserva los datos generales. Usa **Añadir** para guardar otro con tus propias palabras. Cada dato tiene un menú:

- **Editar** permite cambiarlo ahí mismo.
- **No es sobre** esa persona lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, que aparece contraído justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido sobre ese elemento: un rol, dónde trabaja alguien, la relación entre dos personas, un dato o un cambio de proyecto. Cada línea incluye la fecha y la fuente; toca la fuente para leer el mensaje.

Si una línea está mal, usa **⋯** para corregirla ahí mismo: **Editar**, **Quitar**, **No es sobre** esa persona o **Deshacer** para devolver un proyecto a su estado anterior. Se muestran tres líneas; **Mostrar más** enseña las demás.

Las personas cuya información actualizó tu Machine hoy tienen un punto pequeño en la lista de Personas, y **4 personas actualizadas hoy** aparece en la parte superior de la lista con sus nombres. Consulta [The Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea**, en el menú **⋯** de una persona, organización o proyecto, crea una tarea sobre ese elemento.
