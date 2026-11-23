---
title: Fleets
area: fleet
summary: Un Fleet de trabajo para tu equipo y un Fleet familiar para casa. Machines que se ayudan siguiendo tus reglas para compartir.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: f75a79e685f3a0cc
---
Un Fleet permite que tu Machine trabaje con las Machines de tu equipo, familia o amigos a través de The Machine Network. Todo lo que se comunican está cifrado de extremo a extremo, y tu Machine solo responde según tus reglas.

## Tipos de Fleet

- **Fleet de trabajo**: tu equipo. Pasa trabajo, pregunta quién conoce a alguien, consigue presentaciones y recibe un resumen del equipo.
- **Fleet familiar**: hasta 6 personas. Cuando todos tienen tiempo, pueden compartir tareas y planes, y hacer preguntas a la Machine de otra persona. Es gratis; las Machines alojadas en él tienen un precio familiar. Consulta [Familia](family.md).
- **Amigos**: cualquier persona de The Machine, de una en una. Es gratis. Consulta [Amigos](friends.md).

## La pestaña Fleet

Aparece cuando estás en un Fleet. Incluye un panel para cada Fleet y, después, Amigos, Network, Compartir y Actividad. Los propietarios y administradores también ven **Gestionar**, y en un Fleet de trabajo que comparte su Graph aparece **Qué se comparte**.

## Coste, salir y crear otro Fleet

Debajo del nombre de cada Fleet, **Lo que cuesta** muestra sus plazas, quién paga tu Machine y, para el propietario, la tarjeta y las facturas del Fleet. **Salir de este Fleet** te permite abandonarlo; si eres el propietario, primero tienes que pasárselo a otra persona. **Crear otro Fleet** inicia uno nuevo.

Cada opción abre esa sección de tu cuenta. Si cambia el precio, primero verás el importe que debes confirmar. En una Machine alojada por ti, se abre tu cuenta en una pestaña nueva y tendrás que iniciar sesión.

## Pregunta a tu Fleet

Pregunta «¿quién conoce a alguien en Acme?» desde la pestaña Fleet, o selecciona **Preguntar al Fleet** en una organización de [Graph](graph.md). La Machine de cada compañero responde según sus propias reglas para compartir y, si la regla lo indica, primero le pregunta.

Para cualquier otra cosa, usa **Pregunta lo que quieras** en el panel de tu Fleet de trabajo. Cada compañero recibe un borrador de respuesta preparado con sus propias cuentas de trabajo. No recibirás nada hasta que lo envíe.

## Respuestas automáticas en un Fleet de trabajo

En un Fleet de trabajo estándar, tu Machine responde automáticamente a tres tipos de preguntas de tus compañeros: **quién conoce a alguien**, **contexto de reuniones** («¿quién es esta persona invitada?») y **quién se ocupa de los correos compartidos**. Solo usa la información que el [Graph del equipo](team-graph.md) ya comparte con tu equipo, nunca conversaciones privadas, personales o confidenciales. Cada respuesta aparece en la pestaña Fleet, en **Actividad**.

Para detener una respuesta automática, selecciona **Nunca** en **Compartir**. Una regla configurada como **Pregúntame primero** funciona igual que **Siempre**. Si está desactivado el uso compartido de Graph del equipo, primero te preguntará quién conoce a alguien y el contexto de reuniones.

Los Fleets de trabajo con controles estrictos, Amigos y los Fleets familiares siempre te preguntan primero. Las presentaciones de confianza, los traspasos y las preguntas gratuitas siguen teniendo sus propias reglas.

## Aprendizajes del equipo

Tu Machine registra cómo trabaja tu equipo a partir de las conversaciones con clientes que Graph del equipo ya comparte, como máximo una vez al día. Por ejemplo: «Las solicitudes de reembolso se responden desde la bandeja de entrada de soporte con la plantilla de reembolsos». Aparecen en el panel de tu Fleet de trabajo, en **Aprendizajes del equipo**, y los ve todo el Fleet. Además, cada uno queda registrado en **Actividad**. No se pregunta a nadie antes.

- Solo se usan conversaciones en las que haya participado alguien de tu equipo. Nunca conversaciones privadas, personales o confidenciales.
- Solo se incluyen cosas que se repiten con varios clientes: un proceso, una herramienta, un estilo de escritura o quién se ocupa de cada cosa. Nunca información sobre un único cliente, comentarios sobre tu propio producto, nombres, direcciones, números ni citas.
- Se descartan los aprendizajes sobre los que haya dudas.

Tu Machine usa los aprendizajes pertinentes cuando prepara una tarea de trabajo para esta empresa. Tus propios datos, reglas y habilidades tienen prioridad, y las tareas personales no los usan nunca. Si una tarea ha usado un aprendizaje, lo indica, por ejemplo: «Se ha usado un aprendizaje del equipo: los reembolsos se tramitan desde la bandeja de entrada de soporte». Pulsa **Quitar** para eliminarlo de todo el Fleet.

Cualquier persona del Fleet puede **Quitar** un aprendizaje. Desaparece para todos y no vuelve a generarse. Para impedirlo, desactiva **Ofrecer compartir aprendizajes** en Ajustes, Seguridad. Los Fleets de trabajo con controles estrictos no reciben aprendizajes.

## Resumen del equipo

Selecciona **Diario** o **Semanal** para **Resumen del equipo** en la pestaña Fleet, dentro de **Compartir**. Entonces, tu Machine pide a las Machines de tus compañeros datos numéricos y fechas. Lo que necesita tu atención aparece en Tareas, en Trabajo: un cliente que espera una respuesta de un compañero, una empresa sin actividad durante dos semanas o más, dos personas del equipo escribiendo a los mismos contactos o una reunión compartida.

