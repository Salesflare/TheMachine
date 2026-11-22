---
title: Graph
area: graph
summary: Las personas, organizaciones y proyectos de tus mensajes, siempre al día automáticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 9052c679e45207f7
---
Tu Machine crea un mapa de las personas con las que tratas y de lo que ocurre, a partir de tus mensajes, reuniones y decisiones. No tienes que configurar nada y todo se queda en tu Machine.

- [Personas](people.md): todas las personas con las que estás en contacto, con un resumen y una cronología de cada una.
- [Organizaciones](organizations.md): las empresas donde trabajan, con sus personas y proyectos.
- [Proyectos](projects.md): lo que está pasando, en tableros con etapas, como las oportunidades de venta de un CRM.

## Actualizado hoy

Una línea discreta en la parte superior de cada lista indica qué ha actualizado hoy tu Machine, por ejemplo, **4 personas actualizadas hoy**. Tócala para ver quién y qué ha cambiado. Al tocar un nombre, se abre su página con **Cambios recientes** desplegado. Un punto pequeño marca cada fila y cada tarjeta del tablero que haya cambiado hoy. Solo cuenta los cambios que ha hecho tu Machine desde medianoche.

## Filtrar y ordenar

**Filtrar**, junto a las pestañas, reduce la lista. Cada lista tiene sus propios filtros. Personas: cercanía, último contacto, organización, propietario, etiqueta y **Tiene un proyecto abierto**. Organizaciones: sector, especialidad, tamaño, país, último contacto, propietario, etiqueta y **Tiene un proyecto abierto**. Proyectos: propietario, tablero, etapa, etiqueta, organización, valor, fecha de cierre prevista y **Sin respuesta en más de 10 días**.

Los filtros que elijas aparecen sobre la lista, junto con **Borrar**. En Proyectos, la lista y el tablero comparten un único filtro. En el móvil, se abren como una hoja.

El menú de ordenación permite ordenar la lista. Personas y Organizaciones se ordenan por cercanía, contacto más reciente o más antiguo, y nombre. Organizaciones también se pueden ordenar por tamaño. Proyectos se ordenan por última actividad, nombre, etapa, **Valor** y **Fecha de cierre**. **Descargar CSV**, debajo del menú de ordenación, guarda la pestaña que tienes abierta como una hoja de cálculo.

## Campos y etiquetas

En Campos, dentro de la página de una persona, organización o proyecto, haz clic en un valor para cambiarlo: **Guardar** o Intro guarda el cambio, **Cancelar** o Escape lo descarta y **Quitar** vacía el campo.

**Gestionar campos** (**Añadir un campo** si aún no hay ninguno) añade o quita campos de todos los registros de ese tipo. **Nuevo campo** añade un campo de texto, número, fecha o selección de una lista.

**+ Etiqueta** añade una etiqueta, como VIP o socio; **×** la quita. Las etiquetas aparecen en las listas. En el móvil, las etiquetas de una persona aparecen en su página. También puedes encontrarlas con **Filtrar**.

## Cumpleaños

El cumpleaños de una persona aparece en Contacto, junto con su origen: su contacto de Google, un cumpleaños de Google Calendar (la rutina de cumpleaños lo guarda para los contactos cercanos), una importación de Facebook, tus notas o tú. **Editar** permite añadirlo o corregirlo: el mes y el día, y el año si lo sabes (en ese caso, también aparece su edad).

El dato que añadas tú tiene prioridad sobre todos los demás y se conserva. **Quitar** lo elimina; ni un contacto ni una importación lo volverán a añadir.

Si no hay ningún cumpleaños, puedes añadirlo con **Añadir cumpleaños**, en Campos. La rutina de cumpleaños lee el mismo dato que aparece en la página. El cumpleaños es personal: nunca se comparte con tu equipo, ni siquiera en un registro compartido.

## Importar una hoja de cálculo

**Importar CSV…**, en el menú de ordenación de Personas, Organizaciones o Proyectos, añade una hoja de cálculo guardada como CSV.

1. Revisa las columnas. Tu Machine intenta identificarlas por sus encabezados y contenido. Puedes cambiar cualquiera de ellas. Cuando tu modelo esté listo, también las revisará y te dará una explicación breve cuando no esté segura. Solo verá los encabezados, algunos valores de cada columna y las celdas que las reglas no hayan podido leer.
2. Revisa las correcciones. **Revisar** las muestra con el antes y el después: espacios de más, nombres en mayúsculas, números de teléfono en formato internacional, errores en direcciones de correo (gmial.com), sitios web convertidos a su dominio, fechas y valores en cualquier formato ("€12k" equivale a 12000), varias etiquetas en una celda, una etapa escrita de otra forma y la misma fila repetida. Desmarca un tipo de corrección o una fila para dejarla como está.
3. Revisa la vista previa. Cada fila aparece como nueva, coincide con un registro que ya está en tu Graph o se omite, con una explicación. Una persona coincide por correo (o, si no lo tiene, por nombre y organización), una organización por sitio web o nombre y un proyecto por nombre.
4. **Importar** añade los registros nuevos y completa los que coinciden. Las celdas vacías no cambian nada.

Puedes **Deshacer** justo después de importar o usar **Deshacer la última importación**, en el menú de ordenación, siempre que esos registros no hayan cambiado desde entonces. Si deshacer sobrescribiría una corrección posterior, te explicará el motivo. El archivo se queda en tu Machine.

## Propietario

En un Fleet de trabajo, cada persona, organización y proyecto tiene un propietario. Lo verás en **Propietario**, dentro de Contigo, en su página. Eres tú, a menos que elijas a alguien de tu Fleet de trabajo. **Propietario**, en Filtrar, muestra solo tus registros. Cada cambio aparece en su cronología.

## Equipo

**Equipo**, junto a Míos, muestra lo que comparten tus compañeros, con las mismas pestañas y el mismo menú de ordenación. **Filtrar** permite reducir la lista por quién lo compartió, organización (Personas) o estado (Proyectos). Lo que añadas ahí será tuyo.

El trabajo con clientes se comparte con las Machines de tus compañeros, junto con su propietario, campos y etiquetas. Lo que ellos compartan aparecerá en la tuya. Cada hilo indica **Equipo** o **Solo tú**. Consulta [Graph del equipo](team-graph.md).
