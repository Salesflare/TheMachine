---
title: Rutinas
area: cards
summary: Trabajo que tu Machine hace por su cuenta y con cierta frecuencia, como un resumen de tus oportunidades abiertas cada lunes. Solo lee.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: ed2171ef31eb6213
---
## Crear una rutina

Abre **Rutinas** en la barra lateral y escribe en una línea qué debe hacer y cuándo: «cada lunes a las 9, resume mis oportunidades abiertas» o «cada mañana entre semana, enumera los correos a los que todavía tengo que responder». Después, pulsa **Añadir**.

Si no indicas una hora, se ejecuta a las 8:00. La hora se basa en el reloj de tu Machine. La primera vez que se ejecuta, se le asigna un nombre corto.

Al pulsar **Añadir** por primera vez, se ejecuta una prueba para que veas el resultado antes de conservarla. No se envía ni se guarda nada. Después, **Añadir** la deja activada para que se ejecute con la frecuencia indicada, **Cambiar** prueba otras palabras o un nombre nuevo y **Cancelar** la descarta.

## Plantillas

En **Plantillas**, al final de Rutinas, **Añadir** activa una rutina prediseñada. Se ejecuta una vez enseguida y luego cada mañana a las 7:30 (Limpieza de spam, cada hora; Suscripciones y pruebas, una vez al mes). Su tarjeta muestra las instrucciones, como cualquier rutina, y **Editar** permite cambiarlas o cambiar el nombre.

Cuando recibes muchos newsletters y Limpieza de newsletters está desactivada (25 o más en una semana, de al menos 5 remitentes), aparece una línea encima de tus tareas que indica cuántos llegaron y qué haría, con las opciones **Activarla** y **No, gracias**.

Limpieza de spam se ofrece de la misma forma si durante una semana moviste manualmente 5 o más correos a spam. **Activarla** la añade igual que **Añadir** aquí. Si pulsas **No, gracias**, no volverá a ofrecerse. Tampoco volverá a ofrecerse una plantilla que ya habías rechazado.

**Limpieza de newsletters** crea una tarea por área (trabajo y personal) con los newsletters del día anterior. Cada uno incluye las opciones **Mantener** o **Darse de baja**. Para darte de baja, usa el enlace de un solo clic de la lista o, si el envío está activado, el correo para darse de baja desde tu dirección. Si no, The Machine se da de baja en la página de la lista, desde su propio navegador. Si hace falta iniciar sesión, resolver un captcha o elegir opciones, te toca hacerlo a ti: la fila explica el motivo e incluye **Abrir página de baja**.

Se excluyen los recibos, los pedidos y los avisos de pago. Los correos recibidos a través de una dirección de grupo, como un grupo de Google, aparecen con el nombre de quien los escribió y nunca te dan de baja del grupo. Si el remitente no ofrece una opción para darse de baja, la fila muestra **Darse de baja a mano**.

**Limpieza de spam** crea una tarea por área con los correos de remitentes desconocidos que parecen spam. Cada uno incluye las opciones **Spam** o **No es spam**. Outlook mueve el spam a Correo no deseado y Gmail lo marca como spam. La rutina revisa el correo cada hora, así que normalmente el spam ya está identificado cuando lo consultas. El spam nuevo se añade a la misma tarea mientras siga abierta.

Si Gmail está conectado en modo de solo lectura, como en una Machine alojada, no se pueden mover correos a spam. En ese caso, **Spam** muestra un enlace para marcarlo en Gmail y The Machine recuerda que ese remitente es spam. Si no hay ninguna cuenta de correo conectada, la plantilla muestra **Conectar correo** en lugar de **Añadir**.

Se considera desconocido a alguien a quien nunca le has escrito. Un «Re:» solo cuenta como conversación si has escrito en ese hilo. Si vuelve a llegarte un correo de un remitente que marcaste como spam, ya sea desde la tarea o en tu buzón, aparecerá en la siguiente tarea con la etiqueta **Marcado como spam antes**. Los correos que tú hayas movido a spam también ayudan a detectar otros parecidos.

No cambia nada hasta que lo confirmas en la tarea. Toca el remitente para leer el correo antes: seguirá sin leerse y no cambiará nada. En Limpieza de spam, las imágenes de la web no se cargan, así que el remitente no puede saber que abriste el correo. No volverá a preguntarte por los remitentes sobre los que ya decidiste. Si un día no recibes newsletters ni spam, no se crea ninguna tarea. Estas tareas nunca envían notificaciones.

Cuando hayas decidido qué hacer con todos los remitentes, la tarea indicará que está terminada y aparecerá **Marcar como hecha**.

