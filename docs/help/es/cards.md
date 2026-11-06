---
title: Tareas
area: cards
summary: Una tarea por cada cosa que te necesita, lista para tu sí. Qué significan las partes de una tarea.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
---
Tu Machine lee todo lo nuevo y solo crea una tarea cuando algo te necesita. Una tarea por asunto, por muchos mensajes que abarque.

## Dónde están las tareas

La página **Tareas** las agrupa:

- **Lista para ti**: preparada y esperando tu aprobación.
- **Necesita tu decisión**: algo que solo tú puedes decidir.
- **Preparando**: tu Machine está trabajando en ella. Una tarea a la que acabas de decir **Hazlo** se queda donde estaba mientras se prepara, y luego pasa a **Lista para ti**.
- **Recién hecho**: un último paso que confirmaste, como enviar un formulario o crear un issue, salió bien mientras no estabas. Muestra lo que pasó hasta que tocas **Entendido**, un día como mucho, y tu teléfono también se entera. Después solo está en Hecho.
- **Vuelve más tarde**: pospuesta, y las tareas sin respuesta a **¿Aún hace falta?** (abajo).
- **Promesas**: lo que prometiste y lo que otros te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: cada tarea terminada, por cuándo se terminó, las más recientes primero, de 30 en 30 según te desplazas. Una tarea que acabas de enviar está arriba, y cada una dice cuándo, como «Hecho hace 5 minutos». Las tareas que ya parecen terminadas van entre ellas según cuándo empezaron a parecerlo, con la etiqueta **Parece hecho**.

Después de enviar, una nota breve dice dónde está la tarea, como «Enviado. Movido a Hecho.» o, si espera una respuesta, «Enviado. Movido a Más tarde hasta el lun.» **Abrir** te lleva a ella. Que el hilo salga de tu bandeja de entrada unos días solo afecta a tu correo. La búsqueda encuentra una tarea por su título o por a quién se envió, también en Más tarde y Hecho.

En Lista para ti, Necesita tu decisión, Preparando y Esperando a otros, una tarea vencida o que vence a más tardar mañana va primero. Las demás van de la más reciente a la más antigua, según la hora que muestra cada tarea. La barra lateral sigue el mismo orden.

Una tarea con **Parece hecho** se ve como una hecha, con lo que muestra que está hecha, como "PR #3451 fusionado". Aún no está cerrada: **Reabrir** la devuelve a tu lista, y tu Machine aprende de ello. Nunca aparecen como atrasadas ni cuentan como pendientes de ti.

Una tarea cuyo último paso sigue abierto en manos de otra persona, como una revisión, una fusión o una respuesta, muestra **Esperando:** ese paso y sigue abierta. Espera en **Esperando a otros**, plegada encima de Vuelve más tarde, y no cuenta como lista para ti. Un mensaje nuevo sobre ella la trae de vuelta.

Una tarea que nadie tocó en una semana pregunta una vez: **¿Aún hace falta?** **Descartar** la cierra como **No hace falta**, con **Deshacer**. **Mantener** la mantiene, y no vuelve a preguntar. Abrirla, un mensaje en el chat, un cambio, posponerla o un mensaje nuevo sobre ella cuentan como tocarla. Si no hay respuesta en otra semana, se guarda en Vuelve más tarde, bajo ¿Aún hace falta?, en lugar de desaparecer. Tocarla la trae de vuelta.

**Todo al día.** significa que ahora nada te necesita. La línea de abajo dice cuándo tu Machine revisó por última vez.

**Todo**, **Trabajo** y **Personal**, encima de la lista en la barra lateral, muestran todas las tareas o solo un tipo. Tu Machine guarda la elección, así que tu teléfono y tu ordenador muestran la misma lista. Mientras Trabajo o Personal está activo, la parte de arriba de la lista lo indica, con **Mostrar todo** para volver.

Una tarea de un proyecto muestra el nombre del proyecto en la línea bajo su título; abre el proyecto. **Proyecto** en **Detalles** lo cambia o lo quita. Consulta [las tareas de un proyecto](graph.md#a-projects-to-dos).

**Área** en **Detalles** pasa la tarea a tu otra área, como una personal que tiene que salir desde tu dirección del trabajo. Lo que puede leer y desde dónde puede enviar cambia con ella; los mensajes de los que vino se quedan donde están. **Deshacer** en el aviso que sigue la devuelve.

Cuando una tarea necesita otra área para seguir, lo pide con un botón **Mover a Trabajo**. Nada se mueve hasta que lo tocas; después sigue sola. Una tarea que añadiste sin elegir Trabajo o Personal se mueve sola en cuanto sabe dónde va.

Cuando inicias una tarea, siempre puede leer los mensajes de los que vino, también en el buzón de otra empresa. Si necesita otros mensajes de otra área, lo pide con **Usar este correo para esta tarea**; un toque los añade y sigue. El correo para otra de tus empresas va desde el principio a las tareas de esa empresa. Una tarea de tu propia vida, como tu familia escribiendo a tu dirección del trabajo, es Personal desde el principio.

## Revisar ahora

Tu Machine lee cada fuente cada pocos minutos, de día y de noche, y revisa lo que llegó en busca de tareas en cuanto hay 40 mensajes esperando o el mensaje más antiguo lleva 15 minutos esperando.

**Revisar ahora**, arriba en Tareas, lee al momento cada fuente y revisa lo que llegó, también cuando todo está en calma. Al lado, una línea dice cuándo revisó por última vez, cuándo toca la próxima revisión y cuántos mensajes esperan. Pulsarlo otra vez mientras revisa muestra la misma revisión. La app del móvil también lo tiene. En el chat, pídele que revise ahora.

LinkedIn, X y Salesflare siguen su propio ritmo.

## Los botones

Una tarea muestra su siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md).

