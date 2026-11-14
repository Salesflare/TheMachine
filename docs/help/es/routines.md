---
title: Rutinas
area: cards
summary: Trabajo que tu Machine hace por su cuenta siguiendo un ritmo, como un resumen de tus oportunidades abiertas los lunes. Solo lee.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: 9c3559a910b9dd37
---
## Crear una

Abre **Rutinas** en la barra lateral y escribe en una línea qué debe hacer y cuándo: «todos los lunes a las 9, resume mis oportunidades abiertas» o «todas las mañanas entre semana, lista los correos que todavía tengo que responder». Después, pulsa **Añadir**.

Si no indicas una hora, se ejecuta a las 8:00. La hora corresponde al reloj de tu Machine. La primera vez que se ejecuta, le pone un nombre corto.

Al pulsar **Añadir**, primero se hace una prueba para que veas el resultado antes de guardarla. No se envía ni se guarda nada. Después, **Añadir** la deja activada con su ritmo, **Cambiar** prueba otras palabras o un nombre nuevo y **Cancelar** la descarta.

## Plantillas

En **Plantillas**, al final de Rutinas, **Añadir** activa una rutina lista para usar. Se ejecuta una vez de inmediato y luego cada mañana a las 7:30 (Limpieza de spam, cada hora; Suscripciones y pruebas, una vez al mes). Su tarjeta muestra las instrucciones, como cualquier rutina, y **Editar** permite cambiarlas o cambiar el nombre.

Si recibes muchos newsletters y Limpieza de newsletters está desactivada (25 o más en una semana, de al menos 5 remitentes), aparece una línea encima de tus tareas que indica cuántos han llegado y qué haría la rutina, con las opciones **Activarla** y **No, gracias**.

Limpieza de spam se ofrece de la misma forma si en una semana has movido manualmente 5 o más correos a spam. **Activarla** la añade igual que **Añadir** aquí. Si eliges **No, gracias**, no volverá a ofrecerse, y una plantilla que ya hayas usado tampoco volverá a aparecer.

**Limpieza de newsletters** crea una tarea por área (trabajo y personal) con los newsletters del último día. Cada uno tiene las opciones **Mantener** y **Darse de baja**. Para darte de baja, usa el enlace de un solo clic de la lista o el correo de baja enviado desde tu dirección, si el envío está activado. Si no, The Machine se da de baja desde la página de la lista en su propio navegador. Si necesitas iniciar sesión, resolver un captcha o elegir opciones, tendrás que hacerlo tú: la fila explica por qué y ofrece **Abrir página de baja**.

Se excluyen los recibos, los pedidos y los avisos de pago. Los correos recibidos a través de una dirección de grupo, como Google Groups, aparecen bajo el nombre de quien los escribió y nunca te dan de baja del grupo. Si el remitente no tiene una opción para darse de baja, la fila muestra **Darse de baja a mano**.

**Limpieza de spam** crea una tarea por área con correos de remitentes desconocidos que parecen spam. Cada uno tiene las opciones **Spam** y **No es spam**. Outlook mueve el spam a Correo no deseado y Gmail lo marca como spam. La rutina comprueba cada hora, así que normalmente el spam ya estará ahí cuando lo revises. Si llegan nuevos correos de spam mientras la tarea está abierta, se añaden a ella.

Gmail conectado en modo de solo lectura, como en una Machine alojada, no puede mover correos a spam. En ese caso, **Spam** muestra un enlace para marcarlo en Gmail y The Machine recuerda que ese remitente es spam. Si no hay ninguna cuenta de correo conectada, la plantilla muestra **Conectar correo** en lugar de **Añadir**.

Se considera desconocido a alguien a quien nunca has escrito. Un «Re:» solo cuenta como conversación si aparece en un hilo en el que tú hayas escrito. Si vuelve a llegar un correo de un remitente que marcaste como spam, desde la tarea o desde tu bandeja de entrada, aparecerá en la siguiente tarea como **Marcado como spam antes**. Los correos que tú mismo hayas movido a spam también ayudan a detectar mensajes similares.

Nada cambia hasta que lo confirmas en la tarea. Pulsa el nombre de un remitente para leer el correo primero: seguirá sin leerse y nada cambiará. En Limpieza de spam, las imágenes de la web no se cargan, así que el remitente no puede saber que lo has abierto. No volverán a preguntarte por los remitentes sobre los que ya hayas decidido. Si en un día no hay newsletters ni spam, no se crea ninguna tarea, y estas tareas nunca envían notificaciones.

Cuando hayas decidido qué hacer con todos los remitentes, la tarea indicará que ha terminado y mostrará **Marcar como hecha**.

