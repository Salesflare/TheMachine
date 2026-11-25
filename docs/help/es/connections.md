---
title: Conexiones
area: connections
summary: Todas tus fuentes en un mismo lugar: consulta su estado, añade una nueva o desconéctala.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 0896d8f689ca9699
---
## Cómo va cada una

La pestaña **Conexiones** muestra tus fuentes por tipo, con **Inicios de sesión** y **Revisiones** debajo de una línea. En el móvil, toca un tipo para abrirlo y **Conexiones** para volver. Primero se abre el tipo que tenga una fuente que requiera tu atención. Cada fuente aparece en una fila: muestra su estado (Conectado, Esperando la primera sincronización, Reconectando automáticamente o Necesita tu ayuda) y lo que ha recibido últimamente. Tócala para ver su tarjeta y **Detalles**.

Si una sincronización falla, pero otra posterior lo soluciona, se muestra en gris. Solo se marca como problema el fallo más reciente, junto con la hora a la que volverá a intentarlo.

Los recuentos incluyen todo lo que ha incorporado, también su [historial](history.md), lo recibido en las últimas 24 horas y lo que aún no se ha revisado. En un calendario, se cuentan sus eventos.

Cada fuente lleva el nombre de su cuenta, tal como la identifica el servicio: tu dirección, un perfil de X, un espacio de trabajo de Slack o la persona a la que pertenece la cuenta de Signal o Telegram. Debajo del nombre aparece primero **Trabajo** o **Personal**, y también la dirección o el nombre de usuario si el nombre no los incluye ya. Si hay dos fuentes del mismo tipo con el mismo nombre, se indica además qué las distingue, como Slack o X, o la dirección del espacio de trabajo.

Cada fuente también explica en una línea qué incorpora y, si puede actuar, que solo lo hará cuando pulses **Enviar** o des tu aprobación.

## Añadir una fuente

Abre un tipo (**Correo**, **Calendario**, **Chat**, **Reuniones**, **Documentos y archivos**, **Clientes**, **Proyectos y código**, **Otras**) y elige una fuente en **Añadir otro**, o debajo de la lista si aún no hay ninguna conectada. Al final aparecen las opciones genéricas: **Otro correo** en Correo, y **Enlace de calendario (ICS)** y **Otro calendario** en Calendario. Exchange Server lee reuniones, por eso aparece en Calendario.

**Sugerido para ti** aparece en la parte superior de **Conexiones** cuando tu Machine detecta un motivo para añadir una fuente. El motivo se explica en una línea: correos de Stripe, reuniones de Zoom en tu calendario, mensajes con enlaces a Google Docs o una configuración que no se completó. La fuente también sigue apareciendo en su grupo, marcada como **Sugerido**. Estos recuentos se calculan en tu Machine; nada sale de ella. Nunca se sugiere una fuente que ya esté conectada.

Microsoft Teams aparece dos veces: en **Chat**, para sus chats, y en **Reuniones**, como **Reuniones de Teams**, para las notas de sus reuniones. Ambas opciones usan el mismo inicio de sesión de Microsoft, así que al conectar una también se conecta la otra.

En la lista, las fuentes que ya conectaste aparecen identificadas con su cuenta. Selecciónalas para añadir otra junto a ellas: el formulario lo indica y enlaza con la que ya tienes.

Completa los datos necesarios (una clave o una dirección), elige **Trabajo** e indica la empresa, o elige **Personal**. En Correo y Calendario solo se te pregunta si la dirección no lo deja claro. Luego, pulsa **Conectar**. Si el servicio es un sitio como LinkedIn o X, se abre su inicio de sesión en el navegador de tu Machine y el proceso continúa automáticamente cuando inicias sesión. GitHub, WhatsApp y Codex muestran un código para introducir; los chats de Telegram y Signal muestran un código QR para escanear.

**Cancelar** detiene el proceso. ¿Te fuiste antes de terminar? Vuelve a abrir **Conexiones** desde cualquier dispositivo y continuarás desde el mismo paso. Una vez conectada, tu Machine empieza a leer la fuente de inmediato y muestra cómo va la primera sincronización.

