---
title: Seguimientos
area: graph
summary: Haz seguimiento automáticamente cuando alguien no responda, en todo un tablero o en un proyecto. Te pregunta antes, salvo que le indiques lo contrario.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 0e7bdfb2c9b2deb5
---
Cuando alguien deja de responder en un tablero, tu Machine redacta el seguimiento por ti, con tu estilo y en la misma conversación. Está desactivado hasta que lo actives. Si una de tus habilidades encaja con el tablero, los borradores la siguen, incluido el orden del contenido del correo.

## Activarlo

Pulsa **⋯** en un tablero y luego **Seguimientos…**. Marca **Hacer seguimiento si no hay respuesta**. Se aplica a todos los proyectos de ese tablero. También puedes pulsar **Seguimientos desactivados** debajo del nombre del tablero o **Hacerles seguimiento** en una etapa con proyectos que llevan 10 días o más sin respuesta.

Para un solo proyecto, pulsa **Seguimientos…** en **⋯**, ya sea en el tablero o en su página. **Para este proyecto** te permite elegir **Activado**, **Desactivada** o el ajuste del tablero. El ajuste propio de un proyecto tiene prioridad sobre el del tablero.

## Ajustes

- De forma predeterminada, espera de 3 a 7 días sin respuesta. El seguimiento se redacta una vez transcurrido el plazo más corto y se envía antes de que termine el más largo, incluso si estás cerca del límite de uso.
- **Solo en días laborables**: no se redacta ni se envía nada en tus días libres (según **Ajustes** > **Notificaciones** > **Horario laboral**). Lo que venza entonces esperará hasta la mañana de tu próximo día laborable. Está activado para Trabajo y desactivado para Personal.
- De forma predeterminada, hace de 1 a 3 seguimientos. Siempre envía el mínimo y redacta los demás. Si cree que es mejor parar, el borrador explica por qué ("The Machine pararía aquí: 9 correos sin respuesta desde agosto") y no está marcado. Puedes enviarlo, omitirlo o elegir **Parar los seguimientos aquí**. Nunca superará el máximo.
- **Etapas**: **Todas las etapas abiertas**, es decir, todas menos la última etapa del tablero y Estancado o rechazado. **Personalizar** te permite activar o desactivar etapas y definir un tiempo de espera para cada una.
- **Canales**: los canales conectados que permiten enviar mensajes. El seguimiento se envía por el mismo canal que el último mensaje. **Cambiar de canal si no hay respuesta** prueba el siguiente canal permitido.
- **Mover a Estancado o rechazado después del último**: está activado si el tablero tiene esa fila.

## Preguntar antes de enviar o enviar automáticamente

**Pregúntame antes de enviar** es la opción predeterminada: los borradores esperan en tus tareas. **Enviar sin preguntar** es un permiso permanente para ese tablero o proyecto. Si algo falla o es inusual, seguirá esperando tu aprobación, y el nivel Cauteloso siempre pregunta. Un seguimiento nunca se envía dos veces. Los seguimientos nunca te avisan mediante notificaciones push o correo: los borradores esperan en tu lista y en el resumen de la mañana.

Justo antes de enviar uno, se vuelve a comprobar el hilo. Si alguien escribió después de que se redactara el borrador, no se envía: "No se ha enviado: hay un mensaje nuevo en el hilo". La tarea muestra el mensaje, quién lo escribió y cuándo, con **Leerla** y **Rehacer para este mensaje**. Esta última opción pide un borrador nuevo que tenga en cuenta el mensaje.

## Revisarlos

Los seguimientos de un tablero aparecen en una sola tarea, nunca en una por correo. Mientras se redactan, dice "Redactando 3 seguimientos…" y, cuando están listos, "8 seguimientos listos para probadores de Alpha".

**Revisar** los muestra uno debajo de otro, completos, para que puedas leerlos todos al desplazarte. **Enviar**, **Editar** y **Omitir** aparecen en el seguimiento actual. Con el teclado, j y k (o las flechas) te permiten moverte; Enter lo envía, e lo edita, s lo omite (y vuelve a pulsarlo para deshacer), x marca o desmarca, y c permite hacer cambios. **Enviar todos los marcados** envía los que sigan marcados.

