---
title: Rutinas
area: cards
summary: Tareas que tu Machine hace por su cuenta y con cierta frecuencia, como un resumen de los negocios abiertos cada lunes. Solo lee.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: e0d519d5927cdde0
---
## Crea una rutina

Abre **Rutinas** en la barra lateral y di en una línea qué debe hacer y cuándo: «todos los lunes a las 9, resume mis negocios abiertos» o «todas las mañanas entre semana, enumera los correos que aún tengo que responder». Después, **Añadir**.

Si no indicas una hora, se ejecuta a las 8:00. La hora es la del reloj de tu Machine. En la primera ejecución se le asigna un nombre corto.

Al pulsar **Añadir**, primero se hace una prueba para que veas el resultado antes de conservarla. No se envía ni se guarda nada. Después, **Añadir** la deja activa con esa frecuencia, **Cambiar** prueba otras palabras o un nombre nuevo y **Cancelar** la descarta.

## Plantillas

En **Plantillas**, al final de Rutinas, **Añadir** activa una rutina ya preparada. Se ejecuta una vez enseguida y luego cada mañana a las 7:30 (Limpieza de spam cada hora, Hallazgos de segunda mano cada 3 horas, Suscripciones y pruebas una vez al mes). Su tarjeta muestra sus instrucciones, como en cualquier rutina, y **Editar** permite cambiarlas o cambiar el nombre.

Cuando recibes muchos newsletters y Limpieza de newsletters está desactivada (25 o más en una semana, de al menos 5 remitentes), aparece una línea sobre tus tareas que indica cuántos han llegado y qué haría la rutina, con **Activar** y **No, gracias**.

Limpieza de spam se ofrece de la misma forma cuando has movido manualmente 5 o más correos a spam en una semana. **Activar** la añade como lo hace **Añadir** aquí. Si eliges **No, gracias**, no volverá a ofrecerse. Tampoco se volverá a ofrecer una plantilla que ya hayas tenido.

**Limpieza de newsletters** crea una tarea por área (trabajo y personal) con los newsletters del último día. Cada uno incluye **Mantener** o **Darse de baja**. Para darse de baja, usa el enlace de un clic de la lista o envía un correo de baja desde tu dirección, si el envío está activado. Si no, The Machine se da de baja en la página de la lista desde su propio navegador. Si allí hace falta iniciar sesión, resolver un captcha o elegir una opción, tendrás que hacerlo tú: la fila explica por qué e incluye **Abrir página de baja**.

Se excluyen recibos, pedidos y avisos de pago. Los correos recibidos a través de una dirección de grupo, como Google Group, aparecen bajo el nombre de quien los escribió y nunca te dan de baja del grupo. Si el remitente no tiene su propio sistema para darse de baja, la fila muestra **Darse de baja a mano**.

**Limpieza de spam** crea una tarea por área con correos de remitentes desconocidos que parecen spam. Cada uno incluye **Spam** o **No es spam**. Outlook mueve el spam a Correo no deseado y Gmail lo marca como spam. La rutina comprueba cada hora, así que normalmente el spam ya está ahí antes de que lo veas. El spam nuevo se añade a la misma tarea mientras siga abierta.

Gmail conectado en modo de solo lectura, como en una Machine alojada, no puede mover correos a spam. En ese caso, **Spam** incluye un enlace para marcarlo en Gmail, y The Machine recuerda que el remitente es spam. Si no hay ninguna cuenta de correo conectada, la plantilla muestra **Conectar correo** en vez de **Añadir**.

Un remitente es desconocido si nunca le has escrito. Un «Re:» solo cuenta como conversación si has escrito en ese hilo. Si vuelve a llegar correo de un remitente que marcaste como spam, en la tarea o en tu buzón, aparecerá en la siguiente tarea con la etiqueta **Marcado como spam antes**. Lo que tú mismo hayas movido a spam también ayuda a identificar correos similares.

