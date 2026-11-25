---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 43d9497d3a1c4a86
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo necesita tu atención. Una tarea por asunto, aunque aparezca en varios mensajes.

## Dónde están las tareas

La página **Tareas** las agrupa así:

- **Recién hecho**: arriba, aparece el último paso que confirmaste, como un formulario o un problema, que se completó mientras no estabas. Se queda ahí hasta que pulses **Entendido**, durante un máximo de un día. También recibirás una notificación en el móvil.
- **Para ti**: todo lo que está pendiente de ti, primero lo que vence mañana o antes. Cada tarea indica **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo pone en marcha), **Te necesita** (primero hace falta que decidas o respondas; cuando el trabajo no puede continuar ni usarse sin algo que solo tú tienes, como un precio, un dato o una decisión, aparece una línea bajo el título que lo explica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas que no han tenido novedades en una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas, mensajes que [se envían más tarde](send-later.md) y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, primero las más recientes y con la hora a la que se completaron, como «Hecho hace 5 minutos». Las tareas que parecen terminadas llevan la marca **Parece hecha**.

Después de enviar, aparece una nota breve que indica dónde ha ido la tarea, como «Enviado. Movido a Hecho» o «Enviado. Movido a Más tarde hasta el lun.». Si la respuesta solo promete que se hará el trabajo, como «Lo enviaré el martes», la tarea sigue abierta: «Enviado. Se mantiene abierta». **Abrir** te lleva a la tarea. Puedes buscar una tarea por su título o por la persona a quien se envió, también en Más tarde y Hecho.

En **Para ti**, primero aparecen las tareas vencidas o que vencen mañana o antes, después las preguntas de tu Fleet, luego los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, primero aparecen las más recientes. Una tarea mantiene su posición mientras tu Machine la prepara y cuando se completa: solo cambia su marca. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana o antes; después, el resto, de la más reciente a la más antigua. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está terminada, como «PR #3451 integrado», pero aún no está cerrada. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si aparece en un mensaje, se cierra automáticamente al cabo de un día y puedes usar **Deshacer**. Si no, espera a que pulses **Marcar como hecho**.

Las tareas que ya hayas resuelto por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierran automáticamente. Una respuesta que dice que se adjunta un archivo cuando no es así no cierra la tarea.

Si un mensaje procede de una dirección que solo parece ser de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». Muestra a la persona con su propia dirección, nunca con el nombre que ha usado. Tu Machine comprueba estos mensajes con la persona de la dirección que ya tienes, nunca con quien los ha escrito.

Una tarea que sigue pendiente de otra persona, como una revisión o una respuesta, indica **Esperando a**: ese paso. Se queda en **Esperando a otros**, plegada encima de Vuelve más tarde, hasta que un mensaje nuevo la haga reaparecer. Lo mismo ocurre después de que hayas devuelto una pregunta: vuelve a aparecer la mañana anterior a la fecha límite, en la fecha límite si es más tarde hoy o a la mañana siguiente si ya ha pasado. También indica de quién sigue esperando respuesta.

Cuando una tarea depende de un resultado que debe entregar otra persona, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no cierra la tarea: se queda en **Esperando a otros** hasta que un mensaje indique que ha llegado el resultado. Entonces se cierra automáticamente y puedes usar **Deshacer**. Si no llega nada cuando toca hacer seguimiento, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Dile en el chat qué se considera terminado para cambiarlo.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que al volver después de unos días veas primero las nuevas. No hay novedades si no ha llegado ningún mensaje nuevo ni has hecho nada en la tarea, como enviar un mensaje de chat, editarla o posponerla. Abrirla no cuenta.

Las tareas urgentes, las que vencen pronto y las que están a punto de enviarse se quedan en Para ti. **Descartar todo** marca como innecesarias todas las tareas de Más antiguos después de una confirmación, igual que **No hace falta** hace con una tarea, y puedes usar **Deshacer**. Si hay alguna novedad en una tarea, vuelve a Para ti.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y puedes usar **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes en otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, envías un mensaje de chat, la editas, la pospones o llega un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede recibir una tarea con un siguiente paso concreto. Como máximo, tres a la semana. Consulta [Proyectos](projects.md).

Cuando nada necesita tu atención, tu Machine descansa y muestra una lista vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, aparece una línea que lo explica, con **Revisar ahora** debajo.

Las opciones **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo las de un tipo. En el móvil y el ordenador aparece la misma selección. Mientras esté activada la opción Trabajo o Personal, **Mostrar todo** te lleva de vuelta a todas las tareas. Una alerta sobre tu Machine, como una pieza que se reinicia una y otra vez, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también te lleva directamente a la otra opción: si estás en **Solo personal**, pulsa **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el título de tu último resumen de la mañana o de la tarde y qué cuenta, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Púlsala para volver a leerlo y usar **Copiar** para pegarlo donde quieras. Cuando lo abras o pulses su **×**, aparecerá en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo de la opción que hayas seleccionado.

Las tareas de un proyecto muestran el nombre del proyecto bajo el título. Púlsalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Las tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a la otra área. También cambia qué puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita la otra área para continuar y todos los mensajes relacionados están allí, se mueve automáticamente y sigue adelante. Si no, muestra **Mover a Trabajo**, y no se mueve hasta que lo pulses. Una tarea que añadas sin elegir Trabajo ni Personal se moverá automáticamente cuando encuentre dónde corresponde. Hasta entonces, no aparece en Trabajo ni en Personal y sigue siendo privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. Los correos de otra de tus empresas van a las tareas de esa empresa, y una tarea sobre tu vida personal, como un mensaje de tu familia en tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp, un pedido en tu buzón personal o una [promesa](promises.md) sobre el trabajo, es Trabajo desde el principio.

Una tarea que hayas movido o asignado tú se queda siempre donde la hayas puesto. Trabajo o Personal determina dónde aparece la tarea y con quién se comparte, nunca dónde responde: la respuesta siempre se envía en la conversación correspondiente, también después de moverla, salvo que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de trabajo ni en el Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar** en el encabezado de Para ti te permite revisarlas de una en una, en el orden de la lista, con cada borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el proceso. El encabezado indica cuánto tardarás a tu ritmo, como «unos 2 min».

Al terminar, cuenta lo que se ha enviado o cerrado y lo que sigue preparándose.

Las tareas que te hacen una pregunta no se incluyen en ninguna de las dos opciones: necesitan tu respuesta, no un toque.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en menos de una hora.

Por la noche, entre las 00:00 y las 06:30, se pausan las comprobaciones: los mensajes nuevos se siguen leyendo y guardando, y se revisan todos juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Conexiones, las comprobaciones indican «Pausadas por la noche; se ponen al día a las 06:30». Si haces clic, escribes o te desplazas por la app, escribes en el chat o pulsas una tarea por la noche, las comprobaciones siguen como siempre hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba todo al momento.

**Revisar ahora** lee todas las fuentes al momento. Si no tienes tareas abiertas, pulsa la línea de tu Machine para verla, con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, aparece arriba en el ordenador. Allí solo aparece una línea breve mientras se ejecuta una comprobación o si ha fallado o se ha retrasado. También puedes preguntarlo en el chat.

LinkedIn, X y Salesflare mantienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que ha encontrado en todas las fuentes que ha leído, como «13 mensajes comprobados a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». Solo se refiere a esa comprobación: las tareas que ya estaban en tu lista siguen pendientes igual que antes. Si una tarea nueva tiene que esperar a un mejor momento, como el resumen de la mañana, indica hasta cuándo: «1 tarea en espera hasta mañana a las 08:30».

Pulsa la línea para ver cada conversación de correo, chat y notificación, con el icono de su fuente: quién la ha escrito, el asunto o las primeras palabras y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo está en copia; otra persona del equipo está respondiendo» o «La reunión ya está fijada para el jueves». Una conversación no muestra el motivo si la comprobación solo dio uno poco claro. Pulsa un elemento para leerlo y ver lo que se dijo a su alrededor.

Se muestran los 10 primeros. Pulsa debajo para ver el resto. Un número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Una notificación de Android sobre un mensaje que ya aparece en la lista solo se muestra una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de reparación, nunca se leen ni se muestran en la lista. Los correos sobre facturación, tu periodo de prueba o una invitación se leen con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué quieres cambiar: cómo hacerlo o, cuando haya un borrador listo, qué cambiar en él. Si dejas el texto a medias, seguirá ahí cuando vuelvas; **Cancelar** lo descarta.

**Marcar como hecho** indica que ya está resuelta. En un ordenador, aparece junto a los otros botones cuando caben en una línea. En el móvil, está a la vista en las tareas listas sin borrador y en las que te hacen una pregunta. En los demás casos, está arriba en **…**. La tarea desaparece de la lista al momento y aparece **Deshacer** en el mensaje. Desliza el mensaje o arrástralo fuera con el ratón para cerrarlo antes. El cambio se mantiene.

Si quieres que se haga de otra manera, dilo en su **Chat**. La respuesta solo menciona los cambios realizados, como que se ha pospuesto y hasta cuándo. Si no se ha podido cambiar algo, como la fecha de vencimiento, te lo indica.

En **…**:

- **Pasar…**: asígnasela a alguien del equipo, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve a aparecer siguiendo un ritmo](recurring.md).
- **No hace falta**: desaparece. Si quieres, indica el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Pulsa el título o **Nombre**, en **Detalles**, para cambiarlo, o pídelo en su chat, por ejemplo: «Cámbiale el nombre a…». El título que elijas se mantiene.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve a aparecer automáticamente cuando ocurre algo nuevo, como recibir un mensaje de esa persona, pero no si respondes tú. Entonces indica que ha vuelto a aparecer y se ordena como una tarea nueva. El chat continúa donde lo dejaste, aunque hayan pasado semanas.

