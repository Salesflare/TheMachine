---
title: Conexiones
area: connections
summary: Tus fuentes en un mismo sitio: consulta su estado, añade una o desconéctala.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 353fdfaa67678a1f
---
## Cómo van

La pestaña **Conexiones** muestra tus fuentes por tipo, con **Inicios de sesión** y **Revisiones** debajo de una línea. En el móvil, toca un tipo para abrirlo y **Conexiones** para volver. Si un tipo tiene una fuente que te necesita, se abre primero. Cada fuente aparece en una fila: muestra su estado (Conectada, Esperando la primera sincronización, Reconectando automáticamente o Necesita tu ayuda) y lo que ha llegado últimamente. Tócala para ver su tarjeta y **Detalles**.

Si una sincronización falla, pero una posterior lo compensa, se muestra en gris. Solo se marca como problema el fallo más reciente, junto con la hora del próximo intento.

Los recuentos muestran todo lo que ha recibido, incluido su [historial](history.md), lo que ha llegado en las últimas 24 horas y lo que aún no se ha revisado. En los calendarios se cuentan los eventos.

Cada fuente lleva el nombre de su cuenta, tal como lo muestra el servicio: tu dirección, un perfil de X, un espacio de trabajo de Slack o de quién es la cuenta de Signal o Telegram. Debajo del nombre aparece primero **Trabajo** o **Personal**, y también la dirección o el nombre de usuario si el nombre no lo indica ya. Si dos fuentes del mismo tipo tienen el mismo nombre, también se muestra cómo distinguirlas, por ejemplo, Slack o X, o la dirección del espacio de trabajo.

Cada fuente también indica en una línea qué recibe y, si puede actuar, que solo lo hace después de que pulses **Enviar** o des tu aprobación.

## Añadir una fuente

Abre un tipo (**Correo**, **Calendario**, **Chat**, **Reuniones**, **Documentos y archivos**, **Clientes**, **Proyectos y código**, **Otras**) y elige una fuente en **Añadir otro**, o debajo de la lista si aún no hay ninguna conectada. Al final aparecen las opciones generales: **Otro correo** en Correo, y **Enlace de calendario (ICS)** y **Otro calendario** en Calendario. Exchange Server lee las reuniones, así que aparece en Calendario.

**Sugerido para ti** aparece en la parte superior de **Conexiones** cuando tu Machine detecta un motivo para añadir una fuente. El motivo se indica en una línea: correos de Stripe, reuniones de Zoom en tu calendario, mensajes con enlaces a Google Docs o una configuración que no se completó. La fuente también aparece en su propio grupo, marcada como **Sugerido**. Tu Machine hace estos recuentos en ella; no sale nada de tu Machine. Las fuentes conectadas nunca se sugieren.

Microsoft Teams aparece dos veces: en **Chat**, para sus chats, y en **Reuniones** como **Reuniones de Teams**, para las notas de sus reuniones. Ambas opciones usan el mismo inicio de sesión de Microsoft, así que conectar una también conecta la otra.

La lista indica si ya has conectado una fuente y muestra su cuenta. Selecciónala para añadir otra junto a ella: el formulario lo indica y enlaza con la que ya tienes.

Introduce los datos que necesita (una clave, una dirección), elige **Trabajo** y el nombre de la empresa, o **Personal** (en el caso del correo y los calendarios, solo se pregunta si la dirección no lo deja claro), y pulsa **Conectar**. Si es un sitio como LinkedIn o X, se abre la página de inicio de sesión en el navegador de tu Machine y el proceso continúa automáticamente cuando inicias sesión. GitHub, WhatsApp y Codex muestran un código para introducir. Telegram y Signal muestran un código QR para escanear.

**Cancelar** detiene el proceso. ¿Te fuiste antes de terminar? Vuelve a abrir **Conexiones** en cualquier dispositivo y continuarás desde el mismo paso. Al conectarse, tu Machine empieza a leer la fuente de inmediato y muestra cómo va la primera sincronización.

