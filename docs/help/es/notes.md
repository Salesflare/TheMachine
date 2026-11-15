---
title: Notas
area: graph
summary: Una página fácil de leer por tema, como un viaje o tu hogar, enlazada con las personas y los proyectos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, folder_overview.py, memory_seed.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 1087ac0970878932
---
Una nota es un resumen de un tema: un viaje, tu hogar, cómo se gestionan las facturas. Las notas aparecen en Graph junto a People, Organizations y Projects. Se guardan en tu Machine y no se comparten con tu equipo.

## Empezar una nota

Pulsa **Nueva nota** en la parte superior de Notas. Ponle un título y pulsa **Empezar la nota** para abrir su página. **Añadir una línea** añade lo que quieras guardar. Cada línea de texto se convierte en una línea independiente.

## Enlazar personas, proyectos y otras notas

Escribe @ y unas cuantas letras de un nombre en una línea. Elige una persona, organización, proyecto o nota de la lista y su nombre aparecerá como enlace. En la página de lo que hayas enlazado aparecerá **Enlazado desde** con tu nota.

## Notas dentro de otras notas

Una nota puede estar dentro de otra, como Electrodomésticos dentro de Hogar. Notas las muestra en forma de árbol: la flecha junto a una nota abre las que contiene. Para mover una nota, pulsa **Editar** y elige dónde colocarla en **Debajo de**. **Nueva nota debajo de esta**, en el menú ⋯, crea una nota ahí mismo.

En la parte superior de la página de una nota se muestra dónde está, como **Notas › Hijos**. Toca cualquier parte para ir allí. En el móvil, las notas intermedias se ocultan en ⋯.

## Notas que guarda tu Machine

Tu Machine también escribe notas por su cuenta a partir de tus mensajes y las mantiene actualizadas. Cada línea indica de dónde viene, por ejemplo, quién envió el correo: tócala para abrir el mensaje. Una línea de **Lo que he aprendido** indica **De lo que aprendí**.

Las reuniones y citas de tu calendario nunca aparecen como una línea independiente: se quedan en [Calendario](calendar.md). Lo mismo ocurre con sus correos: la invitación, las respuestas, las actualizaciones y las cancelaciones.

**Hogar**, **Salud** y **Hijos** solo aparecen cuando tu Machine tiene al menos dos cosas concretas que decir sobre ellos, como una factura o algo que haya aprendido. Hasta entonces, no aparecen en la lista. Si vuelven a quedarse sin contenido, desaparecen.

Tus cambios siempre se mantienen. Cambia el nombre de una nota, muévela, cambia sus fechas o una línea, y tu Machine la mantendrá así cuando la actualice. Si eliminas una línea o una nota, no volverá a aparecer. Las notas que se creen más adelante sobre el mismo tema irán donde pusiste la primera.

**Volver al original** muestra de nuevo las palabras originales de tu Machine. Si editas una línea que viene de algo que tu Machine aprendió, también cambiará en **Lo que he aprendido**, para que solo haya una versión.

## Páginas redactadas

Cuando una nota tiene al menos dos líneas de tus mensajes o de algo que tu Machine haya aprendido, tu Machine redacta su página en la parte superior. Lee las conversaciones, no solo sus asuntos:

- Un breve resumen: de qué trata y en qué estado está.
- **Datos clave**, **Decisiones**, **Temas pendientes** y una **Cronología**, solo cuando hay algo concreto que decir.
- Después aparecen las líneas de la nota, numeradas, en **Fuentes**. Cada frase termina con los números de las líneas de las que procede: toca un número para ir a esa línea.

La página solo se vuelve a redactar cuando cambian las líneas de la nota, como máximo una vez al día. Si las fuentes no dicen nada concreto, no hay página, solo las líneas. Si eliminas una línea, también desaparece de la página lo que procedía únicamente de ella. La lista de Notas muestra el comienzo del resumen de cada página debajo del nombre de la nota.

Los proyectos y las organizaciones ya tienen su propia página en Graph, con su descripción en la parte superior. Las conversaciones sobre ellos van en esa página, no en una nota.

## Resúmenes

Una nota que contiene otras notas, como **Trabajo** o **Hogar**, muestra un breve resumen en la parte superior cuando al menos dos de ellas tienen novedades: una o dos frases sobre lo que pasa y algunas cosas que han cambiado hace poco o que están por venir. Al final de cada una aparecen los nombres de las notas de las que procede: toca uno para abrir esa nota.

El resumen se prepara a partir de las páginas y las líneas más recientes de las notas que contiene, como máximo una vez al día y solo si han cambiado. Si no hay novedades, no se muestra ningún resumen. La lista de Notas muestra el comienzo del resumen debajo del nombre de la carpeta.