**Resumen diario** selecciona una vez al día los pocos artículos de newsletters que merecen tu atención y los reúne en una tarea. Cada uno incluye una línea que explica por qué te interesa. Pulsa un artículo para leer el correo o usa **Abrir en tu correo**. Solo se incluyen newsletters: nunca correos de personas, recibos o remitentes de los que te hayas dado de baja, ni correos que ya hayas leído. Si no hay nada destacable, no se crea ninguna tarea.

La rutina aprende qué te interesa a partir de lo que abres, marcas con una estrella o archivas sin leer, y de las opciones **Más como esto** y **Menos como esto** de cada sugerencia. Los temas que selecciona aparecen en la tarjeta de la rutina, en **Más de** y **Menos de**. Pulsa × para quitar un tema o añade uno propio. Los temas con línea discontinua los ha aprendido por sí sola. Cada nuevo resumen sustituye al anterior si sigue abierto, y nunca envía notificaciones.

Solo lee el remitente, el asunto y el comienzo de cada newsletter nueva, y hace una pregunta breve sobre ellos a tu IA, con un límite diario para que no cueste mucho. **Cambiar cuándo** permite ajustar la hora. Si cambias las instrucciones, se ejecuta como cualquier rutina, siguiendo las instrucciones que escribiste.

**Cumpleaños** crea una tarea por cada contacto cercano que cumpla años hoy: personas a las que escribes tú, como amistades, familiares y contactos habituales. Cada tarea incluye un saludo breve preparado donde sueles hablar con esa persona, como su chat de WhatsApp o el hilo de correo, y en su idioma. Solo se envía si tú lo haces. Si ese día no hay cumpleaños, no se crea ninguna tarea.

Los cumpleaños se obtienen de tus calendarios (los eventos de cumpleaños de Google y el calendario Cumpleaños, que se consultan cada mañana aunque no estén sincronizados, y el calendario Cumpleaños de Outlook), de tus contactos de Google en una Machine autohospedada y de un campo de fecha llamado Birthday en una persona de Graph. Si todavía no hay cumpleaños en ninguna de esas fuentes, el resultado indica **Aún no hay información sobre cumpleaños** y explica cómo añadirla.

**Importar cumpleaños de Facebook**: cuando Cumpleaños esté activada, una tarea te ofrecerá leer la página de cumpleaños de Facebook. Pulsa **Importar** y The Machine abrirá la página en su navegador, se desplazará hasta que se hayan cargado todos los meses y leerá el nombre y el cumpleaños de cada amistad. Te mostrará cuántos encontró y quiénes coinciden con personas de tu Graph por nombre y apellidos. Si más de una persona tiene el mismo nombre, se omite y se incluye en la lista.

Solo **Guardar** los añade, en la página de cada persona: el cumpleaños y la foto de perfil de Facebook si aún no tiene una. Los cumpleaños o las fotos que ya hayas añadido se conservan, y nunca se sustituye una foto que ya tengan. No se escribe nada en Facebook.

No vuelve a leer la página por su cuenta: para hacerlo, pulsa **Importar de nuevo** en la tarea. El navegador debe tener una sesión iniciada en Facebook. Si no la tiene, pulsa **Iniciar sesión en Facebook** en la tarea e inicia sesión allí; una vez dentro, leerá la página automáticamente. The Machine nunca inicia sesión por ti.

Se cuentan las amistades que no estén en tu Graph y se muestran algunos nombres. **Añadir … como contactos personales** las añade todas a la vez, también después de pulsar **Guardar**: cada una con su nombre y cumpleaños, y nunca se comparte con una Work Fleet. Se omite cualquier persona cuyo nombre ya exista en tu Graph o que hayas eliminado permanentemente. Los recordatorios de cumpleaños siguen apareciendo solo para las personas a las que escribes.

Si pulsas **Deshacer** en la tarea, se eliminan exactamente esas personas, también después de **Importar de nuevo**.

**Suscripciones y pruebas** lee tus recibos, facturas y avisos de renovación una vez al mes, y reúne tus suscripciones en una tarea: cuánto cuesta cada una, cuándo se cobra el próximo pago y una alerta cuando termina una prueba o sube el precio. Solo se incluyen las que identifica con seguridad. Si no encuentra ninguna, no se crea ninguna tarea.

Elige **Mantener** o **Cancelar** para cada una. No volverán a preguntarte por las que mantengas, salvo que cambie su precio. **Cancelar** muestra la página para cancelar o un borrador para pedir la cancelación, que solo se envía cuando tú lo haces. Entre una ejecución y otra, comprueba cada día y crea una tarea si una prueba o una renovación se cobrará en los próximos 7 días.