Nada cambia hasta que lo confirmes en la tarea. Toca un remitente para leer primero el correo: seguirá sin leerse y nada cambiará. En Limpieza de spam, no se cargan las imágenes de Internet, así que el remitente no puede saber que lo has abierto. No se te volverá a preguntar por los remitentes sobre los que ya hayas decidido. Si un día no hay newsletters ni spam, no se crea ninguna tarea. Estas tareas nunca envían una notificación.

Cuando hayas decidido sobre todos los remitentes, la tarea indicará que ha terminado e incluirá **Marcar como hecho**.

**Resumen diario** selecciona los pocos artículos de newsletters que merecen la pena y los reúne en una tarea diaria. Cada uno explica en una línea por qué te interesa. Tócalo para leer el correo o usa **Abrir en tu correo**. Solo incluye newsletters: nunca correos de personas, recibos ni remitentes de los que te hayas dado de baja, y nunca contenido que ya hayas leído. Si no encuentra nada destacable, no crea ninguna tarea.

Aprende qué te interesa a partir de lo que abres, marcas con una estrella o archivas sin leer, y de las opciones **Más como esto** y **Menos como esto** de cada selección. Los temas que elige aparecen en la tarjeta de la rutina, bajo **Más de** y **Menos de**. Elimina uno con × o añade los tuyos. Los temas con línea discontinua los ha aprendido por su cuenta. Cada resumen nuevo sustituye al que esté abierto y nunca envía una notificación.

Solo lee el remitente, el asunto y el principio de cada newsletter nuevo, y le hace a tu IA una pregunta breve sobre ellos, con un límite diario para que no resulte caro. **Cambiar cuándo** ajusta la hora. Cuando cambias las instrucciones, se ejecuta con ellas como cualquier otra rutina.

**Cumpleaños** crea una tarea por cada contacto cercano que cumpla años hoy: personas a las que escribes tú, como amistades, familiares y contactos habituales. Cada tarea incluye un saludo breve redactado en el lugar donde sueles hablar con esa persona, como su chat de WhatsApp o tu hilo de correo, y en su idioma. Solo se envía cuando lo envías tú. Si nadie cumple años ese día, no se crea ninguna tarea.

Los cumpleaños se obtienen de tus calendarios (los eventos de cumpleaños de Google y el calendario Cumpleaños, que se consultan cada mañana aunque no estén sincronizados, y el calendario Cumpleaños de Outlook), de tus contactos de Google en una Machine autoalojada y de un campo de fecha llamado Birthday en una persona de Graph. Si ninguno contiene todavía un cumpleaños, el resultado muestra **Aún no hay información sobre cumpleaños** y explica cómo añadirla.

**Importar cumpleaños de Facebook**: cuando Cumpleaños está activado, una tarea ofrece consultar la página de cumpleaños de Facebook. Toca **Importar** y The Machine la abre en su navegador, se desplaza hasta que se hayan cargado todos los meses y lee el nombre y el cumpleaños de cada amistad. Indica cuántos ha encontrado y quién coincide con personas de tu Graph por nombre y apellido. Si más de una persona tiene el mismo nombre, se omite y se muestra en la lista.

Solo **Guardar** los añade, en la página de cada persona: el cumpleaños y su foto de perfil de Facebook si aún no tiene ninguna. Si ya has añadido un cumpleaños o una foto, se conservan. Nunca se sustituye una foto que ya tenga. No se escribe nada en Facebook.

No vuelve a consultar la página por su cuenta: para hacerlo, pulsa **Importar de nuevo** en la tarea. El navegador debe tener una sesión iniciada en Facebook. Si no es así, toca **Iniciar sesión en Facebook** en la tarea e inicia sesión allí. Cuando hayas iniciado sesión, la página se consultará automáticamente. The Machine nunca inicia sesión por ti.

