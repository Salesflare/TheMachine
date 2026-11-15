---
title: Notas
area: graph
summary: Una página clara por tema, como un viaje o tu hogar, enlazada con las personas y los proyectos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 8e27b2c69f77196d
---
Una nota es un resumen de un tema: un viaje, tu hogar o cómo se gestionan las facturas. Las notas aparecen en Graph junto a Personas, Organizaciones y Proyectos. Se quedan en tu Machine y no se comparten con tu equipo.

## Empezar una nota

Pulsa **Nueva nota** en la parte superior de Notas. Ponle un título y pulsa **Empezar la nota** para abrir la página. Con **Añadir una línea** puedes guardar lo que quieras. Cada línea de texto se convierte en una línea independiente.

## Enlazar con personas, proyectos y otras notas

Escribe @ y unas cuantas letras de un nombre en una línea. Elige una persona, organización, proyecto o nota de la lista para añadir su nombre como enlace. En la página de lo que hayas enlazado, aparecerá **Enlazado desde** junto con tu nota.

## Notas dentro de otras notas

Puedes guardar una nota dentro de otra, como Electrodomésticos dentro de Hogar. Notas las muestra en forma de árbol: pulsa la flecha junto a una nota para abrir las notas que contiene. Para mover una nota, pulsa **Editar** y elige dónde colocarla en **Debajo de**. Con **Nueva nota debajo de esta** en el menú ⋯ puedes crear una nota ahí mismo.

En la parte superior de la página de una nota se muestra dónde está, por ejemplo, **Notas › Hijos**. Pulsa cualquier parte para ir allí. En el móvil, las notas intermedias se agrupan en ⋯.

## Notas que guarda tu Machine

Tu Machine también escribe notas por su cuenta a partir de tus mensajes y las mantiene al día. Cada línea indica de dónde viene, por ejemplo, quién envió el correo: púlsala para abrir el mensaje. Las líneas que vienen de **Lo que he aprendido** muestran **De lo que aprendí**. Las reuniones y las citas del calendario nunca aparecen como líneas independientes: se quedan en [Calendario](calendar.md).

**Hogar**, **Salud** e **Hijos** solo aparecen cuando tu Machine tiene al menos dos datos concretos que incluir, como una factura o algo que haya aprendido. Hasta entonces, no aparecen en la lista. Si después se quedan sin datos, desaparecen.

Tus cambios siempre se mantienen. Si cambias el nombre de una nota, la mueves, cambias sus fechas o editas una línea, tu Machine lo conserva cuando actualiza la nota. Si eliminas una línea o una nota, no volverá a aparecer. Las notas que se creen más adelante sobre el mismo tema irán donde hayas puesto la primera.

**Volver al original** muestra de nuevo el texto original de tu Machine. Si editas una línea que viene de algo que tu Machine aprendió, también cambiará en **Lo que he aprendido**, para que solo haya una versión.

## Viajes

Cuando recibes un correo con una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje en **Viajes**. Las reservas de un mismo trayecto se agrupan en un viaje: la ida, el hotel y la vuelta. El viaje incluye el código de reserva, el asiento y el billete de cada línea, en orden cronológico, y muestra las fechas. En [Calendario](calendar.md) aparece como una franja que abarca esos días. Al pulsarla, se abre el viaje.

Tu Machine lee los detalles de la reserva que las aerolíneas, los hoteles y las webs de reservas incluyen en sus correos de confirmación. Si un correo no los incluye, no se crea un viaje. Los correos con reservas anteriores, dentro del año de [historial](history.md) que conserva tu Machine, se procesan en segundo plano cuando se incorpora ese historial, empezando por tus buzones personales.

Si cambia una reserva, se actualiza su línea. Si se cancela, se elimina. Cuando se cancelan todas las reservas de un viaje, también se elimina el viaje.

## Eventos

Cuando recibes entradas para un concierto, un partido, un festival o una conferencia, tu Machine añade el evento en **Eventos**, como una nota por evento. Una línea indica dónde es e incluye el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade a la misma nota. Al igual que un viaje, el evento muestra sus fechas y aparece como una franja en [Calendario](calendar.md) que abre la nota.

- Cada línea indica de quién son las entradas, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo de las entradas creó una tarea, como pagar las entradas, aparecerá **Abrir la tarea**.
- Los eventos reservados en tu buzón de trabajo son de Trabajo. Los demás son Personales.

Tu Machine lee los detalles de las entradas que los vendedores incluyen en sus correos de confirmación, sin usar IA. Si un correo no los incluye, no se crea un evento. Si se cancela una reserva, se elimina. Cuando se cancelan todas las entradas de un evento, también se elimina el evento.

## Hogar

En **Hogar**, tu Machine guarda lo que sabe sobre tu hogar: **Facturas y suscripciones**, **Electrodomésticos**, **Reparaciones y mantenimiento** y **Hogar**. Cada sección aparece cuando tiene al menos dos líneas.

