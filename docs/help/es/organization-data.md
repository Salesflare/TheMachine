---
title: Datos de la organización
area: graph
summary: Sector, tamaño, ubicación y un logotipo junto a cada organización, consultados a partir de su dirección web.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 5
translated: f403410953e50582
---
## De dónde salen

- En una Machine alojada, los datos de las organizaciones se consultan por ti, sin coste.
- En tu propio ordenador, esta función está desactivada hasta que añadas una clave de un servicio de consulta, como Apollo, People Data Labs o Hunter. Consulta la [guía de configuración](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Solo se envía la dirección web de la organización, nunca tus mensajes ni las personas que conoces allí. Una Machine alojada, o una en The Machine Network, consulta hasta 1000 organizaciones al día; en los demás casos, hasta 50. Los datos se actualizan cada 90 días. Nunca se consultan sitios compartidos ni proveedores de correo, como gmail.com. Las personas se consultan por separado: consulta [Cargo y foto](people.md#job-title-and-photo).

Si la consulta no devuelve un logotipo, The Machine usa el icono del sitio web de la organización y lo guarda en tu Machine. Ningún servicio de logotipos sabe con quién trabajas. Si hay un logotipo y un icono, en espacios pequeños, como la línea de una tarea, se muestra el icono cuadrado.

Si la consulta devuelve especialidades, se muestran hasta 5 debajo de la descripción de la organización. También puedes filtrar la lista de organizaciones por especialidad: **Filtrar** y luego **Especialidad**. Si la consulta de una persona incluye los datos de su empresa, estos también se añaden a la organización, así que no hace falta consultarla por separado. Los datos consultados en los últimos 90 días no cambian.

## Corregir una organización incorrecta

En la página de la organización:

- Usa **Editar** para cambiar el nombre, el sector, el tamaño, la ubicación, el año de fundación, la descripción, el sitio web, LinkedIn, las notas y tu relación con ella. Tus cambios se conservan. Deja un campo vacío para volver a usar el valor consultado.
- Usa **Empresa equivocada, borrar datos**, en **Editar**, si se ha seleccionado la empresa incorrecta.
- **Volver a buscar**, que aparece después de borrar los datos, consulta datos actualizados.
