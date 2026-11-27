---
title: Rutinas
area: cards
summary: Tareas que tu Machine hace sola, con cierta frecuencia, como un resumen de tus oportunidades abiertas cada lunes. Solo lee.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 57b97c44b031845f
---
## Crea una rutina

Abre **Rutinas** en la barra lateral y explica en una línea qué debe hacer y cuándo: «todos los lunes a las 9, resume mis oportunidades abiertas» o «todas las mañanas entre semana, enumera los correos a los que aún tengo que responder». Después, pulsa **Añadir**.

Si no indicas una hora, se ejecuta a las 8:00. La hora se basa en el reloj de tu Machine. La primera ejecución le asigna un nombre corto.

Al pulsar **Añadir** primero se hace una prueba para que veas el resultado antes de conservarla. No se envía ni se guarda nada. Después, **Añadir** la mantiene con la frecuencia indicada, **Cambiar** prueba otras palabras o un nombre nuevo y **Cancelar** la descarta.

## Plantillas

En **Plantillas**, al final de Rutinas, **Añadir** activa una rutina lista para usar. Se ejecuta una vez al momento y, después, cada mañana a las 7:30 (Limpieza de spam, cada hora; Hallazgos de segunda mano, cada 3 horas; Suscripciones y pruebas, una vez al mes). Su tarjeta muestra el texto de la rutina, como cualquier otra, y **Editar** permite cambiarlo o cambiar el nombre.

Cuando recibes muchos newsletters y Limpieza de newsletters está desactivada (25 o más en una semana, de al menos 5 remitentes), aparece una línea encima de tus tareas que indica cuántos han llegado y qué haría la rutina, con las opciones **Activar** y **No, gracias**.

Limpieza de spam se ofrece del mismo modo cuando has movido a mano al menos 5 correos a spam en una semana. **Activar** la añade igual que **Añadir** aquí. Si eliges **No, gracias**, no volverá a ofrecerse, ni tampoco una plantilla que ya hayas tenido.

**Limpieza de newsletters** crea una tarea por área (trabajo y personal) con los newsletters del último día. Cada uno incluye las opciones **Mantener** o **Darse de baja**. Para darte de baja, usa el enlace de baja con un solo clic de la lista o envía un correo de baja desde tu dirección, si está activado el envío. Si no, The Machine se da de baja en la página de la lista desde su propio navegador. Si la página requiere iniciar sesión, completar un captcha o elegir opciones, tendrás que hacerlo tú: la fila lo explica y ofrece **Abrir página de baja**.

Si solo quieres evitar que una lista genere tareas y seguir recibiendo sus correos, escribe «Ningún mensaje de esta lista necesita una tarea» en el chat de uno de ellos.

Se excluyen los recibos, los pedidos y los avisos de pago. Los correos que llegan a través de una dirección de grupo, como un grupo de Google Groups, aparecen bajo el nombre de quien los escribió y nunca te dan de baja del grupo. Si el remitente no tiene una opción propia para darse de baja, la fila muestra **Darse de baja a mano**.

**Limpieza de spam** crea una tarea por área con los correos de remitentes desconocidos que parecen spam. Cada uno incluye las opciones **Spam** o **No es spam**. Outlook mueve el spam a Correo no deseado y Gmail lo marca como spam. La rutina comprueba cada hora, así que normalmente el spam ya estará ahí cuando lo revises. El spam nuevo se añade a la misma tarea mientras siga abierta.

Si Gmail está conectado en modo de solo lectura, como en una Machine alojada, no se pueden mover correos a spam. En ese caso, **Spam** incluye un enlace para marcarlo en Gmail y The Machine recuerda que ese remitente es spam. Si no hay ninguna cuenta de correo conectada, la plantilla muestra **Conectar correo** en lugar de **Añadir**.

Un remitente es desconocido si nunca le has escrito. Un «Re:» solo cuenta como conversación en un hilo en el que hayas escrito. Si vuelve a llegarte un correo de un remitente que hayas marcado como spam, en la tarea o en tu buzón, aparecerá en la siguiente tarea con la etiqueta **Marcado como spam antes**. Los correos que tú hayas movido a spam también ayudan a reconocer mensajes parecidos.