Se cuenta a las amistades que no están en tu Graph y se muestran algunos nombres. **Añadir … como contactos personales** las añade todas a la vez, también después de Guardar: cada una con su nombre y cumpleaños, nunca compartida con un Fleet de trabajo. Se omite a quien ya tenga alguien en tu Graph con el mismo nombre, o a quien hayas eliminado permanentemente. Los recordatorios de cumpleaños siguen apareciendo solo para las personas a las que escribes.

**Deshacer** en la tarea elimina exactamente esas personas, también después de **Importar de nuevo**.

**Suscripciones y pruebas** lee tus recibos, facturas y avisos de renovación una vez al mes y reúne tus suscripciones en una tarea: cuánto cuesta cada una, cuándo se cobra la próxima vez y si está a punto de terminar una prueba o de subir el precio. Solo muestra las que identifica con seguridad. Si no encuentra ninguna, no crea una tarea.

Elige **Mantener** o **Cancelar** para cada una. No volverá a preguntarte por las que mantengas, a menos que cambie el precio. **Cancelar** te lleva a la página para darte de baja o crea un borrador para pedir la cancelación. El mensaje solo se envía cuando lo envías tú. Entre una ejecución y otra, comprueba cada día y crea una tarea cuando falten 7 días o menos para que termine una prueba o se cobre una renovación.

**Mantenerse en contacto** te recuerda de vez en cuando que escribas a alguien cercano, solo cuando hay un motivo real. En la tarjeta, elige quiénes quieres incluir de una lista breve de personas con las que intercambias mensajes durante meses. Elimina a alguien con ×.

Solo recibirás un recordatorio si hace mucho más de lo habitual que no habláis y hay algo concreto que decir: noticias que compartió, una promesa pendiente o un mensaje que nunca respondiste. Se crea una tarea con el motivo y un mensaje breve redactado en el lugar donde sueles hablar con esa persona y en su idioma. Solo se envía cuando lo envías tú. Si no hay nada que decir, no se crea ninguna tarea.

Envía como máximo dos recordatorios por semana y uno por persona al mes. No envía ninguno a alguien con quien hayas hablado hace poco. **No hace falta** en un recordatorio hace que espere más tiempo antes de volver a recordártelo, y cada vez espera más. Nunca envía notificaciones y es Personal: nunca se comparte con un Fleet de trabajo.

**Hallazgos de segunda mano** busca anuncios en sitios de segunda mano, como Marktplaats, Vinted, eBay o Facebook Marketplace. Haz una búsqueda en el sitio con los filtros que quieras, copia la dirección de los resultados y pégala después de pulsar **Añadir**. Si quieres, añade filtros con tus propias palabras, como «menos de 300, a menos de 30 km, sin “para piezas”». Cada búsqueda es una rutina independiente, así que tendrás que volver a añadirla para la siguiente.

Cada 3 horas, abre la búsqueda en el navegador propio de The Machine y busca anuncios que aún no haya visto. Primero comprueba el precio, la distancia y las palabras que hayas excluido, con código sencillo.

Abre cada anuncio nuevo que cumpla los criterios. Tu IA evalúa su estado a partir de la foto y la descripción, y al vendedor según sus reseñas, valoración y antigüedad de la cuenta. Los anuncios que parecen buenos se reúnen en una tarea, cada uno con su foto, título, precio y una valoración breve. Toca uno para abrir el anuncio en el navegador de The Machine.

Mientras la tarea está abierta, los nuevos hallazgos se añaden al principio, aumenta el recuento y vuelve a avisarte, porque las buenas ofertas vuelan. Cuando la marques como hecha, el siguiente hallazgo creará una tarea nueva. Si una búsqueda no encuentra nada bueno, no cambia nada.

La rutina es moderada y económica: consulta la búsqueda una vez por ejecución, abre como máximo 6 anuncios por ejecución con una pausa entre ellos y comprueba como máximo 40 anuncios al día entre todas tus búsquedas. Cada comprobación es una pregunta breve a tu IA con una foto. En la primera ejecución comprueba los anuncios más recientes y marca el resto como vistos, así que las siguientes solo mostrarán lo nuevo.

