---
title: Tareas
area: cards
summary: Una tarea por cada cosa que requiere tu atención, lista para que des tu visto bueno. Qué significa cada parte de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
Tu Machine lee todo lo nuevo y crea una tarea solo cuando algo requiere tu atención. Una tarea por asunto, sin importar cuántos mensajes incluya.

## Dónde están las tareas

La página **Tareas** las agrupa así:

- **Para ti**: todo lo que espera por ti, empezando por lo más urgente. Cada tarea indica **Preparada** (el trabajo está hecho y **Hazlo** o **Enviar** lo lleva a cabo), **Te necesita** (primero necesita que tomes una decisión o respondas) o **Preparando…** (tu Machine está trabajando en ella).
- **Recién hecho**: un último paso que confirmaste, como un formulario o una incidencia, se completó mientras no estabas. Se queda ahí hasta que toques **Entendido**, como máximo un día, y también recibirás un aviso en el teléfono.
- **Vuelve más tarde**: tareas pospuestas y tareas sin respuesta a **¿Aún hace falta?** (más abajo).
- **Promesas**: lo que prometiste y lo que otras personas te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: todas las tareas completadas, de la más reciente a la más antigua, con la hora de finalización, como «Hecha hace 5 minutos». Las tareas que parecen haberse completado ya aparecen marcadas como **Parece hecho**.

Después de enviar algo, una nota breve indica dónde quedó la tarea, como «Enviado. Movida a Hecho» o «Enviado. Movida a Más tarde hasta el lun». **Abrir** te lleva a la tarea. La búsqueda permite encontrar una tarea por su título o por la persona a quien se envió, también en Más tarde y Hecho.

**Para ti** muestra primero lo que está vencido o vence mañana o antes, después las preguntas de tu Fleet y, por último, el resto. Dentro de cada grupo, primero aparece lo más reciente. Una tarea mantiene su lugar mientras tu Machine la prepara y cuando se completa: solo cambia su estado. En los demás grupos abiertos, primero aparece lo vencido o lo que vence mañana o antes, y luego el resto, empezando por lo más reciente. La barra lateral mantiene el mismo orden.

**Parece hecho** significa que tu Machine ve que ya está hecho, como «PR #3451 combinado», pero aún no se ha cerrado. **Reabrir** lo devuelve a tu lista y tu Machine aprende de ello. Estas tareas nunca aparecen como atrasadas. Al cabo de un día, se cierran solas y aparece **Deshacer**. Una tarea que ya resolviste por tu cuenta, por ejemplo, al responder en Gmail o Slack, también se cierra sola.

Si un mensaje viene de una dirección que se parece a la de alguien que conoces, como sam@acme-corp.example en lugar de sam@acmecorp.example, la tarea lo indica claramente: «Esta persona no es Sam Lee». Muestra a esa persona con su propia dirección, nunca con el nombre que usó. Tu Machine comprueba estos mensajes con la persona cuya dirección ya tienes, nunca con quien los escribió.

Una tarea que aún espera a otra persona, como una revisión o una respuesta, indica el paso pendiente con **Esperando a:**. Se queda en **Esperando a otros**, contraído encima de Vuelve más tarde, hasta que un mensaje nuevo la reactive. Lo mismo ocurre después de que hayas respondido con una pregunta: vuelve la mañana anterior a la fecha límite, en la fecha límite si es más tarde ese mismo día, o a la mañana siguiente si ya pasó, e indica a quién sigue esperando.

Cuando una tarea depende de un resultado que debe entregar otra persona, como un contrato firmado, en **Detalles** aparece como **Hecho cuando**. Enviar tu parte no la cierra: se queda en **Esperando a otros** hasta que un mensaje confirme el resultado y entonces se cierra sola. Aparece **Deshacer**. Si no llega nada para cuando toque insistir, vuelve a aparecer con **Escribe un recordatorio breve** en su chat. Dile en el chat qué cuenta como hecho para cambiarlo.

Si nadie toca una tarea durante una semana, pregunta una vez: **¿Aún hace falta?** **No hace falta** la cierra. Aparece **Deshacer**. **Mantener** la conserva y no vuelve a preguntar. Si no respondes durante otra semana, se contrae en Vuelve más tarde y deja de contar en el número del icono de la app y en el resumen de la mañana. Si la abres, escribes en el chat, la editas, la pospones o llega un mensaje nuevo, vuelve a aparecer.

Una vez por semana, un proyecto que lleva tiempo inactivo y no tiene tareas abiertas puede generar una tarea con un siguiente paso concreto, hasta tres por semana. Consulta [Proyectos](projects.md).

