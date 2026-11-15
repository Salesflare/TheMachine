---
title: Notas
area: graph
summary: Una página fácil de leer por tema, como un viaje o tu Hogar, enlazada con las personas y los proyectos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: b88647412222409d
---
Una nota es un resumen de un tema: un viaje, tu Hogar, cómo se gestionan las facturas. Las notas aparecen en Graph junto a Personas, Organizaciones y Proyectos. Se guardan en tu Machine y no se comparten con tu equipo.

## Empezar una nota

Pulsa **Nueva nota** en la parte superior de Notas. Ponle un título y pulsa **Empezar la nota** para abrir la página. **Añadir una línea** añade lo que quieras guardar. Cada línea de texto se convierte en una línea independiente.

## Enlazar personas, proyectos y otras notas

Escribe @ y las primeras letras de un nombre en una línea. Elige una persona, organización, proyecto o nota de la lista para añadir su nombre como enlace. En la página de lo que hayas enlazado aparecerá **Enlazado desde** con tu nota.

## Notas dentro de otras notas

Una nota puede estar dentro de otra, como Electrodomésticos dentro de Hogar. Notas las muestra en forma de árbol: pulsa la flecha junto a una nota para ver las que contiene. Para mover una nota, pulsa **Editar** y elige dónde colocarla en **Debajo de**. **Nueva nota debajo de esta**, en el menú ⋯, crea una nota ahí mismo.

## Notas que guarda tu Machine

Tu Machine también crea notas a partir de tus mensajes y las mantiene al día. Cada línea indica de dónde viene, por ejemplo, quién envió el correo: tócala para abrir el mensaje. Una línea de **Lo que he aprendido** indica **De lo que aprendí**.

Tus cambios siempre se mantienen. Cambia el nombre de una nota, muévela o modifica sus fechas o una línea, y tu Machine lo conservará cuando actualice la nota. Si eliminas una línea o una nota, no volverá a aparecer. Las notas futuras sobre el mismo tema se añadirán donde hayas puesto la primera.

**Volver al original** muestra de nuevo las palabras originales de tu Machine. Si editas una línea que tu Machine obtuvo de algo que aprendió, también cambiará en **Lo que he aprendido**, para que solo haya una versión.

## Viajes

Cuando recibes en tu correo una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje en **Viajes**. Las reservas de un mismo trayecto van juntas en un viaje: la ida, el hotel y la vuelta. El viaje incluye el código de reserva, el asiento y el billete de cada línea, en orden cronológico, y muestra las fechas. En [Calendario](calendar.md) aparece como una sola franja que abarca esos días; al abrirla, se muestra el viaje.

Tu Machine lee los datos de las reservas que las aerolíneas, los hoteles y las webs de reservas incluyen en sus correos de confirmación. Si un correo no contiene esos datos, no se crea ningún viaje. Los correos de reservas anteriores, dentro del año de [historial](history.md) que conserva tu Machine, se procesan en segundo plano cuando se añade ese historial. Si se modifica una reserva, se actualiza su línea; si se cancela, se elimina. Cuando se cancelan todas las reservas de un viaje, también se elimina el viaje.

## Eventos

Cuando recibes en tu correo entradas para un concierto, un partido, un festival o una conferencia, tu Machine añade el evento en **Eventos**, en una nota por evento. Una línea indica dónde es e incluye el código de reserva, el asiento y la cantidad de entradas. Si haces otro pedido para el mismo evento, se añade a la misma nota. Al igual que un viaje, el evento muestra sus fechas y aparece como una franja en [Calendario](calendar.md) que abre la nota.

- Cada línea indica quién envió las entradas, como **De Example Tickets**, y abre ese correo.
- Si del correo de las entradas se creó una tarea, por ejemplo, para pagarlas, **Abrir la tarea** la muestra.
- Un evento reservado desde tu correo de trabajo es de Trabajo; de lo contrario, es Personal.

Tu Machine lee los datos de las entradas que los vendedores incluyen en sus correos de confirmación, sin usar IA. Si un correo no contiene esos datos, no se crea ningún evento. Si se cancela una reserva, se elimina; cuando se cancelan todas las entradas de un evento, también se elimina el evento.

## Hogar