Si el sitio te pide iniciar sesión, muestra una comprobación de robot o impide la lectura, una tarea te lo indicará e incluirá **Abrir** para verlo en el navegador de The Machine. Inicia sesión o completa la comprobación tú mismo; la siguiente ejecución volverá a consultar la página. The Machine nunca inicia sesión ni resuelve comprobaciones por ti. Tampoco contacta con vendedores, puja ni compra.

**Cambiar búsqueda** en la tarjeta de la rutina permite usar una dirección o unos filtros nuevos. **Cambiar cuándo** permite elegir otra frecuencia, como «cada 6 horas».

**Reordenaciones** lee las confirmaciones de pedidos de tiendas online que llegan a tu correo y detecta qué compras una y otra vez, como café, comida para mascotas o vitaminas. Cuando cree que toca repetir una compra, crea una tarea con el producto, la tienda, el último precio y la fecha de la última compra. **Ver en la tienda** te lleva a la página del producto para que lo compres tú. No compra nada por ti.

Necesita al menos tres pedidos del mismo producto a intervalos regulares, así que una compra puntual o un intervalo inusual no crea ninguna tarea. Por ahora, lee tiendas que funcionan con Shopify. Tu IA solo lee los nuevos correos de pedido de esas tiendas y hace una pregunta breve por ejecución. Estas tareas nunca envían una notificación. Si vuelves a pedir el producto, se cierra la tarea abierta.

Mientras una rutina de plantilla conserve las instrucciones originales, se ejecuta con su propio código, sin usar tu plan de IA. Limpieza de spam, por ejemplo, primero enumera con código los correos nuevos de remitentes desconocidos y solo hace una pregunta breve a tu IA si hay alguno. Mantenerse en contacto solo pregunta por una o dos personas que haya seleccionado. Si cambias las instrucciones, se ejecuta con ellas como cualquier otra rutina.

Limpieza de newsletters y Limpieza de spam siguen creando una tarea con una opción para cada correo. Si editas Cumpleaños, muestra el resultado y como máximo un borrador, no una tarea por persona. **Volver a la plantilla** en **Editar** restaura las instrucciones originales.

## Qué hace una rutina

A la hora indicada, tu Machine lee lo que necesita, como tus mensajes, reuniones y Graph, y pone el resultado en la página Rutinas. Cada resultado indica **Para revisar**, **Nada nuevo** (y por qué) o **No funcionó** (y por qué). Si una ejecución termina sin resultado, cuenta como fallida, nunca como completada.

Las rutinas solo leen: tus mensajes, páginas web, GitHub y sitios como X en el navegador. No envían mensajes, responden, publican ni cambian nada. Abren páginas que encuentran en lo que leen o en una búsqueda, direcciones de páginas normales y sitios conocidos. Nunca abren una dirección inventada para incluir lo que han leído. Solo una plantilla modifica el correo, y únicamente lo que confirmes en su tarea.

Si el trabajo de una rutina termina con una publicación o un mensaje, hace todo hasta ese paso y muestra el borrador, como **Se publicaría en X:**. Después de una ejecución real, lo recibes como tarea para aprobarlo. Una ejecución de prueba solo lo muestra.

El nombre indica de qué trata y dónde se publicará. **Desde tu rutina**, debajo, abre la rutina. El botón indica el paso, como **Preparar publicación**: la deja lista, pero no publica nada. La publicas desde el resultado. Si The Machine no puede publicarla por ti, el botón abre la página donde puedes hacerlo.

La tarea empieza en el área de la cuenta desde la que se publicará, como Trabajo para la cuenta de X de tu empresa, así que nunca te pide que la muevas.

