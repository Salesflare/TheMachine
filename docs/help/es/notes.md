---
title: Notas
area: graph
summary: Una página fácil de leer por tema, como un viaje o tu hogar, enlazada con las personas y los proyectos que incluye.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 88cfd4099bf27f38
---
Una nota es el resumen general de un tema: un viaje, tu hogar o cómo se gestionan las facturas. Las notas aparecen en Graph, junto a Personas, Organizaciones y Proyectos. Se guardan en tu Machine y no se comparten con tu equipo.

## Empezar una nota

Toca **Nueva nota** en la parte superior de Notas. Ponle un título y toca **Empezar la nota** para abrir su página. **Añadir una línea** agrega lo que quieras guardar. Cada línea de texto se convierte en una línea independiente.

## Enlazar personas, proyectos y otras notas

Escribe @ y algunas letras de un nombre en una línea. Elige una persona, organización, proyecto o nota de la lista para insertar un enlace con su nombre. En la página de lo que hayas enlazado, verás **Enlazado desde** y el nombre de tu nota.

## Notas dentro de otras notas

Una nota puede estar dentro de otra, como Electrodomésticos dentro de Hogar. Notas las muestra en forma de árbol: la flecha junto a una nota abre las que contiene. Para mover una nota, toca **Editar** y elige dónde colocarla en **Debajo de**. **Nueva nota debajo de esta**, en el menú ⋯, crea una nota justo ahí.

En la parte superior de la página de una nota se muestra dónde está, por ejemplo, **Notas › Hijos**. Toca cualquier parte para ir allí. En el teléfono, las notas intermedias se agrupan en ⋯.

## Notas que guarda tu Machine

Tu Machine también escribe notas por su cuenta a partir de tus mensajes y las mantiene actualizadas. Cada línea indica de dónde viene, por ejemplo, quién envió el correo: tócala para abrir el mensaje. Las líneas que vienen de **Lo que he aprendido** indican **De lo que aprendí**. Las reuniones y las citas de tu calendario nunca aparecen como líneas por sí solas: se quedan en [Calendario](calendar.md).

**Hogar**, **Salud** e **Hijos** solo aparecen cuando tu Machine tiene al menos dos datos concretos que añadir, como una factura o algo que haya aprendido. Hasta entonces, no aparecen en la lista. Si vuelven a quedarse sin datos, desaparecen.

Tus cambios siempre se mantienen. Si cambias el nombre de una nota, la mueves, cambias sus fechas o editas una línea, tu Machine la conserva así cuando la actualiza. Si eliminas una línea o una nota, no vuelve a aparecer. Las notas posteriores sobre el mismo tema se guardan donde hayas puesto la primera.

**Volver al original** muestra de nuevo las palabras de tu Machine. Si editas una línea que proviene de algo que tu Machine aprendió, también cambia en **Lo que he aprendido**, para que haya una sola versión.

## Páginas redactadas

Cuando una nota tiene al menos dos líneas de tus mensajes o de cosas que tu Machine ha aprendido, tu Machine redacta una página en la parte superior. Lee las conversaciones, no solo sus temas:

- Un breve resumen de qué trata y en qué estado está.
- **Datos clave**, **Decisiones**, **Temas pendientes** y una **Cronología**, solo cuando hay algo concreto que decir.
- Debajo aparecen las líneas de la nota, numeradas, en **Fuentes**. Al final de cada frase están los números de las líneas de las que procede: toca un número para ir a esa línea.

La página solo se vuelve a redactar cuando cambian las líneas de la nota, como máximo una vez al día. Si las fuentes no dicen nada concreto, no hay página, solo las líneas. Si eliminas una línea, también desaparece de la página lo que dependía únicamente de ella. En la lista de Notas, debajo del nombre de cada nota, aparece el comienzo del resumen de su página.

Los proyectos y las organizaciones ya tienen su propia página en Graph, con una descripción en la parte superior. Las conversaciones sobre ellos se guardan allí, no en una nota.

## Notas de tus conversaciones

Tu Machine lee las conversaciones completas y guarda cada una en la nota del tema correspondiente: un hilo de correo de cualquiera de tus cuentas, un chat de WhatsApp, Slack, Telegram, LinkedIn u otra aplicación conectada, y tus notas de reuniones. Los mensajes de chat cuentan como una sola conversación hasta que el chat lleva dos días sin actividad.

