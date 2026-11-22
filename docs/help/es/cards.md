---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: c54b334f5764bdf9
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo necesita tu atención. Una tarea por asunto, aunque incluya muchos mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba del todo, aparece el último paso que confirmaste, como un formulario o una incidencia que se completó mientras no estabas. Se queda ahí hasta que toques **Entendido**, como máximo un día, y también recibes un aviso en el teléfono.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (el trabajo está hecho y **Hazlo** o **Enviar** lo ejecuta), **Te necesita** (antes hace falta que decidas o respondas), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con el momento en que terminaron, como «Hecha hace 5 minutos». Las tareas que parecen terminadas ya llevan la marca **Parece hecho**.

Después de enviar algo, aparece una nota breve que indica adónde fue la tarea, como «Enviado. Se movió a Hecho» o «Enviado. Se movió a Más tarde hasta el lunes». **Abrir** te lleva a la tarea. La búsqueda encuentra tareas por título o por destinatario, también en Más tarde y Hecho.

**Para ti** muestra primero lo que está vencido o vence mañana como muy tarde, luego las preguntas de tu Fleet, después los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, muestra primero lo más reciente. Una tarea conserva su posición mientras tu Machine la prepara y cuando termina: solo cambia su estado. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana como muy tarde y, después, el resto, de la más reciente a la más antigua. La barra lateral mantiene el mismo orden.

**Parece hecho** significa que tu Machine ve que ya está terminado, como «PR #3451 fusionada», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Al cabo de un día, se cierra sola y puedes usar **Deshacer**. Una tarea que ya resolviste por tu cuenta, por ejemplo al responder en Gmail o Slack, también se cierra sola.

Si un mensaje viene de una dirección que se parece a la de alguien que conoces, como sam@acme-corp.example en vez de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La muestra con su propia dirección, nunca con el nombre que haya usado. Tu Machine comprueba estos mensajes con la persona de la dirección que ya tienes, nunca con quien escribió el mensaje.

Si una tarea sigue pendiente de otra persona, por ejemplo una revisión o una respuesta, indica el paso en **Esperando a:**. Se queda plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que respondas con una pregunta: vuelve la mañana anterior a la fecha límite, en la fecha límite si es más tarde ese mismo día, o a la mañana siguiente si la fecha ya pasó. También indica de quién sigue esperando respuesta.

Si la tarea consiste en que otra persona entregue algo, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje indique que se ha entregado el resultado. Entonces se cierra sola y puedes usar **Deshacer**. Si no llega nada cuando toque insistir, vuelve a aparecer con la opción **Escribe un recordatorio breve** en su chat. Para cambiar qué cuenta como terminado, indícalo en el chat.

Si nadie toca una tarea durante una semana, aparece una vez la pregunta **¿Aún hace falta?**. **No hace falta** la cierra y puedes usar **Deshacer**. **Mantener** la conserva y no vuelve a preguntarte. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el icono de la app y en el resumen de la mañana. Si la abres, escribes en el chat, la editas o la pospones, o llega un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede recibir una tarea con un siguiente paso concreto, hasta tres por semana. Consulta [Proyectos](projects.md).

Cuando nada necesita tu atención, tu Machine descansa y muestra una lista vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, lo indica en su línea y muestra **Revisar ahora** debajo.

