---
title: Tareas
area: cards
summary: Una tarea por cada asunto que requiere tu atención, lista para que des el visto bueno. Esto es lo que significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 32c3a3e62b74548f
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo requiere tu atención. Una tarea por asunto, aunque incluya varios mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba del todo, muestra el último paso que confirmaste, como enviar un formulario o resolver un problema, y que se completó mientras no estabas. Se queda hasta que toques **Entendido**, como máximo durante un día, y también aparece en tu móvil.
- **Para ti**: todo lo que está pendiente de ti, primero lo que vence mañana o antes. Cada tarea indica si está **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo pone en marcha), **Te necesita** (primero necesita que decidas o respondas; si no se puede continuar o usar el resultado sin algo que solo tú sabes, como un precio, un dato o una decisión, aparece una línea debajo del título que lo explica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe que no requiere ninguna decisión).
- **Más antiguos**: tareas plegadas que no han tenido novedades en una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que has prometido y lo que otras personas te han prometido. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con la hora a la que se terminaron, como «Hecho hace 5 minutos». Las tareas que parecen terminadas ya aparecen como **Parece hecha**.

Después de enviar algo, aparece una nota breve que indica adónde fue la tarea, como «Enviado. Se ha movido a Hecho» o «Enviado. Se ha movido a Más tarde hasta el lunes». Si una respuesta solo promete que se hará el trabajo, como «Lo enviaré el martes», la tarea sigue abierta: «Enviado. Se ha mantenido abierta». **Abrir** te lleva a la tarea. La búsqueda encuentra tareas por su título o por la persona a quien se enviaron, también en Más tarde y Hecho.

En **Para ti** aparecen primero las tareas vencidas o que vencen mañana o antes, luego las preguntas de tu Fleet, después los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, aparecen de más reciente a más antigua. La tarea conserva su sitio mientras tu Machine la prepara y cuando se termina: solo cambia su marca. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana o antes, y después el resto, de más reciente a más antigua. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que está terminada, como «PR #3451 fusionada», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si aparece un mensaje que lo confirma, se cierra automáticamente al cabo de un día y puedes **Deshacer**. Si no, espera a que uses **Marcar como hecho**.

Las tareas que ya has resuelto por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierran automáticamente. Una respuesta que diga que se adjunta un archivo cuando no hay ninguno no la cierra.

Si un mensaje viene de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en vez de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que ha usado. Tu Machine comprueba estos mensajes con la persona de la dirección que ya tienes, nunca con quien los ha escrito.

Si una tarea sigue pendiente de otra persona, por ejemplo, de una revisión o una respuesta, indica el paso pendiente con **Esperando a:**. Aparece plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la haga aparecer de nuevo. Lo mismo ocurre si has respondido con una pregunta: la tarea vuelve a aparecer la mañana antes de la fecha límite, en la fecha límite si es más tarde ese mismo día o a la mañana siguiente si ya ha pasado. También indica de quién sigue esperando una respuesta.

Si una tarea depende de un resultado que entregará otra persona, como un contrato firmado, **Detalles** lo indica en **Hecho cuando**. Enviar tu parte no cierra la tarea: se queda en **Esperando a otros** hasta que un mensaje muestre el resultado. Entonces se cierra automáticamente y puedes **Deshacer**. Si no llega nada cuando toque insistir, la tarea vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Para cambiar qué cuenta como terminado, indícalo en el chat.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que las nuevas aparezcan primero después de unos días sin entrar. No hay novedades si no hay ningún mensaje nuevo sobre la tarea ni has hecho nada en ella, como enviar un mensaje por chat, editarla o posponerla. Abrirla no cuenta.

Las tareas urgentes, las que vencen pronto y las que están a punto de enviarse se quedan en Para ti. **Descartar todo** marca todas las tareas de Más antiguos como innecesarias después de una sola confirmación, igual que **No hace falta** permite hacerlo de una en una, y puedes **Deshacer**. Si hay novedades en una tarea, vuelve a Para ti.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y puedes **Deshacer**. **Mantener** la conserva y no vuelve a preguntarte. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, envías un mensaje por el chat, la editas, la pospones o llega un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que se haya quedado parado y no tenga nada abierto puede generar una tarea con un siguiente paso concreto. Como máximo, tres por semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine descansa y deja la lista vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, lo indica en la línea y muestra **Revisar ahora** debajo.

