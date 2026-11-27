---
title: Fleets
area: fleet
summary: Un Fleet de trabajo para tu equipo y un Fleet familiar para casa. Machines que se ayudan entre sí según tus reglas para compartir.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 17927ccd0e4aa40d
---
Un Fleet permite que tu Machine trabaje con las Machines de tu equipo, familia o amigos a través de The Machine Network. Lo que se dicen está cifrado de extremo a extremo y tu Machine responde solo según tus reglas.

## Tipos de Fleet

- **Fleet de trabajo**: tu equipo. Pasa trabajo, pregunta quién conoce a alguien, consigue presentaciones y consulta un resumen del equipo.
- **Fleet familiar**: hasta 6 personas. Cuando todos tienen tiempo, podéis compartir tareas y planes, y hacer preguntas a las Machines de los demás. Es gratis; las Machines alojadas en él tienen un precio familiar. Consulta [Familia](family.md).
- **Amigos**: cualquier persona de The Machine, de una en una. Es gratis. Consulta [Amigos](friends.md).

## La pestaña Fleet

Aparece cuando ya estás en un Fleet, con un panel para cada Fleet, seguido de Amigos, Network, Compartir y Actividad. Los propietarios y administradores también tienen **Gestionar**, y en un Fleet de trabajo que comparte su Graph aparece **Qué se comparte**.

## Coste, cómo salir y cómo crear otro Fleet

Debajo del nombre de cada Fleet, **Lo que cuesta** muestra sus plazas, quién paga tu Machine y, para el propietario, la tarjeta y las facturas del Fleet. **Salir de este Fleet** te permite salir; si eres el propietario, primero tienes que pasárselo a otra persona. **Crear otro Fleet** inicia uno nuevo.

Cada opción abre ese paso de tu cuenta, y si el precio cambia, primero se muestra el importe para que lo confirmes. En una Machine alojada por ti, se abre tu cuenta en una pestaña nueva para que inicies sesión.

## Pregunta a tu Fleet

Pregunta «¿quién conoce a alguien en Acme?» desde la pestaña Fleet, o usa **Preguntar al Fleet** en una organización de [Graph](graph.md). La Machine de cada compañero responde según sus propias reglas para compartir y les pregunta primero cuando así lo indican sus reglas.

Para cualquier otra cosa, usa **Pregunta lo que quieras** en el panel de tu Fleet de trabajo. Cada compañero recibe un borrador de respuesta elaborado a partir de sus propias cuentas de trabajo, y no recibirás nada hasta que lo envíe. El borrador solo tiene en cuenta lo que esa persona escribió o las reuniones a las que asistió. Los correos que solo recibió, como un boletín o un mensaje en copia, aparecen como encontrados, pero no generan ningún borrador.

## Respuestas automáticas en un Fleet de trabajo

En un Fleet de trabajo Estándar, tu Machine responde automáticamente a tres tipos de preguntas de tus compañeros: **quién conoce a alguien**, **contexto de reuniones** («¿quién es este invitado?») y **quién se ocupa de los correos compartidos**. Solo usa lo que el [Graph del equipo](team-graph.md) ya comparte con tu equipo, nunca conversaciones privadas, personales o delicadas. Cada respuesta aparece en la pestaña Fleet, en **Actividad**.

Para detener una respuesta, cambia su ajuste a **Nunca** en **Compartir**. Si una regla está en **Pregúntame primero**, funciona como **Siempre**. Mientras esté desactivado el uso compartido de Graph del equipo, las preguntas sobre quién conoce a alguien y el contexto de reuniones te las harán primero.

Los Fleets de trabajo con reglas estrictas, Amigos y los Fleets familiares siempre te preguntan primero. Las presentaciones, los traspasos y las preguntas gratuitas siguen teniendo sus propias reglas.

## Aprendizajes del equipo

Tu Machine registra cómo trabaja tu equipo a partir de las conversaciones con clientes que Graph del equipo ya comparte, como máximo una vez al día. Por ejemplo: «Las solicitudes de reembolso se responden desde la bandeja de entrada de asistencia con la plantilla de reembolsos». Aparecen en el panel de tu Fleet de trabajo, en **Aprendizajes del equipo**, a la vista de todos los miembros del Fleet, y cada uno queda registrado en **Actividad**. No se pregunta a nadie primero.

- Solo se usan conversaciones en las que haya escrito alguien de tu equipo. Nunca conversaciones privadas, personales o delicadas.
- Solo se incluyen patrones que se repiten con varios clientes: un proceso, una herramienta, un estilo de escritura o quién se ocupa de cada cosa. Nunca información sobre un cliente en concreto, comentarios sobre tu propio producto, nombres, direcciones, números ni citas.
- Se descartan los aprendizajes sobre los que haya dudas.

Tu Machine usa los aprendizajes pertinentes al preparar una tarea de trabajo para esta empresa. Tus propios datos, reglas y habilidades tienen prioridad, y las tareas personales nunca los usan. Si una tarea ha usado un aprendizaje, lo indica, por ejemplo: «Se ha usado un aprendizaje del equipo: los reembolsos se envían desde la bandeja de entrada de asistencia». Pulsa **Quitar** para eliminarlo de todo el Fleet.

Cualquier persona del Fleet puede **Quitar** un aprendizaje: desaparece para todos y no se vuelve a crear. Para evitarlo, desactiva **Ofrecer compartir aprendizajes** en Ajustes, Seguridad. Los Fleets de trabajo con reglas estrictas no reciben aprendizajes.

## Resumen del equipo

Selecciona **Diario** o **Semanal** para **Resumen del equipo** en la pestaña Fleet, dentro de **Compartir**. Tu Machine pide entonces a las Machines de tus compañeros cifras y fechas. Lo que requiera tu atención aparece en Tareas, en Trabajo: un cliente que espera a un compañero, una empresa que lleva dos semanas o más sin actividad, dos personas del equipo escribiendo a los mismos contactos o una reunión compartida.

