---
title: The Graph
area: graph
summary: Las personas, organizaciones y proyectos de tus mensajes, siempre al día por sí solos.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: e437109f98725e65
---
Tu Machine crea un mapa de las personas con las que tratas y de lo que ocurre, a partir de tus mensajes, reuniones y decisiones. No tienes que configurar nada y todo se queda en tu Machine.

- [Personas](people.md): todas las personas con las que estás en contacto, con un resumen y una cronología de cada una.
- [Organizaciones](organizations.md): las empresas donde trabajan, con sus personas y proyectos.
- [Proyectos](projects.md): lo que está pasando, en tableros con etapas, como los acuerdos en un CRM.
- [Notas](notes.md): una página fácil de leer por tema, como un viaje o tu Hogar.

## Actualizado hoy

Una línea discreta en la parte superior de cada lista indica qué actualizó tu Machine hoy, como **4 personas actualizadas hoy**. Tócala para ver quién y qué cambió. Al tocar un nombre, se abre su página con **Cambios recientes** desplegado. Un punto pequeño marca cada fila y tarjeta del tablero que cambió hoy. Solo cuenta los cambios que hizo tu Machine, desde la medianoche.

## Filtrar y ordenar

**Filtrar**, junto a las pestañas, reduce la lista. Cada lista tiene sus propios filtros. Personas: cercanía, último contacto, organización, propietario, etiqueta y **Tiene un proyecto abierto**. Organizaciones: sector, especialidad, tamaño, país, último contacto, propietario, etiqueta y **Tiene un proyecto abierto**. Proyectos: propietario, tablero, etapa, etiqueta, organización, valor, fecha de cierre prevista y **Sin respuesta en más de 10 días**.

Los filtros que elegiste aparecen encima de la lista, junto a **Borrar**. En Proyectos, la lista y el tablero comparten un solo filtro. En el móvil, los filtros se abren en una hoja.

El menú de ordenación permite ordenar la lista. Personas y Organizaciones se ordenan por cercanía, contacto más reciente o más antiguo y nombre. Organizaciones también se pueden ordenar por tamaño. Proyectos se ordenan por última actividad, nombre, etapa, **Valor** y **Fecha de cierre**. **Descargar CSV**, debajo del menú de ordenación, guarda la pestaña que tienes abierta como hoja de cálculo.

## Campos y etiquetas

En Campos, dentro de la página de una persona, organización o proyecto, haz clic en un valor para cambiarlo. **Guardar** o Intro lo guarda; **Cancelar** o Esc lo descarta; **Quitar** lo borra.

**Gestionar campos** (o **Añadir un campo** si todavía no hay ninguno) permite añadir o quitar campos de todos los registros de ese tipo. **Campo nuevo** añade uno: de texto, número, fecha o una opción de una lista.

**+ Etiqueta** añade una etiqueta, como VIP o socio; **×** la quita. Las etiquetas aparecen en las listas y puedes encontrarlas con **Filtrar**.

## Cumpleaños

El cumpleaños de una persona aparece en Contacto, junto con su origen: su contacto de Google, un cumpleaños de Google Calendar (la rutina de cumpleaños lo guarda para un contacto cercano), una importación de Facebook, tus notas o tú. **Editar** permite añadirlo o corregirlo: el mes y el día, y el año si lo sabes. En ese caso, también aparece su edad.

El dato que añadas tú tiene prioridad sobre todas las fuentes y se conserva. **Quitar** lo elimina; el contacto o una importación no lo volverán a añadir.

Si no hay ninguno, **Añadir cumpleaños**, en Campos, permite añadirlo. La rutina de cumpleaños lee el mismo cumpleaños que aparece en la página. El cumpleaños es un dato personal: nunca se comparte con tu equipo, ni siquiera en un registro compartido.

## Importar una hoja de cálculo

**Importar CSV…**, debajo del menú de ordenación de Personas, Organizaciones o Proyectos, permite añadir una hoja de cálculo guardada como CSV.

1. Revisa las columnas. Tu Machine intenta identificarlas por los encabezados y el contenido; puedes cambiar cualquiera de ellas. Cuando tu modelo puede ejecutarse, también las revisa y explica brevemente los casos en los que no está segura. Solo ve los encabezados, algunos valores de cada columna y las celdas que las reglas no pudieron leer.
2. Revisa las correcciones. **Revisar** las muestra como antes y después: espacios de más, nombres en mayúsculas, números de teléfono en formato internacional, errores en direcciones de correo (gmial.com), sitios web convertidos a su dominio, fechas y valores en cualquier formato ("€12k" equivale a 12000), varias etiquetas en una celda, una etapa escrita de otra forma y una fila duplicada. Desmarca un tipo de corrección o una fila para dejarla como está.
3. Revisa la vista previa. Cada fila es nueva, coincide con una que ya está en tu Graph o se omite, con el motivo. Una persona coincide por correo (si no, por nombre y organización), una organización por sitio web o nombre y un proyecto por nombre.
4. **Importar** añade los registros nuevos y completa los que coinciden. Las celdas vacías no cambian nada.

**Deshacer** justo después, o **Deshacer la última importación** debajo del menú de ordenación, revierte la última importación siempre que esos registros no hayan cambiado desde entonces. Si al hacerlo se sobrescribiría una corrección posterior, te explica el motivo. El archivo se queda en tu Machine.

## Propietario

En una Fleet de trabajo, cada persona, organización y proyecto tiene un propietario: **Propietario**, en «Contigo» en su página. Eres tú, a menos que elijas a alguien de tu Fleet de trabajo. **Propietario**, en Filtrar, muestra solo los tuyos. Cada cambio aparece en su cronología.

## Equipo

**Equipo**, junto a «Mío», muestra lo que comparten tus compañeros, con las mismas pestañas y el mismo menú de ordenación. **Filtrar** permite reducir la lista según quién lo haya compartido, una organización (Personas) o el estado (Proyectos). Lo que añadas allí es tuyo.

El trabajo con clientes se comparte con las Machines de tus compañeros, junto con su propietario, campos y etiquetas. Lo que ellos tienen también aparece en la tuya. Cada hilo indica **Equipo** o **Solo tú**. Consulta [Graph del equipo](team-graph.md).
