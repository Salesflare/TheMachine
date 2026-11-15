---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesita de ti, lista para que des tu visto bueno. Esto es lo que significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 81b65d513aa5941b
---
The Machine lee todo lo nuevo y crea una tarea solo cuando algo necesita de ti. Una tarea por asunto, sin importar cuántos mensajes abarque.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba del todo, aparece un último paso que confirmaste, como un formulario o una solicitud, y que se completó mientras no estabas. Se queda ahí hasta que toques **Entendido**, como máximo un día, y también recibirás una notificación en el teléfono.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (el trabajo está hecho y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero hace falta que decidas o respondas), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe breve, sin nada que decidir).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso le corresponde a otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas y las que no tienen respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, empezando por las más recientes, con la hora en que se terminaron, como «Hecha hace 5 minutos». Las tareas que parecen terminadas aparecen marcadas como **Parece hecho**.

Después de enviar algo, aparece una nota breve que indica adónde fue la tarea, como «Enviado. Movido a Hecho» o «Enviado. Movido a Más tarde hasta el lun.». **Abrir** te lleva a ella. La búsqueda encuentra tareas por su título o por la persona a quien se enviaron, también en Más tarde y Hecho.

En **Para ti**, primero aparecen las tareas atrasadas o que vencen mañana o antes; después, las preguntas de tu Fleet, luego, los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, primero aparecen las más recientes. Una tarea conserva su posición mientras tu Machine la prepara y cuando se termina: solo cambia su marca. En los demás grupos abiertos, primero aparecen las tareas atrasadas o que vencen mañana o antes, y después el resto, empezando por las más recientes. La barra lateral mantiene el mismo orden.

**Parece hecho** significa que tu Machine ve que ya está hecho, como «PR #3451 fusionada», pero la tarea aún no está cerrada. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Al cabo de un día, se cierra automáticamente y aparece **Deshacer**. Una tarea que ya resolviste por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierra automáticamente.

Si un mensaje viene de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La muestra con su propia dirección, nunca con el nombre que usó. Tu Machine comprueba el mensaje con la persona cuya dirección ya tienes, nunca con quien lo escribió.

Si una tarea sigue pendiente de otra persona, por ejemplo, una revisión o una respuesta, indica **Esperando a:** y el paso pendiente. Aparece plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la vuelva a mostrar. Lo mismo ocurre después de que tú haces una pregunta: vuelve a aparecer la mañana anterior a la fecha límite, en la fecha límite si es más tarde hoy, o a la mañana siguiente si ya pasó. También indica de quién sigue esperando respuesta.

Si la tarea depende de un resultado que debe entregar otra persona, como un contrato firmado, **Detalles** lo muestra en **Hecho cuando**. Enviar tu parte no cierra la tarea: queda en **Esperando a otros** hasta que un mensaje indique que se obtuvo el resultado. Entonces se cierra automáticamente y aparece **Deshacer**. Si no recibes nada para cuando toque hacer seguimiento, la tarea vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como tarea terminada para cambiarlo.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y aparece **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, escribes un mensaje en el chat, la editas, la pospones o llega un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que se haya quedado inactivo y no tenga tareas abiertas puede recibir una tarea con un siguiente paso concreto, como máximo tres por semana. Consulta [Proyectos](projects.md).

Si nada necesita de ti, tu Machine descansa con una lista vacía. Mientras comprueba, se activa y te lo indica. Si una comprobación falla o se retrasa, su línea lo indica y aparece **Revisar ahora** debajo.

**Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, permiten mostrar todas las tareas o solo las de un tipo. El teléfono y el ordenador muestran la misma selección. Si tienes activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como que un componente se reinicia continuamente, no es ni de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente a otra opción: si estás en **Solo personal**, toca **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el último resumen de la mañana o de la tarde y lo que incluye, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leer ese resumen. Puedes usar **Copiar** para pegarlo donde quieras. Cuando lo abres o tocas su **×**, aparece en todos tus dispositivos hasta el siguiente resumen.

