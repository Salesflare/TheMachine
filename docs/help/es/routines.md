---
title: Rutinas
area: cards
summary: Trabajo que tu Machine hace por su cuenta con cierta frecuencia, como un resumen de tus oportunidades abiertas cada lunes. Solo lee.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours
translated: 3e6d9d8d446a5dde
---
## Crear una rutina

Abre **Rutinas** en la barra lateral y escribe en una línea qué debe hacer y cuándo: «todos los lunes a las 9, resume mis oportunidades abiertas» o «cada mañana de lunes a viernes, enumera los correos a los que aún tengo que responder». Luego, toca **Añadir**.

Si no indicas una hora, se ejecuta a las 8:00. La hora es la del reloj de tu Machine. La primera vez que se ejecuta, recibe un nombre corto.

Al principio, **Añadir** ejecuta una prueba para que veas el resultado antes de guardarla. No se envía ni se guarda nada. Después, **Añadir** la deja activa para que se ejecute con regularidad, **Cambiar** prueba otras palabras o un nombre nuevo y **Cancelar** la descarta.

## Plantillas

En **Plantillas**, al final de Rutinas, **Añadir** activa una rutina prediseñada. Se ejecuta una vez enseguida y luego cada mañana a las 7:30 (Limpieza de spam cada hora, Hallazgos de segunda mano cada 3 horas, Suscripciones y pruebas una vez al mes). Su tarjeta muestra las palabras que usa, como cualquier rutina, y **Editar** permite cambiarlas o cambiar su nombre.

Cuando recibes muchos newsletters y Limpieza de newsletters está desactivada (25 o más en una semana, de al menos 5 remitentes), aparece una línea encima de tus tareas que indica cuántos recibiste y qué haría la rutina, con las opciones **Activarla** y **No, gracias**.

Limpieza de spam se ofrece de la misma manera cuando, durante una semana, has movido a spam 5 o más correos manualmente. **Activarla** la añade igual que **Añadir** aquí. Si tocas **No, gracias**, no volverá a ofrecerse. Tampoco volverá a ofrecerse una plantilla que ya tuvieras.

**Limpieza de newsletters** crea una tarea por área (trabajo y personal) con los newsletters del último día. Cada uno incluye las opciones **Mantener** o **Darse de baja**. Para darte de baja, usa el enlace de un solo clic de la lista o envía un correo desde tu dirección, si el envío está activado. Si no, The Machine se da de baja en la página de la lista desde su propio navegador. Si allí tienes que iniciar sesión, resolver un captcha o elegir alguna opción, tendrás que hacerlo tú. La fila indica el motivo y muestra **Abrir página de baja**.

Se excluyen los recibos, los pedidos y los avisos de pago. Los correos que llegan a través de una dirección de grupo, como un Google Group, aparecen bajo el nombre de quien los escribió y nunca te dan de baja del grupo. Si el remitente no tiene su propio sistema para darse de baja, la fila muestra **Darse de baja a mano**.

**Limpieza de spam** crea una tarea por área con correos de remitentes desconocidos que parecen spam. Cada uno incluye las opciones **Spam** o **No es spam**. Outlook mueve el spam a Correo no deseado y Gmail lo marca como spam. La rutina comprueba cada hora, así que normalmente el spam ya está detectado antes de que lo revises. El spam nuevo se añade a la misma tarea mientras siga abierta.

Una cuenta de Gmail conectada con acceso de solo lectura, como en una Machine alojada, no puede mover correos a spam. En ese caso, **Spam** incluye un enlace para marcarlo en Gmail, y The Machine recuerda que el remitente es spam. Si no hay ninguna cuenta de correo conectada, la plantilla muestra **Conectar correo** en lugar de **Añadir**.

Se considera desconocido a alguien a quien nunca has escrito. Un «Re:» solo cuenta como conversación si tú escribiste en el hilo. Si vuelve a llegarte un correo de un remitente que marcaste como spam, ya sea desde la tarea o en tu buzón, aparecerá en la siguiente tarea como **Marcado como spam antes**. Los correos que tú mismo moviste a spam también ayudan a detectar mensajes similares.

Nada cambia hasta que lo confirmas en la tarea. Toca un remitente para leer primero el correo: seguirá sin leerse y nada cambiará. En Limpieza de spam, las imágenes de la web no se cargan, así que el remitente no puede saber que lo abriste. No volverá a preguntarte por los remitentes sobre los que ya hayas decidido. Si en un día no hay newsletters ni spam, no se crea ninguna tarea. Estas tareas nunca envían notificaciones.

