---
title: Datos de la organización
area: graph
summary: Sector, tamaño, ubicación y logotipo de cada organización, consultados a partir de su dirección web.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 5
translated: 1690f417d7a70829
---
## De dónde salen

- En una Machine alojada, los datos de las organizaciones se consultan por ti y gratis.
- En tu ordenador, esta función está desactivada hasta que añadas una clave de un servicio de búsqueda de datos, como Apollo, People Data Labs o Hunter. Consulta la [guía de configuración](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Solo se envía la dirección web de la organización, nunca tus mensajes ni con quién tienes relación. En una Machine alojada o una Machine conectada a The Machine Network se consultan hasta 1,000 organizaciones al día; en los demás casos, hasta 50. Los datos se actualizan cada 90 días. No se consultan sitios compartidos ni proveedores de correo, como gmail.com. Las personas tienen su propia búsqueda de datos: consulta [Cargo y foto](people.md#job-title-and-photo).

Si la búsqueda no encuentra un logotipo, The Machine usa el icono que identifica el sitio web de la organización, guardado en tu Machine. Ningún servicio de logotipos sabe con quién tienes relación. Si hay un logotipo y un icono, en espacios pequeños, como la línea de una tarea, se muestra el icono cuadrado.

Si la búsqueda encuentra especialidades de la organización, se muestran hasta 5 debajo de su descripción. También puedes filtrar la lista de organizaciones por especialidad: **Filtrar** y luego **Especialidad**. Si la búsqueda de una persona también encuentra los datos de su empresa, esos datos se añaden a la organización, así que no hace falta consultarla por separado. Los datos consultados en los últimos 90 días no cambian.

## Corregir datos incorrectos

En la página de la organización:

- Pulsa **Editar** para cambiar el nombre, el sector, el tamaño, la ubicación, el año de fundación, la descripción, el sitio web, LinkedIn, las notas y qué significa para ti. Los cambios se conservan. Deja un campo vacío para volver a usar el valor encontrado en la búsqueda.
- Pulsa **Empresa equivocada, borrar datos**, en **Editar**, si se ha seleccionado la empresa equivocada.
- **Volver a buscar**, que aparece una vez borrados los datos, obtiene datos actualizados.
