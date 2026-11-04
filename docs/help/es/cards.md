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
- **Vuelve más tarde**: pospuesta.
- **Promesas**: lo que prometiste y lo que otros te prometieron. Consulta [Promesas](promises.md).
- **Hecho / descartado**: cada tarea terminada, las más recientes primero, de 30 en 30 según te desplazas. Las tareas que ya parecen terminadas van primero, con la etiqueta **Parece hecho**.

Una tarea con **Parece hecho** se ve como una hecha, con lo que muestra que está hecha, como "PR #3451 fusionado". Aún no está cerrada: **Reabrir** la devuelve a tu lista, y tu Machine aprende de ello. Nunca aparecen como atrasadas ni cuentan como pendientes de ti.

Una tarea cuyo último paso sigue abierto en manos de otra persona, como una revisión, una fusión o una respuesta, muestra **Esperando:** ese paso y sigue abierta. Espera en **Esperando a otros**, plegada encima de Vuelve más tarde, y no cuenta como lista para ti. Un mensaje nuevo sobre ella la trae de vuelta.

**Todo al día.** significa que ahora nada te necesita. La línea de abajo dice cuándo tu Machine revisó por última vez.

**Todo**, **Trabajo** y **Personal**, encima de la lista en la barra lateral, muestran todas las tareas o solo un tipo. Tu Machine guarda la elección, así que tu teléfono y tu ordenador muestran la misma lista. Mientras Trabajo o Personal está activo, la parte de arriba de la lista lo indica, con **Mostrar todo** para volver.

Una tarea de un proyecto muestra el nombre del proyecto en la línea bajo su título; abre el proyecto. **Proyecto** en **Detalles** lo cambia o lo quita. Consulta [las tareas de un proyecto](graph.md#a-projects-to-dos).

**Área** en **Detalles** pasa la tarea a tu otra área, como una personal que tiene que salir desde tu dirección del trabajo. Lo que puede leer y desde dónde puede enviar cambia con ella; los mensajes de los que vino se quedan donde están. **Deshacer** en el aviso que sigue la devuelve.

Cuando una tarea necesita otra área para seguir, lo pide con un botón **Mover a Trabajo**. Nada se mueve hasta que lo tocas; después sigue sola.

Cuando inicias una tarea, siempre puede leer los mensajes de los que vino, también en el buzón de otra empresa. Si necesita otros mensajes de otra área, lo pide con **Usar este correo para esta tarea**; un toque los añade y sigue. El correo para otra de tus empresas va desde el principio a las tareas de esa empresa.

## Los botones

Una tarea muestra su siguiente paso, como **Hazlo** o **Revisar y enviar**, con **Posponer** al lado. Consulta [Hazlo](do-it.md) y [Posponer](snooze.md). Una tarea lista también tiene **Pedir cambios** (di qué cambiar en el borrador y lo rehace). **Marcar como hecha** (ya está resuelta) también está: a la vista sin borrador, si no, arriba en **…**.

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

**Detalles** muestra su nombre, proyecto y área (toca uno para cambiarlo), el mensaje del que viene (tócalo para leer el hilo), tu última nota y el resultado de un agente de código. **Chat ›** al final de esa línea abre el chat. Una tarea hecha se queda corta: su título, una línea y lo que se envió.

Una tarea "Esperando a" (alguien te prometió algo) enlaza tu último mensaje a esa persona, el que espera respuesta: "Email a Pat · mar".

## Crea una tú

**Nueva tarea** (debajo de **Buscar** en un ordenador) añade una tarea para lo que sea. Crearla no envía nada.

- **Vence**: escribe un día o una hora, como "mañana", "el viernes que viene", "3 nov", "15:00", "2pm", "en 2 horas" o "mañana 9". También entiende otros idiomas ("over 2 uur", "morgen 9u"). El icono del calendario tiene opciones rápidas, como al posponer, y **Elegir fecha**.
- **Correo**: adjunta el correo del que trata. Solo busca en tu correo, por asunto o remitente.
- **Archivos**: toca el clip en el cuadro, pega una captura de pantalla o suelta archivos en el formulario. En un teléfono también puedes hacer una foto. Hasta 5 archivos, de los mismos tipos y tamaños que en el chat (consulta [Añade archivos](card-chat.md#add-files)). × quita uno.

Los archivos se quedan con la tarea: se ven en ella y en su chat, y The Machine los lee cuando trabaja en ella.
