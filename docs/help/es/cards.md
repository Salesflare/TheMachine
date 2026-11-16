---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 6cbbad37c4dfaf07
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo necesita tu atención. Una tarea por asunto, aunque haya muchos mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba, muestra el último paso que confirmaste, como enviar un formulario o resolver un problema, que se completó mientras no estabas. Se queda ahí hasta que toques **Entendido**, como máximo un día, y también te llega al teléfono.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (el trabajo está hecho y **Hazlo** o **Enviar** lo pone en marcha), **Te necesita** (primero necesita que decidas o respondas), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso le toca a otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otros te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, empezando por la más reciente, con el momento en que terminaron, como «Hecho hace 5 minutos». Las tareas que parecen terminadas ya llevan la marca **Parece hecho**.

Después de enviar algo, aparece una nota breve que indica adónde fue la tarea, como «Enviado. Se movió a Hecho» o «Enviado. Se movió a Más tarde hasta el lun.». **Abrir** te lleva a la tarea. La búsqueda encuentra tareas por su título o por la persona a quien se enviaron, también en Más tarde y Hecho.

En **Para ti**, primero aparecen las tareas vencidas o que vencen mañana; después, las preguntas de tu Fleet, los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, primero aparecen las más recientes. La tarea conserva su lugar mientras tu Machine la prepara y cuando termina: solo cambia su marca. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana y, después, el resto, empezando por las más recientes. La barra lateral mantiene el mismo orden.

**Parece hecho** significa que tu Machine ve que ya se terminó, como «PR n.º 3451 fusionada», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Al cabo de un día, se cierra automáticamente y puedes **Deshacer**. Una tarea que ya resolviste por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierra automáticamente.

Si un mensaje viene de una dirección que se parece a la de alguien que conoces, como sam@acme-corp.example en vez de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La persona aparece con su dirección, nunca con el nombre que usó. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo escribió.

Si una tarea sigue pendiente de otra persona, como una revisión o una respuesta, indica **Esperando a:** ese paso. Aparece plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que respondas con una pregunta: vuelve a aparecer la mañana anterior a la fecha límite, el mismo día de la fecha límite si es más tarde, o a la mañana siguiente si ya pasó. También indica quién tiene que responder.

Si una tarea depende de un resultado que debe entregar otra persona, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no la cierra: permanece en **Esperando a otros** hasta que un mensaje indique que se completó el resultado. Entonces se cierra automáticamente y puedes **Deshacer**. Si no llega nada para cuando toque hacer seguimiento, la tarea vuelve con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como terminado para cambiarlo.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y puedes **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Al abrirla, enviar un mensaje en el chat, editarla, posponerla o recibir un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que se haya quedado inactivo y no tenga tareas abiertas puede recibir una tarea con un siguiente paso concreto, hasta tres por semana. Consulta [Proyectos](projects.md).

Cuando nada necesita tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, aparece en su línea, con **Revisar ahora** debajo.

