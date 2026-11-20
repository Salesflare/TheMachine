---
title: Conexiones
area: connections
summary: Tus fuentes en un mismo lugar: consulta cómo va cada una, añade otra o desconéctala.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 38d682b69cab758d
---
## Cómo van

La pestaña **Conexiones** muestra tus fuentes por tipo, con **Inicios de sesión** y **Revisiones** debajo de una línea divisoria. En el teléfono, toca un tipo para abrirlo y **Conexiones** para volver. Primero se abre el tipo que tenga una fuente que te necesite. Cada fuente aparece en una fila con su estado (Conectada, Esperando la primera sincronización, Reconectando automáticamente o Necesita tu ayuda) y lo que ha recibido últimamente. Tócala para ver su tarjeta y **Detalles**.

Si una sincronización falla, pero otra posterior lo soluciona, el fallo aparece en gris. Solo se muestra como problema el fallo más reciente, junto con la fecha del próximo intento.

Los recuentos muestran todo lo que ha recibido, incluido su [historial](history.md), lo que ha recibido en las últimas 24 horas y lo que aún no se ha revisado. En un calendario se cuentan los eventos.

Cada fuente lleva el nombre de su cuenta, tal como la identifica el servicio: tu dirección, un perfil de X, un espacio de trabajo de Slack o la persona a la que pertenecen Signal o Telegram. Debajo del nombre aparece primero **Trabajo** o **Personal**, además de la dirección o el nombre de usuario si el nombre no los incluye. Si dos fuentes del mismo tipo tienen el mismo nombre, también se muestra el dato que las distingue, como Slack o X, o la dirección del espacio de trabajo.

Cada fuente también indica en una línea qué aporta y, si puede realizar acciones, que solo las hará después de que pulses **Enviar** o las autorices.

## Añadir una

Abre un tipo (**Correo**, **Calendario**, **Chat**, **Reuniones**, **Documentos y archivos**, **Clientes**, **Proyectos y código**, **Otras**) y elige una fuente en **Añadir otro**, o debajo de la lista si aún no hay ninguna conectada. Al final aparece una opción para cualquier otro caso: **Otro correo** en Correo, y **Enlace de calendario (ICS)** y **Otro calendario** en Calendario. Exchange Server lee las reuniones, por eso está en Calendario.

**Sugerido para ti** aparece encima de **Conexiones** cuando tu Machine detecta un motivo para sugerir una fuente. El motivo se explica en una línea: correos de Stripe, reuniones de Zoom en tu calendario, mensajes con enlaces a Google Docs o una configuración que no se completó. La fuente también aparece en su propio grupo, marcada como **Sugerido**. El recuento se calcula en tu Machine: no se envía nada. Las fuentes conectadas nunca se sugieren.

Microsoft Teams aparece dos veces: en **Chat**, para sus chats, y en **Reuniones**, como **Reuniones de Teams**, para las notas de sus reuniones. Ambas usan el mismo inicio de sesión de Microsoft, así que al conectar una también se conecta la otra.

Si ya has conectado una fuente, la lista lo indica junto con su cuenta. Selecciónala para añadir otra al lado: el formulario te lo indica y enlaza con la que ya tienes.

Introduce los datos que necesite, como una clave o una dirección, elige **Trabajo** e indica la empresa, o elige **Personal**. En el caso del correo y los calendarios, solo se te pregunta si la dirección no lo deja claro. Luego pulsa **Conectar**. En sitios como LinkedIn o X, se abre el inicio de sesión en el navegador de tu Machine y el proceso continúa automáticamente cuando inicias sesión. GitHub, WhatsApp y Codex muestran un código que debes introducir. Telegram y Signal muestran un código QR que debes escanear.

**Cancelar** detiene el proceso. Si sales antes de terminar, vuelve a abrir **Conexiones** desde cualquier dispositivo y continuarás en el mismo paso. Cuando se conecta, tu Machine empieza a leer la fuente enseguida y muestra el estado de la primera sincronización.