Nada cambia hasta que lo confirmas en la tarea. Pulsa un remitente para leer primero el correo: seguirá sin leerse y no cambiará nada. Desde Limpieza de spam no se cargan las imágenes de la web, así que el remitente no puede saber que has abierto el correo. No se te volverá a preguntar por los remitentes sobre los que ya hayas decidido. Si un día no hay newsletters ni spam, no se crea ninguna tarea. Estas tareas nunca envían notificaciones.

Cuando hayas decidido sobre todos los remitentes, la tarea indicará que ha terminado y mostrará **Marcar como hecha**.

**Resumen diario** elige los pocos artículos de newsletters que merecen la pena y los reúne en una tarea al día. Cada uno explica en una línea por qué puede interesarte. Púlsalo para leer el correo o usa **Abrir en tu correo**. Solo incluye newsletters, nunca correos de personas, recibos ni remitentes de los que te hayas dado de baja; tampoco incluye lo que ya hayas leído. Si no destaca nada, no se crea ninguna tarea.

La rutina aprende qué te interesa según lo que abres, destacas o archivas sin leer, y según lo que indicas con **Más como esto** y **Menos como esto** en cada selección. Los temas que tiene en cuenta aparecen en la tarjeta de la rutina, bajo **Más de** y **Menos de**. Elimina un tema con × o añade los tuyos. Los temas con línea discontinua los ha aprendido la rutina. Un resumen nuevo sustituye al que esté abierto y nunca envía notificaciones.

Solo lee el remitente, el asunto y el principio de cada newsletter nuevo, y hace una pregunta breve al modelo de IA que uses, con un límite diario, para que no resulte caro. **Cambiar cuándo** permite cambiar la hora. Si cambias el texto de la rutina, se ejecutará como cualquier otra, siguiendo tus indicaciones.

**Cumpleaños** crea una tarea por cada persona cercana que cumpla años hoy: personas a las que escribes tú, como amistades, familiares y contactos habituales. Para cada una prepara un saludo breve en el lugar donde sueles hablar con ella, como su chat de WhatsApp o el hilo de correo, en su idioma. Solo se envía cuando lo haces tú. Si no hay cumpleaños ese día, no se crea ninguna tarea.

Los cumpleaños se obtienen de tus calendarios (los eventos de cumpleaños de Google y el calendario Cumpleaños, que se leen cada mañana aunque no estén sincronizados, y el calendario Cumpleaños de Outlook), de tus contactos de Google en una Machine autohospedada y de un campo de fecha llamado Birthday en una persona de Graph. Si todavía no hay ningún cumpleaños en esas fuentes, el resultado indica **Aún no hay información sobre cumpleaños** y explica cómo añadirla.

**Importar cumpleaños de Facebook**: cuando Cumpleaños esté activada, una tarea te ofrecerá leer la página de cumpleaños de Facebook. Pulsa **Importar** y The Machine abrirá la página en su navegador, se desplazará hasta que se hayan cargado todos los meses y leerá el nombre y el cumpleaños de cada amistad. Te mostrará cuántos ha encontrado y quién coincide con personas de tu Graph por nombre y apellido. Si hay más de una persona con el mismo nombre, se omitirá y aparecerá en una lista.

Solo **Guardar** los añade, en la página de cada persona: el cumpleaños y la foto de perfil de Facebook, si todavía no tiene foto. Se conservarán los cumpleaños y las fotos que hayas añadido ahí, y nunca se sustituirá una foto que ya tenga. No se escribe nada en Facebook.

No se vuelve a leer automáticamente: puedes hacerlo con **Importar de nuevo** en la tarea. El navegador debe tener una sesión iniciada en Facebook. Si no la tiene, pulsa **Iniciar sesión en Facebook** en la tarea e inicia sesión allí. Cuando lo hayas hecho, la página se leerá automáticamente. The Machine nunca inicia sesión por ti.