Cuando nada requiere tu atención, tu Machine descansa y la lista queda vacía. Mientras comprueba si hay novedades, se activa y te lo indica. Si una comprobación falla o se retrasa, lo indica en su línea y muestra **Revisar ahora**.

Las opciones **Todo**, **Trabajo** y **Personal**, en la parte superior de la barra lateral, muestran todas las tareas o solo las de un tipo. El teléfono y el ordenador muestran la misma selección. Si tienes activado Trabajo o Personal, **Mostrar todo** vuelve a la vista completa. Una alerta sobre tu Machine, como una pieza que se reinicia sin parar, no es de Trabajo ni Personal y solo aparece en Todo.

La línea de la parte superior de la lista también cambia directamente a la otra vista: **Solo personal · Trabajo · Mostrar todo**.

La fila superior de la lista muestra el nombre de tu último resumen de la mañana o de la tarde y lo que cuenta, como **Resumen de ayer por la tarde** · 12 hechas, 3 abiertas. Tócala para volver a leer ese resumen. Usa **Copiar** para copiarlo y pegarlo donde quieras. Cuando lo abras o toques su **×**, estará disponible en todos tus dispositivos hasta el siguiente resumen.

Si no hay un resumen reciente, aparece **Hoy hasta ahora**: lo que se ha hecho hoy y lo que sigue pendiente, tanto en Trabajo como en Personal o solo en el área que hayas seleccionado.

Una tarea de un proyecto muestra el nombre del proyecto debajo del título. Tócalo para abrir el proyecto. En **Detalles**, **Proyecto** te permite cambiarlo o quitarlo. Consulta [las tareas de un proyecto](projects.md#a-projects-to-dos).

En **Detalles**, **Área** mueve una tarea a la otra área. También se mueve el acceso a los mensajes que puede leer y enviar. **Deshacer** en la nota la devuelve a su área anterior.

Si una tarea necesita la otra área para continuar y todos los mensajes de los que procede están allí, se mueve sola y sigue adelante. Si no, aparece **Mover a Trabajo** y no se mueve hasta que lo toques. Una tarea que añadiste sin elegir Trabajo o Personal se mueve sola cuando encuentra dónde corresponde. Hasta entonces, no aparece en Trabajo ni en Personal y se mantiene privada.

Una tarea siempre puede leer los mensajes de los que procede. Si necesita otros mensajes de tu otra área, te pregunta con **Usar este correo para esta tarea**. Un buzón de trabajo que marcaste como Personal cuenta como Personal. El correo de otras empresas tuyas se asigna a las tareas de esa empresa. Una tarea sobre tu vida personal, como un familiar que escribe a tu dirección de trabajo, se considera Personal desde el principio.

El trabajo que te llega a una cuenta personal, como un cliente por WhatsApp o un pedido en tu buzón personal, se considera Trabajo desde el principio. Una tarea que moviste o asignaste tú siempre se queda donde la pusiste. Trabajo o Personal determina dónde aparece la tarea y con quién se comparte, nunca dónde responde: la respuesta siempre se envía en la conversación correspondiente, incluso después de moverla, salvo que elijas otra opción.

Una tarea Personal de este tipo sigue respondiendo desde la dirección de trabajo a la que llegó el correo y nunca aparece en un Fleet de Trabajo ni en el Graph del equipo.

Si hay dos o más tareas pendientes, **Repasar** en el encabezado de Para ti te permite revisarlas una por una, en el orden de la lista, con cada borrador completo y las opciones **Enviar** o **Hazlo**, **Pedir cambios**, **Posponer** y **Omitir**. En un ordenador, Enter envía lo que aparece en pantalla, `S` pospone, `→` omite y Esc detiene el repaso. Debajo del título, el encabezado también indica cuánto tiempo te llevará a tu ritmo, como «unos 2 min».

Las tareas que te hacen una pregunta no se incluyen en ninguna de las dos opciones: necesitan tu respuesta, no que toques un botón.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche. Comprueba lo que ha llegado cuando hay 40 mensajes pendientes o cuando el mensaje más antiguo de una persona lleva 15 minutos esperando. Los boletines, las notificaciones y los recibos se incluyen en la siguiente comprobación, dentro de una hora.

Por la noche, de 00:00 a 06:30, las comprobaciones se pausan: los mensajes nuevos se siguen leyendo y guardando, y se revisan juntos a las 06:30 para que tus tareas estén listas antes del resumen de la mañana. En Comprobaciones, dentro de Conexiones, aparece «Pausadas por la noche; se ponen al día a las 06:30». Si abres la app, escribes en el chat o tocas una tarea durante la noche, las comprobaciones vuelven a funcionar con normalidad hasta que lleves una hora sin usarla. **Revisar ahora** siempre inicia una comprobación de inmediato.

**Revisar ahora** lee todas las fuentes de inmediato. Si no tienes tareas abiertas, toca la línea de tu Machine para verla, con **Detalles**, que abre Comprobaciones en Conexiones. Si tienes tareas abiertas, aparece arriba en el ordenador. Solo se muestra una línea breve mientras se ejecuta una comprobación, o cuando una ha fallado o se ha retrasado. También puedes preguntarle en el chat.

LinkedIn, X y Salesflare tienen su propio ritmo.

## Última comprobación

Después de una comprobación que haya leído mensajes nuevos, una línea encima de tus tareas indica qué encontró en todas las fuentes que leyó, como «13 mensajes comprobados a las 16:11 · nada requiere tu atención» o «· 2 tareas nuevas». Si una tarea nueva espera a un momento más oportuno, como el resumen de la mañana, indica hasta cuándo: «1 tarea aplazada hasta mañana a las 08:30».

Toca la línea para ver cada hilo de correo, chat y notificación, con el icono de su fuente: quién escribió, el asunto o las primeras palabras y la tarea nueva o el motivo por el que no hacía falta ninguna, como «Solo estabas en copia; un compañero está respondiendo» o «La reunión ya está programada para el jueves». Si la comprobación dio un motivo impreciso, el hilo no muestra ningún motivo. Tócalo para leerlo.

Se muestran los primeros 10. Toca debajo para ver el resto. Un número después de un nombre, como (3), indica cuántos mensajes nuevos tiene ese chat. Una notificación del teléfono sobre un mensaje que ya aparece en la lista solo se muestra una vez. La línea permanece visible durante 12 horas después de la comprobación.

Solo cuenta el correo que recibes. Tus respuestas se leen para tener contexto y registrar promesas, pero no cuentan como correo nuevo. Los correos de The Machine para ti, como el resumen de la mañana o un aviso de reparación, nunca se leen ni aparecen en la lista. El correo sobre la facturación, tu periodo de prueba o una invitación se lee con normalidad.

## Los botones

Una tarea muestra el siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

**Pedir cambios** indica qué cambiar: cómo hacerlo o, cuando el borrador esté listo, qué cambiar en él. **Marcar como hecha** indica que ya está resuelta. En una tarea preparada sin borrador, aparece directamente; en los demás casos, está en la parte superior de **…**, también en las tareas que requieren que tomes una decisión. La tarea se quita de la lista de inmediato y aparece **Deshacer** en el mensaje. Desliza el mensaje para quitarlo o arrástralo fuera con el ratón para cerrarlo antes. El cambio se conserva.

Para que se haga de otra manera, díselo en su **Chat**.

En **…**:

- **Pasar…**: asígnala a un compañero, a [Claude Code o Codex](hand-to-agent.md), o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve a aparecer de forma periódica](recurring.md).
- **No hace falta**: la quita de la lista. Si quieres, indica el motivo: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título o **Nombre** en **Detalles** para cambiarle el nombre. El título que elijas se conserva.

