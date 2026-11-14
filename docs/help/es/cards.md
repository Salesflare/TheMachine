---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita de ti, lista para que la apruebes. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e4ad156150993936
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo necesita de ti. Una tarea por asunto, aunque abarque muchos mensajes.

## Dónde están las tareas

La página **Tareas** las agrupa así:

- **Para ti**: todo lo que está esperando por ti, empezando por lo más urgente. Cada tarea indica **Preparada** (el trabajo está hecho y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero necesita una decisión o respuesta tuya) o **Preparando…** (tu Machine está trabajando en ella).
- **Recién hecho**: un último paso que confirmaste, como un formulario o una incidencia, se completó mientras no estabas. Se queda aquí hasta que toques **Entendido**, como máximo durante un día, y también te avisa en el teléfono.
- **Vuelve más tarde**: las tareas pospuestas y las que no tienen respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas completadas, de la más reciente a la más antigua, con la hora a la que se completaron, como «Hecho hace 5 minutos». Las tareas que parecen completadas ya se marcan como **Parece hecho**.

Después de enviar algo, aparece una nota breve que indica adónde fue la tarea, como «Enviado. Se movió a Hecho» o «Enviado. Se movió a Más tarde hasta el lun.». **Abrir** te lleva a la tarea. Puedes buscar una tarea por su título o por la persona a quien se envió, también en Más tarde y Hecho.

En **Para ti**, primero aparecen las tareas vencidas o que vencen mañana, después las preguntas de tu Fleet y, por último, el resto. Dentro de cada grupo, aparecen de la más reciente a la más antigua. Una tarea mantiene su posición mientras tu Machine la prepara y cuando se completa: solo cambia su estado. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana y luego el resto, de la más reciente a la más antigua. La barra lateral mantiene el mismo orden.

**Parece hecho** significa que tu Machine ve que ya está hecho, como «PR #3451 fusionada», pero la tarea aún no se ha cerrado. **Reabrir** la vuelve a poner en tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Después de un día, se cierra sola y puedes **Deshacer**. Una tarea que ya resolviste por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierra sola.

Una tarea que aún está esperando a otra persona, como una revisión o una respuesta, indica **Esperando a**: ese paso. Aparece en **Esperando a otros**, contraída encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que tú hagas una pregunta: vuelve la mañana antes de la fecha límite, en la fecha límite si es más tarde ese mismo día o a la mañana siguiente si ya pasó. También indica a quién sigue esperando.

Cuando una tarea depende de algo que otra persona debe entregar, como un contrato firmado, **Detalles** lo indica en **Hecho cuando**. Enviar tu parte no la cierra: espera en **Esperando a otros** hasta que un mensaje confirme el resultado. Entonces se cierra sola y puedes **Deshacer**. Si no llega nada para cuando toque insistir, vuelve con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como hecho para cambiarlo.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y puedes **Deshacer**. **Mantener** la conserva y no vuelve a preguntarlo. Si no respondes durante otra semana, se contrae en Vuelve más tarde, y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, escribes un mensaje en el chat, la editas, la pospones o llega un mensaje nuevo, vuelve a aparecer.

Una vez a la semana, un proyecto que se haya quedado inactivo y sin tareas abiertas puede generar una tarea con un siguiente paso concreto, como máximo tres veces por semana. Consulta [Proyectos](projects.md).

Cuando nada necesita de ti, tu Machine descansa y la lista queda vacía. Mientras revisa, se activa y te avisa. Si falla una revisión o se retrasa, la línea lo indica y muestra **Revisar ahora** debajo.

Los filtros **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo un tipo. El teléfono y el ordenador muestran la misma selección. Cuando está activo Trabajo o Personal, **Mostrar todo** vuelve a mostrarlo todo. Una alerta sobre tu Machine, como una parte que se reinicia constantemente, no es ni de Trabajo ni de Personal, y solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente a otro filtro: **Solo Personal · Trabajo · Mostrar todo**.

