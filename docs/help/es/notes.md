---
title: Notas
area: graph
summary: Una página clara por tema, como un viaje o tu hogar, enlazada con las personas y los proyectos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a32102a88a8b3856
---
Una nota ofrece una visión general de un tema: un viaje, tu hogar o cómo se gestionan las facturas. Las notas están en Graph, junto a Personas, Organizaciones y Proyectos. Se quedan en tu Machine y no se comparten con tu equipo.

## Empezar una nota

Pulsa **Nueva nota** en la parte superior de Notas. Ponle un título y pulsa **Empezar la nota** para abrir la página. **Añadir una línea** añade lo que quieras guardar. Cada línea de texto se convierte en una línea independiente.

## Enlazar personas, proyectos y otras notas

Escribe @ y las primeras letras de un nombre en una línea. Elige una persona, organización, proyecto o nota de la lista para añadir su nombre como enlace. En la página de lo que hayas enlazado, aparece **Enlazado desde** con tu nota.

## Notas debajo de otras notas

Una nota puede estar debajo de otra, como Electrodomésticos debajo de Hogar. Notas las muestra como un árbol: la flecha junto a una nota abre las que están debajo. Para mover una nota, pulsa **Editar** y elige dónde colocarla en **Debajo de**. **Nueva nota debajo de esta**, en el menú ⋯, crea una nota justo ahí.

## Notas que guarda tu Machine

Tu Machine también escribe notas por su cuenta a partir de tus mensajes y las mantiene al día. Cada línea indica de dónde viene, por ejemplo, quién envió el correo: tócala para abrir el mensaje. Una línea de **Lo que he aprendido** indica **De lo que aprendí**.

Tus cambios siempre se mantienen. Cambia el nombre de una nota, muévela, modifica sus fechas o una línea, y tu Machine lo conservará cuando actualice la nota. Si eliminas una línea o una nota, no volverá a aparecer. Las notas posteriores sobre el mismo tema se guardan donde pusiste la primera.

**Volver al original** muestra de nuevo las palabras que escribió tu Machine. Si editas una línea que viene de algo que aprendió tu Machine, también cambia en **Lo que he aprendido**, así solo hay una versión.

## Viajes

Cuando recibes en tu correo una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje en **Viajes**. Las reservas de un mismo trayecto van en un solo viaje: la ida, el hotel y la vuelta. El viaje incluye el código de reserva, el asiento y el billete de cada línea, en orden cronológico, y muestra las fechas. En [Calendario](calendar.md) aparece como una franja que abarca esos días y, al abrirla, muestra el viaje.

Lee los detalles de las reservas que las aerolíneas, los hoteles y las webs de reservas incluyen en sus correos de confirmación. Si un correo no los incluye, no se crea ningún viaje. Si cambia una reserva, se actualiza su línea; si se cancela, se elimina. Si se cancelan todas las reservas de un viaje, también se elimina el viaje.

## Eventos

Cuando recibes en tu correo entradas para un concierto, un partido, un festival o una conferencia, tu Machine añade el evento en **Eventos**, con una nota por evento. Una línea indica dónde es e incluye el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade a la misma nota. Al igual que un viaje, el evento muestra sus fechas y aparece como una franja en [Calendario](calendar.md) que abre la nota.

- Cada línea indica quién envió las entradas, como **De Example Tickets**, y abre ese correo.
- Si el correo de las entradas generó una tarea, por ejemplo, pagar las entradas, **Abrir la tarea** la muestra.
- Un evento reservado desde tu buzón de trabajo se marca como Trabajo; de lo contrario, como Personal.

Lee los detalles de las entradas que los vendedores incluyen en sus correos de confirmación, sin usar IA. Si un correo no los incluye, no se crea ningún evento. Si se cancela una reserva, se elimina; si se cancelan todas las entradas de un evento, también se elimina el evento.

## Hogar

