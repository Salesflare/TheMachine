---
title: Tareas
area: cards
summary: Una tarea por cada asunto que necesita tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 84b8879d98f26aa2
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo necesita tu atención. Una tarea por asunto, aunque abarque muchos mensajes.

## Dónde están las tareas

La página **Tareas** las agrupa así:

- **Recién hecho**: arriba, aparece el último paso que confirmaste, como un formulario o una incidencia, que se completó mientras no estabas. Se queda ahí hasta que toques **Entendido**, como máximo un día, y también recibirás un aviso en el móvil.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (el trabajo está hecho y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero necesita que tomes una decisión o respondas), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas que no han tenido novedades durante una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con la hora a la que terminaron, como «Hecha hace 5 minutos». Las tareas que parecen estar terminadas ya se marcan como **Parece hecha**.

Después de enviar, aparece una nota breve que indica dónde ha ido la tarea, como «Enviado. Movido a Hecho» o «Enviado. Movido a Más tarde hasta el lunes». Si la respuesta solo promete hacer el trabajo, como «Lo enviaré el martes», la tarea sigue abierta: «Enviado. Se mantiene abierta». **Abrir** te lleva a la tarea. La búsqueda encuentra tareas por título o por la persona a quien se enviaron, también en Más tarde y Hecho.

En **Para ti** aparecen primero las tareas vencidas o que vencen mañana como muy tarde, después las preguntas de tu Fleet, luego los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, primero aparecen las más recientes. Una tarea no cambia de sitio mientras tu Machine la prepara ni cuando se termina: solo cambia su marca. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana como muy tarde, y después el resto, de la más reciente a la más antigua. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está terminada, como «PR #3451 fusionada», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Al cabo de un día, se cierra sola y aparece **Deshacer**. También se cierra sola una tarea que ya hayas resuelto tú, por ejemplo, respondiendo en Gmail o Slack.

Si un mensaje procede de una dirección que solo parece ser de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo dice claramente: «Esta persona no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que ha usado. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo ha escrito.

Una tarea que sigue pendiente de otra persona, como una revisión o una respuesta, indica **Esperando a**: ese paso. Aparece plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la vuelva a mostrar. Lo mismo ocurre después de que hagas una pregunta: la tarea vuelve a aparecer la mañana anterior a la fecha límite, en la fecha límite si es más tarde hoy o a la mañana siguiente si ya ha pasado. También indica quién sigue pendiente de responder.

Si la tarea depende de un resultado que debe entregarte otra persona, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no cierra la tarea: se queda en **Esperando a otros** hasta que un mensaje indique que se ha conseguido el resultado. Entonces se cierra sola y aparece **Deshacer**. Si no recibes nada para cuando toque hacer seguimiento, la tarea vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como terminado para cambiarlo.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que las nuevas aparezcan primero después de unos días sin entrar. No hay novedades cuando no ha llegado ningún mensaje nuevo ni has hecho nada en la tarea, como enviar un mensaje de chat, editarla o posponerla. Solo mirarla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca todas las tareas de Más antiguos como innecesarias después de que lo confirmes una vez, igual que **No hace falta** las marca de una en una. Aparece **Deshacer**. Si una tarea recibe novedades, vuelve a Para ti.

Si nadie ha tocado una tarea durante una semana, se pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y aparece **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Abrirla, enviar un mensaje de chat, editarla, posponerla o recibir un mensaje nuevo hace que vuelva a aparecer.

Una vez a la semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede recibir una tarea con un siguiente paso concreto. Como máximo, tres por semana. Consulta [Proyectos](projects.md).

Cuando nada necesita tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba si hay novedades, se despierta y te lo indica. Si falla una comprobación o se retrasa, la línea lo indica y aparece **Revisar ahora** debajo.

**Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, muestran todas las tareas o solo las de un tipo. El móvil y el ordenador muestran la misma selección. Cuando está seleccionado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Un aviso sobre tu Machine, como que un componente no deja de reiniciarse, no es ni de Trabajo ni Personal, así que solo aparece en Todo.

