---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita tu atención, lista para que des el visto bueno. Descubre qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 4209ed807e753101
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo necesita tu atención. Una tarea por asunto, aunque abarque varios mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba, muestra el último paso que confirmaste, como enviar un formulario o resolver un problema mientras no estabas. Se queda ahí hasta que toques **Entendido**, durante un día como máximo, y también aparece en tu móvil.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero necesita que decidas o respondas; si el trabajo se ha detenido por algo que solo tú tienes, como un dato, iniciar sesión o elegir, aparece una línea debajo del título que lo explica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas en las que no ha habido novedades durante una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y las que no han recibido respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que has prometido y lo que otros te han prometido. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, empezando por la más reciente, con la hora en que se completaron, como «Hecha hace 5 minutos». Las tareas que parecen terminadas aparecen marcadas como **Parece hecha**.

Después de enviar algo, aparece una nota breve que indica adónde ha ido la tarea, como «Enviado. Se ha movido a Hecho» o «Enviado. Se ha movido a Más tarde hasta el lun.». Una respuesta que solo promete hacer el trabajo, como «Lo enviaré antes del martes», deja la tarea abierta: «Enviado. Se ha mantenido abierta». **Abrir** te lleva a la tarea. La búsqueda encuentra tareas por su título o por la persona a quien se enviaron, también en Más tarde y Hecho.

**Para ti** muestra primero lo que ha vencido o vence mañana como muy tarde, después las preguntas de tu Fleet, luego los seguimientos de un tablero y, por último, el resto. En cada grupo, primero aparecen las tareas más recientes. Una tarea conserva su posición mientras tu Machine la prepara y cuando se completa: solo cambia su marca. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana como muy tarde, y después el resto, empezando por las más recientes. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está hecha, como «PR #3451 fusionada», pero todavía no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si un mensaje indica que está hecha, se cierra automáticamente al cabo de un día y puedes usar **Deshacer**. De lo contrario, espera a que pulses **Marcar como hecho**. Una tarea que ya hayas resuelto por tu cuenta, por ejemplo, con una respuesta en Gmail o Slack, también se cierra automáticamente.

Si un mensaje viene de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La identifica con su propia dirección, nunca con el nombre que haya usado. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo ha escrito.

Una tarea pendiente de otra persona, como una revisión o una respuesta, indica el paso con **Esperando a**:. Se queda en **Esperando a otros**, plegada y encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que tú hayas hecho una pregunta: vuelve la mañana antes de la fecha límite, en la fecha límite si es más tarde ese mismo día, o a la mañana siguiente si ya ha pasado. También indica a quién sigue esperando.

Si una tarea depende de que otra persona entregue un resultado, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no cierra la tarea: se queda en **Esperando a otros** hasta que un mensaje indique que ya está el resultado y entonces se cierra automáticamente. Puedes usar **Deshacer**. Si no llega nada para cuando toque hacer el seguimiento, vuelve con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como terminado para cambiarlo.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que lo nuevo aparezca primero después de que hayas estado fuera unos días. No hay novedades si no ha llegado ningún mensaje nuevo sobre la tarea ni has hecho nada en ella, como enviar un mensaje en el chat, editarla o posponerla. Solo mirarla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca todas las tareas de Más antiguos como innecesarias tras una confirmación, igual que **No hace falta** permite hacerlo de una en una. Puedes usar **Deshacer**. Si hay novedades en una tarea, vuelve a Para ti.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra. Puedes usar **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, envías un mensaje en el chat, la editas, la pospones o llega un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede recibir una tarea con un siguiente paso concreto. Como máximo, tres a la semana. Consulta [Proyectos](projects.md).

Cuando nada necesita tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, aparece una línea que lo explica, con **Revisar ahora** debajo.

Los filtros **Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, muestran todas las tareas o solo un tipo. En el móvil y el ordenador aparece la misma selección. Si está activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como que una pieza se reinicia continuamente, no es de Trabajo ni de Personal y solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente al otro filtro: en **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el nombre de tu último resumen de la mañana o de la tarde y cuántas tareas incluye, por ejemplo, **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leer el resumen y usa **Copiar** para pegarlo donde quieras. Cuando lo abres o tocas la **×**, aparece en todos tus dispositivos hasta el siguiente resumen.