Mientras la rutina de una plantilla conserve sus instrucciones originales, se ejecuta con su propio código, sin usar tu plan de IA (Limpieza de spam primero busca en el código correos nuevos de remitentes desconocidos y solo hace una pregunta breve a tu IA si encuentra alguno). Si cambias el nombre, se conserva ese comportamiento. Si cambias las instrucciones, se ejecuta como cualquier rutina, siguiendo las instrucciones que escribiste.

Limpieza de newsletters y Limpieza de spam siguen creando una misma tarea con una opción por correo. Si editas Cumpleaños, se muestra su resultado y, como máximo, un borrador, no una tarea por persona. **Volver a la plantilla**, en **Editar**, restaura sus instrucciones originales.

## Qué hace una rutina

A la hora programada, tu Machine lee lo que necesita, como tus mensajes, reuniones y Graph, y muestra el resultado en la página Rutinas. Cada resultado indica **Para revisar**, **Nada nuevo** (con una explicación) o **No funcionó** (con una explicación). Una ejecución que termina sin resultado cuenta como fallida, nunca como completada.

Las rutinas solo leen: tus mensajes, páginas web, GitHub y sitios como X en el navegador. No envían mensajes, no responden, no publican ni cambian nada. Solo una plantilla modifica el correo, y únicamente lo que confirmes en su tarea.

Si el trabajo de una rutina termina con una publicación o un mensaje, completa todos los pasos anteriores y muestra el borrador, por ejemplo, **Se publicaría en X:**. Después de una ejecución real, aparece como tarea para que lo apruebes; una ejecución de prueba solo lo muestra. Su nombre indica el tema y dónde se publicaría, el botón indica el paso, como **Publícalo**, y **Desde tu rutina**, debajo, abre la rutina.

La tarea empieza en el área de la cuenta desde la que se enviaría, como Trabajo para la cuenta de X de tu empresa, así que nunca te pedirá que la muevas.

Una ejecución puede seguir tus [habilidades](skills.md) activadas, seleccionadas según lo que haga la rutina: solo se leen por completo las que correspondan. El resultado las indica debajo de **Usado:**. Una habilidad nunca hace que una rutina envíe ni cambie nada.

Tus rutinas aparecen en **Tus rutinas**, debajo de las sugerencias. Si el resultado es largo, se muestra una vista previa breve; pulsa **Mostrar más** o el propio resultado para abrirlo.

Cada ejecución tiene en cuenta el último resultado, así que puede indicar qué ha cambiado desde entonces.

Después de una ejecución correcta, tu Machine puede escribir una receta para las partes de la lectura que siempre son iguales, como qué correos o cambios de GitHub debe revisar. En las siguientes ejecuciones, primero las lee con código sencillo; después, la IA solo selecciona lo importante y lo redacta, usando menos tokens. La receta solo lee. Si deja de funcionar, la rutina vuelve a leer por su cuenta y la corrige. La receta aparece en **Avanzado: pasos de script**, en el menú ⋯.

## Días sin conexión

Si tu Machine estaba apagada u ocupada, no acumula las ejecuciones omitidas: solo ejecuta la más reciente, una vez. Cada fecha se procesa una sola vez, incluso después de reiniciar.

Las rutinas se ejecutan de una en una y esperan si el uso de tu plan de IA es bajo, como cualquier trabajo en segundo plano. **Ejecutar ahora** la ejecuta de inmediato; el resultado aparece en la tarjeta cuando esté listo.

## Cambiarla o detenerla

Estas opciones están en el menú ⋯ de la rutina. **Editar** cambia el nombre y lo que hace; conserva la hora de ejecución y los resultados anteriores. **Cambiar cuándo** permite escribir un ritmo nuevo con tus propias palabras, como «todos los días laborables a las 8». Ambas opciones incluyen **Guardar** y **Cancelar**; en un ordenador, también puedes cancelar con Esc o haciendo clic fuera.

En **Editar**, **Probarlo** ejecuta una vez las instrucciones nuevas y muestra el resultado allí. La rutina sigue igual hasta que pulses **Guardar**.

**Pausar** detiene las ejecuciones hasta que pulses **Reanudar**. Las rutinas pausadas aparecen al final, en **En pausa**, y no se ejecuta después nada de lo que se haya omitido mientras estaban pausadas. **Detener** termina la rutina definitivamente.

Si usas **Pedir cambios** en una tarea de la rutina o escribes en su chat, y tu nota debe aplicarse a todas las ejecuciones, como «nunca uses emojis», la tarea te ofrecerá **Cambiar también la rutina**. La opción aparece en la tarea y en su chat, debajo de la respuesta. Verás qué cambia en las instrucciones de la rutina, que solo se actualizarán cuando pulses **Cambiarla**. **Dejarla así** las mantiene igual. Si solo corriges ese borrador, no aparecerá ninguna opción.

## Avanzado: pasos de script

No necesitas ningún script: describe con tus propias palabras lo que debe hacer una rutina y tu Machine se encarga del resto.

