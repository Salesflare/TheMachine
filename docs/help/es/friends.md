---
title: Amigos y la Network
area: fleet
summary: Añade amigos por nombre de usuario, encuentra a gente que conoces y que tiene una Machine, y empareja una Machine en tu propio ordenador.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 3565b3898b234575
---
## Amigos

Añade a alguien con su nombre de usuario exacto, en la pestaña **Fleet**, dentro de Amigos. Tus amigos pueden preguntar quién conoce a alguien, obtener contexto sobre reuniones y presentaciones, y ver cuándo tienes la agenda ocupada (solo los horarios, nunca los detalles). Puedes eliminar o bloquear a un amigo cuando quieras.

## Encuentra a gente que conoces

En **Fleet**, dentro de **Network**:

- «Comprobar cuáles de mis contactos tienen una Machine» te sugiere personas que conoces.
- «Permitir que me encuentren quienes tienen mi correo» permite que te encuentren.

Ambas opciones están activadas de forma predeterminada y desactivadas en el nivel de seguridad Cuidadoso. Puedes desactivar cualquiera cuando quieras y tu elección se mantiene. Pueden encontrarte por el correo con el que inicias sesión (siempre activado) y por tus direcciones conectadas, cada una con su propio interruptor en **Localizable por**. Las direcciones compartidas, como info@, permanecen desactivadas hasta que las actives.

Las personas que conoces aparecen enseguida cuando activas la opción y también cuando se unen más adelante. Para cada una puedes elegir Conectar, Ahora no o **No sugerir nunca**. Cuando ya sois amigos, dejan de aparecer como sugerencia. **Salir de la Network** te elimina de la Network.

Las personas que encuentra aparecen como **Tiene una Machine** en tu lista de Personas. Comprueba las direcciones de tus mensajes y las que hayas añadido a una persona con **Editar**. Si alguien se registró con otra dirección, añádela a su perfil. En la página de alguien que haya encontrado, **Añadir como amigo** envía la misma solicitud que Conectar (**Añadir como familia** está en el menú ⋯).

Para alguien que no tiene una Machine, aparece **Invitar a The Machine**. Se abre el correo que recibirá en **¿Enviar este correo?**, el mismo que para cualquier tarea, para que lo edites si quieres. No se envía nada hasta que pulses **Enviar ahora**. Si cierras la ventana, la invitación queda pendiente como tarea. Si no tienes un buzón desde el que enviar: **Copiar** o **Abrir en tu correo**.

También se tienen en cuenta los números de teléfono: los de tus chats de WhatsApp con personas a las que hayas escrito o con las que te hayas reunido, y los que hayas añadido con **Editar**. Tu número de WhatsApp vinculado y los números de la sección Sobre ti permiten que te encuentren, cada uno con su propio interruptor en **Localizable por**. Un número solo permite encontrar a alguien si esa persona también te ha buscado o si sois amigos. Así nadie puede probar números para ver quién tiene una Machine.

## Agendar con otras Machines

Cuando alguien con una Machine te escribe «quedemos la semana que viene», tu Machine le pregunta a la suya por los horarios disponibles y busca uno que les venga bien a ambos, dentro de tu horario laboral. Cada uno recibe una tarea, como «Quedar con Alex Example», con la hora debajo. Pulsa **Reservar**, **Otra hora** o **No hace falta**. La invitación solo se envía cuando ambos hayáis pulsado Reservar.

Solo se comparte si estás libre u ocupado, con cifrado de extremo a extremo, durante un máximo de 14 días y en intervalos de 15 minutos. Los eventos privados cuentan como ocupados. Una Machine solo puede preguntar si os habéis enviado correos mutuamente. Configúralo en **Qué pueden preguntar otras Machines a la mía**: **Libre/ocupado para agendar** o **Desactivada**, junto con la duración de la reunión, el margen entre reuniones y tus horarios preferidos. Cada solicitud aparece en Actividad, dentro de Calendario.

Si la otra persona no tiene una Machine o no responde, el borrador del correo incluye un enlace para que elija uno de tus horarios disponibles. Su elección aparece como una tarea con **Reservar**. No se agenda nada hasta que pulses esa opción.

El enlace muestra solo los horarios disponibles, según las mismas reglas, y no revela nada más sobre ti. Deja de funcionar cuando se agenda la reunión o después de 14 días. En el correo aparece como «Elegir una hora». Al pie de la página dice «Tu Machine encontró estos horarios. Consigue la tuya», junto con tu nombre. Puedes desactivar ese texto con **Pie en los enlaces de reserva**. Cada enlace y cada elección aparecen en Actividad.

## Una Machine en tu propio ordenador

Para unirte a la Network desde una Machine que ejecutas tú:

1. En el panel de control de tu Machine, abre **Ajustes** y pulsa **Unirte a la Network**.
2. En la página que se abre, inicia sesión (o crea tu cuenta) y confirma. Tu Machine se conecta automáticamente, sin reiniciarse.

También puedes hacerlo con el código: pulsa **Emparejar una Machine autoalojada** en la página de tu cuenta en app.themachine.computer. Luego ejecuta `assistant fleet-pair` con el código en tu ordenador y reinicia. El código se puede usar una sola vez y dura 15 minutos.

Puedes tener hasta 5 Machines por cuenta. Puedes desconectar cada una desde esa página.
