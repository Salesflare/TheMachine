---
title: El Graph
area: graph
summary: Las personas, organizaciones y proyectos de tus mensajes, siempre al día solos.
covers: tab:people
code: graph.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, enrichment.py, dashboard.html
order: 1
---
Tu Machine construye un mapa de con quién tratas y de qué está pasando, a partir de tus mensajes, reuniones y decisiones. No hay nada que configurar, y se queda en tu Machine.

## Personas

Todas las personas con las que tienes contacto, las más cercanas primero. La página de una persona empieza con su foto, nombre, cargo, organización y lugar, y una línea sobre cómo estáis en contacto ("Habláis a diario · último vie, 23 oct · próxima reunión mar, 27 oct"). Debajo:

- **Contacto**: sus teléfonos y correos. Toca uno para llamar o escribir, o **Copiar**.
- **Contigo**: qué es para ti, contacto de Trabajo o Personal, y tu Family o Fleet, con **Ver en Fleet**.
- **También en**: los otros sitios donde habláis. **Slack** abre a la persona en Slack, o tu hilo de Slack más reciente con ella.
- Las **Personas** y los **Proyectos** de los que forma parte, **Pendiente entre ambos** (promesas en los dos sentidos, con **Hecho** y **Descartar**), y su **Cronología**.

Las direcciones y chats de alguien se unen solos cuando está claro que son una sola persona, como un correo de trabajo con su propia dirección en CC.

Las pestañas **Trabajo** y **Personal** solo listan esos contactos. **Descargar CSV**, en el menú de orden, guarda la pestaña en la que estás como hoja de cálculo, también para Organizaciones y Proyectos.

### Cronología

Cada página de persona y de organización tiene una, lo más reciente primero: correos, reuniones y sus resúmenes de Zoom, conversaciones de Intercom (abiertas o cerradas, con **Abrir en Intercom**), chats de WhatsApp, Telegram, Slack, LinkedIn y X, tareas, promesas y movimientos de proyectos. Las etiquetas de arriba muestran una fuente cada vez. **Mostrar más** carga las más antiguas.

Las reuniones que aún no han llegado quedan aparte arriba, en **Lo próximo**, la más cercana primero; **Mostrar todos los próximos** muestra el resto. Una reunión que está en más de uno de tus calendarios aparece una vez.

La cronología de una organización tiene los mensajes de su gente y las conversaciones de Intercom de su dominio. Tus cronologías son tuyas: el Graph del equipo solo muestra lo que permiten tus reglas para compartir.

Si una página dice **No se pudo cargar esta página.**, toca **Reintentar**. Si lo sigue diciendo, usa **¿Algo va mal?** al pie de la página.

## Filtra y ordena

**Filtrar**, junto a las pestañas de Personas, Organizaciones y Proyectos, acota la lista por propietario, etiqueta, tablero, etapa, organización, valor, fecha de cierre prevista y **Sin respuesta en más de 10 días**. Las personas y organizaciones coinciden a través de sus proyectos abiertos. En Proyectos, la lista y el tablero comparten un solo filtro.

Los filtros que elegiste aparecen encima de la lista, con **Borrar**. El menú de orden también ordena por **Valor** y **Fecha de cierre**. El filtrado lo hace tu Machine, así que las listas largas siguen siendo rápidas. En un teléfono, los filtros se abren como una hoja.

## Equipo

**Equipo**, junto a Míos, muestra lo que comparten tus compañeros. Tiene las mismas pestañas, el mismo menú de orden y **Nueva persona** o **Nueva organización** como Míos; lo que añades es tuyo. **Filtrar** lo acota por quién lo compartió, una organización (Personas) o un estado (Proyectos). En Proyectos, **Míos**, **Me toca** y **Todo** eligen los mismos proyectos que en un tablero compartido.

## Propietario

En un Work Fleet, cada persona, organización y proyecto tiene un propietario: **Propietario**, en Contigo, en su página. Eres tú, a menos que elijas a alguien de tu Work Fleet. **Propietario** en Filtrar solo muestra los tuyos, en la lista y en el tablero. Una tarjeta de tablero muestra el nombre de su propietario. Cada cambio aparece en su cronología. Un registro compartido con tu equipo lleva consigo su propietario, con las mismas reglas para compartir que el resto.

## Campos y etiquetas

En Campos de una persona, organización o proyecto, haz clic en un valor para cambiarlo: **Guardar** o Enter lo guarda, **Cancelar** o Escape lo deja, **Quitar** lo vacía. **Gestionar campos** añade o quita campos: **Nuevo campo** añade uno para todos los de ese tipo: texto, número, fecha o una opción de una lista. **Quitar** elimina un campo para todos.

