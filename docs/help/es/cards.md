---
title: Tareas
area: cards
summary: Una tarea por cada cosa que necesite tu atención, lista para que des el visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 12be97d431968927
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo requiere tu atención. Una tarea por asunto, aunque abarque muchos mensajes.

## Dónde están las tareas

La página **Tareas** las organiza así:

- **Recién hecho**: arriba, aparece el último paso que confirmaste, como un formulario o una incidencia, que se completó mientras no estabas. Se queda hasta que toques **Entendido**, como máximo durante un día, y también recibirás una notificación en el teléfono.
- **Para ti**: todo lo que está pendiente de ti, empezando por lo más urgente. Cada tarea indica **Preparada** (el trabajo está hecho y **Hazlo** o **Enviar** lo ejecuta), **Te necesita** (primero necesita tu decisión o respuesta), **Preparando…** (tu Machine está trabajando en ello) o **Para leer** (un resumen o informe breve, sin nada que decidir).
- **Esperando a otros**: las tareas plegadas cuyo siguiente paso depende de otra persona (más abajo).
- **Vuelve más tarde**: las tareas pospuestas y las que no recibieron respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas terminadas, empezando por las más recientes, con la hora a la que se completaron, como «Hecho hace 5 minutos». Las tareas que parecen terminadas ya aparecen marcadas como **Parece hecho**.

Después de enviar algo, una nota breve indica adónde fue la tarea, como «Enviado. Movido a Hecho» o «Enviado. Movido a Más tarde hasta el lun.». **Abrir** te lleva a la tarea. La búsqueda encuentra tareas por título o por la persona a quien se enviaron, también en Más tarde y Hecho.

En **Para ti**, primero aparecen las tareas vencidas o que vencen mañana como muy tarde, después las preguntas de tu Fleet, luego los seguimientos de un tablero y, por último, el resto. Dentro de cada grupo, las más recientes aparecen primero. Una tarea conserva su lugar mientras tu Machine la prepara y cuando está hecha: solo cambia su estado. En los demás grupos abiertos, primero aparecen las tareas vencidas o que vencen mañana como muy tarde, y luego el resto, empezando por las más recientes. La barra lateral mantiene el mismo orden.

**Parece hecho** significa que tu Machine ve que ya está terminado, como «PR #3451 combinado», pero aún no está cerrado. **Reabrir** lo devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Al cabo de un día, se cierra automáticamente y aparece **Deshacer**. Una tarea que ya hayas resuelto por tu cuenta, por ejemplo, respondiendo en Gmail o Slack, también se cierra automáticamente.

Cuando un mensaje llega de una dirección que solo se parece a la de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «No es Sam Lee». La persona aparece con su propia dirección, nunca con el nombre que usó. Tu Machine comprueba estos mensajes con la persona de la dirección que ya tienes, nunca con quien escribió.

Una tarea que aún depende de otra persona, como una revisión o una respuesta, indica ese paso con **Esperando a**. Se queda plegada en **Esperando a otros**, por encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que hagas una pregunta: vuelve la mañana antes de la fecha límite, en la fecha límite si es más tarde ese mismo día o a la mañana siguiente si ya pasó. También indica a quién sigue esperando.

Cuando una tarea depende de un resultado que debe entregar otra persona, como un contrato firmado, **Detalles** lo muestra como **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje indique que ya se obtuvo el resultado. Entonces se cierra automáticamente y aparece **Deshacer**. Si no llega nada para cuando toque hacer seguimiento, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Para cambiar qué cuenta como terminado, explícalo en el chat.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra y aparece **Deshacer**. **Mantener** la conserva y no volverá a preguntar. Si no respondes durante otra semana, se pliega en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, escribes en el chat, la editas, la pospones o llega un mensaje nuevo, vuelve a aparecer.

Una vez a la semana, un proyecto que lleva un tiempo inactivo y no tiene tareas abiertas puede generar una tarea con un siguiente paso concreto. Como máximo, tres a la semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine descansa con la lista vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, la línea lo indica y muestra **Revisar ahora** debajo.

Las opciones **Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, muestran todas las tareas o solo las de un tipo. El teléfono y el ordenador muestran la misma selección. Mientras esté seleccionada la opción Trabajo o Personal, **Mostrar todo** vuelve a mostrar todas las tareas. Una alerta sobre tu Machine, como un componente que se reinicia continuamente, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también cambia directamente a la otra opción: **Solo Personal · Trabajo · Mostrar todo**.

La fila de la parte superior de la lista muestra el nombre de tu último resumen de la mañana o de la tarde y lo que incluía, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leer ese resumen. Puedes usar **Copiar** para pegarlo donde quieras. Cuando lo abres o tocas su **×**, aparece en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto de Trabajo como de Personal, o solo de la opción que hayas seleccionado.

