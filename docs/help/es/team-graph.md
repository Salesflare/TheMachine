---
title: Graph del equipo
area: fleet
summary: Experimental. Comparte el trabajo con clientes con tu Fleet de trabajo, como en un CRM. Qué se comparte, qué nunca se comparte y cómo mantener algo en privado.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: 9788be6d2d5e3fa6
---
En un Fleet de trabajo, tu Machine puede compartir el trabajo con clientes con las Machines de tus compañeros, como en un CRM compartido. Es **Experimental** y está desactivado de forma predeterminada.

## Activarlo

Un administrador activa **Compartir el Graph en este Fleet** en **Qué se comparte** y confirma que la empresa puede compartir este correo y que ha informado a sus empleados. Todo el mundo puede ver si está activado.

Si se hace obligatorio el correo o el calendario de trabajo de todo el mundo, también se activa. Después, cada persona elige qué más comparte en **Tus conexiones**. El primer contenido que comparte un nuevo compañero espera una hora, para que pueda mantenerlo en privado primero.

## Tus conexiones

**Tus conexiones** en **Qué se comparte** muestra cada conexión con un interruptor. Las de trabajo del dominio de tu Fleet están activadas de forma predeterminada. Las de dominios de otras empresas están desactivadas y muestran «Otra empresa, no se comparte». Las personales nunca se comparten. Al desactivar una conexión, se retira lo que se había compartido.

El calendario de otra persona que consultas con tu propia cuenta aparece con su propio nombre, como personal.

Dentro de una conexión activada, cada hilo se clasifica por separado. El Slack de tu empresa cuenta solo como comunicación entre compañeros. Solo los chats de Slack Connect con otra empresa pueden ser trabajo con clientes. Los hilos personales, solo entre compañeros, sensibles y automatizados no se comparten, a menos que los compartas tú.

## Obligatorio en el Fleet

Un administrador puede hacer obligatorio el **Correo de trabajo** y el **Calendario de trabajo** de todo el mundo en el dominio del Fleet, en **Obligatorio en el Fleet**, después de confirmar que la empresa ha informado a sus empleados. El correo de trabajo pertenece a la empresa, como en cualquier CRM. Las conexiones obligatorias muestran «Obligatorio en» seguido del nombre de tu Fleet y no se pueden desactivar. Los hilos que mantengas en privado seguirán siendo privados.

## Qué se comparte con el equipo

