---
title: Páginas web vigiladas
area: connections
summary: Una página web que vigilas. Una tarea solo cuando cambia algo que importa.
covers: connector:web_page
code: connectors/web_page.py
---
## Qué lee

El texto de una página web pública por conexión, cada pocas horas y como mucho una vez por hora. Deja fuera los menús, los pies de página, los avisos de cookies y los anuncios. Cuando el texto cambió, The Machine mira qué cambió y solo crea una tarea si importa, como un precio nuevo o una política cambiada. Las fechas, los contadores y los pequeños cambios de redacción nunca crean una tarea. Una página sin cambios no cuesta nada.

Primero consulta el robots.txt del sitio y deja la página en paz si el sitio dice que no. Las páginas que piden iniciar sesión o que solo se construyen con JavaScript no se pueden vigilar.

## Qué puede hacer

Nada. Solo lee la página.

## Conéctalo

1. En el panel, abre **Conexiones**, luego **Otras**, y elige Página web. O ejecuta `assistant connect web_page`.
2. Pega la dirección de la página.

O pídelo en tu chat: "Vigila esta página por si cambian los precios" con su dirección. Pregunta qué páginas vigilas, o pide dejar de vigilar una.

## Quítalo

En el panel: **Conexiones**, abre la página, **Detalles** y luego **Desconectar**. O pide a tu chat que deje de vigilarla.
