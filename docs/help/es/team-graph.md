---
title: Graph del equipo
area: fleet
summary: Experimental. Comparte el trabajo con clientes con tu Fleet de trabajo, como en un CRM. Descubre qué se comparte, qué nunca se comparte y cómo mantener algo en privado.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
En un Fleet de trabajo, tu Machine puede compartir el trabajo con clientes con las Machine de tus compañeros, como en un CRM compartido. Es **Experimental** y viene desactivado.

## Activarlo

Un administrador activa **Compartir el Graph en este Fleet** en **Qué se comparte** y confirma que la empresa puede compartir este correo y que se lo ha comunicado a sus empleados. Todo el mundo puede ver si está activado.

Si se exige el correo o el calendario de trabajo de todos, también se activa. Después, cada persona elige qué más comparte en **Tus conexiones**. El primer contenido compartido de un nuevo compañero espera una hora, para que pueda mantenerlo en privado antes.

## Tus conexiones

**Tus conexiones** en **Qué se comparte** muestra cada conexión con un interruptor. Las de trabajo con el dominio de tu Fleet se activan de forma predeterminada. Las de dominios de otras empresas se desactivan de forma predeterminada y muestran «Otra empresa, no compartido». Las personales nunca se comparten. Si desactivas una conexión, se retira lo que se compartió desde ella.

El calendario de otra persona que consultas con tu propio inicio de sesión aparece con su propio nombre, como personal.

Dentro de una conexión activada, cada hilo se clasifica por separado. El Slack de tu empresa solo cuenta como comunicación entre compañeros. Un chat de Slack Connect con otra empresa sí puede ser trabajo con clientes. Los hilos personales, entre compañeros, sensibles y automatizados no se comparten, a menos que compartas uno por tu cuenta.

## Obligatorio en el Fleet

Un administrador puede exigir el **Correo de trabajo** y el **Calendario de trabajo** de todos en el dominio del Fleet, en **Obligatorio en el Fleet**, tras confirmar que la empresa se lo ha comunicado a sus empleados. El correo de trabajo pertenece a la empresa, como en cualquier CRM. Las conexiones obligatorias muestran «Obligatorio en» y el nombre de tu Fleet, y no se pueden desactivar. Los hilos que mantienes en privado siguen siendo privados.

## Qué se comparte con el equipo