**Reabrir** devuelve a la lista una tarea cerrada. También vuelve a aparecer sola cuando pasa algo nuevo, como un mensaje nuevo de esa persona, pero no cuando respondes tú.

Una factura que todavía tienes que pagar tú, de cualquier país, se convierte en una tarea con el importe, la fecha de vencimiento y los datos de pago que aparecen en la factura. Las facturas que se pagan automáticamente, como un débito directo o una tarjeta registrada, no se convierten en tareas. Si un correo posterior indica que se pagó, por ejemplo, si quien la envió confirma que recibió el pago, la tarea se cierra sola. **Deshacer** la recupera durante un día.

Una tarea que solo era relevante hasta una hora determinada, como una confirmación antes de una reunión, se cierra sola cuando pasa esa hora. Se mueve a **Hecho / descartado** con el motivo «Ya no hace falta». **Deshacer** la recupera durante un día.

Antes de que un mensaje o un traspaso para otra persona aparezca como listo, tu Machine comprueba los chats recientes con las personas implicadas, incluidos los chats grupales, y espera a que Slack los lea. Si un mensaje posterior muestra que ya está hecho, como que se lo pidieron y aceptó, la tarea se cierra sola. **Deshacer** la recupera durante un día.

Cuando un mensaje nuevo cambia el plan, como una fiesta que se traslada a otro sitio o una reserva que se cancela, The Machine actualiza sus tareas por su cuenta. Si una tarea sigue siendo necesaria, se ajusta al nuevo plan. Si ya no queda nada por hacer, se mueve a **Hecho / descartado** con el motivo «No hace falta». En su chat aparece «Actualizado:» con el motivo y **Deshacer** la recupera durante un día.