Se cuenta a las amistades que no estén en tu Graph y se muestran algunos nombres. **Añadir … como contactos personales** las añade todas de una vez, también después de guardar: cada persona se añade con su nombre y cumpleaños, nunca a un Fleet de trabajo. Se omite cualquier persona cuyo nombre ya aparezca en tu Graph o que hayas eliminado de forma permanente. Los recordatorios de cumpleaños siguen limitándose a las personas a las que escribes.

**Deshacer** en la tarea vuelve a eliminar exactamente a esas personas, también después de **Importar de nuevo**.

**Suscripciones y pruebas** lee tus recibos, facturas y avisos de renovación una vez al mes, y reúne tus suscripciones en una tarea: cuánto cuesta cada una, cuándo se cobrará y si termina una prueba o sube el precio. Solo se incluyen las que la rutina puede identificar con seguridad. Si no encuentra ninguna, no se crea ninguna tarea.

Elige **Mantener** o **Cancelar** para cada una. No se volverá a preguntar por las que mantengas, salvo que cambie el precio. **Cancelar** te lleva a la página de cancelación o prepara un borrador para pedir la cancelación, que solo se envía cuando lo haces tú. Entre una ejecución y otra, comprueba cada día las suscripciones y crea una tarea si el cobro de una prueba o renovación se producirá en los próximos 7 días.

**Mantenerse en contacto** te recuerda de vez en cuando que escribas a alguien cercano, solo cuando hay un motivo real. En la tarjeta, elige quién forma parte de la rutina de una lista breve de personas con las que intercambias mensajes durante varios meses. Elimina a alguien con ×.

Solo recibirás un recordatorio cuando lleves mucho más tiempo del habitual sin hablar con esa persona y haya algo concreto que decir: novedades que haya compartido, también las del resumen de su página, una promesa pendiente o un mensaje al que nunca respondiste.

Si una novedad tiene una fecha futura, como una mudanza el mes que viene, se vuelve a comprobar justo después de ese día, teniendo en cuenta sus mensajes más recientes. Se crea una tarea con el motivo y un mensaje breve preparado en el lugar donde sueles hablar con esa persona, en su idioma. Solo se envía cuando lo haces tú. Si no hay nada que decir, no se crea ninguna tarea.

Se envían como máximo dos recordatorios a la semana y uno por persona al mes. No se envían a alguien con quien hayas hablado hace poco. **No hace falta** en un recordatorio hace que pase más tiempo antes del siguiente para esa persona, y ese tiempo aumenta cada vez. Nunca se envían notificaciones. La rutina es Personal: nunca se comparte con un Fleet de trabajo ni se basa en lo que llega a tus cuentas de trabajo.

**Hallazgos de segunda mano** supervisa una búsqueda en un sitio de segunda mano, como Marktplaats, Vinted, eBay o Facebook Marketplace. Configura la búsqueda con los filtros que quieras, copia la dirección de los resultados y pégala después de pulsar **Añadir**. Si quieres, añade filtros con tus propias palabras, como «menos de 300, a menos de 30 km, sin anuncios de “para piezas”». Cada búsqueda tiene su propia rutina, así que tendrás que volver a añadirla para la siguiente.

Cada 3 horas, The Machine abre la búsqueda en su propio navegador y busca anuncios que aún no haya visto. Primero comprueba el precio, la distancia y las palabras que hayas excluido, con código sencillo.

Abre cada anuncio nuevo que cumpla los filtros. El modelo de IA que uses evalúa el estado del artículo a partir de la foto y la descripción, y al vendedor según sus reseñas, valoración y antigüedad de la cuenta. Los buenos anuncios se reúnen en una tarea, cada uno con su foto, título, precio y una valoración de una línea. Pulsa uno para abrir el anuncio en el navegador de The Machine.

Mientras la tarea esté abierta, los nuevos hallazgos se añaden al principio, aumenta el recuento y se te vuelve a avisar, porque las buenas ofertas vuelan. Cuando marques la tarea como hecha, el siguiente hallazgo iniciará una nueva. Si una búsqueda no encuentra nada bueno, no cambia nada.

