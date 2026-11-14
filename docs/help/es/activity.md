---
title: Actividad
area: settings
summary: Una lista de todo lo que The Machine hizo por ti, lo más reciente primero: mensajes, documentos, respuestas de Fleet, aprendizajes, conexiones y más.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: 1b5a54aa775234bd
---
## Qué muestra

Abre **Ajustes**, **Actividad**. Cada línea es algo que hizo The Machine, lo más reciente primero, por día:

- qué hizo y cómo terminó: enviado, rechazado, fallido o deshecho
- cuándo, la cuenta o app que usó y [qué lo permitió](activity.md#what-allowed-it)
- un enlace a su tarea, cuando la hay
- para una IA que conectaste, como ChatGPT o Claude: su nombre con **(IA conectada)**, para distinguirla de The Machine

Incluye mensajes y respuestas, cambios en documentos y en el calendario, pasos en la web, correcciones que fusionó, agentes de código, preguntas y respuestas de Fleet, aprendizajes enviados al equipo de The Machine, habilidades, importaciones al Graph, datos que pediste olvidar en el chat (con **Deshacer**), conexiones añadidas o quitadas, y cada revisión de nuestro equipo con el [Acceso de soporte](get-support.md#support-access), también las rechazadas.

## Qué lo permitió

Cada mensaje, cambio en documentos o en el calendario, paso en la web y arreglo fusionado dice qué lo dejó salir, tal como pasó:

- **Aprobado en la tarea** o **Aprobado en Telegram**: tu toque en Enviar, Confirmar o Fusionar
- **Aprobado por voz**: tu sí en Talk
- **Se tocó «Hazlo»**: tu Hazlo en la tarea
- **Pedido en el chat**: lo pediste con palabras, con el inicio de tu mensaje entre comillas. Una cita solo se muestra mientras esas palabras sigan en tu propio mensaje.
- **Seguimiento que envió por sí sola**, **Arreglo pequeño, fusionado por sí sola**, **Documento privado nuevo, creado por sí sola** o **Preparado con antelación, por sí sola**: un ajuste tuyo o una regla propia de The Machine
- **Sin aprobación registrada**: no se registró nada. También va a nuestros [informes de errores](error-reports.md), para encontrar el camino que lo omitió.

Pasos en la web también lista la ejecución de una tarea que hizo clic o escribió en una página, con lo que permitió esa ejecución.

Las líneas antiguas, de antes de registrar esto, conservan sus palabras, como **Tras tu OK**.

## Filtrar

Elige un tipo en la lista de arriba, como **Mensajes** o **Fleet**. **Rechazado o bloqueado** muestra solo lo que no salió, y por qué. **Mostrar más** carga líneas más antiguas.

## Otros lugares

El chat de una tarea sigue contando su propia historia; Actividad enlaza a ella. Fleet, **Actividad** muestra las mismas líneas para tus Fleets y aprendizajes, con **Retirar** para un aprendizaje. En Ajustes, **Seguridad**, **Ver cada revisión en Actividad** abre las revisiones de nuestro equipo.

Actividad solo muestra lo que pasó. Nunca cambia lo que The Machine puede hacer.
