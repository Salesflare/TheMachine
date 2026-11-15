---
title: Notas
area: graph
summary: Una página fácil de leer por tema, como un viaje o tu hogar, enlazada con las personas y los proyectos que incluye.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, dashboard/graph-notes.js
order: 8
translated: 59dd4e1951e7cc7d
---
Una nota ofrece una visión general de un tema: un viaje, tu hogar o cómo se gestionan las facturas. Las notas aparecen en Graph junto a Personas, Organizaciones y Proyectos. Se guardan en tu Machine y no se comparten con tu equipo.

## Empezar una nota

Pulsa **Nueva nota** en la parte superior de Notas. Ponle un título y pulsa **Empezar la nota** para abrir su página. **Añadir una línea** agrega lo que quieras guardar. Cada línea de texto se convierte en una línea independiente.

## Enlazar personas, proyectos y otras notas

Escribe @ y unas cuantas letras de un nombre en una línea. Elige una persona, organización, proyecto o nota de la lista para insertar su nombre como enlace. En la página de cada elemento enlazado aparece **Enlazado desde** con tu nota.

## Notas dentro de otras notas

Una nota puede estar dentro de otra, como Electrodomésticos dentro de Hogar. Notas las muestra en forma de árbol: la flecha junto a una nota abre las notas que contiene. Para mover una nota, pulsa **Editar** y elige dónde colocarla en **Debajo de**. **Nueva nota debajo de esta**, en el menú ⋯, crea una nota justo ahí.

## Notas que tu Machine guarda

Tu Machine también escribe notas por su cuenta a partir de tus mensajes y las mantiene al día. Cada línea indica de dónde viene, por ejemplo, quién envió el correo: tócala para abrir el mensaje. Una línea de **Lo que he aprendido** muestra **De lo que aprendí**.

Tus cambios siempre se respetan. Cambia el nombre de una nota, muévela, modifica sus fechas o una línea, y tu Machine la mantendrá así cuando la actualice. Si eliminas una línea o una nota, no volverá a aparecer. Las notas posteriores sobre el mismo tema se añaden donde colocaste la primera.

**Volver al original** muestra de nuevo las palabras que escribió tu Machine. Si editas una línea que tu Machine aprendió, también cambia en **Lo que he aprendido**, así solo hay una versión.

## Viajes

Cuando llega a tu correo una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje en **Viajes**. Las reservas de un mismo trayecto se agrupan en un viaje: la ida, el hotel y la vuelta. El viaje incluye el código de reserva, el asiento y el billete de cada línea, en orden cronológico, y muestra las fechas. En [Calendario](calendar.md) aparece como una franja que abarca esos días. Al abrirla, se muestra el viaje.

Tu Machine lee los detalles de las reservas que las aerolíneas, los hoteles y los sitios de reservas incluyen en sus correos de confirmación. Un correo sin esos datos no crea un viaje. Si se modifica una reserva, se actualiza su línea; si se cancela, desaparece. Si se cancelan todas las reservas de un viaje, el viaje también desaparece.

## Hogar

En **Hogar**, tu Machine guarda lo que sabe sobre tu hogar: **Facturas y suscripciones**, **Electrodomésticos**, **Reparaciones y mantenimiento** y **Hogar**. Cada sección aparece cuando tiene al menos dos líneas.

- Las facturas periódicas, como las de la luz o el agua, aparecen con una línea que indica cada cuánto llegan y la fecha de la última. **Abrir la tarea** muestra la factura. El importe y los detalles del pago se quedan ahí.
- Las suscripciones que conservas aparecen con una línea que abre su tarea de **Suscripciones**. Las que cancelaste no aparecen.
- La información que tu Machine aprendió sobre tu hogar, como la marca de tu lavavajillas, también aparece en una línea. Si la editas, también cambia en **Lo que he aprendido**.
- Si tienes una nota propia en una sección, por ejemplo una sobre tu lavavajillas en **Electrodomésticos**, la información sobre ese electrodoméstico se añade a tu nota. Tu Machine no crea notas de este tipo por su cuenta.

Solo se usan las facturas y suscripciones personales, y las notas de Hogar siempre son personales. Tu Machine consulta una vez a su IA sobre cada factura, suscripción o dato nuevo que aprende para determinar si está relacionado con tu hogar. En el caso de una factura, le indica quién la envió, nunca el importe.

## Salud

En **Salud**, tu Machine guarda lo que sabe sobre tu salud: **Citas**, **Médicos y atención**, **Medicamentos**, **Alergias y afecciones** y **Facturas y seguro**. Cada sección aparece cuando tiene al menos dos líneas.

- Una cita de tu calendario a la que solo vas tú, como la del dentista, aparece con la próxima fecha o, si ya pasó, con la última. **De tu calendario** la abre.
- Las facturas de un médico, dentista o farmacia aparecen con una línea que abre su tarea. El importe se queda ahí.
- La información que tu Machine aprendió sobre tu salud, como una alergia, también aparece en una línea. Si la editas, también cambia en **Lo que he aprendido**.
- La información sobre un tema se añade a tu propia nota de esa sección, por ejemplo, a una nota sobre tu fisioterapeuta en **Citas**.

Las notas de Salud siempre son personales, aunque la factura haya llegado a tu correo del trabajo. Tu Machine consulta una vez a su IA sobre cada cita, factura o dato nuevo que aprende para determinar si está relacionado con tu salud. Envía el nombre de la cita, nunca sus notas ni quién más está invitado.

## Combinar, eliminar y deshacer

**Combinar en…**, en el menú ⋯, mueve las líneas de una nota y las notas que contiene a otra nota. A partir de entonces, tu Machine añadirá la información a esa nota. **Eliminar** borra una nota. En ambos casos, y también al eliminar una línea, aparece **Deshacer** durante unos instantes.

## No son lo mismo que las notas de reuniones

Las notas de reuniones y las notas sobre una persona u organización se quedan donde estaban. Las notas de aquí son páginas independientes.
