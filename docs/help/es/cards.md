---
title: Tareas
area: cards
summary: Una tarea por cada asunto que necesite tu atención, lista para que des el visto bueno. Esto es lo que significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: baa6b797e040a271
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo requiere tu atención. Una tarea por asunto, por muchos mensajes que abarque.

## Dónde están las tareas

La página **Tareas** las agrupa así:

- **Recién hecho**: arriba, aparece el último paso que confirmaste, como un formulario o una incidencia que se completó mientras no estabas. Se queda ahí hasta que toques **Entendido**, como máximo un día, y también recibirás un aviso en el móvil.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (el trabajo está hecho y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero necesita que tomes una decisión o respondas), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe que no requiere tomar ninguna decisión).
- **Esperando a otros**: las tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: las tareas pospuestas y las que no recibieron respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, empezando por las más recientes, con la hora a la que se completaron, como «Hecha hace 5 minutos». Las tareas que parecen estar terminadas ya se marcan como **Parece hecho**.

Después de enviar algo, aparece una nota breve que indica adónde fue la tarea, como «Enviado. Movida a Hecho» o «Enviado. Movida a Más tarde hasta el lun.». **Abrir** te lleva a ella. La búsqueda encuentra tareas por su título o por la persona a quien se enviaron, también en Más tarde y Hecho.

En **Para ti** aparecen primero las tareas vencidas o que vencen mañana, después las preguntas de tu Fleet, luego los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, aparecen primero las más recientes. Una tarea mantiene su lugar mientras tu Machine la prepara y cuando está hecha: solo cambia su marca. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana y después el resto, empezando por las más recientes. La barra lateral mantiene el mismo orden.

**Parece hecho** significa que tu Machine ve que ya está terminado, como «PR #3451 fusionada», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Al cabo de un día, se cierra sola y aparece **Deshacer**. Una tarea que ya hayas resuelto por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierra sola.

Si un mensaje viene de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La muestra con su propia dirección, nunca con el nombre que usó. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo escribió.

Si una tarea sigue pendiente de otra persona, por ejemplo, porque tiene que revisar o responder algo, indica **Esperando a** y el paso pendiente. Se queda plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que hagas una pregunta: la tarea vuelve la mañana anterior al plazo, el mismo día del plazo si es más tarde, o la mañana siguiente una vez vencido el plazo. También indica a quién sigue esperando.

Cuando una tarea depende de un resultado que debe entregar otra persona, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no cierra la tarea: se queda en **Esperando a otros** hasta que un mensaje indique que ya está, y entonces se cierra sola. Aparece **Deshacer**. Si no llega nada para cuando toque hacer el seguimiento, la tarea vuelve con **Escribe un recordatorio breve** en su chat. Cuéntale en el chat qué se considera terminado para cambiarlo.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra. Aparece **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, envías un mensaje en el chat, la editas, la pospones o llega un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que lleva tiempo sin actividad y no tiene tareas abiertas puede generar una tarea con un siguiente paso concreto, como máximo tres por semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine se echa una siesta y deja la lista vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, lo indica en su mensaje y aparece **Revisar ahora** debajo.

Los filtros **Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, muestran todas las tareas o solo las de un tipo. El móvil y el ordenador muestran la misma selección. Si tienes activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Las alertas sobre tu Machine, como que un componente se reinicia continuamente, no son de Trabajo ni de Personal y solo aparecen en Todo.