- Hilos con clientes: correo de trabajo con personas ajenas a tu empresa, incluidos los archivos adjuntos.
- Personas, organizaciones y proyectos de trabajo, con una cronología breve. En la **Cronología** de una página, **Equipo** muestra cada evento una sola vez, en el idioma en que lo escribió la Machine de un compañero, junto con las personas de las que procede: «vía Sam, Kim y Lee».
- Una copia pequeña del logotipo de una organización y de la foto de trabajo de una persona, obtenida de una búsqueda, Slack, LinkedIn, X, Salesflare o Microsoft. Nunca se comparte una imagen de contactos de Google, WhatsApp, Telegram o Facebook, ni una imagen que hayas cambiado o quitado.
- En un tablero de Equipo, las reuniones de un proyecto, las notas de Zoom, las conversaciones de Intercom y los chats. Los elementos sensibles, como los tratos, y los chats solo entre compañeros no se comparten.
- Recuentos y fechas del [resumen de equipo](fleet.md#brief-requests) de un compañero.
- Respuestas cuando un compañero pregunta quién conoce a alguien o quiere contexto sobre una reunión. Consulta [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Aprendizajes del equipo](fleet.md#team-learnings): cómo trabaja el equipo, sin nombres ni datos de clientes.

## Lo que no se comparte automáticamente

- Hilos sensibles: compra o venta de empresas, inversiones, negociaciones de tratos, RR. HH. y contratación, temas legales, salud, dinero y seguridad. Ni siquiera se comparte que existen.
- Correo automatizado: recibos, facturas, alertas, boletines y facturas de proveedores.
- Hilos solo entre compañeros, correo personal y cualquier contenido de una cuenta personal. El contenido personal nunca se comparte, ni siquiera si tocas **Equipo**.
- Todo lo que marcaste como **Mantener en privado**, y los tableros y proyectos configurados como **Solo tú**.
- Personas que son personales para ti, como tu familia o tus amigos, y su correo. Un proyecto en el que participen se comparte con su tablero, pero sin incluirlos.

Cada hilo se clasifica según su contenido, y la clasificación puede ser incorrecta. Revisa qué se compartiría y usa «Mantener en privado» para corregirlo. Si compartes un hilo por tu cuenta con el equipo o con personas específicas, se anula la etiqueta de contenido sensible. Revisa quién podrá verlo.

## Compartir un tablero con las personas que elijas

En el menú **⋯** de un tablero, toca **Compartir tablero…** y elige a tus compañeros. Solo ellos reciben sus proyectos con las cronologías completas: correo, reuniones y notas de Zoom, conversaciones de Intercom, chats, tareas y cambios. También se comparten los elementos sensibles, como los tratos.

Los hilos personales y solo entre compañeros no se comparten. Tampoco se comparten tu familia y tus amigos, el correo automatizado ni las conexiones que no seleccionaste.

- También se comparte cualquier proyecto que se añada al tablero más adelante. Si se quita del tablero, se retira.
- Si quitas a alguien o no eliges a nadie, el contenido se retira de su Machine.
- Para compartir un hilo con personas específicas, toca su etiqueta y luego **Compartir con…**. Puede incluir correo de trabajo sensible o automatizado, pero nunca hilos personales ni solo entre compañeros.

## ¿No estás seguro? Espera

Si tu Machine no está segura, no comparte el contenido. Esos hilos esperan en **¿Compartir esto?**, agrupados por tipo (por ejemplo, «Intercambios con socios y anuncios»), y cada grupo incluye una sugerencia:

- **Compartir con el equipo**: con todos los miembros del Fleet.
- **Compartir con…**: solo con los compañeros que elijas, como un miembro del tablero para hablar de inversiones.
- **Mantener en privado**: solo tú podrás verlo.

Con un solo toque decides qué hacer con todo un grupo. Abre un grupo para desmarcar los hilos que quieras decidir uno por uno.

Las conversaciones sobre comprar, vender o invertir en una empresa, y los asuntos de juntas directivas, son sensibles, así que no esperan aquí. El trabajo habitual con una empresa asociada cuenta como trabajo con clientes.

## Antes de compartir por primera vez

Tu primer contenido se comparte automáticamente una hora después de que tu Machine te avise. Durante esa hora, abre **Fleet** y luego **Qué se comparte** para ver, por organización, los hilos con clientes que se compartirían. Toca **Mantener en privado** en los que quieras excluir o **Compartir ahora** para compartirlos de inmediato. Los administradores pueden ver quién aún no ha compartido.

## Qué se comparte

**Fleet** › **Qué se comparte** muestra todo: recuentos por tipo, cada hilo compartido y el motivo, los que están en **¿Compartir esto?** y lo que mantienes en privado. Toca un asunto para leerlo. **Ajustes** y la etiqueta de cada hilo también llevan aquí.

Los hilos nuevos con clientes esperan una hora antes de compartirse, para que tengas tiempo de cambiar de opinión.

## Dejar de compartir

Toca la etiqueta **Equipo** de un hilo y luego **Dejar de compartir**. La Machine de cada compañero elimina el hilo, sus archivos adjuntos y las entradas de su cronología, o lo hace cuando vuelve a estar conectada. Es posible que alguien ya lo haya leído.

Si tocas **Mantener en privado** en una persona, organización o proyecto, dejas de compartir todo su contenido.

Si mantienes en privado dos hilos de la misma empresa, tu Machine te preguntará una vez si quieres mantener siempre en privado el contenido de esa empresa.

## Quién puede verlo

Solo las Machine de tus compañeros. El contenido está cifrado de extremo a extremo. The Machine Network lo transmite, pero no puede leerlo.

## Incorporación y dispositivos nuevos

Un administrador da acceso a cada persona una sola vez. La solicitud aparece en **Tareas** para todos los administradores, y cuenta la primera respuesta. Después, ya no hace falta aprobación para compartir.

Hasta entonces, el Graph y el Fleet de la persona nueva indican qué administradores deben aprobar su acceso. **Míos** y **Equipo** aparecen unos segundos después de la aprobación, sin tener que volver a cargar la página.

Una nueva Machine de alguien que ya tiene acceso recibe el Graph del equipo al cabo de 24 horas. Mientras tanto, los administradores pueden tocar **No es suyo** para excluirlo.

## Cuando alguien se va

Desde ese momento, no recibe nada nuevo. Lo que ya compartió permanece con el equipo. Un administrador también puede **Sacar** a alguien y **Volver a compartir** más adelante.

## Desactivarlo para todos

Un administrador desactiva **Compartir el Graph en este Fleet** en **Qué se comparte**. No se comparte nada nuevo.

**Desactivar** conserva lo que los compañeros ya tienen. **Desactivar y quitar los datos compartidos** hace que todas las Machine lo eliminen. Cuando se vuelve a activar el uso compartido, cada persona revisa el contenido de nuevo antes de compartirlo.

## Dejar de compartir tu trabajo

Desactiva tus conexiones en **Tus conexiones**, a menos que el Fleet las exija. Se retira lo que se compartió desde ellas.

Consulta también [Fleets](fleet.md) y [Seguridad y privacidad](security-and-privacy.md).
