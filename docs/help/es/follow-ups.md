---
title: Seguimientos
area: graph
summary: Haz seguimiento automáticamente si alguien no responde, en todo un tablero o en un proyecto. Te pregunta antes, salvo que le indiques lo contrario.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 76bea8f586963be1
---
Cuando una persona de un tablero deja de responder, tu Machine prepara el borrador del seguimiento por ti, con tu tono y en la misma conversación. Está desactivado hasta que lo actives. Si una de tus habilidades encaja con el tablero, los borradores la siguen, incluido el orden de la información en el correo.

## Activarlo

Pulsa **⋯** en un tablero y luego **Seguimientos…**. Marca **Hacer seguimiento si no hay respuesta**. Se aplica a todos los proyectos del tablero. También puedes pulsar **Seguimientos desactivados** debajo del nombre del tablero o **Hacerles seguimiento** en una etapa con proyectos que llevan más de 10 días sin respuesta.

Para un solo proyecto, pulsa **Seguimientos…** en **⋯**, en el tablero o en la página del proyecto. **Para este proyecto** permite elegir **Activado**, **Desactivado** o la configuración del tablero. La configuración del proyecto prevalece sobre la del tablero.

## Ajustes

- De forma predeterminada, espera de 3 a 7 días sin respuesta. El seguimiento se prepara tras el plazo más corto y se envía como máximo al cumplirse el más largo, incluso si tienes poco uso disponible.
- **Solo en días laborables**: no se preparan ni se envían seguimientos en tus días libres (según **Ajustes** > **Notificaciones** > **Horario laboral**). Lo que venza durante esos días espera hasta la mañana de tu próximo día laborable. Está activado para Trabajo y desactivado para Personal.
- De forma predeterminada, hace entre 1 y 3 seguimientos. Siempre envía el mínimo y prepara borradores para el resto. Si cree que es mejor parar, el borrador explica por qué ("The Machine se detendría aquí: 9 correos sin respuesta desde agosto") y no está marcado. Puedes enviarlo, omitirlo o elegir **Parar los seguimientos aquí**. Nunca supera el máximo.
- **Etapas**: **Todas las etapas abiertas**, es decir, no incluye la última etapa del tablero ni Estancado o rechazado. **Personalizar** permite activar o desactivar etapas y asignar un plazo propio a cada una.
- **Canales**: los canales conectados que permiten enviar mensajes. El seguimiento se envía por el mismo canal que el último mensaje. **Cambiar de canal si no hay respuesta** prueba el siguiente canal permitido.
- **Mover a Estancado o rechazado después del último**: se activa si el tablero tiene esa etapa.

## Preguntar antes o enviar automáticamente

**Pregúntame antes de enviar** es la opción predeterminada: los borradores esperan en tus tareas. **Enviar sin preguntar** da permiso permanente para ese tablero o proyecto. Cualquier caso inusual o error seguirá esperando tu revisión, y el nivel Prudente siempre pregunta. Un seguimiento nunca se envía dos veces. Los seguimientos no te avisan, ni mediante notificaciones push ni por correo: sus borradores esperan en tu lista y en el resumen de la mañana.

Justo antes de enviar un seguimiento, se vuelve a revisar el hilo. Si alguien escribió desde que se preparó el borrador, no se envía: "No se ha enviado: hay un mensaje nuevo en el hilo". La tarea muestra ese mensaje, quién lo escribió y cuándo, junto con **Leerla** y **Rehacer para este mensaje**, que pide un borrador nuevo que tenga en cuenta el mensaje.

## Revisar los seguimientos

Los seguimientos de un tablero aparecen en una sola tarea, nunca en una por correo. Mientras se preparan, aparece "Escribiendo 3 seguimientos…" y, al terminar, "8 seguimientos listos para Alpha testers".

**Revisar** los muestra uno debajo del otro y completos, para que puedas leerlos todos desplazándote por la lista. **Enviar**, **Editar** y **Omitir** aparecen en el seguimiento actual. Con el teclado, j y k (o las flechas) permiten moverse; Enter envía; e edita; s omite (y vuelve a pulsarla para deshacerlo); x marca o desmarca; y c pide cambios. **Enviar todos los marcados** envía los que sigan marcados.