Cuando hayas decidido sobre todos los remitentes, la tarea indicará que está terminada y mostrará **Marcar como hecha**.

**Resumen diario** selecciona en una sola tarea, una vez al día, los pocos artículos de newsletters que merecen tu atención. Cada uno incluye una línea que explica por qué te interesa. Tócalo para leer el correo o usa **Abrir en tu correo**. Solo incluye newsletters, nunca correos de personas, recibos ni remitentes de los que te hayas dado de baja. Tampoco incluye mensajes que ya hayas leído. Si nada destaca, no se crea ninguna tarea.

La rutina aprende qué te interesa a partir de lo que abres, marcas con una estrella o archivas sin leer, y de las opciones **Más como esto** y **Menos como esto** de cada selección. Los temas que usa para seleccionar aparecen en la tarjeta de la rutina, bajo **Más de** y **Menos de**. Elimina un tema con × o añade uno propio. Los temas con línea discontinua los ha aprendido por su cuenta. Cada nuevo resumen sustituye al que esté abierto y nunca envía notificaciones.

Solo lee el remitente, el asunto y el comienzo de cada newsletter nuevo, y le hace a tu IA una pregunta breve sobre ellos, con un límite diario, para que el coste sea bajo. **Cambiar cuándo** permite cambiar la hora. Cuando cambias las palabras de la rutina, se ejecuta como cualquier otra rutina con las palabras que escribiste.

**Cumpleaños** crea una tarea por cada contacto cercano que cumple años hoy: personas a las que escribes tú, como amistades, familiares y contactos habituales. Para cada persona, prepara un saludo breve en el lugar donde sueles hablar con ella, como su chat de WhatsApp o el hilo de correo, y en su idioma. Solo se envía cuando lo envías tú. Si nadie cumple años ese día, no se crea ninguna tarea.

Los cumpleaños se obtienen de tus calendarios (los eventos de cumpleaños de Google y el calendario Cumpleaños, que se leen cada mañana aunque no estén sincronizados, y el calendario Cumpleaños de Outlook), tus contactos de Google en una Machine alojada por ti y un campo de fecha llamado Birthday en una persona de Graph. Si todavía no hay ningún cumpleaños en esas fuentes, el resultado indica **Aún no hay información sobre cumpleaños** y explica cómo añadirla.

**Importar cumpleaños de Facebook**: cuando Cumpleaños esté activada, una tarea te ofrecerá leer la página de cumpleaños de Facebook. Toca **Importar** y The Machine abrirá la página en su navegador, se desplazará hasta que se hayan cargado todos los meses y leerá el nombre y el cumpleaños de cada amistad. Te mostrará cuántos encontró y quiénes coincidían con personas de tu Graph por nombre y apellido. Si más de una persona tiene el mismo nombre, se omitirá y aparecerá en una lista.

Solo **Guardar** los añade, en la página de cada persona: el cumpleaños y la foto de perfil de Facebook, si esa persona todavía no tiene foto. Los cumpleaños y las fotos que añadas allí se conservarán, y nunca se reemplazará una foto que ya tenga la persona. No se escribe nada en Facebook.

La rutina no vuelve a leerlos por su cuenta. Para hacerlo, toca **Importar de nuevo** en la tarea. El navegador debe tener una sesión iniciada en Facebook. Si no la tiene, toca **Iniciar sesión en Facebook** en la tarea e inicia sesión allí. Cuando hayas iniciado sesión, la rutina leerá la página automáticamente. The Machine nunca inicia sesión por ti.

También se cuentan las amistades que no están en tu Graph y se muestran algunos nombres. **Añadir … como contactos personales** las añade todas de una vez, también después de tocar **Guardar**. Cada contacto incluirá su nombre y cumpleaños, y nunca se compartirá con una Fleet de trabajo. Se omite a quien ya tenga alguien con ese nombre en tu Graph o haya sido eliminado de forma permanente. Los recordatorios de cumpleaños siguen llegando solo para las personas a las que escribes.

**Deshacer** en la tarea elimina exactamente esos contactos, incluso después de tocar **Importar de nuevo**.

**Suscripciones y pruebas** revisa una vez al mes tus recibos, facturas y avisos de renovación, y reúne tus suscripciones en una sola tarea. Indica cuánto cuesta cada una, cuándo se cobrará de nuevo y si termina una prueba o sube el precio. Solo muestra las que ha podido identificar con seguridad. Si no encuentra ninguna, no se crea ninguna tarea.