**+ Etiqueta** añade una etiqueta, como VIP o partner; **×** la quita. Las etiquetas aparecen en las listas y **Filtrar** las encuentra. Un registro compartido con tu equipo lleva consigo sus campos y etiquetas.

## Importa una hoja de cálculo

**Importar CSV…**, en el menú de orden de Personas, Organizaciones o Proyectos, añade una hoja de cálculo guardada como CSV. Tu Machine adivina qué columna es cuál a partir de los encabezados y de lo que contienen; cambia la que quieras.

Cuando tu modelo puede funcionar, también revisa las columnas, en cualquier idioma y se escriban como se escriban los encabezados, con un breve motivo cuando no está segura. Solo ve los encabezados, algunos valores por columna y las celdas que las reglas no pudieron leer, en tu Machine como una revisión. Sin él, se queda la suposición a partir de los encabezados.

**Revisar**, junto a las correcciones sugeridas, lista las correcciones sencillas como antes y después: espacios de más, nombres en mayúsculas, números de teléfono en formato internacional, erratas en correos (gmial.com), sitios web como su dominio, fechas y valores en cualquier formato ("€12k" es 12000), varias etiquetas en una celda, una etapa escrita distinta que en el tablero, y la misma fila dos veces.

Desmarca un tipo o una sola fila para dejarla como está. No se corrige nada que no esté marcado.

La vista previa muestra cada fila como nueva, como coincidencia con una que ya está en tu Graph, o como omitida, con el motivo. Una coincidencia es el mismo correo para una persona (si no, el mismo nombre en la misma organización), el mismo sitio web o nombre para una organización, y el mismo nombre para un proyecto.

**Importar** añade las nuevas y completa las coincidencias; una celda vacía no cambia nada. **Deshacer** justo después, o **Deshacer la última importación** en el menú de orden, revierte la última importación mientras esos registros no hayan cambiado desde entonces. Las correcciones posteriores se conservan: si Deshacer fuera a sobrescribir una, explica por qué en su lugar. El archivo se queda en tu Machine.

## Una organización, varios sitios web

**⋯**, **Misma organización que…** en la página de una organización la hace parte de otra, con su gente, proyectos y notas. **Añadir un sitio web…** añade otro de sus sitios web, como su .io junto a su .com: las personas con una dirección ahí se unen a ella, y sus datos se buscan para cada sitio web.

Aparecen en **Sitios web**, cada uno con **Separar** para deshacerlo. Los cambios posteriores en la organización combinada se conservan. Las organizaciones que parecen duplicadas aparecen en **¿Misma organización?**: **Fusionar** o **No es la misma**.

## Añade a alguien o una organización

**Nueva persona** arriba en Personas, **Nueva organización** arriba en Organizaciones, o, en un teléfono, **+** en la barra superior. Indica un nombre y, para una persona, un correo y una organización si los tienes; para una organización, su sitio web. Cuando ya hay algo parecido en tu Graph, el formulario lo muestra primero, para que puedas abrir ese. **Añadir** abre la página nueva.

Alguien que añades se queda, aunque aún no haya mensajes. Su primer mensaje se une a esa persona. Una organización que añadiste se puede eliminar desde su menú **⋯** mientras no haya nadie en ella.

## Sobre ti

Tus propias direcciones y números, también los alias, siempre son tú, nunca alguien de tu Graph. Buscarte a ti, o añadir una persona con una de tus direcciones, abre **Sobre ti**, y una importación se salta tu propia fila.

Sobre ti lista tus direcciones con de dónde salió cada una; cámbialas en **Ajustes**, en Cuenta. Una persona creada antes a partir de tu propia dirección pasa sola a Sobre ti, con una copia de seguridad guardada en tu Machine.

Para enviar tu propia tarjeta a un compañero o amigo, elige **Compartir mi contacto**. Consulta [Compartir un contacto](share-contact.md).

## Foto

Haz clic en la foto de la página de una persona u organización para cambiarla: **Subir una imagen**, elige una encontrada para ella, o **Quitar imagen**. Se queda en tu Machine.

## Notas

**Editar** en la página de una persona u organización tiene un campo **Notas**, para lo que quieras recordar. Las notas aparecen en la página y se mantienen al fusionar.

## Edita a alguien

**Editar**, arriba en su página, cambia su nombre, cargo, organización, ubicación, LinkedIn, teléfonos y correos, qué es para ti, y Trabajo o Personal. **Guardar** lo guarda, **Cancelar** lo deja como estaba.

Tus cambios se quedan, también cuando sus datos se vuelven a buscar o una revisión lee otra cosa, y al usar **Fusionar** y **Deshacer**. Vacía un campo para volver a usar el valor buscado. Un nombre vacío recupera el de sus mensajes.