Cada seguimiento incluye su borrador. Si no se puede escribir uno, se indica qué hace falta primero ("No hay borrador. Primero hace falta: saber a quién va dirigido") y no queda marcado. **Escríbelo** pide el borrador de todos modos. Si un borrador tiene más de un destinatario posible, aparece "Destinatario: elige al enviar" y **Enviar** te pide que elijas.

**Omitir** desmarca un borrador y lo mueve al final de la lista, donde aparece como omitido con la opción **Deshacer**. Se omite definitivamente al cerrar la revisión. Puedes recuperarlo con **Recuperar** en los seguimientos del proyecto o en su tarea, en Hecho, siempre que no haya llegado un seguimiento más reciente. El seguimiento de un solo proyecto es una tarea normal.

**Pedir cambios…** reescribe todos los borradores marcados o solo el actual, según lo que indiques. No se envía nada y **Deshacer cambio** recupera el texto anterior. Mientras el cuadro esté abierto o se esté reescribiendo un borrador, no se puede enviar nada. Además, cualquier borrador que haya cambiado vuelve a mostrarse antes de poder enviarlo.

Cuando se envían varios seguidos, incluso con la opción Enviar sin preguntar, cada buzón envía uno cada 30 a 45 segundos. La tarea muestra el progreso: "Enviando 3 de 8…". **Dejar de enviar** detiene el resto: el que ya esté en camino se envía, y los demás vuelven a la revisión como borradores para enviarlos más tarde ("Envío detenido. 1 enviado, 11 guardados como borradores").

## Correos enviados antes de que tu Machine leyera el buzón

También cuentan los correos que enviaste desde otra aplicación antes de que tu Machine leyera ese buzón. Lee la conversación (o, si no puede, los correos anteriores citados en tu último mensaje). Así, tres correos sin respuesta cuentan como tres, y el plazo de «Sin respuesta desde» empieza con el primero. Si ya alcanzaste el máximo, no prepara otro borrador.

## Cuándo se detienen

Los seguimientos se detienen cuando la otra persona responde, cuando el proyecto se gana, se pierde, se archiva o se mueve a una etapa cerrada, y cuando pospones u omites uno. Antes de preparar un borrador, tu Machine revisa si hay algo más reciente en la conversación, para no insistirle a alguien que ya respondió por otro medio.

Un seguimiento también se cierra si alguien ya volvió a escribir en esa misma conversación. El seguimiento de otro proyecto nunca cuenta. Si tu Machine cree que no hace falta enviar uno por otro motivo, la tarea permanece abierta y explica por qué. Tú decides.

**Pausar** en **Seguimientos…** deja en pausa un tablero o proyecto sin desactivar los seguimientos: no se preparan ni se envían, no termina ninguna ronda y las tareas de seguimiento abiertas siguen abiertas. Elige el día en que se reanudarán o pulsa **Reanudar** cuando quieras. El plazo continúa desde donde se quedó y lo que ya vencía se envía de uno en uno. Mientras tanto, aparece **En pausa**.

Después del último seguimiento sin respuesta, el proyecto muestra "Sin respuesta después de 3 seguimientos" y pasa a Estancado o rechazado si esa opción está activada. Si se detiene antes de enviar alguno, muestra "Seguimientos detenidos" y permanece en su etapa.

Si el correo rebota y la persona tiene otra dirección, el seguimiento se envía allí ("Rebotó, ahora se enviará a <address>"). Si la dirección de un borrador rebota antes de enviarlo, el borrador queda en espera: "No se ha enviado: <address> ha rebotado". Se cambia a la otra dirección de esa persona y queda a la espera de que pulses Enviar.

Si no hay otra dirección, los seguimientos pasan a LinkedIn o WhatsApp cuando esté permitido y tengas una conversación por ese canal. De lo contrario, se detienen con el mensaje "El correo ha rebotado". Si el proyecto es importante, se crea una tarea para buscar una dirección nueva.

## Dónde verlo

El encabezado del tablero dice "Seguimientos activados, próximo: jue.". En el tablero, cada proyecto muestra el próximo seguimiento o indica que ya está listo. La página del proyecto enumera los seguimientos enviados, incluidos los que se enviaron automáticamente.

Los seguimientos esperan mientras tu Machine está ocupada o cerca del límite de uso, y se ponen al día más tarde. En un tablero compartido, solo la Machine de la persona propietaria del proyecto hace el seguimiento.
