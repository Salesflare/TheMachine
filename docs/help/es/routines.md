---
title: Rutinas
area: cards
summary: Trabajo que tu Machine hace sola, con un ritmo, como un resumen del lunes de tus deals abiertos. Solo lee.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
---
## Crear una

Abre **Rutinas** en la barra lateral y di en una línea qué debe hacer y cuándo: "cada lunes a las 9, resume mis deals abiertos" o "cada día laborable por la mañana, lista los correos que aún debo responder". Luego **Añadir**.

Sin hora, se ejecuta a las 8:00. La hora es la del reloj de tu Machine.

## Plantillas

En **Plantillas**, al final de Rutinas, **Añadir** activa una rutina ya hecha. Se ejecuta una vez enseguida y luego cada mañana a las 7:30 (Limpieza de spam, cada hora). Su tarjeta muestra sus palabras como cualquier rutina, y **Editar** cambia sus palabras o su nombre.

Cuando llegan muchas newsletters y Limpieza de newsletters está desactivada (25 o más en una semana, de al menos 5 remitentes), una línea encima de tus to-dos dice cuántas llegaron y qué haría, con **Activarla** y **No, gracias**.

Limpieza de spam se ofrece igual cuando en una semana se movieron 5 o más correos a spam a mano. **Activarla** la añade como **Añadir** aquí. Tras **No, gracias** no se vuelve a ofrecer, y una plantilla que ya tuviste nunca.

**Limpieza de newsletters** crea una tarea por área (trabajo y personal) con las newsletters del último día, cada una con **Mantener** o **Darse de baja**. La baja usa el enlace de un clic de la lista, o su correo de baja desde tu dirección si el envío está activado. Si no, muestra **Abrir página de baja**.

Los recibos, pedidos y avisos de pago quedan fuera. El correo que llega por una dirección de grupo, como un Google Group, aparece bajo quien lo escribió y nunca te da de baja del grupo.

**Limpieza de spam** crea una tarea por área con correo de remitentes desconocidos que parece spam, cada uno con **Spam** o **No es spam**. Outlook mueve el spam a Correo no deseado y Gmail lo marca como spam. Revisa cada hora, así el spam suele estar ahí antes de que llegues a él. El spam nuevo va a la misma tarea mientras siga abierta.

Gmail conectado solo para leer, como en una Machine alojada, no puede mover correo a spam. Ahí, **Spam** da un enlace para marcarlo en Gmail, y The Machine recuerda al remitente como spam. Sin ninguna cuenta de correo conectada, la plantilla muestra **Conectar correo** en lugar de **Añadir**.

Desconocido quiere decir que nunca le escribiste, y un “Re:” solo cuenta como conversación en un hilo donde escribiste. Si vuelve a colarse correo de un remitente que marcaste como spam, en la tarea o en tu buzón, aparece en la siguiente tarea como **Marcado como spam antes**. Lo que tú mismo moviste a spam también le ayuda a reconocer correo parecido.

Nada cambia hasta que confirmas en la tarea. Toca un remitente para leer antes el correo: sigue sin leer y nada cambia. Desde Limpieza de spam no se cargan sus imágenes de la web, así el remitente no ve que se abrió. Los remitentes ya decididos no vuelven a salir. Un día sin newsletters ni spam no crea tarea, y estas tareas nunca envían una notificación.

Cuando todos los remitentes están decididos, la tarea dice que está terminada y **Marcar como hecha** está en ella.

**Resumen diario** elige una vez al día las pocas piezas de tus newsletters que valen tu tiempo, en una tarea. Cada una dice en una línea por qué te importa. Tócala para leer el correo, o usa **Abrir en tu correo**. Solo newsletters: nunca correo de personas, recibos ni remitentes de los que te diste de baja, y nunca lo que ya leíste. Cuando nada destaca, no hay tarea.

Aprende lo que te importa de lo que abres, marcas con estrella o archivas sin leer, y de **Más como esto** y **Menos como esto** en cada pieza. Los temas por los que elige están en la tarjeta de la rutina bajo **Más de** y **Menos de**. Quita uno con ×, o añade los tuyos. Los de línea discontinua los aprendió por su cuenta. Un resumen nuevo reemplaza al abierto, y nunca envía una notificación.

Solo lee el remitente, el asunto y el comienzo de cada newsletter nueva, y le hace a tu IA una pregunta corta sobre ellas, con un límite diario, para que siga siendo barato. **Cambiar cuándo** fija su hora. Si cambias sus palabras, se ejecuta como cualquier rutina con tus palabras.

**Cumpleaños** crea una tarea para cada contacto cercano que cumple años hoy: personas a las que tú escribes, como amigos, familia y contactos habituales. Cada una trae una felicitación corta redactada donde sueles hablar con ellos, como su chat de WhatsApp o tu hilo de correo, en su idioma. Solo sale cuando tú la envías. Un día sin cumpleaños no crea ninguna tarea.

