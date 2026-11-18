---
title: Conexiones
area: connections
summary: Tus fuentes en un solo lugar: cómo va cada una, cómo añadir una nueva o desconectarla.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 809547189ccfa026
---
## Cómo van

La pestaña **Conexiones** muestra tus fuentes por tipo, y debajo de una línea, **Inicios de sesión** y **Revisiones**. En el móvil, toca un tipo para abrirlo y **Conexiones** para volver. Primero se abre el tipo que tenga una fuente que te necesita. Cada fuente aparece en una fila: su estado (Conectada, Esperando la primera sincronización, Reconectando automáticamente o Necesita tu ayuda) y lo que ha llegado hace poco. Tócala para ver su tarjeta y **Detalles**.

Si una sincronización falla pero otra posterior lo soluciona, el fallo aparece en gris. Solo se muestra como problema el último intento fallido, junto con la hora del próximo intento.

El recuento incluye todo lo que ha traído, también lo que aparece en el [historial](history.md), lo que ha llegado en las últimas 24 horas y lo que aún no se ha revisado. En un calendario se cuentan los eventos.

Cada fuente lleva el nombre de su cuenta tal como lo muestra el servicio: tu dirección, un perfil de X, un espacio de trabajo de Slack o de quién es la cuenta de Signal o Telegram. Debajo del nombre aparece primero **Trabajo** o **Personal**, además de la dirección o el nombre de usuario si el nombre no los incluye ya. Si hay dos fuentes del mismo tipo con el mismo nombre, también se indica cómo distinguirlas, por ejemplo, Slack o X, o la dirección del espacio de trabajo.

Cada fuente también explica en una línea qué aporta y, si puede realizar acciones, indica que solo las hará cuando pulses **Enviar** o las apruebes.

## Añadir una fuente

Abre un tipo (**Correo**, **Calendario**, **Chat**, **Reuniones**, **Documentos y archivos**, **Clientes**, **Proyectos y código**, **Otras**) y elige una fuente en **Añadir otro**, o debajo de la lista si aún no hay ninguna conectada. Al final encontrarás una opción genérica: **Otro correo** en Correo, y **Enlace de calendario (ICS)** y **Otro calendario** en Calendario. Exchange Server lee reuniones, por eso está en Calendario.

Cuando tu Machine detecta un motivo para añadir una fuente, **Sugerido para ti** aparece en la parte superior de **Conexiones**, con una breve explicación: correos de Stripe, reuniones de Zoom en tu calendario, mensajes con enlaces a Google Docs o una configuración que no se completó. La fuente también aparece en su propio grupo, marcada como **Sugerido**. Este recuento se calcula en tu Machine, nada sale de ella. Las fuentes conectadas nunca se sugieren.

Microsoft Teams aparece dos veces: en **Chat**, para sus chats, y en **Reuniones**, como **Reuniones de Teams**, para las notas de sus reuniones. Ambas usan el mismo inicio de sesión de Microsoft, así que al conectar una también se conecta la otra.

Si ya conectaste una fuente, la lista lo indica junto con su cuenta. Selecciónala para añadir otra al lado: el formulario lo indica y enlaza a la que ya tienes.

Completa los datos que necesita, como una clave o una dirección, elige **Trabajo** y el nombre de tu empresa o **Personal** (el correo y los calendarios solo preguntan si la dirección no lo deja claro) y pulsa **Conectar**. En servicios como LinkedIn o X, se abre la página de inicio de sesión en el navegador de tu Machine y el proceso continúa automáticamente cuando inicias sesión. GitHub, WhatsApp y Codex muestran un código que debes introducir. En los chats de Telegram y Signal, aparece un código QR para escanear.

**Cancelar** detiene el proceso. ¿Saliste antes de terminar? Vuelve a abrir **Conexiones** desde cualquier dispositivo y continuarás donde lo dejaste. Una vez conectada, tu Machine empieza a leer la fuente enseguida y muestra cómo avanza la primera sincronización.