Los filtros **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo las de un tipo. El teléfono y el ordenador muestran el mismo filtro. Si tienes activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas. Un aviso sobre tu Machine, como que una parte se reinicia constantemente, no es de Trabajo ni de Personal, así que solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente al otro filtro: en **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el nombre de tu último resumen de la mañana o de la tarde y lo que incluye, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leer el resumen. Usa **Copiar** para pegarlo donde quieras. Cuando lo abras o toques su **×**, estará disponible en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo del filtro que hayas elegido.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [las tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a la otra área. También cambia qué mensajes puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita la otra área para continuar y todos los mensajes de los que depende están ahí, se mueve sola y sigue adelante. Si no, muestra **Mover a Trabajo** y no se mueve hasta que lo toques. Si creas una tarea sin elegir Trabajo o Personal, se mueve sola a donde corresponde cuando lo averigua. Hasta entonces, no indica Trabajo ni Personal y sigue siendo privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de la otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. El correo de otra de tus empresas va a las tareas de esa empresa. Una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp o un pedido en tu buzón personal, es Trabajo desde el principio. Una tarea que hayas movido o colocado tú se queda donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, pero no dónde responde: la respuesta siempre se envía en la conversación correspondiente, también después de moverla, salvo que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en una Fleet de Trabajo ni en el Graph del equipo.

Si tienes dos tareas pendientes o más, **Repasar**, en el encabezado de Para ti, las recorre de una en una y en el orden de la lista. Muestra cada borrador completo, con las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc sale. Debajo del título, el encabezado también indica cuánto tardarás a tu ritmo, por ejemplo, «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen en el repaso: necesitan una respuesta, no un toque.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en el plazo de una hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan. Los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Conexiones, la línea de comprobaciones dice «Pausadas durante la noche. Se pondrán al día a las 06:30». Si haces clic, escribes o te desplazas por la app, escribes en el chat o tocas una tarea por la noche, las comprobaciones se ejecutan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba todo en el momento.

**Revisar ahora** lee todas las fuentes inmediatamente. Si no hay tareas abiertas, toca la línea de tu Machine para verla y acceder a **Detalles**, que abre Comprobaciones, en Conexiones. Si hay tareas abiertas, aparece arriba del todo en el ordenador. La línea breve solo aparece mientras se ejecuta una comprobación o si ha fallado o se ha retrasado. También puedes pedirlo en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que encontró en todas las fuentes consultadas, como «13 mensajes comprobados a las 16:11 · nada necesita tu atención» o «· 2 tareas nuevas». Si una tarea nueva espera a que llegue un momento más adecuado, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su servicio: quién escribió, el asunto o las primeras palabras, y la nueva tarea o el motivo por el que no hacía falta crear una, como «Solo está en copia. Responde otra persona del equipo» o «La reunión ya está programada para el jueves». Si la comprobación solo indicó un motivo impreciso, el hilo no muestra ningún motivo. Toca uno para leerlo.

Se muestran los 10 primeros. Toca debajo para ver el resto. El número que aparece después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Las notificaciones del teléfono sobre un mensaje que ya aparece en la lista solo se muestran una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para tener contexto y registrar promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de reparación, nunca se leen ni se muestran en la lista. El correo sobre pagos, tu prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué cambiar: cómo hacerlo o, cuando ya hay un borrador, qué cambiar en él. **Marcar como hecha** indica que ya está resuelta: aparece a la vista en las tareas preparadas sin borrador. En los demás casos, está en la parte superior de **…**, también en las tareas que necesitan que decidas. La tarea desaparece de la lista al momento y el mensaje incluye la opción **Deshacer**. Desliza el mensaje para apartarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se mantiene.

Para que se haga de otra manera, indícalo en su **Chat**.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: [volverá a aparecer con cierta frecuencia](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, elige un motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarle el nombre. También puedes pedírselo en el chat, por ejemplo: «Cámbiale el nombre a…». El título que elijas se mantiene.

**Reabrir** devuelve una tarea cerrada a la lista. También puede volver a aparecer por sí sola cuando ocurre algo nuevo, como un mensaje nuevo de esa persona, pero no cuando respondes tú. Entonces indica cuándo volvió y aparece como nueva. El chat continúa donde lo dejaste, aunque hayan pasado semanas.

Una factura que tienes que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluye. Las facturas con pago automático, como un cargo directo o una tarjeta guardada, no. Cuando un correo posterior indica que se ha pagado, por ejemplo, porque el remitente confirma que ha recibido el pago, la tarea se cierra sola. Puedes usar **Deshacer** durante un día para recuperarla.

Una tarea que solo era pertinente hasta una hora determinada, como una confirmación antes de una reunión, se cierra sola después de esa hora. Pasa a **Hecho / descartado** con el motivo «Ya no hace falta». Puedes usar **Deshacer** durante un día para recuperarla.

Antes de marcar como preparada un mensaje o un traspaso para alguien, tu Machine comprueba los chats recientes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está resuelto, por ejemplo, porque se lo pidieron y dijo que sí, la tarea se cierra sola. Puedes usar **Deshacer** durante un día para recuperarla.

Si un mensaje nuevo cambia el plan, como cuando una fiesta cambia de lugar o se cancela una reserva, The Machine actualiza sus tareas por su cuenta. Si una tarea sigue siendo necesaria, se adapta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** con el motivo «No hace falta». En el chat aparece «Actualizado:» seguido del motivo, y puedes usar **Deshacer** durante un día para recuperarla.

En tus primeras tareas, aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**. También te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas su botón o pulsas ×.

El primer día, la parte superior de Tareas te da la bienvenida y te indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero, para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién se trata, la organización cuando corresponda (no solo porque alguien trabaje allí), el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en el Graph.

Los nombres y las organizaciones muestran su foto o logotipo si aparece en el Graph. Si no, muestran sus iniciales. Si un logotipo no se distingue bien a ese tamaño, como uno blanco sobre un fondo transparente o un logotipo con el nombre muy ancho, también se muestran las iniciales.

A veces aparece una línea discreta que indica lo que no se sabe, como «Último contacto hace 12 días por correo. No ha habido nada más». Aparece cuando el último mensaje de esa persona es antiguo o no tiene respuesta e indica los canales que no están conectados, como WhatsApp. Tu Machine te dice lo que no sabe en lugar de adivinar.

Si se menciona un canal que no está conectado, toca **Conectar** al lado para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Una tarea terminada conserva su título y muestra debajo cómo terminó, como «Hecha: Sam la firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede y muestra el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del servicio al que se enviará, para que veas de inmediato si es una respuesta de Slack o un correo.

Si el borrador se basa en información que alguien aportó en otro sitio, como una sugerencia de un compañero en Slack, una línea lo indica, por ejemplo, «Basado en un mensaje de Sam en #ops». Tócala para leer ese mensaje.

Los chats de Slack, WhatsApp, Telegram, Intercom y otros servicios aparecen como una sola conversación, de más antiguo a más reciente: los mensajes anteriores al que motivó la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, igual que en la app. El mensaje de la tarea está marcado como «Esta tarea» y se muestra en pantalla. **Mostrar mensajes anteriores** añade los mensajes más antiguos. Los demás mensajes del hilo de un correo aparecen plegados encima y debajo.

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, lo abre en la app de Gmail si la tienes instalada.

**Detalles** de un correo solo muestra la información que no aparece en su encabezado, como las direcciones completas en Cc, Cco o una dirección de respuesta distinta. Si no hay nada que añadir, no se muestra.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** al final.

**Detalles** muestra el nombre, el proyecto y el área de la tarea (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. Toca el título para abrir el chat. Las tareas terminadas aparecen de forma resumida. El mensaje del que proceden está en **Detalles**.

Una tarea «Esperando a» incluye un enlace a tu último mensaje para esa persona, el que estás esperando que responda: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un teléfono o `N`) crea una tarea para lo que necesites. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, se coloca donde corresponda según quién y qué le concierne. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo viernes», «3 nov», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario incluye sugerencias rápidas y **Elegir fecha**.
- **Se repite**: vuelve a aparecer con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula a las personas o empresas relacionadas, hasta 5.
- Icono de mensaje: adjunta el mensaje correspondiente, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram u otro mensaje que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En un teléfono, toca la cámara que aparece al lado para hacer una foto. Puedes adjuntar hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Toca × para quitar un archivo.

Los archivos se quedan en la tarea y The Machine los lee cuando trabaja en ella. También puedes adjuntar solo archivos: The Machine crea la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas a tamaño completo.
