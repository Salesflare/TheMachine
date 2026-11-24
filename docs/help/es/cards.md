---
title: Tareas
area: cards
summary: Una tarea por cada asunto que requiere tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fcb9a016c9af8551
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo requiere tu atención. Una tarea por asunto, aunque incluya varios mensajes.

## Dónde están las tareas

La página **Tareas** las agrupa así:

- **Recién hecho**: arriba aparece el último paso que confirmaste, como enviar un formulario o resolver una incidencia mientras no estabas. Se queda ahí hasta que pulses **Entendido**, como máximo un día, y también te llega al móvil.
- **Para ti**: todo lo que está pendiente de ti, primero lo que vence mañana o antes. Cada tarea indica **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero requiere que tomes una decisión o respondas; si el trabajo no puede continuar o usarse sin algo que solo tú tienes, como un precio, un dato o una decisión, aparece una línea bajo el título que lo indica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas que llevan una semana sin novedades (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas, mensajes que [se envían más tarde](send-later.md) y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otros te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con la hora de finalización, como «Hecha hace 5 minutos». Las tareas que parecen terminadas aparecen marcadas como **Parece hecha**.

Después de enviar algo, una nota breve indica adónde fue la tarea, como «Enviado. Se ha movido a Hecho» o «Enviado. Se ha movido a Más tarde hasta el lunes». Si la respuesta solo promete que se hará el trabajo, como «Lo enviaré antes del martes», la tarea sigue abierta: «Enviado. Se mantiene abierta». **Abrir** te lleva a la tarea. Puedes buscar tareas por título o por la persona a quien se enviaron, también en Más tarde y Hecho.

En **Para ti**, primero aparecen las tareas vencidas o que vencen mañana o antes, luego las preguntas de tu Fleet, después los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, se ordenan de la más reciente a la más antigua. Una tarea mantiene su sitio mientras tu Machine la prepara y cuando está hecha: solo cambia su marca. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana o antes, y luego el resto, de la más reciente a la más antigua. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está hecha, como «PR #3451 fusionada», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si un mensaje indica que está hecha, se cierra automáticamente al cabo de un día y aparece **Deshacer**. Si no, espera a que pulses **Marcar como hecha**.

Una tarea que ya hayas resuelto por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierra automáticamente. Una respuesta que diga que se ha adjuntado un archivo cuando no es así no la cierra.

Si un mensaje procede de una dirección que solo parece pertenecer a alguien que conoces, como sam@acme-corp.example en vez de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». Se muestra a esa persona con su propia dirección, nunca con el nombre que ha usado. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo ha escrito.

Una tarea que sigue esperando a otra persona, por ejemplo una revisión o una respuesta, indica **Esperando a** y el paso pendiente. Aparece plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un nuevo mensaje la reactive. También ocurre cuando has respondido con una pregunta: la tarea vuelve la mañana anterior a la fecha límite, en la fecha límite si es más tarde hoy o a la mañana siguiente si ya ha pasado. Además, indica a quién sigue esperando.

Si la tarea depende de un resultado que otra persona tiene que entregar, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no cierra la tarea: se queda en **Esperando a otros** hasta que un mensaje indique que ya está, y entonces se cierra automáticamente, con **Deshacer**. Si no llega nada cuando toca hacer seguimiento, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Indícale en el chat qué cuenta como terminado para cambiarlo.

Si una tarea lleva una semana sin novedades, pasa de Para ti a **Más antiguos**, para que las tareas nuevas aparezcan primero después de unos días sin entrar. No hay novedades si no hay ningún mensaje nuevo ni actividad tuya, como un mensaje en el chat, una edición o posponer la tarea. Mirarla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca todas las tareas de Más antiguos como innecesarias con una sola confirmación, igual que **No hace falta** lo hace de una en una, con **Deshacer**. Si hay novedades en una tarea, vuelve a Para ti.

Si nadie toca una tarea durante una semana, aparece una vez la pregunta **¿Aún hace falta?**. **No hace falta** la cierra, con **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el icono de la app y en el resumen de la mañana. Si la abres, escribes en el chat, la editas, la pospones o recibes un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede generar una tarea con un siguiente paso concreto, hasta tres por semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, aparece en la línea correspondiente, con **Revisar ahora** debajo.

Las opciones **Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, muestran todas las tareas o solo un tipo. El móvil y el ordenador muestran la misma selección. Si tienes activado Trabajo o Personal, **Mostrar todo** te lleva de vuelta a la lista completa. Una alerta sobre tu Machine, como que una parte se reinicia continuamente, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también te permite cambiar directamente a la otra vista: en **Solo personal**, pulsa **Trabajo** o **Mostrar todo**.

La fila superior de la lista muestra el nombre de tu último resumen de la mañana o de la tarde y lo que incluye, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leerlo y usa **Copiar** para pegarlo donde quieras. Cuando lo abras o pulses su **×**, estará disponible en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo de la categoría que hayas seleccionado.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, te permite cambiarlo o quitarlo. Consulta [Las tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También cambia el contenido al que puede acceder y desde el que puede enviar mensajes. **Deshacer**, en la nota, la devuelve a su sitio.

Si una tarea necesita pasar a tu otra área para continuar y todos los mensajes de los que procede están allí, se mueve automáticamente y sigue adelante. De lo contrario, aparece **Mover a Trabajo** y no se mueve nada hasta que lo pulses. Una tarea que hayas añadido sin elegir Trabajo o Personal se mueve automáticamente cuando encuentra el área que le corresponde. Hasta entonces, no pertenece ni a Trabajo ni a Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. Los correos de otra de tus empresas van a las tareas de esa empresa, y una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp, un pedido en tu buzón personal o una [promesa](promises.md) relacionada con el trabajo, es Trabajo desde el principio.

Una tarea que hayas movido o asignado tú se queda donde la pongas. Trabajo o Personal determina dónde aparece la tarea y con quién se comparte, nunca desde dónde responde: la respuesta siempre se envía donde está la conversación, aunque la tarea se haya movido, a menos que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo, y nunca aparece en un Fleet de trabajo ni en Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, las recorre de una en una y en el orden de la lista. Muestra cada borrador completo, con **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Intro envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el recorrido. El encabezado indica cuánto se tarda a tu ritmo, por ejemplo, «unos 2 min».

Al final, cuenta lo que se ha enviado o cerrado y lo que sigue preparándose.

Las tareas que te hacen una pregunta no se incluyen en ninguno de los dos casos: necesitan tu respuesta, no que pulses un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, antes de una hora.

Por la noche, desde las 00:00 hasta las 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30 para que las tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «Pausadas por la noche; se pondrán al día a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en el chat o tocas una tarea, las comprobaciones se reanudan con normalidad hasta que lleves una hora sin usarla. **Revisar ahora** inicia una comprobación al momento.

**Revisar ahora** lee todas las fuentes al momento. Si no tienes tareas abiertas, toca la línea de tu Machine para verla, con **Detalles**, que abre Comprobaciones dentro de Conexiones. Si tienes tareas abiertas, aparece arriba en el ordenador. La línea solo se muestra mientras se ejecuta una comprobación o si ha fallado o se ha retrasado. También puedes preguntarle en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de las tareas con lo que ha encontrado en cada fuente que ha leído, como «13 mensajes comprobados a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». Solo se refiere a esa comprobación: las tareas que ya estaban en tu lista siguen igual. Si una tarea nueva queda pendiente para un momento más oportuno, como el resumen de la mañana, la línea indica hasta cuándo: «1 tarea pendiente hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién lo ha escrito, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo está en copia; responde un compañero» o «La reunión ya está programada para el jueves». Si la comprobación solo indicó un motivo impreciso, el hilo no muestra ninguno. Toca un elemento para leerlo y ver lo que se dijo a su alrededor.

Se muestran los 10 primeros. Toca debajo para ver el resto. El número que aparece después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Las notificaciones del móvil sobre mensajes que ya aparecen en la lista solo se muestran una vez. La línea permanece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de reparación, nunca se leen ni aparecen en la lista. El correo sobre la facturación, el periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué hay que cambiar: cómo hacerlo o, cuando ya hay un borrador, qué cambiar en él. **Marcar como hecha** indica que ya está resuelta: aparece a la vista en una tarea preparada sin borrador o en una que te hace una pregunta. En los demás casos, está en la parte superior de **…**. La tarea desaparece de la lista enseguida y aparece **Deshacer** en el mensaje. Desliza el mensaje o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Si quieres que se haga de otra manera, indícalo en su **Chat**. La respuesta menciona solo lo que ha cambiado, como si se ha pospuesto y hasta cuándo. Si no ha podido cambiar algo, como la fecha límite, te lo dice.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve a aparecer con cierta frecuencia](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, elige el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarlo. También puedes pedírselo en el chat, por ejemplo: «Cámbiale el nombre a…». El título que elijas se conserva.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve automáticamente cuando pasa algo nuevo, como recibir un mensaje nuevo de esa persona, pero no cuando respondes tú. Entonces indica cuándo volvió y aparece en la lista como una tarea nueva. El chat continúa donde se quedó, aunque hayan pasado semanas.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que aparecen en ella. Las facturas que se pagan automáticamente, como un recibo domiciliado o un cargo a una tarjeta guardada, no. Cuando un correo posterior indique que se ha pagado, por ejemplo, porque el remitente confirma que ha recibido el pago, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Una tarea que solo era necesaria hasta una hora concreta, como una confirmación antes de una reunión, se cierra automáticamente al llegar esa hora. Pasa a **Hecho / descartado** con la indicación «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de que un mensaje o traspaso para otra persona aparezca como listo, tu Machine comprueba los chats recientes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo pidieron y respondió que sí, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Si otra persona ha escrito en la misma conversación después de que se preparara el borrador, **Enviar** lo retiene: «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** otra vez para enviar el borrador tal como está.

Cuando un mensaje nuevo cambia el plan, por ejemplo, si una fiesta cambia de local o se cancela una reserva, The Machine actualiza sus tareas automáticamente. Si una tarea sigue siendo necesaria, se adapta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** con la indicación «No hace falta». En el chat aparece «Actualizado:» y el motivo, y **Deshacer** la recupera durante un día.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y se indica que no se envía nada hasta que pulses **Enviar**. El consejo desaparece definitivamente cuando usas su botón o pulsas ×.

El primer día, la parte superior de Tareas te da la bienvenida y te dice quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con el título. La línea de debajo indica de quién trata, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si aparece en Graph; de lo contrario, muestran sus iniciales. Si un logotipo no se entiende bien a ese tamaño, como uno blanco sobre fondo transparente o un logotipo apaisado con el nombre completo, también se muestran las iniciales.

A veces, una línea discreta indica qué información falta, como «Último contacto hace 12 días por correo; sin novedades desde entonces». Aparece cuando el último contacto es antiguo o no ha recibido respuesta, y menciona los canales que no están conectados, como WhatsApp. Tu Machine indica lo que no sabe en lugar de hacer suposiciones.

Si menciona un canal que no está conectado, pulsa **Conectar** a su lado para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Las tareas completadas conservan su título y muestran debajo cómo terminaron, como «Hecha: Sam la firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede y muestra el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del lugar al que se enviará, para que veas enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en la aportación de alguien en otro lugar, como una sugerencia de un compañero en Slack, aparece una línea que lo indica, como «Basado en un mensaje de Sam en #ops». Tócala para leer el mensaje. La línea desaparece cuando una actualización sustituye el borrador.

Un chat (Slack, WhatsApp, Telegram, Intercom…) aparece como una sola conversación, de los mensajes más antiguos a los más recientes: los mensajes anteriores al que corresponde a la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje de la tarea está marcado como «Esta tarea» y se abre en la conversación. **Mostrar mensajes anteriores** añade mensajes más antiguos. En los correos, el resto del hilo aparece plegado encima y debajo del mensaje.

Los mensajes se abren igual desde la búsqueda, Graph, las respuestas de Ask o la última comprobación, con la marca «Este mensaje» (o «Mensajes nuevos»).

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, se abre en la app de Gmail si la tienes instalada.

**Detalles** de un correo solo muestra la información que no aparece en su encabezado, como todas las direcciones en Cc, Cco o una dirección de respuesta distinta. Si no hay nada más que mostrar, no aparece.

Las respuestas en un hilo de Slack también muestran lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** abajo.

**Detalles** muestra el nombre, el proyecto y el área, que puedes cambiar si tocas cualquiera de ellos, además de tu última nota y el resultado de un agente de programación. El título abre el chat. Las tareas hechas se muestran de forma compacta; el mensaje del que proceden aparece en **Detalles**.

Una tarea que indica «Esperando a» enlaza al último mensaje que enviaste a esa persona y a cuya respuesta estás esperando: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un móvil o `N`) añade una tarea para lo que necesites. Al crearla no se envía nada. Si no eliges **Trabajo** o **Personal**, se asigna al área que corresponda según de quién y de qué trate. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas», también en tu idioma. El icono del calendario incluye opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve a aparecer con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula a las personas o empresas relacionadas, hasta 5.
- Icono de mensaje: adjunta el mensaje relacionado, como un correo, mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En el móvil, toca la cámara que aparece al lado para hacer una foto. Puedes añadir hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Pulsa × para quitar uno.

Los archivos se quedan con la tarea y The Machine los lee cuando trabaja en ella. Los archivos bastan por sí solos: completa la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas a tamaño completo.