En una Machine alojada, puedes iniciar sesión aquí directamente en las fuentes que tienen su propio inicio de sesión: Google, Microsoft (Outlook, OneDrive y Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce y Trello.

Elige **Trabajo** o **Personal** y pulsa el botón de inicio de sesión correspondiente, como **Iniciar sesión con Google**. Volverás a este formulario, donde verás el resultado. Aquí también se muestran los códigos de GitHub, WhatsApp, Codex, los chats de Telegram y tu teléfono Android.

En tu propio ordenador, esas mismas fuentes permiten iniciar sesión cuando vinculas tu Machine a tu cuenta. La primera vez, pulsa **Vincular esta Machine**. Algunas también ofrecen otra opción, como usar tu propia aplicación o una clave.

**Reconectar**, tanto en una fuente como en **Te necesita**, abre el mismo formulario. En tu propio ordenador, `assistant connect` hace lo mismo desde un terminal.

## Trabajo o personal

Cada fuente se clasifica como de trabajo (para una empresa que indiques) o personal. Puedes cambiarlo en **Detalles**. **Inferido** significa que tu Machine lo dedujo a partir de la dirección. Las tareas de trabajo esperan a tus días laborables.

El correo y los calendarios de Google y Microsoft se clasifican según la dirección cuando está claro: un proveedor de correo como Gmail u Outlook.com se considera Personal; el dominio de tu equipo, Trabajo. Si no está claro, se te pregunta una vez, justo después de iniciar sesión. **Cambiar** te permite elegirlo. Si más adelante los correos indican lo contrario, la tarea **Saca más partido a The Machine** te preguntará una vez si quieres cambiarlo.

## Funciones

Una fuente puede incorporar señales (lo que recibe se convierte en tareas), hacer cosas para tus tareas (leer un documento, o enviar, responder o cambiar algo después de que lo apruebes), o ambas cosas. Si hace ambas, **Detalles** incluye un interruptor para cada función: **Trae señales** y **Puede hacer cosas**. Una siempre permanece activada. Para detener ambas, desconecta la fuente. Los chats solo tienen **Puede hacer cosas**.

Si desactivas **Trae señales**, la fuente no se sincroniza. Si desactivas **Puede hacer cosas**, tu Machine nunca lee, redacta ni cambia nada con esa fuente.

## Quitar una fuente

Abre la fuente, ve a **Detalles** y pulsa **Desconectar**. Dejará de leerla. Lo que ya había incorporado se conserva. En una Machine alojada, las fuentes cuyo inicio de sesión administra la página de configuración muestran **Desconectar ↗**. Al pulsarlo, se abre esa página. Estas fuentes son Google, Microsoft, Google Meet, Slack, Zoom, Stripe y Salesforce.

**Desconectado hace poco** muestra las cuentas de Google, Microsoft, Zoom, Slack, Stripe y Salesforce que quitaste en los últimos 30 días, y cuándo las quitaste. Hasta que el servicio lo confirme, aparece el estado Pendiente y se sigue intentando. Una cuenta de Google aparece una sola vez, incluso si Google Meet o Docs tenían su propio inicio de sesión. Cada cuenta aparece en su tipo correspondiente: una cuenta de Google o Microsoft en **Correo**, y Slack en **Chat**.

## Inicios de sesión guardados

En sitios como LinkedIn o X, marca **Guardar para la próxima vez** al iniciar sesión. Después, **Inicios de sesión** muestra esas cuentas y, si el sitio cierra la sesión de tu Machine, esta vuelve a iniciarla con un solo toque. Las contraseñas permanecen cifradas en tu Machine. **Olvidar** elimina una cuenta.

Un sitio puede tener varias cuentas, como **Trabajo** y **Personal**. **Guardar como** empieza con la clasificación de la tarea, y **Otro nombre…** te permite elegir un nombre. Las tareas inician sesión con la cuenta que les corresponde. Si no está claro cuál es, un cuadro de diálogo te pregunta una vez y recuerda la elección para esa tarea.

**Inicios de sesión** muestra cada sitio una sola vez, con sus cuentas debajo: el nombre de usuario y un menú con su clasificación. Puedes cambiarla ahí cuando quieras. Los inicios de sesión guardados antes de que existieran las cuentas muestran **¿Trabajo o personal?** hasta que elijas una opción. Si cambias la clasificación de una cuenta usada por una tarea, la tarea vuelve a preguntarte cuál usar.

**Importar** añade inicios de sesión desde un gestor de contraseñas. Elige uno:

- **LastPass**, **Bitwarden** o **Google Password Manager**: la página de exportación se abre en el navegador de tu Machine y aparece directamente en el cuadro de diálogo, igual que al pulsar **Hazlo** en una tarea. Inicia sesión ahí y tu Machine avanzará hasta la exportación. Una indicación te dirá qué falta, por ejemplo, escribir tu contraseña maestra. LastPass envía por correo un enlace para confirmar la exportación. Tu Machine inicia el proceso una vez y abre el enlace automáticamente si el correo llega a un buzón conectado en un plazo de 10 minutos. Si no, te pide que confirmes y vuelvas a exportar. En el móvil, la vista se amplía hasta el campo donde tienes que escribir. Si la página no tiene el aspecto esperado, se muestran los pasos para completar el proceso manualmente. Tu Machine recoge el archivo, lo lee una vez y lo elimina.
- **1Password**: exporta un archivo CSV desde la aplicación 1Password en un ordenador y luego selecciona ese archivo. Si `op` de 1Password tiene una sesión iniciada en tu Machine, lo lee desde ahí (también `lpass` de LastPass).
- **Desde un archivo exportado**: un archivo CSV de 1Password, LastPass, Bitwarden o Chrome. Elimínalo cuando termines.

Después, marca los inicios de sesión que quieras conservar. Tu Machine nunca inicia sesión en tu gestor de contraseñas por ti, ni escribe ni lee tu contraseña maestra, y tampoco muestra la página al asistente: la contraseña la escribes tú en la página.

Un inicio de sesión guardado solo se usa en su propia dirección web: el mismo sitio, `https` y el mismo puerto. No se usa en una dirección parecida ni en otro subdominio.

## Revisiones

**Revisiones** muestra cómo lee tu Machine lo que recibe: las revisiones recientes y lo que encontró cada una. Consulta [Sin tareas nuevas](reviews-paused.md).

Cada conexión tiene su propio artículo en esta sección, donde se explica qué lee y qué puede enviar.
