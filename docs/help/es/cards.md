---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita que actúes, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e7e5d78b3291e556
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo requiere que actúes. Una tarea por asunto, por muchos mensajes que abarque.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba aparece el último paso que confirmaste, como un formulario o una incidencia, que se completó mientras no estabas. Se queda ahí hasta que pulses **Entendido**, como máximo durante un día, y también recibirás un aviso en el móvil.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero tienes que decidir o responder; si el trabajo se ha detenido porque falta algo que solo tú tienes, como un dato, un inicio de sesión o una decisión, aparece una línea bajo el título que lo explica), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o un informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas que no tienen novedades desde hace una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que has prometido y lo que otros te han prometido. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, empezando por las más recientes, con la hora a la que terminaron, como «Hecha hace 5 minutos». Las tareas que parecen terminadas ya aparecen marcadas como **Parece hecha**.

Después de enviar, una nota breve indica dónde ha ido la tarea, como «Enviado. Movida a Hecho» o «Enviado. Movida a Más tarde hasta el lun». Si la respuesta solo promete hacer el trabajo, como «Lo enviaré el martes», la tarea sigue abierta: «Enviado. Se ha mantenido abierta». **Abrir** te lleva a ella. La búsqueda encuentra tareas por su título o por la persona a quien se enviaron, también en Más tarde y Hecho.

**Para ti** muestra primero lo que está atrasado o vence mañana como muy tarde, después las preguntas de tu Fleet, luego los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, aparecen primero las tareas más recientes. Una tarea mantiene su posición mientras tu Machine la prepara y cuando se termina: solo cambia su marca. En los demás grupos abiertos, primero aparecen las tareas atrasadas o que vencen mañana como muy tarde, y después el resto, empezando por las más recientes. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está terminada, por ejemplo, «PR #3451 fusionada», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Al cabo de un día, se cierran automáticamente y puedes usar **Deshacer**. Una tarea que ya hayas resuelto por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierra automáticamente.

Si un mensaje procede de una dirección que solo parece pertenecer a alguien que conoces, como sam@acme-corp.example en vez de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que ha usado. Tu Machine comprueba el mensaje con la persona de la dirección que ya tienes, nunca con quien lo ha escrito.

Una tarea que sigue dependiendo de otra persona, como una revisión o una respuesta, indica **Esperando a**: ese paso. Aparece en **Esperando a otros**, plegada y encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que hayas respondido con una pregunta: vuelve a aparecer la mañana anterior a la fecha límite, en la fecha límite si es más tarde ese mismo día o a la mañana siguiente si la fecha ya ha pasado. También indica a quién sigue esperando.

Cuando una tarea consiste en esperar a que otra persona entregue un resultado, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje indique que el resultado está listo. Entonces se cierra automáticamente y puedes usar **Deshacer**. Si no recibes nada para cuando toque hacer un seguimiento, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como terminado para cambiarlo.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que las nuevas aparezcan primero cuando vuelvas unos días después. No hay novedades si no ha llegado ningún mensaje nuevo sobre ella y tampoco has hecho nada, como enviar un mensaje en el chat, editarla o posponerla. Abrirla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca como innecesarias todas las tareas de Más antiguos después de que confirmes una vez. **No hace falta** hace lo mismo con una tarea cada vez. En ambos casos, puedes usar **Deshacer**. Si aparece algo nuevo en una tarea, vuelve a Para ti.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y puedes usar **Deshacer**. **Mantener** la conserva y no vuelve a preguntarlo. Si no respondes durante otra semana, se pliega en Vuelve más tarde, y deja de contar para el número del icono de la app y el resumen de la mañana. Si la abres, escribes un mensaje en el chat, la editas, la pospones o llega un mensaje nuevo, vuelve a aparecer.

Una vez a la semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede recibir una tarea con un siguiente paso concreto, hasta tres por semana. Consulta [Proyectos](projects.md).

Cuando nada necesita que actúes, tu Machine descansa y deja la lista vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si falla una comprobación o se retrasa, su línea lo indica y aparece **Revisar ahora** debajo.

Las opciones **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo un tipo. El móvil y el ordenador muestran la misma selección. Si está activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como que un componente se reinicie una y otra vez, no es ni de Trabajo ni Personal, así que solo aparece en Todo.

La línea de la parte superior de la lista también te permite cambiar directamente a la otra opción: si estás en **Solo personal**, pulsa **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el nombre de tu último resumen de la mañana o de la tarde y lo que incluía, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Pulsa la fila para volver a leerlo. Usa **Copiar** para pegarlo donde quieras. Cuando lo abras o pulses su **×**, estará disponible en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto en Trabajo como en Personal, o solo en el área que hayas elegido filtrar.

