---
title: Conexiones
area: connections
summary: Tus fuentes en un solo lugar: cómo va cada una, cómo añadir otra o desconectarla.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 9f2a2162fe015e0b
---
## Cómo van

La pestaña **Conexiones** muestra tus fuentes por tipo, con **Inicios de sesión** y **Revisiones** debajo de una línea. En el móvil, toca un tipo para abrirlo y **Conexiones** para volver. Primero se abre el tipo que tenga una fuente que requiera tu atención. Cada fuente aparece en una fila: muestra cómo va (Conectada, Esperando la primera sincronización, Reconectando automáticamente o Necesita tu ayuda) y qué ha recibido últimamente. Tócala para ver su tarjeta y **Detalles**.

Si una sincronización fallida se recuperó en la siguiente, aparece en gris. Solo se muestra como problema el último intento fallido, junto con la fecha del próximo intento.

Los recuentos muestran todo lo que ha recibido, incluido su [historial](history.md), lo que ha recibido en las últimas 24 horas y lo que aún no se ha revisado. En el caso de los calendarios, cuentan los eventos.

Cada fuente lleva el nombre de su cuenta, tal como la identifica el servicio: tu dirección, un perfil de X, un espacio de trabajo de Slack o la persona a la que pertenece la cuenta de Signal o Telegram. Debajo del nombre aparece primero **Trabajo** o **Personal**, además de la dirección o el nombre de usuario si no aparecen ya en el nombre. Si hay dos fuentes del mismo tipo con el mismo nombre, también se indica cómo distinguirlas, por ejemplo, Slack o X, o la dirección del espacio de trabajo.

Cada fuente también indica en una línea qué recibe y, si puede realizar acciones, que solo las realiza después de que pulses **Enviar** o las apruebes.

## Añadir una fuente

Abre un tipo (**Correo**, **Calendario**, **Chat**, **Reuniones**, **Documentos y archivos**, **Clientes**, **Proyectos y código**, **Otras**) y elige una fuente en **Añadir otro** o debajo de la lista si todavía no hay ninguna conectada. Al final aparecen las opciones para otros servicios: **Otro correo** en Correo, y **Enlace de calendario (ICS)** y **Otro calendario** en Calendario. Exchange Server permite consultar reuniones, así que está en Calendario.

**Sugerido para ti** aparece en la parte superior de **Conexiones** cuando tu Machine detecta un motivo para añadir una fuente. El motivo se indica en una línea: correos de Stripe, reuniones de Zoom en tu calendario, mensajes con enlaces a Google Docs o una configuración que no se completó. La fuente también sigue apareciendo en su propio grupo, marcada como **Sugerido**. El recuento se calcula en tu Machine; no se envía nada fuera de ella. Las fuentes conectadas nunca aparecen como sugeridas.

Microsoft Teams aparece dos veces: en **Chat**, para los chats, y en **Reuniones**, como **Reuniones de Teams**, para las notas de las reuniones. Ambas usan el mismo inicio de sesión de Microsoft, así que al conectar una también se conecta la otra.

Si ya conectaste una fuente, aparecerá en la lista junto con su cuenta. Selecciónala para añadir otra: el formulario lo indica y enlaza con la que ya tienes.

Rellena los datos que te pida, como una clave o una dirección, elige **Trabajo** con el nombre de la empresa o **Personal** (en el caso del correo y los calendarios, solo te pregunta si la dirección no lo deja claro) y pulsa **Conectar**. Si se trata de un sitio como LinkedIn o X, se abrirá la página de inicio de sesión en el navegador de tu Machine y el proceso continuará automáticamente cuando inicies sesión. GitHub, WhatsApp y Codex muestran un código que debes introducir. Los chats de Telegram y Signal muestran un código QR que puedes escanear.

**Cancelar** detiene el proceso. ¿Saliste antes de terminar? Vuelve a abrir **Conexiones** desde cualquier dispositivo y continuarás donde lo dejaste. Una vez conectada, tu Machine empieza a leer la fuente de inmediato y muestra cómo va la primera sincronización.