La rutina actúa con cuidado y procura no resultar cara: lee la búsqueda una vez por ejecución, abre como máximo 6 anuncios por ejecución, dejando una pausa entre uno y otro, y comprueba como máximo 40 anuncios al día entre todas tus búsquedas. Cada comprobación consiste en una pregunta breve al modelo de IA que uses, con una foto. En la primera ejecución comprueba los anuncios más recientes y considera vistos los demás, así que las siguientes solo incluirán los nuevos.

Si el sitio te pide iniciar sesión, muestra una comprobación para detectar robots o impide la lectura, una tarea te lo indicará y ofrecerá **Abrir** para verlo en el navegador de The Machine. Inicia sesión o completa la comprobación tú. La siguiente ejecución volverá a leer la página. The Machine nunca inicia sesión ni resuelve comprobaciones por ti, y tampoco contacta con vendedores, puja ni compra.

**Cambiar búsqueda** en la tarjeta de la rutina permite usar una dirección o unos filtros nuevos. **Cambiar cuándo** permite cambiar la frecuencia, por ejemplo, a «cada 6 horas».

**Reordenaciones** lee las confirmaciones de pedidos de tiendas online que recibes por correo y detecta lo que compras una y otra vez, como café, comida para mascotas o vitaminas. Cuando cree que toca volver a comprar algo, crea una tarea con el producto, la tienda, el último precio y la fecha de la última compra. **Ver en la tienda** abre la página del producto para que lo compres tú. No compra nada por ti.

Necesita encontrar al menos tres pedidos del mismo producto con una frecuencia regular. Por eso, una compra puntual o un intervalo inusual no generan una tarea. De momento, solo lee tiendas que usan Shopify. El modelo de IA que uses solo lee los correos nuevos de pedidos de esas tiendas, en una pregunta breve por ejecución. Estas tareas nunca envían notificaciones. Si vuelves a pedir el producto, se cierra la tarea abierta.

Mientras la rutina de una plantilla conserve el texto original de la plantilla, se ejecuta con su propio código, sin usar tu plan de IA (Limpieza de spam primero enumera en código los correos nuevos de remitentes desconocidos y solo hace una pregunta breve al modelo de IA que uses si hay alguno; Mantenerse en contacto solo pregunta por una o dos personas). Si cambias el nombre, se mantiene ese funcionamiento. Si cambias el texto de la rutina, se ejecutará como cualquier otra, siguiendo tus indicaciones.

Limpieza de newsletters y Limpieza de spam siguen generando la misma tarea, con una opción para cada correo. Si editas Cumpleaños, se muestra su resultado y como máximo un borrador, no una tarea por persona. **Volver a la plantilla**, dentro de **Editar**, restaura el texto original.

## Cómo funciona una rutina

A la hora indicada, tu Machine lee lo que necesita, como tus mensajes, reuniones y Graph, y muestra el resultado en la página Rutinas. Cada resultado indica **Para revisar**, **Nada nuevo** (y el motivo) o **No funcionó** (y el motivo). Si una ejecución termina sin resultado, cuenta como fallida, nunca como completada.

Las rutinas solo leen: tus mensajes, páginas web, GitHub y sitios como X en el navegador. No envían mensajes, responden, publican ni cambian nada. Abren páginas que encuentran en lo que leen o en una búsqueda, con direcciones de páginas sencillas y sitios conocidos. Nunca abren una dirección inventada para incluir lo que han leído. Solo una plantilla puede cambiar el correo, y únicamente lo que confirmes en su tarea.

Si una rutina acaba con una publicación o un mensaje, hace todo lo anterior y muestra un borrador, como **Publicaría en X:**. Después de una ejecución real, aparece como tarea para que lo apruebes. En una ejecución de prueba solo se muestra.

El nombre indica de qué trata y dónde se publica. **Desde tu rutina**, debajo del nombre, abre la rutina. El botón indica el paso, por ejemplo, **Preparar publicación**: prepara la publicación, pero no publica nada. Puedes publicarla desde el resultado. Si The Machine no puede publicarla por ti, el botón abre la página donde puedes hacerlo.

