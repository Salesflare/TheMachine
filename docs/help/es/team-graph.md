---
title: Graph del equipo
area: fleet
summary: Experimental. Comparte el trabajo con clientes con tu Fleet de trabajo, como si fuera un CRM. Qué se comparte, qué no y cómo mantener algo en privado.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
En un Fleet de trabajo, tu Machine puede compartir el trabajo con clientes con las Machines de tus compañeros, como si fuera un CRM compartido. Es **Experimental** y está desactivado de forma predeterminada.

## Activarlo

Un administrador activa **Compartir el Graph en este Fleet** en **Qué se comparte** y confirma que la empresa puede compartir este correo y que ha informado a su personal. Todo el mundo puede ver si está activado.

Si se requiere el correo o el calendario de trabajo de todo el mundo, también se activa. Después, cada persona elige qué más compartir en **Tus conexiones**. La primera vez que un nuevo compañero comparte algo, se espera una hora para que pueda decidir qué mantener en privado.

## Tus conexiones

**Tus conexiones** en **Qué se comparte** muestra cada conexión con un interruptor. Las conexiones de trabajo del dominio de tu Fleet están activadas de forma predeterminada. Las de dominios de otras empresas están desactivadas y muestran «Otra empresa, no compartida». Las personales nunca se comparten. Si desactivas una conexión, se retira lo que se había compartido.

Los calendarios de otras personas que consultas con tu propia cuenta aparecen con su nombre, como personales.

Dentro de una conexión activada, cada hilo se clasifica por separado. El Slack de tu empresa solo cuenta como conversaciones con compañeros. Solo un chat de Slack Connect con otra empresa puede ser trabajo con clientes. Los hilos personales, solo con compañeros, sensibles y automatizados no se comparten, a menos que compartas uno tú.

## Obligatorio en el Fleet

Un administrador puede exigir el **Correo de trabajo** y el **Calendario de trabajo** de todas las personas del dominio del Fleet en **Obligatorio en el Fleet**, después de confirmar que la empresa ha informado a su personal. El correo de trabajo pertenece a la empresa, como en cualquier CRM. Las conexiones obligatorias indican «Obligatorio en» tu Fleet y no se pueden desactivar. Los hilos que mantengas en privado seguirán siendo privados.

## Qué se comparte con el equipo

