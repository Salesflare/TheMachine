---
title: Tareas
area: cards
summary: Una tarea por cada asunto que requiere tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 16f31364b3da3827
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo requiere tu atención. Una tarea por asunto, aunque implique muchos mensajes.

## Dónde están las tareas

La página **Tareas** las agrupa:

- **Recién hecho**: arriba, aparece el último paso que confirmaste, como un formulario o un problema, que se completó mientras no estabas. Se queda hasta que toques **Entendido**, como máximo un día, y también te avisa en el teléfono.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (el trabajo está hecho y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero hace falta que decidas o respondas), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y las que no recibieron respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otros te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con la hora en que terminaron, como «Hecha hace 5 minutos». Las tareas que parecen estar terminadas se marcan como **Parece hecho**.

Después de enviar algo, aparece una nota breve que indica adónde fue la tarea, como «Enviado. Pasó a Hecho» o «Enviado. Pasó a Más tarde hasta el lunes». **Abrir** te lleva a ella. Puedes buscar una tarea por su título o por la persona a quien se envió, también en Más tarde y Hecho.

En **Para ti**, primero aparecen las tareas vencidas o que vencen mañana o antes, después las preguntas de tu Fleet, luego los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, aparecen de la más reciente a la más antigua. Una tarea mantiene su lugar mientras tu Machine la prepara y cuando termina: solo cambia su estado. En los demás grupos abiertos, primero aparecen las vencidas o las que vencen mañana o antes, y después el resto, de la más reciente a la más antigua. La barra lateral mantiene el mismo orden.

**Parece hecho** significa que tu Machine ve que ya está terminado, como «PR #3451 integrado», pero todavía no está cerrado. **Reabrir** lo devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Después de un día, se cierran solas y puedes usar **Deshacer**. Una tarea que ya resolviste por tu cuenta, por ejemplo respondiendo en Gmail o Slack, también se cierra sola.

Si un mensaje viene de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». Se muestra a esa persona con su dirección, nunca con el nombre que usó. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo escribió.

Si una tarea sigue pendiente de otra persona, como una revisión o una respuesta, indica **Esperando a**: y el paso pendiente. Aparece plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que devuelvas una pregunta: vuelve la mañana antes de la fecha límite, en la fecha límite si es más tarde ese mismo día, o a la mañana siguiente si ya venció. También indica quién sigue pendiente.

Si la tarea depende de algo que tiene que entregar otra persona, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje confirme el resultado y entonces se cierra sola. Puedes usar **Deshacer**. Si no llega nada cuando toque hacer seguimiento, vuelve con **Escribe un recordatorio breve** en su chat. Para cambiar qué se considera terminado, díselo en el chat.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y puedes usar **Deshacer**. **Mantener** la conserva y no vuelve a preguntarte. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Al abrirla, enviar un mensaje por el chat, editarla, posponerla o recibir un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que se haya quedado sin actividad y sin tareas abiertas puede generar una tarea con un siguiente paso concreto, hasta tres por semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, aparece un aviso y **Revisar ahora** debajo.

Los filtros **Todo**, **Trabajo** y **Personal** en la parte superior de la barra lateral muestran todas las tareas o solo las de un tipo. Tu teléfono y tu ordenador muestran la misma selección. Si tienes activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Un aviso sobre tu Machine, como que una parte se reinicia continuamente, no es de Trabajo ni de Personal, y solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente al otro filtro: en **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el último resumen de la mañana o de la tarde y lo que incluía, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leerlo. Puedes usar **Copiar** para pegarlo donde quieras. Cuando lo abras o toques su **×**, estará disponible en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, para Trabajo y Personal, o solo para el filtro que hayas elegido.

Una tarea de un proyecto muestra el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Las tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, pasa una tarea a tu otra área. También cambia el área desde la que puede leer y enviar mensajes. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita pasar a tu otra área para continuar y todos los mensajes relacionados ya están allí, se mueve por sí sola y sigue adelante. Si no, aparece **Mover a Trabajo** y no se mueve hasta que lo toques. Una tarea que hayas añadido sin elegir Trabajo o Personal se mueve sola cuando encuentra el área que le corresponde. Hasta entonces, no aparece ni en Trabajo ni en Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. El correo de otra de tus empresas va a las tareas de esa empresa. Una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que recibes en una cuenta personal, como un cliente en WhatsApp o un pedido en tu buzón personal, es Trabajo desde el principio. Una tarea que hayas movido o asignado tú se queda siempre donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, nunca desde dónde responde: la respuesta siempre va al lugar donde está la conversación, incluso después de moverla, a menos que elijas otra opción.

Aunque sea Personal, una tarea responde desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de Trabajo ni en el Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, te permite revisarlas de una en una en el orden de la lista, con cada borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el proceso. Debajo del título, el encabezado también indica cuánto tardarás a tu ritmo, como «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes nuevos cuando hay 40 pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, dentro de la hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se comprueban juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «Pausadas por la noche; se pondrán al día a las 06:30». Si haces clic, escribes o te desplazas por la app, escribes en el chat o tocas una tarea durante la noche, las comprobaciones se reanudan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba todo de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no tienes tareas abiertas, toca la línea de tu Machine para verla junto con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, está en la parte superior de la lista en el ordenador. Allí solo aparece una línea breve mientras se está realizando una comprobación, o si ha fallado o se ha retrasado. También puedes preguntarle en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas que indica qué encontró en todas las fuentes que leyó, como «Se comprobaron 13 mensajes a las 16:11 · nada requiere tu atención» o «· 2 tareas nuevas». Si una tarea nueva espera al momento oportuno, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, junto al icono de su fuente: quién escribió, el asunto o las primeras palabras, y la nueva tarea o el motivo por el que no hacía falta ninguna, como «Solo estaba en copia; un compañero está respondiendo» o «La reunión ya está programada para el jueves». Un hilo no muestra ningún motivo si la comprobación solo encontró uno impreciso. Toca uno para leerlo.

