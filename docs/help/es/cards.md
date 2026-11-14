---
title: Tareas
area: cards
summary: Una tarea por cada cosa que requiere tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo requiere tu atención. Una tarea por asunto, aunque abarque muchos mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Para ti**: todo lo que está esperando por ti, empezando por lo más urgente. Cada tarea indica **Preparada** (el trabajo está hecho y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero necesita que tomes una decisión o respondas) o **Preparando…** (tu Machine está trabajando en ello).
- **Recién hecho**: un último paso que confirmaste, como un formulario o una incidencia, se completó mientras no estabas. Se queda aquí hasta que pulses **Entendido**, como máximo un día, y también te llega al teléfono.
- **Vuelve más tarde**: las tareas pospuestas y las que no tienen respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con la hora a la que se completaron, como «Hecho hace 5 minutos». Las tareas que parecen terminadas ya llevan la marca **Parece hecho**.

Después de enviar algo, aparece una nota breve que indica adónde fue la tarea, como «Enviado. Movido a Hecho» o «Enviado. Movido a Más tarde hasta el lun.». **Abrir** te lleva a la tarea. La búsqueda encuentra tareas por su título o por la persona a quien se enviaron, también en Más tarde y Hecho.

**Para ti** muestra primero lo vencido o lo que vence mañana o antes, después las preguntas de tu Fleet y, por último, lo demás. Dentro de cada grupo, lo más reciente aparece primero. Una tarea conserva su lugar mientras tu Machine la prepara y cuando está hecha: solo cambia su marca. En los demás grupos abiertos, lo vencido o lo que vence mañana o antes aparece primero, y luego lo demás, de lo más reciente a lo más antiguo. La barra lateral mantiene el mismo orden.

**Parece hecho** significa que tu Machine ve que ya está terminado, como «PR #3451 integrado», pero aún no se ha cerrado. **Reabrir** lo devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Se cierran automáticamente al cabo de un día, con **Deshacer**. Una tarea que ya hayas resuelto por tu cuenta, por ejemplo al responder en Gmail o Slack, también se cierra automáticamente.

Cuando un mensaje viene de una dirección que solo parece ser de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que usó. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo escribió.

Una tarea que todavía espera a otra persona, por ejemplo una revisión o una respuesta, indica el paso pendiente en **Esperando a**. Se queda en **Esperando a otros**, contraído encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que hagas una pregunta: vuelve la mañana antes de la fecha límite, a la hora límite si es más tarde ese mismo día, o a la mañana siguiente si ya pasó. También indica a quién sigue esperando.

Si una tarea depende de un resultado que debe entregar otra persona, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje indique que el resultado llegó, y entonces se cierra automáticamente, con **Deshacer**. Si no llega nada cuando toca insistir, vuelve con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como terminado para cambiarlo.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra, con **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, pasa a Vuelve más tarde y deja de contar para el número del icono de la app y el resumen de la mañana. Abrirla, enviar un mensaje en el chat, editarla, posponerla o recibir un mensaje nuevo hace que vuelva.

Una vez por semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede generar una tarea con un siguiente paso concreto, hasta tres por semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba las novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, la línea lo indica y muestra **Revisar ahora** debajo.

Los filtros **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo las de un tipo. El teléfono y la computadora muestran la misma selección. Si tienes activado Trabajo o Personal, **Mostrar todo** vuelve a la lista completa. Una alerta sobre tu Machine, como una parte que se reinicia continuamente, no es de Trabajo ni de Personal y solo aparece en Todo.

La línea de la parte superior de la lista también cambia directamente al otro filtro: **Solo Personal · Trabajo · Mostrar todo**.

La fila de la parte superior de la lista muestra el último resumen de la mañana o de la tarde y lo que contabilizó, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leerlo, con **Copiar** para pegarlo donde quieras. Cuando lo abras o pulses su **×**, aparecerá en todos tus dispositivos hasta el próximo resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, para Trabajo y Personal, o solo para el filtro que tengas seleccionado.

