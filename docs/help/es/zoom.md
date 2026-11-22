---
title: Zoom
area: connections
summary: Resúmenes y transcripciones de las reuniones que organizas, generados por AI Companion. Solo lectura.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
translated: 9533caa1429fb3fc
---
## Qué lee

El resumen de AI Companion de cada reunión de Zoom que organizas y su transcripción, si Zoom la tiene: las de los últimos 7 días cuando conectas la cuenta y, después, las nuevas que vayan llegando. También lee tu nombre y correo de Zoom para saber de quién son las reuniones.

Los resúmenes requieren un plan de pago de Zoom, AI Companion activado durante la reunión y que no haya cifrado de extremo a extremo.

## Qué hace con esa información

Cada resumen se vincula a la reunión correspondiente de tu calendario. Aparece en **Notas** de esa reunión y la transcripción, en **Transcripción**, con la etiqueta **De Zoom**, junto a todo lo que hayas añadido. Tu Machine convierte en tareas los siguientes pasos que te corresponden. No se envía nada hasta que tú lo envíes.

## Qué puede hacer

Solo lee y solo tus propias reuniones. Nunca crea, cambia ni elimina nada en Zoom. Tu inicio de sesión de Zoom permanece en tu Machine.

## Conectarla

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre Zoom, elige trabajo o personal y pulsa **Conectar Zoom**.
3. Inicia sesión en Zoom y autoriza a The Machine (creada por Salesflare).

O, desde el panel: **Conexiones**, **Reuniones**, elige Zoom y pulsa **Iniciar sesión con Zoom**. Cuando termines, volverás al panel.

En tu propio ordenador, una vez [vinculada a tu cuenta](friends.md#a-machine-on-your-own-computer): abre **Conexiones**, luego **Reuniones**, elige Zoom y pulsa **Iniciar sesión con Zoom**.

## Quitarla

- Desde el panel: **Conexiones**, abre Zoom, **Detalles** y luego **Desconectar**. Dejará de leer. Lo que ya haya importado se queda.
- En una Machine alojada, también puedes pulsar **Quitar** junto a Zoom en tu página de configuración.

## Desinstalarla en Zoom

Inicia sesión en marketplace.zoom.us, abre Manage, luego Added Apps y elimina The Machine. Ya no podrá leer nada. Lo que ya haya importado permanecerá en tu Machine hasta que lo elimines: consulta [Cancelar y eliminar](cancel-and-delete.md).
