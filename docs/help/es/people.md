---
title: Personas
area: graph
summary: Todas las personas con las que tienes contacto: su página, resumen y cronología, y cómo añadir, editar, fusionar o eliminar a alguien.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 84312952f04b8597
---
Todas las personas con las que tienes contacto, empezando por las más cercanas, a partir de tus mensajes y reuniones. Los boletines, recibos y otros envíos no añaden a nadie hasta que respondes. Aparecen en Remitentes ocultos, debajo de la lista: **Mostrar como persona** añade a alguien. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada lista tiene sus propios filtros: consulta [Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente o el nombre de una tienda) cuenta para la organización, no como persona, incluso después de que le escribas.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea sobre cómo os mantenéis en contacto ("Habláis a diario · último contacto ayer · próxima reunión mar., 27 oct."). El contacto reciente aparece como «ahora mismo», «hace 3 horas», «ayer» o «hace 3 días», y el contacto más antiguo, como una fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar** para copiarlo. Aquí también aparece su **Cumpleaños**, junto con el origen (contactos de Google, Google Calendar, Facebook, tus notas o tú): consulta [Graph](graph.md#birthday).
- **Contigo**: qué relación tiene contigo, si es un contacto de Trabajo o Personal, y si forma parte de tu familia o de tu Fleet, con **Ver en Fleet**.
- **También en**: los otros sitios donde hablas con esa persona. **Slack** abre su perfil en Slack o el hilo más reciente que tenéis en Slack.
- Las **Personas** y los **Proyectos** de los que forma parte, lo **Pendiente entre ambos** (promesas en ambas direcciones, con **Marcar como hecho** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se unen automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, si un correo de trabajo incluye su dirección personal en copia. También se unen cuando alguien con quien chateas reserva una llamada desde el enlace que le enviaste en el chat y coincide su empresa o apellido.

Si aparece el mensaje **No se ha podido cargar esta página.**, toca **Reintentar**. Si sigue apareciendo, usa **¿Algo va mal?** al final de la página.

## Resumen

Unas pocas líneas al principio de la página de una persona: qué se decidió, pidió, planeó o prometió, y quién participó. The Machine lo vuelve a redactar cuando hay novedades, solo para las personas con las que realmente tienes contacto, y comprueba cada línea antes. Normalmente, una vez al día; en unas horas si cambia algo relacionado con esa persona, como un nuevo plazo o una petición que se retira.

Si una línea es imprecisa, se omite. Si no hay nada concreto que decir, no aparece ningún resumen. Cada línea enlaza con su origen: los mensajes de un mismo día comparten una fecha con su recuento y se abren juntos.

**Editar** el resumen para expresarlo a tu manera. Cuando hay novedades, The Machine muestra una **Actualización sugerida** con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** se lo devuelve.

La preparación de reuniones lo usa, pero solo incluye las líneas de la categoría de esa tarea, Trabajo o Personal. El resumen se queda en tu Machine. Tu equipo nunca lo ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de más reciente a más antigua: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y cambios de proyecto. Los filtros de arriba muestran una fuente cada vez. **Mostrar más** carga elementos anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, empezando por la más cercana. **Mostrar todos los próximos** muestra el resto. En una reunión aparecen sus asistentes, cada persona una sola vez. Si tiene notas o transcripción, aparece **Notas** o **Transcripción**. Haz clic para leerlas.

Tus cronologías son privadas: Graph del equipo solo muestra lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la cronología, añade lo que han compartido tus compañeros y señala quién compartió cada elemento. **Míos** muestra solo los tuyos.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** organizan a las personas según su tipo, que aparece en su página. Se aplica la opción que elijas (**Editar**). Si no eliges ninguna, tu familia y amistades, y las personas que son familia o amistades tuyas (como tu mujer o tu padre), aparecen como Personal, sea cual sea la dirección desde la que escriban. Tu equipo nunca ve los contactos personales.

## Añadir a alguien

Pulsa **Nueva persona** en la parte superior de Personas o **+** en la barra superior del móvil. Añade un nombre y, si los tienes, un correo y una organización. Si ya hay alguien parecido en tu Graph, el formulario lo muestra primero para que puedas abrir esa ficha en su lugar. **Añadir** abre la nueva página.

La persona que añadas se queda, aunque todavía no haya mensajes. Su primer mensaje se vincula a su ficha.

## Editar a alguien

**Editar**, en la parte superior de su página, permite cambiar su nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, la relación que tiene contigo y si es Trabajo o Personal. El campo **Notas** sirve para apuntar lo que quieras recordar. Las notas se conservan al fusionar fichas. **Guardar** aplica los cambios y **Cancelar** los descarta.

Los cambios que hagas se conservan aunque se vuelvan a consultar sus datos, y también al usar **Fusionar** o **Deshacer**. Borra un campo para volver a usar el valor consultado. Si borras el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella y elige **Subir una imagen**, una de las fotos encontradas para esa persona o **Quitar imagen**. La foto se queda en tu Machine.

## Fusionar a dos personas

Si dos fichas podrían ser de la misma persona, aparece una pregunta en su página y Personas las muestra bajo **¿Misma persona?**. **Fusionar** las une con todos sus mensajes, notas, roles y proyectos. **No es la misma** las mantiene separadas. Tu respuesta aparece un momento junto al par, que después desaparece de la lista. La lista desaparece cuando ya no queda nada por preguntar.

Nunca se propone como la misma persona a alguien cuya dirección solo se parece a una que conoces, como acme-corp.example y acmecorp.example. Solo tú puedes asignarle un rol.

Un nombre por sí solo nunca basta para unir a dos personas de dominios distintos, porque cualquiera puede escribirlo. Solo se propone unir dos direcciones de dominios diferentes cuando hay otro vínculo, como las mismas personas o un proyecto pequeño. Si solo coincide el nombre de pila ("Sam" y "Sam Lee"), hace falta algo más: la misma empresa, el mismo teléfono o el mismo perfil de LinkedIn.

Nunca se propone a alguien que usa tu nombre en una dirección que no es tuya. Añade tus otras direcciones en Ajustes, [Tus direcciones](settings.md#your-addresses).

Si solo coincide el nombre de pila en dominios distintos, como "Sam" y "Sam Lee", solo se propone unirlos si tienen el mismo teléfono o perfil de LinkedIn.

Si solo coincide el nombre de pila con el de una reunión creada desde un chat, o si la dirección pertenece a alguien que ya conocías y solo la persona del chat dice que es suya, te lo preguntamos. The Machine nunca abre un enlace para averiguarlo.

Una dirección compartida, como info@ o una lista de correo, nunca se vincula con las personas que escriben a través de ella. Un contacto de trabajo de fuera de tu empresa y un chat personal que solo comparten un nombre tampoco se unen automáticamente: aparecen como una pregunta.

**Fusionar todo** une de una vez todos los pares de la lista, excepto los que marcaste como **No es la misma**. Si pulsas **Deshacer** justo después, los separa a todos de nuevo.

Para unir tú mismo a dos personas, abre una de sus páginas y selecciona **⋯**, **Misma persona que…** y la otra persona. En la página de la persona unida se muestran los motivos en **Unidas desde**, con la opción **Deshacer** para separarlas de nuevo.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯ y selecciona **Eliminar para siempre…**. Después, pulsa **Eliminar**. Se elimina a esa persona y todo lo que tu Machine sabe sobre ella: su ficha, direcciones, datos consultados, mensajes que solo os implican a los dos y notas sobre ella.

Las tareas que la incluyen se conservan, pero se quita su nombre. No se volverá a añadir, tampoco mediante una importación o una tarea de cumpleaños de Facebook con su nombre o dirección. No se puede deshacer.

## Devuelto

Si se devuelve un correo enviado a alguien, su dirección aparece como **Devuelto**, junto con la fecha, y otra de sus direcciones pasa a ocupar el primer lugar. Los borradores nuevos nunca se envían a esa dirección si se conoce otra. Si es la única, la pantalla de envío te avisa, pero puedes enviar el correo igualmente.

Se considera que un correo se ha devuelto cuando el servidor indica que la dirección no existe o tras 3 errores temporales durante una semana. El aviso desaparece cuando la persona vuelve a escribir desde esa dirección o cuando se envía correctamente un correo a ella.

## Cargo y foto

Las personas con una dirección de empresa tienen un cargo, foto, perfil de LinkedIn y ciudad consultados como los [datos de la organización](organization-data.md). En una Machine alojada, la consulta solo obtiene su nombre y el dominio de la empresa. Para buscar una foto, Gravatar recibe un hash de su dirección de trabajo, nunca la dirección en sí. Desactiva esta opción en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Ese ajuste también impide leer el sitio web antes de una primera reunión y hacer búsquedas web (consulta [Lista para tus reuniones](calendar.md#ready-for-your-meetings)).

Cuando se encuentran esos datos, su página también muestra su descripción, desde cuándo ocupa su cargo actual y los dos cargos anteriores. La preparación de reuniones también los consulta. Solo usa la descripción cuando la persona no tiene una biografía propia.

Tus conexiones se completan con la información que ya han consultado: un cargo, teléfono y zona horaria de Slack; una biografía y ubicación de X; un titular y una foto de LinkedIn; cargos de los contactos de Google y Salesflare; y la foto de un contacto de Salesflare, si Salesflare la conserva. Pasa el cursor por la línea debajo de su nombre para ver de dónde procede la información.

Outlook añade las fotos de tus compañeros de organización y de tus contactos de Outlook, además de los cargos y las empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram se obtienen mediante la sincronización de WhatsApp y la conexión con tus chats de Telegram: hasta 50 al día de cada servicio, solo para personas que ya estén en tu Graph. No se les envía nada. Al importar cumpleaños de Facebook, se añade la foto de perfil de quienes no tienen una foto cuando la guardas ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Graph del equipo](team-graph.md) de un Fleet de trabajo, se incluye una copia pequeña de la foto de trabajo en el registro compartido de una persona. Nunca se incluyen fotos de contactos de Google, WhatsApp, Telegram o Facebook, ni fotos que hayas cambiado o quitado.

## Sobre ti

Tus propias direcciones y números, incluidos los alias, siempre son tuyos y nunca corresponden a alguien de tu Graph. Si te buscas o añades a alguien con una de tus direcciones, se abre **Sobre ti**. Las importaciones omiten tu propia fila.

Sobre ti muestra tus direcciones y su origen. Puedes cambiarlas en **Ajustes**, en Cuenta. Para enviar tus datos de contacto a un compañero o amigo, selecciona **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Los roles que tu Machine encuentra en tus mensajes aparecen en la página de esa persona, en **Para ti**, junto con las palabras que indican el rol, como un cargo. Que alguien diga que es tu contable o cliente no basta: también hace falta información de tu parte, como tus propios mensajes o reuniones con esa persona. No espera a que lo confirmes. ¿No es correcto? **Editar** en su página permite corregirlo, o puedes usar **⋯** en la línea correspondiente de **Cambios recientes**. Aprende de los cambios que haces.

## Lo que sabe sobre alguien

Los datos sobre esa persona aparecen en su página, en **Datos conocidos**. Aprendizaje guarda los datos generales. **Añadir** permite guardar otro con tus propias palabras. Cada dato tiene un menú:

- **Editar** permite cambiarlo directamente.
- **No es sobre** esa persona lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, desplegado justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido sobre esa persona: un rol, dónde trabaja, la relación entre dos personas, un dato o un cambio de proyecto. Cada línea indica la fecha y el origen. Toca el origen para leer el mensaje.

Si una línea no es correcta, puedes corregirla directamente con **⋯**: **Editar**, **Quitar**, **No es sobre** esa persona o **Deshacer** para devolver un proyecto a donde estaba. Se muestran tres líneas; **Mostrar más** muestra el resto.

La lista de Personas muestra un punto junto a quien tu Machine haya actualizado hoy, y el texto **4 personas actualizadas hoy** en la parte superior indica quiénes son. Consulta [Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea**, en el menú **⋯** de una persona, organización o proyecto, crea una tarea sobre esa persona.