Una ejecución puede seguir las [habilidades](skills.md) que tengas activadas, elegidas según lo que haga la rutina: solo lee completas las que encajan. El resultado las indica bajo **Usadas:**. Una habilidad nunca hace que una rutina envíe ni cambie nada.

Tus rutinas están en **Tus rutinas**, debajo de las sugerencias. Los resultados largos se contraen y muestran una vista previa breve. **Mostrar más**, o tocar el resultado, lo abre.

Cada ejecución conoce el último resultado, así que puede indicar qué ha cambiado desde entonces.

Después de una ejecución correcta, tu Machine puede escribir por su cuenta una receta para las lecturas que se repiten, como qué correos o cambios de GitHub debe consultar. En las siguientes ejecuciones, los lee primero con código sencillo y la IA solo selecciona lo importante y lo redacta, usando menos tokens. Una receta solo lee. Si deja de funcionar, la ejecución lo detecta y lo corrige por su cuenta. La receta aparece en **Avanzado: pasos de script**, en el menú ⋯.

## Días sin actividad

Si tu Machine estaba apagada u ocupada, no acumula las ejecuciones pendientes: solo ejecuta la más reciente, una vez. Cada fecha se procesa una sola vez, incluso después de reiniciar.

Las rutinas se ejecutan de una en una y esperan si queda poco uso en tu plan de IA, como todo el trabajo en segundo plano. **Ejecutar ahora** la inicia enseguida. El resultado aparece en la tarjeta cuando esté listo.

## Cambiarla o detenerla

Estas opciones están en el menú ⋯ de la rutina. **Editar** cambia el nombre y lo que hace, pero mantiene cuándo se ejecuta y los resultados anteriores. **Cambiar cuándo** permite elegir otra frecuencia con tus propias palabras, como «todos los días entre semana a las 8». Ambas opciones incluyen **Guardar** y **Cancelar**. En un ordenador, también puedes cancelar con Esc o haciendo clic fuera.

En **Editar**, **Pruébalo** ejecuta una vez las nuevas instrucciones y muestra el resultado allí. La rutina no cambia hasta que pulses **Guardar**.

**Pausar** detiene las ejecuciones hasta que pulses **Reanudar** en la tarjeta. Las rutinas pausadas esperan en **En pausa**, debajo de tus rutinas, y las ejecuciones pendientes durante la pausa no se llevan a cabo después. **Detener** termina la rutina definitivamente.

Puedes tener hasta 20 rutinas, incluidas las pausadas. Detén una para añadir otra.

Si usas **Pedir cambios** en una tarea de la rutina o escribes en su chat, y la nota debe aplicarse a todas las ejecuciones, como «no uses nunca emojis», la tarea te ofrecerá **Cambiar también la rutina**, tanto en la tarea como en su chat, debajo de la respuesta. Te muestra qué cambiaría en las instrucciones de la rutina, que solo cambiarán si tocas **Cambiarla**. **Dejarla así** no hace ningún cambio. Si solo pides corregir ese borrador, no se ofrece esta opción.

## Avanzado: pasos de script

No hace falta ningún script: explica con tus propias palabras qué debe hacer una rutina y tu Machine se encarga del resto.

Si tienes experiencia, también puedes hacer que una rutina ejecute tus propios comandos en tu Machine. En el menú ⋯, elige **Avanzado: pasos de script**. **Editar** solo los muestra cuando la rutina ya tiene alguno. **Consultar datos** ejecuta primero un comando, en su carpeta (o en tu carpeta personal si no indicas ninguna), durante el máximo de segundos establecido. Lo que imprima se envía a la ejecución para que trabaje con ello. Si no hay instrucciones, lo que imprima será el resultado.

**Comprobación** recibe el resultado como entrada después de la ejecución. Si termina con un error, la ejecución muestra **No funcionó** y el mensaje de la comprobación. Si falla un comando de Consultar datos, se muestra de la misma manera.

