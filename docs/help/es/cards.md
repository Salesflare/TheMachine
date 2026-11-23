---
title: Tareas
area: cards
summary: Una tarea por cada asunto que requiere tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e0fd02e557e6daee
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo requiere tu atención. Una tarea por asunto, aunque incluya muchos mensajes.

## Dónde están las tareas

La página **Tareas** las agrupa:

- **Recién hecho**: arriba aparece el último paso que confirmaste, como un formulario o una incidencia, que se completó mientras no estabas. Se queda ahí hasta que pulses **Entendido**, como máximo durante un día. También te avisa en el móvil.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero tienes que decidir o responder; cuando el trabajo se detiene por algo que solo tienes tú, como un dato, un inicio de sesión o una elección, aparece una línea bajo el título que lo explica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o una nota, sin nada que decidir).
- **Más antiguos**: tareas plegadas que no tienen nada nuevo desde hace una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso le toca a otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con la hora a la que terminaron, como «Hecho hace 5 minutos». Las tareas que parecen terminadas ya aparecen marcadas como **Parece hecha**.

Después de enviar, una nota breve indica adónde ha ido la tarea, como «Enviado. Se ha movido a Hecho» o «Enviado. Se ha movido a Más tarde hasta el lunes». Una respuesta que solo promete hacer el trabajo, como «Lo enviaré el martes», deja la tarea abierta: «Enviado. Sigue abierta». **Abrir** te lleva a la tarea. La búsqueda encuentra tareas por título o por destinatario, también en Más tarde y Hecho.

En **Para ti** aparecen primero las tareas vencidas o que vencen mañana, después las preguntas de tu Fleet, luego los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, se ordenan de más nuevas a más antiguas. Una tarea conserva su lugar mientras tu Machine la prepara y cuando termina: solo cambia su marca. En los demás grupos abiertos, primero aparecen las vencidas o las que vencen mañana, y después el resto, de más nuevas a más antiguas. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está terminada, como «PR #3451 se ha fusionado», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si un mensaje la muestra, se cierra sola al cabo de un día y aparece **Deshacer**. Si no, espera a que pulses **Marcar como hecho**. Una tarea que ya hayas gestionado por tu cuenta, por ejemplo respondiendo en Gmail o Slack, también se cierra sola.

Si el mensaje viene de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en vez de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que ha usado. Tu Machine comprueba estos mensajes con la persona de la dirección que ya tienes, nunca con quien los ha escrito.

Una tarea que sigue pendiente de otra persona, como una revisión o una respuesta, indica **Esperando a:** ese paso. Aparece plegada en **Esperando a otros**, por encima de Vuelve más tarde, hasta que un mensaje nuevo la haga aparecer de nuevo. Lo mismo ocurre después de que hayas respondido con una pregunta: vuelve a aparecer la mañana anterior a la fecha límite, en la fecha límite si es más tarde ese mismo día, o a la mañana siguiente si la fecha límite ya ha pasado. También indica de quién sigue esperando respuesta.

Cuando una tarea depende de un resultado que entrega otra persona, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje muestre el resultado y entonces se cierra sola. Aparece **Deshacer**. Si no llega nada cuando toque insistir, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como terminado para cambiarlo.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que las tareas nuevas aparezcan primero después de unos días sin entrar. No hay novedades si no ha llegado ningún mensaje nuevo ni has hecho nada en ella, como enviar un mensaje por el chat, editarla o posponerla. Solo mirarla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca todas las tareas de Más antiguos como innecesarias tras una sola confirmación, igual que **No hace falta** permite hacerlo de una en una. Aparece **Deshacer**. Si una tarea recibe algo nuevo, vuelve a Para ti.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra. Aparece **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Abrirla, enviar un mensaje por el chat, editarla, posponerla o recibir un mensaje nuevo hace que vuelva a aparecer.

Una vez a la semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede generar una tarea con un siguiente paso concreto. Como máximo, tres a la semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine descansa y deja la lista vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, la línea lo explica y aparece **Revisar ahora** debajo.

Las opciones **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo las de un tipo. El móvil y el ordenador muestran la misma selección. Si está activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como que un componente se reinicie constantemente, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también te lleva directamente a la otra opción: en **Solo personal**, pulsa **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el último resumen de la mañana o de la tarde y lo que cuenta, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Pulsa la fila para volver a leer el resumen y usa **Copiar** para pegarlo donde quieras. Cuando lo abras o pulses la **×**, aparecerá en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo del área que hayas seleccionado.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Pulsa el nombre para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a la otra área. También cambia de área lo que puede leer y enviar. **Deshacer** en la nota la devuelve a su área anterior.

