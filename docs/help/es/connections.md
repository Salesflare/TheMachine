---
title: Conexiones
area: connections
summary: Tus fuentes en un solo lugar: consulta cómo va cada una, añade otra o desconéctala.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: ec53596a1636fee7
---
## Cómo van

La pestaña **Conexiones** muestra tus fuentes por tipo, con **Inicios de sesión** y **Revisiones** debajo de una línea. En el móvil, toca un tipo para abrirlo y **Conexiones** para volver. Primero se abre el tipo que tenga una fuente que te necesite. Cada fuente aparece en una fila, con su estado (Conectada, A la espera de la primera sincronización, Reconectando automáticamente o Necesita tu ayuda) y lo que ha llegado últimamente. Tócala para ver su ficha y **Detalles**.

Si una sincronización fallida se recuperó en una posterior, se muestra en gris. Solo aparece como problema el fallo más reciente, junto con la fecha del próximo intento.

Los recuentos muestran todo lo que ha traído, también su [historial](history.md), lo que ha llegado en las últimas 24 horas y lo que aún no se ha revisado. En los calendarios, se cuentan los eventos.

Cada fuente lleva el nombre de su cuenta, tal como la identifica el servicio: tu dirección, un perfil de X, un espacio de trabajo de Slack o de quién es la cuenta de Signal o Telegram. Debajo del nombre aparece primero **Trabajo** o **Personal**, además de la dirección o el nombre de usuario si el nombre no lo indica ya. Si hay dos fuentes del mismo tipo con el mismo nombre, también se muestra el dato que las diferencia, como Slack o X, o la dirección del espacio de trabajo.

Cada fuente también indica en una línea qué aporta y, si puede realizar acciones, que solo las lleva a cabo cuando pulsas **Enviar** o das tu aprobación.

## Añadir una fuente

Abre un tipo (**Correo**, **Calendario**, **Chat**, **Reuniones**, **Documentos y archivos**, **Clientes**, **Proyectos y código**, **Otras**) y elige una fuente en **Añadir otro**, o debajo de la lista si todavía no hay ninguna conectada. Al final aparecen las opciones genéricas: **Otro correo** en Correo, y **Enlace de calendario (ICS)** y **Otro calendario** en Calendario. Exchange Server lee las reuniones, así que está en Calendario.

**Sugerido para ti** aparece encima de **Conexiones** cuando tu Machine detecta un motivo para añadir una fuente. El motivo se indica en una línea: correos de Stripe, reuniones de Zoom en tu calendario, mensajes con enlaces a Google Docs o una configuración que no se completó. La fuente también aparece en su propio grupo, marcada como **Sugerido**. Esto se calcula en tu Machine; no sale nada de ella. Las fuentes conectadas nunca se sugieren.

Microsoft Teams aparece dos veces: en **Chat**, para sus chats, y en **Reuniones**, como **Reuniones de Teams**, para las notas de sus reuniones. Ambas opciones usan el mismo inicio de sesión de Microsoft, así que al conectar una también se conecta la otra.

En la lista, las fuentes que ya conectaste aparecen con su cuenta. Elígelas para añadir otra junto a ellas: el formulario lo indica y enlaza a la que ya tienes.

Completa los datos que te pida, como una clave o una dirección, elige **Trabajo** con el nombre de la empresa o **Personal** (en el caso del correo y los calendarios, solo te lo pregunta si la dirección no lo indica) y pulsa **Conectar**. Al conectar un sitio como LinkedIn o X, se abre su página de inicio de sesión en el navegador de tu Machine y el proceso continúa automáticamente cuando inicias sesión. GitHub, WhatsApp y Codex muestran un código que debes introducir. Los chats de Telegram y Signal muestran un código QR que debes escanear.

**Cancelar** detiene el proceso. ¿Te fuiste antes de terminar? Vuelve a abrir **Conexiones** desde cualquier dispositivo y podrás continuar desde el mismo paso. Cuando esté conectada, tu Machine empieza a leerla de inmediato y muestra cómo va la primera sincronización.