- Las conversaciones sobre un proyecto o una organización de Graph se guardan en su página, no en una nota nueva.
- Una conversación puede guardarse en una sección de **Hogar**, **Salud** o **Hijos**, en una nota tuya o en una nota que tu Machine cree dentro de **Trabajo**, **Coche**, **Impuestos** u otra carpeta.
- Tu Machine solo crea una nota nueva para un tema que tenga al menos dos conversaciones, o una conversación en la que hayas escrito y que claramente siga en curso.
- Cada línea corresponde a una conversación, empezando por la más reciente. Tócala para abrir la conversación.

Envía a la IA un fragmento breve de cada conversación, sin respuestas citadas ni firmas. Cada conversación se procesa una vez y los mensajes nuevos se añaden a ella.

Los correos masivos y los chats nunca se incluyen en una nota ni se envían a la IA: spam, promociones, boletines y otros correos de listas, notificaciones de direcciones que no admiten respuestas, bots y canales de difusión. Las conversaciones en las que hayas escrito sí cuentan, al igual que los correos de reservas para **Viajes** y **Eventos**.

La primera vez, procesa tus últimos tres meses en unas horas, fuera del horario nocturno y solo si tu plan de IA tiene capacidad disponible. Después, organiza las conversaciones nuevas cuando haya diez pendientes o cuando alguna lleve medio día esperando.

## Viajes

Cuando recibes en tu correo una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje dentro de **Viajes**. Las reservas de un mismo trayecto se agrupan en un solo viaje: la ida, el hotel y la vuelta. En cada línea del viaje aparecen el código de reserva, el asiento y el billete, en orden cronológico, además de las fechas del viaje. En [Calendario](calendar.md), el viaje aparece como una franja que abarca esos días y que abre el viaje.

Tu Machine lee los detalles de la reserva que las aerolíneas, los hoteles y las páginas de reservas incluyen en el correo de confirmación. Si el correo no los incluye, no se crea un viaje. Los correos de reservas anteriores, dentro del año de [historial](history.md) que conserva tu Machine, se procesan en segundo plano una vez que se ha cargado ese historial, empezando por tus cuentas de correo Personal. Si más adelante se procesa una confirmación antigua, se añade al viaje que ya existe.

Si cambias una reserva, se actualiza su línea. Si la cancelas, se elimina. Cuando se cancelan todas las reservas de un viaje, también se elimina el viaje.

## Eventos

Cuando recibes en tu correo entradas para un concierto, un partido, un festival o una conferencia, tu Machine añade el evento a **Eventos**, en una nota por evento. Una línea indica dónde es y muestra el código de reserva, el asiento y la cantidad de entradas. Si haces otro pedido para el mismo evento, se añade a la misma nota. Al igual que un viaje, el evento muestra sus fechas y aparece como una franja en [Calendario](calendar.md) que abre la nota.

- Cada línea indica quién envió las entradas, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si el correo de las entradas generó una tarea, como pagar las entradas, **Abrir la tarea** la muestra.
- Si reservaste el evento con tu cuenta de correo del trabajo, es de Trabajo. De lo contrario, es Personal.

Tu Machine lee los detalles de las entradas que los vendedores incluyen en sus correos de confirmación, sin usar IA. Si el correo no los incluye, no se crea un evento. Si cancelas una reserva, se elimina. Cuando se cancelan todas las entradas de un evento, también se elimina el evento.

## Hogar

En **Hogar**, tu Machine guarda lo que sabe sobre tu casa: **Facturas y suscripciones**, **Electrodomésticos**, **Reparaciones y mantenimiento** y **Hogar**. Una sección aparece cuando tiene al menos dos líneas.

