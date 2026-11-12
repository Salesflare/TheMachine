---
title: Microsoft Teams
area: connections
summary: Chats de Teams, chats de reuniones y notas de reuniones para una cuenta profesional o educativa. Solo lee.
covers: connector:teams
code: connectors/teams.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
---
## Qué lee

Tus chats individuales, de grupo y de reuniones en Teams: los últimos 7 días al conectarlo, y luego los mensajes nuevos cada pocos minutos. Cerca de un año de chats antiguos, y de hilos de canales con el visto bueno de tu admin, llega después como [historial](history.md), poco a poco, sin frenar nada.

Con el OK de tu admin, también lee:

- Los hilos de los canales de tus equipos.
- Las transcripciones de las reuniones que organizaste.
- Las notas de reuniones y tareas de Copilot, si tienes una licencia de Microsoft 365 Copilot.

Cada transcripción o conjunto de notas llega a su reunión en tu calendario, marcada **De Teams**. Sin ellas, el chat de la reunión sigue ahí.

Los bots, las apps y los mensajes del sistema quedan fuera.

## Qué puede hacer

Nada en Teams. Solo lee. Para responder, abre el chat con **Abrir en Teams**.

## Qué pide

Microsoft pide dejar que The Machine lea tus chats y tu perfil. Para eso no hace falta un admin.

Los canales, las transcripciones y las notas de Copilot necesitan una vez el OK del admin de tu organización. Hasta entonces, la tarjeta de Teams dice qué no puede leer todavía y por qué.

Solo funciona con una cuenta de Microsoft profesional o educativa. Las cuentas personales no tienen chats de Teams que se puedan leer así.

## Conéctalo

En una Machine alojada:

1. En el panel, abre **Conexiones**, **+ Añadir** y elige **Microsoft Teams** (en Chat) o **Reuniones de Teams** (en Reuniones). Las dos son el mismo inicio de sesión.
2. Pulsa **Iniciar sesión con Microsoft** y da el OK. Vuelves al panel.
3. Para los canales y las notas de reuniones, envía a tu admin el enlace que muestra la página de inicio de sesión. Cuando lo apruebe, conecta Teams de nuevo.

Durante la configuración, la página de configuración también tiene **Connect Microsoft Teams**.

En tu propio ordenador, Teams aún no está disponible.

## Quítalo

En el panel: **Conexiones**, abre Microsoft Teams, **Detalles** y luego **Desconectar**. Lo que ya trajo se queda.

## Revócalo en Microsoft

Abre myapps.microsoft.com y quita The Machine. Si Outlook está conectado con la misma dirección, también se desconecta.
