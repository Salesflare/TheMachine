---
title: Rutinas
area: cards
summary: Tareas que tu Machine hace por su cuenta, de forma periódica, como un resumen de tus oportunidades abiertas cada lunes. Solo lee.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in
translated: 2be351a9cef42215
---
## Crear una rutina

Abre **Rutinas** en la barra lateral y di en una línea qué debe hacer y cuándo: «todos los lunes a las 9, resume mis oportunidades abiertas» o «todas las mañanas entre semana, enumera los correos que aún tengo que responder». Después, **Añadir**.

Si no indicas una hora, se ejecuta a las 8:00. La hora es la de tu Machine. La primera vez que se ejecuta, recibe un nombre corto.

**Añadir** primero hace una prueba para que veas el resultado antes de conservarla. No se envía ni se guarda nada. Después, **Añadir** la mantiene en marcha según lo previsto, **Cambiar** prueba otras palabras o un nombre nuevo y **Cancelar** la elimina.

## Plantillas

En **Plantillas**, al final de Rutinas, **Añadir** activa una rutina lista para usar. Se ejecuta una vez de inmediato y, después, cada mañana a las 7:30 (Limpieza de spam, cada hora; Suscripciones y pruebas, una vez al mes). Su tarjeta muestra las instrucciones, como cualquier rutina, y **Editar** permite cambiarlas o cambiar su nombre.

Si recibes muchos boletines y Limpieza de newsletters está desactivada (25 o más en una semana, de al menos 5 remitentes), aparece una línea encima de tus tareas que indica cuántos han llegado y qué haría la rutina, con las opciones **Activarla** y **No, gracias**.

Limpieza de spam se ofrece de la misma forma cuando has movido a mano 5 correos o más a spam en una semana. **Activarla** la añade igual que **Añadir**. **No, gracias** significa que no volverá a ofrecerse, y tampoco volverá a hacerlo una plantilla que ya habías tenido.

**Limpieza de newsletters** crea una tarea por área (trabajo y personal) con los boletines del último día. Cada uno incluye las opciones **Mantener** o **Darse de baja**. Para darte de baja, usa el enlace de un solo clic de la lista o envía un correo de baja desde tu dirección, si el envío está activado. Si no, The Machine se da de baja en la página de la lista desde su propio navegador. Si hace falta iniciar sesión, completar un captcha o elegir opciones, tendrás que hacerlo tú: la fila explica el motivo e incluye **Abrir página de baja**.

Se excluyen los recibos, los pedidos y los avisos de pago. Los correos recibidos a través de una dirección de grupo, como un grupo de Google, aparecen bajo el nombre de quien los escribió y nunca te dan de baja del grupo. Si el remitente no ofrece una opción para darse de baja, la fila muestra **Darse de baja a mano**.

**Limpieza de spam** crea una tarea por área con correos de remitentes desconocidos que parecen spam. Cada uno incluye las opciones **Spam** o **No es spam**. Outlook mueve el spam a Correo no deseado y Gmail lo marca como spam. La rutina lo comprueba cada hora, así que normalmente el spam ya está ahí cuando llegas. El spam nuevo se añade a la misma tarea mientras siga abierta.

Si Gmail está conectado en modo de solo lectura, como en una Machine alojada, no se pueden mover los correos a spam. En ese caso, **Spam** muestra un enlace para marcarlo en Gmail y The Machine recuerda que el remitente es spam. Si no hay ninguna cuenta de correo conectada, la plantilla muestra **Conectar correo** en lugar de **Añadir**.

Se considera desconocido a alguien a quien nunca has escrito. Además, «Re:» solo cuenta como conversación si participaste en ese hilo. Si vuelve a llegarte un correo de un remitente que marcaste como spam, desde la tarea o tu bandeja de entrada, aparecerá en la próxima tarea como **Marcado como spam antes**. Los correos que tú hayas movido a spam también ayudan a detectar correos parecidos.