- La tarea indica a quién está esperando, desde cuándo, qué le han pedido y qué está en juego, por ejemplo, un proyecto en curso. Si no hay nada concreto que añadir, se queda como una línea del resumen y no se convierte en tarea.
- La empresa y los compañeros enlazan a sus páginas. **Detalles** muestra lo que escribieron (pulsa para leerlo), qué está en juego, quién del equipo está en contacto y sus conversaciones más recientes. Solo incluye lo que comparte el [Graph del equipo](team-graph.md).
- Si lo que escribieron solo está en el correo de un compañero, la tarea indica a quién preguntar.
- **Preguntar al equipo** les envía una pregunta ya preparada sobre el tema. Sus respuestas aparecen en la tarea.
- **No hace falta** la cierra y el resumen lo tiene en cuenta. Solo vuelve a aparecer si hay algo nuevo.
- Cuando alguien responde o se encarga del asunto, la tarea se cierra automáticamente. Si ya tienes una tarea sobre esa empresa, se añade a ella.

## Solicitudes de resumen del equipo

Cada mañana, un compañero que tenga activado el resumen del equipo pide a tu Machine datos numéricos y fechas. En un Fleet de trabajo, tu Machine responde automáticamente solo con la información que ya comparte el [Graph del equipo](team-graph.md). No responde si está desactivado el uso compartido de Graph del equipo. Cada respuesta aparece en la pestaña Fleet, en **Actividad**, nunca como tarea ni como notificación.

Para detenerlo, desactiva **Compartir mis datos del informe con el equipo** en la pestaña Fleet, dentro de **Compartir**. En el resumen de tus compañeros aparecerá que no has respondido.

En un Fleet con controles estrictos, las solicitudes quedan en la pestaña Fleet, en **Solicitudes de resumen del equipo**. Puedes elegir **Compartir una vez**, **Compartir siempre**, **Rechazar** o **Nunca**. No se comparte nada hasta que elijas una opción, y las solicitudes sin responder caducan.

## Graph del equipo

En un Fleet de trabajo, el trabajo con clientes se comparte con tu equipo después de que lo revises. Consulta [Graph del equipo](team-graph.md).

## Conexiones compartidas

Un propietario o administrador puede conectar Stripe o Intercom una vez y compartirlo con el equipo desde **Conexiones compartidas** en la pestaña Fleet. Los compañeros pueden verlo, pero no modificarlo, y pueden ver quién lo ha compartido. Solo los administradores pueden modificarlo o dejar de compartirlo. Consulta [Stripe](stripe.md) e [Intercom](intercom.md).

## Qué responde tu Machine

Configúralo para cada Fleet, en el panel Compartir. Consulta [Reglas para compartir](sharing-rules.md). En **Ajustes** hay un acceso directo: **Reglas de Fleet**.

## Inicio de sesión de empresa

Permite que tus compañeros se unan con su cuenta de empresa. En un Fleet de trabajo alojado, un propietario o administrador que haya iniciado sesión con Google Workspace o Microsoft 365 puede activar **Inicio de sesión de empresa** en la página Cuenta.

Los compañeros que inicien sesión con el dominio de su empresa verán **Solicitar unirse**. Un propietario o administrador tendrá que **Aprobar** cada solicitud. Las cuentas personales de Gmail y Outlook.com nunca se aceptan.

Si eliminas a alguien del Fleet, se cerrará su sesión en todas partes.

Para unirte a un Fleet, crear uno o vincular una Machine en tu propio ordenador, consulta [Planes y facturación](plans-and-billing.md) y [Amigos y la Network](friends.md).

## Para propietarios y administradores

**Gestionar**, en la pestaña Fleet, muestra cada Fleet que administras, sus integrantes, sus roles y las invitaciones. En una Machine alojada, puedes invitar a personas, cambiar sus roles, eliminarlas y responder a solicitudes para unirse desde ahí. Si un cambio afecta al precio, se abrirá tu cuenta para que lo confirmes primero. En una Machine alojada por ti, verás quién forma parte del Fleet y un enlace a sus ajustes en tu cuenta, donde podrás gestionar a sus integrantes y las invitaciones.

**Ajustes del Fleet**, debajo del nombre de cada Fleet en su panel y en Gestionar, abre los ajustes de ese Fleet en tu cuenta. Desde ahí puedes gestionar las conexiones compartidas, la seguridad, el inicio de sesión de empresa, qué responde la Machine y estas dos opciones:

- **Eliminados recientemente**: muestra a cada persona eliminada o que se haya ido. «Eliminado, confirmado» significa que su Machine ha borrado los datos de trabajo y se ha cerrado su sesión en todas partes. Hasta entonces, indica **Pendiente** y el motivo.
- **Actividad**: quién hizo qué y cuándo: invitaciones, incorporaciones, eliminaciones, cambios de rol, Machines alojadas, facturación, conexiones compartidas y aprobaciones. También registra cada vez que nuestro equipo de asistencia lee el informe de la Machine de un miembro o sus registros. Nunca incluye el contenido de los mensajes. **Descargar CSV** lo exporta. Se conserva durante 12 meses.

**Preguntarme antes de iniciar la Machine de un miembro**, para el propietario: si está activado, tendrás que dar el visto bueno antes de iniciar la Machine de un nuevo miembro, incluso en un Fleet gratuito. Si está desactivado, en un Fleet gratuito se inicia de inmediato y se te avisa. Si la Machine tiene un coste, siempre tendrás que confirmar el importe antes de iniciarla.

Después de seleccionar **Dejar de compartir**, una conexión compartida muestra «Eliminada, confirmada» cuando todas las Machines hayan perdido el acceso.
