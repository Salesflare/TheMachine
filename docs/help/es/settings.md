---
title: Ajustes
area: settings
summary: Dónde encontrar cada ajuste, desde el modo claro hasta la seguridad y tu cuenta.
covers: settings:general
code: dashboard.html
order: 1
translated: 012a9e1fdd9e1752
---
Abre **Ajustes** con el icono de engranaje de la parte superior. Estas son sus pestañas:

- **Cuenta**: **Tus direcciones** (las que cuentan como tuyas) y **Cerrar sesión**, en la parte superior. Si tienes una Machine alojada, también encontrarás tu plan, las facturas, Fleet, tus amistades, el inicio de sesión y tus datos, además de **Cancelar plan** y **Eliminar la cuenta** al final. Si tienes una Machine en tu propio ordenador conectada a la Network, encontrarás tu Fleet, nombre de usuario, amistades e inicio de sesión, cada uno con un enlace que abre esa parte de tu cuenta (inicia sesión allí), y **Eliminar la cuenta** al final. Si aún no está conectada, verás **Unirse a la Network** en la parte superior. Consulta [Planes y facturación](plans-and-billing.md).
- **General**: idioma y región, este dispositivo, entrada de voz, el navegador de tu Machine, tu Fleet, exportación e importación, y la versión que tiene instalada. Si no aparece la pestaña Cuenta, **Unirse a la Network** está al final.
- **Seguridad**: Estándar o Precavida. Consulta [Niveles de seguridad](security-levels.md). También encontrarás **Acceso de soporte** mientras esté activado: consulta [Contactar con soporte](get-support.md#support-access).
- **Actividad**: todo lo que The Machine ha hecho por ti, empezando por lo más reciente. Consulta [Actividad](activity.md).
- **Notificaciones**: qué notificaciones recibes y dónde, y tu horario laboral. Consulta [Notificaciones](notifications.md) y [Horario laboral](work-hours.md).
- **Redacción**: firmas y tu forma de escribir. Consulta [Redacción](writing.md).
- **Habilidades**: instrucciones que sigue tu Machine. Consulta [Habilidades](skills.md).
- **Apps**: las apps de The Machine para tu móvil y ordenador, y después Claude, ChatGPT y otras IA que hayas conectado, además de lo que puede hacer cada una. En un ordenador, aparecen las apps de escritorio para Windows, Mac y Linux, con **Descargar** para cada una, y se indica cuál es la de **Este equipo**. Consulta [La app móvil](mobile-app.md), [La app de escritorio](desktop-app.md) y [Conecta otras IA](ai-connections.md).
- **Modelo**: la IA que lee y redacta por ti, y sus límites. Consulta [Modelo](model.md). También encontrarás **Codex y Claude Code**: consulta [Pasar tareas a Claude Code o Codex](hand-to-agent.md). Y **Búsqueda por significado**, más abajo.

Las pestañas que no tienen nada que mostrar están ocultas.

## General

- **Idioma y región**: la **Región** determina cómo se muestran las fechas, horas y números (24 oct o 24 de oct.). En **Formato de hora** puedes elegir entre 12 horas (2:05 p. m.) y 24 horas (14:05). Las tareas, Telegram, el resumen y los mensajes de Fleet siguen estos dos ajustes. En una Machine alojada se usa la zona horaria que elegiste al registrarte.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 o Русский. Se elige inicialmente según el idioma de tu navegador. El panel, la Ayuda, las notificaciones, Telegram, el resumen semanal y las tareas que redacta tu Machine cambian al idioma que elijas. Los textos anteriores se quedan como estaban. Tus compañeros reciben las preguntas de Fleet y Family en su propio idioma, y los borradores para otras personas se mantienen en el idioma de la conversación.
- **Este dispositivo**: **Instalar app**, **Notificaciones**, con **Enviar una prueba**, y **Modo claro**, solo para este navegador o móvil. Consulta [Instala la app y activa las notificaciones](phone-app.md). En [Omarchy](omarchy.md), también encontrarás **Tema de Omarchy**.
- **Entrada de voz**: cómo se convierte en texto lo que dices y qué voz se usa en Habla en directo. Consulta [Entrada de voz](voice-input.md) y [Hablar en vivo](talk-live.md).
- **Abrir el navegador de la Machine ↗**: el navegador que usa tu Machine para sitios como LinkedIn.
- **Reglas de Fleet**: consulta [Reglas para compartir](sharing-rules.md).
- **Exportar**:
  - **Todo**: todo lo que sabe tu Machine, en un único archivo cifrado para trasladarlo o guardarlo, e **Importar** para cargar un archivo. Consulta [Pasar a otro ordenador](moving.md).
  - **Conocimiento para otra IA**: lo que ha aprendido tu Machine, en archivos que puede leer cualquier IA. Consulta [Conocimiento para otra IA](knowledge-export.md).

## Versión

La versión que tiene tu Machine. Las actualizaciones se instalan automáticamente. Cuando hay una versión nueva disponible en una Machine alojada, **Actualizar ahora** la instala de inmediato. Tarda unos minutos y tus datos se conservan.

En tu propio ordenador, un temporizador diario instala cada nueva versión firmada en Linux. Consulta [Ejecútala en tu propio ordenador](self-hosted-setup.md).

## Búsqueda por significado

En **Ajustes**, **Modelo**. Encuentra correos, mensajes y notas por su tema, no solo por las palabras que contienen. En una Machine alojada, una IA pequeña lo hace en la propia Machine y no se envía nada a ningún sitio. Está activada a partir de 8 GB de memoria. Si tienes 4 GB, actívala con el interruptor. Usa alrededor de medio gigabyte, así que puede ralentizar una Machine con mucha actividad. Si está desactivada, la preparación de una tarea sigue buscando mensajes relacionados por sus palabras.

En tu propio ordenador, es el bloque `embeddings` de `config.json`. Reinicia la Machine después de cambiarlo.

## En esta Machine

Cuando tu Machine funciona en tu propio ordenador, algunas tareas se hacen allí, desde un terminal:

- El archivo de ajustes, `config.json`: todos los ajustes en un solo lugar. Reinicia la Machine después de cambiarlo.
- `assistant connect`: añade una fuente, como `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` o `off`: mensajes en Telegram. Consulta [Telegram](telegram.md).
- `assistant doctor`: lo comprueba todo e indica cómo solucionar cada problema.

## Tus direcciones

Todas las direcciones tuyas que ha encontrado la Machine: tus cuentas, alias de Gmail u Outlook, tu calendario y tus perfiles de Slack e Intercom. Los correos y las reuniones de cualquiera de ellas cuentan como tuyos. **Quitar** una que no sea tuya.

Una dirección compartida, como info@ o un grupo de Google, nunca cuenta por sí sola. Las direcciones sobre las que la Machine no está segura aparecen en **Quizá tuyas**. Elige una opción:

- **Mía: solo yo la respondo**: cuenta como tuya. Los correos que recibas en ella pueden convertirse en tus tareas.
- **Del equipo: otros también la responden**: no cuenta como tuya. Los correos enviados solo a esa dirección no crearán tareas ni borradores para ti. Aun así, se incluyen en Graph.
- **No es mía**: no contará como tuya.

Elige según quién responda a esa dirección hoy. Una bandeja de entrada del equipo, como support@, pertenece al equipo. Una como partnerships@, a la que solo respondes tú, es tuya. Cámbiala cuando otras personas también empiecen a responder.

Pulsa **Cambiar** en la fila para modificar la opción más adelante. Tu propia dirección de inicio de sesión siempre es tuya.

### Los dominios de tu empresa

Los dominios de tus direcciones cuentan como dominios de tu empresa. ¿Usas también otro, como acme.co además de acme.com? Escríbelo en **Los dominios de tu empresa** y pulsa **Añadir**.

Las personas que tengan esas direcciones se considerarán compañeros, nunca clientes: sus conversaciones no aparecerán en Graph del equipo y no se creará ninguna organización para ellas. **Quitar** elimina el dominio. No se pueden añadir dominios de correo gratuitos como gmail.com.

Un alias de Gmail tuyo también puede aparecer como **De** en un borrador, si Gmail confirma que puedes enviar mensajes desde esa dirección. Consulta [Gmail](gmail.md#what-it-can-send).