Una tarea de un proyecto muestra el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [las tareas de un proyecto](projects.md#a-projects-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También cambia de área aquello que puede leer y enviar. **Deshacer** en la nota la devuelve a su área anterior.

Si una tarea necesita tu otra área para continuar y todos los mensajes de los que viene están allí, se mueve automáticamente y continúa. De lo contrario, aparece **Mover a Trabajo** y no se mueve hasta que lo pulses. Si añades una tarea sin elegir Trabajo ni Personal, se mueve automáticamente cuando encuentra el área que le corresponde. Hasta entonces, no pertenece a Trabajo ni a Personal y sigue siendo privada.

Una tarea siempre puede leer los mensajes de los que viene. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. El correo de otras empresas tuyas va a las tareas de esa empresa, y una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp o un pedido en tu buzón personal, es Trabajo desde el principio. Una tarea que hayas movido o asignado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, nunca adónde responde: la respuesta siempre se envía en la conversación original, también después de moverla, a menos que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de Trabajo ni en el Graph del equipo.

Si hay dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, las recorre de una en una, en el orden de la lista, y muestra cada borrador completo, con **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En una computadora, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. Debajo del título, el encabezado también indica cuánto tardarás si vas a tu ritmo, como «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen en ninguno de los dos grupos: necesitan tu respuesta, no que pulses un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, dentro de la hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Conexiones, las comprobaciones indican «Pausadas por la noche; se ponen al día a las 06:30». Si abres la app, escribes en el chat o tocas una tarea por la noche, las comprobaciones vuelven a funcionar con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba todo de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no tienes tareas abiertas, toca la línea de tu Machine para verla, junto con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, está en la parte superior de la pantalla de la computadora. Solo aparece una línea breve mientras se ejecuta una comprobación o si alguna ha fallado o se ha retrasado. También puedes preguntarlo en el chat.

LinkedIn, X y Salesflare mantienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas que indica lo que encontró en todas las fuentes que leyó, como «13 mensajes revisados a las 16:11 · nada requiere tu atención» o «· 2 tareas nuevas». Si una tarea nueva debe esperar a un momento mejor, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién escribió, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hizo falta crear una, como «Solo estás en copia; un compañero está respondiendo» o «La reunión ya está programada para el jueves». Si la comprobación solo dio un motivo impreciso, el hilo no muestra ningún motivo. Toca uno para leerlo.

Se muestran los primeros 10; toca debajo para ver el resto. Un número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Una notificación del teléfono sobre un mensaje que ya aparece en la lista solo se muestra una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta los correos que recibes. Tus propias respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de reparación, nunca se leen ni aparecen en la lista. Los correos sobre facturación, tu periodo de prueba o una invitación se leen con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, junto a **Posponer**. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué cambiar: cómo hacerlo o, cuando ya hay un borrador, qué cambiar en él. **Marcar como hecha** significa que ya está resuelta. Aparece en una tarea preparada sin borrador, o dentro de **…** en los demás casos, incluso si necesita que tomes una decisión. La tarea sale de la lista de inmediato y el mensaje ofrece **Deshacer**. Desliza el mensaje para quitarlo o arrástralo fuera con el mouse para cerrarlo antes. El cambio se mantiene.

Para que se haga de otra manera, dilo en su **Chat**.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve a aparecer con una frecuencia determinada](recurring.md).
- **No hace falta**: desaparece. Si quieres, elige un motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarlo. Tu título se mantiene.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve automáticamente cuando ocurre algo nuevo, como recibir un mensaje nuevo de esa persona, pero no cuando respondes tú.

Una factura que aún tengas que pagar, sea del país que sea, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluya. Las facturas que se pagan automáticamente, como las domiciliadas o las que usan una tarjeta guardada, no se convierten en tareas. Cuando un correo posterior indica que ya se pagó, por ejemplo, porque quien lo envió confirma que recibió el pago, la tarea se cierra automáticamente. **Deshacer** la devuelve durante un día.