La tarea aparece primero en el área de la cuenta desde la que se publicará, como Trabajo para la cuenta de X de tu empresa, así que nunca te pedirá que la cambies de área.

Una rutina puede seguir tus [habilidades](skills.md) activadas, según lo que haga: solo se leen por completo las que encajen. El resultado las enumera debajo de **Usadas:**. Una habilidad nunca hace que una rutina envíe ni cambie nada.

Tus rutinas aparecen en **Tus rutinas**, debajo de las sugerencias. Los resultados largos se contraen y muestran una vista previa breve. **Mostrar más**, o pulsar el resultado, lo abre.

Cada ejecución tiene en cuenta el resultado anterior para indicar qué ha cambiado desde entonces.

Después de una buena ejecución, tu Machine puede escribirse una receta para las lecturas que se repiten, como qué correos o cambios de GitHub debe revisar. En las siguientes ejecuciones, lee primero esos datos con código sencillo. Después, la IA elige lo importante y lo redacta, con menos tokens. La receta solo lee. Si deja de funcionar, la rutina vuelve a leer por sí sola y la arregla. La receta aparece en **Avanzado: pasos de script**, en el menú ⋯.

## Días sin conexión

Si tu Machine estaba apagada u ocupada, las ejecuciones pendientes no se acumulan: solo se ejecuta la más reciente, una vez. Cada fecha se ejecuta una sola vez, incluso después de reiniciar.

Las rutinas se ejecutan de una en una y esperan si el uso de tu plan de IA es bajo, como cualquier otra tarea en segundo plano. **Ejecutar ahora** la ejecuta de inmediato. El resultado aparece en la tarjeta cuando esté listo.

## Cambiar una rutina o detenerla

Estas opciones están en el menú ⋯ de la rutina. **Editar** permite cambiar el nombre y lo que hace; conserva la hora de ejecución y los resultados anteriores. **Cambiar cuándo** permite indicar una nueva frecuencia con tus propias palabras, como «todos los días entre semana a las 8». Ambas opciones incluyen **Guardar** y **Cancelar**. En un ordenador, también puedes cancelar con Esc o haciendo clic fuera.

En **Editar**, **Pruébalo** ejecuta una vez el texto nuevo y muestra el resultado ahí. La rutina no cambia hasta que pulses **Guardar**.

**Pausar** detiene las ejecuciones hasta que pulses **Reanudar** en su tarjeta. Las rutinas en pausa aparecen debajo de tus rutinas, en **En pausa**. Las ejecuciones que no se hayan hecho durante la pausa no se recuperan después. **Detener** pone fin a una rutina de forma permanente.

Puedes tener hasta 20 rutinas, incluidas las pausadas. Detén una para añadir otra.

Si usas **Pedir cambios** en una tarea de una rutina o escribes en su chat una nota para todas las ejecuciones, como «no uses nunca emojis», la tarea ofrece **Cambiar también la rutina**. La opción aparece en la tarea y en su chat, debajo de la respuesta. Te muestra qué cambiaría en el texto de la rutina, que solo se modifica cuando pulsas **Cambiarla**. **Dejarla así** conserva la rutina tal como está. Si solo pides corregir ese borrador, no se ofrece esta opción.

## Avanzado: pasos de script

No necesitas scripts: explica con tus propias palabras qué debe hacer una rutina y tu Machine se encargará del resto.

Si tienes experiencia, también puedes ejecutar tus propios comandos en tu Machine. En el menú ⋯, elige **Avanzado: pasos de script**. **Editar** solo muestra los pasos cuando la rutina ya tiene alguno. **Consultar datos** ejecuta primero un comando, dentro de su carpeta (o de tu carpeta personal si no indicas ninguna), durante un máximo de los segundos especificados. Lo que imprima se incluye en la ejecución para que pueda procesarlo. Si no hay texto, lo que imprima será el resultado.

**Comprobación** recibe el resultado como entrada después de la ejecución. Si termina con un error, la ejecución muestra **No funcionó** junto con lo que haya indicado la comprobación. Si falla un comando de Consultar datos, se muestra lo mismo.