Las tareas de un proyecto muestran su nombre debajo del título. Púlsalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También cambia los mensajes que puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita pasar a tu otra área para continuar y todos los mensajes relacionados ya están ahí, se mueve por sí sola y continúa. Si no, aparece **Mover a Trabajo** y no se mueve hasta que lo pulses. Una tarea que hayas añadido sin elegir Trabajo o Personal se mueve por sí sola cuando encuentra dónde corresponde. Hasta entonces, no aparece ni como Trabajo ni como Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. El correo de otra de tus empresas va a las tareas de esa empresa, y una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp o un pedido en tu buzón personal, es de Trabajo desde el principio. Una tarea que hayas movido o asignado tú se queda donde la hayas puesto. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, pero no dónde responde: la respuesta siempre se envía al lugar donde está la conversación, también después de moverla, salvo que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de Trabajo ni en el Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, te permite recorrerlas de una en una en el orden de la lista. Verás cada borrador completo, con **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Intro envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. Debajo del título, el encabezado también indica cuánto tardarás a tu ritmo, como «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen: necesitan tu respuesta, no que pulses un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes recibidos cuando hay 40 pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, dentro de la hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30, para que las tareas estén listas antes del resumen de la mañana. En Conexiones, las comprobaciones indican «Pausadas por la noche. Se pondrán al día a las 06:30». Si haces clic, escribes o te desplazas por la app, escribes en el chat o pulsas una tarea por la noche, las comprobaciones se reanudan como siempre hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba todo al momento.

**Revisar ahora** lee todas las fuentes al momento. Si no tienes tareas abiertas, pulsa la línea de tu Machine para verla con **Detalles**, que abre Comprobaciones, en Conexiones. Si tienes tareas abiertas, aparece arriba en el ordenador. Allí solo se muestra una línea breve mientras se ejecuta una comprobación, o cuando una ha fallado o se ha retrasado. También puedes preguntarlo en el chat.

LinkedIn, X y Salesflare mantienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de las tareas con lo que ha encontrado en todas las fuentes consultadas, por ejemplo, «13 mensajes comprobados a las 16:11 · nada requiere que actúes» o «· 2 tareas nuevas». Si una tarea nueva se espera a un momento más oportuno, como el resumen de la mañana, la línea indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Pulsa la línea para ver cada conversación de correo, chat y notificación, junto al icono de su servicio: quién ha escrito, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo estás en copia, responde un compañero» o «La reunión ya está fijada para el jueves». Si la comprobación solo ha dado un motivo impreciso, la conversación no muestra ningún motivo. Pulsa una para leerla.

Se muestran las 10 primeras. Pulsa debajo para ver el resto. El número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Las notificaciones del móvil sobre un mensaje que ya aparece en la lista solo se muestran una vez. La línea permanece visible durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de una reparación, nunca se leen ni aparecen en la lista. El correo sobre la facturación, tu periodo de prueba o una invitación se lee como siempre.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué cambiar: cómo hacerlo o, cuando el borrador esté listo, qué cambiar en él. **Marcar como hecho** indica que ya está resuelta: aparece directamente en una tarea lista que no tiene borrador. En los demás casos, está arriba en **…**, también en las tareas que necesitan que decidas. La tarea desaparece de la lista al momento y puedes usar **Deshacer** en el mensaje. Desliza el mensaje para quitarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se mantiene.

Para que se haga de otra forma, dilo en su **Chat**.

En **…**:

