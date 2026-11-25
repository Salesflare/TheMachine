---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 91b111b2d6f2a97b
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo necesita tu atención. Una tarea por asunto, aunque ocupe muchos mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba, aparece el último paso que confirmaste, como un formulario o una incidencia, que se completó mientras no estabas. Se queda ahí hasta que pulses **Entendido**, como máximo durante un día. También recibirás una notificación en el móvil.
- **Para ti**: todo lo que espera por ti, primero lo que vence mañana o antes. Cada tarea indica si está **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero necesita que tomes una decisión o respondas; si el trabajo no puede continuar o no se puede usar sin algo que solo tú tienes, como un precio, un dato o una decisión, aparece una línea bajo el título que lo explica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas que llevan una semana sin novedades (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas, mensajes que [se envían más tarde](send-later.md) y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otros te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con la hora a la que se completaron, como «Hecho hace 5 minutos». Las tareas que parecen terminadas se marcan como **Parece hecha**.

Después de enviar algo, aparece una nota breve que indica adónde fue la tarea, como «Enviado. Se ha movido a Hecho» o «Enviado. Se ha movido a Más tarde hasta el lunes». Si la respuesta solo promete hacer el trabajo, como «Lo enviaré el martes», la tarea sigue abierta: «Enviado. Se ha mantenido abierta». **Abrir** te lleva a ella. La búsqueda encuentra tareas por título o por la persona a quien se enviaron, también en Más tarde y Hecho.

En **Para ti** aparecen primero las tareas vencidas o que vencen mañana o antes, después las preguntas de tu Fleet, luego los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, primero aparecen las más recientes. Una tarea conserva su posición mientras tu Machine la prepara y cuando se completa: solo cambia su marca. En los demás grupos abiertos, primero aparecen las vencidas o las que vencen mañana o antes; después, el resto, de la más reciente a la más antigua. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está terminada, como «PR #3451 se ha fusionado», pero aún no está cerrada. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si el mensaje lo indica, se cierra automáticamente al cabo de un día y puedes usar **Deshacer**. Si no, espera a que pulses **Marcar como hecho**.

Una tarea que ya hayas resuelto por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierra automáticamente. Si una respuesta dice que hay un archivo adjunto cuando no lo hay, la tarea no se cierra.

Si un mensaje viene de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que ha usado. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo escribió.

Si una tarea sigue esperando a otra persona, por ejemplo, una revisión o una respuesta, indica **Esperando a** qué paso. Aparece plegada en **Esperando a otros**, por encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que respondas con una pregunta: vuelve a aparecer la mañana anterior a la fecha límite, en la fecha límite si es más tarde ese mismo día, o a la mañana siguiente si ya ha pasado. También indica a quién sigue esperando.

Si una tarea depende de un resultado que tiene que entregar otra persona, como un contrato firmado, en **Detalles** aparece **Hecho cuando**. Enviar tu parte no la cierra: permanece en **Esperando a otros** hasta que un mensaje indique que ya está, y entonces se cierra automáticamente. Puedes usar **Deshacer**. Si no llega nada cuando sea el momento de insistir, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Dile en el chat qué se considera terminado para cambiarlo.

Si una tarea lleva una semana sin novedades, pasa de Para ti a **Más antiguos** para que las nuevas aparezcan primero después de que hayas estado unos días fuera. No hay novedades si no ha llegado ningún mensaje nuevo y no has hecho nada en la tarea, como enviar un mensaje en el chat, editarla o posponerla. Con solo abrirla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca como no necesarias todas las tareas de Más antiguos con una sola confirmación, igual que **No hace falta** permite hacerlo de una en una. Puedes usar **Deshacer**. Si llega algo nuevo en una tarea, vuelve a Para ti.

Si nadie ha tocado una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra. Puedes usar **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, pasa plegada a Vuelve más tarde y deja de contar para el número del icono de la app y el resumen de la mañana. Si la abres, escribes un mensaje en el chat, la editas, la pospones o recibes un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que se haya quedado parado y no tenga nada abierto puede recibir una tarea con un siguiente paso concreto, hasta tres a la semana. Consulta [Proyectos](projects.md).

Cuando nada necesita tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba las fuentes, se activa y te avisa. Si una comprobación falla o se retrasa, aparece una línea que lo indica, con **Revisar ahora** debajo.

**Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, muestran todas las tareas o solo las de un tipo. El móvil y el ordenador muestran la misma selección. Si está activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como que un componente se reinicia continuamente, no es de Trabajo ni Personal: solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente a la otra opción: en **Solo personal**, pulsa **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el último resumen de la mañana o de la tarde y lo que incluía, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Púlsala para volver a leerlo y usa **Copiar** para pegarlo donde quieras. Cuando lo abres o pulsas su **×**, aparece en todos tus dispositivos hasta el siguiente resumen.

Si no hay ningún resumen reciente, aparece **Hoy hasta ahora**: lo que se ha completado hoy y lo que sigue abierto, tanto de Trabajo como de Personal, o solo de la opción seleccionada.

Una tarea de un proyecto muestra el nombre del proyecto bajo el título. Púlsalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También se mueve lo que puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita tu otra área para continuar y todos los mensajes de los que procede están allí, se mueve automáticamente y continúa. De lo contrario, aparece **Mover a Trabajo** y no se mueve hasta que lo pulses. Una tarea que hayas añadido sin elegir Trabajo o Personal se mueve automáticamente cuando encuentra el área que le corresponde. Hasta entonces, no pertenece a Trabajo ni a Personal y sigue siendo privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pregunta con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. Los correos de otra de tus empresas van a las tareas de esa empresa. Una tarea sobre tu vida personal, como un familiar que escribe a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente que te escribe por WhatsApp, un pedido en tu buzón personal o una [promesa](promises.md) relacionada con el trabajo, es Trabajo desde el principio.

Una tarea que hayas movido o creado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, nunca adónde responde: las respuestas siempre se envían en la conversación original, también después de moverla, a menos que elijas otra opción.

Si una tarea Personal de este tipo responde a un correo, lo hace desde la dirección de trabajo a la que llegó. Nunca aparece en un Fleet de trabajo ni en el Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, las recorre de una en una en el orden de la lista. Muestra cada borrador completo, con **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Intro envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. El encabezado indica cuánto se tarda a tu ritmo, como «unos 2 min».

Al terminar, indica cuántas tareas se han enviado o cerrado y cuántas se siguen preparando.

Las tareas que te hacen una pregunta no se incluyen: necesitan tu respuesta, no que pulses un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, como máximo en una hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan. Los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «Pausadas por la noche. Se pondrán al día a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en el chat o pulsas una tarea, las comprobaciones se reanudan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre inicia una comprobación al momento.

**Revisar ahora** lee todas las fuentes al momento. Si no hay tareas abiertas, pulsa la línea de tu Machine para verla, con **Detalles**, que abre Comprobaciones dentro de Conexiones. Si hay tareas abiertas, aparece arriba en el ordenador. Allí solo se muestra una línea breve mientras se ejecuta una comprobación o si ha fallado o se ha retrasado. También puedes preguntarle en el chat.

LinkedIn, X y Salesflare siguen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de las tareas con lo que encontró en todas las fuentes consultadas, como «Se han revisado 13 mensajes a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». Solo se refiere a esa comprobación: las tareas que ya estaban en tu lista siguen igual. Si una tarea nueva espera un mejor momento, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Pulsa la línea para ver cada hilo de correo, chat y notificación, junto al icono de su fuente: quién lo escribió, el asunto o las primeras palabras y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo estaba en copia, responde un compañero» o «La reunión ya está programada para el jueves». Si la comprobación solo encontró un motivo impreciso, no se muestra ninguno. Pulsa un mensaje para leerlo junto con el contexto.

Se muestran los 10 primeros. Pulsa debajo para ver el resto. El número que aparece junto a un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Si una notificación del móvil es sobre un mensaje que ya aparece en la lista, solo se muestra una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus respuestas se leen para tener contexto y detectar promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de reparación, nunca se leen ni aparecen en la lista. Los correos sobre facturación, la prueba gratuita o una invitación se leen con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, junto a **Posponer**. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** permite indicar qué quieres cambiar: cómo hacerlo o, cuando haya un borrador, qué cambiar en él. Si dejas el texto a medias, seguirá ahí cuando vuelvas. **Cancelar** lo descarta.

**Marcar como hecho** indica que ya está resuelta. En un ordenador aparece con los demás botones cuando caben en una línea. En el móvil está visible en una tarea lista que no tiene borrador o que te hace una pregunta. En los demás casos, aparece al principio de **…**. La tarea desaparece de la lista al momento y aparece **Deshacer** en el mensaje. Desliza el mensaje o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Para que se haga de otra manera, díselo en su **Chat**. La respuesta solo indica qué ha cambiado, por ejemplo, que se ha pospuesto y hasta cuándo. Si no se pudo cambiar algo, como la fecha de vencimiento, te lo dice.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve a aparecer con cierta frecuencia](recurring.md).
- **No hace falta**: desaparece. Si quieres, indica el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Pulsa el título o **Nombre**, en **Detalles**, para cambiarlo. También puedes pedírselo en el chat, por ejemplo: «Cámbiale el nombre a…». Se conserva el título que elijas.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve a aparecer automáticamente cuando pasa algo nuevo, como un mensaje nuevo de esa persona, pero no cuando respondes tú. Entonces indica cuándo volvió y aparece como nueva. El chat continúa donde lo dejaste, aunque hayan pasado semanas.