Elige **Mantener** o **Cancelar** para cada suscripción. No volverá a preguntarte por las que mantengas, salvo que cambie su precio. **Cancelar** muestra la página para darla de baja o un borrador para pedir que la cancelen. El mensaje solo se envía cuando lo envías tú. Entre una revisión mensual y otra, comprueba cada día y crea una tarea si faltan 7 días o menos para que termine una prueba o se renueve una suscripción.

**Mantenerse en contacto** te recuerda de vez en cuando que escribas a alguien cercano, solo cuando hay un motivo real. En su tarjeta, elige quiénes formarán parte de la rutina de una lista breve de personas con las que hablas directamente, en ambos sentidos, desde hace meses. Elimina a alguien con ×.

Solo recibirás un recordatorio cuando lleves mucho más tiempo de lo habitual sin hablar con esa persona y haya algo concreto que decir: una noticia que compartió, una promesa pendiente o un mensaje que nunca respondiste. La rutina crea una tarea con el motivo y un mensaje breve, redactado en el lugar donde sueles hablar con esa persona y en su idioma. Solo se envía cuando lo envías tú. Si no hay nada que decir, no se crea ninguna tarea.

Envía como máximo dos recordatorios por semana y uno por persona al mes. No envía ninguno a alguien con quien hayas hablado hace poco. Si tocas **No hace falta** en un recordatorio, esperará más tiempo antes de volver a recordarte que escribas a esa persona, y esperará aún más cada vez que lo hagas. Nunca envía notificaciones y siempre es personal: nunca se comparte con una Fleet de trabajo.

**Hallazgos de segunda mano** sigue una búsqueda en un sitio de artículos de segunda mano, como Marktplaats, Vinted, eBay o Facebook Marketplace. Haz una búsqueda en el sitio con los filtros que quieras, copia la dirección de los resultados y pégala después de tocar **Añadir**. Si quieres, añade filtros con tus propias palabras, como «menos de 300, a menos de 30 km, sin “para piezas”». Cada búsqueda es una rutina independiente, así que vuelve a añadirla para crear otra.

Cada 3 horas, abre la búsqueda en el navegador propio de The Machine y busca anuncios que todavía no haya visto. Primero comprueba el precio, la distancia y las palabras que excluiste, con código sencillo.

Abre cada anuncio nuevo que cumpla los requisitos. Tu IA evalúa el estado a partir de la foto y la descripción, y al vendedor a partir de sus reseñas, valoración y antigüedad de la cuenta. Los anuncios que parecen buenos aparecen en una sola tarea, cada uno con su foto, título, precio y un veredicto de una línea. Toca un anuncio para abrirlo en el navegador de The Machine.

Mientras la tarea esté abierta, los nuevos hallazgos se añaden al principio, aumenta el número y vuelve a llegarte una notificación, porque las buenas ofertas se agotan rápido. Cuando marques la tarea como hecha, el siguiente hallazgo crea una nueva. Si una búsqueda no encuentra nada interesante, no cambia nada.

La rutina procura ser respetuosa y económica: lee la búsqueda una vez por ejecución, abre como máximo 6 anuncios por ejecución con una pausa entre ellos y comprueba como máximo 40 anuncios al día entre todas tus búsquedas. Cada comprobación es una pregunta breve a tu IA con una foto. La primera vez comprueba los anuncios más recientes y considera vistos los demás, así que las siguientes veces solo muestra lo nuevo.

Si el sitio te pide iniciar sesión, muestra una comprobación para robots o impide la lectura, una tarea te lo indicará y mostrará **Abrir** para que lo veas en el navegador de The Machine. Inicia sesión o resuelve la comprobación tú mismo allí. La siguiente ejecución volverá a leer la página. The Machine nunca inicia sesión ni resuelve comprobaciones por ti, y nunca contacta con vendedores, puja ni compra.

**Cambiar búsqueda** en la tarjeta de la rutina permite usar otra dirección o cambiar los filtros. **Cambiar cuándo** permite cambiar la frecuencia, por ejemplo, a «cada 6 horas».

Mientras la rutina de una plantilla conserve las palabras de la plantilla, se ejecuta con código propio, sin usar el plan de tu IA (Limpieza de spam primero enumera con código los correos nuevos de remitentes desconocidos y solo le hace a tu IA una pregunta breve si hay alguno; Mantenerse en contacto solo pregunta por una o dos personas que haya seleccionado). Si cambias el nombre, seguirá funcionando así. Cuando cambias las palabras de la rutina, se ejecuta como cualquier otra rutina con las palabras que escribiste.

Limpieza de newsletters y Limpieza de spam siguen creando una sola tarea con una opción por correo. Una rutina Cumpleaños editada muestra su resultado y como máximo un borrador, no una tarea por persona. Toca **Volver a la plantilla** en **Editar** para restaurar las palabras originales.

