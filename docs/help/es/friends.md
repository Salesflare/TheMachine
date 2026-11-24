---
title: Amigos y la Network
area: fleet
summary: Añade amigos por nombre de usuario, encuentra a personas que conoces y que tienen una Machine, y vincula una Machine en tu propio ordenador.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 70a39b4999d112b7
---
## Amigos

Añade a alguien por su nombre de usuario exacto, en la pestaña **Fleet**, en Amigos. Tus amigos pueden preguntar quién conoce a alguien, obtener contexto sobre reuniones y presentaciones, y ver cuándo estás ocupado (solo las horas, nunca el motivo). Los días que no aparecen en el calendario figuran como desconocidos, nunca como libres. Puedes eliminar o bloquear a un amigo cuando quieras.

## Encuentra a personas que conoces

En **Fleet**, en **Network**:

- «Comprueba cuáles de mis contactos tienen una Machine» te sugiere personas que conoces.
- «Deja que me encuentren las personas que tienen mi correo» permite que te encuentren.

Ambas opciones están activadas de forma predeterminada y desactivadas en el nivel de seguridad Cuidadoso. Puedes desactivar cualquiera cuando quieras y la opción que elijas se mantiene. Pueden encontrarte con tu correo de inicio de sesión (siempre activado) y tus direcciones conectadas, cada una con su propio interruptor en **Localizable por**. Las direcciones compartidas, como info@, permanecen desactivadas hasta que las actives.

Las personas que conoces aparecen como tarea en cuanto activas la opción y también cuando se unen más adelante. Para cada una, puedes elegir **Amigo** o **Familia** (**Conectar** para un compañero de trabajo), **Ahora no** o **No sugerir nunca** en el menú ⋯. Cuando ya sois amigos, dejan de aparecer como sugerencias. **Salir de la Network** te elimina de ella.

Las personas que encuentra aparecen como **Tiene una Machine** en tu lista de personas. Comprueba las direcciones de tus mensajes y las que añadiste a una persona con **Editar**. Si alguien se registró con otra dirección, añádela a su perfil. En la página de una persona que haya encontrado, **Añadir como amigo** envía la misma solicitud que Conectar (**Añadir como familia** está en el menú ⋯).

Para alguien que no tiene una Machine, aparece **Invitar a The Machine**. Se abre el correo que recibirá en **¿Enviar este correo?**. Es el mismo que para cualquier tarea y puedes modificarlo si quieres. No se envía nada hasta que pulses **Enviar ahora**. Si lo cierras, la invitación queda pendiente como tarea. Si no tienes un buzón desde el que enviar correo: **Copiar** o **Abrir en tu correo**.

También cuentan los números de teléfono: los de tus chats de WhatsApp con personas a las que has escrito o con las que te has visto, y los que añadiste con **Editar**. Tu número de WhatsApp vinculado y los números de la sección «Sobre ti» permiten que te encuentren, cada uno con su propio interruptor en **Localizable por**. Un número solo permite encontrar a alguien si esa persona también te ha buscado o si sois amigos. Así, nadie puede probar números para averiguar quién tiene una Machine.

## Organizar reuniones con otras Machines

Cuando alguien con una Machine escribe «quedemos la semana que viene», tu Machine le pide a la suya que busque horas libres y encuentra una que os venga bien a ambos, dentro de tu horario laboral. Cada uno recibe una tarea, como «Queda con Alex Example», con la hora debajo. Pulsa **Reservar**, **Otra hora** o **No hace falta**. La invitación solo se envía cuando ambos habéis pulsado Reservar.

Solo se comparte si estás libre u ocupado, con cifrado de extremo a extremo, para un máximo de 14 días y en intervalos de 15 minutos. Los eventos privados cuentan como ocupados. Una Machine solo puede preguntar si os habéis enviado correos mutuamente. Configúralo en **Qué pueden preguntar otras Machines a la mía**: **Libre/ocupado para agendar** o **Desactivado**, junto con la duración de la reunión, el margen y las horas que prefieres. Cada solicitud aparece en Actividad, en Calendario.

Una hora solo cuenta como libre si así lo indica tu calendario. Tu Machine no ofrece horas si no hay ningún calendario conectado, si no ha podido leerlo durante un día o si la fecha es dentro de más de 30 días. Los eventos de todo el día cuentan como ocupados si están marcados como Ocupado, y los marcados como Libre nunca cuentan como ocupados. Un evento de todo el día que añada una tarea es Libre, a menos que estés de viaje o hayas reservado esos días. En ese caso, indica «ocupado» antes de que lo añadas.

Si la otra persona no tiene una Machine o no responde, el borrador del correo incluye un enlace para que elija una de tus horas libres. La hora que elija aparece como una tarea con **Reservar**. No se reserva nada hasta que pulses el botón.

El enlace solo muestra las horas libres, según las mismas reglas, y no revela nada más sobre ti. Deja de funcionar cuando se reserva la reunión o después de 14 días. En el correo aparece como «Elige una hora». Al final de la página se lee «La Machine de Alex ha encontrado estas horas. Consigue la tuya.», con tu nombre. Desactiva esta opción con **Pie en los enlaces de reserva**. Cada enlace y elección aparece en Actividad.

## Una Machine en tu propio ordenador

Para unirte a la Network desde una Machine que ejecutas por tu cuenta:

1. En el panel de control de tu Machine, abre **Ajustes** y pulsa **Unirse a la Network**.
2. En la página que se abre, inicia sesión (o crea tu cuenta) y confirma. Tu Machine lo detecta automáticamente, sin necesidad de reiniciarla.

También puedes usar el código: pulsa **Vincular una Machine autoalojada** en la página de tu cuenta en app.themachine.computer. Después, ejecuta `assistant fleet-pair` con el código en tu ordenador y reiníciala. El código solo funciona una vez y durante 15 minutos.

Puedes tener hasta 5 Machines por cuenta. Puedes desconectar cada una desde allí.
