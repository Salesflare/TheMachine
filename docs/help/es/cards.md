---
title: Tareas
area: cards
summary: Una tarea por cada asunto que requiere tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 51db64e67403d2ea
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo requiere tu atención. Una tarea por asunto, aunque abarque muchos mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba aparece el último paso que confirmaste, como un formulario o una incidencia, que se completó mientras no estabas. Se queda ahí hasta que toques **Entendido**, como máximo un día, y también te avisamos en el móvil.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero requiere que tomes una decisión o respondas; si el trabajo se ha detenido por algo que solo tú tienes, como un dato, un inicio de sesión o una decisión, aparece una línea debajo del título que lo explica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe que no requiere ninguna decisión).
- **Más antiguos**: tareas plegadas que no han tenido novedades durante una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que has prometido y lo que otras personas te han prometido. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con la hora a la que terminaron, como «Hecho hace 5 minutos». Las tareas que parecen estar terminadas aparecen marcadas como **Parece hecha**.

Después de enviar algo, una nota breve indica dónde ha ido la tarea, como «Enviado. Movido a Hecho» o «Enviado. Movido a Más tarde hasta el lunes». Si una respuesta solo promete hacer el trabajo, como «Lo enviaré el martes», la tarea sigue abierta: «Enviado. Se ha mantenido abierta». **Abrir** te lleva a la tarea. La búsqueda encuentra tareas por su título o por la persona a quien se enviaron, también en Más tarde y Hecho.

**Para ti** muestra primero lo que está vencido o vence mañana, después las preguntas de tu Fleet, las tareas de seguimiento de un tablero y, por último, el resto. Dentro de cada grupo, aparecen primero las más recientes. La tarea mantiene su sitio mientras tu Machine la prepara y cuando se termina: solo cambia su marca. En los demás grupos abiertos, aparecen primero las tareas vencidas o que vencen mañana, y después el resto, de la más reciente a la más antigua. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está terminada, como «PR #3451 combinado», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Nunca aparece como atrasada. Si se muestra en un mensaje, se cierra automáticamente al cabo de un día y aparece **Deshacer**. Si no, espera a que toques **Marcar como hecho**. Las tareas que ya has resuelto por tu cuenta, por ejemplo respondiendo en Gmail o Slack, también se cierran automáticamente.

Si el mensaje viene de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en vez de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que haya usado. Tu Machine comprueba estos mensajes con la persona de la dirección que ya tienes, nunca con quien los ha escrito.

Si una tarea sigue pendiente de otra persona, por ejemplo de una revisión o una respuesta, indica el paso pendiente con **Esperando a:**. Aparece plegada en **Esperando a otros**, por encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que hayas respondido a una pregunta: la tarea vuelve a aparecer la mañana anterior a la fecha límite, en la fecha límite si es más tarde ese mismo día, o a la mañana siguiente si la fecha ya ha pasado. También indica de quién sigue pendiente.

Si la tarea depende de un resultado que tiene que entregar otra persona, como un contrato firmado, en **Detalles** aparece **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje indique que ya se ha entregado el resultado. Entonces se cierra automáticamente y aparece **Deshacer**. Si no llega nada cuando toca insistir, la tarea vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como terminado para cambiarlo.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que las nuevas aparezcan primero cuando vuelvas después de unos días. No hay novedades cuando no llega ningún mensaje nuevo y tú tampoco haces nada en la tarea, como enviar un mensaje en el chat, editarla o posponerla. Solo mirarla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca como no necesarias todas las tareas de Más antiguos tras una sola confirmación, igual que **No hace falta** permite hacerlo de una en una. Aparece **Deshacer**. Si una tarea recibe novedades, vuelve a Para ti.

Si nadie interactúa con una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y aparece **Deshacer**. **Mantener** la conserva y no vuelve a preguntarlo. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Abrirla, enviar un mensaje en el chat, editarla, posponerla o recibir un mensaje nuevo hace que vuelva a aparecer.

Una vez por semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede generar una tarea con un único paso siguiente concreto, hasta un máximo de tres por semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine se queda en reposo y la lista está vacía. Mientras comprueba las fuentes, se activa y te lo indica. Si una comprobación falla o se retrasa, lo verás en una línea con **Revisar ahora** debajo.

