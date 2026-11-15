---
title: Notas
area: graph
summary: Una página fácil de leer por tema, como un viaje o tu hogar, enlazada con las personas y los proyectos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a71c5e46042cddd0
---
Una nota es el resumen de un tema: un viaje, tu hogar o cómo se gestionan las facturas. Las notas aparecen en Graph junto a Personas, Organizaciones y Proyectos. Se guardan en tu Machine y no se comparten con tu equipo.

## Empezar una nota

Pulsa **Nueva nota** en la parte superior de Notas. Ponle un título y pulsa **Empezar la nota** para abrir la página. **Añadir una línea** agrega lo que quieras guardar. Cada línea de texto se convierte en una línea independiente.

## Enlazar personas, proyectos y otras notas

Escribe @ y las primeras letras de un nombre en una línea. Elige una persona, organización, proyecto o nota de la lista para añadir su nombre como enlace. En la página de lo que hayas enlazado aparecerá **Enlazado desde** con tu nota.

## Notas dentro de otras notas

Una nota puede estar dentro de otra, como Electrodomésticos dentro de Hogar. Notas las muestra en forma de árbol: la flecha junto a una nota abre las notas que contiene. Para mover una nota, pulsa **Editar** y elige dónde colocarla en **Debajo de**. **Nueva nota debajo de esta**, en el menú ⋯, crea una nota justo ahí.

En la parte superior de la página de una nota se muestra dónde está, por ejemplo, **Notas › Hijos**. Pulsa cualquier parte para ir allí. En el teléfono, las notas intermedias se agrupan en ⋯.

## Notas que guarda tu Machine

Tu Machine también escribe notas automáticamente a partir de tus mensajes y las mantiene actualizadas. Cada línea indica de dónde viene, por ejemplo, quién envió el correo. Púlsala para abrir el mensaje. Una línea de **Lo que he aprendido** indica **De lo que aprendí**.

Una reunión o cita del calendario nunca aparece como una línea por sí sola: se queda en [Calendario](calendar.md). Lo mismo ocurre con sus correos: la invitación, las respuestas, las actualizaciones y las cancelaciones.

**Hogar**, **Salud** e **Hijos** solo aparecen cuando tu Machine tiene al menos dos cosas concretas que decir, como una factura o algo que haya aprendido. Hasta entonces, no aparecen en la lista. Si vuelven a quedarse sin contenido, desaparecen.

Tus cambios siempre se mantienen. Cambia el nombre de una nota, muévela, cambia sus fechas o modifica una línea, y tu Machine la mantendrá así cuando la actualice. Si eliminas una línea o una nota, no volverá a aparecer. Las notas posteriores sobre el mismo tema irán donde pusiste la primera.

**Volver al original** vuelve a mostrar las palabras originales de tu Machine. Si editas una línea que viene de algo que tu Machine aprendió, también cambiará en **Lo que he aprendido**, para que solo haya una versión.

## Páginas redactadas

Cuando una nota tiene al menos dos líneas de tus mensajes o de cosas que tu Machine ha aprendido, tu Machine escribe el contenido de la página en la parte superior. Lee las conversaciones, no solo sus asuntos:

- Un breve resumen: de qué trata y en qué estado está.
- **Datos clave**, **Decisiones**, **Temas pendientes** y una **Cronología**, solo cuando hay algo concreto que decir.
- Después aparecen las líneas de la nota, numeradas, en **Fuentes**. Al final de cada oración aparecen los números de las líneas en las que se basa. Pulsa uno para ir a esa línea.

La página solo se vuelve a redactar cuando cambian las líneas de la nota, como máximo una vez al día. Si las fuentes no dicen nada concreto, no hay página, solo las líneas. Si eliminas una línea, también desaparece de la página lo que dependía solo de ella. En la lista de Notas se muestra el principio del resumen de cada página, debajo del nombre de la nota.

Los proyectos y las organizaciones ya tienen su propia página en Graph, con su descripción en la parte superior. Las conversaciones sobre ellos van ahí, no en una nota.

## Notas de tus conversaciones

