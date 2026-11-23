---
title: Tareas
area: cards
summary: Una tarea por cada asunto que necesite tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 88ccf5426e5a538f
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo necesita tu atención. Una tarea por asunto, aunque abarque muchos mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba, aparece el último paso que confirmaste, como un formulario o un problema, que se completó mientras no estabas. Se queda ahí hasta que pulses **Entendido**, durante un día como máximo. También recibirás una notificación en el móvil.
- **Para ti**: todo lo que tienes pendiente, empezando por lo más urgente. Cada tarea indica **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero necesita que tomes una decisión o respondas; si el trabajo se ha detenido porque falta algo que solo tienes tú, como un dato, iniciar sesión o elegir, aparece una línea bajo el título que lo explica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe que no requiere decidir nada).
- **Más antiguos**: tareas plegadas que no han tenido novedades durante una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso le corresponde a otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con la hora a la que se completaron, como «Hecha hace 5 minutos». Las tareas que parecen terminadas llevan la marca **Parece hecha**.

Después de enviar algo, una nota breve indica adónde ha ido la tarea, como «Enviado. Se ha movido a Hecho» o «Enviado. Se ha movido a Más tarde hasta el lunes». Si una respuesta solo promete hacer el trabajo, como «Lo enviaré el martes», la tarea sigue abierta: «Enviado. Se ha mantenido abierta». **Abrir** te lleva a la tarea. Puedes buscar una tarea por su título o por la persona a quien se envió, también en Más tarde y Hecho.

En **Para ti** aparecen primero las tareas vencidas o que vencen mañana como muy tarde, después las preguntas de tu Fleet, luego los seguimientos de los tableros y, por último, el resto. Dentro de cada grupo, se ordenan de más reciente a más antigua. La tarea conserva su lugar mientras tu Machine la prepara y cuando está hecha: solo cambia su marca. En los demás grupos abiertos, primero aparecen las vencidas o las que vencen mañana como muy tarde, y después el resto de más reciente a más antigua. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está terminada, como «PR #3451 se ha fusionado», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como retrasadas. Si aparece en un mensaje, se cierra sola al cabo de un día y puedes pulsar **Deshacer**. Si no, espera a que pulses **Marcar como hecha**. Una tarea que ya hayas resuelto por tu cuenta, por ejemplo respondiendo en Gmail o Slack, también se cierra sola.

Si un mensaje viene de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en vez de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que haya usado. Tu Machine comprueba estos mensajes con la persona de la dirección que ya tienes, nunca con quien los ha escrito.

Una tarea que aún depende de otra persona, como una revisión o una respuesta, indica **Esperando a**: el paso pendiente. Se queda plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que respondas a una pregunta: vuelve la mañana anterior a la fecha límite, en la fecha límite si es más tarde ese mismo día o a la mañana siguiente cuando ya haya vencido. La tarea indica a quién sigue esperando.

Si una tarea consiste en esperar un resultado que debe entregar otra persona, como un contrato firmado, en **Detalles** aparece **Hecho cuando**. Enviar tu parte no la cierra: espera en **Esperando a otros** hasta que un mensaje muestre el resultado y entonces se cierra sola. Puedes pulsar **Deshacer**. Si no llega nada cuando toca hacer el seguimiento, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como tarea terminada para cambiarlo.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que las tareas nuevas aparezcan primero después de unos días sin entrar. No hay novedades cuando no llega ningún mensaje nuevo ni haces nada en la tarea, como enviar un mensaje en el chat, editarla o posponerla. Solo mirarla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca todas las tareas de Más antiguos como No hace falta después de que lo confirmes. **No hace falta** permite hacerlo de una en una y **Deshacer** lo revierte. Si hay novedades, la tarea vuelve a Para ti.

Si nadie toca una tarea durante una semana, aparece una vez la pregunta **¿Aún hace falta?**. **No hace falta** la cierra; puedes pulsar **Deshacer**. **Mantener** la conserva y no vuelve a preguntarte. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, envías un mensaje en el chat, la editas, la pospones o recibes un mensaje nuevo, vuelve a aparecer.

Una vez a la semana, un proyecto que se haya quedado parado y no tenga nada abierto puede recibir una tarea con un siguiente paso concreto. Como máximo, tres a la semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine descansa y muestra una lista vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, aparece una línea que lo explica, con **Revisar ahora** debajo.

Las opciones **Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, muestran todas las tareas o solo las de un tipo. El móvil y el ordenador muestran la misma selección. Si está activado Trabajo o Personal, **Mostrar todo** vuelve a la lista completa. Una alerta sobre tu Machine, como que un componente se reinicie constantemente, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente a la otra vista: en **Solo personal**, pulsa **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el último resumen de la mañana o de la tarde y lo que cuenta, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Pulsa la fila para volver a leer ese resumen y **Copiar** para pegarlo donde quieras. Cuando lo abras o pulses la **×**, aparecerá en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto en Trabajo como en Personal, o solo en el área que hayas seleccionado.