Las opciones **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo las de un tipo. El móvil y el ordenador muestran la misma opción. Si tienes activado Trabajo o Personal, **Mostrar todo** vuelve a la lista completa. Una alerta sobre tu Machine, como que una parte se reinicia continuamente, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también te lleva directamente a la otra opción: si está activado **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista indica cuál fue tu último resumen de la mañana o de la tarde y qué incluía, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leer el resumen y usar **Copiar** para pegarlo donde quieras. Cuando lo abres o tocas su **×**, aparece en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha terminado hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo de la opción que hayas filtrado.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Las tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a la otra área. También cambia de área lo que puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita cambiar de área para continuar y todos los mensajes de los que procede están allí, se mueve automáticamente y sigue adelante. Si no, aparece **Mover a Trabajo** y no se mueve hasta que lo toques. Una tarea que hayas añadido sin elegir Trabajo o Personal se mueve automáticamente cuando encuentra el área que le corresponde. Hasta entonces no indica ni Trabajo ni Personal, y sigue siendo privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. Los correos de otras empresas tuyas van a las tareas de esa empresa. Las tareas sobre tu vida personal, como un mensaje de un familiar a tu dirección de trabajo, son Personales desde el principio.

El trabajo que te llega a una cuenta personal, como el de un cliente por WhatsApp o un pedido en tu buzón personal, es de Trabajo desde el principio. Una tarea que hayas movido o asignado tú se queda siempre donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, pero no dónde responde: la respuesta siempre va a la conversación original, también después de moverla, a menos que elijas otra forma.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo, y nunca aparece en un Fleet de trabajo ni en el Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar** en el encabezado de Para ti te permite recorrerlas de una en una, en el orden de la lista, con cada borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Intro envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el recorrido. El encabezado indica cuánto tardarás a tu ritmo, como «unos 2 min».

Al terminar, indica cuántas tareas se han enviado o cerrado y cuántas siguen preparándose.

Las tareas que te hacen una pregunta no se incluyen: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes cuando hay 40 sin revisar o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en el plazo de una hora.

Por la noche, desde las 00:00 hasta las 06:30, las comprobaciones se pausan. Los mensajes nuevos se siguen leyendo y guardando, y se comprueban juntos a las 06:30 para que las tareas estén listas antes del resumen de la mañana. En Comprobaciones, en Conexiones, aparece «Pausadas por la noche; se reanudan a las 06:30». Si haces clic, escribes o desplazas la pantalla en la app, escribes en el chat o tocas una tarea durante la noche, las comprobaciones se ejecutan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre inicia una comprobación al momento.

**Revisar ahora** lee todas las fuentes al momento. Si no tienes tareas abiertas, toca la línea de tu Machine para verla junto con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, aparece arriba del todo en el ordenador. Solo se muestra una línea breve mientras se realiza una comprobación, o si ha fallado o se ha retrasado. También puedes pedirlo por chat.

LinkedIn, X y Salesflare mantienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea sobre tus tareas que indica qué ha encontrado en cada fuente que ha leído, como «13 mensajes revisados a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». Solo se refiere a esa comprobación: las tareas que ya están en tu lista siguen pendientes. Si una tarea nueva espera al momento oportuno, como el resumen de la mañana, indica hasta cuándo: «1 tarea en espera hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién lo ha escrito, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo estabas en copia; responde un compañero» o «La reunión ya está programada para el jueves». Si la comprobación solo indicó un motivo impreciso, el hilo no muestra ninguno. Toca uno para leerlo.