La línea superior de la lista también permite cambiar directamente a la otra vista: en **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila superior de la lista muestra el último resumen de la mañana o de la tarde y lo que cuenta, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leerlo. Con **Copiar**, puedes pegarlo donde quieras. Después de abrirlo o tocar su **×**, aparece en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo del tipo que hayas seleccionado.

Las tareas de un proyecto muestran el nombre del proyecto bajo el título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También cambia lo que puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita pasar a tu otra área y todos los mensajes relacionados están allí, se mueve sola y sigue adelante. Si no, aparece **Mover a Trabajo** y no se mueve hasta que lo toques. Una tarea que hayas añadido sin elegir Trabajo ni Personal se mueve sola cuando encuentra el área que le corresponde. Hasta entonces, no aparece ni en Trabajo ni en Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. El correo de otra de tus empresas va a las tareas de esa empresa. Una tarea sobre tu vida personal, como un familiar que escribe a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp o un pedido en tu buzón personal, es Trabajo desde el principio. Una tarea que hayas movido o asignado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, pero no dónde responde: la respuesta siempre se envía en la conversación original, también después de moverla, a menos que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de trabajo ni en Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar** en el encabezado de Para ti te permite recorrerlas de una en una, en el orden de la lista. Muestra cada borrador completo con **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. Debajo del título, el encabezado también indica cuánto tardarás si vas a tu ritmo, como «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen en ninguno de los dos grupos: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o el mensaje más antiguo de una persona lleva esperando 15 minutos. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en el plazo de una hora.

Por la noche, entre las 00:00 y las 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30, para que tus tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «En pausa por la noche. Se pondrá al día a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en un chat o tocas una tarea, las comprobaciones se ejecutan con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre inicia una comprobación de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no tienes tareas abiertas, toca la línea de tu Machine para verla, con **Detalles**, que abre Comprobaciones en Conexiones. Si hay tareas abiertas, aparece arriba del todo en un ordenador. Solo se muestra una línea breve mientras se ejecuta una comprobación o cuando alguna ha fallado o se ha retrasado. También puedes pedirlo en un chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que ha encontrado en todas las fuentes que ha leído, como «13 mensajes comprobados a las 16:11 · nada necesita tu atención» o «· 2 tareas nuevas». Si una tarea nueva espera un momento más oportuno, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Toca la línea para ver cada conversación de correo, chat y notificación, con el icono de su fuente: quién escribió, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta ninguna, como «Solo estás en copia, responde un compañero» o «La reunión ya está fijada para el jueves». Si la comprobación solo dio un motivo impreciso, no se muestra ningún motivo para la conversación. Toca una para leerla.

Se muestran las 10 primeras. Toca debajo para ver el resto. El número que aparece después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Las notificaciones del móvil sobre mensajes que ya aparecen en la lista solo se muestran una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus respuestas se leen para tener en cuenta el contexto y las promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de reparación, nunca se leen ni aparecen en la lista. El correo sobre facturación, tu periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué cambiar: cómo hacerlo o, cuando ya hay un borrador, qué cambiar en él. **Marcar como hecho** indica que ya está resuelto: aparece directamente en una tarea preparada sin borrador o, en los demás casos, en la parte superior de **…**, también en las tareas que necesitan que tomes una decisión. La tarea desaparece de la lista de inmediato y aparece **Deshacer** en el mensaje. Desliza el mensaje para descartarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Para que se haga de otra forma, dilo en su **Chat**.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve a aparecer periódicamente](recurring.md).
- **No hace falta**: desaparece. Si quieres, elige el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarlo. También puedes pedirlo en el chat, por ejemplo: «Cámbiale el nombre a…». El título se conserva.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve a aparecer automáticamente cuando ocurre algo nuevo, como un mensaje nuevo de esa persona, pero no si respondes tú. En ese caso, indica cuándo ha vuelto y aparece como nueva en la lista. El chat continúa donde se quedó, aunque hayan pasado semanas.

Una factura que aún tengas que pagar tú, sea del país que sea, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que aparecen en la factura. Las facturas con pago automático, como un recibo domiciliado o una tarjeta registrada, no se convierten en tareas. Cuando un correo posterior indique que se ha pagado, por ejemplo, porque el remitente confirma que ha recibido el pago, la tarea se cierra sola. **Deshacer** la recupera durante un día.

