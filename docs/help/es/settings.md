---
title: Ajustes
area: settings
summary: Dónde encontrar cada ajuste, desde el modo claro hasta la seguridad y tu cuenta.
covers: settings:general
code: dashboard.html
order: 1
translated: 00e42f9aeb395d21
---
Abre **Ajustes** con el engranaje de la parte superior. Estas son sus pestañas:

- **Cuenta**: **Tus direcciones** (las que cuentan como tuyas) y **Cerrar sesión**, en la parte superior. En una Machine alojada, también encontrarás tu plan, las facturas, Fleet, amigos, inicio de sesión y datos, además de **Cancelar plan** y **Eliminar la cuenta** al final. En una Machine en tu propio ordenador, vinculada a la Network: Fleet, tu nombre de usuario, amigos e inicio de sesión, cada uno con un enlace que abre esa sección de tu cuenta (inicia sesión allí), y **Eliminar la cuenta** al final. Si aún no está vinculada: **Unirte a la Network**, en la parte superior. Consulta [Planes y facturación](plans-and-billing.md).
- **General**: idioma y región, este dispositivo, entrada de voz, el navegador de tu Machine, tu Fleet, exportación e importación, y la versión que usa.
- **Seguridad**: Estándar o Cuidadoso. Consulta [Niveles de seguridad](security-levels.md). También **Acceso de soporte**, mientras esté activado: consulta [Obtener ayuda](get-support.md#support-access).
- **Actividad**: todo lo que The Machine ha hecho por ti, de lo más reciente a lo más antiguo. Consulta [Actividad](activity.md).
- **Notificaciones**: qué recibes y dónde, y tu horario laboral. Consulta [Notificaciones](notifications.md) y [Horario laboral](work-hours.md).
- **Redacción**: firmas y tu forma de escribir. Consulta [Redacción](writing.md).
- **Habilidades**: guías que sigue tu Machine. Consulta [Habilidades](skills.md).
- **Apps**: las apps de The Machine para tu teléfono y ordenador; después, Claude, ChatGPT y otras IA que hayas conectado, y lo que puede hacer cada una. Consulta [La app móvil](mobile-app.md) y [Conectar otras IA](ai-connections.md).
- **Modelo**: la IA que lee y redacta por ti, y sus límites. Consulta [Modelo](model.md). También **Codex y Claude Code**: consulta [Delegar en Claude Code o Codex](hand-to-agent.md). Y **Búsqueda por significado**, más abajo.

Las pestañas sin contenido no aparecen.

## General

- **Idioma y región**: **Región** determina cómo se muestran las fechas, horas y números (24 oct o 24 oct). **Formato de hora** permite elegir entre el formato de 12 horas (2:05 PM) o el de 24 horas (14:05). Las tareas, Telegram, el resumen y los mensajes de Fleet usan ambas preferencias. Una Machine alojada parte de la zona horaria que elegiste al registrarte.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano o Português (Brasil). Se elige inicialmente según el idioma de tu navegador. El panel, la Ayuda, las notificaciones, Telegram, el resumen semanal y las tareas que redacta tu Machine cambian al idioma elegido. El texto anterior no cambia. Tus compañeros reciben las preguntas de Fleet y Family en su propio idioma, y los borradores para otras personas siguen en el idioma de la conversación.
- **Este dispositivo**: **Instalar app**, **Notificaciones** con **Enviar una prueba** y **Modo claro**, solo para este navegador o teléfono. Consulta [Instalar la app y activar las notificaciones](phone-app.md). En [Omarchy](omarchy.md), también está **Tema de Omarchy**.
- **Entrada de voz**: cómo se convierte en texto lo que dices y la voz de Hablar en directo. Consulta [Entrada de voz](voice-input.md) y [Hablar en directo](talk-live.md).
- **Abrir el navegador de la Machine ↗**: el navegador que usa tu Machine para sitios como LinkedIn.
- **Reglas de Fleet**: consulta [Reglas para compartir](sharing-rules.md).
- **Exportar**:
  - **Todo**: todo lo que sabe tu Machine en un solo archivo cifrado, para trasladarlo o guardarlo, e **Importar** para cargar un archivo. Consulta [Pasar a otro ordenador](moving.md).
  - **Conocimiento para otra IA**: lo que ha aprendido tu Machine, en archivos que cualquier IA puede leer. Consulta [Conocimiento para otra IA](knowledge-export.md).

## Versión

La versión que usa tu Machine. Las actualizaciones se instalan automáticamente. Cuando hay una versión nueva disponible en una Machine alojada, **Actualizar ahora** la instala de inmediato. Tarda unos minutos y tus datos se conservan.

En tu propio ordenador, un temporizador diario instala cada nueva versión firmada en Linux. Consulta [Ejecutar en tu propio ordenador](self-hosted-setup.md).

## Búsqueda por significado

En **Ajustes**, **Modelo**. Encuentra correos, mensajes y notas por su tema, no solo por las palabras que contienen. En una Machine alojada, lo hace una IA pequeña que funciona en la propia Machine, sin enviar nada a ningún sitio. Está activada a partir de 8 GB de memoria. Con 4 GB, actívala con el interruptor. Usa alrededor de medio gigabyte, así que una Machine con mucha actividad puede volverse más lenta.

En tu propio ordenador, es el bloque `embeddings` de `config.json`. Reinicia la Machine después de cambiarlo.

## En esta Machine

Cuando tu Machine funciona en tu propio ordenador, algunas tareas se hacen allí, en un terminal:

- El archivo de ajustes, `config.json`: todos los ajustes en un mismo sitio. Reinicia la Machine después de cambiarlo.
- `assistant connect`: añade una fuente, como `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` o `off`: mensajes en Telegram. Consulta [Telegram](telegram.md).
- `assistant doctor`: lo comprueba todo e imprime una solución para cada problema.

## Tus direcciones

Todas las direcciones tuyas que ha encontrado la Machine: tus cuentas, alias de Gmail o Outlook, tu calendario y tus perfiles de Slack e Intercom. El correo y las reuniones de cualquiera de ellas cuentan como tuyos. **Quitar** elimina las que no sean tuyas.

Una dirección compartida, como info@ o un Google Group, nunca cuenta por sí sola. Las direcciones sobre las que la Machine no está segura aparecen en **Quizá tuyas**. Elige una opción:

- **Mía: solo yo la respondo**: cuenta como tuya. Los correos que recibas ahí pueden convertirse en tareas.
- **Del equipo: otros también la responden**: no es tuya. Los correos que solo se envíen a esa dirección no crearán tareas ni borradores para ti. Aun así, se incluyen en Graph.
- **No es mía**: no contará como tuya.

Elige según quién responda hoy. Una bandeja de equipo como support@ pertenece al equipo. Una como partnerships@, que solo respondes tú, es tuya. Cámbiala si otras personas empiezan a responderla también.

**Cambiar** en la fila permite modificar la opción más adelante. Tu propia dirección de inicio de sesión siempre es tuya.

### Los dominios de tu empresa

Los dominios de tus propias direcciones cuentan como los de tu empresa. ¿También usas otro, como acme.co además de acme.com? Escríbelo en **Los dominios de tu empresa** y pulsa **Añadir**.

A partir de entonces, las personas de esos dominios son compañeros, nunca clientes: sus conversaciones no aparecen en Team Graph y no se crea ninguna organización para ellas. **Quitar** elimina el dominio. No se pueden añadir dominios de correo gratuitos como gmail.com.

Un alias tuyo de Gmail también puede aparecer como **De** en un borrador, si Gmail confirma que puedes enviar correo desde esa dirección. Consulta [Gmail](gmail.md#what-it-can-send).