En una Machine alojada, puedes iniciar sesión directamente aquí en las fuentes que tienen su propio inicio de sesión: Google, Microsoft (Outlook, OneDrive y Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce y Trello.

Elige **Trabajo** o **Personal** y pulsa el botón de inicio de sesión correspondiente, como **Iniciar sesión con Google**. Volverás a este formulario, donde se mostrará el resultado. Aquí también se muestran los códigos de GitHub, WhatsApp, Codex, los chats de Telegram y tu teléfono Android.

En tu propio ordenador, puedes iniciar sesión en esas mismas fuentes cuando vincules tu Machine a tu cuenta. Pulsa **Vincular esta Machine** la primera vez. Algunas también ofrecen otra opción, como usar tu propia aplicación o una clave.

**Reconectar**, tanto en una fuente como en **Te necesita**, abre el mismo formulario. En tu propio ordenador, `assistant connect` hace lo mismo desde un terminal.

## Trabajo o personal

Cada fuente se clasifica como de trabajo, para una empresa que indiques, o personal. Puedes cambiarlo en **Detalles**. **Adivinado** significa que tu Machine lo dedujo a partir de la dirección. Las tareas de trabajo esperan a tus días laborables.

El correo y los calendarios de Google y Microsoft usan la dirección para determinarlo cuando está claro: un proveedor de correo como Gmail o Outlook.com se considera Personal, y el dominio de tu empresa, Trabajo. Si no está claro, te pregunta una vez, justo después de iniciar sesión. **Cambiar** te permite elegirlo. Si más adelante el correo indica lo contrario, la tarea **Saca más partido a The Machine** te preguntará una vez si quieres cambiarlo.

## Permisos

Una fuente puede traer señales (lo que recibe se convierte en tareas), realizar acciones para tus tareas (leer un documento o enviar, responder o cambiar algo cuando lo apruebes), o ambas cosas. Si puede hacer ambas, **Detalles** incluye un interruptor para cada opción: **Trae señales** y **Puede hacer cosas**. Una de las dos siempre debe estar activada. Para desactivar ambas, desconecta la fuente. Los chats solo tienen **Puede hacer cosas**.

Si desactivas **Trae señales**, la fuente no se sincroniza. Si desactivas **Puede hacer cosas**, tu Machine nunca leerá, redactará ni cambiará nada con esa fuente.

## Eliminar una fuente

Abre la fuente, ve a **Detalles** y pulsa **Desconectar**. Dejará de leerla. Lo que ya haya recibido se conserva. En una Machine alojada, las fuentes cuyo inicio de sesión gestiona la página de configuración (Google, Microsoft, Google Meet, Slack, Zoom, Stripe y Salesforce) muestran **Desconectar ↗**, que abre esa página.

**Desconectado hace poco** muestra las cuentas de Google, Microsoft, Zoom, Slack, Stripe y Salesforce que desconectaste en los últimos 30 días, y cuándo las desconectaste. Hasta que el servicio lo confirme, aparece el estado Pendiente y se sigue intentando. Las cuentas de Google aparecen una sola vez, aunque Google Meet o Docs tuvieran su propio inicio de sesión. Cada cuenta aparece en su tipo: las cuentas de Google y Microsoft en **Correo**, y las de Slack en **Chat**.

## Inicios de sesión guardados

En sitios como LinkedIn o X, marca **Guardar para la próxima vez** cuando inicies sesión. Después, **Inicios de sesión** los mostrará y, si un sitio cierra la sesión de tu Machine, esta volverá a iniciarla con un solo toque. Las contraseñas se guardan cifradas en tu Machine. Pulsa **Olvidar** para eliminar un inicio de sesión.

Un sitio puede tener varias cuentas, como **Trabajo** y **Personal**. **Guardar como** empieza por la opción de la propia tarea, y **Otro nombre…** te permite ponerle el nombre que quieras. Las tareas inician sesión con la cuenta que les corresponde. Si no está claro cuál usar, un cuadro de diálogo te preguntará una vez y lo recordará para esa tarea.

**Inicios de sesión** muestra cada sitio una sola vez, con sus cuentas debajo: el nombre de usuario y un menú con su clasificación. Puedes cambiarla ahí cuando quieras. Los inicios de sesión guardados antes de que existieran las cuentas muestran **¿Trabajo o personal?** hasta que elijas una opción. Si cambias la clasificación, las tareas que usaban ese inicio de sesión volverán a preguntarte cuál usar.

**Importar** permite importar inicios de sesión desde un gestor de contraseñas: un archivo CSV exportado de 1Password, LastPass, Bitwarden o Chrome, o directamente desde las herramientas de línea de comandos de 1Password y LastPass si has iniciado sesión en ellas en este ordenador. Puedes marcar cuáles quieres conservar. Tu Machine nunca inicia sesión en tu gestor de contraseñas ni te pide la contraseña maestra. Cuando termines, elimina el archivo exportado.

Un inicio de sesión guardado solo se usa en su propia dirección web: el mismo sitio, `https` y puerto. No se usa en una dirección parecida ni en otro subdominio.

## Revisiones

**Revisiones** muestra cómo lee tu Machine lo que recibe: las revisiones recientes y lo que encontró en cada una. Consulta [No hay tareas nuevas](reviews-paused.md).

Cada conexión tiene su propio artículo en esta sección, donde se indica qué lee y qué puede enviar.