Si tienes que pagar una factura tú, de cualquier país, se crea una tarea con el importe, la fecha de vencimiento y los datos de pago que incluye la factura. No se crean tareas para las facturas que se pagan automáticamente, como una domiciliación o una tarjeta guardada. Cuando un correo posterior indique que se ha pagado, por ejemplo, si quien lo envía confirma que ha recibido el pago, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Una tarea que solo era relevante hasta una hora determinada, como una confirmación antes de una reunión, se cierra automáticamente cuando pasa esa hora. Se mueve a **Hecho / descartado** con el estado «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de que un mensaje o una asignación para otra persona aparezca como lista, tu Machine comprueba los chats recientes que hayas tenido con las personas incluidas, también los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo pidieron y aceptó, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Si otra persona escribe en la misma conversación después de que se haya creado el borrador, **Enviar** lo detiene: «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Vuelve a pulsar **Enviar** para enviar el borrador tal como está.

Cuando un mensaje más reciente cambia los planes, como una fiesta que se traslada a otro sitio o una reserva que se cancela, The Machine actualiza sus tareas automáticamente. Si una tarea sigue siendo necesaria, se adapta a los nuevos planes. Si ya no queda nada por hacer, pasa a **Hecho / descartado** como «No hace falta». En su chat aparece «Actualizado:» junto con el motivo y puedes usar **Deshacer** para recuperarla durante un día.

