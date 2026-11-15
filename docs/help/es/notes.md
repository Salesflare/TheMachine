---
title: Notas
area: graph
summary: Una página clara por tema, como un viaje o tu hogar, enlazada con las personas y los proyectos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, bookings.py, home_notes.py, dashboard/graph-notes.js
order: 8
translated: 4a6b4d56a8d9b93f
---
Una nota ofrece una visión general de un tema: un viaje, tu hogar o cómo se pagan las facturas. Las notas aparecen en Graph junto a Personas, Organizaciones y Proyectos. Se quedan en tu Machine y no se comparten con tu equipo.

## Crear una nota

Pulsa **Nueva nota** en la parte superior de Notas. Ponle un título y pulsa **Empezar la nota** para abrir la página. **Añadir una línea** añade lo que quieras guardar. Cada línea de texto se convierte en una línea independiente.

## Enlazar con personas, proyectos y otras notas

Escribe @ y algunas letras de un nombre en una línea. Elige una persona, organización, proyecto o nota de la lista para insertar su nombre como enlace. En la página de cada elemento enlazado aparece **Enlazado desde** con tu nota.

## Notas dentro de otras notas

Una nota puede estar dentro de otra, como Electrodomésticos dentro de Hogar. Notas las muestra en forma de árbol: la flecha junto a una nota abre las que contiene. Para mover una nota, pulsa **Editar** y elige dónde colocarla en **Debajo de**. **Nueva nota debajo de esta**, en el menú ⋯, crea una nota justo ahí.

## Notas que guarda tu Machine

Tu Machine también escribe notas por su cuenta a partir de tus mensajes y las mantiene al día. Cada línea indica de dónde procede, por ejemplo, quién envió el correo: tócala para abrir el mensaje. Las líneas de **Lo que he aprendido** indican **De lo que aprendí**.

Tus cambios siempre prevalecen. Cambia el nombre de una nota, muévela, cambia sus fechas o edita una línea, y tu Machine lo mantendrá así cuando actualice la nota. Si eliminas una línea o una nota, no vuelve a aparecer. Las notas posteriores sobre el mismo tema se añaden donde colocaste la primera.

**Volver al original** muestra de nuevo las palabras de tu Machine. Si editas una línea que procede de algo que tu Machine aprendió, también se actualiza en **Lo que he aprendido**, así solo hay una versión.

## Viajes

Cuando recibes en el correo una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje en **Viajes**. Las reservas de un mismo trayecto se agrupan en un viaje: la ida, el hotel y la vuelta. El viaje incluye el código de reserva, el asiento y el billete de cada línea, en orden cronológico, y muestra las fechas. En [Calendario](calendar.md) aparece como una sola franja que abarca esos días; al abrirla, se muestra el viaje.

Tu Machine lee los datos de la reserva que las aerolíneas, los hoteles y los sitios de reservas incluyen en el correo de confirmación. Si el correo no los incluye, no se crea un viaje. Si se modifica una reserva, se actualiza su línea; si se cancela, se elimina. Cuando se cancelan todas las reservas de un viaje, el viaje también desaparece.

## Hogar

En **Hogar**, tu Machine guarda lo que sabe sobre tu hogar: **Facturas y suscripciones**, **Electrodomésticos**, **Reparaciones y mantenimiento** y **Hogar**. Cada sección aparece cuando tiene al menos dos líneas.

- Las facturas periódicas, como las de la luz o el agua, aparecen en una línea que indica cada cuánto llegan y la fecha de la última. **Abrir la tarea** muestra la factura; el importe y los datos de pago siguen ahí.
- Las suscripciones que mantienes aparecen en una línea que abre su tarea de **Suscripciones**. Las que cancelaste no aparecen.
- Lo que tu Machine ha aprendido sobre tu hogar, como la marca de tu lavavajillas, también aparece en una línea. Si la editas, también se actualiza en **Lo que he aprendido**.
- Si tienes una nota propia en una sección, por ejemplo, una sobre tu lavavajillas en **Electrodomésticos**, la información sobre ese aparato se añade a tu nota. Tu Machine no crea notas de este tipo por su cuenta.

Solo se usan las facturas y suscripciones personales, y las notas de Hogar siempre son personales. Tu Machine pregunta una sola vez a su IA si cada factura, suscripción o elemento nuevo que ha aprendido tiene que ver con tu hogar. En el caso de una factura, envía quién la emite, nunca el importe.

## Combinar, eliminar y deshacer

**Combinar en…**, en el menú ⋯, mueve las líneas de una nota y las notas que contiene a otra nota. A partir de entonces, tu Machine añade información a esa nota. **Eliminar** borra una nota. Ambas acciones muestran **Deshacer** durante un momento. Lo mismo ocurre al eliminar una línea.

## No son lo mismo que las notas de reuniones

Las notas de reuniones y las notas sobre una persona o una organización siguen donde estaban. Las notas de aquí son páginas independientes.
