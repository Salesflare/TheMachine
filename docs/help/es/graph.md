---
title: The Graph
area: graph
summary: Las personas, organizaciones y proyectos de tus mensajes, siempre actualizados automáticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
Tu Machine crea un mapa de las personas con las que te relacionas y de lo que ocurre, a partir de tus mensajes, reuniones y decisiones. No tienes que configurar nada y todo se queda en tu Machine.

- [Personas](people.md): todas las personas con las que estás en contacto, con un resumen y una cronología de cada una.
- [Organizaciones](organizations.md): las empresas donde trabajan, con sus personas y proyectos.
- [Proyectos](projects.md): lo que ocurre en tableros con etapas, como las oportunidades de un CRM.

## Actualizado hoy

Una línea discreta en la parte superior de cada lista indica qué ha actualizado hoy tu Machine, por ejemplo, **4 personas actualizadas hoy**. Tócala para ver quién y qué cambió. Al tocar un nombre, se abre su página con **Cambios recientes** abierto. Un punto pequeño marca cada fila y elemento del tablero que cambió hoy. Solo cuenta los cambios que ha hecho tu Machine, desde la medianoche.

## Filtrar y ordenar

**Filtrar**, junto a las pestañas, reduce la lista. Cada lista tiene sus propios filtros. Personas: cercanía, último contacto, organización, propietario, etiqueta y **Tiene un proyecto abierto**. Organizaciones: sector, especialidad, tamaño, país, último contacto, propietario, etiqueta y **Tiene un proyecto abierto**. Proyectos: propietario, tablero, etapa, etiqueta, organización, valor, fecha de cierre prevista y **Sin respuesta en más de 10 días**.

Los filtros que elijas aparecen encima de la lista, junto con **Borrar**. En Proyectos, la lista y el tablero comparten un mismo filtro. En el teléfono, se abren en una hoja.

El menú de ordenación ordena la lista. Personas y Organizaciones se ordenan por cercanía, contacto más reciente o más antiguo y nombre. Organizaciones también se pueden ordenar por tamaño. Proyectos se ordenan por actividad reciente, nombre, etapa, **Valor** y **Fecha de cierre**. **Descargar CSV**, debajo del menú de ordenación, guarda la pestaña que tienes abierta como una hoja de cálculo.

## Campos y etiquetas

En Campos, dentro de la página de una persona, organización o proyecto, haz clic en un valor para cambiarlo: **Guardar** o Intro lo conserva, **Cancelar** o Escape descarta el cambio y **Quitar** lo deja vacío.

**Gestionar campos** (**Añadir un campo** cuando no hay ninguno) añade o quita campos de todos los registros de ese tipo. **Campo nuevo** añade uno: de texto, número, fecha o una opción de una lista.

**+ Etiqueta** añade una etiqueta, como VIP o socio; **×** la quita. Las etiquetas aparecen en las listas y puedes encontrarlas con **Filtrar**.

## Cumpleaños

El cumpleaños de una persona aparece en Contacto, junto con su origen: su contacto de Google, un cumpleaños de Google Calendar (la rutina de cumpleaños lo guarda si es un contacto cercano), una importación de Facebook, tus notas o tú. **Editar** permite añadirlo o corregirlo: el mes y el día, y el año si lo sabes (en ese caso, también aparece su edad).

El dato que añadas tú tiene prioridad sobre cualquier otra fuente y no se borra. **Quitar** lo elimina; el contacto o una importación no lo vuelven a añadir.

Si no hay ninguno, **Añadir cumpleaños**, en Campos, lo añade. La rutina de cumpleaños lee el mismo dato que aparece en la página. El cumpleaños es personal: nunca se comparte con tu equipo, ni siquiera en un registro compartido.

## Importar una hoja de cálculo

**Importar CSV…**, debajo del menú de ordenación de Personas, Organizaciones o Proyectos, añade una hoja de cálculo guardada como CSV.

1. Comprueba las columnas. Tu Machine deduce qué contiene cada una a partir de los encabezados y los datos, pero puedes cambiar cualquiera de ellas. Cuando tu modelo puede ejecutarse, también las comprueba y da una breve explicación cuando no está seguro. Solo ve los encabezados, algunos valores de cada columna y las celdas que las reglas no pudieron leer.
2. Comprueba las correcciones. **Revisar** muestra el antes y el después: espacios de más, nombres en mayúsculas, números de teléfono en formato internacional, errores tipográficos en correos electrónicos (gmial.com), sitios web convertidos en su dominio, fechas y valores en cualquier formato ("€12k" equivale a 12000), varias etiquetas en una celda, una etapa escrita de otra forma y la misma fila dos veces. Desmarca un tipo de corrección o una fila para dejarla como está.
3. Comprueba la vista previa. Cada fila es nueva, coincide con una que ya está en tu Graph o se omite, con una explicación. Las personas coinciden por correo electrónico (si no, por nombre y organización), las organizaciones por sitio web o nombre y los proyectos por nombre.
4. **Importar** añade los registros nuevos y completa los que coinciden. Las celdas vacías no cambian nada.

**Deshacer** justo después de importar, o **Deshacer la última importación** debajo del menú de ordenación, revierte la última importación mientras esos registros no hayan cambiado desde entonces. Si eso sobrescribiría una corrección posterior, se indica el motivo. El archivo se queda en tu Machine.

## Propietario

En una Fleet de trabajo, cada persona, organización y proyecto tiene un propietario: **Propietario**, en la sección Contigo de su página. Eres tú, a menos que elijas a alguien de tu Fleet de trabajo. **Propietario** en Filtrar muestra solo los tuyos. Cada cambio aparece en su cronología.

## Equipo

**Equipo**, junto a Lo mío, muestra lo que comparten tus compañeros, con las mismas pestañas y el mismo menú de ordenación. **Filtrar** permite limitarlo según quién lo haya compartido, una organización (Personas) o el estado (Proyectos). Lo que añadas ahí es tuyo.

El trabajo con clientes se comparte con las Machines de tus compañeros, junto con su propietario, campos y etiquetas. Lo que ellos compartan aparece en la tuya. Cada hilo indica **Equipo** o **Solo tú**. Consulta [Graph del equipo](team-graph.md).