Cada seguimiento incluye su borrador. Si no se puede redactar, indica qué hace falta primero ("No hay borrador. Primero hace falta: saber a quién va dirigido") y no aparece marcado. **Escríbelo** pide que se redacte de todos modos. Si un borrador tiene varios destinatarios posibles, dice "Destinatario: elige uno al enviar" y, al pulsar **Enviar**, te pide que elijas.

**Omitir** desmarca un borrador y lo mueve al final. Aparece como Omitido, con la opción **Deshacer**. Se omite definitivamente al cerrar la revisión. Puedes recuperarlo con **Recuperar** en los seguimientos del proyecto o en su tarea de Hecho, siempre que no haya llegado un seguimiento más reciente. El seguimiento de un solo proyecto es una tarea normal.

**Pedir cambios…** reescribe todos los borradores marcados, o solo el actual, según lo que indiques. No se envía nada y **Deshacer cambio** recupera el texto anterior. Mientras el cuadro esté abierto o se esté reescribiendo un borrador, no se puede enviar nada. Además, cualquier borrador que haya cambiado vuelve a mostrarse antes de poder enviarse.

Si se envían varios seguidos, incluso con Enviar sin preguntar, cada buzón envía uno cada 30 a 45 segundos. La tarea indica el progreso: "Enviando 3 de 8…". **Dejar de enviar** detiene los demás. Si ya hay uno en camino, se envía; los demás vuelven a la revisión como borradores para enviarlos más tarde ("Se detuvo el envío. 1 enviado, 11 guardados como borradores").

## Correos enviados antes de que tu Machine los leyera

También se tienen en cuenta los correos que enviaste desde otra aplicación antes de que tu Machine leyera ese buzón. Lee la conversación (o, si no puede, los correos anteriores citados en el último mensaje que enviaste). Así, tres correos sin respuesta cuentan como tres, y el plazo de «Sin respuesta durante» empieza desde el primero. Si ya alcanzaste el máximo, no redacta otro.

## Cuándo se detienen

Los seguimientos se detienen cuando responden, cuando el proyecto se gana, se pierde, se archiva o pasa a una etapa cerrada, y cuando pospones u omites uno. Antes de redactar, tu Machine comprueba si hay algo nuevo en la conversación para no insistirle a alguien que ya respondió por otro canal.

**Pausar** en **Seguimientos…** suspende los seguimientos de un tablero o proyecto sin desactivarlos: no se redacta ni se envía nada, no termina ninguna ronda y las tareas de seguimiento abiertas siguen abiertas. Elige un día para reanudarlos o pulsa **Reanudar** cuando quieras. El tiempo de espera continúa desde donde quedó y lo que ya vencía se procesa de uno en uno. Mientras tanto, aparece **En pausa**.

Después del último seguimiento sin respuesta, el proyecto muestra "Sin respuesta después de 3 seguimientos" y pasa a Estancado o rechazado si esa opción está activada. Si se detuvo antes de enviar alguno, muestra "Seguimientos detenidos" y permanece en su etapa.

Si el correo rebotó y la persona tiene otra dirección, el seguimiento se envía allí ("Correo rebotado. Ahora se enviará a <address>"). Si el correo de un borrador rebota antes de enviarlo, se retiene: "No se ha enviado: <address> ha rebotado". Se cambia a la otra dirección de esa persona y queda a la espera de que pulses Enviar.

Si no hay otra dirección, los seguimientos pasan a LinkedIn o WhatsApp cuando esté permitido y converses por ahí. De lo contrario, se detienen y muestran "El correo ha rebotado". Si el proyecto es importante, recibirás una tarea para buscar una dirección nueva.

## Dónde verlo

El encabezado del tablero indica "Seguimientos activados, el próximo jue". En el tablero, cada proyecto muestra su próximo seguimiento o que ya está listo. En la página del proyecto aparece una lista de los seguimientos enviados, incluidos los enviados automáticamente.

Los seguimientos esperan si tu Machine está ocupada o cerca del límite de uso, y se ponen al día más tarde. En un tablero compartido, solo la Machine de quien sea propietario del proyecto hace el seguimiento.
