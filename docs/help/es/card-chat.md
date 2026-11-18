---
title: Chat de la tarea
area: cards
summary: Pregunta sobre una tarea o modifica su borrador en un chat que pertenece a esa tarea.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 340b9cfc0e3a424d
---
## Abrir el chat

En el teléfono, toca el título de la tarea. En el ordenador, haz clic en **Ver en el chat ›** o en el enlace al chat de la tarea. Si haces clic en el título en el ordenador, cambiarás el nombre de la tarea.

## Correos electrónicos en el chat

Cada correo muestra solo lo nuevo. Los mensajes anteriores que cita están plegados bajo **Mensajes anteriores**. **Leer el hilo** abre los correos completos.

## Qué hizo

Cada ejecución aparece en una sola línea discreta, como «Comprobó 12 cosas». Ábrela para ver cada tipo de paso una vez, junto con el número de veces que se hizo: «Usó el navegador en example.com · 7». Indica el sitio, nunca la dirección, un comando ni un archivo.

Cuando se detiene para preguntarte algo, la pregunta también aparece en una línea discreta, como «Preguntó: ¿Lo envío hoy o el lunes?». Debajo, tu mensaje muestra solo tu respuesta.

## Qué puedes preguntar

Antes de escribir, el chat puede ofrecerte hasta tres sugerencias basadas en esta tarea, como «Propón el martes a las 10:00 en su lugar». Al tocar una, aparece en el cuadro de mensaje para que la envíes o la modifiques. Si no hay ninguna sugerencia concreta adecuada, no aparece ninguna.

- Sobre el hilo, las personas o el contexto: «¿Qué pidieron la última vez?»
- Para cambiar el borrador: «Hazlo más corto» o «Menciona la nueva fecha».

Una pregunta obtiene una respuesta y no modifica el borrador. Para enviar, usa los botones de la tarea: el chat nunca envía un borrador en la misma respuesta en que lo redacta. Los cambios que pidas y que no lleguen a nadie más, como limpiar un documento, se hacen de inmediato, sin pedirte otra confirmación. Cualquier cosa que vaya más allá de lo que pediste espera a que la apruebes. Una tarea con más de un paso permanece abierta hasta que se completen todos.

En el ordenador, Enter o Ctrl+Enter (Cmd+Enter en un Mac) envía el mensaje y Shift+Enter crea una nueva línea. En el teléfono, usa el botón de envío.

## Si algo está mal

Dilo en el chat, por ejemplo: «No es el director ejecutivo» o «Dejó la empresa». The Machine corrige el dato en su origen: un cargo, una empresa, un título, la fase de un proyecto, el proyecto de la tarea o una regla que haya aprendido. El chat muestra qué cambió, por ejemplo: «Corregido: el cargo de Sam es responsable de ventas, según su firma de correo», con **Deshacer**. Al deshacer, se recupera el valor anterior, a menos que haya cambiado desde entonces.

Los demás borradores basados en el valor incorrecto se vuelven a redactar, de uno en uno. En sus chats aparece **Volviendo a redactar el borrador tras una corrección**. Los borradores que hayas editado o aprobado, y los que estén por enviarse, no cambian. La respuesta indica cuántos hay de cada tipo.

En una página de GBrain, solo cambia la sección de The Machine. Lo que hayas escrito ahí se conserva. Si no puede determinar de dónde viene algo, aprende de tu nota en su lugar.

## Modelo y razonamiento

Debajo del cuadro de mensaje, el chat muestra el modelo y el nivel de razonamiento, como «GPT-6.2 Sol» y «Razonamiento bajo». Toca cualquiera de los dos para elegir otro solo para este chat. Los chats nuevos usan lo que hayas elegido en **Ajustes**, **Modelo** (consulta [Modelo](model.md)).

**Rápido**, al final del menú de modelos, hace que los chats de tareas respondan más rápido, con un coste aproximadamente doble (o el doble de tu plan). Se aplica a los mensajes que envías y a **Hazlo**, en todos tus chats de tareas, nunca al trabajo en segundo plano. Está desactivado de forma predeterminada y aparece en gris si el modelo no lo admite.

## Detener una respuesta

Mientras se escribe una respuesta, el botón de envío se convierte en **Detener**. Al detenerla, termina de inmediato y conserva lo que había escrito hasta ese momento, marcado como **Detenida**. Escribe un mensaje nuevo para continuar o toca **Reintentar**.

## Añadir archivos

Toca el clip, pega una captura de pantalla o arrastra archivos al chat. Cada archivo aparece encima del cuadro de mensaje y × lo quita. El mensaje puede contener solo archivos.

- Las imágenes (PNG, JPEG, GIF, WebP) de hasta 5 MB se envían al modelo como imágenes.
- Los PDF, archivos de texto, hojas de cálculo (CSV) y archivos de Office de hasta 10 MB: The Machine los lee y puede adjuntarlos a un borrador.
- Hasta 5 archivos por mensaje.

Los archivos permanecen en tu Machine, cifrados como tus mensajes. Los archivos que añadas pero nunca envíes se eliminan al cabo de un día. También puedes adjuntar archivos a una tarea nueva desde **Nueva tarea** (consulta [Crear una tú mismo](cards.md#make-one-yourself)).