La fila de la parte superior de la lista muestra el nombre de tu último resumen de la mañana o de la tarde y lo que cuenta, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leer el resumen, con **Copiar** para pegarlo donde quieras. Cuando lo abres o tocas su **×**, aparece en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue abierto, para Trabajo y Personal o solo para el filtro que hayas elegido.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [las tareas de un proyecto](projects.md#a-projects-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También se mueve el acceso a los mensajes que puede leer y enviar. **Deshacer** en la nota la devuelve a su área anterior.

Cuando una tarea necesita tu otra área para continuar y todos los mensajes de los que procede están ahí, se mueve sola y continúa. Si no, muestra **Mover a Trabajo** y no se mueve hasta que lo toques. Una tarea que añadas sin elegir Trabajo o Personal se mueve sola cuando encuentra el área que le corresponde. Hasta entonces, no pertenece ni a Trabajo ni a Personal, y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Cuando necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. El correo de otra de tus empresas va a las tareas de esa empresa, y una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp o un pedido en tu buzón personal, es Trabajo desde el principio. Una tarea que hayas movido o asignado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, pero nunca dónde responde: la respuesta siempre se envía a la conversación original, incluso después de moverla, a menos que elijas otra forma.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo, y nunca aparece en una Fleet de Trabajo ni en el Team Graph.

Si hay dos tareas o más esperando, **Repasar** en el encabezado de Para ti te permite revisarlas una por una, en el orden de la lista. Muestra cada borrador completo, con **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. Debajo del título, el encabezado también indica cuánto se tarda a tu ritmo, como «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen en ninguna de las dos opciones: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Revisa lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente revisión, dentro de la hora.

Por la noche, desde las 00:00 hasta las 06:30, las revisiones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se revisan juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Conexiones, Revisiones indica «Pausadas por la noche. Se pondrán al día a las 06:30». Si abres la app, escribes en el chat o tocas una tarea por la noche, las revisiones vuelven a ejecutarse con normalidad hasta que lleves una hora sin usarla. **Revisar ahora** siempre inicia una revisión de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no tienes tareas abiertas, toca la línea de tu Machine para verla, junto con **Detalles**, que abre Revisiones en Conexiones. Si tienes tareas abiertas, aparece en la parte superior en el ordenador. Solo se muestra una línea breve mientras se realiza una revisión, o cuando una ha fallado o se ha retrasado. También puedes preguntar en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última revisión

Después de una revisión que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que encontró en todas las fuentes que leyó, como «13 mensajes revisados a las 16:11 · nada necesita de ti» o «· 2 tareas nuevas». Si una tarea nueva espera a un momento más oportuno, como el resumen de la mañana, indica hasta cuándo: «1 tarea reservada hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién escribió, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo estabas en copia, una persona del equipo responderá» o «La reunión ya está programada para el jueves». Si la revisión solo encontró un motivo impreciso, no se muestra ninguno. Toca un elemento para leerlo.

Se muestran los primeros 10 y, al tocar debajo, aparece el resto. Un número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Las notificaciones del teléfono sobre mensajes que ya aparecen en la lista se muestran una sola vez. La línea aparece durante 12 horas después de la revisión.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Los propios correos de The Machine, como el resumen de la mañana o un aviso de solución, nunca se leen ni aparecen en la lista. El correo sobre la facturación, la prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** sirve para indicar qué cambiar: cómo hacerlo o, cuando el borrador esté listo, qué cambiar en él. **Marcar como hecha** indica que ya está resuelta: aparece directamente en una tarea lista sin borrador; en los demás casos, incluida una tarea que necesita tu decisión, está al principio de **…**. La tarea sale de la lista inmediatamente y aparece **Deshacer** en el mensaje. Desliza el mensaje para quitarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se mantiene.

Para que se haga de otra manera, dilo en su **Chat**.

En **…**:

- **Pasar…**: asígnasela a alguien del equipo, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: [volverá a aparecer de forma periódica](recurring.md).
- **No hace falta**: desaparece. Si quieres, elige un motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarle el nombre. El título que le pongas se mantiene.

**Reabrir** vuelve a abrir una tarea cerrada. También puede volver a aparecer automáticamente cuando ocurre algo nuevo, como recibir un mensaje de esa persona, pero no al responder tú.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluya. Las facturas con pago automático, como las domiciliadas o las cargadas a una tarjeta guardada, no se convierten en tareas. Cuando un correo posterior indica que se ha pagado, por ejemplo, porque el remitente confirma que recibió el pago, la tarea se cierra sola. Puedes **Deshacer** durante un día.

Una tarea que solo era relevante hasta una hora determinada, como una confirmación antes de una reunión, se cierra sola después de esa hora. Pasa a **Hecho / descartado** con el estado «Ya no hace falta». Puedes **Deshacer** durante un día.

Antes de que un mensaje o un traspaso para alguien aparezca como listo, tu Machine revisa tus chats recientes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, que se lo pidieron y dijo que sí, la tarea se cierra sola. Puedes **Deshacer** durante un día.

Cuando un mensaje nuevo cambia el plan, como cuando una fiesta se traslada a otro sitio o se cancela una reserva, The Machine actualiza sus tareas. Si una tarea sigue siendo relevante, se ajusta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** con el estado «No hace falta». En el chat aparece «Actualizado:» junto con el motivo y puedes **Deshacer** durante un día.

En tus primeras tareas, aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**. También te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas el botón o pulsas ×.

El primer día, la parte superior de Tareas te da la bienvenida e indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno; de lo contrario, muestran sus iniciales. Si un logotipo no se distingue bien en tamaño pequeño, por ejemplo, porque es blanco sobre un fondo transparente o porque es un logotipo apaisado con el nombre, también se muestran las iniciales.

A veces aparece una línea discreta que indica lo que no se sabe, como «Último contacto hace 12 días por correo; no ha habido nada desde entonces». Se muestra cuando el último contacto con esa persona es antiguo o sigue sin respuesta, y nombra los canales que no están conectados, como WhatsApp. Tu Machine indica lo que no sabe en lugar de adivinar.

Si menciona un canal que no está conectado, **Conectar**, a su lado, abre esa conexión.

El título indica lo que hay que hacer y solo cambia si eso cambia. Una tarea completada conserva su título y muestra debajo cómo terminó, como «Hecho: Sam lo firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede, con el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del destino para que veas de inmediato si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que alguien dijo en otro lugar, como una sugerencia de un compañero en Slack, una línea lo indica, como «Basado en un mensaje de Sam en #ops». Tócala para leer ese mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) aparece como una sola conversación, de los mensajes más antiguos a los más recientes: los mensajes anteriores al que dio lugar a la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje relacionado con la tarea se marca como «Esta tarea» y se abre en la conversación. **Mostrar mensajes anteriores** añade mensajes más antiguos. En un correo, el resto del hilo aparece contraído encima y debajo.

**Detalles** de un correo solo muestra lo que no aparece en el encabezado, como las direcciones completas en Cc, Bcc o una dirección distinta para responder. Si no hay nada que añadir, no aparece.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre, el proyecto y el área (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. **Chat ›** abre el chat. Una tarea completada se muestra de forma resumida; el mensaje del que procede aparece en **Detalles**.

Una tarea con el estado «Esperando a» enlaza tu último mensaje a esa persona, el que está esperando respuesta: «Correo a Pat · mar».

## Crear una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador) crea una tarea para cualquier cosa. Al crearla no se envía nada. Si no eliges Trabajo o Personal, se asigna al área que le corresponde según de quién y de qué trate. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie.», «3 nov», «14:00» o «en 2 horas». También puedes escribirlo en tu idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Mensaje**: adjunta el mensaje relacionado: un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde viene, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En el teléfono, puedes hacer una foto con la cámara que aparece al lado. Puedes añadir hasta 5 archivos, como en el chat (consulta [Añadir archivos](card-chat.md#add-files)). × quita un archivo.

Los archivos se quedan con la tarea y The Machine los lee cuando trabaja en ella. Puedes adjuntar archivos sin más: completa la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas a tamaño completo.
