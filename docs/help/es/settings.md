---
title: Ajustes
area: settings
summary: Dónde encontrar cada ajuste, desde el modo claro hasta la seguridad y tu cuenta.
covers: settings:general
code: dashboard.html
order: 1
translated: 31820c6221312d35
---
Abre **Ajustes** con el icono del engranaje de la parte superior. Estas son sus pestañas:

- **Cuenta**: **Tus direcciones** (las que cuentan como tuyas) y **Cerrar sesión**, en la parte superior. Si tienes una Machine alojada, también aparecen tu plan, las facturas, Fleet, tus amigos, el inicio de sesión y tus datos, con **Cancelar plan** y **Eliminar la cuenta** al final. Si tienes una Machine en tu propio ordenador, vinculada a Network, aparecen tu Fleet, nombre de usuario, amigos e inicio de sesión, cada uno con un enlace que abre esa parte de tu cuenta (inicia sesión allí), y **Eliminar la cuenta** al final. Si aún no está vinculada: **Unirse a la Network**, en la parte superior. Consulta [Planes y facturación](plans-and-billing.md).
- **General**: idioma y región, este dispositivo, entrada de voz, el navegador de tu Machine, tu Fleet, exportación e importación, y la versión que usa. Si no hay pestaña Cuenta, **Unirse a la Network** aparece al final.
- **Seguridad**: Estándar o Cuidadoso. Consulta [Niveles de seguridad](security-levels.md). También aparece **Acceso de soporte** mientras esté activado: consulta [Contactar con soporte](get-support.md#support-access).
- **Actividad**: todo lo que The Machine ha hecho por ti, empezando por lo más reciente. Consulta [Actividad](activity.md).
- **Notificaciones**: qué recibes y dónde, y tu horario laboral. Consulta [Notificaciones](notifications.md) y [Horario laboral](work-hours.md).
- **Redacción**: firmas y tu forma de escribir. Consulta [Redacción](writing.md).
- **Habilidades**: instrucciones que sigue tu Machine. Consulta [Habilidades](skills.md).
- **Apps**: las apps de The Machine para tu móvil y ordenador; después, Claude, ChatGPT y otras IA que hayas conectado, y lo que puede hacer cada una. Consulta [La app móvil](mobile-app.md) y [Conectar otras IA](ai-connections.md).
- **Modelo**: la IA que lee y redacta por ti, y sus límites. Consulta [Modelo](model.md). También **Codex y Claude Code**: consulta [Pasar tareas a Claude Code o Codex](hand-to-agent.md). Y **Búsqueda por significado**, más abajo.

Las pestañas sin contenido se ocultan.

## General

- **Idioma y región**: la **Región** determina cómo se muestran las fechas, horas y números (24 oct o 24 oct). **Formato de hora** permite elegir entre el formato de 12 horas (2:05 PM) y el de 24 horas (14:05). Las tareas, Telegram, el resumen y los mensajes de Fleet siguen estos dos ajustes. En una Machine alojada, se usa inicialmente la zona horaria que elegiste al registrarte.
- **Idioma**: inglés, neerlandés, francés, alemán, español, italiano, portugués (Brasil), chino simplificado, japonés, coreano o ruso. Se elige inicialmente según el idioma de tu navegador. El panel, la ayuda, las notificaciones, Telegram, el resumen semanal y las tareas que redacta tu Machine cambian al idioma elegido en cuanto lo seleccionas. El texto anterior no cambia. Tus compañeros reciben las preguntas de Fleet y Family en su propio idioma, y los borradores para otras personas siguen en el idioma de la conversación.
- **Este dispositivo**: **Instalar app**, **Notificaciones** con **Enviar una prueba** y **Modo claro**, solo para este navegador o móvil. Consulta [Instala la app y activa las notificaciones](phone-app.md). Si usas [Omarchy](omarchy.md), también aparece **Tema de Omarchy**.
- **Entrada de voz**: cómo se convierte lo que dices en texto y qué voz usa Talk live. Consulta [Entrada de voz](voice-input.md) y [Habla en vivo](talk-live.md).
- **Abrir el navegador de la Machine ↗**: el navegador que usa tu Machine para sitios como LinkedIn.
- **Reglas de Fleet**: consulta [Reglas para compartir](sharing-rules.md).
- **Exportar**:
  - **Todo**: todo lo que sabe tu Machine, en un único archivo cifrado para trasladarlo o guardarlo, y **Importar** para cargar un archivo. Consulta [Pasar a otro ordenador](moving.md).
  - **Conocimiento para otra IA**: lo que ha aprendido tu Machine, en archivos que puede leer cualquier IA. Consulta [Conocimiento para otra IA](knowledge-export.md).

## Versión

La versión que usa tu Machine. Las actualizaciones se instalan automáticamente. Cuando hay una versión nueva disponible en una Machine alojada, **Actualizar ahora** la instala de inmediato. El proceso tarda unos minutos y tus datos se conservan.

En tu propio ordenador, un temporizador diario instala cada nueva versión firmada en Linux. Consulta [Ejecútala en tu propio ordenador](self-hosted-setup.md).

## Búsqueda por significado

En **Ajustes**, **Modelo**. Busca correos, mensajes y notas por su tema, no solo por las palabras que contienen. En una Machine alojada, lo hace una IA pequeña que se ejecuta en la propia Machine, sin enviar nada a ninguna parte. Está activada a partir de 8 GB de memoria. Con 4 GB, puedes activarla con el interruptor. Usa alrededor de medio gigabyte, así que puede ralentizar una Machine con mucha actividad. Si está desactivada, al preparar una tarea se siguen buscando mensajes relacionados por palabras.

En tu propio ordenador, está en el bloque `embeddings` de `config.json`. Reinicia la Machine después de cambiarlo.

## En esta Machine

Cuando tu Machine está en tu propio ordenador, algunas acciones se realizan allí, en un terminal:

- El archivo de ajustes, `config.json`: todos los ajustes en un solo lugar. Reinicia la Machine después de cambiarlo.
- `assistant connect`: añade una fuente, como `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` o `off`: mensajes de Telegram. Consulta [Telegram](telegram.md).
- `assistant doctor`: lo comprueba todo y muestra una solución para cada problema.

## Tus direcciones

Todas las direcciones tuyas que ha encontrado The Machine: las de tus cuentas, tus alias de Gmail u Outlook, tu calendario y tus perfiles de Slack e Intercom. Los correos y las reuniones de cualquiera de ellas cuentan como tuyos. **Quitar** las que no sean tuyas.

Una dirección compartida, como info@ o un grupo de Google, nunca cuenta por sí sola. Si The Machine no está segura de una dirección, la encontrarás en **Quizá tuyas**. Elige una opción:

- **Mía: solo yo la respondo**: cuenta como tuya. Los correos que recibas en ella pueden convertirse en tareas.
- **Del equipo: otros también la responden**: no cuenta como tuya. Los correos enviados solo a esa dirección no generan tareas ni borradores para ti. Aun así, completan el Graph.
- **No es mía**: no contará como tuya.

Elige según quién responda hoy. Una bandeja del equipo, como support@, es del equipo. Una como partnerships@, si solo la respondes tú, es tuya. Cámbiala cuando también empiecen a responder otras personas.

**Cambiar** en la fila de una dirección te permite modificarlo más adelante. Tu propia dirección de inicio de sesión siempre es tuya.

### Los dominios de tu empresa

Los dominios de tus propias direcciones cuentan como dominios de tu empresa. ¿También usas otro, como acme.co además de acme.com? Escríbelo en **Los dominios de tu empresa** y pulsa **Añadir**.

A partir de entonces, las personas de esos dominios se consideran compañeros, nunca clientes: sus conversaciones no aparecen en Graph del equipo y no se crea ninguna organización para ellas. **Quitar** elimina el dominio. No se pueden añadir dominios de correo gratuitos, como gmail.com.

Un alias tuyo de Gmail también puede aparecer como **De** en un borrador, si Gmail confirma que puedes enviar mensajes desde esa dirección. Consulta [Gmail](gmail.md#what-it-can-send).
