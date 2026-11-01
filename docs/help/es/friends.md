---
title: Amigos y la Network
area: fleet
summary: Añade amigos por nombre de usuario, encuentra a gente que conoces que tiene una Machine y vincula una Machine en tu propio ordenador.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
---
## Amigos

Añade a alguien por su nombre de usuario exacto, en la pestaña **Fleet**, en Amigos. Los amigos pueden preguntar quién conoce a alguien, recibir contexto para reuniones y presentaciones cercanas, y ver cuándo estás ocupado (solo las horas ocupadas, nunca qué haces). Quita o bloquea a un amigo cuando quieras.

## Encuentra a gente que conoces

En el panel Network:

- "Ver cuáles de mis contactos tienen una Machine" te sugiere gente que conoces.
- "Dejar que me encuentren quienes tienen mi correo" permite que te encuentren.

Los dos están activados por defecto, y desactivados en el nivel de seguridad Prudente. Desactiva cualquiera cuando quieras; tu elección se mantiene. Te pueden encontrar por el correo con el que inicias sesión y tus direcciones conectadas, salvo las compartidas como info@, que siguen desactivadas hasta que las actives.

La gente que conoces y está en la Network se te sugiere en cuanto la activas, y cuando alguien se une más tarde. Cada coincidencia viene con Conectar, Ahora no o **No sugerir nunca**. **Salir de la Network** te saca de ella.

## Agendar con otras Machines

Cuando alguien con una Machine escribe «veámonos la semana que viene», tu Machine pide a la suya sus horas libres y encuentra una que os vaya bien a los dos, dentro de tu horario laboral. Cada uno recibe un solo to-do, como «Reunión con Alex Example», con la hora debajo. Toca **Reservar**, **Otra hora** o **No hace falta**. La invitación solo sale cuando los dos habéis tocado Reservar. Sin Machine o sin respuesta: el to-do conserva su borrador de email con horas.

Solo se envía libre u ocupado, cifrado de extremo a extremo, para 14 días como mucho y redondeado a 15 minutos. Los eventos privados cuentan como ocupados. Una Machine solo puede preguntar si os habéis escrito en ambos sentidos. Configúralo en el panel Network en **Qué pueden preguntar otras Machines a la mía**: **Libre/ocupado para agendar** o **Desactivado**, con la duración, el margen y las horas preferidas. Cada solicitud aparece en Actividad, en Calendario.

## Una Machine en tu propio ordenador

Para unirte a la Network desde una Machine que gestionas tú:

1. En la página de tu cuenta en app.themachine.computer, pulsa **Vincular una Machine autoalojada**. El código funciona una vez, durante 15 minutos.
2. En tu ordenador, ejecuta `assistant fleet-pair` con el código y reinicia.

Hasta 5 Machines por cuenta. Cada una se puede desconectar desde ahí.