Los cumpleaños vienen de tus calendarios (los cumpleaños y el calendario Cumpleaños de Google, leídos cada mañana aunque no se sincronicen, y el calendario Cumpleaños de Outlook), de tus contactos de Google en una Machine autoalojada y de un campo de fecha llamado Cumpleaños en una persona del Graph. Si ninguno tiene todavía un cumpleaños, el resultado dice **Aún no hay cumpleaños** y cómo añadirlos.

**Importar cumpleaños de Facebook**: con Cumpleaños activado, una tarea ofrece leer la página de cumpleaños de Facebook. Toca **Importar** y The Machine la abre en su navegador, se desplaza hasta que cargan todos los meses y lee el nombre y el cumpleaños de cada amigo. Muestra cuántos encontró y quiénes coinciden por nombre y apellido con personas de tu Graph. Un nombre que tiene más de una persona se omite y se lista.

Solo **Guardar** los conserva, en la página de cada persona: el cumpleaños y, si aún no tiene foto, su foto de perfil de Facebook. Un cumpleaños o una foto que pusiste ahí se queda, y una foto que ya tiene nunca se reemplaza. No se escribe nada en Facebook.

Nunca vuelve a leer por sí sola: lo hace **Importar de nuevo** en la tarea. El navegador tiene que tener sesión iniciada en Facebook. Si no la tiene, toca **Inicia sesión en Facebook** en la tarea e inicia sesión ahí; después lee la página por sí sola. The Machine nunca inicia sesión por ti.

Los amigos que nadie en tu Graph tiene se cuentan, con algunos nombres. **Añadir … como contactos personales** los añade todos a la vez, también después de Guardar: cada uno con su nombre y cumpleaños, nunca compartido con una Work Fleet. Un nombre que ya tiene alguien de tu Graph, o que tenía alguien que borraste para siempre, se omite. Los recordatorios de cumpleaños siguen llegando solo para la gente a la que escribes.

**Deshacer** en la tarea quita exactamente a esas personas, también después de **Importar de nuevo**.

Mientras sus palabras sean las de la plantilla, funciona con su propio código, sin tu plan de IA (Limpieza de spam primero lista con código el correo nuevo de remitentes desconocidos, y solo hace una pregunta corta a tu IA cuando hay alguno). Un nombre nuevo no cambia eso. Si cambias sus palabras, funciona como cualquier rutina con tus palabras.

Limpieza de newsletters y Limpieza de spam siguen terminando en la misma tarea con una opción por correo. Un Cumpleaños editado da su resultado y como mucho un borrador, no una tarea por persona. **Volver a la plantilla** en **Editar** devuelve sus palabras.

## Qué hace una rutina

A su hora, tu Machine lee lo que necesita, como tus mensajes, reuniones y el Graph, y deja el resultado en la página Rutinas. Cada resultado dice **Para revisar**, **Nada nuevo** (con el porqué) o **No funcionó** (con el porqué). Una ejecución que termina sin resultado cuenta como fallida, nunca como hecha.

Las rutinas solo leen: tus mensajes, páginas web, GitHub y sitios como X en el navegador. No envían, responden, publican ni cambian nada. Solo una plantilla cambia correo, y solo lo que confirmas en su tarea.

Cuando la tarea de una rutina termina en una publicación o un mensaje, hace todo hasta ese paso y muestra el borrador, como **Publicaría en X:**. Tras una ejecución real lo recibes como tarea para aprobar; una ejecución de prueba solo lo muestra. Su nombre dice de qué trata y adónde va, su botón nombra el paso, como **Publícalo**, y **De tu rutina** debajo abre la rutina.

La tarea empieza en el área de la cuenta desde la que sale, como Trabajo para la cuenta de X de tu empresa, así que nunca pide moverla.

Cada ejecución conoce el último resultado, así puede decir qué cambió desde entonces.

Después de una buena ejecución, tu Machine puede escribirse una receta para la lectura que es igual cada vez, como qué correos o cambios de GitHub mirar. Las siguientes ejecuciones leen eso primero, con código simple, y la IA solo elige lo que importa y lo escribe, con menos tokens. Una receta solo lee; si deja de funcionar, la ejecución lee por sí misma y la arregla. Aparece en **Avanzado: pasos de script** en el menú ⋯.

## Días perdidos

Si tu Machine estaba apagada u ocupada, las ejecuciones perdidas no se acumulan: solo corre la más reciente, una vez. Cada fecha corre una vez, incluso tras un reinicio.

Las rutinas corren de una en una y esperan cuando el uso de tu plan de IA está bajo, como todo el trabajo en segundo plano. **Ejecutar ahora** la ejecuta enseguida.

## Cambiarla o detenerla

Está en el menú ⋯ de la rutina. **Cambiar cuándo** toma un nuevo ritmo en tus propias palabras, como "cada día laborable a las 8". **Pausar** detiene las ejecuciones hasta **Reanudar**; lo perdido durante la pausa no corre después. **Detener** termina una rutina para siempre.

