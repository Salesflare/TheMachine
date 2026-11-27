---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesite tu atención, lista para que des tu visto bueno. Descubre qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: dfbc7ccc7313ecfe
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo necesita tu atención. Una tarea por asunto, por muchos mensajes que incluya.

## Dónde están las tareas

La página **Tareas** las agrupa así:

- **Recién hecho**: arriba aparece el último paso que confirmaste, como un formulario o una incidencia, que se completó mientras no estabas. Se queda ahí hasta que pulses **Entendido**, como máximo durante un día, y también recibirás una notificación en el móvil.
- **Para ti**: todo lo que está pendiente de ti, primero lo que vence mañana o antes. Cada tarea indica **Preparada** (hay un borrador o un resultado listo, y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (antes hace falta que decidas o respondas; si el trabajo no puede continuar o utilizarse sin algo que solo tú tienes, como un precio, un dato o una decisión, debajo del título se indica qué es), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe, sin nada que decidir).
- **Más antiguos**: tareas plegadas que no han tenido novedades en una semana (más abajo).
- **Esperando a otros**: tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: tareas pospuestas, mensajes que [se envían más tarde](send-later.md) y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, de la más reciente a la más antigua, con el momento en que terminaron, como «Hecha hace 5 minutos». Las tareas que parecen terminadas llevan la etiqueta **Parece hecha**.

Después de enviar algo, una nota breve indica adónde ha ido la tarea, como «Enviado. Se ha movido a Hecho» o «Enviado. Se ha movido a Vuelve más tarde hasta el lunes». Si una respuesta solo promete hacer el trabajo, como «Te lo enviaré el martes», la tarea sigue abierta: «Enviado. Se ha mantenido abierta». **Abrir** te lleva a la tarea. Puedes buscar tareas por título o por la persona a quien se enviaron, también en Vuelve más tarde y Hecho.

En **Para ti** aparecen primero las tareas vencidas o que vencen mañana o antes, luego las preguntas de tu Fleet, después los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, las más recientes van primero. Una tarea no cambia de sitio mientras tu Machine la prepara ni cuando termina: solo cambia su estado. En los demás grupos abiertos, primero aparecen las vencidas o las que vencen mañana o antes; después, las demás, de más recientes a más antiguas. La barra lateral mantiene el mismo orden.

**Parece hecha** significa que tu Machine ve que ya está terminada, como «PR #3451 fusionada», pero aún no se ha cerrado. **Reabrir** la devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Si aparece en un mensaje, se cierra automáticamente al cabo de un día y puedes pulsar **Deshacer**. En los demás casos, espera a que pulses **Marcar como hecho**.

Una tarea que ya hayas resuelto tú, por ejemplo, respondiendo en Gmail o Slack, también se cierra automáticamente. Si una respuesta dice que se ha adjuntado un archivo y no es así, la tarea no se cierra.

Si un mensaje procede de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que ha usado. Tu Machine comprueba estos mensajes con la persona de la dirección que ya tienes, nunca con quien los ha escrito.

Si una tarea sigue pendiente de otra persona, por ejemplo de una revisión o una respuesta, indica el paso pendiente con **Esperando a**. Se queda plegada en **Esperando a otros**, encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que hayas hecho una pregunta: la tarea vuelve a aparecer la mañana anterior a la fecha límite, cuando llegue la fecha límite si es más tarde ese mismo día, o a la mañana siguiente si ya ha pasado. También indica quién tiene que responder.

Si una tarea depende de un resultado que te entregará otra persona, como un contrato firmado, en **Detalles** aparece como **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje muestre el resultado. Entonces se cierra automáticamente con el resultado y **Deshacer**. Si no recibes nada para cuando toque insistir, la tarea vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Para cambiar qué cuenta como terminado, díselo en el chat.

Si el resultado aparecerá en una página web pública que se menciona en los mensajes, como un artículo que te incluirá, tu Machine consulta esa página cuando llega el momento de insistir. Si aparece el resultado y no aparecía cuando la tarea empezó a esperar, se cierra automáticamente y muestra el resultado. Puedes pulsar **Deshacer**. Tu Machine solo consulta la página, como lo haría cualquier visitante, y nunca envía nada.

Si el resultado no aparece en la página y aún no ha llegado la fecha límite, tu Machine vuelve a consultarla a la mañana siguiente. En los demás casos, la tarea vuelve a aparecer como antes, con «Comprobado» o «No se ha podido abrir» y la página en su chat.

