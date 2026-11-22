---
title: Graph
area: graph
summary: Las personas, organizaciones y proyectos de tus mensajes, siempre actualizados automáticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 181ff5fa2a9d8f47
---
Tu Machine crea un mapa de las personas con las que tienes contacto y de lo que ocurre, a partir de tus mensajes, reuniones y decisiones. No tienes que configurar nada y todo se queda en tu Machine.

- [Personas](people.md): todas las personas con las que tienes contacto, con un resumen y una cronología de cada una.
- [Organizaciones](organizations.md): las empresas en las que trabajan, con sus personas y proyectos.
- [Proyectos](projects.md): lo que ocurre en tableros con fases, como las oportunidades de un CRM.

Tus cambios aparecen al instante. Los nuevos contactos, los mensajes nuevos en sus cronologías y los datos consultados aparecen en un plazo de 30 minutos.

## Actualizado hoy

En la parte superior de cada lista, una línea discreta indica qué ha actualizado hoy tu Machine, como **Hoy se han actualizado 4 personas**. Púlsala para ver quién y qué ha cambiado. Al abrir un nombre, se muestra su página con **Cambios recientes** abierto. Un punto pequeño marca cada fila y tarjeta del tablero que haya cambiado hoy. Solo cuenta los cambios hechos por tu Machine desde medianoche.

## Filtrar y ordenar

**Filtrar**, junto a las pestañas, limita los resultados de la lista. Cada lista tiene sus propios filtros. Personas: cercanía, último contacto, organización, propietario, etiqueta y **Tiene un proyecto abierto**. Organizaciones: sector, especialidad, tamaño, país, último contacto, propietario, etiqueta y **Tiene un proyecto abierto**. Proyectos: propietario, tablero, fase, etiqueta, organización, valor, fecha de cierre prevista y **Sin respuesta en más de 10 días**.

Los filtros que hayas elegido aparecen encima de la lista, junto con **Borrar**. En Proyectos, la lista y el tablero comparten el mismo filtro. En el móvil, los filtros se abren en un panel.

El menú de ordenación permite ordenar la lista. Personas y Organizaciones se pueden ordenar por cercanía, contacto más reciente o más antiguo y nombre. Organizaciones también se pueden ordenar por tamaño. Proyectos se pueden ordenar por última actividad, nombre, fase, **Valor** y **Fecha de cierre**. **Descargar CSV**, debajo del menú de ordenación, guarda la pestaña que estás viendo como una hoja de cálculo.

## Campos y etiquetas

En Campos, dentro de una persona, organización o proyecto, haz clic en un valor para cambiarlo. **Guardar** o Intro guarda el cambio; **Cancelar** o Esc lo descarta; **Quitar** vacía el campo.

**Gestionar campos** (**Añadir un campo** si todavía no hay ninguno) añade o quita campos de todos los registros de ese tipo. **Nuevo campo** añade un campo de texto, número, fecha o selección de una lista.

**+ Etiqueta** añade una etiqueta, como VIP o socio; **×** la quita. Las etiquetas aparecen en las listas. En el móvil, las etiquetas de una persona aparecen en su página. **Filtrar** permite buscarlas.

## Cumpleaños

El cumpleaños de una persona aparece en Contacto, junto con su procedencia: su contacto de Google, un cumpleaños de Google Calendar (la rutina Cumpleaños lo guarda para los contactos cercanos), una importación de Facebook, tus notas o tú. **Editar** permite añadirlo o corregirlo: el mes y el día, y el año si lo sabes. Si añades el año, también aparece su edad.

El dato que añadas tú prevalece sobre todas las fuentes y se conserva. **Quitar** lo elimina; ni un contacto ni una importación lo vuelven a añadir.

Si no hay ninguno, puedes añadirlo con **Añadir cumpleaños**, en Campos. La rutina Cumpleaños lee el mismo cumpleaños que aparece en la página. El cumpleaños es un dato personal: nunca se comparte con tu equipo, ni siquiera en un registro compartido.

## Importar una hoja de cálculo

**Importar CSV…**, debajo del menú de ordenación de Personas, Organizaciones o Proyectos, añade una hoja de cálculo guardada como CSV.

1. Revisa las columnas. Tu Machine intenta identificarlas a partir de los encabezados y su contenido. Puedes cambiar cualquiera. Cuando el modelo esté disponible, también las revisará e indicará brevemente si no está seguro. Solo verá los encabezados, algunos valores de cada columna y las celdas que las reglas no hayan podido leer.
2. Revisa las correcciones. **Revisar** las muestra con el antes y el después: espacios de más, nombres en mayúsculas, números de teléfono con formato internacional, errores en correos (gmial.com), sitios web convertidos a su dominio, fechas y valores con cualquier formato ("€12k" equivale a 12000), varias etiquetas en una celda, una fase escrita de otra forma y filas duplicadas. Desmarca un tipo o una fila para dejarlo sin cambios.
3. Revisa la vista previa. Cada fila se indica como nueva, coincidente con una que ya está en tu Graph o descartada, con el motivo. Una persona coincide por correo (o, si no lo hay, por nombre y organización); una organización, por sitio web o nombre; y un proyecto, por nombre.
4. **Importar** añade los registros nuevos y completa los que coinciden. Las celdas vacías no cambian nada.

Puedes **Deshacer** justo después o usar **Deshacer la última importación**, debajo del menú de ordenación, siempre que esos registros no hayan cambiado desde entonces. Si la acción sobrescribiría una corrección posterior, se indica el motivo. El archivo se queda en tu Machine.

## Propietario

En un Fleet de trabajo, cada persona, organización y proyecto tiene un propietario, indicado como **Propietario** en «Contigo», en su página. Eres tú, a menos que elijas a alguien de tu Fleet de trabajo. **Propietario**, en Filtrar, muestra solo tus registros. Cada cambio aparece en su cronología.

## Equipo

**Equipo**, junto a Mío, muestra lo que comparten tus compañeros, con las mismas pestañas y el mismo menú de ordenación. **Filtrar** permite limitar los resultados por quién lo ha compartido, por organización (Personas) o por estado (Proyectos). Lo que añadas ahí será tuyo.

El trabajo con clientes se comparte con la Machine de cada compañero de equipo, junto con su propietario, campos y etiquetas. Lo que compartan ellos aparece en tu Machine. Cada conversación indica si es **Equipo** o **Solo tú**. Consulta [Graph del equipo](team-graph.md).