En una Machine alojada, puedes iniciar sesión aquí mismo en las fuentes que tienen su propio inicio de sesión: Google, Microsoft (Outlook, OneDrive y Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce y Trello.

Elige **Trabajo** o **Personal** y pulsa el botón de inicio de sesión, como **Iniciar sesión con Google**. Volverás a este formulario, que te mostrará el resultado. GitHub, WhatsApp, Codex, los chats de Telegram y tu teléfono Android también muestran aquí su código.

En tu propio ordenador, puedes iniciar sesión en esas mismas fuentes cuando vincules tu Machine a tu cuenta: pulsa **Vincular esta Machine** la primera vez. Algunas también ofrecen otra forma de conectarse, como tu propia aplicación o una clave.

**Reconectar**, tanto en una fuente como en **Te necesita**, abre el mismo formulario. En tu propio ordenador, `assistant connect` hace lo mismo desde un terminal.

## Trabajo o personal

Cada fuente se clasifica como de trabajo, para una empresa que indiques, o personal. Puedes cambiarlo en **Detalles**. **Calculado** significa que tu Machine lo dedujo a partir de la dirección. Las tareas de trabajo esperan a tus días laborables.

El correo y los calendarios de Google y Microsoft se clasifican según la dirección cuando está claro: un proveedor de correo como Gmail u Outlook.com se considera Personal, y el dominio de tu equipo, Trabajo. Si no está claro, se te pregunta una vez justo después de iniciar sesión. **Cambiar** te permite elegirlo. Si más adelante el correo indica lo contrario, la tarea **Saca más partido a The Machine** te preguntará una vez si quieres cambiarlo.

## Funciones

Una fuente puede traer señales (lo que llega se convierte en tareas), realizar acciones para tus tareas (leer un documento, o enviar, responder o cambiar algo después de que lo apruebes), o ambas cosas. Si hace las dos, **Detalles** incluye un interruptor para cada función: **Trae señales** y **Puede hacer cosas**. Una debe permanecer activada. Para desactivar ambas, desconecta la fuente. Los chats solo tienen **Puede hacer cosas**.

Si desactivas **Trae señales**, la fuente no se sincroniza. Si desactivas **Puede hacer cosas**, tu Machine nunca lee, redacta ni cambia nada con esa fuente.

## Quitar una fuente

Abre la fuente, ve a **Detalles** y pulsa **Desconectar**. Dejará de leerla. Lo que ya haya importado se conserva. En una Machine alojada, las fuentes cuyo inicio de sesión gestiona tu página de configuración (Google, Microsoft, Google Meet, Slack, Zoom, Stripe y Salesforce) muestran **Desconectar ↗**, que abre esa página.

**Desconectado hace poco** muestra las cuentas de Google, Microsoft, Zoom, Slack, Stripe y Salesforce que eliminaste en los últimos 30 días, y cuándo las quitaste. Hasta que el servicio lo confirme, aparece como Pendiente y se sigue intentando. Una cuenta de Google aparece una sola vez, aunque Google Meet o Docs tuviera su propio inicio de sesión. Cada cuenta aparece en su tipo correspondiente: una cuenta de Google o Microsoft en **Correo**, y Slack en **Chat**.

## Inicios de sesión guardados

En sitios como LinkedIn o X, marca **Guardar para la próxima vez** al iniciar sesión. Después, **Inicios de sesión** los muestra y, si un sitio cierra la sesión de tu Machine, puedes volver a iniciarla con un toque. Las contraseñas permanecen cifradas en tu Machine. Pulsa **Olvidar** para eliminar una.

Un sitio puede tener varias cuentas, como **Trabajo** y **Personal**. **Guardar como** empieza con el tipo de la tarea y **Otro nombre…** te permite ponerle el nombre que quieras. Una tarea inicia sesión con la cuenta que le corresponde. Si no está claro cuál es, un cuadro de diálogo te pregunta una vez y recuerda la elección para esa tarea.

**Inicios de sesión** muestra cada sitio una sola vez, con sus cuentas debajo: el nombre de usuario y un menú con el tipo de cuenta. Puedes cambiarlo ahí cuando quieras. Los inicios de sesión guardados antes de que existieran las cuentas muestran **¿Trabajo o personal?** hasta que elijas una opción. Si cambias el tipo de cuenta, las tareas que usaban ese inicio de sesión volverán a preguntarte cuál usar.

**Importar** añade inicios de sesión desde un gestor de contraseñas. Elige uno:

- **LastPass**, **Bitwarden** o **Google Password Manager**: se abre la página de exportación en el navegador de tu Machine. Inicia sesión y exporta desde ahí; los pasos aparecen al lado. Tu Machine encontrará el archivo, lo leerá una vez y lo eliminará.
- **1Password**: exporta un CSV desde la aplicación de 1Password en un ordenador y luego selecciona ese archivo. Si la `op` de 1Password está iniciada en tu Machine, lo leerá desde ahí en su lugar (también la `lpass` de LastPass).
- **Desde un archivo exportado**: un CSV de 1Password, LastPass, Bitwarden o Chrome. Elimínalo cuando hayas terminado.

Después, marca cuáles quieres conservar. Tu Machine nunca inicia sesión en el gestor de contraseñas por ti ni te pide la contraseña maestra: la escribes tú en la página.

Un inicio de sesión guardado solo se usa en su propia dirección web: el mismo sitio, `https` y puerto. Nunca en una dirección parecida ni en otro subdominio.

## Revisiones

**Revisiones** muestra cómo lee tu Machine lo que llega: las revisiones recientes y lo que encontró en cada una. Consulta [No hay tareas nuevas](reviews-paused.md).

Cada conexión tiene su propio artículo en esta sección, donde se explica qué lee y qué puede enviar.