Si tienes más experiencia, una rutina también puede ejecutar tus propios comandos en tu Machine: abre el menú ⋯ y elige **Avanzado: pasos de script**. **Editar** solo aparece cuando la rutina ya tiene alguno. **Obtener datos** ejecuta primero un comando en su carpeta (tu carpeta de inicio si no se indica ninguna), durante un máximo de los segundos especificados. Lo que muestre el comando pasa a la ejecución para que trabaje con ello. Si no hay instrucciones, lo que muestre será el resultado.

**Comprobación** recibe el resultado como entrada después de la ejecución. Si el comando termina con un error, la ejecución muestra **No funcionó** junto con el mensaje de la comprobación. Si falla el comando de Obtener datos, también se muestra de la misma forma.

Cada comando debe ocupar una sola línea y se ejecuta sin un shell: no se admiten tuberías ni variables. Los pasos de script son tuyos y solo se configuran en tu panel. Las ejecuciones de prueba y las de **Probarlo** también ejecutan Obtener datos y lo indican; aun así, no envían ni guardan nada. Una rutina nunca envía nada, así que los pasos de script solo deben leer.

## Desde tus trabajos de OpenClaw

Si antes creaste trabajos programados en OpenClaw, tu Machine los lee (nunca los cambia) y ofrece como rutinas los que encajan, en **Sugerido**. Cada uno se ejecutó una vez, así que puedes ver un resultado real.

Conserva las correcciones que hayas hecho al trabajo y omite lo que haya enviado o publicado. Si un trabajo ejecutaba un script o leía datos recopilados por un trabajo con script, los incluye como Obtener datos. **Añadir** lo convierte en una rutina; si pulsas **No, gracias**, no volverá a preguntarte por ese trabajo. Si un trabajo te recordaba hacer algo, aparecerá como una oferta de tarea periódica en Tareas.

Antes de añadir una sugerencia, puedes cambiarla como cualquier rutina desde **Editar** y **Cambiar cuándo**, en el menú ⋯. **Ejecutar de nuevo** la ejecuta ahora con las instrucciones actuales para ver resultados más recientes, por ejemplo, después de un fin de semana tranquilo. Solo lee, se ejecuta una vez por cada toque y sustituye el resultado anterior por el nuevo.

Puede haber hasta tres sugerencias a la vez. Después de una semana de ejecuciones correctas, la rutina te pregunta **¿Desactivar el antiguo trabajo de OpenClaw?**. Solo lo desactiva si pulsas **Desactivar**; puedes volver a activarlo en OpenClaw.

## Según lo que haces

Tu Machine también detecta tareas que haces con cierta frecuencia y las ofrece como rutinas en **Sugerido**, aunque no uses OpenClaw. Busca lo siguiente:

- la misma petición tres veces seguidas o más, como «resume los tickets de soporte abiertos» todos los lunes;
- un correo que envías regularmente, como un informe semanal para tu equipo;
- newsletters y correos de novedades que llegan todas las semanas;
- un canal de Slack con mucha actividad en el que otras personas escriben cada semana;
- correos que reenvías de uno en uno a la misma persona, como los del colegio o de actividades extraescolares que reenvías a tu pareja: un resumen semanal para esa persona evita que tengas que reenviarlos;
- la misma petición que respondes regularmente, como una aprobación mensual para la misma persona.

Cada sugerencia indica qué ha detectado, como «Lo has pedido 4 veces seguidas» o «Has reenviado 6 correos a Sam en 3 semanas», y se ejecuta una vez para que veas un resultado real. Puede servir, por ejemplo, para resumir el trabajo del equipo, prepararte antes de una llamada semanal, resumir solicitudes de soporte o de desarrollo, hacer un seguimiento de tus cifras o resumir los newsletters que recibes.

Solo sugiere rutinas que sean específicas para ti y claramente útiles: un resumen de noticias solo incluiría tus propios newsletters, nunca uno genérico. Si no encuentra nada que encaje, no habrá sugerencias.

Busca como máximo una vez al día y añade como máximo una sugerencia nueva por semana, sin enviar notificaciones. Si pulsas **No, gracias**, no volverá a aparecer esa sugerencia. Los reenvíos y las respuestas permanecen en la cuenta desde la que se enviaron, así que Trabajo y Personal no se mezclan. Todo permanece en tu Machine. Una tarea que completes regularmente aparecerá como oferta de tarea periódica.

## Rutinas y tareas periódicas

Una tarea periódica (recurring.md) te recuerda que hagas algo. Una rutina es un trabajo que tu Machine hace por su cuenta y te muestra. Usa una tarea periódica para «pagar el alquiler el día 1» y una rutina para «todos los viernes, dime qué oportunidades se han quedado paradas».