Si una tarea necesita la otra área para continuar y todos los mensajes de los que procede están allí, se mueve y continúa por su cuenta. Si no, aparece **Mover a Trabajo** y no se mueve nada hasta que lo pulses. Una tarea que hayas añadido sin elegir Trabajo o Personal se mueve sola cuando encuentra su área. Hasta entonces, no aparece como Trabajo ni Personal y sigue siendo privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita leer otros mensajes de tu otra área, te pregunta con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. Los correos de otras empresas tuyas van a las tareas de esa empresa. Una tarea sobre tu vida personal, como un mensaje de tu familia que llega a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp o un pedido en tu buzón personal, es de Trabajo desde el principio. Una tarea que hayas movido o asignado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, nunca desde dónde responde: la respuesta siempre se envía al mismo sitio que la conversación, también después de mover la tarea, salvo que elijas otra opción.

Aun así, una tarea Personal responde desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de trabajo ni en el Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar** en el encabezado de Para ti las va mostrando de una en una, en el orden de la lista. Muestra cada borrador completo, con **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En el ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el proceso. El encabezado indica cuánto tardarás a tu ritmo, como «unos 2 min».

Al terminar, indica cuántas tareas se han enviado o cerrado y cuántas siguen preparándose.

Las tareas que te hacen una pregunta no se incluyen en ninguna de las dos opciones: necesitan tu respuesta, no un toque.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes recibidos cuando hay 40 en espera o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en el plazo de una hora.

Por la noche, entre las 00:00 y las 06:30, se pausan las comprobaciones: los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30 para que las tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «Pausadas por la noche; se pondrán al día a las 06:30». Si haces clic, escribes o te desplazas por la app, escribes en el chat o pulsas una tarea durante la noche, las comprobaciones se ejecutan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba todo al momento.

**Revisar ahora** lee todas las fuentes al momento. Si no tienes tareas abiertas, pulsa la línea de tu Machine para verla, junto con **Detalles**, que abre Comprobaciones dentro de Conexiones. Si tienes tareas abiertas, aparece arriba en el ordenador. Solo se muestra una línea breve mientras se ejecuta una comprobación o si alguna ha fallado o se ha retrasado. También puedes preguntarlo en el chat.

LinkedIn, X y Salesflare mantienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de las tareas con lo que ha encontrado en cada fuente leída, como «13 mensajes comprobados a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». La línea solo se refiere a esa comprobación: las tareas que ya estaban en la lista no cambian. Si una tarea nueva se deja para un mejor momento, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Pulsa la línea para ver cada conversación de correo, chat y notificación, con el icono de su fuente: quién la escribió, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo en copia; un compañero está respondiendo» o «La reunión ya está programada para el jueves». Si una conversación no muestra ningún motivo, es porque la comprobación solo dio uno poco claro. Pulsa una para leerla y ver lo que se dijo alrededor.

Se muestran las 10 primeras. Pulsa debajo para ver el resto. El número que aparece después de un nombre, como (3), indica cuántos mensajes nuevos hay en ese chat. Las notificaciones del móvil sobre un mensaje que ya aparece en la lista solo se muestran una vez. La línea permanece durante 12 horas después de la comprobación.

Solo cuenta los correos que recibes. Tus respuestas se leen para tener en cuenta el contexto y las promesas, pero no cuentan como correos nuevos. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de reparación, nunca se leen ni aparecen en la lista. Los correos sobre facturación, tu periodo de prueba o una invitación se leen con normalidad.

## Los botones