Se muestran los 10 primeros; toca debajo para ver el resto. Un número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Las notificaciones del móvil sobre mensajes que ya aparecen en la lista solo se muestran una vez. La línea permanece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tu Machine lee tus propias respuestas para entender el contexto y las promesas, pero no las cuenta como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de una reparación, nunca se leen ni se muestran en la lista. El correo sobre la facturación, tu periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué cambiar: cómo hacerlo o, cuando haya un borrador listo, qué cambiar en él. **Marcar como hecho** indica que ya está resuelta. Aparece a la vista en una tarea lista sin borrador o en una que te hace una pregunta; en los demás casos, está en la parte superior de **…**. La tarea desaparece de la lista al momento y aparece **Deshacer** en el mensaje. Desliza el mensaje para apartarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Para que se haga de otra manera, dilo en su **Chat**. La respuesta solo indica lo que ha cambiado, por ejemplo que se ha pospuesto y hasta cuándo. Si no se ha podido cambiar algo, como la fecha de vencimiento, te lo dice.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve a aparecer con una frecuencia fija](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, elige un motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarle el nombre. También puedes pedírselo en el chat, por ejemplo: «Cámbiale el nombre a…». El título se conserva.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve a aparecer automáticamente cuando ocurre algo nuevo, como recibir un mensaje de esa persona, pero no cuando respondes tú. En ese caso, indica cuándo ha vuelto y se ordena como nueva. El chat continúa donde lo dejaste, aunque hayan pasado semanas.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que aparecen en la factura. Las facturas que se pagan automáticamente, como las domiciliadas o las de una tarjeta guardada, no. Cuando un correo posterior indique que ya está pagada, por ejemplo si quien la envió confirma que ha recibido el pago, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Una tarea que solo era relevante hasta una hora concreta, como una confirmación antes de una reunión, se cierra automáticamente cuando pasa esa hora. Se mueve a **Hecho / descartado** con el estado «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de que un mensaje o un traspaso para otra persona aparezca como listo, tu Machine comprueba los chats recientes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo porque se lo pidieron y dijo que sí, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Si otra persona escribe en la misma conversación después de que se haya creado tu borrador, **Enviar** lo detiene: «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** otra vez para enviar el borrador tal como está.

Si un mensaje nuevo cambia el plan, por ejemplo porque una fiesta se traslada a otro sitio o se cancela una reserva, The Machine actualiza las tareas por su cuenta. Si una tarea sigue siendo necesaria, se adapta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** con el estado «No hace falta», su chat indica «Actualizado:» y el motivo, y **Deshacer** la recupera durante un día.

En tus primeras tareas, aparece un consejo breve con las acciones clave: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece definitivamente cuando usas el botón o pulsas ×.

El primer día, la parte superior de Tareas te saluda y te indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización si es relevante (no solo porque alguien trabaje allí), el proyecto, si es de Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si aparece en Graph; de lo contrario, muestran sus iniciales. Si un logotipo no se distingue en ese tamaño, por ejemplo porque es blanco sobre fondo transparente o porque es un nombre ancho, también se muestran las iniciales.

A veces aparece una línea tenue que indica qué no se sabe, como «Último contacto hace 12 días por correo; no hay novedades». Se muestra cuando hace tiempo que no hay noticias de esa persona o cuando una respuesta sigue pendiente. También indica los canales que no están conectados, como WhatsApp. Tu Machine dice lo que no sabe en vez de hacer suposiciones.

Si menciona un canal que no está conectado, toca Conectar al lado para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si cambia la tarea. Las tareas terminadas conservan el título y muestran debajo cómo terminaron, como «Hecho: Sam lo firmó el martes».

Sobre el borrador aparece una línea tenue que indica de qué mensaje procede y muestra el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del lugar al que se enviará, para que veas enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en la aportación de alguien en otro sitio, como una sugerencia de un compañero en Slack, aparece una línea que lo indica, como «Basado en un mensaje de Sam en #ops». Tócala para leer el mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) aparece como una conversación, del mensaje más antiguo al más reciente: incluye los mensajes anteriores al que originó la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, igual que en la app. El mensaje relacionado con la tarea está marcado como «Esta tarea» y se abre a la vista. **Mostrar mensajes anteriores** añade mensajes más antiguos. Los mensajes anteriores y posteriores de un hilo de correo aparecen plegados.

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, se abre en la app de Gmail si la tienes.

En **Detalles** de un correo solo aparecen los datos que no están en el encabezado, como las direcciones completas de Cc, Bcc o una dirección de respuesta distinta. Si no hay nada más que añadir, no aparecen.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre, el proyecto y el área (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Las tareas terminadas se muestran de forma breve; el mensaje del que proceden aparece en **Detalles**.

Una tarea de «Esperando a» enlaza con tu último mensaje a esa persona, cuya respuesta estás esperando: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un móvil o `N`) añade una tarea para cualquier cosa. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, se asigna al área que le corresponde por la persona y el asunto. También encuentra el correo al que hace seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo viernes», «3 nov», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario incluye opciones rápidas y **Elegir fecha**.
- **Se repite**: vuelve a aparecer con una frecuencia fija. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula las personas o empresas relacionadas, hasta un máximo de 5.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En un móvil, la cámara que aparece al lado permite hacer una foto. Puedes añadir hasta 5 archivos, como en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Toca × para quitar uno.

Los archivos se quedan con la tarea y The Machine los lee cuando trabaja en ella. No hace falta añadir nada más: puede rellenar la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas; tócalas para verlas a tamaño completo.