## Notas de tus conversaciones

Tu Machine lee las conversaciones completas y clasifica cada una en la nota correspondiente: un hilo de correo de cualquiera de tus buzones, un chat de WhatsApp, Slack, Telegram, LinkedIn u otra app conectada, y tus notas de reuniones. Los mensajes de chat cuentan como una sola conversación hasta que el chat lleva dos días sin actividad.

- Una conversación sobre un proyecto o una organización de tu Graph va en su página, no en una nota nueva.
- Una conversación puede ir en una sección de **Hogar**, **Salud** o **Hijos**, en una nota tuya o en una nota que tu Machine cree dentro de **Trabajo**, **Coche**, **Impuestos** u otra carpeta.
- Tu Machine solo crea una nota nueva para un tema del que haya al menos dos conversaciones o sobre el que hayas escrito algo que claramente sigue en curso.
- Cada línea corresponde a una conversación, empezando por la más reciente. Tócala para abrir la conversación.

Tu Machine envía a la IA un fragmento breve de cada conversación, sin las respuestas citadas ni las firmas. La IA analiza cada conversación una vez y, después, también tiene en cuenta los mensajes nuevos que lleguen a ella.

Los correos masivos y los chats nunca se incluyen en una nota ni se envían a la IA: spam, promociones, boletines y otros correos de listas, notificaciones de direcciones sin respuesta, bots y canales de difusión. Las conversaciones en las que hayas escrito sí cuentan, al igual que los correos de reservas de **Viajes** y **Eventos**.

La primera vez, tu Machine revisa los últimos tres meses en unas horas, fuera del horario nocturno y solo mientras tu plan de IA tenga capacidad. Después, clasifica las conversaciones nuevas cuando haya diez pendientes o una lleve medio día esperando.

## Notas de la memoria de OpenClaw

Si ya usabas OpenClaw, tu Machine lee una sola vez las páginas temáticas de su carpeta de memoria, como una página sobre un viaje o tu salud. Lo que siga siendo relevante se guarda en la nota sobre ese tema o en una nueva. Cada línea indica de qué página procede, por ejemplo, **De tus páginas de memoria · Lisboa**, junto con la fecha. Pasa el cursor por encima para ver dónde está esa página.

Tu Machine nunca cambia esas páginas y omite los registros diarios, las páginas sobre la propia asistente y las carpetas marcadas como sensibles o privadas. Lee como máximo 80 páginas, de unas pocas en unas pocas, y no vuelve a leerlas.

## Viajes

Cuando llega a tu correo una reserva de vuelo, hotel, tren, autobús, ferry o coche de alquiler, tu Machine la añade a un viaje dentro de **Viajes**. Las reservas de un mismo trayecto van en un solo viaje: la ida, el hotel y la vuelta. El viaje incluye el código de reserva, el asiento y el billete de cada línea, en orden cronológico, y muestra sus fechas. En [Calendario](calendar.md) aparece como una franja que abarca esos días y que abre el viaje.

Tu Machine lee los datos de la reserva que las aerolíneas, los hoteles y las páginas de reservas incluyen en sus correos de confirmación. Si un correo no los incluye, no se crea ningún viaje. Los correos de reservas anteriores, dentro del año de [historial](history.md) que conserva tu Machine, se leen en segundo plano una vez que se haya cargado ese historial, empezando por tus buzones personales. Si se lee más adelante una confirmación antigua, se añade al viaje que ya existe.

Si cambia una reserva, se actualiza su línea. Si se cancela, se elimina. Cuando se cancelan todas las reservas de un viaje, también se elimina el viaje.

## Eventos

Cuando recibes por correo entradas para un concierto, un partido, un festival o una conferencia, tu Machine añade el evento a **Eventos**, en una nota por evento. Una línea indica dónde es e incluye el código de reserva, el asiento y el número de entradas. Si haces otro pedido para el mismo evento, se añade a la misma nota. Al igual que un viaje, el evento muestra sus fechas y aparece como una franja en [Calendario](calendar.md) que abre la nota.

- Cada línea indica quién envió las entradas, por ejemplo, **De Example Tickets**, y abre ese correo.
- Si del correo de las entradas se creó una tarea, como pagar las entradas, **Abrir la tarea** la muestra.
- Si reservaste el evento desde tu buzón del trabajo, es de Trabajo. En caso contrario, es Personal.

Tu Machine lee los datos de las entradas que los vendedores incluyen en sus correos de confirmación, sin usar la IA. Si un correo no los incluye, no se crea ningún evento. Si se cancela una reserva, se elimina. Cuando se cancelan todas las entradas de un evento, también se elimina el evento.

## Hogar

