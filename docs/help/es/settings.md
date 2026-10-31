---
title: Ajustes
area: settings
summary: Dónde encontrar cada ajuste, del modo claro a la seguridad y tu cuenta.
covers: settings:general
code: dashboard.html
order: 1
---
Abre **Ajustes** con el engranaje de arriba. Sus pestañas:

- **Cuenta**: **Tus direcciones**, las que cuentan como tú, con de dónde salió cada una. Tu plan en resumen, botones a las páginas de tu cuenta y **Cerrar sesión**. Consulta [Planes y facturación](plans-and-billing.md).
- **General**: idioma y región, este dispositivo, el navegador de tu Machine, tu Fleet y tu cuenta.
- **Seguridad**: Estándar o Prudente, y los ajustes que fijan. Consulta [Niveles de seguridad](security-levels.md). También **Acceso de soporte**, mientras está activo: consulta [Obtener ayuda](get-support.md#support-access).
- **Actividad**: todo lo que The Machine hizo por ti, lo más reciente primero. Consulta [Actividad](activity.md).
- **Notificaciones**: qué te llega y por dónde, y tu horario laboral. Consulta [Notificaciones](notifications.md) y [Horario laboral](work-hours.md).
- **Redacción**: firmas y cómo escribes. Consulta [Redacción](writing.md).
- **Habilidades**: guías que sigue tu Machine. Consulta [Habilidades](skills.md).
- **Modelo**: qué responde por ti, y sus límites. Consulta [Modelo](model.md). También **Codex y Claude Code**: consulta [Pasar a Claude Code o Codex](hand-to-agent.md).

Una pestaña sin nada que mostrar se oculta.

## General

- **Idioma y región**: tu **Región** fija cómo se leen las fechas (Oct 24 o 24 oct) y el reloj habitual. **Formato de hora** elige en su lugar 12 horas (2:05 PM) o 24 horas (14:05). Las tareas, Telegram, el resumen y los mensajes del Fleet lo siguen. Una Machine alojada parte del país de la zona horaria que elegiste al registrarte. Las horas como "hace 3 horas" y los números también lo siguen.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano o Português (Brasil). La primera vez que abres el panel elige el idioma de tu navegador, si es uno de estos (el portugués de Portugal recibe por ahora portugués de Brasil). El panel, las fechas, los mensajes de Telegram, las notificaciones, el resumen semanal y las notas y títulos de tareas que tu Machine escribe por ti lo siguen desde el momento en que lo eliges; lo que ya estaba escrito se queda como estaba. Las preguntas del Fleet y de la Family se leen en el idioma de cada compañero. Los borradores para otras personas se quedan en el idioma de su conversación. Ayuda y sus páginas también lo siguen.
- **Este dispositivo**: la app (**Instalar app**), **Notificaciones** con **Enviar una prueba**, y **Modo claro**, solo para este navegador o teléfono. Consulta [Instala la app y activa las notificaciones](phone-app.md).
- **Abrir el navegador de la Machine ↗**: el navegador que usa tu Machine para sitios como LinkedIn.
- **Reglas de Fleet**: consulta [Reglas para compartir](sharing-rules.md).
- **Cuenta**: **Abrir cuenta** y **Cerrar sesión**, en una Machine alojada.

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
