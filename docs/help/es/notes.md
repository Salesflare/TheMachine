---
title: Notas
area: graph
summary: Una página clara por tema, como un viaje o tu hogar, enlazada con las personas y los proyectos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 336e0f0dad44f19a
---
Una nota es el resumen de un tema: un viaje, tu hogar o cómo se pagan las facturas. Las notas aparecen en Graph junto a las personas, las organizaciones y los proyectos. Se guardan en tu Machine y no se comparten con tu equipo.

## Empezar una nota

Pulsa **Nueva nota** en la parte superior de Notas. Ponle un título y pulsa **Empezar la nota** para abrir su página. **Añadir una línea** agrega lo que quieras guardar. Cada línea de texto se convierte en una línea independiente.

## Enlazar personas, proyectos y otras notas

Escribe @ y unas letras del nombre en una línea. Elige una persona, organización, proyecto o nota de la lista para añadir su nombre como enlace. En la página de lo que hayas enlazado, verás **Enlazado desde** y el nombre de tu nota.

## Notas dentro de otras notas

Una nota puede estar dentro de otra, como Electrodomésticos dentro de Hogar. Notas las muestra como un árbol: pulsa la flecha junto a una nota para abrir las que contiene. Para mover una nota, pulsa **Editar** y elige dónde colocarla en **Debajo de**. **Nueva nota debajo de esta**, en el menú ⋯, crea una nota ahí mismo.

En la parte superior de la página de una nota se muestra dónde está, como **Notas › Hijos**: pulsa cualquier parte para ir allí. En el móvil, las notas intermedias se ocultan en ⋯.

## Notas que guarda tu Machine

Tu Machine también escribe notas por su cuenta a partir de tus mensajes y las mantiene actualizadas. Cada línea indica de dónde viene, por ejemplo, quién envió el correo: púlsala para abrir el mensaje. Las líneas que vienen de **Lo que he aprendido** indican **De lo que aprendí**. Las reuniones y las citas de tu calendario nunca aparecen como líneas independientes: se quedan en [Calendario](calendar.md).

**Hogar**, **Salud** e **Hijos** aparecen solo cuando tu Machine tiene al menos dos datos concretos que añadir, como una factura o algo que haya aprendido. Hasta entonces no aparecen en la lista y, si vuelven a quedarse sin datos, desaparecen.

Tus cambios siempre se mantienen. Cambia el nombre de una nota, muévela, cambia sus fechas o una línea, y tu Machine lo conservará al actualizarla. Si eliminas una línea o una nota, no volverá a aparecer. Las notas posteriores sobre el mismo tema se guardan donde pusiste la primera.

**Volver al original** muestra de nuevo las palabras originales de tu Machine. Si editas una línea que viene de algo que tu Machine aprendió, también cambiará en **Lo que he aprendido**, para que solo haya una versión.

## Viajes

Cuando llega a tu correo una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje en **Viajes**. Las reservas de un mismo viaje se agrupan: la ida, el hotel y la vuelta. El viaje incluye el código de reserva, el asiento y el billete de cada línea, por orden cronológico, y muestra las fechas. En [Calendario](calendar.md) aparece como una franja que abarca esos días y que abre el viaje.

Tu Machine lee los datos de las reservas que las aerolíneas, los hoteles y las páginas de reservas incluyen en los correos de confirmación. Los correos que no los incluyen no generan un viaje. Los correos de reservas anteriores que estén dentro del año de [historial](history.md) que guarda tu Machine se leen en segundo plano una vez que ese historial está disponible, empezando por tus buzones personales. Si más adelante se lee una confirmación antigua, se añade al viaje que ya existe.

Si una reserva cambia, se actualiza su línea. Si se cancela, se elimina. Cuando se cancelan todas las reservas de un viaje, el viaje también desaparece.

## Eventos

Cuando llegan a tu correo entradas para un concierto, un partido, un festival o una conferencia, tu Machine añade el evento en **Eventos**, con una nota por evento. Una línea indica dónde es e incluye el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade a la misma nota. Al igual que un viaje, el evento muestra sus fechas y aparece como una franja en [Calendario](calendar.md) que abre la nota.

- Cada línea indica quién envió las entradas, como **De Example Tickets**, y abre ese correo.
- Si el correo de las entradas generó una tarea, por ejemplo, pagar las entradas, aparece **Abrir la tarea**.
- Un evento reservado desde tu buzón del trabajo es de Trabajo; si no, es Personal.

Tu Machine lee, sin usar IA, los datos de las entradas que los vendedores incluyen en sus correos de confirmación. Los correos que no los incluyen no generan un evento. Si se cancela una reserva, se elimina. Cuando se cancelan todas las entradas de un evento, el evento también desaparece.

## Hogar

En **Hogar**, tu Machine guarda lo que sabe sobre tu hogar: **Facturas y suscripciones**, **Electrodomésticos**, **Reparaciones y mantenimiento** y **Hogar**. Cada sección aparece cuando tiene al menos dos líneas.