- Las facturas periódicas, como las de luz o agua, aparecen en una línea que indica cada cuánto llegan y la fecha de la última. **Abrir la tarea** muestra la factura. El importe y los datos de pago se quedan allí.
- Las suscripciones que mantienes aparecen en una línea que abre su tarea de **Suscripciones**. Las que cancelas no aparecen.
- Las personas o entidades que escriben a menudo a tu hogar, como tu compañía de luz, tu proveedor de Internet o el ayuntamiento, aparecen en una línea que indica cada cuánto escriben. Púlsala para abrir su correo más reciente.
- Lo que tu Machine haya aprendido sobre tu hogar, como la marca del lavavajillas, también aparece en una línea. Si la editas, también cambiará en **Lo que he aprendido**.
- Si tienes una nota propia en una sección, por ejemplo, una para tu lavavajillas en **Electrodomésticos**, todo lo relacionado con ese aparato se incluirá en tu nota. Tu Machine no crea notas de este tipo por su cuenta.

Solo se usan facturas, suscripciones y correos personales, y las notas de Hogar siempre son personales. Tu Machine consulta una vez a su IA por cada factura, suscripción o dato nuevo que aprende para determinar si está relacionado con tu hogar. En el caso de una factura, le envía quién la ha emitido, pero nunca el importe.

Para **Hogar**, **Salud** e **Hijos**, tu Machine también consulta una vez a su IA por cada remitente de tus correos personales. Le envía el nombre del remitente, cuántos correos ha enviado y los asuntos de los más recientes, con los números ocultos. Nunca le envía el correo en sí.

La primera vez, revisa el último año de tus correos en unas horas, fuera del horario nocturno y solo cuando tu plan de IA tenga capacidad disponible. Después, revisa los remitentes nuevos cada seis horas.

## Salud

En **Salud**, tu Machine guarda lo que sabe sobre tu salud: **Citas**, **Resultados de las pruebas**, **Médicos y atención**, **Medicamentos**, **Alergias y afecciones** y **Facturas y seguro**. Cada sección aparece cuando tiene al menos dos líneas.

- Las facturas de médicos, dentistas o farmacias aparecen en una línea que abre su tarea. El importe se queda allí.
- Cada correo de tu consulta médica, un hospital, un laboratorio o tu aseguradora de salud aparece como una línea con fecha y asunto, para que tu historial se vaya acumulando. Pulsa la línea para abrir el correo.
- Lo que tu Machine haya aprendido sobre tu salud, como una alergia, también aparece en una línea. Si la editas, también cambiará en **Lo que he aprendido**.
- Si tienes una nota propia en una sección, por ejemplo, una para tu fisioterapeuta en **Citas**, todo lo relacionado con esa persona se incluirá en tu nota.

Las notas de Salud siempre son personales, incluso si una factura llega a tu dirección de correo de trabajo. Tu Machine consulta una vez a su IA por cada factura o dato nuevo que aprende para determinar si está relacionado con tu salud.

## Hijos

En **Hijos**, tu Machine guarda lo que sabe sobre tus hijos: **Escuela**, **Actividades**, **Cuidado infantil**, **Médicos y atención** y **Facturas y tarifas**. Las niñeras y las guarderías se incluyen en Cuidado infantil, nunca en Médicos y atención. Cada sección aparece cuando tiene al menos dos líneas.

- Lo que tu Machine haya aprendido sobre tus hijos, como el nombre de su tutor o el día que tienen natación, aparece en una línea enlazada a su página. Considera que alguien es tu hijo cuando en **Para ti** aparece como hija o hijo.
- Las facturas de la escuela, un club o el cuidado infantil aparecen en una línea que abre su tarea. El importe se queda allí.
- Cada correo de la escuela, un club o el servicio de cuidado infantil, como la circular semanal o un aviso sobre una excursión, aparece en una línea con fecha y asunto, para que todos sus mensajes estén en un mismo lugar. Pulsa la línea para abrir el correo.
- Si tienes una nota propia para uno de tus hijos en una sección, por ejemplo, una para Isla en **Escuela**, todo lo relacionado con ese hijo se incluirá en tu nota.

Las notas de Hijos siempre son personales, incluso si la escuela escribe a tu dirección de correo de trabajo. Tu Machine consulta una vez a su IA por cada dato nuevo para determinar si está relacionado con tus hijos.

## Combinar, eliminar y deshacer

**Combinar en…** en el menú ⋯ mueve las líneas de una nota y las notas que contiene a otra nota. A partir de entonces, tu Machine añadirá los datos nuevos a esa nota. **Eliminar** borra una nota. Ambas acciones muestran **Deshacer** durante unos instantes. También aparece al eliminar una línea.

## No son notas de reuniones

Las notas de reuniones y las notas de una persona o una organización se quedan donde estaban. Las notas de aquí son páginas independientes.