En **Hogar**, tu Machine guarda lo que sabe sobre tu hogar: **Facturas y suscripciones**, **Electrodomésticos**, **Reparaciones y mantenimiento** y **Hogar**. Una sección aparece cuando tiene al menos dos líneas.

- Una factura periódica, como la de la luz o el agua, aparece en una línea que indica cada cuánto llega y la fecha de la última. **Abrir la tarea** muestra la factura; el importe y los datos de pago se quedan ahí.
- Una suscripción que mantienes aparece en una línea que abre su tarea de **Suscripciones**. Las que hayas cancelado no aparecen.
- Lo que tu Machine ha aprendido sobre tu hogar, como la marca de tu lavavajillas, también aparece en una línea. Si la editas, también cambiará en **Lo que he aprendido**.
- Si guardas una nota propia en una sección, por ejemplo, una sobre tu lavavajillas en **Electrodomésticos**, lo relacionado con ese aparato se añade a tu nota. Tu Machine no crea notas de ese tipo por su cuenta.

Solo se usan las facturas y suscripciones personales, y las notas de Hogar siempre son personales. Tu Machine le pregunta una vez a su IA sobre cada factura, suscripción o cosa nueva que haya aprendido, para determinar si tiene que ver con tu hogar. En el caso de una factura, le indica quién la envía, nunca el importe.

## Salud

En **Salud**, tu Machine guarda lo que sabe sobre tu salud: **Citas**, **Médicos y atención**, **Medicamentos**, **Alergias y afecciones** y **Facturas y seguro**. Una sección aparece cuando tiene al menos dos líneas.

- Una cita de tu calendario a la que solo vas tú, como la del dentista, aparece en una línea con la próxima fecha o la última. **De tu calendario** la abre.
- Una factura de un médico, dentista o farmacia aparece en una línea que abre su tarea. El importe se queda ahí.
- Lo que tu Machine ha aprendido sobre tu salud, como una alergia, también aparece en una línea. Si la editas, también cambiará en **Lo que he aprendido**.
- Si tienes una nota propia en una sección, por ejemplo, una sobre tu fisioterapeuta en **Citas**, lo relacionado con ese tema se añade a esa nota.

Las notas de Salud siempre son personales, aunque la factura haya llegado a tu correo del trabajo. Tu Machine le pregunta una vez a su IA sobre cada cita, factura o cosa nueva que haya aprendido, para determinar si tiene que ver con tu salud. Le envía el nombre de la cita, nunca las notas ni los nombres de otras personas invitadas.

## Hijos

En **Hijos**, tu Machine guarda lo que sabe sobre tus hijos: **Escuela**, **Actividades**, **Médicos y atención** y **Facturas y tarifas**. Una sección aparece cuando tiene al menos dos líneas.

- Lo que tu Machine ha aprendido sobre tus hijos, como el nombre de su tutor o tutora de clase o el día que tienen natación, aparece en una línea enlazada a su página. Considera que alguien es tu hijo cuando en **Para ti** se indica que lo es, por ejemplo, hija o hijo.
- Un evento de tu calendario al que solo vas tú, como una reunión de padres, aparece en una línea con la próxima fecha o la última. **De tu calendario** lo abre.
- Una factura de la escuela, de una actividad o de la guardería aparece en una línea que abre su tarea. El importe se queda ahí.
- Si tienes una nota propia para uno de tus hijos en una sección, por ejemplo, una nota sobre Isla en **Escuela**, lo relacionado con ese hijo se añade a esa nota.

Las notas de Hijos siempre son personales, aunque la escuela escriba a tu correo del trabajo. Tu Machine le pregunta una vez a su IA sobre cada cosa nueva para determinar si tiene que ver con tus hijos.

## Combinar, eliminar y deshacer

**Combinar en…**, en el menú ⋯, mueve las líneas de una nota y las notas que contiene a otra nota. A partir de entonces, tu Machine añadirá contenido a esa nota. **Eliminar** borra una nota. Durante un momento, aparece **Deshacer** después de cualquiera de estas acciones y también al eliminar una línea.

## No son notas de reuniones

Las notas de reuniones y las notas sobre personas u organizaciones se quedan donde estaban. Las notas de aquí son páginas independientes.
