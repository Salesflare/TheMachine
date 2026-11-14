---
title: Conexiones
area: connections
summary: Tus fuentes en un solo lugar: consulta cómo va cada una, añade otra o desconéctala.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 1ca62ab8f65b77ff
---
## Cómo van

La pestaña **Conexiones** muestra tus fuentes por tipo, con **Inicios de sesión** y **Revisiones** debajo de una línea. En el móvil, toca un tipo para abrirlo y **Conexiones** para volver. Primero se abre el tipo que tenga una fuente que te necesite. Cada fuente aparece en una fila: muestra cómo va (Conectada, Esperando la primera sincronización, Reconectando automáticamente o Necesita tu ayuda) y qué ha recibido últimamente. Tócala para ver su tarjeta y **Detalles**.

Los errores de sincronización que se hayan corregido en una sincronización posterior aparecen en gris. Solo se muestra como problema el error que siga siendo el más reciente, junto con la fecha de la próxima sincronización.

Las cifras muestran todo lo que ha incorporado, incluido su [historial](history.md), lo que ha llegado en las últimas 24 horas y lo que aún no se ha revisado. En los calendarios, se cuentan los eventos.

Cada fuente lleva el nombre de su cuenta, tal como la llama el servicio: tu dirección, un perfil de X, un espacio de trabajo de Slack o la persona cuya cuenta de Signal o Telegram es. Debajo del nombre aparece primero **Trabajo** o **Personal**, y también la dirección o el usuario si el nombre no lo indica ya. Si hay dos fuentes del mismo tipo con el mismo nombre, también se muestra cómo distinguirlas, como Slack o X, o la dirección del espacio de trabajo.

Cada fuente también indica en una línea qué incorpora y, si puede realizar acciones, que solo las realiza cuando pulsas **Enviar** o le das el visto bueno.

## Añadir una conexión

Abre un tipo (**Correo**, **Calendario**, **Chat**, **Reuniones**, **Documentos y archivos**, **Clientes**, **Proyectos y código**, **Otras**) y elige una fuente en **Añadir otro**, o debajo de la lista si aún no hay ninguna conectada. Al final aparecen las opciones genéricas: **Otro correo** en Correo, y **Enlace de calendario (ICS)** y **Otro calendario** en Calendario. Exchange Server lee las reuniones, así que aparece en Calendario.

**Sugerido para ti** aparece en la parte superior de **Conexiones** cuando tu Machine detecta un motivo para sugerirte una fuente. El motivo se indica en una línea: correo de Stripe, reuniones de Zoom en tu calendario, mensajes con enlaces a Google Docs o una configuración que no se completó. La fuente también permanece en su propio grupo, marcada como **Sugerido**. Estas sugerencias se calculan en tu Machine; nada sale de ella. Las fuentes conectadas nunca aparecen como sugerencias.

Microsoft Teams aparece dos veces: en **Chat**, para sus chats, y en **Reuniones** como **Reuniones de Teams**, para las notas de sus reuniones. Ambas opciones usan el mismo inicio de sesión de Microsoft, así que al conectar una también se conecta la otra.

La lista indica si ya conectaste una fuente y muestra su cuenta. Selecciónala para añadir otra junto a ella: el formulario lo indica y enlaza con la que ya tienes.

Completa los datos que te pida, como una clave o una dirección, elige **Trabajo** con el nombre de tu empresa o **Personal** y pulsa **Conectar**. En el caso del correo y los calendarios, solo se te pregunta si la dirección no lo indica. Si un sitio como LinkedIn o X abre la página de inicio de sesión en el navegador de tu Machine, el proceso continúa automáticamente cuando inicias sesión. GitHub, WhatsApp y Codex muestran un código que debes introducir. Los chats de Telegram muestran un código QR que debes escanear.

**Cancelar** detiene la conexión. ¿Te fuiste antes de terminar? Vuelve a abrir **Conexiones** desde cualquier dispositivo y retomarás el proceso en el mismo paso. Cuando se conecta, tu Machine empieza a leer la fuente de inmediato y muestra cómo avanza la primera sincronización.

En una Machine alojada, puedes iniciar sesión en Google, Microsoft, Microsoft OneDrive, Zoom, Stripe e Intercom aquí mismo: elige **Trabajo** o **Personal** y pulsa **Iniciar sesión**. Volverás a este formulario, donde verás cómo ha ido. GitHub, WhatsApp, Codex, los chats de Telegram y tu teléfono Android también muestran aquí sus códigos.

**Reconectar**, tanto en una fuente como en **Te necesita**, abre el mismo formulario. En tu propio ordenador, `assistant connect` hace lo mismo desde una terminal.

## Trabajo o personal

Cada fuente se clasifica como de trabajo, para una empresa que indiques, o personal. Puedes cambiarlo en **Detalles**. «Inferido» significa que tu Machine lo dedujo a partir de la dirección. Las tareas de trabajo esperan a tus días laborables.

El correo y los calendarios de Google y Microsoft se clasifican según la dirección cuando está claro: un proveedor de correo como Gmail o Outlook.com significa Personal, y el dominio de tu equipo significa Trabajo. Si no está claro, se te pregunta una vez justo después de iniciar sesión. **Cambiar** te permite elegirlo. Si más adelante el correo indica lo contrario, la tarea **Saca más partido a The Machine** te preguntará una vez si quieres cambiarlo.

## Funciones

Una fuente puede incorporar señales, que se convierten en tareas, realizar acciones para tus tareas, como leer un documento, enviar algo, responder o hacer un cambio después de que des el visto bueno, o ambas cosas. Si puede hacer ambas, **Detalles** incluye un interruptor para cada función: **Trae señales** y **Puede hacer cosas**. Una de las dos debe permanecer activada. Para desactivar ambas, desconecta la fuente. Los chats solo tienen **Puede hacer cosas**.

Si desactivas **Trae señales**, la fuente no se sincroniza. Si desactivas **Puede hacer cosas**, tu Machine nunca lee, redacta ni cambia nada usando esa fuente.

## Quitar una fuente

Abre la fuente, selecciona **Detalles** y luego **Desconectar**. Tu Machine dejará de leerla, pero conservará lo que ya había incorporado. En una Machine alojada, Google, Microsoft, Microsoft OneDrive, Zoom y Stripe muestran **Desconectar ↗**, que abre tu página de configuración.

**Desconectado hace poco** muestra las cuentas de Google, Microsoft, Zoom, Slack, Stripe y Salesforce que quitaste en los últimos 30 días, y cuándo las quitaste. Cada cuenta de Google aparece una sola vez, incluso si Google Meet o Docs tenían su propio inicio de sesión. Cada cuenta aparece en su propio tipo: las cuentas de Google o Microsoft en **Correo**, y las de Slack en **Chat**.

## Inicios de sesión guardados

En sitios como LinkedIn o X, marca **Guardar para la próxima vez** cuando inicies sesión. Después, **Inicios de sesión** mostrará esas cuentas. Si un sitio cierra la sesión de tu Machine, podrás volver a iniciarla con un toque. Las contraseñas permanecen cifradas en tu Machine. **Olvidar** elimina una cuenta.

## Revisiones

**Revisiones** muestra cómo lee tu Machine lo que llega: las revisiones recientes y lo que encontró cada una. Consulta [No hay tareas nuevas](reviews-paused.md).

Cada conexión tiene su propio artículo en esta sección, con detalles de lo que lee y de lo que puede enviar.