- Hilos con clientes: correos de trabajo con personas ajenas a tu empresa, incluidos los archivos adjuntos.
- Personas, organizaciones y proyectos de trabajo, con una cronología breve. En la **Cronología** de una página, **Equipo** muestra cada evento una sola vez, en tu idioma si la Machine de un compañero lo escribió así, y con todas las personas de quienes procede: «a través de Sam, Kim y Lee».
- Una copia pequeña del logotipo de una organización y de la foto de trabajo de una persona, obtenida de una búsqueda, Slack, LinkedIn, X, Salesflare o Microsoft. Nunca se comparte una foto de Google Contacts, WhatsApp, Telegram o Facebook, ni una foto que hayas cambiado o eliminado.
- En un tablero del equipo, las reuniones de un proyecto, las notas de Zoom, las conversaciones de Intercom y los chats. Los contenidos sensibles, como las negociaciones, y los chats solo entre compañeros no se comparten.
- El número y las fechas de las [fichas de equipo](fleet.md#brief-requests) de un compañero.
- Las respuestas cuando un compañero pregunta quién conoce a alguien o busca contexto para una reunión. Consulta [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Aprendizajes del equipo](fleet.md#team-learnings): cómo trabaja el equipo, sin nombres ni datos de clientes.

## Qué no se comparte automáticamente

- Hilos sensibles: compra o venta de una empresa, inversiones, negociaciones, recursos humanos y contratación, asuntos legales, salud, dinero y seguridad. Ni siquiera se comparte que existen.
- Correos automatizados: recibos, facturas, alertas, boletines y facturas de proveedores.
- Hilos solo entre compañeros, correos personales y cualquier contenido de una cuenta personal. El contenido personal nunca se comparte, ni siquiera al tocar **Equipo**.
- Todo lo que hayas marcado como **Mantener en privado**, y los tableros y proyectos configurados como «Solo tú».
- Alguien que sea una persona personal para ti, como parte de tu familia o tus amigos, y sus correos. Si participa en un proyecto, este se comparte con su tablero, pero sin incluir a esa persona.

Cada hilo se clasifica según su contenido, y la clasificación puede ser incorrecta. Comprueba qué se compartiría y usa «Mantener en privado» para corregirlo. Si compartes un hilo con el equipo o con personas concretas, se ignora su etiqueta de contenido sensible. Comprueba quién tendrá acceso.

## Compartir un tablero con personas concretas

En el menú **⋯** de un tablero, toca **Compartir tablero…** y elige a tus compañeros. Solo ellos recibirán los proyectos del tablero con sus cronologías completas: correos, reuniones y notas de Zoom, conversaciones de Intercom, chats, tareas y cambios. También se compartirán los contenidos sensibles, como las negociaciones.

Los hilos personales y los que son solo entre compañeros seguirán sin compartirse. Lo mismo ocurre con tu familia y tus amigos, los correos automatizados y las conexiones que no hayas seleccionado.

- Los proyectos que añadas al tablero más adelante también se compartirán. Si quitas uno, dejará de compartirse.
- Si quitas a alguien o no eliges a nadie, el contenido se retirará de su Machine.
- Para compartir un hilo con personas concretas, toca su etiqueta y después **Compartir con…**. Puedes compartir correos de trabajo sensibles o automatizados, pero nunca hilos personales ni solo entre compañeros.

## ¿No lo tienes claro? Espera

Si tu Machine no está segura, no comparte el contenido. Esos hilos esperan en **¿Compartir esto?**, agrupados por tipo, por ejemplo, «Intercambios con socios y anuncios», y cada grupo incluye una sugerencia:

- **Compartir con el equipo**: con todo el mundo en el Fleet.
- **Compartir con…**: solo con los compañeros que elijas, como un miembro del tablero para hablar de inversores.
- **Mantener en privado**: el contenido se queda contigo.

Con un solo toque decides qué hacer con todo un grupo. Abre el grupo para desmarcar los hilos que quieras decidir uno por uno.

Las conversaciones sobre la compra, venta o inversión en una empresa, y los asuntos del consejo, son sensibles y no aparecen aquí. El trabajo habitual con una empresa socia cuenta como trabajo con clientes.

## Antes de compartir por primera vez

La primera vez que compartas, el contenido se enviará automáticamente una hora después de que tu Machine te avise. Durante esa hora, abre **Fleet** y después **Qué se comparte** para ver, por organización, los hilos con clientes que se compartirían. Toca **Mantener en privado** en los que quieras excluir o **Compartir ahora** para enviarlos inmediatamente. Los administradores pueden ver quién todavía no ha compartido nada.

## Qué se comparte

**Fleet** › **Qué se comparte** muestra todo: el número de elementos de cada tipo, cada hilo compartido y el motivo por el que se compartió, los que aparecen en **¿Compartir esto?** y lo que mantienes en privado. Toca un asunto para leerlo. También puedes acceder aquí desde **Ajustes** y desde la etiqueta de cada hilo.

Los hilos nuevos con clientes esperan una hora antes de compartirse, para que tengas tiempo de cambiar de opinión. Después, se comparten en un plazo de media hora. Dejar de compartir y marcar como **Mantener en privado** se refleja en el equipo en un máximo de 5 minutos.

## Dejar de compartir

Toca la etiqueta **Equipo** de un hilo y después **Dejar de compartir**. La Machine de cada compañero eliminará el hilo, los archivos adjuntos y las entradas de la cronología, o lo hará cuando vuelva a estar en línea. Puede que alguien ya lo haya leído.

Si marcas a una persona, organización o proyecto como **Mantener en privado**, dejarás de compartir todo su contenido.

Si mantienes en privado dos hilos de la misma empresa, tu Machine te preguntará una vez si quieres mantener siempre en privado todo lo relacionado con esa empresa.

## Quién puede verlo

Solo las Machines de tus compañeros. El contenido está cifrado de extremo a extremo. The Machine Network lo transmite, pero no puede leerlo.

## Incorporar personas y añadir dispositivos

Un administrador da permiso a cada persona una sola vez. La solicitud aparece en **Tareas** de todos los administradores y cuenta la primera respuesta. Después, no hace falta volver a dar permiso para compartir.

Hasta entonces, el Graph y el Fleet de la persona nueva indican qué administradores tienen que responder. **Míos** y **Equipo** aparecen unos segundos después de dar el visto bueno, sin tener que volver a cargar la página.

Una nueva Machine de alguien que ya forma parte del Fleet recibe el Graph del equipo después de 24 horas. Mientras tanto, los administradores pueden tocar **No es suyo** para impedir que se comparta.

## Cuando alguien se va

Desde ese momento, no recibe contenido nuevo. Lo que haya compartido se queda con el equipo. Un administrador también puede **Sacar** a alguien y **Volver a compartir** más adelante.

## Desactivar el uso compartido para todo el mundo

Un administrador desactiva **Compartir el Graph en este Fleet** en **Qué se comparte**. No se compartirá nada nuevo.

**Desactivar** conserva el contenido que ya tienen los compañeros. **Desactivar y quitar los datos compartidos** hace que todas las Machines lo eliminen. Cuando se vuelve a activar el uso compartido, cada persona revisa el contenido primero.

## Dejar de compartir tu propio trabajo

Desactiva tus conexiones en **Tus conexiones**, a menos que sean obligatorias en el Fleet. Se retirará lo que se había compartido.

Consulta también [Fleets](fleet.md) y [Seguridad y privacidad](security-and-privacy.md).