- Las facturas periódicas, como las de la luz o el agua, aparecen en una línea que indica cada cuánto llegan y la fecha de la última. **Abrir la tarea** muestra la factura. El importe y los datos de pago se quedan allí.
- Las suscripciones que conservas aparecen en una línea que abre su tarea de **Suscripciones**. Las que cancelaste no aparecen.
- Las entidades que se ponen en contacto habitualmente con tu hogar, como la compañía de luz, el proveedor de Internet o el ayuntamiento, aparecen en una línea que indica cada cuánto escriben. Tócala para abrir su correo más reciente.
- Lo que tu Machine ha aprendido sobre tu hogar, como la marca de tu lavavajillas, también aparece en una línea. Si la editas, también cambia en **Lo que he aprendido**.
- Si tienes una nota propia en una sección, por ejemplo, una sobre tu lavavajillas en **Electrodomésticos**, lo relacionado con ese aparato se guarda en tu nota. Tu Machine no crea notas de ese tipo por su cuenta.

Solo se usan facturas, suscripciones y correos Personales, y las notas de Hogar siempre son Personales. Tu Machine consulta a su IA una vez por cada factura, suscripción o dato nuevo que haya aprendido, para determinar si tiene que ver con tu hogar. En el caso de las facturas, le envía quién las emitió, nunca el importe.

Las conversaciones también se guardan en estas notas, como se explica más arriba en **Notas de tus conversaciones**.

## Salud

En **Salud**, tu Machine guarda lo que sabe sobre tu salud: **Citas**, **Resultados de las pruebas**, **Médicos y atención**, **Medicamentos**, **Alergias y afecciones** y **Facturas y seguro**. Una sección aparece cuando tiene al menos dos líneas.

- Las facturas de un médico, dentista o farmacia aparecen en una línea que abre su tarea. El importe se queda allí.
- Cada correo de tu consulta médica, un hospital, un laboratorio o tu aseguradora de salud aparece en una línea con fecha y asunto, para que tu historial se vaya completando con el tiempo. Tócala para abrir el correo.
- Lo que tu Machine ha aprendido sobre tu salud, como una alergia, también aparece en una línea. Si la editas, también cambia en **Lo que he aprendido**.
- Si tienes una nota propia en una sección, por ejemplo, una sobre tu fisioterapeuta en **Citas**, lo relacionado con esa persona se guarda en tu nota.

Las notas de Salud siempre son Personales, aunque una factura haya llegado a tu dirección de correo del trabajo. Tu Machine consulta a su IA una vez por cada factura o dato nuevo que haya aprendido, para determinar si tiene que ver con tu salud.

## Hijos

En **Hijos**, tu Machine guarda lo que sabe sobre tus hijos: **Escuela**, **Actividades**, **Cuidado infantil**, **Médicos y atención** y **Facturas y tarifas**. Las niñeras y las guarderías se incluyen en Cuidado infantil, nunca en Médicos y atención. Una sección aparece cuando tiene al menos dos líneas.

- Lo que tu Machine ha aprendido sobre tu hijo, como quién es su tutor o qué día tiene natación, aparece en una línea que enlaza con su página. Considera que alguien es tu hijo cuando en **Para ti** se indica que lo es, por ejemplo, hija o hijo.
- Las facturas de la escuela, un club o el cuidado infantil aparecen en una línea que abre su tarea. El importe se queda allí.
- Cada correo de la escuela, un club o el servicio de cuidado infantil, por ejemplo, una nota sobre una excursión o un cambio de planes, aparece en una línea con fecha y asunto, para que todo lo que te envíen esté en un mismo lugar. Tócala para abrir el correo.
- Si tienes una nota propia para uno de tus hijos en una sección, por ejemplo, una sobre Isla en **Escuela**, lo relacionado con ese hijo se guarda en tu nota.

Las notas de Hijos siempre son Personales, aunque la escuela escriba a tu dirección de correo del trabajo. Tu Machine consulta a su IA una vez por cada dato nuevo para determinar si tiene que ver con tus hijos.

## Combinar, eliminar y deshacer

**Combinar en…**, en el menú ⋯, mueve las líneas de una nota y las notas que contiene a otra nota. A partir de entonces, tu Machine añade la información a esa nota. **Eliminar** borra una nota. Ambas opciones muestran **Deshacer** durante un momento. También aparece al eliminar una línea.

## No son lo mismo que las notas de reuniones

Las notas de reuniones y las notas sobre personas u organizaciones se quedan donde estaban. Las notas de aquí son páginas independientes.
