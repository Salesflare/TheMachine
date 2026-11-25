---
title: Chat de tareas
area: cards
summary: Pregunta sobre una tarea o modifica su borrador en el chat asociado a esa tarea.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 18a428fbe38a70e7
---
## Ábrelo

Pulsa **Chat** en la tarea o selecciónala en la lista de la barra lateral. Al pulsar o hacer clic en el título, puedes editarlo.

## Correos en el chat

Cada correo muestra solo lo nuevo. Los mensajes anteriores que cita aparecen plegados bajo **Mensajes anteriores**. **Leer el hilo** abre los correos completos.

## Qué ha hecho

Mientras trabaja, aparece **Trabajando en ello…** encima del cuadro de mensaje y unos puntos de escritura en el chat. Cuando usa el navegador, también aparece una pequeña imagen de la página.

Lo que hace en cada ejecución aparece en una sola línea discreta con un contador, como «Comprobó 12 cosas». Ábrela para ver una vez cada tipo de paso, junto con el número de veces que lo hizo: «Usó el navegador en example.com · 7». Indica el sitio, nunca la dirección, un comando ni un archivo.

Con Claude Code, los pasos no aparecen en el chat mientras trabaja. En su lugar, el paso más reciente aparece sobre los puntos de escritura, como «Leyendo el correo», y no aparece nada encima del cuadro de mensaje.

Si se detiene para preguntarte algo, la pregunta también aparece en una línea discreta, como «Preguntó: ¿Lo envío hoy o el lunes?». Debajo, tu mensaje solo muestra tu respuesta.

## Qué puedes pedir

Antes de escribir, el chat puede ofrecerte hasta tres sugerencias basadas en esta tarea, como «Propón el martes a las 10:00 en su lugar». Al pulsar una, se añade al cuadro de mensaje para que la envíes o la modifiques. Si no hay ninguna sugerencia adecuada, no aparece ninguna.

- Sobre el hilo, las personas o el contexto: «¿Qué pidieron la última vez?»
- Para cambiar el borrador: «Hazlo más corto» o «Menciona la nueva fecha».

Una pregunta recibe respuesta y no modifica el borrador. Para enviar, usa los botones de la tarea: el chat nunca envía un borrador en la misma respuesta en que lo redacta. Los cambios que pidas y que no lleguen a nadie más, como corregir un documento, se hacen al momento, sin pedirte confirmación. Cualquier cosa que vaya más allá de lo que pediste espera tu visto bueno. Una tarea con más de un paso permanece abierta hasta que se completen todos.

En un ordenador, Enter o Ctrl+Enter (Cmd+Enter en un Mac) envía el mensaje, y Shift+Enter crea una nueva línea. En un móvil, usa el botón de enviar.

## Si algo está mal

Dilo en el chat, por ejemplo: «No es el director general» o «Dejó la empresa». The Machine lo corrige en origen: un puesto, una empresa, un título, la fase de un proyecto, el proyecto de la tarea o una regla que aprendió. El chat muestra qué ha cambiado, como «Corregido: el puesto de Sam es Head of Sales, según su firma de correo», junto con **Deshacer**. Al deshacer, se recupera el valor anterior, salvo que haya cambiado desde entonces.

Los demás borradores basados en el valor incorrecto se vuelven a generar, de uno en uno. Su chat muestra **Volviendo a crear el borrador tras una corrección**. Los borradores que hayas editado o aprobado, y los que estén a punto de enviarse, se quedan como están. La respuesta indica cuántos hay de cada tipo.

En una página de GBrain, solo cambia la sección propia de The Machine. Lo que escribas allí se mantiene. Cuando no puede saber de dónde procede algo, aprende de tu nota en su lugar.

## Modelo y razonamiento

Debajo del cuadro de mensaje, el chat muestra el modelo y el nivel de razonamiento, como «GPT-6.2 Sol» y «Razonamiento bajo». Pulsa cualquiera de los dos para elegir otro solo para este chat. Los chats nuevos usan lo que hayas seleccionado en **Ajustes**, **Modelo** (consulta [Modelo](model.md)).

**Rápido**, al final del menú de modelos, hace que los chats de tareas respondan más deprisa, por aproximadamente el doble de coste (o el doble de tu plan). Se aplica a los mensajes que envías y a **Hazlo**, en todos tus chats de tareas, pero nunca al trabajo en segundo plano. Está desactivado de forma predeterminada y aparece en gris si el modelo no lo admite.

## Detener una respuesta

Mientras se escribe una respuesta, el botón de enviar se convierte en **Detener**. Al detenerla, se para al instante y se conserva lo que haya escrito hasta ese momento, marcado como **Detenida**. Escribe un mensaje nuevo para continuar o pulsa **Reintentar**.

## Añadir archivos

Pulsa el clip, pega una captura de pantalla o arrastra archivos al chat. Cada archivo aparece encima del cuadro de mensaje y puedes quitarlo con ×. El mensaje puede contener solo archivos.

- Las imágenes (PNG, JPEG, GIF, WebP) de hasta 5 MB se envían al modelo como imágenes.
- Los PDF, los archivos de texto, las hojas de cálculo (CSV) y los archivos de Office de hasta 10 MB: The Machine los lee y puede adjuntarlos a un borrador.
- Hasta 5 archivos por mensaje.

Los archivos permanecen en tu Machine, cifrados igual que tus mensajes. Los archivos que añadas pero no envíes se eliminan al cabo de un día. Una tarea nueva también puede incluir archivos, desde **Nueva tarea** (consulta [Crea una tú](cards.md#make-one-yourself)).