En **Hogar**, tu Machine guarda lo que sabe sobre tu hogar: **Facturas y suscripciones**, **Electrodomésticos**, **Reparaciones y mantenimiento** y **Hogar**. Una sección aparece cuando tiene al menos dos líneas.

- Las facturas periódicas, como las de electricidad o agua, tienen una línea que indica cada cuánto llegan y la fecha de la última. **Abrir la tarea** muestra la factura. El importe y los datos de pago se quedan ahí.
- Las suscripciones que conserves tienen una línea que abre su tarea de **Suscripciones**. Las canceladas no aparecen.
- Las personas y entidades que te escriben con frecuencia sobre tu hogar, como la compañía eléctrica, el proveedor de internet o el ayuntamiento, tienen una línea que indica cada cuánto te escriben. Tócala para abrir el correo más reciente.
- Lo que tu Machine haya aprendido sobre tu hogar, como la marca del lavavajillas, también aparece en una línea. Si la editas, también cambiará en **Lo que he aprendido**.
- Si tienes una nota propia en una sección, como una sobre tu lavavajillas en **Electrodomésticos**, lo relacionado con ese electrodoméstico irá en tu nota. Tu Machine no crea notas de ese tipo por su cuenta.

Solo se usan las facturas, suscripciones y los correos personales, y las notas de Hogar siempre son personales. Tu Machine pregunta una vez a su IA por cada nueva factura, suscripción o cosa que haya aprendido, para saber si tiene que ver con tu hogar. En el caso de una factura, le envía quién la ha enviado, nunca el importe.

Tus conversaciones también se incluyen en estas notas, como se explica arriba en **Notas de tus conversaciones**.

## Salud

En **Salud**, tu Machine guarda lo que sabe sobre tu salud: **Citas**, **Resultados de las pruebas**, **Médicos y atención**, **Medicamentos**, **Alergias y afecciones** y **Facturas y seguro**. Una sección aparece cuando tiene al menos dos líneas.

- Las facturas de un médico, dentista o farmacia tienen una línea que abre su tarea. El importe se queda ahí.
- Cada correo de tu consulta, un hospital, un laboratorio o tu aseguradora médica aparece como una línea fechada con su asunto, para que tu historial vaya creciendo con el tiempo. Tócala para abrir el correo.
- Lo que tu Machine haya aprendido sobre tu salud, como una alergia, también aparece en una línea. Si la editas, también cambiará en **Lo que he aprendido**.
- Si tienes una nota propia en una sección, como una sobre tu fisioterapeuta en **Citas**, lo relacionado con esa persona irá en tu nota.

Las notas de Salud siempre son personales, aunque la factura haya llegado a tu dirección de trabajo. Tu Machine pregunta una vez a su IA por cada nueva factura o cosa que haya aprendido, para saber si tiene que ver con tu salud.

## Hijos

En **Hijos**, tu Machine guarda lo que sabe sobre tus hijos: **Escuela**, **Actividades**, **Cuidado infantil**, **Médicos y atención** y **Facturas y tarifas**. Las niñeras y las guarderías van en Cuidado infantil, nunca en Médicos y atención. Una sección aparece cuando tiene al menos dos líneas.

- Lo que tu Machine haya aprendido sobre tus hijos, como quién es su tutor o qué día tienen natación, aparece en una línea enlazada a su página. Considera que alguien es tu hijo cuando en **Para ti** indica ese parentesco, como hija o hijo.
- Las facturas de la escuela, un club o el cuidado infantil tienen una línea que abre su tarea. El importe se queda ahí.
- Cada correo de la escuela, un club o el servicio de cuidado infantil, como una nota sobre una excursión o un cambio de planes, aparece en una línea fechada con su asunto, para que todos esos correos estén en un mismo lugar. Tócala para abrir el correo.
- Si tienes una nota propia para uno de tus hijos en una sección, como una para Isla en **Escuela**, lo relacionado con ese hijo irá en tu nota.

Las notas de Hijos siempre son personales, aunque la escuela escriba a tu dirección de trabajo. Tu Machine pregunta una vez a su IA por cada novedad, para saber si tiene que ver con tus hijos.

## Combinar, eliminar y deshacer

**Combinar en…**, en el menú ⋯, mueve las líneas de una nota y las notas que contiene a otra nota. A partir de entonces, tu Machine añadirá el contenido nuevo a esa nota. **Eliminar** borra una nota. Ambas acciones muestran **Deshacer** durante un momento. Lo mismo ocurre al eliminar una línea.

## No son lo mismo que las notas de reuniones

Las notas de reuniones y las notas sobre una persona u organización se quedan donde estaban. Las notas de aquí son páginas independientes.