En **Hogar**, tu Machine guarda lo que sabe sobre tu hogar: **Facturas y suscripciones**, **Electrodomésticos**, **Reparaciones y mantenimiento** y **Hogar**. Una sección aparece cuando tiene al menos dos líneas.

- Una factura periódica, como la de la luz o el agua, aparece en una línea con la frecuencia con la que llega y la fecha de la última. **Abrir la tarea** muestra la factura; el importe y los datos de pago se quedan ahí.
- Una suscripción que mantienes aparece en una línea que abre su tarea de **Suscripciones**. Las que cancelas no aparecen.
- Lo que tu Machine ha aprendido sobre tu hogar, como la marca de tu lavavajillas, también aparece en una línea. Si la editas, también cambia en **Lo que he aprendido**.
- Si guardas una nota propia en una sección, como una sobre tu lavavajillas en **Electrodomésticos**, lo relacionado con ese aparato se añade a tu nota. Tu Machine no crea por su cuenta notas de este tipo.

Solo se usan las facturas y suscripciones personales, y las notas de Hogar siempre son personales. Tu Machine consulta una vez a su IA sobre cada factura, suscripción o elemento nuevo que haya aprendido para determinar si tiene que ver con tu hogar. Si se trata de una factura, le indica quién la envía, nunca el importe.

## Salud

En **Salud**, tu Machine guarda lo que sabe sobre tu salud: **Citas**, **Médicos y atención**, **Medicamentos**, **Alergias y afecciones** y **Facturas y seguro**. Una sección aparece cuando tiene al menos dos líneas.

- Una cita de tu calendario a la que solo vas tú, como la del dentista, aparece en una línea con la próxima fecha o la última. **De tu calendario** la abre.
- Una factura de un médico, dentista o farmacia aparece en una línea que abre su tarea. El importe se queda ahí.
- Lo que tu Machine ha aprendido sobre tu salud, como una alergia, también aparece en una línea. Si la editas, también cambia en **Lo que he aprendido**.
- Tu nota personal en una sección, como una sobre tu fisioterapeuta en **Citas**, incluye lo relacionado con ese tema.

Las notas de Salud siempre son personales, aunque la factura llegue a tu correo de trabajo. Tu Machine consulta una vez a su IA sobre cada cita, factura o elemento nuevo que haya aprendido para determinar si tiene que ver con tu salud. De una cita, envía el nombre, nunca las notas ni quién más está invitado.

## Hijos

En **Hijos**, tu Machine guarda lo que sabe sobre tus hijos: **Escuela**, **Actividades**, **Médicos y atención** y **Facturas y tarifas**. Una sección aparece cuando tiene al menos dos líneas.

- Lo que tu Machine ha aprendido sobre tus hijos, como el nombre de su tutor o el día de natación, aparece en una línea enlazada a su página. Considera que alguien es hijo tuyo cuando en **Para ti** aparece esa relación, como hija o hijo.
- Un evento de tu calendario al que solo vas tú, como una reunión de padres, aparece en una línea con la próxima fecha o la última. **De tu calendario** lo abre.
- Una factura de la escuela, un club o una guardería aparece en una línea que abre su tarea. El importe se queda ahí.
- Tu nota personal sobre uno de tus hijos en una sección, como una sobre Isla en **Escuela**, incluye lo relacionado con ese hijo.

Las notas de Hijos siempre son personales, aunque la escuela escriba a tu correo de trabajo. Tu Machine consulta una vez a su IA sobre cada elemento nuevo para determinar si tiene que ver con tus hijos.

## Combinar, eliminar y deshacer

**Combinar en…**, en el menú ⋯, mueve las líneas de una nota y las notas que contiene a otra nota. A partir de entonces, tu Machine añadirá contenido a esa nota. **Eliminar** elimina una nota. Ambas acciones muestran **Deshacer** durante unos instantes. También aparece al eliminar una línea.

## No son notas de reuniones

Las notas de reuniones y las notas sobre personas u organizaciones se quedan donde estaban. Las notas de aquí son páginas independientes.