Las opciones **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo las de un tipo. El teléfono y el ordenador muestran la misma selección. Si tienes activada la vista de Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como que un componente se reinicie continuamente, no es ni de Trabajo ni Personal, así que solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente a la otra vista: en **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el nombre de tu último resumen de la mañana o de la tarde y lo que incluía, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leerlo y usa **Copiar** para pegarlo donde quieras. Cuando lo abras o toques la **×**, estará disponible en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se hizo hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo de la opción que hayas elegido.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. En **Detalles**, **Proyecto** permite cambiarlo o quitarlo. Consulta [las tareas de un proyecto](projects.md#a-project-s-to-dos).

En **Detalles**, **Área** mueve una tarea a tu otra área. También cambia el área de la que puede leer mensajes y desde la que puede enviar. **Deshacer** en la nota la devuelve a su área anterior.

Si una tarea necesita tu otra área para continuar y todos los mensajes relacionados están allí, se mueve a esa área automáticamente y continúa. De lo contrario, aparece **Mover a Trabajo** y no se mueve hasta que lo toques. Una tarea que añadiste sin elegir Trabajo o Personal se mueve automáticamente cuando encuentra el área a la que pertenece. Hasta entonces, no indica ni Trabajo ni Personal, y sigue siendo privada.

Una tarea siempre puede leer los mensajes de los que surgió. Si necesita otros mensajes de tu otra área, te pregunta con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. El correo de otras empresas tuyas va a las tareas de esa empresa. Y una tarea sobre tu vida personal, como un mensaje familiar que llega a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp o un pedido en tu buzón personal, es Trabajo desde el principio. Una tarea que hayas movido o colocado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece la tarea y con quién se comparte, nunca desde dónde responde: la respuesta siempre va a la conversación correspondiente, incluso después de moverla, a menos que elijas otra opción.

Si una tarea Personal sigue respondiendo desde la dirección de trabajo a la que llegó el correo, nunca aparece en una Fleet de Trabajo ni en el Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar** en el encabezado de Para ti te permite revisarlas de una en una, en el orden de la lista, con el borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Intro envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el proceso. Debajo del título, el encabezado también indica cuánto tardarás si vas a tu ritmo, como «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen: necesitan una respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes recibidos cuando hay 40 pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en menos de una hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «Pausa nocturna. Se pondrá al día a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en el chat o tocas una tarea, las comprobaciones se reanudan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba todo de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no hay tareas abiertas, toca la línea de tu Machine para verla, con **Detalles**, que abre Comprobaciones en Conexiones. Si hay tareas abiertas, aparece arriba en el ordenador. Allí solo aparece una línea breve mientras se realiza una comprobación, o si alguna falla o se retrasa. También puedes preguntarle en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas que indica lo que encontró en cada fuente que leyó, como «Se comprobaron 13 mensajes a las 16:11 · nada necesita tu atención» o «· 2 tareas nuevas». Si una tarea nueva debe esperar a un mejor momento, como el resumen de la mañana, indica hasta cuándo: «1 tarea en espera hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién escribió, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo estaba en copia; responde un compañero» o «La reunión ya está programada para el jueves». Si la comprobación solo dio un motivo impreciso, no se muestra ninguno. Toca un elemento para leerlo.

Se muestran los 10 primeros. Toca debajo para ver el resto. Un número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. La notificación del teléfono sobre un mensaje que ya aparece en la lista solo se muestra una vez. La línea permanece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Nunca se leen ni se incluyen los propios correos de The Machine, como el resumen de la mañana o un aviso de solución. El correo sobre la facturación, tu prueba o una invitación sí se lee con normalidad.

## Los botones

Una tarea muestra su siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** te permite indicar qué cambiar: cómo hacer la tarea o, cuando el borrador ya esté listo, qué cambiar en él. **Marcar como hecha** indica que ya está resuelta: aparece a la vista en las tareas preparadas sin borrador; en los demás casos, está arriba en **…**, también en las tareas que necesitan que decidas. La tarea sale de la lista de inmediato y aparece **Deshacer** en el mensaje. Desliza el mensaje para descartarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Para que se haga de otra forma, díselo en su **Chat**.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: la tarea [vuelve con cierta frecuencia](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, indica el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre** en **Detalles** para cambiarlo. El título que elijas se mantiene.

**Reabrir** devuelve una tarea cerrada. También vuelve a aparecer automáticamente cuando ocurre algo nuevo, como recibir un mensaje de esa persona, pero no cuando respondes tú.

Una factura que aún tengas que pagar personalmente, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que figuran en ella. Las facturas que se pagan automáticamente, como un débito directo o una tarjeta guardada, no se convierten en tareas. Si un correo posterior indica que ya se pagó, por ejemplo, porque el remitente confirma que recibió el pago, la tarea se cierra automáticamente. **Deshacer** la devuelve durante un día.

Una tarea que solo importa hasta cierta hora, como una confirmación antes de una reunión, se cierra automáticamente después de esa hora. Pasa a **Hecho / descartado** como «Ya no hace falta». **Deshacer** la devuelve durante un día.

Antes de que un mensaje o un traspaso para otra persona aparezca como preparado, tu Machine revisa los chats recientes con las personas que participan, también los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya se resolvió, por ejemplo, porque se lo pidieron y dijo que sí, la tarea se cierra automáticamente. **Deshacer** la devuelve durante un día.

Si un mensaje nuevo cambia el plan, como cuando una fiesta se traslada a otro lugar o se cancela una reserva, The Machine actualiza sus tareas automáticamente. Si todavía hace falta hacer algo, la tarea se adapta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** como «No hace falta». En su chat aparece «Actualizado:» seguido del motivo, y **Deshacer** la devuelve durante un día.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**. También te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece definitivamente cuando usas el botón o pulsas ×.

El primer día, en la parte superior de Tareas aparece un saludo que indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de abajo indica de quién se trata, la organización si corresponde (no solo porque esa persona trabaje allí), el proyecto, Trabajo o Personal, y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno, y sus iniciales si no. Si un logotipo no se ve bien a ese tamaño, por ejemplo, porque es blanco sobre fondo transparente o porque es un logotipo alargado con el nombre, también se muestran las iniciales.

A veces aparece una línea discreta que indica lo que no se sabe, como «Último contacto hace 12 días por correo; no hubo nada después». Aparece cuando el último contacto es antiguo o no tuvo respuesta, y menciona los canales que no están conectados, como WhatsApp. Tu Machine indica lo que no sabe en vez de hacer suposiciones.

Si menciona un canal que no está conectado, junto a él aparece Conectar para abrir esa conexión.

El título indica lo que hay que hacer y solo cambia cuando eso cambia. Una tarea hecha conserva su título y muestra debajo cómo terminó, como «Hecho: Sam lo firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje viene, con el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del servicio al que se enviará, para que veas enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que alguien dijo en otro lugar, como la sugerencia de un compañero en Slack, una línea lo indica, por ejemplo, «Basado en un mensaje de Sam en #ops». Tócala para leer el mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) aparece como una conversación, de más antiguo a más reciente: muestra los mensajes anteriores al que dio lugar a la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje relacionado con la tarea lleva la marca «Esta tarea» y se abre en la conversación. **Mostrar mensajes anteriores** añade los mensajes más antiguos. En un correo, el resto del hilo aparece plegado encima y debajo.

En **Detalles** de un correo solo aparecen los datos que no figuran en el encabezado, como las direcciones completas en Cc, Cco o una dirección de respuesta distinta. Si no hay nada más que añadir, no aparece ningún detalle.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** abajo.

**Detalles** muestra el nombre, el proyecto y el área (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Una tarea hecha se muestra de forma resumida; el mensaje que la originó está en **Detalles**.

Una tarea que indica que está esperando a alguien enlaza al último mensaje que le enviaste y cuya respuesta esperas, por ejemplo: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un teléfono o `N`) añade una tarea para cualquier cosa. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, se coloca donde corresponda según de quién y de qué se trate. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «en 2 horas». También puedes escribirlo en tu idioma. El icono del calendario muestra opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula a las personas o empresas relacionadas, hasta 5.
- Icono de mensaje: adjunta el mensaje relacionado, como un correo, un mensaje de Slack, Teams, WhatsApp o Telegram, o cualquier otro mensaje que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde viene, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En un teléfono, la cámara que aparece al lado permite sacar una foto. Puedes añadir hasta 5 archivos, como en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Toca × para quitar un archivo.

Los archivos se quedan con la tarea y The Machine los lee cuando trabaja en ella. Puedes añadir solo archivos: The Machine completa la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas a tamaño completo.