Sin preparar, tiene **Cambiar el enfoque** (di cómo hacerla en su lugar); lista, **Pedir cambios** (di qué cambiar en el borrador). Si la fila no cabe en el móvil, **Posponer** pasa a **…**. **Marcar como hecha** (ya está resuelta) también está: a la vista sin borrador, si no, arriba en **…**.

Para que se haga de otra forma, dilo en su **Chat**.

En **…** (en el teléfono se abre desde abajo de la pantalla):

- **Pasar…**: pásala a un compañero, a [Claude Code o Codex](hand-to-agent.md) (los que has configurado) o [pide a alguien que la revise](ask-to-review.md).
- **Repetir…**: [vuelve con un ritmo](recurring.md).
- **No hace falta**: desaparece. Si quieres, elige por qué: **No es relevante**, **Datos incorrectos** o **Ya resuelto**. Tu Machine aprende de ello.

Toca el título, o **Nombre** en **Detalles**, para renombrarla. Tu título se queda, también cuando la tarea cambia.

Una tarea cerrada puede volver con **Reabrir**. También vuelve sola cuando pasa algo nuevo, como un mensaje nuevo de esa persona. Tu propia respuesta no la hace volver.

Una tarea que solo importaba hasta un momento concreto, como una confirmación antes de una reunión, se cierra sola cuando ese momento pasa. Pasa a las hechas con "Ya no hace falta" y cuándo fue. **Deshacer** la recupera durante un día.

En tus primeras tareas, una línea corta bajo los botones muestra lo esencial: **Cambiar el enfoque** (o **Pedir cambios**) y **No hace falta** cuando una tarea no es del todo así, y en tu primer borrador listo, que no sale nada hasta que pulsas **Enviar**. Un consejo desaparece para siempre en cuanto usas su botón o pulsas ×, en todos tus dispositivos.

En tu primer día, la parte de arriba de Tareas te saluda por tu nombre y muestra quién lleva más tiempo esperando tu respuesta. The Machine redacta esa respuesta primero, para que esté lista cuando llegues. No sale nada hasta que la envías. La línea desaparece después de tu primer día o de tu primera tarea decidida.

Cada tarea empieza por su título. La línea de debajo dice de quién trata, su organización, el proyecto, Trabajo o Personal (en **Todo**) y cuándo llegó, además de cómo va cuando su grupo no lo dice ya. Toca un nombre para abrir su página en el Graph.

A veces una línea discreta bajo el texto dice lo que no se sabe, como «Último contacto hace 12 días por correo; nada desde entonces.» Solo aparece cuando el último contacto es antiguo o sigue sin respuesta, y nombra los canales no conectados por los que quizá respondieron, como WhatsApp. Tu Machine prepara con los mismos datos, así que dice lo que no sabe en vez de adivinar.

Un título dice qué hay que hacer. Solo cambia cuando eso cambia, como con una nueva petición. Una tarea hecha conserva su título, con debajo cómo terminó, como lo que se envió o "Hecho: Sam lo firmó el martes".

Sobre el borrador, una línea discreta nombra el mensaje del que viene, con el logo del servicio (Gmail, Slack, WhatsApp…). Tócala para leer el hilo. El borrador empieza con el logo de adónde va, así ves si es una respuesta en Slack o un correo antes de leer. Un paso sin borrador, como un traspaso, muestra el logo en su botón.

Cuando el borrador sigue lo que otra persona dijo en otro mensaje, como la sugerencia de un compañero en Slack, una línea bajo la tarea lo indica, como "Según Sam en #ops". Tócala para abrir ese mensaje.

Un chat (Slack, WhatsApp, Telegram, Intercom…) se lee como una sola conversación, del más antiguo al más nuevo, cada mensaje una vez; el mensaje del que trata la tarea tiene una línea fina al lado.

**Detalles** muestra su nombre, proyecto y área (toca uno para cambiarlo), tu última nota y el resultado de un agente de código. **Chat ›** al final de esa línea abre el chat. Una tarea hecha se queda corta: su título, una línea y lo que se envió; el mensaje del que viene está en sus **Detalles**.

Una tarea "Esperando a" (alguien te prometió algo) enlaza tu último mensaje a esa persona, el que espera respuesta: "Email a Pat · mar".

## Crea una tú

**Nueva tarea** (debajo de **Buscar** en un ordenador) añade una tarea para lo que sea. Crearla no envía nada. Sin elegir Trabajo o Personal, va donde corresponde: según de quién y de qué trata, una empresa o buzón que nombra, o el correo al que da seguimiento. Si nada lo indica, empieza donde están la mayoría de tus tareas. The Machine busca ese correo en tu buzón, también correos más antiguos que aún no ha traído.

- **Vence**: escribe un día o una hora, como "mañana", "el viernes que viene", "3 nov", "15:00", "2pm", "en 2 horas" o "mañana 9". También entiende otros idiomas ("over 2 uur", "morgen 9u"). El icono del calendario tiene opciones rápidas, como al posponer, y **Elegir fecha**.
- **Correo**: adjunta el correo del que trata. Solo busca en tu correo, por asunto o remitente.
- **Archivos**: toca el clip en el cuadro, pega una captura de pantalla o suelta archivos en el formulario. En un teléfono también puedes hacer una foto. Hasta 5 archivos, de los mismos tipos y tamaños que en el chat (consulta [Añade archivos](card-chat.md#add-files)). × quita uno.

Los archivos se quedan con la tarea: se ven en ella y en su chat, y The Machine los lee cuando trabaja en ella. Basta con archivos: The Machine lee el texto de un PDF o de un archivo de texto y completa la tarea con él.