Una tarea que solo sea necesaria hasta una hora concreta, como una confirmación antes de una reunión, se cierra sola después de esa hora. Pasa a **Hecho / descartado** con el estado «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de que un mensaje o un traspaso para otra persona aparezca como listo, tu Machine comprueba tus chats recientes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo han pedido y ha dicho que sí, la tarea se cierra sola. **Deshacer** la recupera durante un día.

Cuando un mensaje más reciente cambia el plan, como cuando una fiesta cambia de local o se cancela una reserva, The Machine actualiza sus tareas automáticamente. Si una tarea sigue siendo necesaria, se ajusta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** con el estado «No hace falta». En su chat aparece «Actualizada:» con el motivo y **Deshacer** la recupera durante un día.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**. También te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece definitivamente cuando usas su botón o pulsas ×.

El primer día, en la parte superior de Tareas, te saluda un mensaje que indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización cuando corresponde (no solo porque esa persona trabaje allí), el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si aparece en Graph; si no, muestran sus iniciales. Si un logotipo no se distingue bien en ese tamaño, como uno blanco sobre fondo transparente o un logotipo apaisado con el nombre, también se muestran las iniciales.

A veces aparece una línea discreta con información que se desconoce, como «Último contacto hace 12 días por correo; no ha habido más noticias». Aparece cuando el último contacto con esa persona es antiguo o no ha tenido respuesta. También indica los canales que no están conectados, como WhatsApp. Tu Machine dice lo que no sabe en vez de hacer suposiciones.

Si indica un canal que no está conectado, **Conectar**, junto a ese canal, abre la conexión.

El título indica qué hay que hacer y solo cambia si cambia la tarea. Una tarea terminada conserva el título y muestra debajo cómo terminó, como «Hecha: Sam la firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede y muestra el logotipo del servicio. Tócala para leer la conversación. El borrador muestra el logotipo del destino, para que veas al instante si es una respuesta en Slack o un correo.

Si el borrador se basa en lo que otra persona dijo en otro lugar, como una sugerencia de un compañero en Slack, aparece una línea que lo indica, como «Basado en un mensaje de Sam en #ops». Tócala para leer ese mensaje.

Los chats (Slack, WhatsApp, Telegram, Intercom…) aparecen como una sola conversación, en orden cronológico: primero los mensajes anteriores al que trata la tarea y después las respuestas. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje relacionado con la tarea se marca como «Esta tarea» y se abre en la conversación. **Mostrar mensajes anteriores** añade mensajes más antiguos. Los demás mensajes de una conversación de correo aparecen plegados encima y debajo del mensaje relacionado.

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, se abre en la app de Gmail si la tienes instalada.

En **Detalles** de un correo solo aparece la información que no figura en el encabezado, como las direcciones completas de Cc, Cco o una dirección de respuesta distinta. Si no hay nada más que añadir, no aparece ningún detalle.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** al final.

**Detalles** muestra el nombre, el proyecto y el área (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. Al tocar el título se abre el chat. Las tareas terminadas se muestran de forma resumida; el mensaje del que proceden está en **Detalles**.

Una tarea que está «Esperando a» alguien incluye un enlace a tu último mensaje para esa persona, el que está pendiente de respuesta: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, con **+** en un móvil o con `N`) crea una tarea para cualquier cosa. Crear una tarea no envía nada. Si no eliges **Trabajo** o **Personal**, se asigna al área que le corresponde según la persona y el asunto. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo viernes», «3 nov», «14:00» o «en 2 horas». También puedes hacerlo en tu propio idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve a aparecer periódicamente. Consulta [Tareas periódicas](recurring.md).
- **Persona**: vincula hasta 5 personas o empresas relacionadas con la tarea.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde viene, quién lo ha enviado y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En un móvil, puedes sacar una foto con la cámara que aparece al lado. Puedes añadir hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). × quita un archivo.

Los archivos se quedan con la tarea y The Machine los lee mientras trabaja en ella. No hace falta nada más: puede completar la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas a tamaño completo.