## Qué hace una rutina

A la hora programada, tu Machine lee lo que necesita, como tus mensajes, reuniones y Graph, y muestra el resultado en la página Rutinas. Cada resultado indica **Para revisar**, **Nada nuevo** (y el motivo) o **No funcionó** (y el motivo). Una ejecución que termina sin resultado cuenta como fallida, nunca como completada.

Las rutinas solo leen: tus mensajes, páginas web, GitHub y sitios como X en el navegador. No envían mensajes, responden, publican ni cambian nada. Solo una plantilla modifica el correo, y solo lo que confirmes en su tarea.

Si el trabajo de una rutina termina con una publicación o un mensaje, la rutina completa todos los pasos anteriores y muestra el borrador, como **Se publicaría en X:**. Después de una ejecución real, aparece como una tarea para que la apruebes. Una ejecución de prueba solo muestra el borrador. El nombre indica de qué trata y dónde se publicaría. El botón indica el paso, como **Publícalo**, y **Desde tu rutina**, debajo, abre la rutina.

La tarea aparece primero en el área de la cuenta desde la que se enviaría, como Trabajo para la cuenta de X de tu empresa, así que nunca te pedirá que la muevas.

Una ejecución puede seguir las [habilidades](skills.md) activadas que correspondan a lo que hace la rutina. Solo se leen completas las que son pertinentes. El resultado las enumera bajo **Usadas:**. Una habilidad nunca hace que una rutina envíe ni cambie nada.

Tus rutinas aparecen en **Tus rutinas**, debajo de las sugerencias. Los resultados largos se pliegan para mostrar una vista previa breve. Toca **Mostrar más** o el resultado para abrirlo.

Cada ejecución conoce el último resultado, así que puede indicar qué ha cambiado desde entonces.

Después de una buena ejecución, tu Machine puede escribir por su cuenta una receta para las lecturas que se repiten cada vez, como qué correos o cambios de GitHub revisar. En las siguientes ejecuciones, primero los lee con código sencillo. Después, la IA selecciona lo importante y lo redacta con menos tokens. La receta solo lee. Si deja de funcionar, la rutina vuelve a leer por su cuenta y la corrige. La receta aparece en **Avanzado: pasos de script**, en el menú ⋯.

## Días sin actividad

Si tu Machine estaba apagada u ocupada, las ejecuciones pendientes no se acumulan: solo se ejecuta la más reciente, una vez. Cada fecha se ejecuta una sola vez, incluso después de reiniciar.

Las rutinas se ejecutan de una en una y esperan cuando queda poco uso disponible en el plan de tu IA, como el resto del trabajo en segundo plano. **Ejecutar ahora** la inicia enseguida. El resultado aparece en la tarjeta cuando esté listo.

## Cambiar o detener una rutina

Estas opciones están en el menú ⋯ de la rutina. **Editar** permite cambiar el nombre y lo que hace. La hora de ejecución y los resultados anteriores se mantienen. **Cambiar cuándo** permite indicar una nueva frecuencia con tus propias palabras, como «cada día laborable a las 8». Ambas opciones incluyen **Guardar** y **Cancelar**. En una computadora, también puedes cancelar con Esc o haciendo clic fuera.

En **Editar**, **Probarlo** ejecuta una vez las nuevas instrucciones y muestra el resultado. La rutina no cambia hasta que toques **Guardar**.

**Pausar** detiene las ejecuciones hasta que toques **Reanudar** en su tarjeta. Las rutinas pausadas aparecen bajo **En pausa**, debajo de tus rutinas. Las ejecuciones que se pierdan mientras esté pausada no se ejecutarán después. **Detener** elimina la rutina de forma definitiva.

Puedes tener hasta 20 rutinas, incluidas las pausadas. Detén una para añadir otra.

Si tocas **Pedir cambios** en la tarea de una rutina o escribes en su chat, y tu nota se aplica a todas las ejecuciones, como «no uses nunca emojis», la tarea te ofrecerá **Cambiar también la rutina**. La opción aparece en la tarea y en su chat, debajo de la respuesta. Te mostrará qué cambiaría en las instrucciones de la rutina, que solo cambiarán cuando toques **Cambiarla**. **Dejarla así** las mantiene como están. Si el cambio solo sirve para ese borrador, no se ofrecerá esta opción.

## Avanzado: pasos de script

No hace falta escribir scripts: explica con tus propias palabras qué debe hacer una rutina y tu Machine se encarga del resto.