- Las facturas periódicas, como las de energía o agua, tienen una línea que indica cada cuánto llegan y la fecha de la última. **Abrir la tarea** muestra la factura; el importe y los datos de pago se quedan ahí.
- Las suscripciones que mantienes tienen una línea que abre su tarea de **Suscripciones**. Las que cancelaste no aparecen.
- Las personas o entidades que suelen escribirte sobre tu hogar, como tu proveedor de energía, de internet o el ayuntamiento, tienen una línea que indica cada cuánto escriben. Púlsala para abrir su correo más reciente.
- Lo que tu Machine haya aprendido sobre tu hogar, como la marca de tu lavavajillas, también aparece en una línea. Si la editas, también cambiará en **Lo que he aprendido**.
- Si guardas una nota propia en una sección, por ejemplo, una sobre tu lavavajillas en **Electrodomésticos**, lo relacionado con ese aparato se guarda en tu nota. Tu Machine no crea notas de este tipo por su cuenta.

Solo se usan las facturas, las suscripciones y los correos personales, y las notas de Hogar siempre son personales. Tu Machine pregunta una vez a su IA por cada factura, suscripción o dato nuevo que aprende para determinar si tiene que ver con tu hogar. En el caso de una factura, le indica quién la envía, pero nunca el importe.

Para **Hogar**, **Salud** e **Hijos** en conjunto, tu Machine también pregunta una vez a su IA por cada remitente de tus correos personales. Le envía el nombre del remitente, cuántos correos envió y los asuntos más recientes con los números ocultos, pero nunca el correo en sí. Si un correo llegó dos veces o a dos de tus buzones, cuenta una sola vez. Lo mismo ocurre con una respuesta que tiene el mismo asunto que otros correos del hilo.

Los correos masivos nunca se añaden a estas notas ni se envían a la IA: el spam, las promociones, los boletines y otros correos de listas, además de las notificaciones de direcciones que no admiten respuestas. Los correos de un hilo al que respondiste sí cuentan, al igual que los correos de reservas para **Viajes** y **Eventos**.

La primera vez, tu Machine revisa los correos del último año en unas horas, fuera del horario nocturno y solo si tu plan de IA tiene capacidad disponible. Después, revisa los remitentes nuevos cada seis horas.

## Salud

En **Salud**, tu Machine guarda lo que sabe sobre tu salud: **Citas**, **Resultados de las pruebas**, **Médicos y atención**, **Medicamentos**, **Alergias y afecciones** y **Facturas y seguro**. Cada sección aparece cuando tiene al menos dos líneas.

- Las facturas de un médico, dentista o farmacia tienen una línea que abre su tarea. El importe se queda ahí.
- Cada correo de tu clínica, un hospital, un laboratorio o tu aseguradora médica aparece como una línea fechada con su asunto, para que tu historial se complete con el tiempo. Púlsala para abrir el correo.
- Lo que tu Machine haya aprendido sobre tu salud, como una alergia, también aparece en una línea. Si la editas, también cambiará en **Lo que he aprendido**.
- En una nota propia de una sección, como una sobre tu fisioterapeuta en **Citas**, se guarda lo relacionado con esa persona.

Las notas de Salud siempre son personales, incluso si una factura llegó a tu correo del trabajo. Tu Machine pregunta una vez a su IA por cada factura o dato nuevo que aprende para determinar si tiene que ver con tu salud.

## Hijos

En **Hijos**, tu Machine guarda lo que sabe sobre tus hijos: **Escuela**, **Actividades**, **Cuidado infantil**, **Médicos y atención** y **Facturas y tarifas**. Las niñeras y las guarderías aparecen en Cuidado infantil, nunca en Médicos y atención. Cada sección aparece cuando tiene al menos dos líneas.

- Lo que tu Machine haya aprendido sobre tu hijo, como quién es su tutor o qué día tiene natación, aparece en una línea que enlaza con su página. Considera que alguien es tu hijo cuando en **Para ti** aparece como tal, por ejemplo, como hija o hijo.
- Las facturas de la escuela, un club o el cuidado infantil tienen una línea que abre su tarea. El importe se queda ahí.
- Cada correo de la escuela, un club o el servicio de cuidado infantil, como un aviso sobre una excursión o un cambio de planes, aparece como una línea fechada con su asunto. Así, todos los mensajes están en un mismo sitio. Púlsala para abrir el correo.
- En una nota propia de una sección para uno de tus hijos, como una sobre Isla en **Escuela**, se guarda lo relacionado con ese hijo.

Las notas de Hijos siempre son personales, incluso si la escuela escribe a tu correo del trabajo. Tu Machine pregunta una vez a su IA por cada dato nuevo para determinar si tiene que ver con tus hijos.

## Combinar, eliminar y deshacer

**Combinar en…**, en el menú ⋯, mueve las líneas de una nota y las notas que contiene a otra nota. A partir de entonces, tu Machine añadirá la información a esa nota. **Eliminar** borra una nota. En ambos casos, aparece **Deshacer** durante un momento; también aparece al eliminar una línea.

## No son notas de reuniones

Las notas de reuniones y las notas sobre personas u organizaciones se quedan donde estaban. Las notas de aquí son páginas independientes.
