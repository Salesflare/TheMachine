---
title: Zoom
area: connections
summary: Los resúmenes y transcripciones de AI Companion de las reuniones que organizas. Solo lee.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
---
## Qué lee

El resumen de AI Companion de cada reunión de Zoom que organizas, y su transcripción cuando Zoom la tiene: los últimos 7 días al conectar, y luego los nuevos según llegan. También lee tu nombre y correo de Zoom, para saber de quién son las reuniones.

Los resúmenes necesitan un plan de pago de Zoom, AI Companion activado durante la reunión y sin cifrado de extremo a extremo.

## Qué hace con ellos

Cada resumen se empareja con la reunión de tu calendario. Tus revisiones lo usan luego para el seguimiento de esa reunión, y un reparto de seguimiento del Fleet llega ya rellenado con quién hace qué. Tú lo revisas y lo editas primero; no se envía nada hasta que lo envíes.

## Qué puede hacer

Solo lee. Nunca crea, cambia ni elimina nada en Zoom, y solo ve tus propias reuniones. Tu inicio de sesión de Zoom se guarda en tu propia Machine.

## Conéctalo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre Zoom, elige trabajo o personal, y pulsa **Conectar Zoom**.
3. Inicia sesión en Zoom y permite The Machine. La hace Salesflare.

En tu propio ordenador, una vez [vinculado con tu cuenta](fleet.md): abre **Conexiones**, luego **+ Añadir**, elige Zoom y pulsa **Iniciar sesión con Zoom**.

## Quítalo

- En el panel: **Conexiones**, abre Zoom, **Detalles** y luego **Desconectar**. Deja de leer. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Desinstálalo en Zoom

Inicia sesión en marketplace.zoom.us, abre Manage, luego Added Apps, y quita The Machine. Ya no puede leer nada. Lo que ya trajo se queda en tu Machine hasta que lo elimines: consulta [Cancelar y eliminar](cancel-and-delete.md).