En tus primeras tareas aparece un consejo breve sobre las acciones más importantes: **Pedir cambios** y **No hace falta**, y que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas el botón o pulsas ×.

El primer día, la parte superior de Tareas te da la bienvenida e indica quién lleva más tiempo esperando tu respuesta. Primero se prepara un borrador de esa respuesta para que esté listo cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, si es de Trabajo o Personal y cuándo llegó. Pulsa un nombre para abrir su página en Graph.

Si Graph tiene una foto o un logotipo de una persona o una organización, lo muestra. Si no, muestra sus iniciales. Si un logotipo no se distingue bien a ese tamaño, por ejemplo, si tiene texto blanco sobre un fondo transparente o un nombre muy ancho, también muestra la inicial.

A veces, aparece una línea discreta que indica lo que no se sabe, como «Último contacto hace 12 días por correo; no hay novedades desde entonces». Aparece si el último contacto con esa persona es antiguo o no ha recibido respuesta, y menciona los canales que no están conectados, como WhatsApp. Tu Machine indica lo que no sabe en lugar de hacer suposiciones.

Si menciona un canal que no está conectado, pulsa **Conectar** al lado para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Una tarea completada conserva su título y muestra debajo cómo terminó, como «Hecho: Sam lo firmó el martes».

Encima del borrador, una línea atenuada indica el mensaje del que procede, con el logotipo del servicio. Púlsala para leer la conversación. El borrador muestra el logotipo del canal donde se enviará, para que veas de un vistazo si es una respuesta en Slack o un correo.

