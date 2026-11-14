---
title: The Graph
area: graph
summary: Las personas, organizaciones y proyectos de tus mensajes, siempre actualizados automáticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
Tu Machine crea un mapa de las personas con las que tratas y de lo que ocurre, a partir de tus mensajes, reuniones y decisiones. No tienes que configurar nada y todo permanece en tu Machine.

- [Personas](people.md): todas las personas con las que estás en contacto, con un resumen y una cronología de cada una.
- [Organizaciones](organizations.md): las empresas en las que trabajan, con sus personas y proyectos.
- [Proyectos](projects.md): lo que está pasando, organizado en tableros con etapas, como los acuerdos en un CRM.

## Actualizado hoy

Una línea discreta en la parte superior de cada lista indica lo que tu Machine ha actualizado hoy, como **4 personas actualizadas hoy**. Tócala para ver quién y qué cambió. Al tocar un nombre, se abre su página con **Cambios recientes** a la vista. Un punto pequeño marca cada fila y tarjeta del tablero que haya cambiado hoy. Solo cuenta los cambios que hizo tu Machine desde la medianoche.

## Filtrar y ordenar

**Filtrar**, junto a las pestañas, reduce la lista. Cada lista tiene sus propios filtros. Personas: cercanía, último contacto, organización, propietario, etiqueta y **Tiene un proyecto abierto**. Organizaciones: sector, especialidad, tamaño, país, último contacto, propietario, etiqueta y **Tiene un proyecto abierto**. Proyectos: propietario, tablero, etapa, etiqueta, organización, valor, fecha de cierre prevista y **Sin respuesta en más de 10 días**.

Los filtros que hayas elegido aparecen encima de la lista, junto a **Borrar**. En Proyectos, la lista y el tablero comparten el mismo filtro. En el teléfono, los filtros se abren en una hoja.

El menú de ordenación permite ordenar la lista. Personas y Organizaciones se pueden ordenar por cercanía, contacto más reciente o más antiguo y nombre. Organizaciones también se pueden ordenar por tamaño. Proyectos se pueden ordenar por última actividad, nombre, etapa, **Valor** y **Fecha de cierre**. **Descargar CSV**, debajo del menú de ordenación, guarda la pestaña que tienes abierta como una hoja de cálculo.

## Campos y etiquetas

En **Campos**, dentro de la página de una persona, organización o proyecto, haz clic en un valor para cambiarlo: **Guardar** o Enter guarda los cambios, **Cancelar** o Escape los descarta y **Quitar** borra el valor.

**Gestionar campos** (o **Añadir un campo** si no hay ninguno) permite añadir o quitar campos de todos los registros de ese tipo. **Nuevo campo** añade un campo de texto, número, fecha o una opción de una lista.

**+ Etiqueta** añade una etiqueta, como VIP o socio; **×** la quita. Las etiquetas aparecen en las listas y puedes encontrarlas con **Filtrar**.

## Cumpleaños

El cumpleaños de una persona aparece en **Contacto**, junto con la fuente: sus contactos de Google, un cumpleaños de Google Calendar (la rutina Cumpleaños lo guarda para los contactos cercanos), una importación de Facebook, tus notas o tú. **Editar** permite añadirlo o corregirlo: el mes y el día, y el año si lo sabes (en ese caso también aparece su edad).

El cumpleaños que añadas tú tiene prioridad sobre cualquier otra fuente y se conserva. **Quitar** lo elimina; ni los contactos ni una importación lo vuelven a añadir.

Si no hay un cumpleaños, **Añadir cumpleaños** en **Campos** permite añadirlo. La rutina Cumpleaños lee el mismo cumpleaños que aparece en la página. El cumpleaños es un dato personal: nunca se comparte con tu equipo, ni siquiera en un registro compartido.

## Importar una hoja de cálculo

**Importar CSV…**, debajo del menú de ordenación de Personas, Organizaciones o Proyectos, permite añadir una hoja de cálculo guardada como CSV.

1. Revisa las columnas. Tu Machine intenta identificarlas según los encabezados y su contenido; puedes cambiar cualquiera. Cuando tu modelo pueda ejecutarse, también las revisará e indicará brevemente qué no tiene claro. Solo ve los encabezados, algunos valores de cada columna y las celdas que no pudo leer según las reglas.
2. Revisa las correcciones. **Revisar** las muestra antes y después: espacios adicionales, nombres en mayúsculas, números de teléfono en formato internacional, errores en direcciones de correo (gmial.com), sitios web reducidos a su dominio, fechas y valores en cualquier formato ("€12k" equivale a 12000), varias etiquetas en una celda, una etapa con una escritura distinta y filas duplicadas. Desmarca un tipo de corrección o una fila para dejarla como está.
3. Revisa la vista previa. Cada fila se marcará como nueva, coincidente con una que ya está en tu Graph o como omitida, con el motivo. Una persona coincide por correo electrónico (o, si no lo hay, por nombre y organización); una organización, por sitio web o nombre; y un proyecto, por nombre.
4. **Importar** añade los registros nuevos y completa los coincidentes. Las celdas vacías no cambian nada.

**Deshacer** justo después de importar, o **Deshacer la última importación** en el menú de ordenación, revierte la última importación siempre que esos registros no hayan cambiado desde entonces. Si al deshacer se sobrescribiría una corrección posterior, te explica el motivo. El archivo permanece en tu Machine.

## Propietario

En una Fleet de trabajo, cada persona, organización y proyecto tiene un propietario: **Propietario**, en **Contigo**, dentro de su página. Eres tú, a menos que elijas a alguien de tu Fleet de trabajo. **Propietario** en Filtrar muestra solo los registros que te pertenecen. Cada cambio aparece en su cronología.

## Equipo

**Equipo**, junto a **Míos**, muestra lo que comparten tus compañeros de equipo, con las mismas pestañas y el mismo menú de ordenación. **Filtrar** permite reducir la lista según quién lo haya compartido, una organización (Personas) o el estado (Proyectos). Lo que añadas ahí será tuyo.

El trabajo con clientes se comparte con las Machines de tus compañeros de equipo, junto con su propietario, campos y etiquetas. Lo que ellos añadan también aparece en la tuya. Cada conversación indica **Equipo** o **Solo tú**. Consulta [Graph del equipo](team-graph.md).