Cada comando debe ocupar una sola línea y se ejecuta sin un shell: no se admiten tuberías ni variables. Los pasos de script son tuyos y solo se configuran en tu panel. Las ejecuciones de prueba y las de **Pruébalo** también ejecutan Consultar datos y lo indican, pero no envían ni guardan nada. Las rutinas nunca envían nada, así que un paso de script solo debería leer.

## Desde tus trabajos de OpenClaw

Si antes creaste trabajos programados en OpenClaw, tu Machine los lee (nunca los modifica) y ofrece como rutinas, en **Sugerido**, los que encajan. Cada uno se ejecutó una vez para que veas un resultado real.

Conserva las correcciones que hayas hecho al trabajo y omite lo que haya enviado o publicado. Si un trabajo ejecutaba un script o leía lo que había recopilado un trabajo de script, lo incluye como Consultar datos. **Añadir** lo convierte en una rutina. **No, gracias** hace que no vuelva a preguntarte por ese trabajo. Si el trabajo te recordaba hacer algo, aparecerá como una oferta de tarea periódica en Tareas.

Antes de añadir una sugerencia, puedes cambiarla como cualquier rutina con **Editar** y **Cambiar cuándo**, en su menú ⋯. **Ejecutar de nuevo** la ejecuta ahora con el texto actual para ver resultados más recientes, por ejemplo, después de un fin de semana tranquilo. Solo lee, se ejecuta una vez por toque y sustituye el resultado anterior por el nuevo.

Puede haber como máximo tres sugerencias pendientes a la vez. Después de una semana de buenas ejecuciones, la rutina te pregunta **¿Desactivar el antiguo trabajo de OpenClaw?**. Solo se desactiva si pulsas **Desactivar**. Puedes volver a activarlo en OpenClaw. **Mantener** deja los dos en marcha.

## A partir de lo que haces

Tu Machine también detecta las tareas que haces con cierta frecuencia y las ofrece como rutinas en **Sugerido**, aunque no uses OpenClaw. Busca lo siguiente:

- la misma petición tres veces seguidas o más, como «resume los tickets de soporte abiertos» todos los lunes;
- un correo que envías con cierta frecuencia, como un informe semanal para tu equipo;
- newsletters y correos de novedades que llegan todas las semanas;
- un canal de Slack con mucha actividad en el que otras personas escriben todas las semanas;
- correos que reenvías uno a uno a la misma persona, como los del colegio y las actividades extraescolares que envías a tu pareja: un resumen semanal le ahorraría tener que reenviarlos;
- la misma petición a la que respondes con cierta frecuencia, como una aprobación mensual para la misma persona.

Cada sugerencia explica qué ha detectado, por ejemplo, «Lo has pedido 4 veces seguidas» o «Has reenviado 6 correos a Sam en 3 semanas». También se ha ejecutado una vez para que veas un resultado real. Puede servirte para preparar un resumen del equipo, un informe breve antes de una llamada semanal, un resumen de soporte o desarrollo, un seguimiento de tus cifras o un resumen de los newsletters que recibes.

Solo sugiere rutinas que sean específicas para ti y claramente útiles: un resumen de noticias solo incluiría tus propios newsletters, nunca uno genérico. Si nada encaja, no habrá sugerencias.

Busca sugerencias como máximo una vez al día y añade como máximo una nueva a la semana, sin enviarte notificaciones. **No, gracias** hace que no vuelva a aparecer esa sugerencia. Los reenvíos y las respuestas se quedan en la cuenta desde la que se enviaron, así que Trabajo y Personal no se mezclan. Todo permanece en tu Machine. Si cierras una tarea periódica, se ofrece como una tarea periódica en su lugar.

## Rutinas y tareas periódicas

Una [tarea periódica](recurring.md) te recuerda que hagas algo. Una rutina es trabajo que tu Machine hace por sí sola y te muestra. Usa una tarea periódica para «pagar el alquiler el día 1» y una rutina para «cada viernes, dime qué oportunidades llevan tiempo sin avanzar».