**Resumen diario** elige una vez al día, en una sola tarea, los pocos artículos de newsletters que vale la pena leer. Cada uno incluye una frase que explica por qué te interesa. Tócalo para leer el correo o usa **Abrir en tu correo**. Solo incluye newsletters: nunca correos de personas, recibos ni remitentes de los que te hayas dado de baja, y nunca contenido que ya hayas leído. Si nada destaca, no se crea ninguna tarea.

Aprende qué te interesa a partir de lo que abres, marcas con una estrella o archivas sin leer, y de las opciones **Más como esto** y **Menos como esto** de cada sugerencia. Los temas que busca aparecen en la tarjeta de la rutina, debajo de **Más de** y **Menos de**. Quita un tema con × o añade uno propio. Los temas con línea discontinua los ha aprendido por su cuenta. Un resumen nuevo reemplaza al que esté abierto y nunca envía notificaciones.

Solo lee el remitente, el asunto y el comienzo de cada newsletter nuevo, y le hace una pregunta breve a tu IA sobre ellos, con un límite diario para que resulte económico. **Cambiar cuándo** permite cambiar la hora. Cuando cambias las instrucciones, se ejecuta como cualquier rutina, siguiendo tus instrucciones.

**Cumpleaños** crea una tarea por cada contacto cercano que cumpla años hoy: personas a las que sueles escribir, como amistades, familiares y contactos habituales. Incluye un saludo breve preparado en el lugar donde normalmente hablas con esa persona, como su chat de WhatsApp o el hilo de correo, y en su idioma. Solo se envía si tú lo mandas. Si nadie cumple años, no se crea ninguna tarea.

Los cumpleaños se obtienen de tus calendarios (los eventos de cumpleaños de Google y el calendario Cumpleaños, que se consultan cada mañana aunque no estén sincronizados, y el calendario Cumpleaños de Outlook), de tus contactos de Google en una Machine autoalojada y de un campo de fecha llamado Birthday en una persona del Graph. Si todavía no hay cumpleaños en ninguno de esos lugares, el resultado indica **Aún no hay información sobre cumpleaños** y explica cómo añadirla.

**Importar cumpleaños de Facebook**: cuando Cumpleaños esté activada, una tarea te ofrecerá leer la página de cumpleaños de Facebook. Pulsa **Importar** y The Machine abrirá la página en su navegador, se desplazará hasta cargar todos los meses y leerá el nombre y el cumpleaños de cada amistad. Te mostrará cuántos encontró y quiénes coincidieron con personas de tu Graph por nombre y apellido. Si hay más de una persona con el mismo nombre, se omiten y se muestran en una lista.

Solo **Guardar** los añade, en la página de cada persona: el cumpleaños y la foto de perfil de Facebook si esa persona todavía no tiene foto. Los cumpleaños y las fotos que ya hayas añadido se conservan, y nunca se reemplaza una foto que la persona ya tenga. No se escribe nada en Facebook.

No vuelve a leer la página por su cuenta: para hacerlo, pulsa **Importar de nuevo** en la tarea. El navegador debe tener una sesión iniciada en Facebook. Si no la tiene, pulsa **Iniciar sesión en Facebook** en la tarea e inicia sesión allí. Cuando lo hayas hecho, leerá la página automáticamente. The Machine nunca inicia sesión por ti.

Se cuentan las amistades que nadie de tu Graph tiene, y se muestran algunos nombres. **Añadir … como contactos personales** las añade todas de una vez, también después de pulsar **Guardar**: cada una con su nombre y cumpleaños, que nunca se comparten con una Fleet de trabajo. Se omite a quien ya tenga una persona con el mismo nombre en tu Graph o haya sido eliminado definitivamente. Los recordatorios de cumpleaños solo llegan para las personas a las que escribes.

La opción **Deshacer** de la tarea elimina exactamente a esas personas, incluso después de pulsar **Importar de nuevo**.

**Suscripciones y pruebas** revisa tus recibos, facturas y avisos de renovación una vez al mes, y reúne tus suscripciones en una tarea. Muestra cuánto cuesta cada una, cuándo será el próximo cobro y señala si una prueba está por terminar o si sube el precio. Solo incluye las que puede identificar con seguridad. Si no encuentra ninguna, no se crea una tarea.

Elige **Mantener** o **Cancelar** para cada una. No volverá a preguntarte por una suscripción que decidas mantener, salvo que cambie el precio. **Cancelar** muestra la página para cancelar o un borrador para pedir la cancelación, que solo se envía cuando tú lo mandas. Entre una ejecución y otra, revisa cada día y crea una tarea si se acerca un cobro de renovación o si una prueba termina en los próximos 7 días.

Mientras una rutina de plantilla conserve las instrucciones de la plantilla, se ejecuta con código propio, sin usar el plan de IA (Limpieza de spam primero enumera con código los correos nuevos de remitentes desconocidos y solo le hace una pregunta breve a tu IA si hay alguno). Si le cambias el nombre, eso se mantiene. Cuando cambias las instrucciones, se ejecuta como cualquier rutina, siguiendo tus instrucciones.

