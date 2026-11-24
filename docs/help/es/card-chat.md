---
title: Chat de tareas
area: cards
summary: Pregunta sobre una tarea o cambia su borrador en un chat que pertenece a esa tarea.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 224f6163a84e80ca
---
## Ábrelo

Pulsa **Chat** en la tarea o selecciónala en la lista de la barra lateral. Toca o haz clic en el título para editarlo.

## Correos en el chat

Cada correo muestra solo lo nuevo. Los mensajes anteriores que cita aparecen plegados bajo **Mensajes anteriores**. **Leer el hilo** abre los correos completos.

## Qué ha hecho

Mientras trabaja en tu mensaje, su último paso aparece encima de los puntos de escritura, como «Leyendo el correo», igual que en la tarea mientras se prepara. Cuando usa el navegador, también aparece una imagen pequeña de la página.

Cada ejecución terminada aparece en una sola línea discreta, como «Ha comprobado 12 cosas». Ábrela para ver una vez cada tipo de paso, con la cantidad de veces que se ha repetido: «Ha usado el navegador en example.com · 7». Indica el sitio, nunca la dirección, un comando o un archivo.

Si se detiene para preguntarte algo, la pregunta también aparece en una línea discreta, como «Ha preguntado: ¿Lo envío hoy o el lunes?», y debajo, tu mensaje muestra solo tu respuesta.

## Qué preguntar

Antes de escribir, el chat puede ofrecerte hasta tres opciones basadas en esta tarea, como «Propón el martes a las 10:00». Al tocar una, aparece en el cuadro de mensaje para que la envíes o la cambies. Si no hay ninguna opción concreta que encaje, no se muestra ninguna.

- Sobre el hilo, las personas o el contexto: «¿Qué pidieron la última vez?»
- Para cambiar el borrador: «Acórtalo» o «Menciona la nueva fecha».

Si haces una pregunta, recibes una respuesta y el borrador no cambia. Para enviar, usa los botones de la tarea: el chat nunca envía un borrador en la misma respuesta en la que lo ha redactado. Los cambios que pidas y que no lleguen a nadie más, como corregir un documento, se hacen enseguida, sin pedirte una confirmación adicional. Cualquier cosa que vaya más allá de lo que has pedido espera a que des tu visto bueno. Una tarea con más de un paso permanece abierta hasta que se completen todos.

En un ordenador, pulsa Intro o Ctrl+Intro (Cmd+Intro en un Mac) para enviar, y Mayús+Intro para empezar una línea nueva. En un móvil, usa el botón de envío.

## Si algo está mal

Dilo en el chat, por ejemplo: «No es el director general» o «Ya no trabaja en la empresa». The Machine lo corrige en el origen: un cargo, una empresa, un título, la fase de un proyecto, el proyecto de la tarea o una regla que haya aprendido. El chat muestra qué ha cambiado, como «Corregido: el cargo de Sam es director de ventas, según su firma de correo», junto con **Deshacer**. Deshacer restaura el valor anterior, salvo que haya cambiado desde entonces.

Se vuelven a redactar, una por una, las demás versiones basadas en el valor incorrecto. En su chat aparece **Rehaciendo el borrador tras una corrección**. Los borradores que hayas editado o aprobado, y los que estén a punto de enviarse, no cambian. La respuesta indica cuántos hay de cada tipo.

En una página de GBrain, solo cambia la sección de The Machine. Lo que hayas escrito ahí se mantiene. Si no puede saber de dónde viene algo, lo aprende de tu nota.

## Modelo y razonamiento

Debajo del cuadro de mensaje, el chat muestra el modelo y su nivel de razonamiento, como «GPT-6.2 Sol» y «Razonamiento bajo». Toca cualquiera de los dos para elegir otro solo para este chat. Los chats nuevos usan lo que hayas configurado en **Ajustes**, **Modelo** (consulta [Modelo](model.md)).

**Rápido**, al final del menú de modelos, hace que los chats de tareas respondan más deprisa, por aproximadamente el doble de coste (o el doble de tu plan). Se aplica a los mensajes que envías y a **Hazlo**, en todos tus chats de tareas, nunca al trabajo en segundo plano. Está desactivado de forma predeterminada y aparece atenuado si el modelo no lo admite.

## Detener una respuesta

Mientras se escribe una respuesta, el botón de envío cambia a **Detener**. Al detenerla, se termina enseguida y se conserva lo que se haya escrito hasta ese momento, marcado como **Detenida**. Escribe un mensaje nuevo para continuar o toca **Reintentar**.

## Añadir archivos

Toca el clip, pega una captura de pantalla o arrastra archivos al chat. Cada archivo aparece encima del cuadro de mensaje. Pulsa × para quitarlo. Puedes enviar un mensaje que solo contenga archivos.

- Las imágenes (PNG, JPEG, GIF, WebP) de hasta 5 MB se envían al modelo como imágenes.
- The Machine lee los PDF, archivos de texto, hojas de cálculo (CSV) y archivos de Office de hasta 10 MB, y puede adjuntarlos a un borrador.
- Puedes adjuntar hasta 5 archivos por mensaje.

Los archivos se quedan en tu Machine, cifrados igual que tus mensajes. Los archivos que añadas pero no envíes se eliminan al cabo de un día. También puedes adjuntar archivos a una tarea nueva desde **Nueva tarea** (consulta [Crea una tú](cards.md#make-one-yourself)).
