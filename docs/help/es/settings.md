---
title: Ajustes
area: settings
summary: Dónde encontrar cada ajuste, desde el modo claro hasta la seguridad y tu cuenta.
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
Abre **Ajustes** con el engranaje de arriba. Estas son sus pestañas:

- **Cuenta**: **Tus direcciones** (las que cuentan como tuyas) y **Cerrar sesión**, arriba. Si usas una Machine alojada, también encontrarás tu plan, las facturas, Fleet, amigos, inicio de sesión y datos, además de **Cancelar plan** y **Eliminar la cuenta** al final. Si usas una Machine en tu propio ordenador vinculada a Network, encontrarás Fleet, tu nombre de usuario, amigos e inicio de sesión, cada uno con un enlace a esa sección de tu cuenta (inicia sesión allí), y **Eliminar la cuenta** al final. Si aún no está vinculada: **Unirse a la Network**, arriba. Consulta [Planes y facturación](plans-and-billing.md).
- **General**: idioma y región, este dispositivo, entrada de voz, el navegador de tu Machine, Fleet, exportación e importación y la versión que ejecuta. Si no hay pestaña Cuenta, **Unirse a la Network** aparece al final.
- **Seguridad**: Estándar o Prudente. Consulta [Niveles de seguridad](security-levels.md). También encontrarás **Acceso de soporte** mientras esté activado. Consulta [Contactar con soporte](get-support.md#support-access).
- **Actividad**: todo lo que The Machine ha hecho por ti, empezando por lo más reciente. Consulta [Actividad](activity.md).
- **Notificaciones**: qué recibes y dónde, y tu horario laboral. Consulta [Notificaciones](notifications.md) y [Horario laboral](work-hours.md).
- **Redacción**: firmas y tu forma de escribir. Consulta [Redacción](writing.md).
- **Habilidades**: guías que sigue tu Machine. Consulta [Habilidades](skills.md).
- **Apps**: las apps de The Machine para tu teléfono y ordenador, y luego Claude, ChatGPT y otras IA que hayas conectado, además de lo que puede hacer cada una. Consulta [La app móvil](mobile-app.md) y [Conectar otras IA](ai-connections.md).
- **Modelo**: la IA que lee y redacta por ti, y sus límites. Consulta [Modelo](model.md). También encontrarás **Codex y Claude Code**. Consulta [Pasar tareas a Claude Code o Codex](hand-to-agent.md). Y **Búsqueda por significado**, más abajo.

Las pestañas que no tienen nada que mostrar están ocultas.

## General

- **Idioma y región**: la **Región** determina cómo se muestran las fechas, las horas y los números (oct 24 o 24 oct). **Formato de hora** permite elegir entre el formato de 12 horas (2:05 PM) y el de 24 horas (14:05). Las tareas, Telegram, el resumen y los mensajes de Fleet usan ambos ajustes. Una Machine alojada parte de la zona horaria que elegiste al registrarte.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 o Русский. Se usa el idioma de tu navegador de forma predeterminada. El panel, la ayuda, las notificaciones, Telegram, el resumen semanal y las tareas que redacta tu Machine cambian al idioma que elijas. Los textos anteriores no cambian. Tus compañeros reciben las preguntas de Fleet y Familia en su propio idioma, y los borradores para otras personas conservan el idioma de la conversación.
- **Este dispositivo**: **Instalar app**, **Notificaciones** con **Enviar una prueba** y **Modo claro**, solo para este navegador o teléfono. Consulta [Instala la app y activa las notificaciones](phone-app.md). Si usas [Omarchy](omarchy.md), también encontrarás **Tema de Omarchy**.
- **Entrada de voz**: cómo se convierte en texto lo que dices y qué voz usa Talk live. Consulta [Entrada de voz](voice-input.md) y [Habla en vivo](talk-live.md).
- **Abrir el navegador de la Machine ↗**: el navegador que tu Machine usa para sitios como LinkedIn.
- **Reglas de Fleet**: consulta [Reglas para compartir](sharing-rules.md).
- **Exportar**:
  - **Todo**: todo lo que sabe tu Machine en un archivo cifrado, para trasladarlo o guardarlo, y **Importar** para importar uno. Consulta [Pasar a otro ordenador](moving.md).
  - **Conocimiento para otra IA**: lo que ha aprendido tu Machine, en archivos que puede leer cualquier IA. Consulta [Conocimiento para otra IA](knowledge-export.md).

## Versión

La versión que ejecuta tu Machine. Las actualizaciones se instalan automáticamente. Si hay una versión nueva para una Machine alojada, **Actualizar ahora** la instala de inmediato. Tarda unos minutos y tus datos se conservan.

En tu propio ordenador, un temporizador diario instala cada nueva versión firmada en Linux. Consulta [Ejecútala en tu propio ordenador](self-hosted-setup.md).

## Búsqueda por significado

En **Ajustes**, **Modelo**. Encuentra correos, mensajes y notas según el tema, no solo por las palabras que contienen. En una Machine alojada, lo hace una pequeña IA en la propia Machine, sin enviar nada a ningún sitio. Está activada a partir de 8 GB de memoria. Si tienes 4 GB, puedes activarla con el interruptor. Usa cerca de medio gigabyte, así que una Machine con mucha actividad puede ir más lenta.

En tu propio ordenador, es el bloque `embeddings` de `config.json`. Reinicia la Machine después de cambiarlo.

## En esta Machine

Si tu Machine se ejecuta en tu propio ordenador, puedes hacer algunas cosas allí, desde un terminal:

- El archivo de ajustes, `config.json`: todos los ajustes en un solo lugar. Reinicia la Machine después de cambiarlo.
- `assistant connect`: añade una fuente, como `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` o `off`: mensajes en Telegram. Consulta [Telegram](telegram.md).
- `assistant doctor`: comprueba todo e imprime una solución para cada problema.

## Tus direcciones

Todas las direcciones tuyas que ha encontrado The Machine: tus cuentas, alias de Gmail o Outlook, tu calendario y tus perfiles de Slack e Intercom. Los correos y las reuniones de cualquiera de ellas cuentan como tuyos. **Quitar** elimina las que no sean tuyas.

Una dirección compartida, como info@ o un grupo de Google, nunca cuenta por sí sola. Las direcciones sobre las que The Machine tiene dudas aparecen en **Quizá tuyas**. Elige una:

- **Mía: solo yo la respondo**: cuenta como tuya. Los correos que recibas en ella pueden convertirse en tus tareas.
- **Del equipo: otros también la responden**: no cuenta como tuya. Los correos enviados solo a esa dirección no generan tareas ni borradores para ti. Aun así, completan el Graph.
- **No es mía**: no contará como tuya.

Elige según quién responda hoy. Un buzón de equipo como support@ es del equipo. Una dirección como partnerships@ que solo respondes tú es tuya. Cámbiala cuando también empiecen a responder otras personas.

**Cambiar** en la fila permite modificarlo más adelante. La dirección que usas para iniciar sesión siempre es tuya.

### Los dominios de tu empresa

Los dominios de tus direcciones cuentan como dominios de tu empresa. ¿También usas otro, como acme.co además de acme.com? Escríbelo en **Los dominios de tu empresa** y pulsa **Añadir**.

A partir de entonces, las personas de esos dominios serán compañeros, nunca clientes: sus conversaciones no aparecerán en el Graph del equipo y no se creará ninguna organización para ellas. **Quitar** elimina el dominio. No se pueden añadir dominios de correo gratuitos como gmail.com.

Un alias tuyo de Gmail también puede aparecer en el campo **De** de un borrador, si Gmail confirma que puedes enviar mensajes desde esa dirección. Consulta [Gmail](gmail.md#what-it-can-send).