En una Machine alojada, las fuentes que tienen su propio inicio de sesión se conectan aquí: Google, Microsoft (Outlook, OneDrive y Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce y Trello.

Elige **Trabajo** o **Personal** y pulsa el botón de inicio de sesión correspondiente, como **Iniciar sesión con Google**. Volverás a este formulario, donde se mostrará el resultado. GitHub, WhatsApp, Codex, los chats de Telegram y tu teléfono Android también muestran aquí su código.

En tu propio ordenador, esas mismas fuentes se conectan cuando vinculas tu Machine a tu cuenta. La primera vez, pulsa **Vincular esta Machine**. Algunas también ofrecen otra opción, como usar tu propia aplicación o una clave.

**Reconectar**, en una fuente o en **Te necesita**, abre el mismo formulario. En tu propio ordenador, `assistant connect` hace lo mismo desde un terminal.

## Trabajo o personal

Cada fuente se clasifica como de trabajo, para una empresa que indiques, o personal. Puedes cambiarlo en **Detalles**. El estado **Inferido** significa que tu Machine lo dedujo a partir de la dirección. Las tareas de trabajo esperan hasta tus días laborables.

El correo y los calendarios de Google y Microsoft se clasifican a partir de la dirección cuando está claro: un proveedor de correo como Gmail u Outlook.com es Personal, y el dominio de tu equipo es Trabajo. Si no está claro, se te pregunta una vez justo después de iniciar sesión. **Cambiar** te permite elegirlo. Si más adelante el correo indica lo contrario, la tarea **Saca más partido a The Machine** te preguntará una vez si quieres cambiarlo.

## Qué puede hacer

Una fuente puede aportar señales (lo que recibe se convierte en tareas), hacer cosas para tus tareas (leer un documento o enviar, responder o cambiar algo después de que lo autorices), o ambas cosas. Si puede hacer ambas, **Detalles** muestra un interruptor para cada opción: **Trae señales** y **Puede hacer cosas**. Una de las dos debe permanecer activada. Para detener ambas, desconecta la fuente. Un chat solo tiene **Puede hacer cosas**.

Si desactivas **Trae señales**, la fuente no se sincroniza. Si desactivas **Puede hacer cosas**, tu Machine nunca lee, redacta ni cambia nada con esa fuente.

## Quitar una fuente

Abre la fuente, ve a **Detalles** y pulsa **Desconectar**. Dejará de leerla, pero lo que ya haya recibido se conservará. En una Machine alojada, las fuentes cuyo inicio de sesión está en tu página de configuración (Google, Microsoft, Google Meet, Slack, Zoom, Stripe y Salesforce) muestran **Desconectar ↗**, que abre esa página.

**Desconectado hace poco** muestra las cuentas de Google, Microsoft, Zoom, Slack, Stripe y Salesforce que quitaste en los últimos 30 días, y cuándo las quitaste. Hasta que el servicio lo confirme, aparece como Pendiente y se sigue intentando. Una cuenta de Google solo aparece una vez, incluso si Google Meet o Docs tenían su propio inicio de sesión. Cada cuenta aparece en su tipo: una cuenta de Google o Microsoft en **Correo**, y una de Slack en **Chat**.

## Inicios de sesión guardados

En sitios como LinkedIn o X, marca **Guardar para la próxima vez** al iniciar sesión. Después, **Inicios de sesión** muestra esas cuentas y, cuando un sitio cierra la sesión de tu Machine, puedes volver a iniciarla con un solo toque. Las contraseñas se mantienen cifradas en tu Machine. **Olvidar** elimina una cuenta.

Un sitio puede tener varias cuentas, como **Trabajo** y **Personal**. **Guardar como** empieza con el ámbito de la tarea, y **Otro nombre…** te permite elegir un nombre. Una tarea inicia sesión con la cuenta que le corresponde. Si no está claro cuál es, el cuadro de diálogo te lo pregunta una vez y lo recuerda para esa tarea.

**Inicios de sesión** muestra cada sitio una sola vez, con sus cuentas debajo: el nombre de usuario y un menú con su ámbito. Puedes cambiarlo cuando quieras. Los inicios de sesión guardados antes de que existieran las cuentas muestran **¿Trabajo o personal?** hasta que elijas una opción. Si cambias el ámbito, una tarea que usaba ese inicio de sesión vuelve a preguntarte cuál usar.

**Importar** añade inicios de sesión desde un gestor de contraseñas. Elige uno:

- **LastPass**, **Bitwarden** o **Google Password Manager**: se abre la página de exportación en el navegador de tu Machine. Inicia sesión allí y tu Machine continúa con la exportación. Una línea te indica qué queda por hacer, como escribir tu contraseña maestra. En el teléfono, la vista se acerca al lugar donde tienes que escribir. Si la página no tiene el aspecto esperado, se muestran los pasos para terminar manualmente. Tu Machine recoge el archivo, lo lee una vez y lo elimina.
- **1Password**: exporta un CSV desde la aplicación de 1Password en un ordenador y luego selecciona ese archivo. Si has iniciado sesión en `op` de 1Password desde tu Machine, lo leerá directamente desde ahí. Lo mismo ocurre con `lpass` de LastPass.
- **Desde un archivo exportado**: un CSV de 1Password, LastPass, Bitwarden o Chrome. Elimínalo cuando termines.

Después, marca cuáles quieres conservar. Tu Machine nunca inicia sesión en tu gestor de contraseñas por ti, ni escribe ni lee su contraseña maestra, ni muestra la página a la asistente. Tú escribes la contraseña en la página.

Un inicio de sesión guardado solo se usa en su propia dirección web: el mismo sitio, `https` y puerto. No se usa en una dirección parecida ni en otro subdominio.

## Revisiones

**Revisiones** muestra cómo lee tu Machine lo que recibe: las revisiones recientes y lo que encontró cada una. Consulta [No hay tareas nuevas](reviews-paused.md).

Cada conexión tiene su propio artículo en esta sección, donde se explica qué lee y qué puede enviar.