Si no hay ningún resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo del filtro que hayas elegido.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [las tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También cambia lo que puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita tu otra área para continuar y todos los mensajes relacionados pertenecen a esa área, se mueve allí y sigue adelante automáticamente. Si no, aparece **Mover a Trabajo** y no se mueve hasta que lo toques. Si añades una tarea sin elegir Trabajo o Personal, se mueve automáticamente cuando encuentra el área que le corresponde. Hasta entonces, no es ni de Trabajo ni Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te pregunta con **Usar este correo para esta tarea**. Un buzón del trabajo que hayas etiquetado como Personal cuenta como Personal. El correo de otra de tus empresas va a las tareas de esa empresa. Una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp, un pedido en tu buzón personal o una [promesa](promises.md) sobre el trabajo, es de Trabajo desde el principio.

Una tarea que hayas movido o colocado por tu cuenta siempre se queda donde la pongas. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, nunca desde dónde responde: la respuesta siempre se envía en la conversación original, también después de moverla, a menos que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo, y nunca aparece en un Fleet de trabajo ni en Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, las recorre una a una en el orden de la lista. Muestra cada borrador completo y permite usar **Enviar**, **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En el ordenador, Intro envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. El encabezado indica cuánto tardarás a tu ritmo, por ejemplo, «unos 2 min».

Al terminar, cuenta lo que se ha enviado o cerrado y lo que sigue en preparación.

Las tareas que te hacen una pregunta no se incluyen en el repaso: necesitan una respuesta, no un toque.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en el plazo de una hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Conexiones, las comprobaciones indican «Pausadas por la noche. Se pondrán al día a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en el chat o tocas una tarea, las comprobaciones se reanudan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba todo al momento.

**Revisar ahora** lee todas las fuentes de inmediato. Si no tienes tareas abiertas, toca la línea de tu Machine para verla, junto con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, en el ordenador aparece arriba. Solo se muestra una línea breve mientras se realiza una comprobación, o si ha fallado o se ha retrasado. También puedes preguntarle en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que ha encontrado en todas las fuentes que ha leído, por ejemplo, «13 mensajes comprobados a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». Solo se refiere a esa comprobación: las tareas que ya estaban en tu lista siguen pendientes. Si una tarea nueva se reserva para un momento más oportuno, como el resumen de la mañana, se indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién lo ha escrito, el asunto o las primeras palabras, y la nueva tarea o el motivo por el que no hacía falta ninguna, como «Solo estás en copia, otra persona del equipo está respondiendo» o «La reunión ya está programada para el jueves». Si la comprobación solo encontró un motivo impreciso, el hilo no muestra ningún motivo. Toca un elemento para leerlo y ver lo que se dijo a su alrededor.

Se muestran los 10 primeros; toca debajo para ver el resto. El número que aparece después de un nombre, como (3), indica cuántos mensajes nuevos hay en ese chat. Las notificaciones del móvil sobre mensajes que ya aparecen en la lista solo se muestran una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta el correo que te envían. Tus propias respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de una corrección, nunca se leen ni aparecen en la lista. El correo sobre facturación, tu periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, junto a **Posponer**. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué cambiar: cómo hacerlo o, cuando el borrador esté listo, qué modificar en él. **Marcar como hecho** indica que ya está resuelto: aparece a la vista en una tarea lista sin borrador o en una que te hace una pregunta. En los demás casos, está arriba, en **…**. La tarea sale de la lista al momento y aparece **Deshacer** en el mensaje. Desliza el mensaje para quitarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se mantiene.

Para que se haga de otra manera, dilo en su **Chat**. La respuesta solo indica lo que ha cambiado, como si se ha pospuesto y hasta cuándo. Si no ha podido cambiar algo, como la fecha de vencimiento, te lo dice.

En **…**:

- **Pasar…**: asígnasela a alguien del equipo, a [Claude Code o Codex](hand-to-agent.md), o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: la tarea [vuelve con cierta frecuencia](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, elige un motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarle el nombre. También puedes pedírselo en el chat, por ejemplo: «Cámbiale el nombre a…». El título se mantiene.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve automáticamente cuando ocurre algo nuevo, como recibir un mensaje de esa persona, pero no cuando respondes tú. Entonces indica cuándo se reactivó y aparece como nueva. El chat continúa donde se quedó, aunque hayan pasado semanas.

Una factura que tengas que pagar personalmente, sea del país que sea, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluye. Las facturas que se pagan automáticamente, como un recibo domiciliado o un cargo a una tarjeta guardada, no. Cuando un correo posterior indica que se ha pagado, por ejemplo, porque quien lo envía confirma que ha recibido el pago, la tarea se cierra automáticamente. **Deshacer** la devuelve durante un día.

Una tarea que solo era pertinente hasta una hora determinada, como una confirmación antes de una reunión, se cierra automáticamente cuando pasa esa hora. Se mueve a **Hecho / descartado** con el motivo «Ya no hace falta». **Deshacer** la devuelve durante un día.

Antes de que un mensaje o un traspaso para otra persona aparezca como listo, tu Machine comprueba los chats recientes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo han pedido y ha dicho que sí, la tarea se cierra automáticamente. **Deshacer** la devuelve durante un día.

Si alguien ha escrito en la misma conversación después de que se preparara el borrador, **Enviar** lo detiene: «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** otra vez para enviar el borrador tal como está.

Si un mensaje más reciente cambia el plan, como cuando una fiesta cambia de lugar o se cancela una reserva, The Machine actualiza sus tareas. Las que sigan siendo pertinentes se adaptan al nuevo plan. Las que ya no necesiten ningún paso se mueven a **Hecho / descartado** con el motivo «No hace falta». En el chat aparece «Actualizado:» y se explica el motivo. **Deshacer** la devuelve durante un día.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece definitivamente cuando usas su botón o pulsas ×.

El primer día, en la parte superior de Tareas, aparece un saludo y el nombre de la persona que lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización si está relacionada con una (no solo porque alguien trabaje allí), el proyecto, si es de Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno; si no, muestran sus iniciales. Si un logotipo no se distingue bien a ese tamaño, por ejemplo, porque es blanco sobre un fondo transparente o tiene un nombre muy ancho, también se muestran las iniciales.

A veces, una línea discreta indica qué datos faltan, como «Último contacto hace 12 días por correo; no hay novedades». Aparece cuando la última comunicación con esa persona es antigua o no ha tenido respuesta. También indica los canales que no están conectados, como WhatsApp. Tu Machine te dice lo que no sabe en lugar de hacer suposiciones.

Si indica un canal que no está conectado, **Conectar**, a su lado, abre esa conexión.

El título indica lo que hay que hacer y solo cambia si cambia la tarea. Una tarea hecha conserva su título y debajo indica cómo terminó, como «Hecha: Sam la firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede y muestra el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del destino para que veas de inmediato si se trata de una respuesta de Slack o de un correo.

Si el borrador se basa en lo que alguien ha dicho en otro sitio, como una sugerencia de un compañero en Slack, aparece una línea que lo indica, como «Basado en un mensaje de Sam en #ops». Tócala para leer ese mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) aparece como una sola conversación, ordenada de más antiguo a más reciente: incluye los mensajes anteriores al que trata la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje relacionado con la tarea se marca como «Esta tarea» y se abre en la conversación. **Mostrar mensajes anteriores** añade los mensajes más antiguos. En un correo, el resto del hilo aparece plegado encima y debajo.

Los mensajes se abren igual desde la búsqueda, Graph, las respuestas de Ask o la última comprobación. Aparecen marcados como «Este mensaje» o «Mensajes nuevos».

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, se abre en la app de Gmail si la tienes instalada.

**Detalles** de un correo muestra solo la información que no aparece en su encabezado, como las direcciones completas en Cc, Cco o una dirección de respuesta distinta. Si no hay nada más que añadir, no aparece.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** abajo.

**Detalles** muestra el nombre, el proyecto y el área de la tarea (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Las tareas hechas se muestran de forma resumida; el mensaje de origen aparece en **Detalles**.

Una tarea que indique «Esperando a» enlaza tu último mensaje a esa persona, el que estás esperando: «Correo a Pat · mar».

## Crea una tarea

**Nueva tarea**, debajo de **Buscar** en el ordenador, **+** en el móvil o `N`, permite añadir una tarea sobre cualquier cosa. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, se asigna al área que le corresponde según de quién y de qué trate. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula las personas o empresas relacionadas, hasta un máximo de 5.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o por remitente. Cada resultado indica su origen, quién lo ha enviado y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En el móvil, la cámara de al lado permite hacer una foto. Puedes añadir hasta 5 archivos, igual que en el chat. Consulta [Añadir archivos](card-chat.md#add-files). Pulsa × para quitar un archivo.

Los archivos se quedan en la tarea y The Machine los lee cuando trabaja en ella. También puedes añadir solo archivos: completará la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas a tamaño completo.
