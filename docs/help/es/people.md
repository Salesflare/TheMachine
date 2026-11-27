---
title: Personas
area: graph
summary: Todas las personas con las que tienes contacto: su página, resumen y cronología, y cómo añadir, editar, fusionar o eliminar a alguien.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 315403ed8889dbac
---
Todas las personas con las que tienes contacto, empezando por las más cercanas, a partir de tus mensajes y reuniones. Los boletines, recibos y otros envíos no añaden a nadie hasta que respondes. Aparecen en Remitentes ocultos, debajo de la lista: **Mostrar como persona** añade a alguien. Los campos, las etiquetas y la importación funcionan igual en las tres listas, y cada una tiene sus propios filtros: consulta [Graph](graph.md).

Una bandeja de entrada compartida (info@, atención al cliente, el nombre de una tienda) cuenta para su organización, no como persona, incluso después de que escribas a esa dirección.

## Página de una persona

Empieza con su foto, nombre, cargo, organización y ubicación, y una línea sobre cómo os relacionáis ("Habláis a diario · último contacto ayer · próxima reunión mar., 27 de oct."). El contacto reciente aparece como «ahora mismo», «hace 3 horas», «ayer» o «hace 3 días», y los contactos más antiguos, con una fecha. Pasa el cursor por encima para ver la fecha exacta. Debajo:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar**lo. También aparece su **Cumpleaños**, junto con su procedencia (Contactos de Google, Google Calendar, Facebook, tus notas o tú): consulta [Graph](graph.md#birthday).
- **Contigo**: qué relación tiene contigo, si es un contacto de Trabajo o Personal y si forma parte de tu familia o de tu Fleet, con **Ver en Fleet**.
- **También en**: los otros sitios donde hablas con esa persona. **Slack** la abre en Slack o muestra el chat más reciente que tienes con ella en Slack.
- Las **Personas** y los **Proyectos** de los que forma parte, **Pendiente entre ambos** (promesas en ambos sentidos, con **Marcar como hecho** y **Descartar**) y su **Cronología**.

Las direcciones y los chats de una persona se unen automáticamente cuando está claro que pertenecen a la misma persona, por ejemplo, un correo del trabajo con su dirección personal en copia. También se unen si alguien con quien chateas reserva una llamada desde el enlace que le enviaste allí y coincide su empresa o apellido.

Si aparece el mensaje **No se ha podido cargar esta página.**, toca **Reintentar**. Si sigue apareciendo, usa **¿Algo va mal?** al final de la página.

## Resumen

Unas pocas líneas al principio de la página de una persona: lo que se decidió, pidió, planeó o prometió, con los nombres de todos. The Machine lo reescribe cuando hay novedades, solo para las personas con las que tienes contacto de verdad, y revisa cada línea antes. Normalmente, una vez al día; en unas horas si cambia algo relacionado con esa persona, como una nueva fecha límite o una petición que se retira.

Si una línea es vaga, se omite. Si no hay nada concreto que decir, no aparece ningún resumen. Cada línea enlaza con su origen: los mensajes de un mismo día comparten una fecha con el número de mensajes y se abren juntos.

**Editar** el resumen para expresarlo a tu manera. Cuando hay novedades, The Machine muestra una **Actualización sugerida** con las opciones **Usarla** y **Mantener la mía**. **Que lo escriba The Machine** vuelve a dejarlo en sus manos.

La preparación de reuniones lo usa, pero solo las líneas del ámbito de esa tarea (Trabajo o Personal). Se queda en tu Machine; tu equipo nunca la ve.

## Cronología

Todas las páginas de personas y organizaciones tienen una, ordenada de lo más reciente a lo más antiguo: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y cambios en proyectos. Las fichas de arriba muestran una fuente cada vez. **Mostrar más** carga las anteriores.

Las próximas reuniones aparecen arriba, en **Lo próximo**, empezando por la más cercana. **Mostrar todos los próximos** muestra las demás. En cada reunión aparecen sus asistentes, una vez por persona. Si tiene notas o una transcripción, aparece **Notas** o **Transcripción**. Haz clic para leerlas.

Tus cronologías son privadas: el Graph del equipo solo muestra lo que permiten tus reglas para compartir. En una página, **Equipo**, encima de la cronología, añade lo que hayan compartido tus compañeros, indicando quién lo compartió en cada elemento. **Míos** muestra solo lo tuyo.

## Trabajo y Personal

Las pestañas **Trabajo** y **Personal** muestran las personas según su tipo, que aparece en su página. Prevalece el tipo que hayas elegido (**Editar**). Si no has elegido ninguno, tu familia y amigos, y las personas que son familia o amigas tuyas (tu mujer, tu padre), son contactos personales, escriban desde la dirección que escriban. Tu equipo nunca ve los contactos personales.

## Añadir a alguien

Toca **Nueva persona** en la parte superior de Personas o **+** en la barra superior del móvil. Añade un nombre y, si los tienes, un correo y una organización. Si ya hay alguien parecido en tu Graph, el formulario te lo muestra primero para que puedas abrir esa página. **Añadir** abre la página nueva.

La persona que añadas se queda, aunque todavía no haya mensajes. Su primer mensaje se asociará a ella.

## Editar a alguien

**Editar**, en la parte superior de su página, permite cambiar su nombre, cargo, organización, ubicación, perfil de LinkedIn, teléfonos y correos, qué relación tiene contigo y si es de Trabajo o Personal. El campo **Notas** sirve para apuntar lo que quieras recordar. Las notas se conservan al fusionar personas. **Guardar** guarda los cambios; **Cancelar** los descarta.

Tus cambios se conservan aunque se vuelvan a consultar sus datos, y también al usar **Fusionar** y **Deshacer**. Vacía un campo para volver a usar el valor consultado. Si vacías el nombre, se recupera el que aparece en sus mensajes.

Para cambiar su foto, haz clic en ella: **Subir una imagen**, elige una de las que se hayan encontrado para esa persona o **Quitar imagen**. La foto se queda en tu Machine.

## Fusionar a dos personas

Cuando dos personas podrían ser la misma, su página pregunta si lo son y Personas las muestra en **¿Misma persona?**. **Fusionar** las une con todos sus mensajes, notas, roles y proyectos. **No es la misma** las mantiene separadas definitivamente. Tu respuesta aparece un momento en la pareja y después la pareja desaparece de la lista. La lista desaparece cuando ya no queda nada que preguntar.

Nunca se propone como la misma persona a alguien con una dirección que solo se parece a una que conoces, como acme-corp.example y acmecorp.example. Además, solo tú puedes asignarle un rol.

Un nombre por sí solo nunca basta para unir a personas de dos dominios, porque cualquiera puede escribirlo. Solo se propone unir dos direcciones de dominios distintos cuando hay algo más que las relaciona, como las mismas personas o un proyecto pequeño. Si solo coincide el nombre de pila («Sam» y «Sam Lee»), hace falta algo más: la misma empresa, el mismo teléfono o el mismo perfil de LinkedIn.

Nunca se propone a alguien que use tu nombre en una dirección que no es tuya. Añade tus otras direcciones en Ajustes, [Tus direcciones](settings.md#your-addresses).

Si solo coincide el nombre de pila en dominios distintos, como «Sam» y «Sam Lee», solo se propone unirlos si tienen el mismo teléfono o perfil de LinkedIn.

Si solo coincide el nombre de pila con el de una reunión creada desde un chat, o si la dirección pertenece a alguien que ya conocías y solo la persona del chat dice que es suya, se te pregunta. The Machine nunca abre un enlace para averiguarlo.

Una dirección compartida, como info@ o una lista de correo, nunca se une a las personas que escriben a través de ella. Un contacto de trabajo de fuera de tu empresa y un chat personal que solo tienen un nombre en común no se unen automáticamente: aparecen como una pregunta.

**Fusionar todo** une de una vez todas las parejas de la lista, excepto las que marcaste como **No es la misma**. Si usas **Deshacer** justo después, las vuelve a separar.

Para unir tú mismo a dos personas, abre una de ellas y selecciona **⋯**, **Misma persona que…** y la otra persona. La página de una persona fusionada muestra el motivo en **Fusionada a partir de**, con **Deshacer** para volver a separarlas.

## Eliminar a alguien para siempre

En su página, abre el menú ⋯ y selecciona **Eliminar para siempre…**. Después, toca **Eliminar**. Se elimina a esa persona y todo lo que tu Machine sabe sobre ella: su ficha, direcciones, datos consultados, los mensajes que solo intercambiaron entre vosotros y las notas sobre ella.

Las tareas en las que participe se mantienen, pero se quita su nombre. No volverá a añadirse, tampoco mediante una importación ni una tarea de cumpleaños de Facebook con su nombre o dirección. Esta acción no se puede deshacer.

## Correo rechazado

Cuando se rechaza un correo enviado a alguien, su dirección aparece como **Rechazado**, con la fecha, y se muestra primero otra dirección suya. Si se conoce otra dirección, los borradores nuevos nunca se envían a la rechazada. Si es la única, la pantalla de envío te avisa, pero puedes enviar el correo.

Se considera que un correo se ha rechazado cuando el servidor de correo indica que la dirección no existe o después de 3 errores temporales en una semana. El aviso desaparece cuando esa persona vuelve a escribir desde esa dirección o cuando se envía correctamente un correo a ella.

## Cargo y foto

Las personas con una dirección de empresa tienen un cargo, una foto, un perfil de LinkedIn y una ciudad, consultados como los [datos de la organización](organization-data.md). En una Machine alojada, la consulta solo recibe su nombre y el dominio de la empresa. Para buscar una foto, Gravatar recibe un hash de su dirección del trabajo, nunca la dirección en sí. Desactiva esta opción en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Esta opción también impide leer la web antes de una primera reunión y hacer una búsqueda web cuando está configurada (consulta [Preparación para tus reuniones](calendar.md#ready-for-your-meetings)).

Si encuentra datos, su página también muestra su descripción, desde cuándo ocupa su puesto actual y los dos puestos anteriores. La preparación también los consulta, pero solo usa la descripción si la persona no tiene una biografía propia.

Tus contactos se completan con la información que ya han consultado: cargo, teléfono y zona horaria de Slack; biografía y ubicación de X; titular y foto de LinkedIn; cargos de Contactos de Google y Salesflare; y la foto de un contacto de Salesflare, si el propio servicio la guarda. Pasa el cursor por encima de la línea debajo de su nombre para ver de dónde viene la información.

Outlook añade las fotos de tus compañeros de la organización y de tus contactos de Outlook, además de los cargos y las empresas de tus contactos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Las fotos de WhatsApp y Telegram se obtienen mediante la sincronización de WhatsApp y la conexión con tus chats de Telegram: hasta 50 al día de cada servicio, solo de personas que ya estén en tu Graph. No se les envía nada. Si importas cumpleaños de Facebook, se añade la foto de perfil de una persona que no tenga foto cuando la guardas ([Rutinas](routines.md)). Todo se queda en tu Machine.

En el [Graph del equipo](team-graph.md) de un Fleet de trabajo, se comparte una copia pequeña de la foto de trabajo junto con la ficha de una persona. Nunca se comparten las fotos de Contactos de Google, WhatsApp, Telegram o Facebook, ni las fotos que hayas cambiado o quitado.

## Sobre ti

Tus propias direcciones y números, incluidos tus alias, siempre son tuyos, nunca de alguien de tu Graph. Si te buscas o añades a alguien con una de tus direcciones, se abre **Sobre ti**. Al importar, se omite tu propia fila.

Sobre ti muestra tus direcciones y de dónde viene cada una. Cámbialas en **Ajustes**, en Cuenta. Para enviar tu contacto a un compañero o amigo, selecciona **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Qué relación tiene contigo

Los roles que tu Machine detecta en tus mensajes aparecen en la página de esa persona, en **Para ti**, junto con las palabras que indican el rol, como un cargo. Que alguien diga que es tu contable o cliente no basta: también hace falta algo por tu parte, como tus mensajes o reuniones con esa persona. No espera a que lo confirmes. ¿Está mal? **Editar** en su página lo corrige. También puedes tocar **⋯** en la línea correspondiente de **Cambios recientes**. Aprende de tus cambios.

## Lo que sabe sobre alguien

Los datos sobre esa persona aparecen en su página, en **Datos conocidos**. En Aprendizaje se guardan los datos generales. **Añadir** permite guardar otro dato con tus propias palabras. Cada dato tiene un menú:

- **Editar** permite cambiarlo ahí mismo.
- **No es sobre esta persona** lo convierte de nuevo en un dato general, en **Aprendizaje**, **Datos**.
- **Quitar** lo elimina de todas partes.

## Cambios recientes

**Cambios recientes**, desplegado justo encima de la cronología de una persona, organización o proyecto, muestra lo que tu Machine ha cambiado o aprendido sobre ellos: un rol, dónde trabaja alguien, la relación entre dos personas, un dato o un cambio de proyecto. Cada línea tiene una fecha y una fuente. Toca la fuente para leer el mensaje.

Si una línea es incorrecta, puedes corregirla desde **⋯**: **Editar**, **Quitar**, **No es sobre esta persona** o **Deshacer** para devolver un proyecto a su estado anterior. Se muestran tres líneas; **Mostrar más** muestra el resto.

Si tu Machine ha actualizado a alguien hoy, aparece un punto junto a su nombre en la lista Personas, y **4 personas actualizadas hoy** encima de la lista indica quiénes son. Consulta [Graph](graph.md).

## Una tarea sobre alguien

**Nueva tarea** en el menú **⋯** de una persona, organización o proyecto crea una tarea sobre esa persona.
