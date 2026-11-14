---
title: Conexiones
area: connections
summary: Todas tus fuentes en un solo lugar: consulta cómo va cada una, añade otra o desconecta una.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 60304f2504ee5676
---
## Cómo van

La pestaña **Conexiones** muestra tus fuentes por tipo, con **Inicios de sesión** y **Revisiones** debajo de una línea. En el móvil, toca un tipo para abrirlo y **Conexiones** para volver. Primero se abre el tipo que tenga una fuente que te necesite. Cada fuente aparece en una fila con su estado (Conectada, Esperando la primera sincronización, Reconectando automáticamente o Necesita tu ayuda) y lo que ha recibido últimamente. Tócala para ver su tarjeta y **Detalles**.

Si una sincronización falla, pero otra posterior lo soluciona, el fallo aparece en gris. Solo se muestra como problema el fallo más reciente, junto con la fecha del próximo intento.

Los recuentos muestran todo lo que ha recibido, incluido su [historial](history.md), lo que ha llegado en las últimas 24 horas y lo que aún no se ha revisado. En un calendario se cuentan los eventos.

Cada fuente lleva el nombre de su cuenta, tal como la identifica el servicio: tu dirección, un perfil de X, un espacio de trabajo de Slack o de quién es la cuenta de Signal o Telegram. Debajo del nombre aparece primero **Trabajo** o **Personal**, además de la dirección o el nombre de usuario si el nombre no lo indica ya. Si hay dos fuentes del mismo tipo con el mismo nombre, también se muestra cómo distinguirlas, por ejemplo, Slack o X, o la dirección del espacio de trabajo.

Cada fuente también indica en una línea qué aporta y, si puede realizar acciones, que solo las realiza cuando pulsas **Enviar** o las apruebas.

## Añadir una fuente

Abre un tipo (**Correo**, **Calendario**, **Chat**, **Reuniones**, **Documentos y archivos**, **Clientes**, **Proyectos y código**, **Otras**) y elige una fuente en **Añadir otro**, o debajo de la lista si aún no hay ninguna conectada. Al final aparecen las opciones para cualquier otro servicio: **Otro correo** en Correo, y **Enlace de calendario (ICS)** y **Otro calendario** en Calendario. Exchange Server lee las reuniones, así que aparece en Calendario.

**Sugerido para ti** aparece en la parte superior de **Conexiones** cuando tu Machine detecta un motivo para sugerirte una fuente. El motivo se explica en una línea: correos de Stripe, reuniones de Zoom en tu calendario, mensajes con enlaces a Google Docs o una configuración que no se completó. La fuente también permanece en su propio grupo, marcada como **Sugerido**. Tu Machine hace estos recuentos en ella; no se envía nada fuera. Nunca se sugiere una fuente conectada.

Microsoft Teams aparece dos veces: en **Chat**, para sus chats, y en **Reuniones**, como **Reuniones de Teams**, para las notas de sus reuniones. Ambas usan el mismo inicio de sesión de Microsoft, así que conectar una también conecta la otra.

En la lista, las fuentes que ya conectaste aparecen con su cuenta. Elígelas para añadir otra junto a ellas: el formulario lo indica y enlaza con la que ya tienes.

Completa los datos necesarios, como una clave o una dirección, elige **Trabajo** con el nombre de la empresa o **Personal** (Correo y Calendario solo te lo preguntan si la dirección no lo indica) y pulsa **Conectar**. En sitios como LinkedIn o X, se abre la página de inicio de sesión en el navegador de tu Machine y el proceso continúa automáticamente cuando inicias sesión. GitHub, WhatsApp y Codex muestran un código que debes introducir. Los chats de Telegram y Signal muestran un código QR que debes escanear.

**Cancelar** detiene el proceso. ¿Te fuiste antes de terminar? Vuelve a abrir **Conexiones** desde cualquier dispositivo y continuarás desde el mismo paso. Una vez conectada, tu Machine empieza a leer la fuente de inmediato y muestra el estado de la primera sincronización.

