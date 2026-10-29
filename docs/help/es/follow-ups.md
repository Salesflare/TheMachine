---
title: Seguimientos
area: graph
summary: Hace seguimiento sola cuando alguien no responde, para todo un tablero o un solo proyecto. Pregunta antes, salvo que digas lo contrario.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 4
---
Cuando alguien de un tablero deja de responder, tu Machine redacta el seguimiento por ti, con tu estilo y en la misma conversación. Desactivado hasta que lo actives.

## Activarlo

**⋯** en un tablero, luego **Seguimientos…**, y marca **Hacer seguimiento si no hay respuesta**. Se aplica a todos los proyectos de ese tablero. O toca **Seguimientos desactivados** bajo el nombre del tablero, o **Hacerles seguimiento** en una etapa con proyectos sin respuesta desde hace más de 10 días.

Para un solo proyecto, **Seguimientos…** en el **⋯** de su tarjeta o en su página. **Para este proyecto** elige **Activado**, **Desactivada** o el ajuste del tablero. El ajuste propio de un proyecto manda sobre el del tablero.

## Ajustes

- Espera de 3 a 7 días sin respuesta. Tras la espera más corta se redacta un seguimiento. La más larga es lo más tarde que sale, aunque tu uso vaya justo.
- Haz seguimiento al menos 1 vez y como máximo 3. El mínimo siempre se envía. Entre ambos, lee la conversación y el proyecto y solo hace seguimiento si todavía tiene sentido. Nunca más del máximo.
- **Etapas**: **Todas las etapas abiertas**, o sea, ni la última etapa del tablero ni Estancado o rechazado. **Personalizar** activa o desactiva etapas y le da a una etapa su propia espera.
- **Canales**: los conectados que pueden enviar. Un seguimiento sale por el mismo canal que el último mensaje. **Cambiar de canal si no hay respuesta** prueba el siguiente permitido.
- **Mover a Estancado o rechazado después del último**: activado si el tablero tiene esa fila.

## Preguntar o enviar sola

**Pregúntame antes de enviar** es lo predeterminado: los borradores esperan en tus tareas. **Enviar sin preguntar** es un sí permanente para ese tablero o proyecto. Lo inusual te sigue esperando, igual que lo que falla. Con el modo Prudente activado, siempre pregunta. Un seguimiento nunca sale dos veces.

Justo antes de enviarlo se revisa el hilo otra vez, y si alguien escribió desde el borrador, no sale: «No enviado: hay un mensaje nuevo en el hilo».

## Revisarlos

Los seguimientos de un tablero llegan como una sola tarea, nunca una por correo. Mientras se redactan dice “Escribiendo 3 seguimientos…” y luego “8 seguimientos listos para Alpha testers”.

**Revisar** los muestra completos, uno debajo de otro, así que los lees todos de un vistazo. **Enviar**, **Editar** y **Omitir** aparecen en el actual. Con teclado, j y k (o las flechas) para moverte, Enter envía, e edita, s omite y c cambia. **Enviar todos los marcados** envía los que siguen marcados. El seguimiento de un solo proyecto es una tarea normal.

**Cambiar…** reescribe todos los borradores marcados, o solo el actual, como digas; no se envía nada y **Deshacer cambio** recupera el texto anterior.

Cuando salen varios seguidos, también con Enviar sin preguntar, cada buzón envía uno cada 30 a 45 segundos y la tarea muestra cómo va: “Enviando 3 de 8…”.

## Correos enviados antes de tu Machine

Los correos que enviaste desde otra app, antes de que tu Machine leyera ese buzón, también cuentan. Lee la conversación (o, si no puede, los correos anteriores citados en tu último), así que tres correos sin respuesta cuentan como tres, y “Sin respuesta desde hace” cuenta desde el primero. Si ya llegaste al máximo, no redacta otro.

## Cuándo se detienen

Los seguimientos se detienen cuando la persona responde, cuando el proyecto se gana, se pierde, se archiva o pasa a una etapa cerrada, y cuando pospones u omites uno. Antes de redactar, tu Machine busca algo más reciente en la conversación, para no insistir a quien ya respondió por otro lado.

Tras el último seguimiento sin respuesta, el proyecto muestra “Sin respuesta tras 3 seguimientos” y pasa a Estancado o rechazado si eso está activado.

Si su email rebotó, los seguimientos pasan a LinkedIn o WhatsApp cuando está permitido y habláis allí. Si no, se detienen con "El email rebotó". Cuando el proyecto importa, recibes un to-do para encontrar una dirección nueva.

## Dónde lo ves

La cabecera del tablero dice “Seguimientos activados, el próximo el jue”. La tarjeta de un proyecto muestra su próximo seguimiento, o que hay uno listo. La página del proyecto lista lo que se envió, también lo enviado automáticamente.

Los seguimientos esperan mientras tu Machine está ocupada con tus tareas o cerca de su límite de uso, y se ponen al día después. En un tablero compartido, solo la Machine del propietario del proyecto hace seguimiento.