Una tarea que solo sea relevante hasta una hora determinada, como una confirmación antes de una reunión, se cierra automáticamente después de esa hora. Pasa a **Hecho / descartado** con el motivo «Ya no hace falta». **Deshacer** la devuelve durante un día.

Antes de que un mensaje o un traspaso para otra persona aparezca como preparado, tu Machine comprueba tus chats recientes con las personas involucradas, incluidos los chats grupales, y espera a que Slack los lea. Si un mensaje posterior indica que ya está resuelto, por ejemplo, porque se lo pidieron y respondió que sí, la tarea se cierra automáticamente. **Deshacer** la devuelve durante un día.

Cuando un mensaje más reciente cambia el plan, por ejemplo, porque una fiesta se cambia de lugar o se cancela una reserva, The Machine actualiza sus tareas automáticamente. Si una tarea sigue siendo necesaria, se ajusta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** con el motivo «No hace falta». En su chat aparece «Actualizado:» y el motivo, y **Deshacer** la devuelve durante un día.

En tus primeras tareas aparece un consejo breve sobre las acciones principales: **Pedir cambios** y **No hace falta**, y sobre cómo no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas su botón o pulsas ×.

El primer día, aparece un saludo en la parte superior de Tareas y se indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, si es Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno, y sus iniciales si no. Si un logotipo no se distingue a ese tamaño, por ejemplo, si es blanco sobre un fondo transparente o un nombre ancho, también se muestran las iniciales.

A veces aparece una línea discreta que indica qué se desconoce, como «Último contacto hace 12 días por correo; no ha habido nada desde entonces». Aparece cuando el último contacto con esa persona es antiguo o no tuvo respuesta, e indica los canales que no están conectados, como WhatsApp. Tu Machine te dice qué no sabe en vez de hacer suposiciones.

Si menciona un canal que no está conectado, **Conectar**, junto a él, abre esa conexión.

El título indica qué hay que hacer y solo cambia cuando cambia la tarea. Una tarea hecha conserva su título y muestra debajo cómo terminó, como «Hecho: Sam lo firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje viene, junto con el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del destino para que veas enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en la opinión de alguien en otro lugar, como una sugerencia de un compañero en Slack, una línea lo indica, por ejemplo, «Basado en el mensaje de Sam en #ops». Tócala para leer ese mensaje.

Los chats (Slack, WhatsApp, Telegram, Intercom…) se muestran como una sola conversación, de más antiguo a más reciente: los mensajes anteriores al que trata la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje relacionado con la tarea lleva la marca «Esta tarea» y se abre directamente. **Mostrar mensajes anteriores** añade los mensajes más antiguos. En un correo, el resto del hilo aparece contraído por encima y por debajo.

**Detalles** de un correo muestra solo lo que no aparece en su encabezado, como las direcciones completas de Cc, Bcc o una dirección de respuesta distinta. Si no hay nada más que añadir, no aparece.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre, el proyecto y el área de la tarea (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. **Chat ›** abre el chat. Una tarea hecha ocupa menos espacio; el mensaje del que viene aparece en **Detalles**.

Una tarea que indique «Esperando a» enlaza con tu último mensaje a esa persona, el que estás esperando: «Correo a Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en una computadora) añade una tarea para lo que quieras. Al crearla no se envía nada. Si no eliges Trabajo ni Personal, se asigna al área que le corresponde según de quién y de qué trata. También encuentra el correo al que da seguimiento, incluso si es antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «en 2 horas», también en tu propio idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Mensaje**: adjunta el mensaje relacionado: un correo, un mensaje de Slack, Teams, WhatsApp, Telegram u otro que tenga The Machine. Busca por texto o por remitente. Cada resultado muestra de dónde viene, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En el teléfono, toca la cámara que aparece al lado para sacar una foto. Puedes añadir hasta 5 archivos, igual que en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Pulsa × para quitar un archivo.

Los archivos se quedan con la tarea y The Machine los lee cuando trabaja en ella. Puedes adjuntar solo archivos: la tarea se completa a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas a tamaño completo.