Limpieza de newsletters y Limpieza de spam siguen creando una misma tarea con una opción para cada correo. Si editas Cumpleaños, muestra el resultado y, como máximo, un borrador, no una tarea por persona. **Volver a la plantilla**, en **Editar**, restaura sus instrucciones.

## Qué hace una rutina

A la hora programada, tu Machine lee lo que necesita, como tus mensajes, reuniones y el Graph, y publica el resultado en la página Rutinas. Cada resultado muestra **Para revisar**, **Nada nuevo** (con el motivo) o **No funcionó** (con el motivo). Si una ejecución termina sin resultado, cuenta como fallida, nunca como completada.

Las rutinas solo leen: tus mensajes, páginas web, GitHub y sitios como X en el navegador. No envían mensajes, responden, publican ni cambian nada. Solo una plantilla puede modificar el correo, y únicamente lo que confirmes en su tarea.

Si una rutina debe terminar con una publicación o un mensaje, hace todo lo necesario hasta ese paso y muestra el borrador, por ejemplo, **Se publicaría en X:**. Después de una ejecución real, aparece como una tarea para que la apruebes. Una ejecución de prueba solo muestra el resultado. El nombre indica de qué trata y dónde se publicaría, el botón nombra el paso, como **Publícalo**, y **Desde tu rutina**, debajo, abre la rutina.

La tarea empieza en el área de la cuenta desde la que se publicaría, como Trabajo para la cuenta de X de tu empresa, así que nunca te pide que la muevas.

Una ejecución puede seguir tus [habilidades](skills.md) activadas, según lo que haga la rutina: solo se leen completas las que correspondan. El resultado las enumera debajo de **Usado:**. Una habilidad nunca hace que una rutina envíe o cambie nada.

Tus rutinas están en **Tus rutinas**, debajo de las sugerencias. Los resultados largos se contraen y muestran una vista previa breve. **Mostrar más**, o tocar el resultado, lo abre.

Cada ejecución conoce el último resultado, así que puede indicar qué cambió desde entonces.

Después de una ejecución correcta, tu Machine puede crear una receta para automatizar las consultas que siempre son iguales, como qué correos o cambios de GitHub debe revisar. En las siguientes ejecuciones, primero los revisa con código sencillo. Luego, la IA elige lo que importa y lo redacta con menos tokens. La receta solo lee. Si deja de funcionar, la rutina se ejecuta por su cuenta y la corrige. La receta aparece debajo de **Avanzado: pasos de script**, en el menú ⋯.

## Días sin ejecución

Si tu Machine estaba apagada u ocupada, no acumula las ejecuciones pendientes: solo ejecuta la más reciente, una vez. Cada fecha se ejecuta una sola vez, incluso después de reiniciar.

Las rutinas se ejecutan de una en una y esperan si queda poco uso en tu plan de IA, como cualquier tarea en segundo plano. **Ejecutar ahora** la inicia enseguida. El resultado aparece en la tarjeta cuando esté listo.

## Cambiarla o detenerla

Estas opciones están en el menú ⋯ de la rutina. **Editar** cambia el nombre y lo que hace, pero conserva el horario y los resultados anteriores. **Cambiar cuándo** permite indicar una nueva frecuencia con tus propias palabras, como «cada día laborable a las 8». Ambas opciones incluyen **Guardar** y **Cancelar**. En una computadora, también puedes cancelar con Esc o haciendo clic fuera.

En **Editar**, **Probarlo** ejecuta una vez las instrucciones nuevas y muestra el resultado allí. La rutina no cambia hasta que pulses **Guardar**.

**Pausar** detiene las ejecuciones hasta que pulses **Reanudar** en su tarjeta. Las rutinas en pausa se encuentran debajo de tus rutinas, en **En pausa**, y las ejecuciones que se hayan perdido durante la pausa no se ejecutan después. **Detener** termina la rutina definitivamente.

Puedes tener hasta 20 rutinas, incluidas las que estén en pausa. Detén una para añadir otra.

Si usas **Pedir cambios** en una tarea de la rutina o escribes en su chat, y tu nota debe aplicarse a todas las ejecuciones, como «no uses nunca emojis», la tarea te ofrece **Cambiar también la rutina**. La opción aparece en la tarea y en su chat, debajo de la respuesta. Muestra qué cambiará en las instrucciones de la rutina. La rutina solo cambia cuando pulsas **Cambiarla**. **Dejarla así** la mantiene como está. Si solo quieres corregir ese borrador, no se ofrece esta opción.

## Avanzado: pasos de script

No necesitas usar scripts: describe con tus propias palabras qué debe hacer una rutina y tu Machine se encarga del resto.

