---
title: Chat de tareas
area: cards
summary: Pregunta sobre una tarea o modifica su borrador en un chat asociado a esa tarea.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 64a15c6ce46c6679
---
## Ábrelo

En un móvil, toca el título de la tarea. En un ordenador, pulsa **Ver en el chat ›** o el enlace al chat de la tarea. Si haces clic en el título desde un ordenador, cambiarás el nombre de la tarea.

## Correos en el chat

Cada correo muestra solo las novedades. Los mensajes anteriores que cita aparecen plegados en **Mensajes anteriores**. **Leer el hilo** abre los correos completos.

## Qué ha hecho

Mientras trabaja en tu mensaje, el último paso aparece encima de los puntos de escritura, como «Leyendo el correo», igual que en la tarea mientras se prepara. Cuando usa el navegador, también aparece una pequeña imagen de la página.

Cada ejecución completada aparece en una sola línea discreta, como «Ha revisado 12 elementos». Ábrela para ver cada tipo de paso una vez, con el número de veces: «Ha usado el navegador en example.com · 7». Nombra el sitio, nunca la dirección, un comando o un archivo.

Cuando se detiene para preguntarte algo, la pregunta también aparece en una línea discreta, como «Ha preguntado: ¿Lo envío hoy o el lunes?». Debajo, tu mensaje muestra solo tu respuesta.

## Qué puedes preguntar

Antes de escribir, el chat puede ofrecerte hasta tres sugerencias basadas en esta tarea, como «Propón el martes a las 10:00». Al tocar una, aparece en el cuadro de mensaje, desde donde puedes enviarla o modificarla. Si no hay nada concreto que encaje, no se muestran sugerencias.

- Sobre el hilo, las personas o el contexto: «¿Qué pidieron la última vez?»
- Para cambiar el borrador: «Hazlo más corto» o «Menciona la nueva fecha».

Una pregunta recibe una respuesta y deja el borrador tal como está. Para enviar, usa los botones de la tarea: el chat nunca envía un borrador en la misma respuesta en la que lo ha escrito. Los cambios que pidas y que no afecten a nadie más, como limpiar un documento, se hacen de inmediato, sin pedir una confirmación adicional. Cualquier cosa que vaya más allá de lo que has pedido queda pendiente de tu visto bueno. Una tarea con más de un paso permanece abierta hasta que se completen todos.

En un ordenador, pulsa Enter o Ctrl+Enter (Cmd+Enter en un Mac) para enviar, y Shift+Enter para empezar una línea nueva. En un móvil, usa el botón de enviar.

## Si algo no está bien

Dilo en el chat, por ejemplo: «No es el director general» o «Dejó la empresa». The Machine lo corrige desde el origen: un cargo, una empresa, un título, la fase de un proyecto, el proyecto de la tarea o una regla que haya aprendido. El chat muestra qué ha cambiado, por ejemplo: «Corregido: Sam es responsable de ventas, según su firma de correo», junto con **Deshacer**. Al deshacer, se recupera el valor anterior, a menos que haya cambiado desde entonces.

Los otros borradores basados en el valor incorrecto se vuelven a redactar, uno a uno. En su chat aparece **Volviendo a redactar el borrador tras una corrección**. Los borradores que hayas editado o aprobado, y los que estén a punto de enviarse, no cambian. La respuesta indica cuántos hay de cada tipo.

En una página de GBrain, solo cambia la sección propia de The Machine. Lo que hayas escrito ahí se mantiene. Cuando no puede saber de dónde viene algo, aprende de tu nota en su lugar.

## Modelo y razonamiento

Debajo del cuadro de mensaje, el chat muestra el modelo y el nivel de razonamiento, como «GPT-6.2 Sol» y «Razonamiento bajo». Toca cualquiera para elegir otro solo para este chat. Los chats nuevos usan lo que hayas seleccionado en **Ajustes**, **Modelo** (consulta [Modelo](model.md)).

**Rápido**, al final del menú de modelos, hace que los chats de tareas respondan más deprisa, a aproximadamente el doble de coste (o gastando el doble de tu plan). Se aplica a los mensajes que envíes y a Hazlo, en todos tus chats de tareas, pero nunca al trabajo en segundo plano. Está desactivado de forma predeterminada y aparece atenuado en los modelos que no lo admiten.

## Detener una respuesta

Mientras se escribe una respuesta, el botón de enviar se convierte en **Detener**. Al detenerla, termina al instante y conserva lo que ha escrito hasta ese momento, marcado como **Detenida**. Escribe un mensaje nuevo para continuar o toca **Reintentar**.

## Añadir archivos

Toca el clip, pega una captura de pantalla o arrastra archivos al chat. Cada archivo aparece encima del cuadro de mensaje. Pulsa × para quitarlo. El mensaje puede contener solo archivos.

- Las imágenes (PNG, JPEG, GIF, WebP) de hasta 5 MB se envían al modelo como imágenes.
- Los PDF, archivos de texto, hojas de cálculo (CSV) y archivos de Office de hasta 10 MB: The Machine los lee y puede adjuntarlos a un borrador.
- Hasta 5 archivos por mensaje.

Los archivos se quedan en tu Machine, cifrados igual que tus mensajes. Los archivos que añadas pero no envíes se eliminan al cabo de un día. También puedes adjuntar archivos a una tarea nueva desde **Nueva tarea** (consulta [Crear una por tu cuenta](cards.md#make-one-yourself)).