Si una tarea no tiene novedades durante una semana, pasa de Para ti a **Más antiguos**, para que las tareas recientes aparezcan primero cuando vuelvas después de unos días. Se considera que no hay novedades si no hay mensajes nuevos ni actividad tuya, como escribir en el chat, editar o posponer la tarea. Solo mirarla no cuenta.

Las tareas urgentes, las que vencen pronto y las que tienen un envío en curso se quedan en Para ti. **Descartar todo** marca todas las tareas de Más antiguos como no necesarias con una sola confirmación, igual que **No hace falta** lo hace de una en una. Puedes pulsar **Deshacer**. Si hay novedades en una tarea, vuelve a Para ti.

Si nadie interactúa con una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra. Puedes pulsar **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, escribes en el chat, la editas, la pospones o recibes un mensaje nuevo, vuelve a aparecer.

Una vez a la semana, un proyecto que se haya quedado parado y no tenga tareas abiertas puede generar una tarea con un siguiente paso concreto. Como máximo, se crean tres a la semana. Consulta [Proyectos](projects.md).

Cuando nada necesita tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba las fuentes, se activa y te lo indica. Si una comprobación falla o se retrasa, la línea lo indica y aparece **Revisar ahora** debajo.

Las opciones **Todo**, **Trabajo** y **Personal** de la parte superior de la barra lateral muestran todas las tareas o solo las de un tipo. En el móvil y el ordenador aparece la misma selección. Si está activado Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como que un componente se reinicia continuamente, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también permite cambiar directamente a la otra opción: si estás en **Solo personal**, pulsa **Trabajo** o **Mostrar todo**.

La fila de la parte superior de la lista muestra el último resumen de la mañana o de la tarde y lo que incluye, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Púlsala para volver a leerlo. Con **Copiar**, puedes pegarlo donde quieras. Cuando lo abres o pulsas su **×**, aparece en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha terminado hoy y lo que sigue abierto, tanto de Trabajo como de Personal o solo de la opción seleccionada.