Una tarea de un proyecto muestra el nombre del proyecto bajo el título. Púlsalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a la otra área. También se mueve el contenido que puede leer y desde el que puede enviar mensajes. **Deshacer**, en la nota, la devuelve a su sitio.

Si una tarea necesita pasar a la otra área y todos los mensajes de los que procede están allí, se mueve sola y continúa. Si no, aparece **Mover a Trabajo** y no se mueve nada hasta que lo pulses. Una tarea que añadas sin elegir Trabajo o Personal se mueve sola cuando encuentra el área que le corresponde. Hasta entonces, no pertenece a Trabajo ni a Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de la otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. El correo de otras empresas tuyas va a las tareas de esa empresa. Una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp o un pedido en tu buzón personal, es Trabajo desde el principio. Una tarea que hayas movido o clasificado tú se queda donde la pongas. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, nunca dónde responde: la respuesta siempre se envía donde está la conversación, también después de moverla, a menos que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de trabajo ni en el Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, las recorre de una en una y en el orden de la lista. Muestra el borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el proceso. El encabezado indica cuánto tardarás a tu ritmo, por ejemplo, «unos 2 min».

Al terminar, cuenta lo que se ha enviado o cerrado y lo que aún se está preparando.

Las tareas que te hacen una pregunta no se incluyen en ninguno de los dos grupos: necesitan una respuesta, no que pulses un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, dentro de una hora.

Por la noche, de 00:00 a 06:30, se pausan las comprobaciones. Los mensajes nuevos se siguen leyendo y guardando, y se comprueban juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «Pausadas durante la noche; se reanudan a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en el chat o pulsas una tarea, las comprobaciones se ejecutan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba todo de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no tienes tareas abiertas, pulsa la línea de tu Machine para ver sus **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, la opción aparece arriba en el ordenador. Una línea breve solo aparece mientras se ejecuta una comprobación o si alguna ha fallado o se ha retrasado. También puedes preguntarlo en el chat.

LinkedIn, X y Salesflare siguen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que ha encontrado en todas las fuentes que ha leído, como «Se han comprobado 13 mensajes a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». La línea solo corresponde a esa comprobación: las tareas que ya estaban en tu lista no cambian. Si una tarea nueva espera a un momento más oportuno, como el resumen de la mañana, se indica hasta cuándo: «1 tarea en espera hasta mañana a las 08:30».

Pulsa la línea para ver cada hilo de correo, chat y notificación con el icono de su fuente, quién lo ha escrito, el asunto o las primeras palabras y la tarea nueva o el motivo por el que no hacía falta ninguna, como «Solo estaba en copia; responde un compañero» o «La reunión ya está programada para el jueves». Si la comprobación solo dio un motivo impreciso, el hilo no muestra ninguno. Pulsa un elemento para leerlo.

Se muestran los 10 primeros. Pulsa debajo para ver el resto. El número junto a un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Las notificaciones del móvil sobre mensajes que ya aparecen en la lista solo se muestran una vez. La línea permanece visible durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de reparación, nunca se leen ni se muestran. El correo sobre la facturación, el periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra su siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué hay que cambiar: cómo hacerlo o, cuando ya hay un borrador, qué cambiar en él. **Marcar como hecha** indica que ya está resuelta. Aparece a la vista en las tareas preparadas sin borrador. En los demás casos, incluida una tarea que necesita que tomes una decisión, está en la parte superior de **…**. La tarea sale de la lista de inmediato y aparece **Deshacer** en el mensaje. Desliza el mensaje o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Para que se haga de otra manera, dilo en su **Chat**. La respuesta indica solo lo que ha cambiado, como una tarea pospuesta y hasta cuándo. Si no se ha podido cambiar algo, como la fecha límite, te lo dice.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve a aparecer con cierta frecuencia](recurring.md).
- **No hace falta**: desaparece. Si quieres, puedes elegir el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Pulsa el título o **Nombre**, en **Detalles**, para cambiarlo. También puedes pedirlo en el chat, por ejemplo: «Cámbiale el nombre a…». Se conserva el título que elijas.

**Reabrir** devuelve una tarea cerrada. También vuelve a aparecer por sí sola cuando ocurre algo nuevo, como recibir un mensaje de esa persona, pero no si respondes tú. Entonces indica cuándo ha vuelto y aparece como nueva en la lista. El chat continúa donde se quedó, incluso después de varias semanas.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluya. No ocurre con las facturas que se pagan automáticamente, como los recibos domiciliados o los cargos a una tarjeta guardada. Si un correo posterior indica que se ha pagado, por ejemplo, porque quien lo envió confirma que ha recibido el pago, la tarea se cierra sola. Puedes pulsar **Deshacer** durante un día.

