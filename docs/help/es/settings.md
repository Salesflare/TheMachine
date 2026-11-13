---
title: Ajustes
area: settings
summary: Dónde encontrar cada ajuste, del modo claro a la seguridad y tu cuenta.
covers: settings:general
code: dashboard.html
order: 1
---
Abre **Ajustes** con el engranaje de arriba. Sus pestañas:

- **Cuenta**: **Tus direcciones**, las que cuentan como tú, con de dónde salió cada una, y **Cerrar sesión**. En una Machine alojada, también tu plan, facturas, Machine, Fleet, dirección, amigos, inicio de sesión y datos, cada uno con su botón. Consulta [Planes y facturación](plans-and-billing.md). **Cerrar sesión** está arriba, **Cancelar plan** y **Eliminar la cuenta** al final del todo. En una Machine en tu propio ordenador, vinculada al Network: tu Fleet, usuario, amigos e inicio de sesión, cada uno con un enlace que abre esa parte de tu cuenta (inicia sesión allí), y **Eliminar la cuenta** al final. Aún sin vincular: **Unirte a la Network**, arriba.
- **General**: idioma y región, entrada de voz, este dispositivo, el navegador de tu Machine, tu Fleet, exportar e importar, y la versión que ejecuta. Sin la pestaña Cuenta, **Unirte a la Network** está al final.
- **Seguridad**: Estándar o Prudente, y los ajustes que fijan. Consulta [Niveles de seguridad](security-levels.md). También **Acceso de soporte**, mientras está activo: consulta [Obtener ayuda](get-support.md#support-access).
- **Actividad**: todo lo que The Machine hizo por ti, lo más reciente primero. Consulta [Actividad](activity.md).
- **Notificaciones**: qué te llega y por dónde, y tu horario laboral. Consulta [Notificaciones](notifications.md) y [Horario laboral](work-hours.md).
- **Redacción**: firmas y cómo escribes. Consulta [Redacción](writing.md).
- **Habilidades**: guías que sigue tu Machine. Consulta [Habilidades](skills.md).
- **Apps**: las apps de The Machine para el móvil y el ordenador, y después Claude, ChatGPT y otras IA que conectaste, y lo que puede hacer cada una. Consulta [La app móvil](mobile-app.md) y [Conectar otras IA](ai-connections.md).
- **Modelo**: qué responde por ti, y sus límites. Consulta [Modelo](model.md). También **Codex y Claude Code**: consulta [Pasar a Claude Code o Codex](hand-to-agent.md). Y **Búsqueda por significado**, más abajo.

Una pestaña sin nada que mostrar se oculta.

## General

- **Idioma y región**: tu **Región** fija cómo se leen las fechas (Oct 24 o 24 oct) y el reloj habitual. **Formato de hora** elige en su lugar 12 horas (2:05 PM) o 24 horas (14:05). Las tareas, Telegram, el resumen y los mensajes del Fleet lo siguen. Una Machine alojada parte del país de la zona horaria que elegiste al registrarte. Las horas como "hace 3 horas" y los números también lo siguen.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano o Português (Brasil). La primera vez que abres el panel elige el idioma de tu navegador, si es uno de estos (el portugués de Portugal recibe por ahora portugués de Brasil). El panel, las fechas, los mensajes de Telegram, las notificaciones, el resumen semanal y las notas y títulos de tareas que tu Machine escribe por ti lo siguen desde el momento en que lo eliges; lo que ya estaba escrito se queda como estaba. Las preguntas del Fleet y de la Family se leen en el idioma de cada compañero. Los borradores para otras personas se quedan en el idioma de su conversación. Ayuda y sus páginas también lo siguen.
- **Este dispositivo**: la app (**Instalar app**), **Notificaciones** con **Enviar una prueba**, y **Modo claro**, solo para este navegador o teléfono. Consulta [Instala la app y activa las notificaciones](phone-app.md).
- **Entrada de voz**: cómo lo que dices se convierte en texto, y la voz de Hablar en vivo. Consulta [Entrada de voz](voice-input.md) y [Hablar en vivo](talk-live.md).
- **Abrir el navegador de la Machine ↗**: el navegador que usa tu Machine para sitios como LinkedIn.
- **Reglas de Fleet**: consulta [Reglas para compartir](sharing-rules.md).
- **Exportar**:
  - **Todo**: todo lo que sabe tu Machine en un solo archivo cifrado, para mudarte o guardarlo, e **Importar** para traer uno. Consulta [Pásate a otro ordenador](moving.md).
  - **Conocimiento para otra IA**: lo que tu Machine ha aprendido, en archivos que cualquier IA puede leer. Consulta [Conocimiento para otra IA](knowledge-export.md).

## Versión

La versión que ejecuta tu Machine. Las actualizaciones se instalan solas. Cuando hay una versión más reciente en una Machine alojada, **Actualizar ahora** la instala al momento. Tarda unos minutos, y tus datos se quedan.

En tu propio ordenador, un temporizador diario instala cada nueva versión firmada en Linux. Consulta [Ejecútala en tu propio ordenador](self-hosted-setup.md).

## Búsqueda por significado

En **Ajustes**, **Modelo**. Encuentra correos, mensajes y notas según de qué tratan, no solo por sus palabras. En una Machine alojada lo hace una pequeña IA en la propia Machine, y no se envía nada a ningún sitio. Está activada a partir de 8 GB de memoria. Con 4 GB, actívala con su interruptor. Usa aproximadamente medio gigabyte, así que una Machine ocupada puede ir más lenta.

En tu propio ordenador, es el bloque `embeddings` de `config.json`. Reinicia la Machine después de un cambio.

## En esta Machine

Algunos ajustes están en el ordenador donde funciona tu Machine, no en la app:

- `config.json`: todos los ajustes, en un archivo. Reinicia la Machine después de un cambio.
- `assistant connect`: añade una fuente, como `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` u `off`: mensajes por Telegram. Consulta [Telegram](telegram.md).
- `assistant doctor`: lo revisa todo y muestra una solución para cada problema.

## Tus direcciones

Cada dirección tuya que encontró la Machine: tus cuentas, alias de Gmail u Outlook, tu calendario, tu perfil de Slack e Intercom. El correo y las reuniones de cualquiera de ellas aparecen como tuyos. **Quitar** una que no sea tuya.

Una dirección compartida, como info@ o un Google Group, nunca cuenta por sí sola. Una de la que la Machine no está segura aparece en **Quizá tuyas**, y no se elige nada por ti. Elige una opción:

- **Mía: solo yo la respondo**: cuenta como tuya. El correo que le llega puede convertirse en tus tareas.
- **Del equipo: otros también la responden**: no eres tú. El correo que solo fue a esa dirección no crea tareas ni borradores para ti. Sigue alimentando el Graph, compartido con tu equipo como antes.
- **No es mía**: no contará como tuya.

Elige según quién la responde hoy. Una bandeja del equipo como support@ es del equipo. Una como partnerships@ que ahora solo respondes tú es tuya; pásala al equipo cuando otros también la respondan.

**Cambiar** en su fila lo cambia más adelante. Tu propia dirección de inicio de sesión siempre es tuya.

### Los dominios de tu empresa

Los dominios de tus propias direcciones cuentan como los de tu empresa. Si usa otro, como acme.co junto a acme.com, escríbelo en **Los dominios de tu empresa** y pulsa **Añadir**.

Quienes están ahí pasan a ser tus colegas, nunca clientes: sus hilos quedan fuera del Team Graph como cualquier hilo solo entre colegas, y no se crea una organización. **Quitar** lo saca de nuevo. Un dominio de correo gratuito como gmail.com no se puede añadir.
