---
title: Tareas
area: cards
summary: Una tarea por cada asunto que requiera tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: f77d6b07f6f94ce5
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo requiere tu atención. Una tarea por asunto, aunque abarque muchos mensajes.

## Dónde están las tareas

La página **Tareas** las agrupa así:

- **Recién hecho**: arriba del todo, muestra el último paso que confirmaste, como un formulario o una incidencia, y que se completó mientras no estabas. Se queda ahí hasta que toques **Entendido**, como máximo un día, y también recibirás una notificación en el móvil.
- **Para ti**: todo lo que está pendiente de ti, primero lo que vence mañana o antes. Cada tarea indica **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo ejecuta), **Te necesita** (primero necesita que decidas o respondas; cuando el trabajo no puede continuar o utilizarse sin algo que solo tú sabes, como un precio, un dato o una elección, aparece una línea bajo el título que lo indica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas que no han tenido novedades en una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas, mensajes que [se envían más tarde](send-later.md) y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otros te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, primero las más recientes y con la hora a la que se completaron, como «Hecho hace 5 minutos». Las tareas que parecen terminadas ya aparecen como **Parece hecha**.

Después de enviar, aparece una nota breve que indica dónde ha ido la tarea, como «Enviado. Movido a Hecho» o «Enviado. Movido a Más tarde hasta el lun.». Una respuesta que solo promete hacer el trabajo, como «Te lo envío el martes», deja la tarea abierta: «Enviado. Se ha dejado abierta». **Abrir** te lleva a ella. La búsqueda encuentra una tarea por su título o por la persona a quien se envió, también en Más tarde y Hecho.

**Para ti** muestra primero lo que está vencido o vence mañana o antes, luego las preguntas de tu Fleet, después los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, primero aparecen las más recientes. La tarea mantiene su posición mientras tu Machine la prepara y cuando se completa: solo cambia su marca. En los demás grupos abiertos, primero aparecen las vencidas o las que vencen mañana o antes, y después el resto, de más recientes a más antiguas. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está terminada, como «PR n.º 3451 combinada», pero todavía no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si aparece en un mensaje, se cierra automáticamente al cabo de un día y puedes usar **Deshacer**. En los demás casos, espera a que uses **Marcar como hecho**.

Una tarea que ya hayas resuelto por tu cuenta, por ejemplo con una respuesta en Gmail o Slack, también se cierra automáticamente. Una respuesta que diga que se ha adjuntado un archivo cuando no es así no la cierra.

Si un mensaje procede de una dirección que solo parece ser de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que haya usado. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo escribió.

Una tarea que siga pendiente de otra persona, como una revisión o una respuesta, indica **Esperando a** quién o qué: ese paso. Aparece plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que hayas hecho una pregunta: vuelve la mañana antes de la fecha límite, en la fecha límite si es más tarde ese mismo día o a la mañana siguiente si ya ha pasado, e indica de quién sigue esperando respuesta.

Cuando una tarea depende de un resultado que entrega otra persona, como un contrato firmado, **Detalles** muestra **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje indique que ya está el resultado y entonces se cierra automáticamente. Puedes usar **Deshacer**. Si no llega nada para cuando toque insistir, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Dile en el chat qué se considera terminado para cambiarlo.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que las tareas recientes aparezcan primero cuando vuelvas tras unos días. No hay novedades si no llega ningún mensaje nuevo ni haces nada en la tarea, como enviar un mensaje por el chat, editarla o posponerla. Consultarla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca todas las tareas de Más antiguos como innecesarias tras una sola confirmación, igual que **No hace falta** permite hacerlo de una en una. Puedes usar **Deshacer**. Si hay novedades en una tarea, vuelve a Para ti.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra. Puedes usar **Deshacer**. **Mantener** la conserva y no vuelve a preguntarlo. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Abrirla, enviar un mensaje por el chat, editarla, posponerla o recibir un mensaje nuevo hace que vuelva a aparecer.

Una vez a la semana, un proyecto que se haya quedado sin actividad y no tenga nada pendiente puede generar una tarea con un siguiente paso concreto, hasta tres por semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación ha fallado o se ha retrasado, aparece una línea que lo explica, con **Revisar ahora** debajo.

**Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, permiten mostrar todas las tareas o solo un tipo. El móvil y el ordenador muestran la misma selección. Mientras esté seleccionado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como que un componente se reinicie constantemente, no es ni de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente a la otra vista: en **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el nombre de tu último resumen de la mañana o de la tarde y lo que incluye, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leer ese resumen y usa **Copiar** para pegarlo donde quieras. Cuando lo abras o toques su **×**, estará disponible en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, para Trabajo y Personal o solo para la categoría seleccionada.

Una tarea de un proyecto muestra el nombre del proyecto bajo el título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Las tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También cambia qué puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita tu otra área para continuar y todos los mensajes de los que procede están allí, se mueve automáticamente y sigue adelante. De lo contrario, aparece **Mover a Trabajo** y no se mueve nada hasta que lo toques. Una tarea que añadas sin elegir Trabajo o Personal se mueve automáticamente cuando encuentra el área que le corresponde. Hasta entonces, no aparece en Trabajo ni en Personal, y sigue siendo privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. El correo de otras empresas tuyas va a las tareas de esa empresa, y una tarea sobre tu vida personal, como un familiar que escribe a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp, un pedido en tu buzón personal o una [promesa](promises.md) relacionada con el trabajo, es Trabajo desde el principio.

Una tarea que hayas movido o colocado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, pero nunca dónde responde: la respuesta siempre se envía al lugar donde está la conversación, incluso después de moverla, salvo que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de trabajo ni en el Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar** en el encabezado de Para ti te permite recorrerlas de una en una, en el orden de la lista, con cada borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Intro envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el proceso. El encabezado indica cuánto tardarás a tu ritmo, como «unos 2 min».

Al terminar, se cuentan las tareas enviadas o cerradas y las que todavía se están preparando.

Las tareas que te hacen una pregunta no se incluyen en ninguno de los dos grupos: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes recibidos cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en el plazo de una hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se revisan juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Comprobaciones, en Conexiones, aparece «Pausa nocturna. Se pondrá al día a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en el chat o tocas una tarea, las comprobaciones se reanudan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba todo de inmediato.

**Revisar ahora** lee todas las fuentes en ese momento. Si no tienes tareas abiertas, toca la línea de tu Machine para verla, junto con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, aparece arriba del todo en el ordenador. Allí solo se muestra una línea breve mientras se realiza una comprobación o si ha fallado o se ha retrasado. También puedes preguntarlo por el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas que indica lo que ha encontrado en todas las fuentes que ha leído, como «13 mensajes comprobados a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». Solo se refiere a esa comprobación: las tareas que ya estaban en tu lista siguen igual. Si una tarea nueva queda pendiente hasta que llegue un momento más oportuno, como el resumen de la mañana, se indica hasta cuándo: «1 tarea pendiente hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, junto con el icono de su servicio: quién escribió, el asunto o las primeras palabras y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo está en copia; responde un compañero» o «La reunión ya está fijada para el jueves». Si la comprobación solo dio un motivo impreciso, el hilo no muestra ningún motivo. Toca uno para leerlo y ver lo que se dijo a su alrededor.

Se muestran los 10 primeros; toca debajo para ver el resto. Un número tras un nombre, como (3), indica cuántos mensajes nuevos hay en ese chat. Las notificaciones del móvil sobre un mensaje que ya aparece en la lista solo se muestran una vez. La línea permanece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para tener en cuenta el contexto y las promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de una corrección, nunca se leen ni aparecen en la lista. El correo sobre facturación, el periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, junto a **Posponer**. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** permite indicar qué cambiar: cómo hacerlo o, cuando el borrador esté listo, qué cambiar en él. Si dejas el texto a medias, seguirá ahí cuando vuelvas; **Cancelar** lo descarta.

**Marcar como hecho** indica que ya está resuelta: aparece a la vista en una tarea lista sin borrador o en una que te hace una pregunta; en los demás casos, está en la parte superior de **…**. La tarea desaparece de la lista de inmediato y aparece **Deshacer** en el mensaje. Desliza el mensaje o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Si quieres que se haga de otra manera, dilo en su **Chat**. La respuesta solo menciona lo que ha cambiado, por ejemplo, que se ha pospuesto y hasta cuándo. Si no ha podido cambiar algo, como una fecha de vencimiento, te lo indica.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: [volverá a aparecer con una frecuencia determinada](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, indica el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre** en **Detalles** para cambiarlo, o pídelo en el chat, por ejemplo, «Cámbiale el nombre a…». Se conserva el título que elijas.

**Reabrir** recupera una tarea cerrada. También vuelve a aparecer automáticamente cuando ocurre algo nuevo, como un mensaje nuevo de esa persona, pero no cuando respondes tú. Entonces indica cuándo volvió y se ordena como una tarea nueva. El chat continúa donde lo dejaste, aunque hayan pasado semanas.

Una factura que todavía tengas que pagar tú, sea del país que sea, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que figuran en la factura. Las facturas que se pagan automáticamente, como un recibo domiciliado o una tarjeta guardada, no se convierten en tareas. Cuando un correo posterior indica que se ha pagado, por ejemplo, porque el remitente confirma que ha recibido el pago, la tarea se cierra automáticamente. Puedes usar **Deshacer** durante un día para recuperarla.

Una tarea que solo sea relevante hasta una hora determinada, como una confirmación antes de una reunión, se cierra automáticamente cuando llega esa hora. Pasa a **Hecho / descartado** con el estado «Ya no hace falta». Puedes usar **Deshacer** durante un día para recuperarla.

Antes de que un mensaje o un traspaso para otra persona aparezca como listo, tu Machine comprueba tus chats recientes con las personas implicadas, también los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo pidieron y dijo que sí, la tarea se cierra automáticamente. Puedes usar **Deshacer** durante un día para recuperarla.

Si alguien escribe en la misma conversación después de que se haya creado el borrador, **Enviar** lo retiene: «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** otra vez para enviar el borrador tal como está.

Si un mensaje nuevo cambia el plan, por ejemplo, porque la fiesta se traslada a otro lugar o se cancela una reserva, The Machine actualiza las tareas automáticamente. Las que sigan siendo necesarias se adaptan al nuevo plan. Las que ya no requieran ninguna acción pasan a **Hecho / descartado** con el estado «No hace falta». En su chat aparece «Actualizada:» y el motivo. Puedes usar **Deshacer** durante un día para recuperarlas.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y con el recordatorio de que no se envía nada hasta que pulses **Enviar**. El consejo desaparece definitivamente cuando usas ese botón o pulsas ×.

El primer día, la parte superior de Tareas te da la bienvenida e indica quién lleva más tiempo esperando tu respuesta. Primero se prepara el borrador de esa respuesta para que esté listo cuando llegues.

Cada tarea empieza con su título. La línea debajo indica a quién se refiere, la organización cuando la tarea trate sobre ella, pero no solo porque alguien trabaje allí, el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en el Graph.

Los nombres y las organizaciones muestran su foto o logotipo si el Graph tiene uno, y sus iniciales si no. Si un logotipo no se distingue bien en tamaño pequeño, como uno blanco sobre fondo transparente o un logotipo horizontal con el nombre, también se muestran las iniciales.

A veces aparece una línea discreta que indica qué se desconoce, como «Último contacto hace 12 días por correo; no hay nada desde entonces». Se muestra cuando el último contacto con esa persona es antiguo o no ha recibido respuesta, y menciona los canales que no están conectados, como WhatsApp. Tu Machine te dice lo que no sabe en vez de adivinar.

Si menciona un canal que no está conectado, toca Conectar junto a él para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Una tarea terminada conserva el título y muestra debajo cómo terminó, como «Hecho: Sam lo firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede, junto con el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del lugar al que se enviará, para que veas enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que alguien ha dicho en otro lugar, como la sugerencia de un compañero en Slack, una línea lo indica, como «Basado en un mensaje de Sam en #ops». Tócala para leer ese mensaje. Desaparece cuando una actualización sustituye el borrador.

Un chat de Slack, WhatsApp, Telegram, Intercom u otro servicio muestra una conversación completa, de los mensajes más antiguos a los más recientes: los mensajes anteriores al que trata la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, igual que en la app. El mensaje de la tarea se marca como «Esta tarea» y aparece abierto. **Mostrar mensajes anteriores** añade los mensajes más antiguos. En un correo, el resto del hilo aparece plegado encima y debajo.

Los mensajes se abren de la misma manera desde la búsqueda, el Graph, las respuestas de Ask o la última comprobación, con la marca «Este mensaje» o «Mensajes nuevos».

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, lo abre en la app de Gmail si la tienes instalada.

**Detalles** de un correo muestra solo la información que no aparece en el encabezado, como las direcciones completas en Cc, Cco o una dirección de respuesta distinta. Si no hay nada más que mostrar, no aparece esta sección.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de empezar el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre, el proyecto y el área de la tarea, puedes tocar uno para cambiarlo, la última nota y el resultado de un agente de programación. Al tocar el título se abre el chat. Una tarea terminada se muestra de forma resumida; el mensaje del que procede está en **Detalles**.

Una tarea que indica «Esperando a» enlaza al último mensaje que enviaste a esa persona y cuya respuesta esperas: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea**, debajo de **Buscar** en un ordenador, **+** en un móvil o `N`, añade una tarea para lo que quieras. Al crearla no se envía nada. Si no eliges **Trabajo** o **Personal**, se asigna al área que corresponda según a quién y a qué se refiera. También encuentra el correo al que da seguimiento, incluso si es antiguo.

Si la cierras antes de añadirla, el texto y las opciones que hayas elegido estarán ahí la próxima vez; los archivos no se conservan. Usa **Descartar** en el mensaje para quitarlos.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve a aparecer con una frecuencia determinada. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula a las personas o empresas relacionadas, hasta un máximo de 5.
- Icono de mensaje: adjunta el mensaje relacionado, como un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En un móvil, puedes usar la cámara que aparece al lado para hacer una foto. Puedes añadir hasta 5 archivos, igual que en el chat. Consulta [Añadir archivos](card-chat.md#add-files). Pulsa × para quitar uno.

Los archivos se quedan con la tarea y The Machine los lee cuando trabaja en ella. Puedes añadir solo archivos: completa la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas a tamaño completo.
