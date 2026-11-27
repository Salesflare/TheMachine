---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: b218e3423a2162c5
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo requiere tu atención. Una tarea por asunto, aunque abarque muchos mensajes.

## Dónde están las tareas

La página **Tareas** las agrupa:

- **Recién hecho**: arriba, un último paso que confirmaste, como enviar un formulario o resolver una incidencia, se completó mientras no estabas. Se queda ahí hasta que toques **Entendido**, como máximo un día. También te avisará en el móvil.
- **Para ti**: todo lo que está pendiente de ti, primero lo que vence mañana o antes. Cada tarea indica **Preparada** (hay un borrador o resultado listo y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero necesita que decidas o respondas; si el trabajo no puede continuar o usarse sin algo que solo tú puedes aportar, como un precio, un dato o una elección, aparece una línea bajo el título que lo explica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas que llevan una semana sin novedades (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso le corresponde a otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas, mensajes que [se envían más tarde](send-later.md) y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, empezando por la más reciente, y cuándo se completaron, por ejemplo, «Hecho hace 5 minutos». Las tareas que parecen terminadas se marcan como **Parece hecha**.

Después de enviar algo, una nota breve indica adónde ha ido la tarea, por ejemplo: «Enviado. Se ha movido a Hecho» o «Enviado. Se ha movido a Más tarde hasta el lunes». Si una respuesta solo promete hacer el trabajo, como «Te lo enviaré el martes», la tarea sigue abierta: «Enviado. Se mantiene abierta». **Abrir** te lleva a la tarea. Puedes buscar tareas por título o por la persona a quien se enviaron, también en Más tarde y Hecho.

En **Para ti** aparecen primero las tareas atrasadas o que vencen mañana o antes, después las preguntas de tu Fleet, luego los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, se muestran primero las más recientes. Una tarea conserva su sitio mientras tu Machine la prepara y cuando está hecha: solo cambia su marca. En los otros grupos abiertos, aparecen primero las tareas atrasadas o que vencen mañana o antes, y después el resto, empezando por las más recientes. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que está hecha, por ejemplo, «PR #3451 fusionada», pero aún no está cerrada. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si el mensaje muestra que está hecha, se cierra sola al cabo de un día y aparece **Deshacer**. Si no, espera a que uses **Marcar como hecha**.

Una tarea que ya resolviste por tu cuenta, por ejemplo respondiendo en Gmail o Slack, también se cierra sola. Si una respuesta dice que se ha adjuntado un archivo cuando no es así, la tarea no se cierra.

Si un mensaje viene de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Este no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que usó. Tu Machine comprueba esos mensajes con la persona de la dirección que ya tienes, nunca con quien los escribió.

Una tarea que sigue pendiente de otra persona, como una revisión o una respuesta, indica ese paso con **Esperando a:**. Aparece plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que hayas respondido con una pregunta: la tarea vuelve a aparecer la mañana anterior a la fecha límite, el mismo día si vence más tarde, o a la mañana siguiente si ya ha vencido. También indica a quién sigue esperando.

Si una tarea depende de que otra persona entregue un resultado, como un contrato firmado, en **Detalles** aparece **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje muestre el resultado. Entonces se cierra sola y muestra el resultado y **Deshacer**. Si no llega nada cuando toque hacer seguimiento, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Para cambiar lo que cuenta como hecho, díselo en el chat.

Antes de cerrarla, tu Machine compara el resultado con lo acordado en el hilo, como el precio, el texto o el enlace que enviaste. Solo la cierra si coincide, y te dice qué ha comprobado. Si algo no coincide, se han saltado tu visto bueno o tu parte de un intercambio sigue pendiente, la tarea vuelve a aparecer y te explica por qué.

Si el resultado va a aparecer en una página web pública mencionada en los mensajes, como un artículo donde aparecerá tu nombre, tu Machine consulta esa página cuando toca hacer seguimiento. Si aparece allí y no lo hacía cuando la tarea empezó a estar pendiente, lo comprueba del mismo modo antes de cerrarla. Solo lee la página, como cualquier visitante, y nunca envía nada.

Si el resultado no aparece en la página y aún no ha llegado la fecha límite, vuelve a consultarla a la mañana siguiente. De lo contrario, la tarea vuelve a aparecer como antes, con «Comprobado» o «No se ha podido abrir» y la página en su chat.

Si una tarea lleva una semana sin novedades, pasa de Para ti a **Más antiguos**, para que lo reciente aparezca primero después de unos días sin entrar. No hay novedades cuando no ha llegado ningún mensaje nuevo ni has hecho nada en la tarea, como enviar un mensaje en el chat, editarla o posponerla. Abrirla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío programado siguen en Para ti. **Descartar todo** marca como innecesarias todas las tareas de Más antiguos después de una confirmación, igual que **No hace falta** las marca una a una, con **Deshacer**. Si hay novedades en una tarea, vuelve a Para ti.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y muestra **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, envías un mensaje en el chat, la editas, la pospones o llega un mensaje nuevo, vuelve a aparecer.

Una vez a la semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede generar una tarea con un siguiente paso concreto. Como máximo, tres por semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine descansa y deja la lista vacía. Mientras comprueba, se activa y te avisa. Si una comprobación ha fallado o se ha retrasado, la línea lo indica y muestra **Revisar ahora** debajo.

Los filtros **Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, muestran todas las tareas o solo las de un tipo. En el móvil y el ordenador aparece la misma selección. Si está activado Trabajo o Personal, **Mostrar todo** vuelve a la vista completa. Una alerta sobre tu Machine, como que un componente se reinicia continuamente, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente al otro filtro: en **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista indica cuál fue tu último resumen de la mañana o de la tarde y qué incluía, por ejemplo, **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leerlo y usa **Copiar** para pegarlo donde quieras. Cuando lo abras o toques su **×**, estará disponible en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue abierto, en Trabajo y Personal o solo en el filtro que hayas seleccionado.

Una tarea de un proyecto muestra el nombre del proyecto debajo del título. Tócalo para abrirlo. **Proyecto**, en **Detalles**, permite cambiar el proyecto o quitarlo. Consulta [Tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. Lo que pueda leer y enviar también cambia con ella. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita estar en tu otra área para continuar y todos los mensajes de los que procede están allí, se mueve sola y sigue adelante. De lo contrario, muestra **Mover a Trabajo** y no se mueve hasta que lo toques. Una tarea que hayas añadido sin elegir Trabajo o Personal se mueve sola cuando encuentra dónde corresponde. Hasta entonces, no aparece ni como Trabajo ni como Personal, y sigue siendo privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, pregunta con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. El correo de otra de tus empresas va a las tareas de esa empresa. Una tarea sobre tu vida personal, como un familiar que escribe a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp, un pedido en tu buzón personal o una [promesa](promises.md) relacionada con el trabajo, es Trabajo desde el principio.

Una tarea que hayas movido o colocado tú siempre se queda donde la pongas. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, pero nunca adónde responde: la respuesta siempre se envía al lugar de la conversación, también después de moverla, salvo que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo, y nunca aparece en un Fleet de trabajo ni en Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar** en el encabezado de Para ti las recorre de una en una, en el orden de la lista. Muestra cada borrador completo, con **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. El encabezado indica cuánto tardarás a tu ritmo, por ejemplo, «unos 2 min».

Al terminar, indica cuántas tareas se han enviado o cerrado y cuántas se siguen preparando.

Las tareas que te hacen una pregunta no se incluyen en el repaso: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, como máximo en una hora.

Por la noche, desde las 00:00 hasta las 06:30, las comprobaciones se pausan. Los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30, para que las tareas estén listas antes del resumen de la mañana. En Conexiones, la sección Comprobaciones indica «Pausado por la noche; se pondrá al día a las 06:30». Si haces clic, escribes o te desplazas por la app, escribes en un chat o tocas una tarea durante la noche, las comprobaciones siguen funcionando como siempre hasta que lleves una hora sin usarla. **Revisar ahora** siempre inicia una comprobación al momento.

**Revisar ahora** lee todas las fuentes al momento. Si no tienes tareas abiertas, toca la línea de tu Machine para verla, con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, aparece arriba en un ordenador. Una línea breve solo aparece mientras se ejecuta una comprobación o si ha fallado o se ha retrasado. También puedes preguntarlo en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que ha encontrado en cada fuente que ha leído, por ejemplo: «Se han comprobado 13 mensajes a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». La línea solo se refiere a esa comprobación: las tareas que ya estaban en tu lista siguen igual. Si una tarea nueva se queda pendiente para un momento más oportuno, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién lo escribió, el asunto o las primeras palabras, y la nueva tarea o el motivo por el que no hacía falta crear una, como «Solo estabas en copia; un compañero está respondiendo» o «La reunión ya está programada para el jueves». Si la comprobación solo dio un motivo impreciso, no se muestra ningún motivo en el hilo. Toca uno para leerlo junto con los mensajes relacionados.

Se muestran los primeros 10; toca debajo para ver el resto. El número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Una notificación de Android sobre un mensaje que ya aparece en la lista solo se muestra una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para tener contexto y detectar promesas, pero no cuentan como correo nuevo. Los correos que te envía The Machine, como el resumen de la mañana o un aviso de reparación, nunca se leen ni aparecen en la lista. El correo sobre facturación, tu periodo de prueba o una invitación se lee como siempre.

## Los botones

Una tarea muestra su siguiente paso, como **Hazlo** o **Revisar y enviar**, y **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué quieres cambiar: cómo hacerlo o, cuando haya un borrador listo, qué cambiar en él. Si dejas el texto a medias, seguirá ahí cuando vuelvas; **Cancelar** lo descarta.

**Marcar como hecha** indica que ya está resuelta. En un ordenador, aparece con los demás botones cuando caben en una línea. En un móvil, se ve en una tarea lista que no tiene borrador o que te hace una pregunta; en los demás casos, está arriba en **…**. La tarea desaparece de la lista al momento y aparece **Deshacer** en el mensaje. Desliza el mensaje o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Para que se haga de otra manera, díselo en su **Chat**. La respuesta solo indica qué ha cambiado, por ejemplo, si se ha pospuesto y hasta cuándo. Si no ha podido cambiar algo, como la fecha de vencimiento, te lo dirá.

En **…**:

- **Pasar…**: asígnala a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve a aparecer con cierta frecuencia](recurring.md).
- **No hace falta**: la quita de la lista. Si quieres, indica por qué: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarlo. También puedes pedirlo en su chat, por ejemplo: «Cámbiale el nombre a…». El título se conserva.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve a aparecer por sí sola cuando pasa algo nuevo, como un mensaje de la otra persona, pero no cuando respondes tú. Entonces indica cuándo volvió y aparece como nueva. El chat continúa donde lo dejaste, incluso si han pasado semanas.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluya. Las facturas que se pagan automáticamente, por ejemplo mediante domiciliación o con una tarjeta guardada, no se convierten en tareas. Cuando un correo posterior indica que se ha pagado, por ejemplo, porque el remitente confirma que ha recibido el pago, la tarea se cierra sola. **Deshacer** la recupera durante un día.

Una tarea que solo era relevante hasta una hora concreta, como una confirmación antes de una reunión, se cierra sola al pasar esa hora. Pasa a **Hecho / descartado** con la indicación «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de que un mensaje o un traspaso para otra persona aparezca como listo, tu Machine comprueba tus chats recientes con las personas involucradas, también los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo pidieron y respondió que sí, la tarea se cierra sola. **Deshacer** la recupera durante un día.

Si otra persona escribe en la misma conversación después de que se haya creado el borrador, **Enviar** lo retiene y muestra: «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** otra vez para enviar el borrador tal como está.

Si un mensaje posterior cambia el plan, por ejemplo, porque la fiesta se traslada a otro local o se cancela una reserva, The Machine actualiza las tareas por su cuenta. Si la tarea sigue siendo necesaria, se adapta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** con la indicación «No hace falta». En el chat aparece «Actualizado:» junto con el motivo, y **Deshacer** la recupera durante un día.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas el botón correspondiente o pulsas ×.

El primer día, aparece un saludo en la parte superior de Tareas y se indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero, para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién se trata, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno; si no, muestran sus iniciales. Si el logotipo no se distingue bien a ese tamaño, por ejemplo, si es blanco sobre fondo transparente o tiene un nombre muy ancho, también se muestra la inicial.

A veces, una línea discreta indica algo que no se sabe, como «Último contacto hace 12 días por correo; no hay novedades». Aparece si hace mucho que no tenéis noticias o si aún no habéis recibido respuesta, e indica los canales que no están conectados, como WhatsApp. Tu Machine dice lo que no sabe en lugar de hacer suposiciones.

Si menciona un canal que no está conectado, al tocar **Conectar** junto a él se abre esa conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Una tarea hecha conserva su título y muestra debajo cómo terminó, por ejemplo, «Hecho: Sam lo firmó el martes».

Encima del borrador, una línea discreta indica de qué mensaje procede, junto con el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del lugar al que se enviará, para que veas de un vistazo si es una respuesta de Slack o un correo.

Si el borrador tiene en cuenta la aportación de alguien en otro sitio, como una sugerencia de un compañero en Slack, una línea lo indica, por ejemplo: «Basado en lo que dijo Sam en #ops». Tócala para leer el mensaje. La línea desaparece cuando una actualización sustituye ese borrador.

Un chat de Slack, WhatsApp, Telegram, Intercom… se muestra como una conversación, de la más antigua a la más reciente: los mensajes anteriores al que trata la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje de la tarea se marca como «Esta tarea» y se abre en la vista. **Mostrar mensajes anteriores** añade los mensajes más antiguos. El resto del hilo de un correo aparece plegado encima y debajo.

Un mensaje se abre del mismo modo desde la búsqueda, Graph, las respuestas de Ask o la última comprobación, y se marca como «Este mensaje» (o «Mensajes nuevos»).

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, se abre en la app de Gmail si la tienes.

En **Detalles** de un correo solo aparece la información que no muestra su encabezado, como las direcciones completas de Cc, Bcc o una dirección de respuesta distinta. Si no hay nada más que añadir, no aparece nada.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** al final.

**Detalles** muestra su nombre, proyecto y área (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Una tarea hecha se muestra de forma resumida; el mensaje del que procede aparece en **Detalles**.

Una tarea que indica «Esperando a» enlaza con tu último mensaje a la persona, el que estás esperando: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un móvil o `N`) crea una tarea sobre cualquier cosa. Al crearla no se envía nada. Si no seleccionas **Trabajo** ni **Personal**, la tarea se coloca donde corresponde según quién y qué la motivaron. También encuentra el correo al que da seguimiento, incluso si es antiguo.

Si la cierras antes de añadirla, el texto y las selecciones estarán ahí la próxima vez; los archivos, no. **Descartar** en el mensaje los elimina.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas», también en tu idioma. El icono del calendario incluye opciones rápidas y **Elegir fecha**.
- **Se repite**: vuelve a aparecer con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula hasta 5 personas o empresas relacionadas.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea de correo, Slack, Teams, WhatsApp, Telegram o cualquier otro que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En un móvil, la cámara que hay al lado permite hacer una foto. Puedes añadir hasta 5 archivos, como en el chat (consulta [Añadir archivos](card-chat.md#add-files)). × quita un archivo.

Los archivos se quedan en la tarea y The Machine los lee cuando trabaja en ella. No hace falta nada más: puede completar la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas; tócalas para verlas a tamaño completo.