Si no hay ningún resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto para Trabajo como para Personal, o solo para la opción que hayas seleccionado.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiar el proyecto o quitar la tarea de él. Consulta [Tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, permite mover una tarea a tu otra área. También cambia lo que puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Si una tarea necesita pasar a tu otra área para continuar y todos los mensajes relacionados están allí, se mueve automáticamente y sigue adelante. Si no, aparece **Mover a Trabajo** y no se mueve hasta que lo toques. Una tarea que añadiste sin elegir Trabajo o Personal se mueve automáticamente cuando encuentra el área a la que pertenece. Hasta entonces, no aparece ni como Trabajo ni como Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes relacionados. Si necesita leer otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. El correo de otra de tus empresas va a las tareas de esa empresa, y una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente que te escribe por WhatsApp o un pedido en tu buzón personal, es Trabajo desde el principio. Una tarea que hayas movido o asignado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece la tarea y con quién se comparte, pero nunca desde dónde responde: la respuesta siempre se envía al lugar donde está la conversación, incluso después de moverla, salvo que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en una Fleet de Trabajo ni en el Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, te las muestra de una en una y en el orden de la lista. Muestra cada borrador completo, con **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. Debajo del título, el encabezado también indica cuánto tardarás a tu ritmo, como «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen en ninguno de los dos grupos: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes recibidos cuando hay 40 pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en el plazo de una hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se comprueban juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «Pausadas por la noche; se pondrán al día a las 06:30». Si abres la app, escribes en el chat o tocas una tarea por la noche, las comprobaciones vuelven a funcionar con normalidad hasta que pase una hora sin actividad. **Revisar ahora** siempre comprueba todo de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no tienes tareas abiertas, toca la línea de tu Machine para verla y acceder a **Detalles**, que abre Comprobaciones dentro de Conexiones. Si tienes tareas abiertas, aparece arriba del todo en el ordenador. Solo se muestra una línea breve mientras se ejecuta una comprobación o cuando una falla o se retrasa. También puedes pedirlo en el chat.

LinkedIn, X y Salesflare mantienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que encontró en todas las fuentes que leyó, como «Se comprobaron 13 mensajes a las 16:11 · nada necesita de ti» o «· 2 tareas nuevas». Si una tarea nueva debe esperar a un momento más oportuno, como el resumen de la mañana, indica hasta cuándo: «1 tarea en espera hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación con el icono de su fuente: quién escribió, el asunto o las primeras palabras y la nueva tarea o el motivo por el que no hacía falta crear una, como «Solo estás en copia; otra persona del equipo responde» o «La reunión ya está programada para el jueves». Si la comprobación solo dio un motivo impreciso, no se muestra ningún motivo para el hilo. Tócalo para leerlo.

Se muestran los primeros 10. Toca debajo para ver el resto. El número que aparece después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Las notificaciones del teléfono sobre mensajes que ya están en la lista solo aparecen una vez. La línea permanece durante 12 horas después de la comprobación.

Solo cuenta el correo que te llega. Tus propias respuestas se leen para tener contexto y registrar promesas, pero no cuentan como correo nuevo. The Machine nunca lee ni muestra sus propios correos, como el resumen de la mañana o un aviso de reparación. El correo sobre facturación, tu periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** te permite indicar qué cambiar: cómo hacerlo o, cuando ya hay un borrador, qué modificar en él. **Marcar como hecha** indica que ya está resuelta: aparece a la vista en las tareas preparadas sin borrador y, en los demás casos, en la parte superior de **…**, también en las tareas que necesitan que decidas. La tarea sale de la lista de inmediato y aparece **Deshacer** en el mensaje. Desliza el mensaje para quitarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se mantiene.

Para que se haga de otra manera, díselo en su **Chat**.

En **…**:

- **Pasar…**: asígnasela a alguien del equipo, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: la tarea [vuelve con cierta frecuencia](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, elige un motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarlo. Tu título se mantiene.

**Reabrir** devuelve una tarea cerrada. También vuelve a aparecer automáticamente cuando pasa algo nuevo, como recibir un mensaje nuevo de esa persona, pero no cuando respondes tú.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluye. Las facturas que se pagan automáticamente, como un cargo directo o una tarjeta guardada, no se convierten en tareas. Cuando un correo posterior indica que se pagó, por ejemplo, porque quien lo envió confirma que recibió el pago, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Una tarea que solo sea importante hasta una hora determinada, como una confirmación antes de una reunión, se cierra automáticamente al llegar esa hora. Pasa a **Hecho / descartado** con el estado «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de que un mensaje o un traspaso para alguien aparezca como preparado, tu Machine comprueba los chats recientes que tienes con las personas involucradas, incluidos los chats grupales, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo pidieron y aceptó, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Si un mensaje nuevo cambia el plan, por ejemplo, porque la fiesta se trasladó a otro lugar o se canceló una reserva, The Machine actualiza sus tareas automáticamente. Si una tarea sigue siendo necesaria, se adapta al nuevo plan. Si ya no queda nada por hacer, pasa a **Hecho / descartado** con el estado «No hace falta». En el chat aparece «Actualizada:» y el motivo, y **Deshacer** la recupera durante un día.

En tus primeras tareas, aparece un consejo breve sobre las acciones clave: **Pedir cambios** y **No hace falta**, y sobre el hecho de que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas su botón o pulsas ×.

El primer día, la parte superior de Tareas te da la bienvenida y te dice quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea debajo indica de quién se trata, la organización si corresponde, pero no solo porque alguien trabaje allí, el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en el Graph.

Los nombres y las organizaciones muestran su foto o logotipo si hay uno en el Graph; de lo contrario, muestran sus iniciales. Si un logotipo no se ve bien en ese tamaño, por ejemplo, por tener texto blanco sobre un fondo transparente o un nombre muy ancho, también se muestran las iniciales.

A veces, aparece una línea discreta con información que no se conoce, como «Último contacto hace 12 días por correo; no ha habido nada desde entonces». Se muestra cuando el último contacto fue hace tiempo o no tuvo respuesta. También indica los canales que no están conectados, como WhatsApp. Tu Machine te dice lo que no sabe en vez de adivinar.

Si menciona un canal que no está conectado, la opción Conectar que aparece al lado abre esa conexión.

El título indica lo que hay que hacer y solo cambia si eso cambia. Una tarea terminada conserva su título y muestra debajo cómo acabó, como «Hecha: Sam la firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje viene y muestra el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del lugar al que se enviará, para que veas de inmediato si es una respuesta en Slack o un correo.

Si el borrador se basa en lo que alguien dijo en otro lugar, como la sugerencia de un compañero en Slack, aparece una línea que lo indica, como «Basado en el mensaje de Sam en #ops». Tócala para leer ese mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) muestra una conversación completa, empezando por los mensajes más antiguos: los que aparecen antes del mensaje relacionado con la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje relacionado con la tarea está marcado como «Esta tarea» y se muestra en la conversación. **Mostrar mensajes anteriores** añade mensajes más antiguos. En un correo, el resto del hilo aparece plegado arriba y abajo.

En **Detalles** de un correo solo aparecen los datos que no figuran en el encabezado, como las direcciones completas de Cc, Bcc o una dirección de respuesta distinta. Si no hay nada más que mostrar, no aparece esta sección.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** al final.

**Detalles** muestra el nombre, el proyecto y el área (toca cualquiera para cambiarlo), tu última nota y el resultado de un agente de programación. El título abre el chat. Las tareas hechas aparecen en una versión resumida; el mensaje relacionado está en **Detalles**.

Una tarea «En espera» enlaza con tu último mensaje a esa persona, el que estás esperando: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea**, debajo de **Buscar** en un ordenador, **+** en un teléfono o `N`, permite crear una tarea para cualquier cosa. Al crearla no se envía nada. Si no seleccionas **Trabajo** ni **Personal**, la tarea se asigna al área correspondiente según de quién se trate y cuál sea el asunto. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie.», «3 nov», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario muestra opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve con cierta frecuencia. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula hasta 5 personas o empresas relacionadas con la tarea.
- Icono de mensaje: adjunta el mensaje relacionado, ya sea un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o por remitente. Cada resultado indica de dónde viene, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En un teléfono, la cámara que aparece al lado te permite hacer una foto. Puedes añadir hasta 5 archivos, igual que en el chat. Consulta [Añadir archivos](card-chat.md#add-files). Toca × para quitar un archivo.

Los archivos se quedan con la tarea y The Machine los lee cuando trabaja en ella. Puedes adjuntar solo archivos: completa la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas en tamaño completo.