En una Machine alojada, los servicios que tienen su propio inicio de sesión se conectan aquí mismo: Google, Microsoft (Outlook, OneDrive y Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce y Trello.

Elige **Trabajo** o **Personal** y pulsa el botón de inicio de sesión correspondiente, como **Iniciar sesión con Google**. Volverás a este formulario, donde verás cómo ha ido. GitHub, WhatsApp, Codex, los chats de Telegram y tu teléfono Android también muestran aquí su código.

En tu propio ordenador, puedes iniciar sesión en esos mismos servicios cuando tu Machine esté vinculada a tu cuenta. La primera vez, pulsa **Vincular esta Machine**. Algunos también ofrecen otra opción, como usar tu propia aplicación o una clave.

**Reconectar**, tanto en una fuente como en **Te necesita**, abre el mismo formulario. En tu propio ordenador, `assistant connect` hace lo mismo desde un terminal.

## Trabajo o personal

Cada fuente se clasifica como de trabajo (para una empresa que indicas) o personal. Puedes cambiarlo en **Detalles**. **Adivinado** significa que tu Machine lo dedujo a partir de la dirección. Las tareas de trabajo esperan hasta tus días laborables.

El correo y los calendarios de Google y Microsoft se clasifican según la dirección cuando está claro: un proveedor de correo como Gmail o Outlook.com es Personal; el dominio de tu equipo es Trabajo. Si no está claro, se te pregunta una vez, justo después de iniciar sesión. **Cambiar** te permite elegirlo. Si más adelante el correo indica lo contrario, la tarea **Saca más partido a The Machine** te preguntará una vez si quieres cambiarlo.

## Funciones

Una fuente puede recibir señales (lo que llega se convierte en tareas), hacer cosas para tus tareas (leer un documento, o enviar, responder o cambiar algo después de que lo apruebes), o ambas cosas. Si hace ambas, **Detalles** muestra un interruptor para cada función: **Trae señales** y **Puede hacer cosas**. Una debe permanecer activada. Para detener ambas, desconecta la fuente. Los chats solo tienen **Puede hacer cosas**.

Si desactivas **Trae señales**, la fuente no se sincroniza. Si desactivas **Puede hacer cosas**, tu Machine nunca lee, redacta ni cambia nada con esa fuente.

## Quitar una fuente

Abre la fuente, ve a **Detalles** y pulsa **Desconectar**. Dejará de leerla. Lo que ya recibió se conserva. En una Machine alojada, las fuentes cuyo inicio de sesión se gestiona desde la página de configuración muestran **Desconectar ↗**. Al pulsarlo, se abre esa página. Son Google, Microsoft, Google Meet, Slack, Zoom, Stripe y Salesforce.

**Desconectado hace poco** muestra las cuentas de Google, Microsoft, Zoom, Slack, Stripe y Salesforce que quitaste en los últimos 30 días, y cuándo las quitaste. Hasta que el servicio lo confirme, aparecerán como Pendiente y se seguirá intentando. Una cuenta de Google aparece una sola vez, incluso si Google Meet o Docs tenían su propio inicio de sesión. Cada cuenta aparece en su propio tipo: una cuenta de Google o Microsoft en **Correo**, y una de Slack en **Chat**.

## Inicios de sesión guardados

Para sitios como LinkedIn o X, marca **Guardar para la próxima vez** al iniciar sesión. Después, **Inicios de sesión** muestra las cuentas guardadas y, si un sitio cierra la sesión de tu Machine, puedes volver a iniciarla con un toque. Las contraseñas permanecen cifradas en tu Machine. **Olvidar** elimina una cuenta guardada.

Un sitio puede tener varias cuentas, como **Trabajo** y **Personal**. **Guardar como** empieza con la opción correspondiente a la tarea, y **Otro nombre…** te permite ponerle el nombre que quieras. Las tareas inician sesión con la cuenta que les corresponde. Si no está claro cuál es, el cuadro de diálogo te pregunta una vez y lo recuerda para esa tarea.

**Inicios de sesión** muestra cada sitio una sola vez y, debajo, sus cuentas: el nombre de usuario y un menú con su categoría. Puedes cambiar la categoría cuando quieras. Los inicios de sesión guardados antes de que existieran las cuentas muestran **¿Trabajo o personal?** hasta que elijas una opción. Si cambias la categoría de un inicio de sesión, las tareas que lo usaban volverán a preguntarte cuál elegir.

**Importar** permite importar inicios de sesión desde un gestor de contraseñas. Elige uno:

- **LastPass**, **Bitwarden** o **Google Password Manager**: la página de exportación se abre en el navegador de tu Machine y se muestra directamente en el cuadro de diálogo, igual que cuando una tarea te pide que la ejecutes con **Hazlo**. Inicia sesión allí y tu Machine continuará con la exportación. Una línea indica qué te falta hacer, como escribir la contraseña maestra. En el móvil, la vista se acerca al lugar donde tienes que escribir. Si la página no tiene el aspecto esperado, se muestran los pasos para terminar manualmente. Tu Machine recoge el archivo, lo lee una vez y lo elimina.
- **1Password**: exporta un archivo CSV desde la aplicación de 1Password en un ordenador y selecciónalo. Si `op` de 1Password tiene la sesión iniciada en tu Machine, lo lee desde allí (también `lpass` de LastPass).
- **Desde un archivo exportado**: un archivo CSV de 1Password, LastPass, Bitwarden o Chrome. Elimínalo cuando termines.

Después, marca cuáles quieres conservar. Tu Machine nunca inicia sesión en tu gestor de contraseñas por ti, nunca escribe ni lee la contraseña maestra y nunca muestra la página a la asistente: tú escribes la contraseña en la página.

Un inicio de sesión guardado solo se usa en su propia dirección web: el mismo sitio, `https` y el mismo puerto. No se usa en una dirección parecida ni en otro subdominio.

## Revisiones

**Revisiones** muestra cómo tu Machine lee lo que llega: las revisiones recientes y lo que encontró cada una. Consulta [No hay tareas nuevas](reviews-paused.md).

Cada conexión tiene su propio artículo en esta sección, donde se explica qué lee y qué puede enviar.