Tu Machine lee las conversaciones completas y las ordena en la nota correspondiente: un hilo de correo de cualquiera de tus buzones, un chat de WhatsApp, Slack, Telegram, LinkedIn u otra aplicación conectada, y tus notas de reuniones. Los mensajes de chat cuentan como una conversación hasta que el chat lleva dos días sin actividad.

- Una conversación sobre un proyecto o una organización de Graph va en esa página, no en una nota nueva.
- Una conversación puede ir en una sección de **Hogar**, **Salud** o **Hijos**, en una nota tuya o en una nota que tu Machine cree dentro de **Trabajo**, **Coche**, **Impuestos** u otra carpeta.
- Tu Machine solo crea una nota nueva para un tema con al menos dos conversaciones o para uno en el que hayas escrito y que claramente siga activo.
- Cada línea corresponde a una conversación, empezando por la más reciente. Al pulsarla, se abre la conversación.

Envía a la IA un fragmento breve de cada conversación, sin respuestas citadas ni firmas. Cada conversación se procesa una sola vez, y los mensajes nuevos se añaden a ella.

Los correos masivos y los chats nunca se incluyen en una nota ni se envían a la IA: correo no deseado, promociones, boletines y otros correos de listas, notificaciones automáticas, bots y canales de difusión. Las conversaciones en las que hayas escrito sí cuentan, al igual que los correos de reservas para **Viajes** y **Eventos**.

La primera vez, procesa los últimos tres meses en unas horas, fuera del horario nocturno y solo si queda espacio en tu plan de IA. Después, organiza las conversaciones nuevas cuando haya diez pendientes o cuando una lleve medio día esperando.

## Viajes

Cuando recibes en tu correo una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje en **Viajes**. Las reservas de un mismo trayecto van en un solo viaje: la ida, el hotel y la vuelta. El viaje incluye el código de reserva, el asiento y el billete de cada línea, por orden cronológico, y muestra las fechas. En [Calendario](calendar.md) aparece como una sola franja que ocupa esos días y, al abrirla, muestra el viaje.

Lee los datos de las reservas que las aerolíneas, los hoteles y los sitios de reservas incluyen en sus correos de confirmación. Un correo sin esos datos no crea un viaje. Los correos de reservas anteriores, dentro del año de [historial](history.md) que conserva tu Machine, se procesan en segundo plano una vez que se ha importado ese historial, empezando por tus buzones Personal. Si más adelante se procesa una confirmación antigua, se añade al viaje que ya existe.

Si cambia una reserva, se actualiza su línea. Si se cancela, se elimina. Cuando se cancelan todas las reservas de un viaje, el viaje también se elimina.

## Eventos

Cuando recibes en tu correo entradas para un concierto, un partido, un festival o una conferencia, tu Machine añade el evento a **Eventos**, con una nota por evento. Una línea indica dónde es e incluye el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade a la misma nota. Al igual que un viaje, el evento muestra sus fechas y aparece como una franja en [Calendario](calendar.md) que abre la nota.

- Cada línea indica quién envió las entradas, por ejemplo, **De Entradas de ejemplo**, y abre ese correo.
- Si el correo de las entradas generó una tarea, como pagar las entradas, **Abrir la tarea** la muestra.
- Un evento reservado desde tu buzón de trabajo es de Trabajo. De lo contrario, es Personal.

Lee los datos de las entradas que los vendedores incluyen en sus correos de confirmación, sin usar IA. Un correo sin esos datos no crea un evento. Si se cancela una reserva, se elimina. Cuando se cancelan todas las entradas de un evento, el evento también se elimina.

## Hogar

En **Hogar**, tu Machine guarda lo que sabe sobre tu hogar: **Facturas y suscripciones**, **Electrodomésticos**, **Reparaciones y mantenimiento** y **Hogar**. Una sección aparece cuando tiene al menos dos líneas.