Las opciones **Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, muestran todas las tareas o solo las de un tipo. En tu móvil y tu ordenador aparece la misma selección. Si tienes Trabajo o Personal activado, **Mostrar todo** vuelve a la vista general. Una alerta sobre tu Machine, como que un componente se reinicia constantemente, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también te permite cambiar directamente a la otra vista: en **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el nombre de tu último resumen de la mañana o de la tarde y lo que incluye, como **Resumen de ayer por la tarde** · 12 terminadas, 3 abiertas. Tócala para volver a leer el resumen, con la opción **Copiar** para pegarlo donde quieras. Cuando lo abras o toques su **×**, aparecerá en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto para Trabajo como para Personal, o solo para la opción que hayas seleccionado.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. La opción **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Las tareas de un proyecto](projects.md#a-project-s-to-dos).

La opción **Área**, en **Detalles**, mueve una tarea a tu otra área. También cambia lo que puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita pasar a tu otra área para continuar y todos los mensajes relacionados están allí, se mueve automáticamente y sigue adelante. Si no, aparece **Mover a Trabajo** y no se mueve nada hasta que lo toques. Las tareas que añadas sin elegir Trabajo o Personal se mueven automáticamente cuando encuentran el área que les corresponde. Hasta entonces no aparecen como Trabajo ni Personal y se mantienen privadas.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. El correo de otra de tus empresas va a las tareas de esa empresa. En cambio, una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente en WhatsApp, un pedido en tu buzón personal o una [promesa](promises.md) relacionada con el trabajo, es Trabajo desde el principio.

Las tareas que hayas movido o asignado a un área tú mismo siempre se quedan donde las pongas. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, pero no adónde se envía la respuesta: siempre se responde en la conversación original, incluso después de moverla, a menos que elijas otra forma.

Las tareas de Personal de este tipo siguen respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparecen en un Fleet de trabajo ni en Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, te permite recorrerlas una a una en el orden de la lista. Verás cada borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Intro envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. El encabezado indica cuánto tardarás a tu ritmo, por ejemplo, «unos 2 min».

Al final, indica cuántas tareas se han enviado o cerrado y cuántas siguen preparándose.

Las tareas que te hacen una pregunta no se incluyen en ninguna de las dos opciones: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes recibidos cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de alguien lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, dentro de la hora siguiente.

Por la noche, desde las 00:00 hasta las 06:30, las comprobaciones se pausan. Los mensajes nuevos se siguen leyendo y guardando, y se comprueban juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «Pausadas por la noche, se pondrán al día a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en el chat o tocas una tarea, las comprobaciones se ejecutan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** comprueba todo inmediatamente.

**Revisar ahora** lee todas las fuentes inmediatamente. Si no tienes tareas abiertas, toca la línea de tu Machine para verla, con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, aparece arriba del todo en un ordenador. Solo se muestra una línea breve mientras se ejecuta una comprobación, o cuando ha fallado o se ha retrasado. También puedes pedirlo por chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que encontró en todas las fuentes que revisó, como «Se han comprobado 13 mensajes a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». La línea solo se refiere a esa comprobación: las tareas que ya estaban en tu lista siguen igual. Si una tarea nueva espera a un momento más oportuno, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién escribió, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo está en copia, responde un compañero» o «La reunión ya está programada para el jueves». Si la comprobación solo encontró un motivo impreciso, el hilo no muestra ningún motivo. Toca uno para leerlo y ver los mensajes que lo rodean.

Se muestran los 10 primeros. Toca debajo para ver el resto. Un número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Una notificación del móvil sobre un mensaje que ya aparece en la lista solo se muestra una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de reparación, nunca se leen ni aparecen en la lista. El correo sobre facturación, tu periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra su siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** te permite indicar qué hay que cambiar: cómo hacer la tarea o, cuando el borrador esté listo, qué cambiar en él. **Marcar como hecho** indica que ya está resuelta: aparece a la vista en una tarea preparada sin borrador o en una que te hace una pregunta. En los demás casos, está en la parte superior de **…**. La tarea desaparece de la lista de inmediato y el mensaje te permite **Deshacer**. Desliza el mensaje para quitarlo o arrástralo con el ratón para cerrarlo antes. El cambio se mantiene.

Para que se haga de otra manera, indícalo en su **Chat**. La respuesta solo menciona lo que ha cambiado, como si se ha pospuesto y hasta cuándo. Si no se ha podido cambiar algo, como una fecha de vencimiento, te lo dice.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: [volverá a aparecer con una frecuencia determinada](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, elige un motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarle el nombre. También puedes pedirlo en su chat, por ejemplo: «Cámbiale el nombre a…». El título se mantiene.

**Reabrir** devuelve a la lista una tarea cerrada. También vuelve a aparecer automáticamente cuando ocurre algo nuevo, como recibir un mensaje de esa persona, pero no cuando respondes tú. Entonces indica cuándo ha vuelto y aparece como nueva. El chat sigue donde lo dejaste, aunque hayan pasado semanas.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que indique la factura. Las facturas que se pagan automáticamente, como un recibo domiciliado o un cargo en una tarjeta guardada, no se convierten en tareas. Si un correo posterior indica que se ha pagado, por ejemplo, si quien lo envió confirma que ha recibido el pago, la tarea se cierra automáticamente. Puedes **Deshacer** durante un día.

Una tarea que solo sea relevante hasta una hora determinada, como una confirmación antes de una reunión, se cierra automáticamente al llegar esa hora. Pasa a **Hecho / descartado** con el mensaje «Ya no hace falta». Puedes **Deshacer** durante un día.

Antes de que un mensaje o un traspaso aparezca como listo, tu Machine revisa los chats recientes que tienes con las personas implicadas, también los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo pidieron y respondió que sí, la tarea se cierra automáticamente. Puedes **Deshacer** durante un día.

Si otra persona escribe en la misma conversación después de que se haya creado el borrador, **Enviar** lo deja en espera con el mensaje «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** otra vez para enviar el borrador tal como está.

Si un mensaje más reciente cambia el plan, por ejemplo, porque la fiesta se traslada a otro sitio o se cancela una reserva, The Machine actualiza sus tareas automáticamente. Las que sigan siendo necesarias se adaptan al nuevo plan. Las que ya no requieran ninguna acción pasan a **Hecho / descartado** con el mensaje «No hace falta». Su chat indica «Actualizado:» y explica por qué. Puedes **Deshacer** durante un día.

Cuando creas tus primeras tareas, aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas el botón o pulsas ×.

El primer día, aparece un saludo en la parte superior de Tareas y se indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero, para que esté lista cuando llegues.

Cada tarea empieza con su título. Debajo aparece de quién trata, la organización si está relacionada con una (no solo porque la persona trabaje allí), el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Si Graph tiene una foto o un logotipo de una persona o una organización, lo muestra. Si no, muestra sus iniciales. Si el logotipo no se ve bien en tamaño pequeño, por ejemplo, si es blanco sobre fondo transparente o es una palabra muy ancha, también muestra la inicial.

A veces aparece una línea discreta que indica qué información falta, como «Último contacto hace 12 días por correo; no ha habido nada desde entonces». Aparece si el último contacto con esa persona es antiguo o no ha recibido respuesta. También menciona los canales que no están conectados, como WhatsApp. Tu Machine indica lo que no sabe en vez de adivinar.

Si menciona un canal que no está conectado, toca Conectar a su lado para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Las tareas terminadas mantienen su título y muestran debajo cómo se resolvieron, como «Hecho: Sam lo firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede y muestra el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del destino, para que veas al instante si se trata de una respuesta de Slack o de un correo.

Si el borrador se basa en lo que ha dicho alguien en otro sitio, como la sugerencia de un compañero en Slack, una línea lo indica, por ejemplo, «Basado en un mensaje de Sam en #ops». Tócala para leer el mensaje. Desaparece cuando una actualización sustituye el borrador.

Los chats de Slack, WhatsApp, Telegram, Intercom y otros muestran una conversación completa, de más antiguo a más reciente: los mensajes anteriores al que dio lugar a la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, igual que en la app. El mensaje relacionado con la tarea se marca como «Esta tarea» y se muestra en su sitio. **Mostrar mensajes anteriores** añade los mensajes más antiguos. En un correo, el resto del hilo aparece plegado encima y debajo.

Los mensajes se abren igual desde la búsqueda, Graph, las respuestas de Ask o la última comprobación. Se marcan como «Este mensaje» o «Mensajes nuevos».

**Abrir en Gmail** abre el correo en la cuenta de Gmail donde lo recibiste. En Android, se abre en la app de Gmail si la tienes instalada.

En **Detalles** de un correo solo aparece la información que no está en el encabezado, como las direcciones completas de Cc, Cco o una dirección de respuesta distinta. Si no hay nada más que añadir, no aparece esta sección.

En una respuesta a un hilo de Slack también puedes ver lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre, el proyecto y el área de la tarea, que puedes cambiar tocando uno de ellos, tu última nota y el resultado de un agente de programación. Toca el título para abrir el chat. Las tareas terminadas se muestran de forma resumida; el mensaje del que proceden aparece en **Detalles**.

Las tareas que indican que esperan algo incluyen un enlace a tu último mensaje a esa persona, el que estás esperando que responda: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un móvil o `N`) permite añadir una tarea para cualquier cosa. Al crearla, no se envía nada. Si no eliges **Trabajo** ni **Personal**, se asigna al área que le corresponde según de quién y de qué trata. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie.», «3 nov», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario muestra opciones rápidas y **Elegir fecha**.
- **Se repite**: vuelve a aparecer con una frecuencia determinada. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula hasta 5 personas u organizaciones relacionadas con la tarea.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o por remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En un móvil, toca la cámara que aparece al lado para hacer una foto. Puedes añadir hasta 5 archivos, igual que en el chat. Consulta [Añadir archivos](card-chat.md#add-files). Pulsa × para quitar uno.

Los archivos se guardan con la tarea y The Machine los lee cuando trabaja en ella. También puedes crear una tarea solo con archivos: The Machine la completa a partir de un PDF o un archivo de texto. Las fotos aparecen como miniaturas. Tócalas para verlas a tamaño completo.
