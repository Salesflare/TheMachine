---
title: Amigos y la Network
area: fleet
summary: Añade amigos por nombre de usuario, encuentra a personas que conoces y tienen una Machine, y vincula una Machine en tu propio ordenador.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 637784bf811800bb
---
## Amigos

Añade a alguien con su nombre de usuario exacto, en la pestaña **Fleet**, dentro de Amigos. Tus amigos pueden preguntar quién conoce a alguien, obtener contexto sobre reuniones y presentaciones cercanas, y ver cuándo estás ocupado (solo los horarios, nunca el motivo). Puedes eliminar o bloquear a un amigo cuando quieras.

## Encuentra a personas que conoces

En **Fleet**, dentro de **Network**:

- **Comprobar cuáles de mis contactos tienen una Machine** te sugiere personas que conoces.
- **Dejar que me encuentren quienes tienen mi correo** hace que puedan encontrarte.

Ambas opciones están activadas de forma predeterminada y desactivadas en el nivel de seguridad Prudente. Puedes desactivar cualquiera cuando quieras; tu elección se mantiene. Las personas pueden encontrarte mediante el correo con el que inicias sesión (siempre activado) y tus direcciones conectadas, cada una con su propio interruptor en **Localizable por**, excepto las direcciones compartidas, como info@, que permanecen desactivadas hasta que las actives.

Las personas que conoces aparecen como una tarea en cuanto activas esta opción y también cuando se unan más adelante. Para cada persona aparecen las opciones **Amigo** y **Familia** (**Conectar** para un compañero de trabajo), **Ahora no** y **No sugerir nunca** en el menú ⋯. Cuando ya son amigos, dejan de aparecer como sugerencias. **Salir de la Network** te elimina de la Network.

Las personas que encuentra aparecen como **Tiene una Machine** en tu lista de Personas. Comprueba las direcciones de tus mensajes y las que añadiste a una persona con **Editar**. Si alguien se registró con otra dirección, añádela a su ficha. En la página de alguien que haya encontrado, **Añadir como amigo** envía la misma solicitud que Conectar (**Añadir como familia** está en el menú ⋯).

Para alguien que no tiene una Machine, aparece **Invitar a The Machine**: se abre el correo que recibirá en **¿Enviar este correo?**, el mismo que para cualquier tarea, para que lo cambies si quieres. No se envía nada hasta que pulses **Enviar ahora**. Si lo cierras, la invitación queda pendiente como una tarea. Si no tienes un buzón desde el que enviar: **Copiar** o **Abrir en tu correo**.

También cuentan los números de teléfono: los que aparecen en tus chats de WhatsApp con personas a las que escribiste o con las que te reuniste, y los que añadiste con **Editar**. Tu número de WhatsApp vinculado y los números de la sección Sobre ti hacen que puedan encontrarte, cada uno con su propio interruptor en **Localizable por**. Un número solo permite encontrar a alguien si esa persona también te ha buscado o si ya son amigos, así nadie puede probar números para ver quién tiene una Machine.

## Agenda con otras Machines

Cuando alguien con una Machine te escribe «quedemos la semana que viene», tu Machine le pide a la suya horarios disponibles y encuentra uno que les venga bien a los dos, dentro de tu horario laboral. Cada uno recibe una tarea, como «Quedar con Alex Example», con la hora debajo. Pulsa **Reservar**, **Otra hora** o **No hace falta**. La invitación solo se envía cuando ambos han pulsado Reservar.

Solo se comparte si estás libre u ocupado, cifrado de extremo a extremo, para un máximo de 14 días y con intervalos de 15 minutos. Los eventos privados cuentan como ocupados. Una Machine solo puede preguntar si se han enviado correos mutuamente. Configura esta opción en **Qué pueden preguntar otras Machines a la mía**: **Libre/ocupado para agendar** o **Desactivado**, junto con la duración de la reunión, el margen entre reuniones y tus horarios preferidos. Cada solicitud aparece en Actividad, dentro de Calendario.

Si la otra persona no tiene una Machine o no responde, el borrador del correo incluye un enlace para que elija uno de tus horarios disponibles. Su elección aparece como una tarea con **Reservar**; no se reserva nada hasta que pulses el botón.

El enlace muestra solo los horarios disponibles, según las mismas reglas, y nada más sobre ti. Deja de funcionar cuando se reserva la reunión o después de 14 días. En el correo aparece como «Elige una hora». Al final de la página dice «La Machine de Alex encontró estos horarios. Consigue la tuya.», con tu nombre. Desactiva esta opción con **Pie en los enlaces de reserva**. Cada enlace y cada elección aparecen en Actividad.

## Una Machine en tu propio ordenador

Para unirte a la Network desde una Machine que ejecutas tú:

1. En el panel de control de tu Machine, abre **Ajustes** y pulsa **Unirse a la Network**.
2. En la página que se abre, inicia sesión (o crea una cuenta) y confirma. Tu Machine lo detecta automáticamente, sin reiniciarse.

También puedes usar el método con código: pulsa **Vincular una Machine autoalojada** en la página de tu cuenta, en app.themachine.computer, y luego ejecuta `assistant fleet-pair` con el código en tu ordenador y reinicia. El código funciona una sola vez durante 15 minutos.

Puedes tener hasta 5 Machines por cuenta. Puedes desconectar cada una desde ahí.