La línea de la parte superior de la lista también te permite cambiar directamente al otro filtro: si tienes activado **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el último resumen de la mañana o de la tarde y lo que incluye, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leerlo y usa **Copiar** para pegarlo donde quieras. Cuando lo abras o toques su **×**, estará disponible en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo del filtro seleccionado.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [las tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También cambia el contenido al que puede acceder y desde el que puede enviar mensajes. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita estar en tu otra área para continuar y todos los mensajes de los que procede están allí, se mueve por sí sola y sigue adelante. De lo contrario, aparece **Mover a Trabajo** y no se mueve hasta que lo toques. Si añades una tarea sin elegir Trabajo o Personal, se mueve sola cuando encuentra el área que le corresponde. Hasta entonces, no aparece en Trabajo ni en Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. El correo de otras empresas tuyas va a las tareas de esa empresa. Una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente que te escribe por WhatsApp o un pedido en tu buzón personal, es Trabajo desde el principio. Una tarea que hayas movido o ubicado tú se queda donde la pusiste. Trabajo o Personal determina dónde aparece la tarea y con quién se comparte, nunca desde dónde responde: la respuesta siempre se envía a donde está la conversación, incluso después de moverla, salvo que elijas otra opción.

Aunque sea Personal, una tarea de este tipo responde desde la dirección de trabajo a la que llegó el correo y nunca aparece en una Fleet de Trabajo ni en el Graph del equipo.

Si hay dos o más tareas pendientes, **Repasar** en el encabezado de Para ti te permite revisarlas de una en una, en el orden de la lista y con cada borrador completo. Puedes usar **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el proceso. Debajo del título, el encabezado también indica cuánto tardarás a tu ritmo, por ejemplo, «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en el plazo de una hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan. Los mensajes nuevos se siguen leyendo y guardando, y se comprueban juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «Pausadas por la noche. Se pondrán al día a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en el chat o tocas una tarea, las comprobaciones siguen como siempre hasta que lleves una hora sin usarla. **Revisar ahora** siempre comprueba todo en el momento.

**Revisar ahora** lee todas las fuentes en el momento. Si no tienes tareas abiertas, toca la línea de tu Machine para verla, junto con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, aparece arriba en el ordenador. Solo se muestra una línea breve mientras se realiza una comprobación o si alguna falla o se retrasa. También puedes preguntarle en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que encontró en todas las fuentes que leyó, como «13 mensajes comprobados a las 16:11 · nada requiere tu atención» o «· 2 tareas nuevas». Si una tarea nueva queda pendiente hasta un momento más oportuno, como el resumen de la mañana, indica hasta cuándo: «1 tarea pendiente hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién escribió, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta ninguna, como «Solo estás en copia, un compañero está respondiendo» o «La reunión ya está programada para el jueves». Si la comprobación solo dio un motivo impreciso, el hilo no muestra ningún motivo. Toca uno para leerlo.

Se muestran los 10 primeros. Toca debajo para ver el resto. El número que aparece después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Una notificación del móvil sobre un mensaje que ya aparece en la lista solo se muestra una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para tener contexto y registrar promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso sobre una solución, nunca se leen ni aparecen en la lista. El correo sobre facturación, tu periodo de prueba o una invitación se lee como siempre.

## Los botones

Una tarea muestra su siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** te permite indicar qué cambiar: cómo hacer la tarea o, cuando ya hay un borrador, qué cambiar en él. **Marcar como hecha** indica que ya está resuelta: aparece a la vista en una tarea preparada sin borrador; en los demás casos, está en la parte superior de **…**, también en las tareas que requieren que tomes una decisión. La tarea sale de la lista enseguida y aparece **Deshacer** en el mensaje. Desliza el mensaje para quitarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se guarda.

Si quieres que se haga de otra manera, díselo en su **Chat**.

En **…**:

- **Pasar…**: asígnala a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: la tarea [vuelve con cierta frecuencia](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, indica por qué: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarle el nombre. El título que pongas se mantiene.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve a aparecer por sí sola cuando ocurre algo nuevo, como recibir otro mensaje de esa persona, pero no cuando respondes tú.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluya. Las facturas con pago automático, como una domiciliación o una tarjeta guardada, no se convierten en tareas. Si un correo posterior indica que ya se ha pagado, por ejemplo, porque el remitente confirma que recibió el pago, la tarea se cierra sola. **Deshacer** la recupera durante un día.

Una tarea que solo era pertinente hasta una hora determinada, como una confirmación antes de una reunión, se cierra sola después de esa hora. Pasa a **Hecho / descartado** con el estado «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de que un mensaje o un traspaso para alguien aparezca como listo, tu Machine comprueba tus chats recientes con las personas incluidas, también los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior muestra que ya está resuelto, por ejemplo, porque ya se lo pidieron y dijo que sí, la tarea se cierra sola. **Deshacer** la recupera durante un día.

Si un mensaje más reciente cambia el plan, por ejemplo, porque la fiesta se ha trasladado a otro sitio o se ha cancelado una reserva, The Machine actualiza sus tareas por su cuenta. Las tareas que aún hagan falta se adaptan al nuevo plan. Las que ya no requieran ninguna acción pasan a **Hecho / descartado** con el estado «No hace falta». Su chat indica «Actualizado:» y el motivo. **Deshacer** las recupera durante un día.

En tus primeras tareas, aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece definitivamente cuando usas el botón o pulsas ×.

El primer día, en la parte superior de Tareas, te damos la bienvenida y te indicamos quién lleva más tiempo esperando tu respuesta. Ese borrador se prepara primero para que esté listo cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización si corresponde (no solo porque esa persona trabaje allí), el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno, o sus iniciales si no. Si un logotipo no se ve bien en pequeño, por ejemplo, por ser blanco sobre un fondo transparente o por ser un logotipo horizontal con el nombre completo, también se muestran las iniciales.

A veces aparece una línea discreta con información que se desconoce, como «Último contacto hace 12 días por correo; no ha habido nada desde entonces». Aparece cuando el último contacto con esa persona es antiguo o no ha tenido respuesta. También indica los canales que no están conectados, como WhatsApp. Tu Machine te dice lo que no sabe en vez de hacer suposiciones.

Si se menciona un canal que no está conectado, pulsa **Conectar** junto a él para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Las tareas hechas conservan su título, con una nota debajo que explica cómo terminaron, como «Hecha: Sam la firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede, junto con el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del destino para que veas enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que alguien dijo en otro lugar, como la sugerencia de un compañero en Slack, aparece una línea que lo indica, como «Según Sam en #ops». Tócala para leer ese mensaje.

Los chats (Slack, WhatsApp, Telegram, Intercom…) aparecen como una sola conversación, en orden cronológico: primero los mensajes anteriores al que trata la tarea y después las respuestas. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje de la tarea lleva la marca «Esta tarea» y se abre directamente. **Mostrar mensajes anteriores** añade los mensajes más antiguos. En un correo, el resto del hilo aparece plegado encima y debajo.

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, se abre en la app de Gmail si la tienes.

En **Detalles** de un correo solo aparece la información que no está en el encabezado, como las direcciones completas de Cc, Bcc o una dirección de respuesta distinta. Si no hay nada más que añadir, no aparece nada.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** abajo.

**Detalles** muestra el nombre, el proyecto y el área de la tarea (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. Al tocar el título se abre el chat. Las tareas hechas se muestran de forma resumida; el mensaje del que proceden aparece en **Detalles**.

Una tarea con el estado «Esperando a» enlaza con tu último mensaje a esa persona, el que estás esperando: «Correo a Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un móvil o `N`) añade una tarea sobre cualquier asunto. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, la tarea va al área que le corresponde según la persona y el asunto. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas», también en tu propio idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve con cierta frecuencia. Consulta [Tareas periódicas](recurring.md).
- **Persona**: vincula a las personas o empresas relacionadas, hasta un máximo de 5.
- Icono de mensaje: adjunta el mensaje relacionado, como un correo, mensaje de Slack, Teams, WhatsApp, Telegram u otro mensaje que tenga The Machine. Busca por texto o por remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En el móvil, la cámara que aparece al lado sirve para hacer una foto. Puedes añadir hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Toca × para quitar uno.

Los archivos se guardan con la tarea y The Machine los lee cuando trabaja en ella. No hace falta añadir nada más: puede completar la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas a tamaño completo.
