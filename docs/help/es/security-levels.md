---
title: Niveles de seguridad
area: security
summary: Un solo control, Estándar o Prudente, define tus ajustes de seguridad y privacidad. El administrador de un Fleet de trabajo elige el nivel para todo el Fleet.
covers: settings:security
code: security_levels.py, dashboard.html, fleet.py
order: 2
translated: cf3ba86c8c1a23f3
---
## Dos niveles

Abre **Ajustes** y luego **Seguridad**.

- **Estándar**: la configuración predeterminada actual. No cambia nada.
- **Prudente**: más estricto, para cuando quieres menos información en tu teléfono y que se guarde menos.

Un nivel es un punto de partida. Si después cambias cualquier ajuste, el nivel pasa a **Personalizado**. Elige un nivel de nuevo para restablecer los ajustes.

## Qué cambia Prudente para ti

- **Texto en las notificaciones** desactivado: una notificación dice «Nueva tarea» o «Para revisar», pero no muestra el contenido de la tarea.
- **Ofrecer guardar inicios de sesión** desactivado. Los sitios en los que ya iniciaste sesión y que guardaste seguirán ahí hasta que pulses **Olvidar todos los inicios de sesión guardados**.
- **Buscar contactos de trabajo**, **Ofrecer compartir aprendizajes** y **Compartir lo que se pregunta a la ayuda** desactivados.
- **Comprobar cuáles de mis contactos tienen una Machine** y **Dejar que me encuentren quienes tienen mi correo** desactivados.
- **Guardar los detalles de Hazlo 90 días** desactivado: se conservan durante 30 días.
- **Qué pueden preguntar otras Machines a la mía** se establece en **Desactivado**: no se pueden programar reuniones con otras Machines. Consulta [Amigos y la Network](friends.md#scheduling-with-other-machines).
- En una Familia, primero tienes que aprobar las solicitudes de horarios disponibles. Con Amigos, se rechaza el contexto de las reuniones.

## Nivel de un Fleet de trabajo

El propietario del Fleet o un administrador lo elige en **Ajustes del Fleet**: ve a **Ajustes** › **Cuenta** y pulsa **Fleet**. Todas las personas del Fleet pueden verlo. Cuando está en Prudente:

- Las respuestas a tus compañeros esperan tu aprobación, no incluyen nombres y solo tratan sobre personas de tus cuentas de trabajo.
- Las presentaciones y los traspasos también esperan tu aprobación.
- El Graph del equipo comparte los correos de clientes, pero no sus archivos adjuntos.
- Las notificaciones de tareas de trabajo no muestran el texto.
- No se buscan contactos de trabajo.
- Tu Machine no comprueba tus contactos en Network ni permite que te encuentren por correo, a menos que hayas activado esa opción.
- Todas las personas tienen que volver a iniciar sesión cada 7 días.
- Un enlace de invitación solo funciona con la dirección de correo a la que se envió.

Los miembros pueden elegir ajustes más estrictos que los del Fleet, pero no menos estrictos. Se conservan sus propios ajustes y se restablecen si el Fleet vuelve a Estándar.

## Lo mismo en ambos niveles

No se envía nada sin tu aprobación: puedes ver cada borrador y pulsar **Enviar**. Hazlo y los agentes de programación funcionan igual. Para iniciar sesión, siempre necesitas un código de autenticación o una clave de acceso.