Una tarea de un proyecto muestra el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. **Proyecto**, en **Detalles**, permite cambiarlo o quitarlo. Consulta [Tareas de un proyecto](projects.md#a-project-s-to-dos).

**Área**, en **Detalles**, mueve una tarea a tu otra área. También cambia de área lo que puede leer y enviar. **Deshacer**, en la nota, la devuelve a su área anterior.

Cuando una tarea necesita tu otra área para continuar y todos los mensajes relacionados están allí, se mueve y continúa automáticamente. De lo contrario, muestra **Mover a Trabajo** y no se mueve hasta que lo toques. Una tarea que hayas añadido sin elegir Trabajo o Personal se mueve automáticamente cuando encuentra su área. Hasta entonces, no pertenece a Trabajo ni a Personal y sigue siendo privada.

Una tarea siempre puede leer los mensajes relacionados con ella. Si necesita otros mensajes de tu otra área, te lo pregunta con **Usar este correo para esta tarea**. Un buzón de trabajo que hayas marcado como Personal cuenta como Personal. Los correos de otras empresas tuyas van a las tareas de esa empresa, y una tarea sobre tu vida personal, como un familiar que escribe a tu dirección de trabajo, se considera Personal desde el principio.

El trabajo que recibes en una cuenta personal, como un cliente por WhatsApp o un pedido en tu buzón personal, se considera Trabajo desde el principio. Una tarea que hayas movido o asignado tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece una tarea y con quién se comparte, pero nunca desde dónde responde: la respuesta siempre se envía al mismo lugar que la conversación, incluso después de moverla, salvo que elijas otro medio.

Aun así, una tarea Personal responde desde la dirección de trabajo a la que llegó el correo y nunca aparece en una Fleet de Trabajo ni en el Graph del equipo.

Si hay dos o más tareas pendientes, **Repasar**, en el encabezado de Para ti, te permite recorrerlas de una en una en el orden de la lista, con cada borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el proceso. Debajo del título, el encabezado también indica cuánto tardarás si vas a tu ritmo, como «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen en el repaso: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba los mensajes cuando hay 40 pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, dentro de la hora.

Por la noche, desde las 00:00 hasta las 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se comprueban todos juntos a las 06:30, para que las tareas estén listas antes del resumen de la mañana. En Conexiones, la sección de comprobaciones indica «Pausadas por la noche, se ponen al día a las 06:30». Si abres la app, escribes en el chat o tocas una tarea por la noche, las comprobaciones vuelven a funcionar con normalidad hasta que lleves una hora sin actividad. **Revisar ahora** siempre inicia una comprobación de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no hay tareas abiertas, toca la línea de tu Machine para verla, con **Detalles**, que abre la sección de comprobaciones en Conexiones. Si hay tareas abiertas, en el ordenador aparece arriba. Una línea breve solo se muestra mientras se está realizando una comprobación, o si alguna ha fallado o se ha retrasado. También puedes preguntarlo en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, aparece una línea encima de tus tareas con lo que encontró en todas las fuentes que leyó, como «13 mensajes comprobados a las 16:11 · nada requiere tu atención» o «· 2 tareas nuevas». Si una tarea nueva espera a un momento más oportuno, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, junto con el icono de su fuente: quién escribió, el asunto o las primeras palabras, y la tarea nueva o el motivo por el que no hacía falta crear una, como «Solo estás en copia, un compañero está respondiendo» o «La reunión ya está programada para el jueves». Si la comprobación solo dio un motivo impreciso, el hilo no muestra ninguno. Toca un elemento para leerlo.

Se muestran los primeros 10 elementos. Toca debajo para ver el resto. Un número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Una notificación del teléfono sobre un mensaje que ya aparece en la lista solo se muestra una vez. La línea permanece durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus propias respuestas se leen para entender el contexto y las promesas, pero no cuentan como correo nuevo. Los correos que The Machine te envía, como el resumen de la mañana o un aviso de reparación, nunca se leen ni aparecen en la lista. El correo sobre facturación, tu periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, junto a **Posponer**. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué cambiar: cómo hacerlo o, cuando ya hay un borrador, qué cambiar en él. **Marcar como hecha** significa que ya está resuelta: aparece a la vista en una tarea preparada sin borrador; en los demás casos, está en la parte superior de **…**, incluso en una tarea que requiere tu decisión. La tarea desaparece de la lista de inmediato y aparece **Deshacer** en el mensaje. Desliza el mensaje o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Para que se haga de otra manera, explícalo en su **Chat**.

En **…**:

- **Pasar…**: asígnasela a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pídele a alguien que la revise](ask-to-review.md).
- **Repetir…**: [volverá a aparecer con cierta frecuencia](recurring.md).
- **No hace falta**: desaparece. Si quieres, elige el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre**, en **Detalles**, para cambiarle el nombre. El título que elijas se conserva.