Si tienes experiencia, también puedes ejecutar tus propios comandos en tu Machine desde una rutina: abre el menú ⋯ y elige **Avanzado: pasos de script**. **Editar** muestra los pasos solo cuando la rutina ya tiene alguno. **Obtener datos** ejecuta primero un comando, en su carpeta (o en tu carpeta de inicio si no indicas ninguna), durante el número de segundos que especifiques como máximo. Lo que imprima se pasa a la ejecución para que trabaje con ello. Si no hay instrucciones, lo que imprima será el resultado.

**Comprobación** recibe el resultado como entrada después de la ejecución. Si termina con un error, el resultado muestra **No funcionó** junto con el mensaje de la comprobación. Si falla un comando de Obtener datos, se muestra lo mismo.

Cada comando debe ir en una línea y se ejecuta sin shell: no admite tuberías ni variables. Los pasos de script son tuyos y solo se configuran en tu panel. Las ejecuciones de prueba y **Probarlo** también ejecutan Obtener datos y lo indican. Aun así, no envían ni guardan nada. Una rutina nunca envía mensajes, así que los pasos de script solo deberían leer.

## Desde tus trabajos de OpenClaw

Si antes creaste trabajos programados en OpenClaw, tu Machine los lee, pero nunca los modifica, y ofrece como rutinas los que encajan en **Sugerido**. Cada uno se ejecutó una vez, así que puedes ver un resultado real.

Conserva las correcciones que hiciste al trabajo y omite lo que haya enviado o publicado. Si un trabajo ejecutaba un script o leía datos recopilados por un trabajo con script, los añade como Obtener datos. **Añadir** lo convierte en una rutina. Si tocas **No, gracias**, no volverá a preguntar por ese trabajo. Si un trabajo te recordaba que hicieras algo, aparecerá como una oferta de tarea recurrente en Tareas.

Antes de añadir una sugerencia, puedes cambiarla como cualquier rutina con **Editar** y **Cambiar cuándo** en su menú ⋯. **Ejecutar de nuevo** la ejecuta ahora con las instrucciones actuales para ver resultados más recientes, por ejemplo, después de un fin de semana tranquilo. Solo lee, se ejecuta una vez por cada toque y el nuevo resultado sustituye al anterior.

Puede haber hasta tres sugerencias a la vez. Después de una semana de buenas ejecuciones, la rutina te preguntará **¿Desactivar el antiguo trabajo de OpenClaw?**. Solo se desactiva si tocas **Desactivar**. Puedes volver a activarlo en OpenClaw. Si tocas **Mantener**, ambos trabajos siguen activos.

## A partir de lo que haces

Tu Machine también detecta las tareas que haces con regularidad y las ofrece como rutinas en **Sugerido**, aunque no uses OpenClaw. Busca:

- la misma petición tres veces seguidas o más, como «resume los tickets de soporte abiertos» todos los lunes;
- un correo que envías con regularidad, como un informe semanal para tu equipo;
- newsletters y correos de novedades que llegan todas las semanas;
- un canal de Slack muy activo donde otras personas escriben todas las semanas;
- correos que reenvías de uno en uno a la misma persona, como correos del colegio y del club a tu pareja. Un resumen semanal le evita tener que reenviarlos;
- la misma solicitud que respondes con regularidad, como una aprobación mensual para la misma persona.

Cada sugerencia indica qué detectó, como «Lo pediste 4 veces seguidas» o «Reenviaste 6 correos a Sam en 3 semanas». Además, se ejecutó una vez para que puedas ver un resultado real. Piensa en un resumen del equipo, una introducción antes de una llamada semanal, un resumen de soporte o desarrollo, un seguimiento de tus cifras o un resumen de los newsletters que recibes.

Solo sugiere rutinas que sean específicas para ti y claramente útiles: un resumen de noticias solo incluirá tus propios newsletters, nunca uno genérico. Si nada encaja, no habrá ninguna sugerencia.

Busca como máximo una vez al día y añade como máximo una sugerencia nueva por semana, sin enviarte una notificación. Si tocas **No, gracias**, no volverá a mostrar esa sugerencia. Los reenvíos y las respuestas se quedan en la cuenta desde la que se enviaron, así que Trabajo y Personal no se mezclan. Todo se queda en tu Machine. Una tarea que cierres con regularidad aparecerá como oferta de tarea recurrente.

## Rutinas y tareas recurrentes

Una [tarea recurrente](recurring.md) te recuerda que hagas algo. Una rutina es un trabajo que tu Machine hace por su cuenta y te muestra. Usa una tarea recurrente para «pagar el alquiler el día uno» y una rutina para «todos los viernes, dime qué oportunidades se han quedado paradas».