- Una tarea indica quién debe responder, desde cuándo, qué pidió y qué está en juego, como un proyecto abierto. Si no hay nada concreto que decir, se queda como una línea del resumen, no como una tarea.
- Los enlaces de la empresa y de los compañeros llevan a sus páginas. **Detalles** muestra lo que escribieron (pulsa para leerlo), qué está en juego, quién del equipo está en contacto y sus conversaciones más recientes, solo lo que comparte el [Graph del equipo](team-graph.md).
- Si lo que escribieron solo está en el correo de un compañero, la tarea indica a quién preguntar.
- **Preguntar al equipo** les envía una pregunta sobre el tema con un texto ya preparado. Sus respuestas aparecen en la tarea.
- **No hace falta** la cierra y el resumen aprende. Solo vuelve a aparecer si hay novedades.
- Cuando alguien responde o se encarga del tema, la tarea se cierra automáticamente. Si ya tienes una tarea para esa empresa, la nueva se añade a esa tarea.

## Solicitudes de resumen del equipo

Cada mañana, un compañero que tenga activado el resumen del equipo pide a tu Machine cifras y fechas. En un Fleet de trabajo, tu Machine responde automáticamente con lo que ya comparte el [Graph del equipo](team-graph.md), y no responde mientras esté desactivado el uso compartido de Graph del equipo. Cada respuesta aparece en la pestaña Fleet, en **Actividad**, nunca como tarea ni notificación.

Para detenerlo, desactiva **Compartir mis datos del informe con el equipo** en la pestaña Fleet, dentro de **Compartir**. A partir de entonces, el resumen de tus compañeros indicará que no has respondido.

En un Fleet con reglas estrictas, las solicitudes esperan tu respuesta en la pestaña Fleet, dentro de **Solicitudes de resumen del equipo**: **Compartir una vez**, **Compartir siempre**, **Rechazar** o **Nunca**. No se comparte nada hasta que elijas una opción y las solicitudes sin responder caducan.

## Graph del equipo

En un Fleet de trabajo, se comparte el trabajo con clientes con tu equipo después de que lo revises. Consulta [Graph del equipo](team-graph.md).

## Conexiones compartidas

Un propietario o administrador puede conectar Stripe o Intercom una vez y compartirlo con el equipo desde **Conexiones compartidas**, en la pestaña Fleet. Los compañeros pueden consultarlo, pero no modificarlo, y pueden ver quién lo ha compartido. Solo los administradores pueden modificarlo o dejar de compartirlo. Consulta [Stripe](stripe.md) e [Intercom](intercom.md).

## Qué responde tu Machine

Configúralo para cada Fleet en el panel Compartir. Consulta [Reglas para compartir](sharing-rules.md). **Ajustes** incluye un acceso directo: **Reglas de Fleet**.

## Inicio de sesión de empresa

Permite que tus compañeros se unan con su cuenta de empresa. En un Fleet de trabajo alojado, un propietario o administrador que haya iniciado sesión con Google Workspace o Microsoft 365 puede activar **Inicio de sesión de empresa** en la página Cuenta.

Los compañeros que inicien sesión con el dominio de su empresa verán **Solicitar unirse**, y un propietario o administrador tendrá que **Aprobar** cada solicitud. Las cuentas personales de Gmail y Outlook.com no cuentan.

Si quitas a alguien del Fleet, se cerrará su sesión en todas partes.

Para unirte a un Fleet, crear uno o vincular una Machine en tu propio ordenador, consulta [Planes y facturación](plans-and-billing.md) y [Amigos y la Network](friends.md).

## Para propietarios y administradores

**Gestionar**, en la pestaña Fleet, muestra cada Fleet que administras: sus miembros, sus funciones y las invitaciones. En una Machine alojada, puedes enviar invitaciones, cambiar funciones, quitar a personas y responder a solicitudes para unirse directamente desde ahí. Si un cambio afecta al precio, se abre tu cuenta para que lo confirmes primero. En una Machine alojada por ti, se muestra quién forma parte del Fleet, con un enlace a los ajustes de ese Fleet en tu cuenta, donde puedes gestionar a sus miembros y las invitaciones.

**Ajustes del Fleet**, debajo del nombre de cada Fleet en su panel y en Gestionar, abre los ajustes de ese Fleet en tu cuenta: conexiones compartidas, seguridad, inicio de sesión de empresa, qué Machine responde y estas dos opciones:

- **Eliminados recientemente**: muestra a cada persona eliminada o que se ha ido. «Eliminado, confirmado» significa que su Machine ha borrado los datos de trabajo y que se ha cerrado su sesión en todas partes. Hasta entonces, indica **Pendiente** y el motivo.
- **Actividad**: quién hizo qué y cuándo: invitaciones, incorporaciones, eliminaciones, funciones, Machines alojadas, facturación, conexiones compartidas y aprobaciones. También cada vez que nuestro equipo de asistencia ha consultado el informe de la Machine de un miembro o sus registros. Nunca incluye el contenido de los mensajes. **Descargar CSV** lo exporta. Se conserva durante 12 meses.

**Pregúntame antes de iniciar la Machine de un miembro**, para el propietario: activada, la Machine de un nuevo miembro espera a que des tu visto bueno, incluso en un Fleet gratuito. Desactivada, en un Fleet gratuito se inicia de inmediato y se te avisa. Si la Machine tiene un coste, siempre espera a que confirmes el importe.

Después de **Dejar de compartir**, una conexión compartida muestra «Eliminada, confirmada» cuando todas las Machines hayan perdido el acceso.
