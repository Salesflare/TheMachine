---
title: Rutinas
area: cards
summary: Trabajo que tu Machine hace sola, con un ritmo, como un resumen del lunes de tus deals abiertos. Solo lee.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, dashboard/routines-page.js
order: 10
keywords: routine, automation, scheduled, every week, every morning, report, suggested, digest, newsletter
---
## Crear una

Abre **Rutinas** en la barra lateral y di en una línea qué debe hacer y cuándo: "cada lunes a las 9, resume mis deals abiertos" o "cada día laborable por la mañana, lista los correos que aún debo responder". Luego **Añadir**.

Sin hora, se ejecuta a las 8:00. La hora es la del reloj de tu Machine.

## Qué hace una rutina

A su hora, tu Machine lee lo que necesita, como tus mensajes, reuniones y el Graph, y deja el resultado en la página Rutinas. Cada resultado dice **Para revisar**, **Nada nuevo** (con el porqué) o **No funcionó** (con el porqué). Una ejecución que termina sin resultado cuenta como fallida, nunca como hecha.

Las rutinas solo leen: tus mensajes, páginas web, GitHub y sitios como X en el navegador. No envían, responden, publican ni cambian nada.

Cuando la tarea de una rutina termina en una publicación o un mensaje, hace todo hasta ese paso y muestra el borrador, como **Publicaría en X:**. Tras una ejecución real lo recibes como tarea para aprobar; una ejecución de prueba solo lo muestra.

Cada ejecución conoce el último resultado, así puede decir qué cambió desde entonces.

Después de una buena ejecución, tu Machine puede escribirse una receta para la lectura que es igual cada vez, como qué correos o cambios de GitHub mirar. Las siguientes ejecuciones leen eso primero, con código simple, y la IA solo elige lo que importa y lo escribe, con menos tokens. Una receta solo lee; si deja de funcionar, la ejecución lee por sí misma y la arregla. Aparece en **Avanzado: pasos de script** en el menú ⋯.

## Días perdidos

Si tu Machine estaba apagada u ocupada, las ejecuciones perdidas no se acumulan: solo corre la más reciente, una vez. Cada fecha corre una vez, incluso tras un reinicio.

Las rutinas corren de una en una y esperan cuando el uso de tu plan de IA está bajo, como todo el trabajo en segundo plano. **Ejecutar ahora** la ejecuta enseguida.

## Cambiarla o detenerla

Está en el menú ⋯ de la rutina. **Cambiar cuándo** toma un nuevo ritmo en tus propias palabras, como "cada día laborable a las 8". **Pausar** detiene las ejecuciones hasta **Reanudar**; lo perdido durante la pausa no corre después. **Detener** termina una rutina para siempre.

## Avanzado: pasos de script

Nunca necesitas un script: di con tus propias palabras qué debe hacer una rutina.

Para usuarios avanzados, una rutina también puede ejecutar tus propios comandos en tu Machine: en el menú ⋯, elige **Avanzado: pasos de script**. **Editar** solo los muestra si una rutina ya tiene. **Obtener datos** ejecuta primero un comando, en su carpeta (vacía: tu carpeta personal) y como mucho durante sus segundos. Lo que imprime va a la ejecución para trabajar con ello. Sin palabras, lo que imprime es el resultado.

**Comprobación** recibe el resultado como entrada después de la ejecución. Si termina con un error, la ejecución muestra **No funcionó** con lo que dijo la comprobación. Un comando de Obtener datos que falla se muestra igual.

Un comando es una línea y corre sin shell: sin pipes ni variables. Los pasos de script son tuyos, solo se configuran en tu panel. Una ejecución de prueba y **Probarlo** también ejecutan Obtener datos y lo dicen; siguen sin enviar ni guardar nada. Una rutina nunca envía, así que un paso de script solo debería leer.

## Desde tus trabajos de OpenClaw

Si antes creaste trabajos programados en OpenClaw, tu Machine los lee (nunca los cambia) y ofrece los que encajan como rutinas en **Sugerido**. Cada uno se ejecutó una vez, para que veas un resultado real.

Mantiene tus correcciones al trabajo y deja fuera lo que enviaba o publicaba. Un trabajo que ejecutaba un script, o leía lo que recogía un trabajo de script, lo trae como Obtener datos. **Añadir** lo convierte en rutina, **No, gracias** nunca vuelve a preguntar por ese trabajo. Un trabajo que te recordaba hacer algo llega en cambio como oferta de tarea recurrente en Tareas.

Esperan como mucho tres sugerencias a la vez. Tras una semana de buenas ejecuciones, la rutina pregunta **¿Desactivar el antiguo trabajo de OpenClaw?** Solo se desactiva cuando tocas **Desactivar**, y puedes volver a activarlo en OpenClaw.

## Desde lo que haces

Tu Machine también nota el trabajo que haces con un ritmo y lo ofrece como rutina en **Sugerido**, también sin OpenClaw. Busca:

- la misma petición, tres veces o más seguidas, como "resume los tickets de soporte abiertos" cada lunes;
- un correo que envías con un ritmo, como un informe semanal a tu equipo;
- newsletters y correos de novedades que llegan cada semana;
- un canal de Slack con mucho movimiento donde otros escriben cada semana.

Cada sugerencia dice lo que vio, como "Pedido 4 veces seguidas", y se ejecutó una vez para que veas un resultado real. Piensa en un resumen del equipo, un brief antes de una llamada semanal, un resumen de soporte o de desarrollo, el pulso de tus cifras o un resumen de las newsletters que recibes.

Solo sugiere lo que es tuyo y claramente útil: un resumen de noticias solo sobre tus propias newsletters, nunca uno genérico. Cuando nada encaja, no hay sugerencia. Mira como mucho una vez al día, y todo se queda en tu Machine. Una tarea que cierras con un ritmo llega en cambio como oferta de tarea recurrente.

## Rutinas y tareas recurrentes

Una tarea recurrente (recurring.md) te recuerda hacer algo. Una rutina es trabajo que tu Machine hace sola y te muestra. Usa una tarea recurrente para "pagar el alquiler el día 1", y una rutina para "cada viernes, dime qué deals se quedaron en silencio".
