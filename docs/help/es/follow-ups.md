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

**⋯** en un tablero, luego **Seguimientos…**, y marca **Hacer seguimiento si no hay respuesta**. Se aplica a todos los proyectos de ese tablero.

Para un solo proyecto, **Seguimientos…** en el **⋯** de su tarjeta o en su página. **Para este proyecto** elige **Activado**, **Desactivada** o el ajuste del tablero. El ajuste propio de un proyecto manda sobre el del tablero.

## Ajustes

- Espera de 3 a 7 días sin respuesta. Tras la espera más corta se redacta un seguimiento. La más larga es lo más tarde que sale, aunque tu uso vaya justo.
- Haz seguimiento al menos 1 vez y como máximo 3. El mínimo siempre se envía. Entre ambos, lee la conversación y el proyecto y solo hace seguimiento si todavía tiene sentido. Nunca más del máximo.
- **Etapas**: **Todas las etapas abiertas**, o sea, ni la última etapa del tablero ni Estancado o rechazado. **Personalizar** activa o desactiva etapas y le da a una etapa su propia espera.
- **Canales**: los conectados que pueden enviar. Un seguimiento sale por el mismo canal que el último mensaje. **Cambiar de canal si no hay respuesta** prueba el siguiente permitido.
- **Mover a Estancado o rechazado después del último**: activado si el tablero tiene esa fila.

## Preguntar o enviar sola

**Pregúntame antes de enviar** es lo predeterminado: los borradores esperan en tus tareas. **Enviar sin preguntar** es un sí permanente para ese tablero o proyecto. Lo inusual te sigue esperando, igual que lo que falla. Con el modo Prudente activado, siempre pregunta. Un seguimiento nunca sale dos veces.

## Revisarlos

Los seguimientos de un tablero llegan como una sola tarea: “8 seguimientos listos para Alpha testers”. **Revisar** los muestra uno debajo de otro, cada uno con **Enviar**, **Editar** y **Omitir**. Con teclado, j y k (o las flechas) para moverte, Enter envía, e edita y s omite. **Enviar todos los marcados** envía los que siguen marcados. El seguimiento de un solo proyecto es una tarea normal.

## Cuándo se detienen

Los seguimientos se detienen cuando la persona responde, cuando el proyecto se gana, se pierde, se archiva o pasa a una etapa cerrada, y cuando pospones u omites uno. Antes de redactar, tu Machine busca algo más reciente en la conversación, para no insistir a quien ya respondió por otro lado.

Tras el último seguimiento sin respuesta, el proyecto muestra “Sin respuesta tras 3 seguimientos” y pasa a Estancado o rechazado si eso está activado.

## Dónde lo ves

La cabecera del tablero dice “Seguimientos activados, el próximo el jue”. La tarjeta de un proyecto muestra su próximo seguimiento, o que hay uno listo. La página del proyecto lista lo que se envió, también lo enviado automáticamente.

Los seguimientos esperan mientras tu Machine está ocupada con tus tareas o cerca de su límite de uso, y se ponen al día después. En un tablero compartido, solo la Machine del propietario del proyecto hace seguimiento.