Si el borrador se basa en la aportación de alguien en otro sitio, como una sugerencia de un compañero en Slack, aparece una línea que lo indica, como «Basado en un mensaje de Sam en #ops». Púlsala para leer ese mensaje. Desaparece cuando una actualización sustituye el borrador.

Un chat (Slack, WhatsApp, Telegram, Intercom…) aparece como una sola conversación, de más antiguo a más reciente: los mensajes anteriores al que trata la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje de la tarea lleva la marca «Esta tarea» y se abre a la vista. **Mostrar mensajes anteriores** añade mensajes más antiguos. En un correo, el resto del hilo aparece plegado arriba y abajo.

Un mensaje se abre de la misma forma desde la búsqueda, Graph, las respuestas de Ask o la última comprobación, con la marca «Este mensaje» (o «Mensajes nuevos»).

**Abrir en Gmail** abre el correo en la cuenta de Gmail donde lo recibiste. En Android, se abre en la app de Gmail si la tienes instalada.

En **Detalles** de un correo solo aparece la información que no se muestra en el encabezado, como las direcciones completas de Cc, Bcc o una dirección de respuesta distinta. Si no hay nada más que añadir, no aparece ninguna.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** abajo.

**Detalles** muestra el nombre, el proyecto y el área (pulsa uno para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Una tarea completada ocupa menos espacio; el mensaje del que procede está en **Detalles**.

Una tarea que indica «Esperando a» incluye un enlace a tu último mensaje para esa persona, el que estás esperando: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (en **Buscar** en un ordenador, en **+** en un móvil o con `N`) añade una tarea sobre lo que quieras. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, se asigna donde corresponde según quién sea y de qué trate. También encuentra el correo al que da seguimiento, aunque sea antiguo.

Si cierras el formulario antes de añadir la tarea, la próxima vez aparecerán el texto y las opciones que hayas elegido. Los archivos no se conservan. **Descartar** en el mensaje los elimina.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas», también en tu idioma. El icono del calendario ofrece accesos rápidos y **Elegir fecha**.
- **Se repite**: vuelve a aparecer siguiendo un ritmo. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula las personas o empresas relacionadas, hasta 5.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o por remitente. Cada resultado indica de dónde procede, quién lo ha enviado y cuándo.
- **Archivos**: pulsa el clip, pega una captura de pantalla o suelta archivos en el formulario. En un móvil, la cámara de al lado permite hacer una foto. Puedes añadir hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Pulsa × para quitar uno.

Los archivos se quedan en la tarea y The Machine los lee mientras trabaja en ella. Puedes adjuntar solo archivos: crea la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Púlsalas para verlas a tamaño completo.
