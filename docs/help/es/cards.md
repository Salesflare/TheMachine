---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita tu atención, lista para que des el visto bueno. Esto es lo que significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e1656daff6fc566a
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo necesita tu atención. Una tarea por asunto, aunque abarque varios mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba, aparece un último paso que confirmaste, como enviar un formulario o resolver un problema, y que se completó mientras no estabas. Se queda ahí hasta que pulses **Entendido**, como máximo un día. También recibirás una notificación en el móvil.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (hay un borrador o resultado listo, y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero necesita que decidas o respondas; si no puede continuar o utilizarse sin algo que solo tú tienes, como un precio, un dato o una decisión, una línea bajo el título te lo explica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas que llevan una semana sin novedades (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, empezando por la más reciente y con la hora a la que se completó, como «Hecha hace 5 minutos». Las tareas que parecen terminadas aparecen como **Parece hecha**.

Después de enviar algo, una nota breve indica adónde ha ido la tarea, por ejemplo, «Enviado. Movida a Hecho» o «Enviado. Movida a Más tarde hasta el lun.». Si una respuesta solo promete hacer el trabajo, como «Lo enviaré el martes», la tarea sigue abierta: «Enviado. Sigue abierta». **Abrir** te lleva a ella. La búsqueda encuentra tareas por título o por la persona a quien se enviaron, también en Más tarde y Hecho.

En **Para ti**, primero aparecen las tareas vencidas o que vencen mañana como máximo, luego las preguntas de tu Fleet, después los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, se ordenan de más recientes a más antiguas. La tarea mantiene su sitio mientras tu Machine la prepara y cuando se termina: solo cambia su marca. En los demás grupos abiertos, primero aparecen las vencidas o las que vencen mañana como máximo; el resto se ordena de más reciente a más antigua. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que la tarea está terminada, por ejemplo, «PR #3451 merged», pero todavía no está cerrada. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si un mensaje indica que está terminada, se cierra automáticamente al cabo de un día y aparece **Deshacer**. Si no, espera a que pulses **Marcar como hecho**. Si ya has resuelto tú una tarea, por ejemplo, al responder en Gmail o Slack, también se cierra automáticamente.

Si un mensaje procede de una dirección que se parece a la de alguien que conoces, por ejemplo, sam@acme-corp.example en vez de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». Muestra la dirección real de esa persona, nunca el nombre que ha usado. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo ha escrito.

Si una tarea sigue dependiendo de otra persona, como una revisión o una respuesta, indica **Esperando a** esa tarea. Se queda en **Esperando a otros**, plegada encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre cuando has devuelto una pregunta: vuelve a aparecer la mañana anterior a la fecha límite, en la fecha límite si es más tarde hoy, o a la mañana siguiente si ya ha pasado. También indica a quién sigue esperando.

Si una tarea consiste en recibir un resultado de otra persona, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje indique que se ha recibido el resultado. Entonces se cierra automáticamente y aparece **Deshacer**. Si no llega nada cuando toca insistir, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Para cambiar qué cuenta como terminado, indícalo en el chat.

Si una tarea lleva una semana sin novedades, pasa de Para ti a **Más antiguos**, para que las tareas nuevas aparezcan primero después de unos días sin entrar. No hay novedades si no ha llegado ningún mensaje nuevo ni has hecho nada en la tarea, como enviar un mensaje por el chat, editarla o posponerla. Solo mirarla no cuenta.

Las tareas urgentes, las que vencen pronto y las que están a punto de enviarse siguen en Para ti. **Descartar todo** marca como innecesarias todas las tareas de Más antiguos tras una sola confirmación, igual que **No hace falta** permite hacerlo de una en una. Aparece **Deshacer**. Si llega algo nuevo, la tarea vuelve a Para ti.

Si nadie toca una tarea durante una semana, se pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y aparece **Deshacer**. **Mantener** la conserva y no vuelve a preguntarlo. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Abrirla, enviar un mensaje por el chat, editarla, posponerla o recibir un mensaje nuevo hace que vuelva a aparecer.

Una vez por semana, un proyecto que se haya quedado parado y no tenga nada pendiente puede recibir una tarea con un siguiente paso concreto, hasta un máximo de tres por semana. Consulta [Proyectos](projects.md).

Cuando nada necesita tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación ha fallado o se ha retrasado, lo verás en su línea, junto con **Revisar ahora**.

Las opciones **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo las de un tipo. El móvil y el ordenador muestran la misma selección. Si tienes activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como que una parte se reinicia continuamente, no es ni de Trabajo ni Personal, así que solo aparece en Todo.

La línea de la parte superior de la lista también te lleva directamente a la otra vista. En **Solo personal**, pulsa **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el resumen más reciente de la mañana o de la tarde y las tareas que incluye, por ejemplo, **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Púlsala para volver a leerlo. Con **Copiar** puedes copiarlo donde quieras. Cuando lo abres o pulsas la **×**, aparece en todos tus dispositivos hasta el siguiente resumen.

Si no hay ningún resumen reciente, aparece **Hoy hasta ahora**: lo que se ha terminado hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo de la categoría que hayas seleccionado.

Una tarea de un proyecto muestra el nombre del proyecto bajo el título. Púlsalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiar el proyecto o quitarlo. Consulta [Las tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También se mueve el acceso a los mensajes que puede leer y enviar. **Deshacer**, en la nota, la devuelve a su sitio.

Si una tarea necesita tu otra área para continuar y todos los mensajes relacionados proceden de esa área, se mueve allí automáticamente y sigue adelante. Si no, aparece **Mover a Trabajo** y no se mueve nada hasta que lo pulses. Si has creado una tarea sin elegir Trabajo o Personal, se mueve automáticamente cuando encuentra dónde corresponde. Hasta entonces, no aparece en Trabajo ni en Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita leer otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. Los correos de otra de tus empresas van a las tareas de esa empresa. Una tarea sobre tu vida personal, como un mensaje de tu familia enviado a tu dirección del trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp, un pedido en tu buzón personal o una [promesa](promises.md) relacionada con el trabajo, es de Trabajo desde el principio.

Una tarea que hayas movido o asignado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, pero no adónde se envía la respuesta: siempre se responde en la conversación correspondiente, aunque la tarea se haya movido, salvo que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección del trabajo a la que llegó el correo, y nunca aparece en un Fleet de trabajo ni en Graph del equipo.

Si hay dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, te permite ir pasando por ellas de una en una, en el orden de la lista. Verás el borrador completo de cada una, con **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Intro envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el proceso. El encabezado indica cuánto tardarás a tu ritmo, por ejemplo, «unos 2 min».

Al terminar, se cuentan las tareas enviadas o cerradas y las que aún se están preparando.

Las tareas que te hacen una pregunta no se incluyen en ninguna de las dos opciones: necesitan una respuesta tuya, no que pulses un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, dentro de la hora siguiente.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan. Los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Conexiones, las comprobaciones muestran «Pausadas por la noche. Se pondrán al día a las 06:30». Si de noche haces clic, escribes, te desplazas por la app, escribes en el chat o pulsas una tarea, las comprobaciones se reanudan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre inicia una comprobación al momento.

**Revisar ahora** lee todas las fuentes al momento. Si no tienes tareas abiertas, pulsa la línea de tu Machine para verla y acceder a **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, aparece arriba en el ordenador. Allí solo aparece una línea breve mientras se ejecuta una comprobación o si alguna ha fallado o se ha retrasado. También puedes preguntarlo en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que ha encontrado en todas las fuentes que ha leído, por ejemplo, «13 mensajes revisados a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». Solo se refiere a esa comprobación: las tareas que ya tenías siguen pendientes como antes. Si una tarea nueva espera a un mejor momento, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Pulsa la línea para ver cada hilo de correo, chat y notificación con el icono de su fuente: quién lo ha escrito, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo está en copia, un compañero está respondiendo» o «La reunión ya está programada para el jueves». Si la comprobación solo ha dado un motivo impreciso, no se muestra ninguno junto al hilo. Pulsa uno para leerlo y ver lo que se ha dicho a su alrededor.

Se muestran los 10 primeros. Pulsa debajo para ver el resto. El número que aparece junto a un nombre, como (3), indica cuántos mensajes nuevos hay en ese chat. Las notificaciones del móvil de un mensaje que ya aparece en la lista solo se muestran una vez. La línea permanece visible durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para tener en cuenta el contexto y las promesas, pero no cuentan como correo nuevo. Tu Machine nunca lee ni muestra los correos que te envía, como el resumen de la mañana o un aviso de reparación. Los correos sobre facturación, el periodo de prueba o una invitación se leen con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, junto a **Posponer**. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué hay que cambiar: cómo hacerlo o, cuando ya hay un borrador, qué modificar en él. **Marcar como hecho** indica que ya está resuelta. Aparece directamente en una tarea lista sin borrador o en una que te hace una pregunta. En los demás casos está en la parte superior de **…**. La tarea desaparece de la lista al momento y aparece **Deshacer** en el mensaje. Desliza el mensaje para quitarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se guarda.

Si quieres que se haga de otra manera, díselo en su **Chat**. La respuesta indica solo qué ha cambiado, por ejemplo, que se ha pospuesto y hasta cuándo. Si no ha podido cambiar algo, como la fecha límite, te lo dice.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: la tarea [vuelve a aparecer con cierta frecuencia](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, indica por qué: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Pulsa el título o **Nombre**, en **Detalles**, para cambiarlo. También puedes pedirlo en el chat de la tarea, por ejemplo, «Cámbiale el nombre a…». El título que elijas se mantiene.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve a aparecer automáticamente si ocurre algo nuevo, como recibir un mensaje de esa persona, pero no si respondes tú. En ese caso, indica cuándo ha vuelto y aparece en la lista como nueva. El chat continúa donde lo dejaste, aunque hayan pasado semanas.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluye. Las facturas que se pagan automáticamente, como las domiciliadas o las que se cargan en una tarjeta guardada, no se convierten en tareas. Si un correo posterior indica que se ha pagado, por ejemplo, porque el remitente confirma que ha recibido el pago, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Una tarea que solo importa hasta una hora concreta, como una confirmación antes de una reunión, se cierra automáticamente cuando pasa esa hora. Pasa a **Hecho / descartado** como «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de que un mensaje o un traspaso para otra persona aparezca como listo, tu Machine revisa los chats recientes que tienes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está resuelto, por ejemplo, porque se lo habían pedido y ha dicho que sí, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Si otra persona ha escrito en la misma conversación después de que se preparara el borrador, **Enviar** lo deja en espera: «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** otra vez para enviar el borrador tal cual.

Si un mensaje nuevo cambia el plan, por ejemplo, porque la fiesta se traslada a otro sitio o se cancela una reserva, The Machine actualiza las tareas automáticamente. Si una tarea sigue haciendo falta, se adapta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** como «No hace falta». En el chat aparece «Actualizado:» seguido del motivo, y **Deshacer** la recupera durante un día.

En tus primeras tareas aparece un consejo breve sobre las acciones más importantes: **Pedir cambios** y **No hace falta**, y sobre cómo no se envía nada hasta que pulses **Enviar**. El consejo desaparece definitivamente cuando usas el botón correspondiente o pulsas ×.

El primer día, la parte superior de Tareas te da la bienvenida y te dice quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, si es de Trabajo o Personal y cuándo llegó. Pulsa un nombre para abrir su página en Graph.

Si Graph tiene una foto o un logotipo de una persona o una organización, lo muestra. Si no, muestra sus iniciales. Si un logotipo no se distingue bien en tamaño pequeño, por ejemplo, si es blanco sobre fondo transparente o tiene el nombre en una línea larga, también muestra la inicial.

A veces, una línea discreta indica algo que no se sabe, como «Último contacto hace 12 días por correo; nada desde entonces». Aparece cuando el último intercambio con esa persona es antiguo o no ha tenido respuesta. También indica los canales que no están conectados, como WhatsApp. Tu Machine explica lo que no sabe en vez de hacer suposiciones.

Si se menciona un canal que no está conectado, pulsa Conectar junto a él para abrir esa conexión.

El título indica lo que hay que hacer y solo cambia si eso cambia. Una tarea terminada conserva el título y muestra debajo cómo terminó, por ejemplo, «Hecha: Sam la firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede y muestra el logotipo del servicio. Púlsala para leer el hilo. El borrador muestra el logotipo del destino, para que veas enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que alguien ha dicho en otro sitio, como una sugerencia de un compañero en Slack, una línea lo indica, por ejemplo, «Basado en un mensaje de Sam en #ops». Púlsala para leer el mensaje. Desaparece cuando una actualización reemplaza el borrador.

Un chat (Slack, WhatsApp, Telegram, Intercom…) aparece como una sola conversación, de los mensajes más antiguos a los más recientes: los mensajes anteriores al que corresponde la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, igual que en la app. El mensaje de la tarea aparece marcado como «Esta tarea» y se abre directamente. **Mostrar mensajes anteriores** añade mensajes más antiguos. En un correo, el resto del hilo aparece plegado por encima y por debajo.

Puedes abrir un mensaje de la misma forma desde la búsqueda, Graph, las respuestas de Ask o la última comprobación. Aparece marcado como «Este mensaje» o «Mensajes nuevos».

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, lo abre en la app de Gmail si la tienes instalada.

En **Detalles**, los correos muestran solo la información que no aparece en el encabezado, como las direcciones completas de Cc, Cco o una dirección de respuesta distinta. Si no hay nada más que añadir, no aparece ninguna.

Las respuestas en un hilo de Slack también muestran lo que se dijo antes de que empezara el hilo. El enlace de la tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** abajo.

**Detalles** muestra el nombre, el proyecto y el área (pulsa uno para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Las tareas terminadas se muestran de forma resumida. El mensaje del que procede aparece en **Detalles**.

Una tarea que indica «Esperando a» enlaza al último mensaje que le enviaste a esa persona y cuya respuesta estás esperando, por ejemplo, «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea**, debajo de **Buscar** en un ordenador, **+** en un móvil o `N`, añade una tarea para cualquier cosa. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, se asigna al área que corresponda según la persona y el asunto. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie.», «3 nov.», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve a aparecer con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula hasta 5 personas u organizaciones relacionadas con la tarea.
- Icono de mensaje: adjunta el mensaje al que se refiere, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro que tenga The Machine. Busca por texto o remitente. Cada resultado muestra de dónde procede, quién lo envió y cuándo.
- **Archivos**: pulsa el clip, pega una captura de pantalla o arrastra archivos al formulario. En un móvil, puedes hacer una foto con la cámara de al lado. Puedes adjuntar hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Pulsa × para quitar uno.

Los archivos se quedan en la tarea y The Machine los lee cuando trabaja en ella. No hace falta nada más: puede crear la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como miniaturas. Púlsalas para verlas a tamaño completo.
