---
title: Personas
area: graph
summary: Todas las personas con las que estás en contacto: su página, resumen y cronología, y cómo añadir, editar, fusionar o eliminar a alguien.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 2fe1c104a74711c4
---
Todas las personas con las que estás en contacto, empezando por las más cercanas, según tus mensajes y reuniones. Los boletines, recibos y otros correos no añaden a nadie hasta que respondes. Aparecen en Remitentes ocultos, debajo de la lista: **Mostrar como persona** añade a alguien a la lista. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada una tiene sus propios filtros: consulta [The Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre de una tienda) se cuenta como parte de la organización, no como una persona, incluso después de que le escribas.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea que indica cómo estás en contacto con ella ("Habláis a diario · último contacto ayer · próxima reunión mar., 27 de oct."). El contacto reciente aparece como «ahora mismo», «hace 3 horas», «ayer» o «hace 3 días», y el más antiguo, como una fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo aparece lo siguiente:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar**. Aquí también aparece su **Cumpleaños**, junto con el origen (contactos de Google, Google Calendar, Facebook o tú): consulta [The Graph](graph.md#birthday).
- **Contigo**: qué relación tienes con esa persona, si es un contacto de Trabajo o Personal, y tu Familia o Fleet, con **Ver en Fleet**.
- **También en**: los otros lugares donde hablas con esa persona. **Slack** la abre en Slack o abre el hilo más reciente que tengas con ella en Slack.
- Las **Personas** y los **Proyectos** de los que forma parte, **Pendiente entre ambos** (promesas en ambos sentidos, con **Marcar como hecha** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se unen automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, si un correo de trabajo incluye su dirección personal en copia.

Si aparece **No se pudo cargar esta página.**, toca **Reintentar**. Si el mensaje sigue apareciendo, usa **¿Algo va mal?** en la parte inferior de la página.

## Resumen

Unas pocas líneas breves en la parte superior de la página de una persona: lo que se decidió, pidió, planeó o prometió, con los nombres de todas las personas mencionadas. The Machine lo vuelve a redactar cuando hay novedades, solo para las personas con las que estás realmente en contacto, y comprueba cada línea antes de mostrarla. Normalmente lo hace una vez al día; si cambia algo relacionado con esa persona, como una nueva fecha límite o una petición que se retira, lo hace en unas horas.

Si una línea es imprecisa, se omite. Si no hay nada concreto que decir, no hay resumen. Cada línea enlaza al contenido del que procede: los mensajes de un mismo día comparten una fecha con el número de mensajes, y se abren juntos.

Pulsa **Editar** para expresarlo a tu manera. Cuando haya novedades, The Machine mostrará una **Actualización sugerida** con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** le devuelve la tarea.

Los preparativos de reuniones usan este resumen, solo las líneas de la parte de esa tarea que corresponda a Trabajo o Personal. Se queda en tu Machine; tu equipo nunca lo ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de lo más reciente a lo más antiguo: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y cambios en proyectos. Los filtros de la parte superior muestran una fuente a la vez. **Mostrar más** carga elementos anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, ordenadas de la más cercana a la más lejana. **Mostrar todos los próximos** muestra las demás. En una reunión aparece quién participó, cada persona una sola vez. Si tiene notas o una transcripción, aparece **Notas** o **Transcripción**; haz clic para leerlas.

Tus cronologías son tuyas: el Graph del equipo solo muestra lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la Cronología, añade lo que han compartido tus compañeros, y cada elemento indica quién lo compartió; **Míos** muestra solo lo tuyo.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran a las personas según su Tipo, que aparece en su página. Se respeta primero la opción que hayas elegido (**Editar**). Si no has elegido ninguna, tu Familia y tus Amigos, y quienes sean familiares o amigos tuyos (tu esposa, tu padre), se clasifican como Personal, sin importar desde qué dirección escriban. Tu equipo nunca ve tus contactos personales.

## Añadir a alguien

Usa **Nueva persona** en la parte superior de Personas o **+** en la barra superior del teléfono. Añade un nombre y, si los tienes, un correo y una organización. Si alguien parecido ya está en tu Graph, el formulario te lo muestra primero para que puedas abrir esa ficha. **Añadir** abre la nueva página.

La persona que añadas se queda, aunque todavía no haya mensajes. Su primer mensaje se asociará a ella.

## Editar a alguien

**Editar**, en la parte superior de su página, permite cambiar el nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, qué relación tienes con esa persona y si es de Trabajo o Personal. El campo **Notas** sirve para apuntar lo que quieras recordar; las notas se conservan al fusionar personas. **Guardar** guarda los cambios y **Cancelar** los descarta.

Tus cambios se conservan aunque se vuelvan a consultar sus datos, y también después de usar **Fusionar** o **Deshacer**. Vacía un campo para volver a usar el valor encontrado. Si vacías el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella: **Subir una imagen**, elige una de las fotos encontradas para esa persona o **Quitar imagen**. La foto se queda en tu Machine.

## Fusionar a dos personas

Si dos personas podrían ser la misma, en sus páginas se te pregunta si son la misma persona y en Personas aparecen en **¿Misma persona?**. **Fusionar** las une junto con todos sus mensajes, notas, funciones y proyectos. **No es la misma** las mantiene separadas definitivamente. Tu respuesta aparece en la pareja por un momento y luego desaparece de la lista. La lista desaparece cuando ya no queda nada por preguntar.

Una dirección compartida, como info@ o una lista de correo, nunca se une a las personas que escriben a través de ella. Un contacto de trabajo de fuera de tu empresa y un chat personal que solo comparten un nombre no se unen automáticamente: aparecen como una pregunta.

**Fusionar todo** fusiona a la vez todas las parejas de la lista, excepto las que marcaste como **No es la misma**. Si usas **Deshacer** justo después, se separarán todas de nuevo.

Para unir a dos personas por tu cuenta, abre una de ellas y luego el menú **⋯**, elige **Misma persona que…** y selecciona a la otra. En la página de la persona fusionada, **Fusionada desde** indica el motivo y **Deshacer** permite separarlas de nuevo.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯ y elige **Eliminar para siempre…** y luego **Eliminar**. Se eliminará a esa persona y todo lo que tu Machine sabe sobre ella: su ficha, direcciones, datos consultados, mensajes que solo intercambiaron ustedes dos y notas sobre ella.

Las tareas relacionadas con esa persona se conservan, pero se quita su nombre. No se volverá a añadir, ni siquiera mediante una importación o una tarea de cumpleaños de Facebook que tenga su nombre o dirección. Esta acción no se puede deshacer.

## Correo rebotado

Cuando rebota un correo que envías a alguien, su dirección aparece como **Rebotado**, junto con la fecha, y cualquier otra dirección suya aparece primero. Los borradores nuevos nunca se envían a esa dirección si se conoce otra. Si es la única, la pantalla de envío te avisa, pero puedes enviar el correo de todas formas.

Se considera que un correo ha rebotado cuando el servidor de correo indica que la dirección no existe o después de 3 fallos temporales en el transcurso de una semana. El aviso desaparece cuando esa persona vuelve a escribir desde esa dirección o cuando se entrega un correo enviado a ella.

## Cargo y foto

Las personas con una dirección de empresa reciben un cargo, una foto, un perfil de LinkedIn y una ciudad, que se consultan como los [datos de la organización](organization-data.md). En una Machine alojada, la consulta solo recibe su nombre y el dominio de la empresa. Para obtener una foto, Gravatar recibe un hash de su dirección de trabajo, nunca la dirección en sí. Puedes desactivarlo en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Cuando la consulta encuentra información, la página también muestra su descripción, desde cuándo ocupa su cargo actual y sus dos cargos anteriores. Los preparativos también la consultan, pero solo usan la descripción si la persona no tiene una biografía propia.

Tus conexiones se completan con información que ya se ha leído: un cargo, teléfono y zona horaria de Slack; una biografía y ubicación de X; un titular y una foto de LinkedIn; cargos de los contactos de Google y Salesflare; y la foto de un contacto de Salesflare, si la tiene guardada. Pasa el cursor por encima de la línea bajo su nombre para ver de dónde procede la información.

Outlook añade las fotos de los compañeros de tu organización y de tus contactos de Outlook, además de los cargos y las empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram se obtienen mediante la sincronización de WhatsApp y la conexión de chats de Telegram: hasta 50 al día de cada uno, solo de personas que ya estén en tu Graph. No se les envía nada. Una importación de cumpleaños de Facebook añade la foto de perfil de alguien que no tenga foto cuando la guardas ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Graph del equipo](team-graph.md) de una Fleet de Trabajo, se incluye una copia pequeña de la foto de trabajo en el registro compartido de una persona. Nunca se incluyen fotos de contactos de Google, WhatsApp, Telegram o Facebook, ni las fotos que hayas cambiado o quitado.

## Sobre ti

Tus propias direcciones y números, incluidos los alias, siempre son tuyos, nunca de alguien de tu Graph. Si te buscas a ti mismo o añades a una persona con una de tus direcciones, se abre **Sobre ti** y se omite tu propia fila al importar.

Sobre ti muestra tus direcciones y el origen de cada una. Cámbialas en **Ajustes**, en Cuenta. Para enviar tu contacto a un compañero o amigo, elige **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Las funciones que tu Machine detecta en tus mensajes aparecen en su página, en **Para ti**, junto con la frase que detectó. No tienes que esperar a que te pregunte. ¿Está mal? **Editar** en su página lo corrige, o puedes usar **⋯** en la línea correspondiente de **Cambios recientes**. Aprende de tus cambios.

## Lo que sabe de alguien

Los datos sobre esa persona aparecen en su página, en **Datos conocidos**; en Aprendizaje se guardan los datos generales. Usa **Añadir** para guardar otro con tus propias palabras. Cada dato tiene un menú:

- **Editar** permite cambiarlo ahí mismo.
- **No es sobre esta persona** lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, que se despliega justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido sobre ellos: una función, dónde trabajan, la relación entre dos personas, un dato o el cambio de un proyecto. Cada línea incluye la fecha y la fuente; toca la fuente para leer el mensaje.

Si una línea es incorrecta, puedes corregirla ahí mismo con **⋯**: **Editar**, **Quitar**, **No es sobre esta persona** o **Deshacer** para devolver un proyecto a su estado anterior. Se muestran tres líneas; **Mostrar más** muestra el resto.

Si tu Machine ha actualizado a alguien hoy, aparece un punto pequeño en la lista de Personas, y **4 personas actualizadas hoy** en la parte superior de la lista indica quiénes son. Consulta [The Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea** en el menú **⋯** de una persona, organización o proyecto inicia una tarea sobre esa persona, organización o proyecto.
