---
title: The Graph
area: graph
summary: Las personas, organizaciones y proyectos de tus mensajes, siempre al día por sí solos.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 4dbe1a4e1702b1c1
---
Tu Machine crea un mapa de las personas con las que tratas y de lo que está pasando, a partir de tus mensajes, reuniones y decisiones. No tienes que configurar nada y todo permanece en tu Machine.

- [Personas](people.md): todas las personas con las que estás en contacto, con un resumen y una cronología de cada una.
- [Organizaciones](organizations.md): las empresas donde trabajan, con sus personas y proyectos.
- [Proyectos](projects.md): lo que está pasando, en tableros con etapas, como los acuerdos en un CRM.

## Actualizado hoy

Una línea discreta en la parte superior de cada lista indica qué actualizó hoy tu Machine, como **4 personas actualizadas hoy**. Tócala para ver quién y qué cambió. Al tocar un nombre, se abre su página con **Cambios recientes** desplegado. Un punto pequeño marca cada fila y tarjeta del tablero que haya cambiado hoy. Solo cuenta los cambios que hizo tu Machine, desde la medianoche.

## Filtrar y ordenar

**Filtrar**, junto a las pestañas, permite acotar la lista. Cada lista tiene sus propios filtros. Personas: cercanía, último contacto, organización, propietario, etiqueta y **Tiene un proyecto abierto**. Organizaciones: sector, especialidad, tamaño, país, último contacto, propietario, etiqueta y **Tiene un proyecto abierto**. Proyectos: propietario, tablero, etapa, etiqueta, organización, valor, fecha de cierre prevista y **Sin respuesta en más de 10 días**.

Los filtros que elegiste aparecen sobre la lista, junto a **Borrar**. En Proyectos, la lista y el tablero comparten un mismo filtro. En el teléfono, los filtros se abren en una hoja.

El menú de ordenación sirve para ordenar la lista. Personas y Organizaciones se pueden ordenar por cercanía, contacto más reciente o más antiguo y nombre. Organizaciones también se pueden ordenar por tamaño. Proyectos también se pueden ordenar por **Valor** y **Fecha de cierre**. **Descargar CSV**, debajo del menú de ordenación, guarda la pestaña que tienes abierta como una hoja de cálculo.

## Campos y etiquetas

En Campos, dentro de la ficha de una persona, organización o proyecto, haz clic en un valor para cambiarlo: **Guardar** o Intro lo conserva, **Cancelar** o Escape descarta los cambios y **Quitar** lo deja vacío.

**Gestionar campos** permite añadir o quitar campos de todos los registros de ese tipo. **Campo nuevo** añade un campo: de texto, número, fecha o con opciones de una lista.

**+ Etiqueta** añade una etiqueta, como VIP o partner; **×** la quita. Las etiquetas aparecen en las listas y puedes encontrarlas con **Filtrar**.

## Cumpleaños

El cumpleaños de una persona aparece en Contacto, junto con su origen: sus contactos de Google, un cumpleaños de Google Calendar (la rutina de cumpleaños lo guarda para los contactos cercanos), una importación de Facebook o tú. **Editar** permite añadirlo o corregirlo: el mes y el día, y el año si lo sabes (en ese caso, también aparece su edad). El dato que añadas tú prevalece sobre cualquier otra fuente y se conserva. **Quitar** lo elimina; no vuelve a aparecer aunque esté en un contacto o una importación.

Si no hay ninguno, **Añadir cumpleaños**, en Campos, permite añadirlo. La rutina de cumpleaños lee el mismo cumpleaños que aparece en la página. El cumpleaños es un dato personal: nunca se comparte con tu equipo, ni siquiera en un registro compartido.

## Importar una hoja de cálculo

**Importar CSV…**, debajo del menú de ordenación de Personas, Organizaciones o Proyectos, permite añadir una hoja de cálculo guardada como CSV.

1. Revisa las columnas. Tu Machine intenta identificarlas por los encabezados y su contenido; puedes cambiar cualquiera. Cuando tu modelo pueda ejecutarse, también las revisará y dará una breve explicación cuando no esté segura. Solo verá los encabezados, algunos valores de cada columna y las celdas que las reglas no hayan podido leer.
2. Revisa las correcciones. **Revisar** las muestra con el antes y el después: espacios de más, nombres en mayúsculas, números de teléfono en formato internacional, errores en direcciones de correo (gmial.com), sitios web convertidos en su dominio, fechas y valores en cualquier formato ("€12k" equivale a 12000), varias etiquetas en una celda, una etapa escrita de otra forma y filas duplicadas. Desmarca un tipo de corrección o una fila para dejarla como está.
3. Revisa la vista previa. Cada fila es nueva, coincide con un registro de Graph o se omite, con una explicación. Una persona coincide por correo electrónico (si no, por nombre y organización); una organización, por sitio web o nombre; y un proyecto, por nombre.
4. **Importar** añade los registros nuevos y completa los que coinciden. Las celdas vacías no cambian nada.

**Deshacer** justo después de importar, o **Deshacer la última importación** debajo del menú de ordenación, revierte la última importación si esos registros no han cambiado desde entonces. Si eso sobrescribiría una corrección posterior, se indica el motivo. El archivo permanece en tu Machine.

## Propietario

En una Fleet de trabajo, cada persona, organización y proyecto tiene un propietario: **Propietario**, en la sección Con quién de su página. Eres tú, a menos que elijas a alguien de tu Fleet de trabajo. **Propietario**, en Filtrar, muestra solo los tuyos. Cada cambio aparece en su cronología.

## Equipo

**Equipo**, junto a Mío, muestra lo que comparten tus compañeros, con las mismas pestañas y el mismo menú de ordenación. **Filtrar** permite acotar la lista por quién lo compartió, una organización (Personas) o el estado (Proyectos). Lo que añadas allí será tuyo.

El trabajo con clientes se comparte con la Machine de cada compañero, junto con su propietario, campos y etiquetas. Lo que ellos compartan aparece en la tuya. Cada conversación indica **Equipo** o **Solo tú**. Consulta [Graph del equipo](team-graph.md).