Cada comando debe ocupar una línea y se ejecuta sin un shell: no se permiten tuberías ni variables. Tú configuras los pasos de script y solo están en tu panel. Las ejecuciones de prueba y **Pruébalo** también ejecutan Consultar datos y lo indican. Aun así, no envían ni guardan nada. Una rutina nunca envía nada, así que un paso de script solo debería leer.

## Desde tus trabajos de OpenClaw

Si antes creaste trabajos programados en OpenClaw, tu Machine los lee (nunca los cambia) y ofrece los que encajan como rutinas en **Sugerido**. Cada uno ya se ha ejecutado una vez, así que puedes ver un resultado real.

Conserva las correcciones que hayas hecho al trabajo y omite lo que haya enviado o publicado. Si un trabajo ejecutaba un script o leía datos recopilados por un trabajo con script, lo añade como Consultar datos. **Añadir** lo convierte en una rutina. **No, gracias** hace que no vuelva a preguntarte por ese trabajo. Si el trabajo te recordaba que tenías que hacer algo, en su lugar aparece en Tareas como una oferta de tarea periódica.

Antes de añadir una sugerencia, puedes cambiarla como cualquier rutina con **Editar** y **Cambiar cuándo**, en su menú ⋯. **Ejecutar de nuevo** la ejecuta ahora con las instrucciones actuales para ver resultados más recientes, por ejemplo, después de un fin de semana tranquilo. Solo lee, se ejecuta una vez por toque y su nuevo resultado sustituye al anterior.

Puede haber un máximo de tres sugerencias en espera a la vez. Después de una semana de ejecuciones correctas, la rutina pregunta **¿Desactivar el antiguo trabajo de OpenClaw?**. Solo se desactiva si tocas **Desactivar**, y puedes volver a activarlo en OpenClaw. **Mantener** deja ambos en funcionamiento.

## A partir de lo que haces

Tu Machine también detecta tareas que haces con cierta frecuencia y las ofrece como rutinas en **Sugerido**, aunque no uses OpenClaw. Busca:

- la misma petición tres veces seguidas o más, como «resume los tickets de soporte abiertos» todos los lunes;
- un correo que envías con cierta frecuencia, como un informe semanal para tu equipo;
- newsletters y correos de novedades que llegan todas las semanas;
- un canal de Slack con mucha actividad en el que otras personas escriben cada semana;
- correos que reenvías uno a uno a la misma persona, como correos del colegio o de actividades extraescolares a tu pareja: un resumen semanal para esa persona evita tener que reenviarlos;
- la misma solicitud que respondes con cierta frecuencia, como una aprobación mensual para la misma persona.

Cada sugerencia explica qué ha detectado, como «Lo has pedido 4 veces seguidas» o «Has reenviado 6 correos a Sam en 3 semanas». También se ha ejecutado una vez, para que veas un resultado real. Puede servirte para preparar un resumen del equipo, un informe antes de una reunión semanal, un resumen de soporte o desarrollo, un seguimiento de tus cifras o un resumen de los newsletters que recibes.

Solo sugiere cosas específicas para ti y claramente útiles: un resumen de noticias solo incluiría tus propios newsletters, nunca uno genérico. Si nada encaja, no aparece ninguna sugerencia.

Busca como máximo una vez al día y añade como máximo una sugerencia nueva por semana, sin enviar notificaciones. **No, gracias** hace que esa sugerencia no vuelva a aparecer. Los reenvíos y las respuestas se quedan en la cuenta desde la que se enviaron, así que Trabajo y Personal no se mezclan. Todo permanece en tu Machine. Si cierras una tarea con cierta frecuencia, en su lugar aparece una oferta de tarea periódica.

## Rutinas y tareas periódicas

Una [tarea periódica](recurring.md) te recuerda que hagas algo. Una rutina es un trabajo que tu Machine hace por su cuenta y te muestra. Usa una tarea periódica para «pagar el alquiler el día 1» y una rutina para «todos los viernes, dime qué negocios se han quedado parados».