Cuando usas **Pedir cambios** en una tarea de una rutina, o escribes en su chat, y tu nota vale para cada ejecución, como "nunca uses emojis", la tarea ofrece **Cambiar también la rutina**, en la tarea y en su chat bajo la respuesta. Muestra qué cambia en las palabras de la rutina, y la rutina solo cambia cuando tocas **Cambiarla**. **Dejarla así** la deja como está. Una corrección solo de ese borrador no ofrece nada.

## Avanzado: pasos de script

Nunca necesitas un script: di con tus propias palabras qué debe hacer una rutina.

Para usuarios avanzados, una rutina también puede ejecutar tus propios comandos en tu Machine: en el menú ⋯, elige **Avanzado: pasos de script**. **Editar** solo los muestra si una rutina ya tiene. **Obtener datos** ejecuta primero un comando, en su carpeta (vacía: tu carpeta personal) y como mucho durante sus segundos. Lo que imprime va a la ejecución para trabajar con ello. Sin palabras, lo que imprime es el resultado.

**Comprobación** recibe el resultado como entrada después de la ejecución. Si termina con un error, la ejecución muestra **No funcionó** con lo que dijo la comprobación. Un comando de Obtener datos que falla se muestra igual.

Un comando es una línea y corre sin shell: sin pipes ni variables. Los pasos de script son tuyos, solo se configuran en tu panel. Una ejecución de prueba y **Probarlo** también ejecutan Obtener datos y lo dicen; siguen sin enviar ni guardar nada. Una rutina nunca envía, así que un paso de script solo debería leer.

## Desde tus trabajos de OpenClaw

Si antes creaste trabajos programados en OpenClaw, tu Machine los lee (nunca los cambia) y ofrece los que encajan como rutinas en **Sugerido**. Cada uno se ejecutó una vez, para que veas un resultado real.

Mantiene tus correcciones al trabajo y deja fuera lo que enviaba o publicaba. Un trabajo que ejecutaba un script, o leía lo que recogía un trabajo de script, lo trae como Obtener datos. **Añadir** lo convierte en rutina, **No, gracias** nunca vuelve a preguntar por ese trabajo. Un trabajo que te recordaba hacer algo llega en cambio como oferta de tarea recurrente en Tareas.

Antes de añadir una sugerencia, **Editar** y **Cambiar cuándo** en su menú ⋯ la cambian como cualquier rutina. **Ejecutar de nuevo** la ejecuta ahora con sus palabras actuales, para ver resultados más nuevos, por ejemplo tras un fin de semana tranquilo. Solo lee, se ejecuta una vez por toque y su nuevo resultado reemplaza al anterior.

Esperan como mucho tres sugerencias a la vez. Tras una semana de buenas ejecuciones, la rutina pregunta **¿Desactivar el antiguo trabajo de OpenClaw?** Solo se desactiva cuando tocas **Desactivar**, y puedes volver a activarlo en OpenClaw.

## Desde lo que haces

Tu Machine también nota el trabajo que haces con un ritmo y lo ofrece como rutina en **Sugerido**, también sin OpenClaw. Busca:

- la misma petición, tres veces o más seguidas, como "resume los tickets de soporte abiertos" cada lunes;
- un correo que envías con un ritmo, como un informe semanal a tu equipo;
- newsletters y correos de novedades que llegan cada semana;
- un canal de Slack con mucho movimiento donde otros escriben cada semana;
- correos que reenvías uno a uno a la misma persona, como los del colegio y el club a tu pareja: un resumen semanal para esa persona te ahorra reenviarlos;
- la misma petición que respondes con un ritmo, como una aprobación mensual para la misma persona.

Cada sugerencia dice lo que vio, como "Pedido 4 veces seguidas" o "6 correos reenviados a Sam en 3 semanas", y se ejecutó una vez para que veas un resultado real. Piensa en un resumen del equipo, un brief antes de una llamada semanal, un resumen de soporte o de desarrollo, el pulso de tus cifras o un resumen de las newsletters que recibes.

Solo sugiere lo que es tuyo y claramente útil: un resumen de noticias solo sobre tus propias newsletters, nunca uno genérico. Cuando nada encaja, no hay sugerencia.

Mira como mucho una vez al día y trae como mucho una sugerencia nueva por semana, sin notificación. **No, gracias** nunca la vuelve a traer. Los reenvíos y las respuestas se quedan con la cuenta desde la que salieron, para que Trabajo y Personal no se mezclen. Todo se queda en tu Machine. Una tarea que cierras con un ritmo llega en cambio como oferta de tarea recurrente.

## Rutinas y tareas recurrentes

Una tarea recurrente (recurring.md) te recuerda hacer algo. Una rutina es trabajo que tu Machine hace sola y te muestra. Usa una tarea recurrente para "pagar el alquiler el día 1", y una rutina para "cada viernes, dime qué deals se quedaron en silencio".