Una factura que tengas que pagar por tu cuenta, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluya. Las facturas que se pagan automáticamente, como un recibo domiciliado o un cargo en una tarjeta guardada, no se convierten en tareas. Si más adelante llega un correo que confirma el pago, por ejemplo, un mensaje del remitente que confirma que lo ha recibido, la tarea se cierra automáticamente. Puedes usar **Deshacer** durante un día para recuperarla.

Una tarea que solo importa hasta una hora concreta, como una confirmación antes de una reunión, se cierra automáticamente cuando pasa esa hora. Se mueve a **Hecho / descartado** como «Ya no hace falta». Puedes usar **Deshacer** durante un día para recuperarla.

Antes de que un mensaje o un traspaso para otra persona aparezca como listo, tu Machine comprueba los chats recientes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si más tarde llega un mensaje que indica que ya está hecho, por ejemplo, porque se lo pidieron y dijo que sí, la tarea se cierra automáticamente. Puedes usar **Deshacer** durante un día para recuperarla.

Si otra persona escribe en la misma conversación después de que se haya creado tu borrador, **Enviar** lo detiene: «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** otra vez para enviar el borrador tal cual.

Cuando un mensaje más reciente cambia el plan, por ejemplo, porque una fiesta se traslada a otro sitio o se cancela una reserva, The Machine actualiza las tareas por su cuenta. Si una tarea sigue haciendo falta, se adapta al nuevo plan. Si ya no queda nada por hacer, se mueve a **Hecho / descartado** como «No hace falta». El chat indica «Actualizado:» y explica por qué. Puedes usar **Deshacer** durante un día para recuperarla.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece definitivamente cuando usas su botón o pulsas ×.