Nada cambia hasta que lo confirmas en la tarea. Toca un remitente para leer el correo primero: seguirá sin leerse y nada cambiará. En Limpieza de spam, las imágenes de la web no se cargan, así que el remitente no puede ver que abriste el correo. No volverá a preguntarte por los remitentes sobre los que ya hayas decidido. Si un día no hay boletines ni spam, no se crea ninguna tarea, y estas tareas nunca envían notificaciones.

Cuando hayas decidido sobre todos los remitentes, la tarea indica que ha terminado e incluye **Marcar como hecha**.

**Resumen diario** selecciona los pocos artículos de boletines que merecen la pena y los reúne en una tarea diaria. Cada uno explica en una línea por qué te interesa. Tócalo para leer el correo o usa **Abrir en tu correo**. Solo incluye boletines: nunca correos de personas, recibos ni remitentes de los que te hayas dado de baja, y tampoco contenido que ya hayas leído. Si no hay nada destacable, no se crea ninguna tarea.

Aprende qué te interesa según lo que abres, marcas con una estrella o archivas sin leer, y con las opciones **Más como esto** y **Menos como esto** de cada selección. En la tarjeta de la rutina, puedes ver los temas que selecciona en **Más de** y **Menos de**. Toca × para quitar un tema o añade los tuyos. Los temas con línea discontinua los ha aprendido por su cuenta. Un resumen nuevo sustituye al que esté abierto y nunca envía una notificación.

Solo lee el remitente, el asunto y el comienzo de cada boletín nuevo, y hace una pregunta breve sobre ellos a tu IA, con un límite diario para que no cueste mucho. **Cambiar cuándo** permite cambiar la hora. Cuando cambias las instrucciones, se ejecuta como cualquier rutina, con tus instrucciones.

**Cumpleaños** crea una tarea por cada contacto cercano que cumpla años hoy: personas a las que escribes tú, como amistades, familiares y contactos habituales. Cada tarea incluye un saludo breve, preparado en el lugar donde sueles hablar con esa persona, como su chat de WhatsApp o el hilo de correo, y en su idioma. Solo se envía cuando tú lo haces. Si no hay cumpleaños ese día, no se crea ninguna tarea.

Los cumpleaños se obtienen de tus calendarios (los eventos de cumpleaños de Google y el calendario Cumpleaños, que se consultan cada mañana aunque no estén sincronizados, y el calendario Cumpleaños de Outlook), de tus contactos de Google en una Machine alojada por tu cuenta y de un campo de fecha llamado Cumpleaños en una persona de Graph. Si todavía no hay ningún cumpleaños, el resultado indica **Aún no hay información sobre cumpleaños** y explica cómo añadirla.

**Importar cumpleaños de Facebook**: cuando Cumpleaños esté activada, una tarea te ofrecerá consultar la página de cumpleaños de Facebook. Toca **Importar** y The Machine abrirá la página en su navegador, se desplazará hasta que se hayan cargado todos los meses y leerá el nombre y el cumpleaños de cada amistad. Te dirá cuántos ha encontrado y quién coincide con personas de tu Graph por nombre y apellidos. Si hay más de una persona con el mismo nombre, se omitirá y se indicará en la lista.

Solo **Guardar** los conserva, en la página de cada persona: el cumpleaños y la foto de perfil de Facebook, si esa persona todavía no tiene foto. Los cumpleaños o las fotos que añadas ahí se conservan, y nunca se reemplaza una foto que ya tenga. No se escribe nada en Facebook.

No vuelve a consultar los datos por sí sola: para hacerlo, toca **Importar de nuevo** en la tarea. El navegador debe tener iniciada la sesión de Facebook. Si no es así, toca **Iniciar sesión en Facebook** en la tarea e inicia sesión allí. Cuando hayas iniciado sesión, la página se consulta automáticamente. The Machine nunca inicia sesión por ti.

