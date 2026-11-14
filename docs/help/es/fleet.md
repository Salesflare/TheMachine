---
title: Fleet
area: fleet
summary: Un Work Fleet para tu equipo y un Family Fleet para casa. Machines que se ayudan entre sí según tus reglas para compartir.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: c9650fc4ffe00e16
---
Un Fleet permite que tu Machine trabaje con las Machines de tu equipo, tu familia o tus amigos a través de The Machine Network. Lo que se cuentan está cifrado de extremo a extremo, y tu Machine responde solo según tus reglas.

## Tipos de Fleet

- **Work Fleet**: tu equipo. Pasa trabajo, pregunta quién conoce a alguien, consigue presentaciones y recibe un resumen del equipo.
- **Family Fleet**: hasta 6 personas. Si todos tienen tiempo libre, pueden compartir tareas y planes. Gratis. Consulta [Familia](family.md).
- **Amigos**: cualquier persona de The Machine, de una en una. Gratis. Consulta [Amigos](friends.md).

## La pestaña Fleet

Aparece cuando formas parte de un Fleet. Incluye un panel para cada Fleet, Familia, Amigos, Network, Compartiendo y Actividad.

## Lo que cuesta, salir de un Fleet y crear otro

Debajo del nombre de cada Fleet, **Lo que cuesta** muestra sus plazas, quién paga tu Machine y, para el propietario, la tarjeta y las facturas del Fleet. **Salir de este Fleet** te permite salir; si eres el propietario, primero tienes que pasárselo a otra persona. **Crear otro Fleet** inicia uno nuevo.

Cada opción abre esa sección de tu cuenta, y si cambia el precio, primero se muestra el importe para que lo confirmes. En una Machine autoalojada, las opciones abren tu cuenta en una pestaña nueva, donde tendrás que iniciar sesión.

## Pregunta a tu Fleet

Pregunta «¿quién conoce a alguien en Acme?» desde la pestaña Fleet o selecciona **Preguntar al Fleet** en una organización de [Graph](graph.md). La Machine de cada compañero responde según sus propias reglas para compartir, y primero le pregunta si así lo indican sus reglas.

## Respuestas automáticas en un Work Fleet

En un Work Fleet estándar, tu Machine responde automáticamente a tres tipos de preguntas de tus compañeros: **quién conoce a alguien**, **contexto de reuniones** («¿quién es este invitado?») y **quién se ocupa de los correos compartidos**. Solo usa lo que el [Graph del equipo](team-graph.md) ya comparte con tu equipo. Nunca usa conversaciones privadas, personales ni confidenciales. Cada respuesta aparece en la pestaña Fleet, en **Actividad**.

Para detener una respuesta automática, selecciona **Nunca** en **Compartiendo**. Una regla guardada como **Pregúntame primero** funciona como **Siempre**. Mientras esté desactivado el uso compartido de Graph del equipo, las preguntas sobre quién conoce a alguien y el contexto de reuniones te las hará primero a ti.

Los Work Fleets con revisión, Amigos y Family siguen preguntándote primero. Las presentaciones, los traspasos y las preguntas gratuitas siguen teniendo sus propias reglas.

## Aprendizajes del equipo

Tu Machine anota cómo trabaja tu equipo a partir de conversaciones con clientes que el Graph del equipo ya comparte, como máximo una vez al día. Por ejemplo: «Las solicitudes de reembolso se responden desde la bandeja de entrada de soporte con la plantilla de reembolso». Aparecen en el panel de tu Work Fleet, en **Aprendizajes del equipo**, para todos los miembros del Fleet. Cada uno queda registrado en **Actividad**. No se le pregunta primero a nadie.

- Solo se incluyen conversaciones en las que haya escrito alguien de tu equipo. Nunca conversaciones privadas, personales ni confidenciales.
- Solo se incluyen cosas que se repiten con varios clientes: un proceso, una herramienta, un estilo de escritura o quién se ocupa de cada cosa. Nunca algo sobre un solo cliente, comentarios sobre tu propio producto, nombres, direcciones, números ni citas.
- Si no está segura, tu Machine descarta el aprendizaje.

Tu Machine usa los aprendizajes pertinentes cuando prepara una tarea de trabajo para esta empresa. Tus propios datos, reglas y habilidades tienen prioridad, y las tareas personales nunca los usan. Una tarea que haya usado uno lo indica, por ejemplo: «Se usó un aprendizaje del equipo: los reembolsos se tramitan desde la bandeja de entrada de soporte». Pulsa **Quitar** para eliminarlo de todo el Fleet.

Cualquier miembro del Fleet puede **Quitar** un aprendizaje: desaparece para todos y no vuelve a generarse. Para evitarlo, desactiva **Ofrecer compartir aprendizajes** en Ajustes, Seguridad. Los Work Fleets con revisión no reciben aprendizajes.

## Resumen del equipo

Selecciona **Diario** o **Semanal** para **Resumen del equipo** en la pestaña Fleet, en **Compartiendo**. Tu Machine pedirá entonces a las Machines de tus compañeros cantidades y fechas. Lo que necesite tu atención aparecerá en Tareas, en Trabajo: un cliente que espera a un compañero, una empresa sin actividad durante dos semanas o más, dos personas del equipo escribiendo a los mismos contactos o una reunión compartida.