El primer día, aparece un saludo en la parte superior de Tareas y se indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién se trata, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, si es de Trabajo o Personal y cuándo llegó. Pulsa un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno, y sus iniciales si no. Si el logotipo no se lee bien en pequeño, por ejemplo, porque es blanco sobre un fondo transparente o porque es una palabra ancha, también se muestran las iniciales.

A veces aparece una línea discreta que indica lo que no se sabe, como «Último contacto hace 12 días por correo; no hay nada desde entonces». Se muestra si el último contacto es antiguo o no ha recibido respuesta, e indica los canales que no están conectados, como WhatsApp. Tu Machine te dice lo que no sabe en vez de adivinar.

Si se menciona un canal que no está conectado, pulsa Conectar junto a él para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si cambia la tarea. Una tarea completada conserva su título y muestra debajo cómo terminó, como «Hecho: Sam lo firmó el martes».

Encima del borrador aparece una línea tenue con el mensaje de origen y el logotipo del servicio. Púlsala para leer el hilo. El borrador muestra el logotipo del destino, para que veas enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en la información de otra persona, como una sugerencia de un compañero en Slack, una línea lo indica, por ejemplo, «Basado en un mensaje de Sam en #ops». Púlsala para leer ese mensaje. Desaparece cuando una actualización sustituye el borrador.

Un chat (Slack, WhatsApp, Telegram, Intercom…) aparece como una sola conversación, de los mensajes más antiguos a los más recientes: los mensajes anteriores al que originó la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje de la tarea se marca como «Esta tarea» y aparece a la vista. **Mostrar mensajes anteriores** añade los mensajes más antiguos. En un correo, el resto del hilo aparece plegado por encima y por debajo.

Un mensaje se abre de la misma manera desde la búsqueda, Graph, las respuestas de Ask o la última comprobación. Se marca como «Este mensaje» (o «Mensajes nuevos»).

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, se abre en la app de Gmail si la tienes.

En **Detalles** de un correo solo aparece lo que no muestra su encabezado, como las direcciones completas de Cc, Bcc o una dirección de respuesta distinta. Si no hay nada que añadir, no aparece nada.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** al final.

**Detalles** muestra el nombre, el proyecto, el área (pulsa cualquiera para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Una tarea completada aparece de forma resumida. El mensaje del que procede está en **Detalles**.

Una tarea que indica «Esperando a» enlaza con tu último mensaje a esa persona, al que estás esperando: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un móvil o `N`) añade una tarea sobre cualquier cosa. Al crearla no se envía nada. Si no seleccionas **Trabajo** ni **Personal**, se asigna al área que le corresponda según de quién y de qué se trate. También encuentra el correo al que da seguimiento, aunque sea antiguo.

Si cierras el formulario antes de añadir la tarea, el texto y las opciones se guardan para la próxima vez. Los archivos no se guardan. **Descartar** en el mensaje los elimina.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario muestra opciones rápidas y **Elegir fecha**.
- **Se repite**: vuelve a aparecer con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula a las personas o empresas relacionadas, hasta un máximo de 5.
- Icono de mensaje: adjunta el mensaje relacionado, como un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: pulsa el clip, pega una captura de pantalla o arrastra archivos al formulario. En el móvil, la cámara que aparece al lado te permite hacer una foto. Puedes añadir hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Pulsa × para quitar uno.

Los archivos permanecen en la tarea y The Machine los lee cuando trabaja en ella. Los archivos son suficientes: puede completar la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Púlsalas para verlas a tamaño completo.
