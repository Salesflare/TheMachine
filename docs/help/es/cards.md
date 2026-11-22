---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fef065570d3fd972
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo necesita tu atención. Una tarea por asunto, aunque ocupe varios mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba del todo, muestra un último paso que confirmaste, como enviar un formulario o resolver un problema, que se completó mientras no estabas. Se queda ahí hasta que pulses **Entendido**, como máximo un día, y también recibirás una notificación en el móvil.
- **Para ti**: todo lo que está pendiente de ti, por orden de urgencia. Cada tarea indica **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (antes necesita que decidas o respondas; si el trabajo se ha detenido por algo que solo tienes tú, como un dato, un inicio de sesión o una elección, una línea bajo el título te lo indica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas que no tienen novedades desde hace una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, empezando por la más reciente, y cuándo se terminaron, por ejemplo, «Hecha hace 5 minutos». Las tareas que parecen estar terminadas se marcan como **Parece hecha**.

Después de enviar algo, aparece una nota breve que indica adónde ha ido la tarea, por ejemplo, «Enviado. Se ha movido a Hecho» o «Enviado. Se ha movido a Más tarde hasta el lunes». Si la respuesta solo promete que se hará el trabajo, como «Lo enviaré antes del martes», la tarea sigue abierta: «Enviado. Se ha mantenido abierta». **Abrir** te lleva a la tarea. La búsqueda encuentra tareas por título o por destinatario, también en Más tarde y Hecho.

**Para ti** muestra primero lo que ya ha vencido o vence mañana como máximo, luego las preguntas de tu Fleet, después los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, lo más reciente aparece primero. La tarea mantiene su posición mientras tu Machine la prepara y cuando se termina: solo cambia su indicador. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana como máximo, y luego las más recientes. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está terminada, como «PR #3451 combinado», pero todavía no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si el mensaje indica que ya está terminada, se cierra automáticamente al cabo de un día y aparece **Deshacer**. Si no, espera a que pulses **Marcar como hecha**. Una tarea que ya hayas resuelto por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierra automáticamente.

Si un mensaje llega de una dirección que se parece a la de alguien que conoces, como sam@acme-corp.example en vez de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». Muestra a la persona con su propia dirección, nunca con el nombre que ha usado. Tu Machine lo comprueba con la persona de la dirección que ya tienes, nunca con quien escribió el mensaje.

Si una tarea sigue pendiente de otra persona, por ejemplo, una revisión o una respuesta, indica ese paso con **Esperando a:**. Aparece plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que hayas respondido con una pregunta: la tarea vuelve a aparecer la mañana anterior a la fecha límite, en la fecha límite si es más tarde hoy o a la mañana siguiente si ya ha pasado. También indica de quién sigue esperando una respuesta.

Si una tarea depende de un resultado que entrega otra persona, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no cierra la tarea: se queda en **Esperando a otros** hasta que un mensaje indique que ya está el resultado. Entonces se cierra automáticamente y aparece **Deshacer**. Si no llega nada cuando toque insistir, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Para cambiar qué cuenta como terminado, indícalo en el chat.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que lo reciente aparezca primero cuando vuelvas después de unos días. Se considera que no hay novedades si no hay mensajes nuevos sobre la tarea ni has hecho nada en ella, como enviar un mensaje por el chat, editarla o posponerla. Abrirla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca como innecesarias todas las tareas de Más antiguos tras una sola confirmación, igual que **No hace falta** lo hace de una en una, con **Deshacer**. Si una tarea recibe novedades, vuelve a Para ti.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y aparece **Deshacer**. **Mantener** la conserva y no vuelve a preguntarlo. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Abrirla, enviar un mensaje por el chat, editarla, posponerla o recibir un mensaje nuevo hace que vuelva a aparecer.

Una vez a la semana, un proyecto que se haya quedado parado y no tenga nada abierto puede generar una tarea con un siguiente paso concreto, como máximo tres veces por semana. Consulta [Proyectos](projects.md).

Cuando nada necesita tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación ha fallado o va con retraso, lo verás en la línea, junto a **Revisar ahora**.

Los filtros **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo un tipo. El móvil y el ordenador mantienen la misma selección. Si tienes activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como una pieza que se reinicia continuamente, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente al otro filtro: en **Solo personal**, pulsa **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el último resumen de la mañana o de la tarde y lo que incluía, por ejemplo, **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Púlsala para volver a leerlo y usa **Copiar** para pegarlo donde quieras. Cuando lo abras o pulses su **×**, aparecerá en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo del filtro que tengas seleccionado.

Las tareas de un proyecto muestran su nombre debajo del título. Púlsalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiar el proyecto o quitarlo. Consulta [Tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. Con ella también cambia a qué mensajes puede acceder y desde cuáles puede enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita pasar a tu otra área para continuar y todos los mensajes relacionados ya están allí, se mueve y sigue adelante automáticamente. De lo contrario, aparece **Mover a Trabajo** y no se mueve hasta que lo pulses. Una tarea que hayas añadido sin elegir Trabajo o Personal se mueve automáticamente cuando encuentra dónde corresponde. Hasta entonces, no se asigna a Trabajo ni a Personal y sigue siendo privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, lo pregunta con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. El correo de otras empresas tuyas se asigna a las tareas de esa empresa. Una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, se considera Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente que te escribe por WhatsApp o un pedido en tu buzón personal, se considera Trabajo desde el principio. Una tarea que hayas movido o asignado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece la tarea y con quién se comparte, pero no desde dónde responde: la respuesta siempre se envía al lugar donde está la conversación, incluso después de mover la tarea, salvo que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de trabajo ni en el Graph del equipo.

Si hay dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, permite ir pasando por ellas de una en una, en el orden de la lista. Muestra cada borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el proceso. El encabezado indica cuánto tardarás a tu ritmo, por ejemplo, «unos 2 min».

Al final, cuenta cuántas tareas se han enviado o cerrado y cuántas se siguen preparando.

Las tareas que te hacen una pregunta no se incluyen en ninguno de los dos grupos: necesitan tu respuesta, no que pulses un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes recibidos cuando hay 40 pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, como máximo en una hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan. Los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30 para que las tareas estén listas antes del resumen de la mañana. En Conexiones, las comprobaciones muestran «Pausadas por la noche. Se pondrán al día a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en el chat o pulsas una tarea, las comprobaciones se reanudan como de costumbre hasta que lleves una hora sin actividad. **Revisar ahora** comprueba todo de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no hay tareas abiertas, pulsa la línea de tu Machine para verla junto con **Detalles**, que abre Comprobaciones en Conexiones. Si hay tareas abiertas, la opción aparece arriba del todo en el ordenador. Solo aparece una línea breve mientras se ejecuta una comprobación, o si ha fallado o va con retraso. También puedes preguntarlo por el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que ha encontrado en todas las fuentes que ha leído, por ejemplo, «13 mensajes revisados a las 16:11 · nada necesita tu atención» o «· 2 tareas nuevas». Si una tarea nueva espera un momento más adecuado, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Pulsa la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién escribió, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta ninguna, como «Solo estás en copia, responde otra persona del equipo» o «La reunión ya está programada para el jueves». Si la comprobación solo da un motivo impreciso, el hilo no muestra ninguno. Púlsalo para leerlo.

Se muestran los 10 primeros. Pulsa debajo para ver el resto. Un número después del nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Una notificación del móvil sobre un mensaje que ya aparece en la lista solo se muestra una vez. La línea permanece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para tener contexto y detectar promesas, pero no cuentan como correo nuevo. Los correos de tu Machine, como el resumen de la mañana o un aviso de reparación, nunca se leen ni se muestran en la lista. El correo sobre facturación, tu periodo de prueba o una invitación se lee como de costumbre.

## Los botones

Una tarea muestra su siguiente paso, como **Hazlo** o **Revisar y enviar**, y la opción **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** permite indicar qué hay que cambiar: cómo hacerlo o, si ya hay un borrador, qué cambiar en él. **Marcar como hecha** indica que ya está resuelta. Aparece directamente en una tarea lista que no tenga borrador; en los demás casos está en la parte superior de **…**, incluso si la tarea necesita que tomes una decisión. La tarea desaparece de la lista de inmediato y aparece **Deshacer** en el mensaje. Desliza el mensaje o arrástralo fuera con el ratón para cerrarlo antes. El cambio se mantiene.

Para que se haga de otra manera, indícalo en el **Chat** de la tarea. La respuesta solo menciona lo que ha cambiado, por ejemplo, que se ha pospuesto y hasta cuándo. Si no ha podido cambiar algo, como la fecha límite, te lo indica.

En **…**:

- **Pasar…**: asígnasela a alguien del equipo, a [Claude Code o Codex](hand-to-agent.md) o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: la tarea [vuelve a aparecer con cierta frecuencia](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, indica el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Pulsa el título o **Nombre**, en **Detalles**, para cambiarlo. También puedes pedirlo en el chat, por ejemplo, «Cámbiale el nombre a…». El título que pongas se mantiene.

**Reabrir** devuelve a la lista una tarea cerrada. También vuelve a aparecer automáticamente cuando ocurre algo nuevo, como recibir un mensaje de esa persona, pero no cuando respondes tú. La tarea indica entonces cuándo volvió a aparecer y se ordena como nueva. El chat continúa donde se quedó, incluso después de varias semanas.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluye. Las facturas que se pagan automáticamente, como las domiciliadas o las cargadas a una tarjeta guardada, no se convierten en tareas. Si un correo posterior confirma el pago, por ejemplo, porque el remitente confirma que lo ha recibido, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Una tarea que solo era necesaria hasta una hora concreta, como una confirmación antes de una reunión, se cierra automáticamente al llegar esa hora. Pasa a **Hecho / descartado** como «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de marcar como listo un mensaje o traspaso para otra persona, tu Machine comprueba tus chats recientes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo habían pedido y ha dicho que sí, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Si otra persona escribe en la misma conversación después de que se haya creado el borrador, **Enviar** lo bloquea: «No enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje junto con **Leerla** y **Rehacer para este mensaje**. Vuelve a pulsar **Enviar** para enviar el borrador tal como está.

Si un mensaje más reciente cambia el plan, por ejemplo, porque una fiesta se traslada a otro sitio o se cancela una reserva, The Machine actualiza sus tareas automáticamente. Las tareas que sigan siendo necesarias se adaptan al nuevo plan. Las que ya no tengan nada pendiente pasan a **Hecho / descartado** como «No hace falta». En el chat aparece «Actualizado:» con el motivo, y **Deshacer** las recupera durante un día.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas el botón o pulsas ×.

Durante tu primer día, la parte superior de Tareas te da la bienvenida y te indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización si corresponde (no solo porque esa persona trabaje allí), el proyecto, si es de Trabajo o Personal y cuándo llegó. Pulsa un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno, y sus iniciales si no. Si un logotipo no se distingue a ese tamaño, por ejemplo, porque es blanco sobre fondo transparente o es un logotipo apaisado con el nombre completo, también se muestran las iniciales.

A veces, una línea discreta indica qué información falta, como «Último contacto hace 12 días por correo; no hay nada desde entonces». Aparece cuando el último contacto con esa persona es antiguo o sigue sin respuesta, y menciona los canales que no están conectados, como WhatsApp. Tu Machine te dice lo que no sabe en vez de hacer conjeturas.

Si menciona un canal que no está conectado, pulsa Conectar a su lado para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Una tarea terminada conserva su título y muestra debajo cómo terminó, por ejemplo, «Hecha: Sam lo firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede y muestra el logotipo del servicio. Púlsala para leer el hilo. El borrador muestra el logotipo del lugar al que se enviará para que veas de inmediato si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que alguien ha dicho en otro lugar, como una sugerencia de un compañero en Slack, una línea lo indica, por ejemplo, «Basado en un mensaje de Sam en #ops». Púlsala para leer el mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) aparece como una sola conversación, de los mensajes más antiguos a los más recientes: incluye los mensajes anteriores a la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje de la tarea lleva la marca «Esta tarea» y se abre en la vista. **Mostrar mensajes anteriores** añade mensajes más antiguos. En un correo, el resto del hilo aparece plegado encima y debajo del mensaje.

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, lo abre en la app de Gmail si la tienes instalada.

Los **Detalles** de un correo solo muestran la información que no aparece en el encabezado, como las direcciones completas en Cc, Cco o una dirección de respuesta distinta. Si no hay nada que añadir, no se muestra nada.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de empezar el hilo. El enlace de la tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre de la tarea, el proyecto, el área (pulsa uno para cambiarlo), tu última nota y el resultado de un agente de programación. Al pulsar el título, se abre el chat. Las tareas terminadas ocupan poco espacio; el mensaje de origen aparece en **Detalles**.

Una tarea «Esperando a» enlaza el último mensaje que enviaste a esa persona, el que estás esperando: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, con **+** en un móvil o con `N`) crea una tarea para cualquier cosa. Al crearla no se envía nada. Si no has elegido **Trabajo** ni **Personal**, se asigna al área que corresponde según quién y qué asunto trate. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas», también en tu idioma. El icono del calendario incluye opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve a aparecer con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula a las personas o empresas relacionadas, hasta 5.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: pulsa el clip, pega una captura de pantalla o arrastra archivos al formulario. En un móvil, la cámara que aparece al lado permite hacer una foto. Puedes adjuntar hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Pulsa × para quitar uno.

Los archivos se quedan en la tarea y The Machine los lee mientras trabaja en ella. También puedes crear una tarea solo con archivos: rellena la información a partir de un PDF o un archivo de texto. Las fotos se muestran como imágenes pequeñas; púlsalas para verlas a tamaño completo.
