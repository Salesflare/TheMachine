---
title: Fleets
area: fleet
summary: Un Fleet de trabajo para tu equipo y un Fleet familiar para casa. Machines que se ayudan según tus reglas para compartir.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 974bbbb54608efc3
---
Un Fleet permite que tu Machine trabaje con las Machines de tu equipo, familia o amigos a través de The Machine Network. Lo que se comunican está cifrado de extremo a extremo, y tu Machine solo responde según tus reglas.

## Tipos de Fleet

- **Fleet de trabajo**: tu equipo. Pasa tareas, pregunta quién conoce a alguien, consigue presentaciones y recibe un resumen del equipo.
- **Fleet familiar**: hasta 6 personas. Cuando todos tienen tiempo, tareas y planes compartidos. Gratis; las Machines alojadas tienen un precio familiar. Consulta [Familia](family.md).
- **Amigos**: cualquier persona de The Machine, de una en una. Gratis. Consulta [Amigos y la Network](friends.md).

## La pestaña Fleet

Aparece cuando ya estás en un Fleet. Tiene un panel para cada Fleet y, después, Amigos, Network, Compartir y Actividad. Los propietarios y administradores también tienen **Gestionar**, y un Fleet de trabajo que comparte su Graph tiene **Qué se comparte**.

## Lo que cuesta, salir y crear otro Fleet

Debajo del nombre de cada Fleet, **Lo que cuesta** muestra sus plazas, quién paga tu Machine y, para el propietario, la tarjeta y las facturas del Fleet. **Salir de este Fleet** te permite salir; antes, el propietario tiene que pasarle el Fleet a otra persona. **Crear otro Fleet** crea uno nuevo.

Cada opción abre esa sección de tu cuenta, y si cambia el precio, primero se muestra el importe para que lo confirmes. En una Machine autoalojada, se abre tu cuenta en una pestaña nueva para que inicies sesión.

## Pregunta a tu Fleet

Pregunta «¿quién conoce a alguien en Acme?» desde la pestaña Fleet, o selecciona **Preguntar al Fleet** en una organización de [Graph](graph.md). La Machine de cada compañero responde según sus propias reglas para compartir y le pregunta antes si así lo indica la regla.

Para cualquier otra cosa, usa **Pregunta lo que quieras** en el panel de tu Fleet de trabajo. Cada compañero recibe un borrador de respuesta basado en sus propias cuentas de trabajo, y no se comparte nada hasta que lo envíe.

## Respuestas automáticas en un Fleet de trabajo

En un Fleet de trabajo Estándar, tu Machine responde automáticamente a tres tipos de preguntas de tus compañeros: **quién conoce a alguien**, **contexto de reuniones** («¿quién es este invitado?») y **quién se ocupa de los correos compartidos**. Solo usa lo que el [Graph del equipo](team-graph.md) ya comparte con tu equipo, nunca conversaciones privadas, personales o sensibles. Cada respuesta aparece en la pestaña Fleet, en **Actividad**.

Para detener una opción, configúrala como **Nunca** en **Compartir**. Una regla guardada como **Pregúntame primero** funciona como **Siempre**. Mientras compartir el Graph del equipo esté desactivado, te preguntará antes quién conoce a alguien y el contexto de reuniones.

Los Fleets de trabajo Prudentes, Amigos y Familia siguen preguntándote primero. Las presentaciones cercanas, los traspasos y las preguntas libres siguen teniendo sus propias reglas.

## Aprendizajes del equipo

Tu Machine anota cómo trabaja tu equipo a partir de conversaciones con clientes que el Graph del equipo ya comparte, como máximo una vez al día. Por ejemplo: «Las solicitudes de reembolso se responden desde la bandeja de entrada de soporte con la plantilla de reembolso». Aparecen en el panel de tu Fleet de trabajo, en **Aprendizajes del equipo**, para todos los miembros del Fleet. Cada uno queda registrado en **Actividad**. No se pregunta antes a nadie.

- Solo se usan conversaciones en las que haya escrito alguien de tu equipo. Nunca conversaciones privadas, personales o sensibles.
- Solo se incluyen cosas que se repiten con varios clientes: un proceso, una herramienta, un estilo de escritura o quién se ocupa de cada cosa. Nunca algo sobre un solo cliente, comentarios sobre tu propio producto, ni nombres, direcciones, números o citas.
- Se descartan los aprendizajes sobre los que no haya seguridad.

Tu Machine usa los aprendizajes pertinentes cuando prepara una tarea de Trabajo para esta empresa. Tus propios datos, reglas y habilidades tienen prioridad, y las tareas personales nunca los usan. Una tarea que haya usado un aprendizaje lo indica, por ejemplo: «Se usó un aprendizaje del equipo: los reembolsos se tramitan desde la bandeja de entrada de soporte». Pulsa **Quitar** para eliminarlo de todo el Fleet.

Cualquier persona del Fleet puede **Quitar** un aprendizaje: desaparece para todos y no se vuelve a crear. Para impedirlo, desactiva **Ofrecer compartir aprendizajes** en Ajustes, Seguridad. Los Fleets de trabajo Prudentes no reciben ningún aprendizaje.

## Resumen del equipo

Elige **Diario** o **Semanal** para el **Resumen del equipo** en la pestaña Fleet, en **Compartir**. A continuación, tu Machine pide a las Machines de tus compañeros cifras y fechas. Lo que requiere tu atención aparece en Tareas, en Trabajo: un cliente que espera a un compañero, una empresa sin actividad durante dos semanas o más, dos personas escribiendo a los mismos contactos o una reunión compartida.