- Una factura periódica, como la de la energía o el agua, aparece en una línea que indica cada cuánto llega y la fecha de la última. **Abrir la tarea** muestra la factura. El importe y los datos de pago se quedan ahí.
- Una suscripción que mantienes aparece en una línea que abre su tarea de **Suscripciones**. Las canceladas no aparecen.
- Quien se comunica habitualmente con tu hogar, como tu proveedor de energía, tu proveedor de internet o el ayuntamiento, aparece en una línea que indica cada cuánto escribe. Al pulsarla, se abre su correo más reciente.
- Lo que tu Machine ha aprendido sobre tu hogar, como la marca de tu lavavajillas, también aparece en una línea. Si la editas, también cambiará en **Lo que he aprendido**.
- Si tienes una nota propia en una sección, como una sobre tu lavavajillas en **Electrodomésticos**, lo relacionado con ese aparato se añade a tu nota. Tu Machine no crea notas de ese tipo por su cuenta.

Solo se usan las facturas, suscripciones y correos Personales, y las notas de Hogar siempre son Personales. Tu Machine consulta una vez a su IA sobre cada factura, suscripción o cosa nueva que haya aprendido, para determinar si tiene que ver con tu hogar. En el caso de las facturas, envía quién las ha emitido, nunca el importe.

Las conversaciones también aparecen en estas notas, tal como se explica más arriba en **Notas de tus conversaciones**.

## Salud

En **Salud**, tu Machine guarda lo que sabe sobre tu salud: **Citas**, **Resultados de las pruebas**, **Médicos y atención**, **Medicamentos**, **Alergias y afecciones** y **Facturas y seguro**. Una sección aparece cuando tiene al menos dos líneas.

- Una factura de un médico, dentista o farmacia aparece en una línea que abre su tarea. El importe se queda ahí.
- Cada correo de tu consulta, un hospital, un laboratorio o tu aseguradora médica aparece en una línea fechada con su asunto, para que tu historial vaya creciendo con el tiempo. Al pulsarla, se abre el correo.
- Lo que tu Machine ha aprendido sobre tu salud, como una alergia, también aparece en una línea. Si la editas, también cambiará en **Lo que he aprendido**.
- Lo relacionado con una nota tuya en una sección, como una nota sobre tu fisioterapeuta en **Citas**, se añade a esa nota.

Las notas de Salud siempre son Personales, aunque la factura haya llegado a tu dirección de trabajo. Tu Machine consulta una vez a su IA sobre cada factura o cosa nueva que haya aprendido, para determinar si tiene que ver con tu salud.

## Hijos

En **Hijos**, tu Machine guarda lo que sabe sobre tus hijos: **Escuela**, **Actividades**, **Cuidado infantil**, **Médicos y atención** y **Facturas y tarifas**. Las niñeras y las guarderías van en Cuidado infantil, nunca en Médicos y atención. Una sección aparece cuando tiene al menos dos líneas.

- Lo que tu Machine ha aprendido sobre tu hijo, como quién es su profesor o qué día tiene natación, aparece en una línea que enlaza con su página. Considera que alguien es tu hijo cuando en **Para ti** dice que lo es, por ejemplo, hija o hijo.
- Una factura de la escuela, una actividad o el cuidado infantil aparece en una línea que abre su tarea. El importe se queda ahí.
- Cada correo de la escuela, una actividad o el servicio de cuidado infantil, como un aviso de una excursión o un cambio de planes, aparece en una línea fechada con su asunto, para que todo lo que envíen esté en un solo lugar. Al pulsarla, se abre el correo.
- Lo relacionado con una nota tuya sobre uno de tus hijos en una sección, como una nota sobre Isla en **Escuela**, se añade a esa nota.

Las notas de Hijos siempre son Personales, aunque la escuela escriba a tu dirección de trabajo. Tu Machine consulta una vez a su IA sobre cada cosa nueva para determinar si tiene que ver con tus hijos.

## Combinar, eliminar y deshacer

**Combinar en…**, en el menú ⋯, mueve las líneas de una nota y las notas que contiene a otra nota. A partir de entonces, tu Machine añadirá contenido a esa nota. **Eliminar** borra una nota. Ambas acciones muestran **Deshacer** durante un momento, al igual que al eliminar una línea.

## No son lo mismo que las notas de reuniones

Las notas de reuniones y las notas sobre personas u organizaciones se quedan donde estaban. Las notas de aquí son páginas independientes.