## ¿Misma persona?

Cuando dos personas podrían ser una, su página pregunta si son la misma persona, y Personas las lista en **¿Misma persona?**. **Fusionar** las une, con todos sus mensajes, notas, cargos y proyectos. **No es la misma** las mantiene separadas para siempre.

**Fusionar todo** fusiona a la vez cada pareja de la lista, salvo las que marcaste como **No es la misma**. **Deshacer** justo después las vuelve a separar todas.

La página de una persona unida lista el motivo en **Unida a partir de**. **Deshacer** las vuelve a separar.

Para unir tú a dos personas, abre una de ellas, luego **⋯**, **Misma persona que…** y elige la otra.

## Cargo y foto

Las personas con una dirección de empresa reciben un cargo, una foto, LinkedIn y una ciudad, buscados como los [datos de la organización](organization-data.md). En una Machine alojada solo se envían su nombre y el dominio de su empresa. Desactívalo en **Ajustes**, en Seguridad: **Buscar contactos de trabajo**.

Tus conexiones completan más datos mientras funcionan, con lo que ya leen y sin pedir nada extra: un cargo, teléfono y zona horaria de Slack, una biografía, lugar y sitio web de X, un titular y una foto de LinkedIn, y cargos de los contactos de Google y de Salesflare. Lo que alguien dice de sí mismo va primero. Pasa el cursor por la línea bajo su nombre para ver de dónde salió. Todo se queda en tu Machine.

Las fotos de WhatsApp llegan a través de tu sincronización de WhatsApp siempre activa, cuando lo permite: hasta 50 al día, solo para personas que ya están en tu Graph. No se les envía nada.

## Elimina a alguien para siempre

En su página, abre el menú ⋯ y elige **Eliminar para siempre…**, y luego **Eliminar**. Quita a esa persona y lo que tu Machine sabe de ella: su entrada, direcciones, datos buscados, los mensajes solo entre vosotros dos y las notas sobre ella. Las tareas en las que participa se quedan, sin su nombre. No se volverá a añadir. No se puede deshacer.

## Quién es quién

Cargos que tu Machine leyó en tus mensajes, esperando tu palabra. **✓ Correcto** confirma uno; **Editar** abre su página en modo edición. Aprende de tus cambios. Solo aparece cuando hay cargos esperando.

## En un Work Fleet

El trabajo con clientes se comparte con las Machines de tus compañeros, y el suyo aparece en la tuya. Cada hilo muestra **Equipo** o **Solo tú**. Consulta [Graph del equipo](team-graph.md).

## Organizaciones

Empresas, a partir de las direcciones y nombres de tus mensajes. Consulta [Datos de la organización](organization-data.md).

La página de una organización está hecha como la de una persona: su logo, nombre y a qué se dedica, una línea sobre cómo estáis en contacto, y luego **Contacto** (su sitio web y LinkedIn), **Contigo** (qué es para ti), las personas que hay ahí y su **Cronología**.

Su lista de **Proyectos** muestra primero los abiertos, cada uno con su etapa. Sus movimientos aparecen en su cronología. **Editar** arriba cambia sus datos y qué es para ti. **Preguntar al Fleet quién la conoce** encuentra una forma de llegar a ella a través de tu Fleet.

El correo de herramientas de calentamiento de correo se deja fuera, en "Oculto como calentamiento", con **Deshacer** por dominio.

## Proyectos

Tu Machine les pone nombre según de qué tratan tus mensajes. Las señales que parecen formar parte aparecen como "probablemente forma parte". Cambiar el nombre de un proyecto al de otro proyecto une los dos.

O gestiónalos a mano, como las oportunidades en un CRM:

- **Nuevo proyecto**: arriba en un tablero, **+ Añadir** bajo una etapa, **Nuevo proyecto** arriba en la lista, **+** en la barra superior en un teléfono, o desde la página de una persona u organización. Ponle un nombre, un tablero y una etapa, una organización (busca en tu Graph, o **Añadir** una nueva), un valor, una fecha de cierre prevista, personas y notas. Los proyectos que ya están en tu Graph con un nombre parecido aparecen primero.
- **Editar** en la página de un proyecto, o **Editar** en el **⋯** de una tarjeta del tablero (o pulsa E en una tarjeta). Cambia todo lo anterior.
- **Ganado** o **Perdido**, con el motivo. Ganado lo mueve a la última etapa del tablero; Perdido, a Estancado o rechazado. **Reabrir** lo deshace.
- **Archivar** lo quita del tablero y de las listas; un mensaje nuevo sobre él lo trae de vuelta. **Eliminar** lo quita para siempre; sus mensajes y personas se quedan.
- Mueve una tarjeta arrastrándola, o con **⋯**, **Mover a** en un teléfono. Tu movimiento se mantiene hasta que un mensaje más reciente lo mueva.
- **Etapas**, arriba en un tablero, muestra solo las etapas que elijas, por tablero. **Borrar** las vuelve a mostrar todas.
- "4 sin respuesta en más de 10 días" bajo una etapa: tócalo para ver solo esos, en el tablero y en la lista. Tócalo otra vez para verlos todos.