Una tarea muestra su siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué cambiar: cómo hacerlo o, cuando el borrador esté listo, qué cambiar en él. **Marcar como hecho** indica que ya está gestionada: aparece a la vista en una tarea preparada sin borrador o en una tarea que te hace una pregunta; en los demás casos, está en la parte superior de **…**. La tarea desaparece de la lista al momento y aparece **Deshacer** en el mensaje. Desliza el mensaje para quitarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Para que se haga de otra manera, díselo en su **Chat**. La respuesta solo indica lo que ha cambiado, como si se ha pospuesto y hasta cuándo. Si no ha podido cambiar algo, como la fecha límite, te lo dice.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: la tarea [vuelve a aparecer con cierta frecuencia](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, indica el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Pulsa el título o **Nombre**, en **Detalles**, para cambiarlo. También puedes pedirlo en el chat, por ejemplo: «Cámbiale el nombre a…». El título que elijas se conserva.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve a aparecer sola cuando ocurre algo nuevo, como recibir un mensaje de esa persona, pero no si respondes tú. Entonces indica cuándo volvió y aparece en el orden de las tareas nuevas. El chat sigue donde lo dejaste, aunque hayan pasado semanas.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluye. No ocurre con las facturas que se pagan automáticamente, como las domiciliaciones o los pagos con tarjeta guardada. Cuando un correo posterior indique que está pagada, por ejemplo porque el remitente confirma que ha recibido el pago, la tarea se cierra sola. **Deshacer** la recupera durante un día.

Una tarea que solo tenía sentido hasta una hora determinada, como una confirmación antes de una reunión, se cierra sola cuando pasa esa hora. Se mueve a **Hecho / descartado** con el motivo «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de mostrar como listo un mensaje o un traspaso para otra persona, tu Machine comprueba tus chats recientes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo porque se lo pidieron y dijo que sí, la tarea se cierra sola. **Deshacer** la recupera durante un día.

Si otra persona ha escrito en la misma conversación después de que se preparara el borrador, **Enviar** lo deja en espera: «No se ha enviado: hay un mensaje nuevo en la conversación». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** otra vez para enviar el borrador tal cual.

Cuando un mensaje nuevo cambia los planes, como si una fiesta cambia de lugar o se cancela una reserva, The Machine actualiza sus tareas por su cuenta. Las que siguen siendo necesarias se adaptan al nuevo plan. Las que ya no tienen nada pendiente se mueven a **Hecho / descartado** con el motivo «No hace falta». En el chat aparece «Actualizado:» con el motivo y **Deshacer** las recupera durante un día.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas su botón o pulsas ×.

El primer día, la parte superior de Tareas te da la bienvenida y te indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con el título. La línea de debajo indica de quién trata, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, si es de Trabajo o Personal y cuándo llegó. Pulsa un nombre para abrir su página en Graph.

Si Graph tiene una foto o un logotipo de una persona o una organización, aparece en su lugar. Si no, aparecen sus iniciales. Los logotipos que no se verían bien en pequeño, como texto blanco sobre fondo transparente o una marca denominativa ancha, también muestran la inicial.

A veces, una línea tenue indica lo que no se sabe, como «Último contacto por correo hace 12 días; no ha habido nada desde entonces». Aparece si el último contacto con esa persona es antiguo o sigue sin respuesta. También indica los canales que no están conectados, como WhatsApp. Tu Machine te dice lo que no sabe en vez de adivinar.

Si se menciona un canal que no está conectado, **Conectar**, junto a su nombre, abre esa conexión.

El título indica qué hay que hacer y solo cambia si cambia la tarea. Las tareas terminadas conservan el título y muestran debajo cómo terminaron, como «Hecho: Sam lo firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede, con el logotipo del servicio. Púlsala para leer la conversación. El borrador muestra el logotipo del canal al que se envía para que veas de un vistazo si es una respuesta de Slack o un correo.

Si el borrador tiene en cuenta lo que ha dicho alguien por otro canal, como una sugerencia de un compañero en Slack, una línea lo indica, por ejemplo: «Basado en un mensaje de Sam en #ops». Púlsala para leer el mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) muestra una conversación completa, de más antigua a más reciente: los mensajes anteriores al que trata la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje de la tarea está marcado como «Esta tarea» y se abre en la conversación. **Mostrar mensajes anteriores** añade mensajes más antiguos. En un correo, el resto de la conversación aparece plegado encima y debajo.

Los mensajes se abren del mismo modo desde la búsqueda, Graph, las respuestas de Ask o la última comprobación, marcados como «Este mensaje» o «Mensajes nuevos».

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, se abre en la app de Gmail si la tienes instalada.

En **Detalles** de un correo solo aparece la información que no figura en el encabezado, como las direcciones completas en Cc, Cco o una dirección distinta para responder. Si no hay nada más que añadir, no aparece ninguna.

Las respuestas en un hilo de Slack también muestran lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** al final.

**Detalles** muestra el nombre, el proyecto y el área de la tarea (pulsa uno para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Las tareas terminadas ocupan menos espacio; el mensaje de origen aparece en **Detalles**.

Una tarea marcada como «Esperando a» enlaza al último mensaje que enviaste a esa persona, el que está pendiente de respuesta: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en el ordenador, **+** en el móvil o `N`) añade una tarea para cualquier asunto. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, se asigna al área que corresponda según de quién y de qué trate. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «en 2 horas». También puedes escribirlo en tu idioma. El icono del calendario muestra opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve a aparecer con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula hasta 5 personas u organizaciones relacionadas con la tarea.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o remitente. Cada resultado muestra su origen, quién lo envió y cuándo.
- **Archivos**: pulsa el clip, pega una captura de pantalla o arrastra archivos al formulario. En el móvil, pulsa la cámara de al lado para hacer una foto. Puedes añadir hasta 5 archivos, como en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Pulsa × para quitar un archivo.

Los archivos se quedan en la tarea y The Machine los lee cuando trabaja en ella. Puedes adjuntar solo archivos: la tarea se completa a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Púlsalas para verlas a tamaño completo.