- Hilos con clientes: correos de trabajo con personas ajenas a tu empresa, incluidos los archivos adjuntos.
- Personas, organizaciones y proyectos de trabajo, con una breve cronología. En la **Cronología** de una página, **Equipo** muestra cada evento una sola vez y en tu idioma, si así lo escribió la Machine de un compañero, junto con quién lo compartió: «a través de Sam, Kim y Lee».
- Una copia pequeña del logotipo de una organización y de la foto de trabajo de una persona, obtenida de una búsqueda, Slack, LinkedIn, X, Salesflare o Microsoft. Nunca se comparten imágenes de contactos de Google, WhatsApp, Telegram o Facebook, ni imágenes que hayas cambiado o eliminado.
- En un tablero de **Equipo**, las reuniones, notas de Zoom, conversaciones de Intercom y chats de un proyecto. Los temas sensibles, como las negociaciones, y los chats solo con compañeros no se comparten.
- Recuentos y fechas del [resumen del equipo](fleet.md#brief-requests) de un compañero.
- Respuestas cuando un compañero pregunta quién conoce a alguien o quiere contexto para una reunión. Consulta [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Aprendizajes del equipo](fleet.md#team-learnings): cómo trabaja el equipo, sin nombres ni datos de clientes.

## Qué no se comparte automáticamente

- Hilos sensibles: compra o venta de empresas, inversiones, negociaciones, Recursos Humanos y contratación, temas legales, salud, dinero y seguridad. Ni siquiera se comparte que existan.
- Correos automatizados: recibos, facturas, alertas, boletines y facturas de proveedores.
- Hilos solo con compañeros, correos personales y cualquier contenido de una cuenta personal. El contenido personal nunca se comparte, ni siquiera al tocar Equipo.
- Todo lo que hayas marcado como **Mantener en privado**, así como los tableros y proyectos configurados como «Solo tú».
- Personas que sean personales para ti, como tu familia o tus amigos, y sus correos. Si forman parte de un proyecto, este se comparte con su tablero, pero sin incluirlos.

Cada hilo se clasifica según su contenido, y puede que la clasificación no sea correcta. Comprueba qué se compartiría y usa Mantener en privado para corregirlo. Si compartes un hilo tú misma con el equipo o con personas concretas, se ignora la etiqueta de sensible. Comprueba quién podrá verlo.

## Compartir un tablero con personas concretas

En el menú **⋯** de un tablero, toca **Compartir tablero…** y elige compañeros. Solo ellos recibirán sus proyectos con la cronología completa: correos, reuniones y notas de Zoom, conversaciones de Intercom, chats, tareas y movimientos. También se compartirán los temas sensibles, como las negociaciones.

Los hilos personales y los que solo son con compañeros no se comparten. Tampoco se comparten tu familia y tus amigos, los correos automatizados ni las conexiones que no hayas seleccionado.

- También se comparte cualquier proyecto que se añada al tablero más adelante. Si se quita un proyecto, se retira lo que se había compartido.
- Si quitas a alguien o no eliges a nadie, el contenido se retira de su Machine.
- Para compartir un solo hilo con personas concretas, toca su etiqueta y luego **Compartir con…**. Puedes incluir correos de trabajo sensibles o automatizados, pero nunca hilos personales o solo con compañeros.

## ¿No lo tienes claro? Espera

Si tu Machine no está segura, no comparte el contenido. Esos hilos esperan en **¿Compartir esto?**, agrupados por tipo, por ejemplo, «Intercambios con socios y anuncios», y cada grupo incluye una sugerencia:

- **Compartir con el equipo**: todo el mundo en el Fleet.
- **Compartir con…**: solo los compañeros que elijas, por ejemplo, un miembro del tablero para hablar de inversiones.
- **Mantener en privado**: solo tú podrás verlo.

Con un toque decides qué hacer con todo un grupo. Abre un grupo para desmarcar los hilos que quieras decidir por separado.

Las conversaciones sobre la compra, venta o inversión en una empresa y los asuntos del consejo son sensibles, así que no aparecen aquí. El trabajo cotidiano con una empresa asociada sí cuenta como trabajo con clientes.

## Antes de compartir por primera vez

La primera vez, tu Machine comparte el contenido automáticamente una hora después de avisarte. Durante esa hora, abre **Fleet** y luego **Qué se comparte** para ver los hilos con clientes que se compartirían, organizados por empresa. Toca **Mantener en privado** en los que quieras excluir o **Compartir ahora** para enviarlos al momento. Los administradores pueden ver quién aún no ha compartido nada.

## Qué se comparte

**Fleet** › **Qué se comparte** lo muestra todo: el recuento por tipo, cada hilo compartido y el motivo, los que aparecen en **¿Compartir esto?** y lo que mantienes en privado. Toca un asunto para leerlo. También puedes acceder desde **Ajustes** y desde la etiqueta de cada hilo.

Los hilos nuevos con clientes esperan una hora antes de compartirse, para que tengas tiempo de cambiar de opinión.

## Dejar de compartir

Toca la etiqueta **Equipo** de un hilo y luego **Dejar de compartir**. La Machine de cada compañero elimina el hilo, sus archivos adjuntos y las líneas correspondientes de la cronología, o lo hace cuando vuelve a conectarse. Es posible que alguien ya lo haya leído.

Si marcas como **Mantener en privado** a una persona, organización o proyecto, dejarás de compartir todo su contenido.

Si mantienes en privado dos hilos de la misma empresa, tu Machine te preguntará una sola vez si quieres mantener siempre en privado todo lo relacionado con esa empresa.

## Quién puede verlo

Solo las Machines de tus compañeros. El contenido está cifrado de extremo a extremo. The Machine Network lo transmite, pero no puede leerlo.

## Incorporar a alguien y añadir dispositivos

Un administrador da acceso a cada persona una sola vez. La solicitud aparece en **Tareas** para todos los administradores, y cuenta la primera respuesta. Después, no hace falta más visto bueno para compartir.

Hasta entonces, el Graph y el Fleet de la persona nueva indican qué administradores deben responder. **Míos** y **Equipo** aparecen unos segundos después del visto bueno, sin tener que volver a cargar la página.

Si alguien que ya tiene acceso añade una Machine nueva, recibirá el Graph del equipo al cabo de 24 horas. Mientras tanto, los administradores pueden tocar **No es suyo** para excluirla.

## Cuando alguien se va

Desde ese momento, no recibe nada nuevo. Lo que haya compartido permanece con el equipo. Además, un administrador puede **Sacar** a alguien y **Volver a compartir** el contenido más adelante.

## Desactivar para todo el mundo

Un administrador desactiva **Compartir el Graph en este Fleet** en **Qué se comparte**. No se compartirá nada nuevo.

**Desactivar** conserva lo que ya tienen los compañeros. **Desactivar y quitar los datos compartidos** hace que todas las Machines lo eliminen. Si se vuelve a activar la opción de compartir, cada persona revisará el contenido antes de compartirlo de nuevo.

## Dejar de compartir tu propio trabajo

Desactiva tus conexiones en **Tus conexiones**, a menos que el Fleet las exija. Se retirará lo que se había compartido.

Consulta también [Fleets](fleet.md) y [Seguridad y privacidad](security-and-privacy.md).