**Reabrir** devuelve una tarea cerrada. También vuelve a aparecer automáticamente cuando ocurre algo nuevo, como recibir otro mensaje de esa persona, pero no cuando respondes tú.

Una factura que tengas que pagar personalmente, desde cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que incluye. Las facturas que se pagan automáticamente, como las domiciliadas o las que se cobran a una tarjeta registrada, no se convierten en tareas. Cuando un correo posterior confirma que se ha pagado, por ejemplo, el remitente confirma que recibió tu pago, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Una tarea que solo importa hasta una hora determinada, como una confirmación antes de una reunión, se cierra automáticamente cuando pasa esa hora. Se mueve a **Hecho / descartado** con el motivo «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de que un mensaje o un traspaso para alguien aparezca como listo, tu Machine revisa tus chats recientes con las personas involucradas, incluidos los chats grupales, y espera a que Slack los lea. Si un mensaje posterior indica que ya está hecho, por ejemplo, porque se lo pidieron y dijo que sí, la tarea se cierra automáticamente. **Deshacer** la recupera durante un día.

Cuando un mensaje nuevo cambia el plan, como cuando una fiesta cambia de lugar o se cancela una reserva, The Machine actualiza sus tareas automáticamente. Si una tarea sigue siendo necesaria, se ajusta al nuevo plan. Si ya no queda nada por hacer, se mueve a **Hecho / descartado** con el motivo «No hace falta». En su chat aparece «Actualizado:» junto con la explicación, y **Deshacer** la recupera durante un día.

En tus primeras tareas, aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas su botón o pulsas ×.

El primer día, la parte superior de Tareas te da la bienvenida y te indica quién lleva más tiempo esperando tu respuesta. Esa respuesta se prepara primero, para que esté lista cuando llegues.

Cada tarea empieza con su título. La línea de debajo indica de quién se trata, la organización si corresponde (no solo porque alguien trabaje allí), el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno; de lo contrario, muestran sus iniciales. Si un logotipo no se lee bien a ese tamaño, por ejemplo, si es blanco sobre fondo transparente o tiene un nombre ancho, también se muestran las iniciales.

A veces, una línea discreta indica qué no se sabe, como «Último contacto hace 12 días por correo; nada desde entonces». Aparece cuando la última comunicación con alguien es antigua o no ha recibido respuesta. También indica los canales que no están conectados, como WhatsApp. Tu Machine dice lo que no sabe en lugar de adivinar.

Si indica un canal que no está conectado, toca Conectar junto a él para abrir esa conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Una tarea hecha conserva su título y muestra debajo cómo terminó, como «Hecho: Sam lo firmó el martes».

Encima del borrador, una línea tenue indica de qué mensaje viene, junto con el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del destino para que veas enseguida si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que alguien dijo en otro lugar, como una sugerencia de un compañero en Slack, aparece una línea que lo indica, como «Basado en el mensaje de Sam en #ops». Tócala para leer el mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) se muestra como una sola conversación, empezando por los mensajes más antiguos: incluye los mensajes anteriores al que origina la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje de la tarea aparece marcado como «Esta tarea» y se abre en la conversación. **Mostrar mensajes anteriores** añade mensajes más antiguos. En un correo, el resto del hilo aparece plegado por encima y por debajo.

Los **Detalles** de un correo solo muestran lo que no aparece en el encabezado, como las direcciones completas en Cc, Bcc o una dirección distinta para responder. Si no hay nada que añadir, no aparece esta sección.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre, el proyecto y el área (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. **Chat ›** abre el chat. Las tareas hechas se muestran de forma resumida; el mensaje que las originó está en **Detalles**.

Una tarea con el estado «Esperando a» enlaza tu último mensaje a esa persona, que es el que estás esperando: «Correo para Pat · mar».

## Crear una tarea tú

**Nueva tarea** (debajo de **Buscar** en un ordenador, **+** en un teléfono o `N`) crea una tarea para lo que quieras. Al crearla, no se envía nada. Si no eliges **Trabajo** ni **Personal**, se asigna al área que corresponda según la persona y el asunto. También encuentra el correo al que da seguimiento, incluso si es antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «en 2 horas», también en tu idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Se repite**: vuelve a aparecer con cierta frecuencia. Consulta [Tareas periódicas](recurring.md).
- **Persona**: vincula hasta 5 personas o empresas relacionadas con la tarea.
- Icono de mensaje: adjunta el mensaje relacionado, como un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro mensaje que tenga The Machine. Busca por texto o por remitente. Cada resultado indica de dónde viene, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En un teléfono, puedes sacar una foto con la cámara que aparece junto al clip. Puedes añadir hasta 5 archivos, como en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Toca × para quitar un archivo.

Los archivos se quedan con la tarea y The Machine los lee mientras trabaja en ella. Puedes añadir solo archivos: completará la tarea a partir de un PDF o un archivo de texto. Las fotos se muestran como imágenes pequeñas. Tócalas para verlas a tamaño completo.