Se muestran los primeros 10. Toca debajo para ver el resto. Un número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Las notificaciones del teléfono sobre un mensaje que ya aparece en la lista solo se muestran una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para tener contexto y registrar promesas, pero no cuentan como correo nuevo. Los correos de The Machine, como el resumen de la mañana o un aviso de reparación, nunca se leen ni aparecen en la lista. El correo sobre facturación, tu periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, y **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué hay que cambiar: cómo hacerlo o, cuando el borrador esté listo, qué cambiar en él. **Marcar como hecha** indica que ya está resuelta: aparece a la vista en una tarea lista sin borrador y, en los demás casos, en la parte superior de **…**, también en las tareas que necesitan que decidas. La tarea sale de la lista de inmediato y aparece **Deshacer** en el mensaje. Desliza el mensaje para quitarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Para que se haga de otra manera, díselo en su **Chat**.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve a aparecer según un ritmo](recurring.md).
- **No es relevante**: desaparece. Si quieres, elige un motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarle el nombre. El título que elijas se conserva.

**Reabrir** devuelve una tarea cerrada. También vuelve a aparecer sola cuando ocurre algo nuevo, como un mensaje nuevo de esa persona, pero no cuando respondes tú. Entonces indica cuándo volvió y aparece como nueva en la lista. El chat continúa donde se quedó, aunque hayan pasado semanas.

Una factura que todavía tienes que pagar, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluye. No ocurre con las facturas que se pagan automáticamente, como un cargo directo o una tarjeta registrada. Cuando un correo posterior confirma que se pagó, por ejemplo, un mensaje del remitente que confirma que recibió el pago, la tarea se cierra sola. Puedes usar **Deshacer** durante un día para recuperarla.

Una tarea que solo era relevante hasta una hora determinada, como una confirmación antes de una reunión, se cierra sola cuando pasa esa hora. Pasa a **Hecho / descartado** con el estado «Ya no hace falta». Puedes usar **Deshacer** durante un día para recuperarla.

Antes de que un mensaje o un traspaso para alguien aparezca como listo, tu Machine comprueba los chats recientes que tienes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está resuelto, por ejemplo, porque se lo pidieron y dijo que sí, la tarea se cierra sola. Puedes usar **Deshacer** durante un día para recuperarla.

Si un mensaje más reciente cambia el plan, como cuando se cambia de lugar una fiesta o se cancela una reserva, The Machine actualiza sus tareas. Si una tarea sigue siendo necesaria, se adapta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** con el estado «No hace falta». En el chat aparece «Actualizado:» junto con el motivo y puedes usar **Deshacer** durante un día para recuperarla.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas su botón o pulsas ×.

El primer día, en la parte superior de Tareas te damos la bienvenida y te decimos quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién se trata, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, si es de Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en el Graph.

Si el Graph tiene una foto o un logotipo de una persona o una organización, lo muestra. Si no, muestra sus iniciales. Si un logotipo no se distingue a ese tamaño, como uno blanco sobre fondo transparente o un logotipo horizontal con el nombre, también muestra las iniciales.

A veces aparece una línea discreta que indica qué no se sabe, como «Último contacto hace 12 días por correo; no ha habido nada desde entonces». Aparece cuando el último mensaje de esa persona es antiguo o no tiene respuesta, y menciona los canales que no están conectados, como WhatsApp. Tu Machine indica lo que no sabe en lugar de adivinar.

Si se menciona un canal que no está conectado, **Conectar**, junto a él, abre esa conexión.

El título indica qué hay que hacer y solo cambia si cambia la tarea. Las tareas terminadas conservan su título y muestran debajo cómo terminaron, como «Hecha: Sam la firmó el martes».

Encima del borrador aparece una línea tenue con el mensaje del que procede y el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del lugar al que se enviará, así puedes ver enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que dijo alguien en otro lugar, como una sugerencia de un compañero en Slack, aparece una línea que lo indica, como «Basado en lo que dijo Sam en #ops». Tócala para leer ese mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) muestra una conversación completa en orden, de los mensajes más antiguos a los más recientes: los mensajes anteriores al que trata la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje relacionado con la tarea se marca como «Esta tarea» y se abre en la conversación. **Mostrar mensajes anteriores** añade mensajes más antiguos. Los demás mensajes del hilo de un correo aparecen plegados encima y debajo.

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, lo abre en la app de Gmail si la tienes instalada.

En **Detalles** de un correo solo aparece la información que no figura en el encabezado, como las direcciones completas en Cc, Cco o una dirección de respuesta distinta. Si no hay nada más, no aparece nada.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre, el proyecto, el área (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Las tareas terminadas se muestran de forma resumida; el mensaje del que proceden está en **Detalles**.

Una tarea con el estado «Esperando a» incluye un enlace a tu último mensaje para esa persona, el que está pendiente de respuesta: «Correo para Pat · mar».

## Crear una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un teléfono o `N`) añade una tarea para cualquier cosa. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, se asigna al área que le corresponde según quién y qué la tarea menciona. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Se repite**: vuelve a aparecer según un ritmo. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula a las personas o empresas relacionadas, hasta 5.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En un teléfono, puedes sacar una foto con la cámara que aparece al lado. Hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Toca × para quitar un archivo.

Los archivos se quedan con la tarea y The Machine los lee cuando trabaja en ella. También puedes crear una tarea solo con archivos: completa los datos a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas a tamaño completo.