En una Machine alojada, puedes iniciar sesión aquí mismo en las fuentes que tienen su propio inicio de sesión: Google, Microsoft (Outlook, OneDrive y Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce y Trello.

Elige **Trabajo** o **Personal** y pulsa el botón de inicio de sesión correspondiente, como **Iniciar sesión con Google**. Volverás al formulario, donde se muestra el resultado. GitHub, WhatsApp, Codex, los chats de Telegram y tu teléfono Android también muestran aquí sus códigos.

En tu propio ordenador, puedes iniciar sesión en esas mismas fuentes cuando tu Machine esté vinculada a tu cuenta. La primera vez, pulsa **Vincular esta Machine**. Algunas también ofrecen otra opción, como usar tu propia aplicación o una clave.

**Reconectar**, tanto en una fuente como en **Te necesita**, abre el mismo formulario. En tu propio ordenador, `assistant connect` hace lo mismo desde una terminal.

## Trabajo o personal

Cada fuente se clasifica como de trabajo, para una empresa que indicas, o personal. Puedes cambiarlo en **Detalles**. **Adivinado** significa que tu Machine lo dedujo de la dirección. Las tareas de trabajo esperan a tus días laborables.

El correo y los calendarios de Google y Microsoft se clasifican según la dirección cuando está claro: un proveedor de correo como Gmail u Outlook.com se considera Personal, y el dominio de tu equipo, Trabajo. Si no está claro, te pregunta una vez justo después de iniciar sesión. **Cambiar** te permite elegirlo. Si más adelante el correo indica lo contrario, la tarea **Saca más partido a The Machine** te preguntará una vez si quieres cambiarlo.

## Permisos

Una fuente puede aportar señales (lo que llega se convierte en tareas), realizar acciones para tus tareas (leer un documento, o enviar, responder o cambiar algo cuando lo apruebas) o ambas cosas. Si hace ambas, **Detalles** muestra un interruptor para cada opción: **Trae señales** y **Puede hacer cosas**. Una de las dos siempre permanece activada. Para desactivar ambas, desconecta la fuente. Un chat solo tiene la opción **Puede hacer cosas**.

Si desactivas **Trae señales**, la fuente no se sincroniza. Si desactivas **Puede hacer cosas**, tu Machine nunca lee, redacta ni cambia nada con esa fuente.

## Quitar una fuente

Abre la fuente y ve a **Detalles**. Luego, pulsa **Desconectar**. Dejará de leerla, pero lo que ya haya incorporado se conservará. En una Machine alojada, las fuentes cuyo inicio de sesión está gestionado por tu página de configuración (Google, Microsoft, Google Meet, Slack, Zoom, Stripe y Salesforce) muestran **Desconectar ↗**, que abre esa página.

**Desconectado hace poco** muestra las cuentas de Google, Microsoft, Zoom, Slack, Stripe y Salesforce que quitaste en los últimos 30 días, junto con la fecha. Hasta que el servicio lo confirme, aparece el estado Pendiente y se sigue intentando. Una cuenta de Google aparece una sola vez, aunque Google Meet o Docs tuvieran su propio inicio de sesión. Cada cuenta aparece en su propio tipo: una cuenta de Google o Microsoft en **Correo**, y Slack en **Chat**.

## Inicios de sesión guardados

En sitios como LinkedIn o X, marca **Guardar para la próxima vez** al iniciar sesión. Después, **Inicios de sesión** muestra esas cuentas y, si un sitio cierra la sesión de tu Machine, puedes volver a iniciarla con un toque. Las contraseñas permanecen cifradas en tu Machine. Pulsa **Olvidar** para quitar una.

Un sitio puede tener varias cuentas, como **Trabajo** y **Personal**. **Guardar como** empieza con la opción correspondiente a la tarea, y **Otro nombre…** te permite ponerle el nombre que quieras. Una tarea inicia sesión con la cuenta que le corresponde. Si no está claro cuál es, el cuadro de diálogo te preguntará una vez y recordará tu elección para esa tarea.

**Inicios de sesión** muestra cada sitio una sola vez, con sus cuentas debajo. Los inicios de sesión guardados antes de que existieran las cuentas aparecen como **Predeterminada** hasta que les asignes una opción.

**Importar** permite importar inicios de sesión desde un gestor de contraseñas: una exportación CSV de 1Password, LastPass, Bitwarden o Chrome, o directamente desde las herramientas de línea de comandos de 1Password y LastPass, si tienes la sesión iniciada en ellas en este ordenador. Puedes marcar cuáles quieres conservar. Tu Machine nunca inicia sesión en el gestor de contraseñas ni te pide su contraseña maestra. Cuando termines, elimina el archivo exportado.

Un inicio de sesión guardado solo se usa en su propia dirección web: el mismo sitio, `https` y el mismo puerto. No se usa en una dirección parecida ni en otro subdominio.

## Revisiones

**Revisiones** muestra cómo lee tu Machine lo que llega: las revisiones recientes y lo que encontró cada una. Consulta [No hay tareas nuevas](reviews-paused.md).

Cada conexión tiene su propio artículo en esta sección, donde se explica qué lee y qué puede enviar.