Se cuenta a las amistades que no están en tu Graph y se muestran algunos nombres. **Añadir … como contactos personales** las añade todas de una vez, también después de Guardar: cada una con su nombre y cumpleaños, sin compartirlas nunca con una Work Fleet. Se omite a quien ya tenga una persona con el mismo nombre en tu Graph, o haya tenido una que eliminaste de forma permanente. Los recordatorios de cumpleaños siguen apareciendo solo para personas a las que escribes.

**Deshacer** en la tarea elimina exactamente a esas personas, también después de **Importar de nuevo**.

**Suscripciones y pruebas** consulta tus recibos, facturas y avisos de renovación una vez al mes y reúne tus suscripciones en una tarea: cuánto cuesta cada una, cuándo se cobra el próximo pago y una marca si termina una prueba o sube el precio. Solo se muestran las suscripciones que ha podido identificar con seguridad. Si no encuentra ninguna, no se crea ninguna tarea.

Elige **Mantener** o **Cancelar** para cada una. No volverá a preguntarte por las que mantengas, a menos que cambie el precio. **Cancelar** te lleva a la página de cancelación o crea un borrador para pedir la cancelación. Solo se envía cuando tú lo haces. Entre una ejecución y otra, las comprueba cada día y crea una tarea cuando falten 7 días o menos para el cobro de una prueba o renovación.

**Mantenerse en contacto** te recuerda de vez en cuando que contactes con alguien cercano, solo cuando hay un motivo real. En su tarjeta, elige quiénes incluir de una lista breve de personas con las que intercambias mensajes tú, en ambos sentidos, desde hace meses. Toca × para quitar a alguien.

Solo aparece un recordatorio si hace mucho más tiempo de lo habitual que no habláis y hay algo concreto que decir: noticias que compartió, una promesa pendiente o un mensaje que nunca respondiste. Es una sola tarea con el motivo y un mensaje breve preparado en el lugar donde sueles hablar con esa persona, en su idioma. Solo se envía cuando tú lo haces. Si no hay nada que decir, no se crea ninguna tarea.

Envía como máximo dos recordatorios a la semana y uno por persona al mes, y no envía ninguno a alguien con quien hayas hablado hace poco. **No hace falta** en un recordatorio hace que espere más tiempo antes de volver a avisarte sobre esa persona, y cada vez espera un poco más. Nunca envía notificaciones y siempre es Personal: nunca se comparte con una Work Fleet.

Mientras la rutina de una plantilla conserve las instrucciones de la plantilla, se ejecuta con su propio código, sin usar tu plan de IA (Limpieza de spam primero enumera en código los correos nuevos de remitentes desconocidos y solo hace una pregunta breve a tu IA si hay alguno; Mantenerse en contacto solo pregunta por una o dos personas que haya seleccionado). Si le cambias el nombre, se mantienen esas condiciones. Cuando cambias las instrucciones, se ejecuta como cualquier rutina, con tus instrucciones.

Limpieza de newsletters y Limpieza de spam siguen creando la misma tarea, con una opción para cada correo. Una versión editada de Cumpleaños muestra su resultado y, como máximo, un borrador, no una tarea por persona. **Volver a la plantilla**, dentro de **Editar**, restaura sus instrucciones.

## Qué hace una rutina

A la hora indicada, tu Machine lee lo que necesita, como tus mensajes, reuniones y Graph, y muestra el resultado en la página Rutinas. Cada resultado indica **Para revisar**, **Nada nuevo** (con el motivo) o **No funcionó** (con el motivo). Si una ejecución termina sin resultado, cuenta como fallida, nunca como completada.

Las rutinas solo leen: tus mensajes, páginas web, GitHub y sitios como X en el navegador. No envían, responden, publican ni cambian nada. Solo una plantilla puede cambiar el correo, y únicamente lo que confirmes en su tarea.

Cuando el trabajo de una rutina termina con una publicación o un mensaje, hace todo hasta ese paso y muestra el borrador, como **Publicaría en X:**. Después de una ejecución real, aparece como tarea para que lo apruebes; una prueba solo lo muestra. El nombre indica de qué trata y dónde se publica, el botón indica el paso, como **Publícalo**, y **Desde tu rutina**, debajo, abre la rutina.