Las tareas de un proyecto muestran el nombre del proyecto debajo del título. Púlsalo para abrir el proyecto. En **Detalles**, puedes cambiar el **Proyecto** o quitarlo. Consulta [Las tareas de un proyecto](projects.md#a-project-s-to-dos).

En **Detalles**, **Área** cambia una tarea a la otra área. También cambia con ella lo que puede leer y enviar. Si pulsas **Deshacer** en la nota, la tarea vuelve a su área anterior.

Si una tarea necesita pasar a la otra área para continuar y todos los mensajes de los que procede están allí, se mueve automáticamente y sigue adelante. Si no, aparece **Mover a Trabajo** y no se mueve hasta que lo pulses. Una tarea que hayas añadido sin elegir Trabajo o Personal se mueve automáticamente cuando encuentra el área a la que pertenece. Hasta entonces, no aparece ni en Trabajo ni en Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te lo pide con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas etiquetado como Personal cuenta como Personal. El correo de otras empresas tuyas va a las tareas de esa empresa. Una tarea sobre tu vida personal, como un mensaje de tu familia a tu dirección de trabajo, es Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp, un pedido en tu buzón personal o una [promesa](promises.md) relacionada con el trabajo, es Trabajo desde el principio.

Una tarea que hayas movido o asignado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece la tarea y con quién se comparte, pero no dónde responde: la respuesta siempre se envía en la conversación original, aunque hayas movido la tarea, salvo que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de trabajo ni en Graph del equipo.

Si tienes dos o más tareas pendientes, **Repasar** en el encabezado de Para ti las recorre de una en una, en el orden de la lista, con cada borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Intro envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. El encabezado indica cuánto tardarás a tu ritmo, como «unos 2 min».

Al final, indica cuántas tareas se han enviado o cerrado y cuántas siguen preparándose.

Las tareas que te hacen una pregunta no se incluyen en el repaso: necesitan tu respuesta, no un toque.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes recibidos cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, en un plazo de una hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan. Los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30, para que las tareas estén listas antes del resumen de la mañana. En Conexiones, las comprobaciones indican «Pausadas por la noche; se pondrán al día a las 06:30». Si por la noche haces clic, escribes o te desplazas por la app, escribes en el chat o pulsas una tarea, las comprobaciones se reanudan como de costumbre hasta que lleves una hora sin actividad. **Revisar ahora** siempre comprueba las fuentes de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no tienes tareas abiertas, pulsa la línea de tu Machine para verla, con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, en el ordenador la opción aparece en la parte superior. La línea breve solo aparece mientras se ejecuta una comprobación o cuando una ha fallado o se ha retrasado. También puedes preguntarlo en el chat.

LinkedIn, X y Salesflare mantienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de las tareas con lo que ha encontrado en todas las fuentes consultadas, como «13 mensajes comprobados a las 16:11 · sin tareas nuevas» o «· 2 tareas nuevas». Solo se refiere a esa comprobación: las tareas que ya estaban en la lista siguen pendientes como antes. Si una tarea nueva tiene que esperar a un mejor momento, como al resumen de la mañana, la línea indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Pulsa la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién lo escribió, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta ninguna, como «Solo estaba en copia; responde otra persona del equipo» o «La reunión ya está programada para el jueves». Si la comprobación solo encontró un motivo impreciso, el hilo no muestra ninguno. Pulsa un elemento para leerlo y ver lo que se dijo a su alrededor.

Se muestran los 10 primeros. Pulsa debajo para ver el resto. El número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Las notificaciones de Android sobre mensajes que ya aparecen en la lista solo se muestran una vez. La línea aparece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Los correos de The Machine, como el resumen de la mañana o un aviso de reparación, nunca se leen ni se muestran. El correo sobre facturación, una prueba o una invitación sí se lee como de costumbre.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** te permite indicar qué hay que cambiar: cómo hacerlo o, cuando el borrador esté listo, qué cambiar en él. Si dejas el texto a medias, seguirá ahí cuando vuelvas. **Cancelar** lo descarta.

**Marcar como hecho** indica que ya está resuelta. En un ordenador, aparece junto a los demás botones cuando caben en una sola línea. En el móvil, está a la vista en las tareas listas que no tienen borrador o que te hacen una pregunta. En los demás casos, está en la parte superior de **…**. La tarea sale de la lista de inmediato y aparece **Deshacer** en el mensaje. Desliza el mensaje o arrástralo con el ratón para cerrarla antes. El cambio se mantiene.

Para resolverla de otra manera, díselo en su **Chat**. La respuesta solo indica qué ha cambiado, por ejemplo, si se ha pospuesto y hasta cuándo. Si no se ha podido cambiar algo, como la fecha de vencimiento, también lo indica.

En **…**:

- **Pasar…**: asígnala a un compañero, a [Claude Code o Codex](hand-to-agent.md) o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: la tarea [vuelve a aparecer con una frecuencia determinada](recurring.md).
- **No hace falta**: la tarea desaparece. Si quieres, elige el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Pulsa el título o **Nombre** en **Detalles** para cambiarlo, o pídelo en el chat, por ejemplo: «Cámbiale el nombre a…». El título se mantiene.

**Reabrir** devuelve a la lista una tarea cerrada. También puede volver automáticamente si ocurre algo nuevo, como recibir un mensaje de esa persona, pero no si respondes tú. En ese caso, indica cuándo volvió y se ordena como una tarea nueva. El chat continúa donde se quedó, aunque hayan pasado semanas.

Una factura que tengas que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que indica la factura. Las facturas que se pagan automáticamente, como las domiciliadas o las que se cargan a una tarjeta guardada, no se convierten en tareas. Cuando un correo posterior indique que se ha pagado, por ejemplo, si el remitente confirma que ha recibido el pago, la tarea se cierra automáticamente. Puedes pulsar **Deshacer** durante un día.

Una tarea que solo sea relevante hasta una hora determinada, como una confirmación antes de una reunión, se cierra automáticamente después de esa hora. Pasa a **Hecho / descartado** con la indicación «Ya no hace falta». Puedes pulsar **Deshacer** durante un día.

Antes de que un mensaje o un traspaso para otra persona aparezca como listo, tu Machine comprueba los chats recientes que tienes con las personas implicadas, incluidos los chats de grupo, y espera a que Slack los lea. Si un mensaje posterior indica que ya está resuelto, por ejemplo, porque se lo pidieron y aceptó, la tarea se cierra automáticamente. Puedes pulsar **Deshacer** durante un día.

Si otra persona escribe en la misma conversación después de que se haya creado el borrador, **Enviar** lo detiene y muestra «No se ha enviado: hay un mensaje nuevo en el hilo». La tarea muestra ese mensaje y las opciones **Leerla** y **Rehacer para este mensaje**. Pulsa **Enviar** otra vez para enviar el borrador tal como está.

Si un mensaje más reciente cambia el plan, por ejemplo, porque la fiesta se traslada a otro local o se cancela una reserva, The Machine actualiza sus tareas automáticamente. Las que sigan siendo necesarias se adaptan al nuevo plan. Las que ya no requieran ninguna acción pasan a **Hecho / descartado** con la indicación «No hace falta». En el chat aparece «Actualizado:» y el motivo. Puedes pulsar **Deshacer** durante un día.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas el botón correspondiente o pulsas ×.

El primer día, aparece un saludo en la parte superior de Tareas y se indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero para que esté lista cuando llegues.

Cada tarea empieza con su título. Debajo se indica a quién se refiere, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, si es de Trabajo o Personal y cuándo llegó. Pulsa un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno; si no, muestran sus iniciales. Si un logotipo no se distingue bien a ese tamaño, por ejemplo, porque tiene letras blancas sobre un fondo transparente o un nombre muy ancho, también se muestran las iniciales.

A veces aparece una línea discreta que indica lo que no se sabe, como «Último contacto por correo hace 12 días; no ha habido nada desde entonces». Aparece si hace mucho que no hay noticias de esa persona o si está esperando una respuesta. También indica los canales que no están conectados, como WhatsApp. Tu Machine dice lo que no sabe en vez de adivinar.

Si menciona un canal que no está conectado, pulsa Conectar junto al nombre para conectar esa cuenta.

El título indica qué hay que hacer y solo cambia si cambia la tarea. Una tarea terminada conserva su título y muestra debajo cómo terminó, como «Hecha: Sam la firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje procede y muestra el logotipo del servicio. Púlsala para leer el hilo. El borrador muestra el logotipo del lugar al que se enviará, para que veas enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que alguien ha dicho en otro sitio, como una sugerencia de un compañero en Slack, aparece una línea que lo indica, como «Basado en un mensaje de Sam en #ops». Púlsala para leer el mensaje. Desaparece cuando una actualización sustituye el borrador.

Un chat de Slack, WhatsApp, Telegram, Intercom u otro servicio se muestra como una sola conversación, de más antiguo a más reciente: los mensajes anteriores al que trata la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje de la tarea lleva la etiqueta «Esta tarea» y se abre directamente en la vista. **Mostrar mensajes anteriores** añade mensajes más antiguos. En los correos, el resto del hilo aparece plegado encima y debajo del mensaje.

Los mensajes también se abren así desde la búsqueda, Graph, las respuestas de Ask o la última comprobación, con la etiqueta «Este mensaje» o «Mensajes nuevos».

**Abrir en Gmail** abre el correo en la cuenta de Gmail a la que llegó. En Android, se abre en la app de Gmail si la tienes instalada.

En **Detalles** de un correo solo aparece lo que no figura en su encabezado, como las direcciones completas de Cc, Cco o una dirección de respuesta distinta. Si no hay nada más que mostrar, no aparece esta sección.

Las respuestas en un hilo de Slack también muestran lo que se dijo antes de que empezara el hilo. El enlace al mensaje de una tarea también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre, el proyecto y el área de la tarea (pulsa cualquiera para cambiarlo), tu última nota y el resultado de un agente de programación. Al pulsar el título, se abre el chat. Las tareas terminadas se muestran de forma resumida; el mensaje del que proceden aparece en **Detalles**.

Una tarea que indica «Esperando a» enlaza tu último mensaje a esa persona con el mensaje que estás esperando: «Correo a Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un móvil o `N`) añade una tarea para lo que quieras. Al crearla no se envía nada. Si no eliges **Trabajo** ni **Personal**, se asigna al área que corresponda según de quién y de qué trate. También encuentra el correo al que da seguimiento, aunque sea antiguo.

Si cierras la tarea antes de añadirla, el texto y las opciones que hayas elegido estarán ahí la próxima vez, pero no los archivos. Pulsa **Descartar** en el mensaje para quitarlos.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «dentro de 2 horas». También puedes escribirlo en tu idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Se repite**: la tarea vuelve a aparecer con una frecuencia determinada. Consulta [Tareas recurrentes](recurring.md).
- **Persona**: vincula las personas o empresas a las que se refiere, hasta 5.
- Icono de mensaje: adjunta el mensaje relacionado, como un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o por remitente. Cada resultado indica de dónde procede, quién lo envió y cuándo.
- **Archivos**: pulsa el clip, pega una captura de pantalla o arrastra archivos al formulario. En el móvil, puedes hacer una foto con la cámara que aparece al lado. Puedes añadir hasta 5 archivos, como en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Pulsa × para quitar uno.

Los archivos se quedan en la tarea y The Machine los lee cuando trabaja en ella. Puedes añadir solo archivos: The Machine crea la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Púlsalas para verlas a tamaño completo.