- **Pasar…**: asígnala a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: la tarea [volverá a aparecer con cierta frecuencia](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, elige el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Pulsa el título o **Nombre**, en **Detalles**, para cambiarlo. También puedes pedirlo en el chat de la tarea, por ejemplo: «Cámbiale el nombre a…». El título se mantiene.

**Reabrir** devuelve una tarea cerrada a la lista. También vuelve a aparecer automáticamente cuando pasa algo nuevo, como un mensaje nuevo de esa persona, pero no cuando respondes tú. La tarea indica cuándo ha vuelto a aparecer y se ordena como nueva. Su chat continúa donde lo dejaste, aunque hayan pasado semanas.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluya. Las facturas que se pagan automáticamente, como un recibo domiciliado o un cargo en una tarjeta guardada, no se convierten en tareas. Si un correo posterior indica que ya se ha pagado, por ejemplo, porque el remitente confirma que ha recibido el pago, la tarea se cierra automáticamente. Puedes usar **Deshacer** para recuperarla durante un día.

Una tarea que solo sea importante hasta una hora determinada, como una confirmación antes de una reunión, se cierra automáticamente cuando pasa esa hora. Se mueve a **Hecho / descartado** como «Ya no hace falta». Puedes usar **Deshacer** para recuperarla durante un día.

Antes de que un mensaje o un traspaso para alguien aparezca como listo, tu Machine comprueba los chats recientes que tienes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo han pedido y ha dicho que sí, la tarea se cierra automáticamente. Puedes usar **Deshacer** para recuperarla durante un día.

Si un mensaje posterior cambia el plan, por ejemplo, porque la fiesta se traslada a otro sitio o se cancela una reserva, The Machine actualiza sus tareas. Las que sigan siendo necesarias se ajustan al nuevo plan. Las que ya no requieran nada pasan a **Hecho / descartado** como «No hace falta». En el chat aparece «Actualizado:» seguido del motivo, y puedes usar **Deshacer** para recuperarlas durante un día.

En tus primeras tareas aparece un consejo breve sobre las acciones principales: **Pedir cambios** y **No hace falta**, y sobre cómo no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas su botón o pulsas ×.

El primer día, aparece un saludo en la parte superior de Tareas que indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero, para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién trata, la organización si tiene que ver con ella, pero no solo porque alguien trabaje allí, el proyecto, Trabajo o Personal y cuándo llegó. Pulsa un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno. Si no, muestran sus iniciales. Si un logotipo no se puede leer en tamaño pequeño, por ejemplo, porque es blanco sobre fondo transparente o porque es una marca denominativa muy ancha, también se muestran las iniciales.

A veces aparece una línea discreta con información desconocida, como «Último contacto hace 12 días por correo; no ha habido nada desde entonces». Se muestra si hace tiempo que no tienes noticias suyas o si no has recibido respuesta, e indica los canales que no están conectados, como WhatsApp. Tu Machine te dice lo que no sabe en lugar de hacer suposiciones.

Si se menciona un canal que no está conectado, pulsa Conectar al lado para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Una tarea terminada conserva su título y muestra debajo cómo terminó, por ejemplo, «Hecha: Sam la firmó el martes».

Encima del borrador, una línea tenue indica el mensaje del que procede y muestra el logotipo del servicio. Púlsala para leer la conversación. El borrador muestra el logotipo del canal al que se enviará, para que veas al instante si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que ha dicho alguien en otro sitio, como la sugerencia de un compañero en Slack, una línea lo indica, por ejemplo: «Basado en el mensaje de Sam en #ops». Púlsala para leer ese mensaje.

Los chats de Slack, WhatsApp, Telegram, Intercom… aparecen como una sola conversación, de los mensajes más antiguos a los más recientes: los mensajes anteriores al que dio lugar a la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje relacionado con la tarea aparece marcado como «Esta tarea» y se abre en pantalla. **Mostrar mensajes anteriores** añade mensajes más antiguos. En el correo, el resto de la conversación aparece plegado encima y debajo del mensaje.

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, lo abre en la app de Gmail si la tienes.

En **Detalles** de un correo solo se muestra la información que no aparece en el encabezado, como las direcciones completas de las personas en copia, la copia oculta o una dirección de respuesta diferente. Si no hay nada más que añadir, no aparece esta sección.

Las respuestas de un hilo de Slack también muestran lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre, el proyecto y el área, que puedes cambiar al pulsar uno, tu última nota y el resultado de un agente de programación. Al pulsar el título, se abre el chat. Las tareas terminadas se muestran de forma compacta; el mensaje del que proceden está en **Detalles**.

Una tarea «Esperando a» incluye un enlace a tu último mensaje a esa persona, el que está pendiente de respuesta: «Correo a Pat · mar».

## Crea una tarea

**Nueva tarea**, debajo de **Buscar** en el ordenador, **+** en el móvil o `N`, añade una tarea para lo que quieras. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, se asigna al área que corresponda según quién y qué estén relacionados. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario incluye opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve a aparecer con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula a las personas o empresas relacionadas, hasta un máximo de 5.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro que tenga The Machine. Busca por texto o remitente. Cada resultado indica su origen, quién lo ha enviado y cuándo.
- **Archivos**: pulsa el clip, pega una captura de pantalla o arrastra archivos al formulario. En el móvil, puedes hacer una foto con la cámara que aparece al lado. Puedes añadir hasta 5 archivos, como en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Pulsa × para quitar uno.

Los archivos se quedan con la tarea y The Machine los lee cuando trabaja en ella. Puedes añadir solo archivos: rellenará la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Púlsalas para verlas a tamaño completo.