La tarea empieza en el área de la cuenta desde la que se enviará, como Trabajo para la cuenta de X de tu empresa, así que nunca te pide que la muevas.

Una ejecución puede seguir tus [habilidades](skills.md) activadas, según lo que haga la rutina: solo lee completas las que encajan. El resultado las enumera en **Usadas:**. Una habilidad nunca hace que una rutina envíe ni cambie nada.

Tus rutinas aparecen en **Tus rutinas**, debajo de las sugerencias, si las hay. Los resultados largos se contraen y muestran una vista previa breve. **Mostrar más**, o tocar el resultado, lo abre.

Cada ejecución conoce el último resultado, así que puede indicar qué ha cambiado desde entonces.

Después de una ejecución correcta, tu Machine puede escribir una receta para repetir las mismas lecturas cada vez, como qué correos o cambios de GitHub revisar. En las siguientes ejecuciones, primero se consultan esos datos con código sencillo y la IA solo selecciona lo que importa y lo redacta, con menos tokens. La receta solo lee; si deja de funcionar, la rutina se ejecuta por su cuenta y la corrige. La receta aparece en **Avanzado: pasos de script**, en el menú ⋯.

## Días sin ejecutar

Si tu Machine estaba apagada u ocupada, no acumula las ejecuciones pendientes: solo ejecuta una vez la más reciente. Cada fecha se ejecuta una sola vez, incluso después de reiniciar.

Las rutinas se ejecutan de una en una y esperan cuando queda poco uso en tu plan de IA, igual que el resto del trabajo en segundo plano. **Ejecutar ahora** la ejecuta de inmediato; el resultado aparece en la tarjeta cuando esté listo.

## Cambiarla o detenerla

Estas opciones están en el menú ⋯ de la rutina. **Editar** cambia el nombre y lo que hace; la hora de ejecución y los resultados anteriores se mantienen. **Cambiar cuándo** permite elegir una nueva frecuencia con tus propias palabras, como «todos los días entre semana a las 8». Ambas opciones incluyen **Guardar** y **Cancelar**. En un ordenador, también puedes cancelar con Esc o haciendo clic fuera.

En **Editar**, **Probarlo** ejecuta una vez las instrucciones nuevas y muestra el resultado ahí. La rutina no cambia hasta que toques **Guardar**.

**Pausar** detiene las ejecuciones hasta que pulses **Reanudar** en su tarjeta. Las rutinas en pausa aparecen en **En pausa**, debajo de tus rutinas, y no se ejecuta después nada de lo que se haya omitido mientras estaban en pausa. **Detener** elimina una rutina definitivamente.

Puedes tener hasta 20 rutinas, incluidas las que estén en pausa. Detén una para añadir otra.

Si eliges **Pedir cambios** en la tarea de una rutina, o escribes en su chat, y la nota debe aplicarse a todas las ejecuciones, como «no uses nunca emojis», la tarea te ofrece **Cambiar también la rutina**, tanto en la tarea como en el chat, debajo de la respuesta. Muestra qué cambiará en las instrucciones de la rutina, que solo se modifica cuando tocas **Cambiarla**. **Dejarla así** la deja como está. Si la corrección es solo para ese borrador, no se ofrece esta opción.

## Avanzado: pasos de script

No necesitas ningún script: describe con tus propias palabras qué debe hacer una rutina y tu Machine se encarga del resto.

Si tienes experiencia, también puedes ejecutar tus propios comandos en tu Machine desde una rutina: en el menú ⋯, elige **Avanzado: pasos de script**. **Editar** solo los muestra cuando la rutina ya tiene alguno. **Obtener datos** ejecuta primero un comando, en su carpeta (tu carpeta de inicio si la dejas vacía) durante el número de segundos que indiques, como máximo. Lo que imprima se pasa a la rutina para que trabaje con ello. Si no hay instrucciones, lo que imprima será el resultado.