Una tarea que solo sea relevante hasta una hora concreta, como una confirmación antes de una reunión, se cierra sola cuando pasa esa hora. Se mueve a **Hecho / descartado** con la indicación «Ya no hace falta». Puedes pulsar **Deshacer** durante un día.

Antes de que un mensaje o un traspaso para otra persona aparezca como listo, tu Machine comprueba tus chats recientes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo pidieron y aceptó, la tarea se cierra sola. Puedes pulsar **Deshacer** durante un día.

Si otra persona escribe en la misma conversación después de que se haya creado el borrador, **Enviar** lo detiene: «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje con **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** de nuevo para enviar el borrador tal cual.

Si un mensaje más reciente cambia el plan, por ejemplo, porque una fiesta se ha trasladado a otro sitio o se ha cancelado una reserva, The Machine actualiza las tareas. Si una tarea sigue siendo necesaria, se adapta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** con la indicación «No hace falta». En el chat aparece «Actualizada:» y el motivo. Puedes pulsar **Deshacer** durante un día.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece definitivamente cuando usas el botón correspondiente o pulsas ×.

El primer día, en la parte superior de Tareas te damos la bienvenida y te decimos quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización si corresponde (no solo porque esa persona trabaje allí), el proyecto, Trabajo o Personal y cuándo llegó. Pulsa un nombre para abrir su página en el Graph.

Los nombres y las organizaciones muestran su foto o logotipo si aparece en el Graph; si no, muestran sus iniciales. Si un logotipo no se distingue a ese tamaño, por ejemplo, porque es blanco sobre un fondo transparente o porque es un rótulo ancho, también se muestran las iniciales.

A veces aparece una línea discreta para indicar qué información falta, como «Último contacto hace 12 días por correo; no ha habido nada desde entonces». Se muestra cuando el último contacto es antiguo o no tiene respuesta, e indica los canales que no están conectados, como WhatsApp. Tu Machine explica lo que no sabe en vez de hacer suposiciones.

Si menciona un canal que no está conectado, pulsa Conectar, junto a ese canal, para abrir la conexión.

El título indica lo que hay que hacer y solo cambia cuando eso cambia. Una tarea hecha conserva el título y muestra debajo cómo terminó, como «Hecha: Sam la firmó el martes».

Encima del borrador, una línea tenue indica el mensaje del que procede, con el logotipo del servicio. Púlsala para leer el hilo. El borrador muestra el logotipo del destino para que veas de inmediato si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que ha dicho otra persona en otro sitio, como una sugerencia de un compañero en Slack, una línea lo indica, por ejemplo, «Basado en un mensaje de Sam en #ops». Púlsala para leer el mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) aparece como una sola conversación, de más antiguo a más reciente: los mensajes anteriores al que trata la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje de la tarea lleva la marca «Esta tarea» y se abre en la conversación. **Mostrar mensajes anteriores** añade los mensajes más antiguos. En un correo, el resto del hilo aparece plegado encima y debajo.

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, lo abre en la app de Gmail si la tienes.

En **Detalles** de un correo solo aparecen los datos que no están en el encabezado, como las direcciones completas de Cc, Cco o una dirección de respuesta distinta. Si no hay nada que añadir, no aparece nada.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** abajo.

**Detalles** muestra el nombre, el proyecto y el área de la tarea (pulsa cualquiera para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Las tareas hechas se muestran de forma resumida; el mensaje del que proceden aparece en **Detalles**.

Una tarea que indica «Esperando a» enlaza con tu último mensaje a esa persona, el que está pendiente de respuesta: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, con **+** en un móvil o con `N`) permite añadir una tarea para cualquier asunto. Al crearla no se envía nada. Si no eliges **Trabajo** o **Personal**, se asigna al área que le corresponde según quién y qué sean. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas», también en tu idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Se repite**: vuelve a aparecer con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: añade las personas o empresas relacionadas, hasta 5.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o por remitente. Cada resultado indica de dónde procede, quién lo ha enviado y cuándo.
- **Archivos**: pulsa el clip, pega una captura de pantalla o arrastra archivos al formulario. En un móvil, la cámara que aparece al lado hace una foto. Puedes añadir hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Pulsa × para quitar un archivo.

Los archivos se quedan con la tarea y The Machine los lee cuando trabaja en ella. También puedes adjuntar solo archivos: rellenará la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Púlsalas para verlas a tamaño completo.