Si tienes experiencia, también puedes hacer que una rutina ejecute tus propios comandos en tu Machine: elige **Avanzado: pasos de script** en el menú ⋯. **Editar** solo los muestra cuando la rutina ya tiene alguno. **Obtener datos** ejecuta primero un comando en su carpeta (tu carpeta de inicio si no indicas una), durante un máximo de los segundos que hayas establecido. El resultado que imprime se pasa a la rutina para que lo use. Si no hay instrucciones, ese resultado se convierte en el resultado de la rutina.

**Comprobación** recibe el resultado como entrada después de la ejecución. Si el comando termina con un error, la rutina muestra **No funcionó** junto con el mensaje de la comprobación. Si falla un comando de Obtener datos, muestra lo mismo.

Los comandos deben estar en una sola línea y se ejecutan sin shell: no se admiten tuberías ni variables. Los pasos de script son tuyos y solo se configuran en tu panel. Las ejecuciones de prueba y **Probarlo** también ejecutan Obtener datos y lo indican. No envían nada ni guardan nada. Las rutinas nunca envían nada, así que los pasos de script solo deben leer.

## Desde tus trabajos de OpenClaw

Si antes creaste trabajos programados en OpenClaw, tu Machine los lee (nunca los modifica) y ofrece como rutinas los que encajan, en **Sugerido**. Cada uno ya se ejecutó una vez, así que puedes ver un resultado real.

Conserva las correcciones que hayas hecho al trabajo y excluye lo que haya enviado o publicado. Si un trabajo ejecutó un script o leyó datos recopilados por un trabajo con script, lo añade como Obtener datos. **Añadir** lo convierte en una rutina. **No, gracias** hace que no vuelva a preguntar por ese trabajo. Si un trabajo te recordaba que hicieras algo, aparece en Tareas como una oferta de tarea recurrente.

Antes de añadir una sugerencia, puedes cambiarla como cualquier rutina con **Editar** y **Cambiar cuándo**, en su menú ⋯. **Ejecutar de nuevo** la ejecuta ahora con las instrucciones actuales para mostrar resultados más recientes, por ejemplo, después de un fin de semana tranquilo. Solo lee, se ejecuta una vez por toque y su nuevo resultado reemplaza al anterior.

Puede haber hasta tres sugerencias pendientes a la vez. Después de una semana de buenas ejecuciones, la rutina pregunta **¿Desactivar el antiguo trabajo de OpenClaw?**. Solo se desactiva si pulsas **Desactivar** y puedes volver a activarlo en OpenClaw. **Mantener** deja ambos en funcionamiento.

## A partir de lo que haces

Tu Machine también detecta tareas que haces con cierta frecuencia y te las ofrece como rutinas en **Sugerido**, incluso si no usas OpenClaw. Busca:

- la misma petición tres veces seguidas o más, como «resume los tickets de soporte abiertos» cada lunes;
- un correo que envías con cierta frecuencia, como un informe semanal para tu equipo;
- newsletters y correos de novedades que llegan todas las semanas;
- un canal activo de Slack en el que otras personas escriben todas las semanas;
- correos que reenvías uno por uno a la misma persona, como los del colegio y las actividades extraescolares a tu pareja: un resumen semanal para esa persona evita que tengas que reenviarlos;
- la misma solicitud a la que respondes con cierta frecuencia, como una aprobación mensual para la misma persona.

Cada sugerencia indica qué detectó, por ejemplo, «Petición repetida 4 veces seguidas» o «Reenviaste 6 correos a Sam en 3 semanas». Además, ya se ejecutó una vez, así que puedes ver un resultado real. Puede servir, por ejemplo, para hacer un resumen del equipo, prepararte para una llamada semanal, resumir información de soporte o desarrollo, seguir tus cifras o resumir los newsletters que recibes.

Solo sugiere rutinas que sean específicas para ti y claramente útiles: un resumen de noticias solo incluiría tus propios newsletters, nunca uno genérico. Si no encuentra nada adecuado, no muestra ninguna sugerencia.

Busca como máximo una vez al día y presenta como máximo una sugerencia nueva por semana, sin enviar notificaciones. **No, gracias** hace que esa sugerencia no vuelva a aparecer. Los reenvíos y las respuestas permanecen en la cuenta desde la que se enviaron, así que Trabajo y Personal no se mezclan. Todo permanece en tu Machine. Una tarea que cierres con cierta frecuencia se ofrece como tarea recurrente.

## Rutinas y tareas recurrentes

Una [tarea recurrente](recurring.md) te recuerda que tienes que hacer algo. Una rutina es trabajo que tu Machine hace por su cuenta y te muestra. Usa una tarea recurrente para «pagar el alquiler el día 1» y una rutina para «cada viernes, dime qué oportunidades se han quedado estancadas».