**Comprobación** recibe el resultado como entrada después de la ejecución. Si termina con un error, la rutina muestra **No funcionó** e indica lo que dijo la comprobación. Si falla un comando de Obtener datos, se muestra lo mismo.

Un comando ocupa una línea y se ejecuta sin shell: no admite tuberías ni variables. Tú defines los pasos de script, y solo en tu propio panel. Una prueba y **Probarlo** también ejecutan Obtener datos y lo indican; aun así, no envían ni guardan nada. Una rutina nunca envía nada, así que los pasos de script solo deben leer.

## Desde tus trabajos de OpenClaw

Si antes creaste trabajos programados en OpenClaw, tu Machine los lee (nunca los cambia) y ofrece como rutinas, en **Sugerido**, los que encajan. Cada uno se ha ejecutado una vez, así que ves un resultado real.

Conserva tus correcciones al trabajo y omite lo que haya enviado o publicado. Si un trabajo ejecutó un script, o leyó datos recopilados por un trabajo con script, los incluye como Obtener datos. **Añadir** lo convierte en una rutina y **No, gracias** hace que no vuelva a preguntarte por ese trabajo. Si un trabajo te recordaba hacer algo, se ofrece como una tarea periódica en Tareas.

Antes de añadir una sugerencia, puedes cambiarla, como cualquier rutina, con **Editar** y **Cambiar cuándo**, en su menú ⋯. **Ejecutar de nuevo** la ejecuta ahora con las instrucciones actuales para que veas resultados más recientes, por ejemplo, después de un fin de semana tranquilo. Solo lee, se ejecuta una vez por cada toque y el nuevo resultado reemplaza al anterior.

Puede haber hasta tres sugerencias a la vez. Después de una semana de ejecuciones correctas, la rutina pregunta **¿Desactivar el antiguo trabajo de OpenClaw?**. Solo lo desactiva si tocas **Desactivar**; puedes volver a activarlo en OpenClaw. **Mantener** deja los dos en marcha.

## Según lo que haces

Tu Machine también detecta las tareas que haces con cierta frecuencia y las ofrece como rutinas en **Sugerido**, aunque no uses OpenClaw. Busca:

- la misma petición tres veces seguidas o más, como «resume los tickets de soporte abiertos» todos los lunes;
- un correo que envías periódicamente, como un informe semanal a tu equipo;
- boletines y correos de novedades que llegan cada semana;
- un canal de Slack con mucha actividad en el que otras personas escriben cada semana;
- correos que reenvías de uno en uno a la misma persona, como correos del colegio y del club a tu pareja: un resumen semanal le ahorraría tener que reenviarlos;
- la misma solicitud a la que respondes periódicamente, como una aprobación mensual para la misma persona.

Cada sugerencia indica lo que ha detectado, como «La has pedido 4 veces seguidas» o «Has reenviado 6 correos a Sam en 3 semanas», y se ha ejecutado una vez para que veas un resultado real. Puede servir para resumir el equipo, preparar información antes de una llamada semanal, resumir soporte o desarrollo, revisar tus cifras o reunir los boletines que recibes.

Solo sugiere cosas concretas para ti y claramente útiles: un resumen de noticias solo incluirá tus propios boletines, nunca uno genérico. Si nada encaja, no se muestra ninguna sugerencia.

Busca como máximo una vez al día y muestra como máximo una sugerencia nueva por semana, sin enviar notificaciones. **No, gracias** hace que esa sugerencia no vuelva a aparecer. Los reenvíos y las respuestas se quedan en la cuenta desde la que se enviaron, así que Trabajo y Personal no se mezclan. Todo se queda en tu Machine. Si completas una tarea de forma periódica, se ofrece como tarea periódica.

## Rutinas y tareas periódicas

Una [tarea periódica](recurring.md) te recuerda que hagas algo. Una rutina es un trabajo que tu Machine hace por su cuenta y te muestra. Usa una tarea periódica para «pagar el alquiler el día 1» y una rutina para «todos los viernes, dime qué oportunidades se han quedado paradas».