- Una tarea indica quién debe responder, desde cuándo, qué pidió y qué está en juego, como un proyecto abierto. Si no hay nada concreto que decir, se queda como una línea del resumen, no como una tarea.
- La empresa y los compañeros enlazan a sus páginas. **Detalles** muestra lo que escribieron (púlsalo para leerlo), qué está en juego, quién del equipo está en contacto y sus conversaciones más recientes, solo lo que comparte el [Graph del equipo](team-graph.md).
- Si lo que escribieron solo está en el correo de un compañero, la tarea indica a quién preguntar.
- **Preguntar al equipo** les envía una pregunta sobre el tema, ya redactada. Sus respuestas aparecen en la tarea.
- **No hace falta** cierra la tarea y el resumen aprende de ello. Solo vuelve a aparecer si hay algo nuevo.
- Cuando alguien responde o se hace cargo, la tarea se cierra automáticamente. Si ya tienes una tarea para esa empresa, la nueva se añade a esa tarea.

## Solicitudes de resumen del equipo

Cada mañana, un compañero que tenga activado el resumen del equipo pide a tu Machine cifras y fechas. En un Fleet de trabajo, tu Machine responde automáticamente solo con lo que ya comparte el [Graph del equipo](team-graph.md), y no responde si compartir el Graph del equipo está desactivado. Cada respuesta aparece en la pestaña Fleet, en **Actividad**, nunca como tarea ni notificación.

Para detenerlo, desactiva **Compartir mis datos del informe con el equipo** en la pestaña Fleet, en **Compartir**. Entonces, en el resumen de tu compañero aparecerás como alguien que no ha respondido.

En un Fleet Prudente, las solicitudes quedan pendientes para que las revises en la pestaña Fleet, en **Solicitudes de resumen del equipo**: **Compartir una vez**, **Compartir siempre**, **Rechazar** o **Nunca**. No se comparte nada hasta que elijas una opción, y las solicitudes sin respuesta caducan.

## Graph del equipo

En un Fleet de trabajo, el trabajo con clientes se comparte con tu equipo cuando ya lo hayas revisado. Consulta [Graph del equipo](team-graph.md).

## Conexiones compartidas

Un propietario o administrador puede conectar Stripe o Intercom una vez y compartirlo con el equipo desde **Conexiones compartidas**, en la pestaña Fleet. Los compañeros pueden ver la conexión, pero no modificarla, y pueden ver quién la compartió. Solo los administradores pueden cambiarla o dejar de compartirla. Consulta [Stripe](stripe.md) e [Intercom](intercom.md).

## Qué responde tu Machine

Configúralo para cada Fleet en el panel Compartir. Consulta [Reglas para compartir](sharing-rules.md). **Ajustes** incluye un acceso directo: **Reglas de Fleet**.

## Inicio de sesión de la empresa

Permite que tus compañeros se unan con su cuenta de empresa. En un Fleet de trabajo alojado, un propietario o administrador que haya iniciado sesión con Google Workspace o Microsoft 365 puede activar **Inicio de sesión de la empresa** en la página Cuenta.

Los compañeros que inicien sesión con el dominio de la empresa verán **Solicitar unirse**, y un propietario o administrador tendrá que **Aprobar** cada solicitud. Las cuentas personales de Gmail y Outlook.com nunca cuentan.

Si eliminas a alguien del Fleet, se cerrará su sesión en todas partes.

Para unirte a un Fleet, crear uno o vincular una Machine en tu propio ordenador, consulta [Planes y facturación](plans-and-billing.md) y [Amigos y la Network](friends.md).

## Para propietarios y administradores

**Gestionar**, en la pestaña Fleet, muestra todos los Fleets que administras: sus miembros, roles e invitaciones. En una Machine alojada, puedes invitar, cambiar roles, eliminar miembros y responder a solicitudes para unirse desde ahí. Si un cambio afecta al precio, se abre tu cuenta para que lo confirmes primero. En una Machine autoalojada, se muestra quién forma parte del Fleet, con un enlace a sus ajustes en tu cuenta, donde puedes administrar a sus miembros e invitaciones.

**Ajustes del Fleet**, debajo del nombre de cada Fleet en su panel y en Gestionar, abre los ajustes de ese Fleet en tu cuenta: conexiones compartidas, seguridad, inicio de sesión de la empresa, qué Machine responde y estas dos opciones:

- **Personas eliminadas recientemente**: muestra a cada persona eliminada o que se fue. «Eliminada, confirmada» significa que su Machine borró los datos de trabajo y se cerró su sesión en todas partes. Hasta entonces, indica **Pendiente** y el motivo.
- **Actividad**: quién hizo qué y cuándo: invitaciones, incorporaciones, eliminaciones, roles, Machines alojadas, facturación, conexiones compartidas y aprobaciones. También registra cada vez que nuestro equipo de soporte lee el informe de la Machine de un miembro o sus registros. Nunca incluye el contenido de los mensajes. **Descargar CSV** lo exporta. Se conserva durante 12 meses.

**Preguntarme antes de iniciar la Machine de un miembro**, para el propietario: si está activado, la Machine de un miembro nuevo espera tu visto bueno, incluso en un Fleet gratuito. Si está desactivado, en un Fleet gratuito se inicia de inmediato y se te avisa. Una Machine de pago siempre espera a que confirmes el importe.

Después de **Dejar de compartir**, una conexión compartida muestra «Eliminada, confirmada» cuando todas las Machines hayan perdido acceso.