### Las tareas de un proyecto

Una tarea puede pertenecer a un proyecto. Tu Machine lo elige cuando su hilo o las personas de las que trata están en un único proyecto abierto, y la tarea muestra su nombre bajo el título. **Cambiar proyecto** en **Más** de la tarea, o **Asignar a un proyecto** en el menú de comandos (Ctrl K), lo cambia o lo quita. Tu elección se queda.

La página de un proyecto lista sus tareas en **Tareas**, las abiertas primero, y su tarjeta en el tablero dice cuántas hay abiertas. Vincular una tarea a un proyecto compartido no comparte nada más: tu equipo sigue viendo solo lo que salió de mensajes compartidos.

### La organización de un proyecto

Cada proyecto se puede vincular a una organización. Su página, su fila y su tarjeta en el tablero la muestran, y enlazan a ella.

Cuando nadie eligió una, tu Machine la fija a partir de las personas del proyecto y de sus mensajes, dejando fuera a tus compañeros. Solo lo hace cuando una organización es claramente la otra parte: el correo personal como Gmail nunca cuenta, y un proyecto con varias empresas se queda sin ninguna. El formulario del proyecto dice entonces "Según su gente".

Tu elección en **Editar** siempre se queda, también cuando la quitas. **Misma organización que…** lleva consigo los proyectos de una organización, y **Separar** los devuelve.

### Tableros

Proyectos de un mismo tipo por etapas, como un pipeline de evaluación. **⋯** en un tablero: **Editar tablero** (nombre, etapas, qué proyectos pertenecen), **Abrir en este tablero** y **Nuevo tablero**. Las revisiones siguen añadiendo proyectos que encajan y los colocan en una etapa. Cuando no están seguras, el tablero muestra "2 proyectos podrían ir aquí": **Añadir** u **Omitir**.

Marca unos cuantos, o **Seleccionar todo**, para hacerlos a la vez, y **Deshacer** justo después si cambias de idea. Un proyecto que agrupa varias contrapartes se convierte en un proyecto por contraparte cuando lo añades.

**Pipeline**, arriba en un tablero, suma el valor de sus proyectos abiertos por etapa, y lo que se espera cerrar cada mes según sus fechas de cierre. Los proyectos ganados, perdidos y estancados no están abiertos; lo que ganaste este mes aparece aparte. Los valores están en euros, salvo que tu Machine tenga configurada otra moneda. Con **Propietario** en Filtrar, solo cuenta los tuyos.

Un tablero nuevo, o un tablero sugerido que guardas, revisa una vez todo tu historial. Encuentra proyectos y organizaciones que encajan, crea un proyecto por organización y coloca cada uno en una etapa. La cabecera dice "Revisando tu historial…" mientras trabaja, y luego cuántos añadió y cuántos esperan tu revisión. Un tablero de Solo tú guarda solo para ti lo que encuentra.

### El tablero de un compañero

En **Equipo**, los tableros que comparten tus compañeros aparecen junto a los tuyos, primero los que tienen más proyectos tuyos. Cada tarjeta dice qué pasó por última vez, con su fecha, como en el tablero de su propietario: la línea más reciente compartida con el equipo, o si no su último movimiento. El nombre del propietario solo aparece cuando una etapa tiene tarjetas de más de un compañero; cuando una persona es dueña de todo el tablero, lo dice la cabecera.

**Míos**, **Me toca** y **Todo** eligen qué muestra un tablero compartido, y también la lista de proyectos del equipo. Míos es en lo que estás: un hilo suyo, un proyecto del que eres propietario o que tienes tú, o una tarea tuya sobre él. Me toca es lo que te espera: una tarea abierta sobre él, o un hilo en el que el mensaje más reciente se te escribió a ti.

El resto de una etapa se pliega en **Mostrar N más**. Los proyectos que se parecen, como una serie de pruebas "… CRM evaluation", se pliegan en una fila con un recuento; tócala para abrirlos. Nada de esto cambia lo que se comparte.

## Una tarea sobre alguien

**Nueva tarea** en el menú **⋯** de una persona, organización o proyecto empieza una tarea sobre ella.

## Lo que sabe de alguien

En Lo que se sabe, cada dato tiene un menú:

- **Olvidar** lo elimina en todas partes.
- No es sobre esta persona solo lo quita de esa página.