- La tarea indica quién debe responder, desde cuándo, qué pidió y qué está en juego, por ejemplo, un proyecto abierto. Si no hay nada concreto que decir, se queda como una línea del resumen y no se convierte en tarea.
- La empresa y los compañeros enlazan a sus páginas. **Detalles** muestra lo que escribieron (pulsa para leerlo), qué está en juego, quién del equipo está en contacto y sus conversaciones más recientes. Solo se muestra lo que comparte el [Graph del equipo](team-graph.md).
- Si lo que escribieron solo aparece en el correo de un compañero, la tarea indica a quién preguntar.
- **Preguntar al equipo** les envía una pregunta al respecto, ya preparada. Sus respuestas aparecen en la tarea.
- **No hace falta** la cierra y el resumen lo tendrá en cuenta. Solo vuelve a aparecer si hay novedades.
- Cuando alguien responde o se ocupa de la tarea, se cierra automáticamente. Si hay una tarea sobre una empresa para la que ya tienes otra, se añade a esa tarea.

## Solicitudes de resumen del equipo

Cada mañana, un compañero que tenga activado el resumen del equipo le pide a tu Machine cantidades y fechas. En un Work Fleet, tu Machine responde automáticamente con lo que el [Graph del equipo](team-graph.md) ya comparte, y no responde si el uso compartido de Graph del equipo está desactivado. Cada respuesta aparece en la pestaña Fleet, en **Actividad**, nunca como tarea ni notificación.

Para detenerlo, desactiva **Compartir mis datos del informe con el equipo** en la pestaña Fleet, en **Compartiendo**. A partir de entonces, el resumen de tus compañeros indicará que no has respondido.

En un Fleet con revisión, las solicitudes esperan en la pestaña Fleet, en **Solicitudes de resumen del equipo**. Puedes elegir **Compartir una vez**, **Compartir siempre**, **Rechazar** o **Nunca**. No se comparte nada hasta que elijas una opción, y las solicitudes sin respuesta caducan.

## Graph del equipo

En un Work Fleet, el trabajo con clientes se comparte con tu equipo después de que lo revises. Consulta [Graph del equipo](team-graph.md).

## Conexiones compartidas

El propietario o un administrador puede conectar Stripe o Intercom una sola vez y compartirlo con el equipo desde **Conexiones compartidas** en la pestaña Fleet. Los compañeros pueden consultarlo, pero no modificarlo, y pueden ver quién lo compartió. Solo los administradores pueden modificarlo o dejar de compartirlo. Consulta [Stripe](stripe.md) e [Intercom](intercom.md).

## Qué responde tu Machine

Configúralo para cada Fleet, en el panel Compartiendo. Consulta [Reglas para compartir](sharing-rules.md). **Ajustes** incluye un acceso directo a **Reglas de Fleet**.

## Inicio de sesión de la empresa

Permite que tus compañeros se unan con su cuenta de empresa. En un Work Fleet alojado, el propietario o un administrador que haya iniciado sesión con Google Workspace o Microsoft 365 puede activar **Inicio de sesión de la empresa** en la página Cuenta.

Los compañeros que inicien sesión con el dominio de esa empresa verán **Solicitar unirse**, y el propietario o un administrador tendrá que **Aprobar** cada solicitud. Las cuentas personales de Gmail y Outlook.com no cuentan.

Si eliminas a alguien del Fleet, se cerrará su sesión en todas partes.

Para unirte a un Fleet, iniciar uno o vincular una Machine en tu propio ordenador, consulta [Planes y facturación](plans-and-billing.md) y [Amigos y Network](friends.md).

## Para propietarios y administradores

**Gestionar**, en la pestaña Fleet, muestra cada Fleet que administras, sus miembros, sus roles y las invitaciones. En una Machine alojada, puedes invitar a personas, cambiar roles, eliminar miembros y responder a solicitudes para unirse desde ahí. Si un cambio afecta al precio, se abrirá tu cuenta para que lo confirmes primero. En una Machine autoalojada, verás quién forma parte del Fleet y un enlace a los ajustes de ese Fleet en tu cuenta, donde podrás administrar sus miembros e invitaciones.

**Ajustes del Fleet**, debajo del nombre de cada Fleet en su panel y en Gestionar, abre los ajustes de ese Fleet en tu cuenta: conexiones compartidas, seguridad, inicio de sesión de la empresa, qué Machine responde y estas dos opciones:

- **Eliminados recientemente**: muestra a cada persona eliminada o que se haya ido. «Eliminado, confirmado» significa que su Machine borró los datos de trabajo y que cerró su sesión en todas partes. Hasta entonces, aparece **Pendiente** y el motivo.
- **Actividad**: quién hizo qué y cuándo: invitaciones, incorporaciones, eliminaciones, cambios de rol, Machines alojadas, facturación, conexiones compartidas y aprobaciones. También registra cada vez que nuestro equipo de soporte leyó el informe de la Machine de un miembro o sus registros. Nunca incluye el contenido de los mensajes. **Descargar CSV** lo exporta. Se conserva durante 12 meses.

**Preguntarme antes de iniciar la Machine de un miembro**, para el propietario: si está activado, la Machine de un nuevo miembro espera tu aprobación, incluso en un Fleet gratuito. Si está desactivado, en un Fleet gratuito se inicia de inmediato y se te avisa. Si la Machine tiene un coste, siempre tendrás que confirmar el importe.

Después de **Dejar de compartir**, una conexión compartida muestra «Eliminado, confirmado» cuando todas las Machines hayan perdido el acceso.