En una Machine alojada, las fuentes con inicio de sesión propio te permiten iniciar sesión desde aquí: Google, Microsoft (Outlook, OneDrive y Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce y Trello.

Elige **Trabajo** o **Personal** y pulsa el botón de inicio de sesión, como **Iniciar sesión con Google**. Volverás a este formulario, donde se mostrará el resultado. GitHub, WhatsApp, Codex, los chats de Telegram y tu teléfono Android también muestran aquí su código.

En tu propio equipo, puedes iniciar sesión en esas mismas fuentes cuando vincules tu Machine a tu cuenta: pulsa **Vincular esta Machine** la primera vez. Algunas también ofrecen otra opción, como usar tu propia aplicación o una clave.

**Reconectar**, tanto en una fuente como en **Te necesita**, abre el mismo formulario. En tu propio equipo, `assistant connect` hace lo mismo desde una terminal.

## Trabajo o personal

Cada fuente se considera de trabajo (para una empresa que indiques) o personal. Puedes cambiarlo en **Detalles**. **Adivinado** significa que tu Machine lo dedujo a partir de la dirección. Las tareas de trabajo esperan hasta tus días laborables.

En el caso del correo y los calendarios de Google y Microsoft, se determina según la dirección si está claro: un proveedor de correo como Gmail o Outlook.com se considera Personal; el dominio de tu equipo, Trabajo. Si no está claro, se te pregunta una vez justo después de iniciar sesión. **Cambiar** te permite elegirlo. Si más adelante el correo indica lo contrario, la tarea de **Saca más partido a The Machine** te preguntará una vez si quieres cambiarlo.

## Funciones

Una fuente puede traer señales (lo que recibe se convierte en tareas), realizar acciones para tus tareas (leer un documento, o enviar, responder o cambiar algo después de que lo apruebes), o ambas cosas. Si hace ambas, **Detalles** incluye un interruptor para cada función: **Trae señales** y **Puede hacer cosas**. Una debe permanecer activada. Para detener ambas, desconecta la fuente. Un chat solo tiene **Puede hacer cosas**.

Si desactivas **Trae señales**, la fuente no se sincroniza. Si desactivas **Puede hacer cosas**, tu Machine nunca leerá, redactará ni cambiará nada con ella.

## Eliminar una fuente

Abre la fuente y ve a **Detalles**. Después, pulsa **Desconectar**. Dejará de leerla, pero conservará lo que ya había recibido. En una Machine alojada, las fuentes cuyo inicio de sesión administra la página de configuración (Google, Microsoft, Google Meet, Slack, Zoom, Stripe y Salesforce) muestran **Desconectar ↗**, que abre esa página.

**Desconectado hace poco** muestra las cuentas de Google, Microsoft, Zoom, Slack, Stripe y Salesforce que desconectaste en los últimos 30 días y cuándo lo hiciste. Hasta que el servicio lo confirme, aparece como Pendiente y se sigue intentando. Una cuenta de Google aparece una sola vez, aunque Google Meet o Docs tuviera su propio inicio de sesión. Cada cuenta aparece en su tipo correspondiente: una cuenta de Google o Microsoft en **Correo** y una de Slack en **Chat**.

## Inicios de sesión guardados

En sitios como LinkedIn o X, marca **Guardar para la próxima vez** cuando inicies sesión. Después, **Inicios de sesión** muestra esas cuentas y, cuando un sitio cierra la sesión de tu Machine, puedes volver a iniciarla con un solo toque. Las contraseñas permanecen cifradas en tu Machine. **Olvidar** elimina una cuenta.

## Revisiones

**Revisiones** muestra cómo tu Machine lee lo que recibe: las revisiones recientes y lo que encontró cada una. Consulta [No hay tareas nuevas](reviews-paused.md).

Cada conexión tiene su propio artículo en esta sección, donde se explica qué lee y qué puede enviar.