En tus primeras tareas aparece un consejo breve con las acciones principales: **Pedir cambios** y **No hace falta**, y te recuerda que no se envía nada hasta que pulses **Enviar**. El consejo desaparece para siempre cuando usas el botón correspondiente o pulsas ×.

El primer día, la parte superior de Tareas te da la bienvenida e indica quién lleva más tiempo esperando tu respuesta. Primero se prepara un borrador de esa respuesta para que esté listo cuando llegues.

Cada tarea empieza con el título. La línea de debajo indica de quién se trata, la organización si corresponde (nunca solo porque alguien trabaje allí), el proyecto, Trabajo o Personal y cuándo llegó. Toca un nombre para abrir su página en Graph.

Los nombres y las organizaciones muestran su foto o logotipo si Graph tiene uno y, si no, sus iniciales. Si un logotipo no se ve bien en tamaño pequeño, como uno blanco con fondo transparente o una palabra ancha, también se muestran las iniciales.

A veces aparece una línea discreta para indicar qué se desconoce, como «Último contacto por correo hace 12 días; no ha habido novedades». Se muestra cuando el último contacto con esa persona fue hace tiempo o sigue sin respuesta, e indica los canales que no están conectados, como WhatsApp. Tu Machine te dice lo que no sabe en lugar de adivinar.

Si menciona un canal que no está conectado, **Conectar**, junto a ese canal, abre la conexión.

El título indica qué hay que hacer y solo cambia si eso cambia. Una tarea hecha conserva el título y muestra debajo cómo se completó, como «Hecha: Sam lo firmó el martes».

Encima del borrador, una línea tenue indica el mensaje del que procede, con el logotipo del servicio. Tócala para leer el hilo. El borrador muestra el logotipo del destino para que veas de inmediato si es una respuesta de Slack o un correo.

Si el borrador se basa en lo que alguien dijo en otro lugar, como la sugerencia de un compañero en Slack, una línea lo indica, como «Basado en un mensaje de Sam en #ops». Tócala para leer ese mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) se muestra como una conversación, de más antiguo a más reciente: los mensajes anteriores al que dio lugar a la tarea y las respuestas posteriores. En WhatsApp, Telegram o Signal, tus mensajes aparecen a la derecha, como en la app. El mensaje relacionado con la tarea está marcado como «Esta tarea» y se abre en la vista. **Mostrar mensajes anteriores** añade mensajes más antiguos. Los demás mensajes del hilo de un correo aparecen contraídos encima y debajo del mensaje correspondiente.

En **Detalles**, un correo solo muestra la información que no aparece en su encabezado, como las direcciones completas en Cc, Bcc o una dirección de respuesta distinta. Si no hay nada más que mostrar, no aparece esta sección.

Una respuesta en un hilo de Slack también muestra lo que se dijo antes de que empezara el hilo. El enlace de una tarea a su propio mensaje también lo abre aquí, con **Abrir en Slack** en la parte inferior.

**Detalles** muestra el nombre, el proyecto y el área (toca uno para cambiarlo), tu última nota y el resultado de un agente de programación. **Chat ›** abre el chat. Una tarea hecha ocupa menos espacio; el mensaje del que procede está en **Detalles**.

Una tarea que está «Esperando a» incluye un enlace a tu último mensaje para esa persona, el que estás esperando: «Correo para Pat · mar».

## Crea una tarea

**Nueva tarea** (debajo de **Buscar** en un ordenador) añade una tarea para lo que necesites. Crear una tarea no envía nada. Si no eliges Trabajo ni Personal, se asigna donde corresponde según la persona y el asunto. También encuentra el correo al que da seguimiento, aunque sea antiguo.

- **Vence**: escribe un día o una hora, como «mañana», «el próximo vie», «3 nov», «14:00» o «en 2 horas». También puedes escribirlo en tu idioma. El icono del calendario ofrece opciones rápidas y **Elegir fecha**.
- **Mensaje**: adjunta el mensaje relacionado: un correo, un mensaje de Slack, Teams, WhatsApp, Telegram o cualquier otro que tenga The Machine. Busca por texto o por remitente. Cada resultado indica de dónde viene, quién lo envió y cuándo.
- **Archivos**: toca el clip, pega una captura de pantalla o arrastra archivos al formulario. En el teléfono, la cámara que aparece al lado sirve para tomar una foto. Puedes añadir hasta 5 archivos, como en el chat (consulta [Añadir archivos](card-chat.md#add-files)). Toca × para quitar un archivo.

Los archivos se guardan con la tarea y The Machine los lee cuando trabaja en ella. No hace falta añadir nada más: puede completar la tarea a partir de un PDF o un archivo de texto. Las fotos aparecen como imágenes pequeñas. Tócalas para verlas en tamaño completo.
