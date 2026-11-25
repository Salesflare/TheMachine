---
title: Actividad
area: settings
summary: Una lista con todo lo que The Machine ha hecho por ti, de lo más reciente a lo más antiguo: mensajes, documentos, respuestas de Fleet, aprendizajes, conexiones y más.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: 1ebeba09417a11e9
---
## Qué muestra

Abre **Ajustes** y **Actividad**. Cada línea muestra una acción de The Machine, ordenada por día, de la más reciente a la más antigua:

- qué hizo y cómo terminó: enviado, rechazado, fallido o deshecho; en el caso de un mensaje que [se envía más tarde](send-later.md), también cuándo se programó, modificó o canceló
- cuándo, qué cuenta o aplicación usó y [qué lo permitió](activity.md#what-allowed-it)
- un enlace a su tarea, si la hay
- si se trata de una IA que conectaste, como ChatGPT o Claude: su nombre seguido de **(IA conectada)**, para que puedas distinguirla de The Machine

La lista incluye mensajes y respuestas, cambios en documentos y calendarios, pasos en la web, arreglos que fusionó, agentes de programación, preguntas y respuestas de Fleet, aprendizajes enviados al equipo de The Machine, habilidades, importaciones de Graph, datos que pediste a tu chat que olvidara (con **Deshacer**), conexiones añadidas o eliminadas y cada revisión de nuestro equipo en [Acceso de soporte](get-support.md#support-access), incluidas las rechazadas.

## Qué lo permitió

Cada mensaje, cambio en un documento o calendario, paso en la web y arreglo fusionado indica qué permitió que se llevara a cabo:

- **Aprobado en la tarea** o **Aprobado en Telegram**: tocaste **Enviar**, **Confirmar** o **Fusionar**
- **Aprobado por voz**: dijiste que sí en Talk
- **Se tocó «Hazlo»**: tocaste **Hazlo** en la tarea
- **Pedido en el chat**: lo pediste con palabras, y se muestra el comienzo de tu mensaje entre comillas. La cita solo aparece mientras esas palabras sigan en tu mensaje.
- **Seguimiento que envió por sí sola**, **Arreglo pequeño, lo fusionó ella sola**, **Documento privado nuevo, creado por sí sola** o **Preparado con antelación, por sí sola**: se debió a un ajuste tuyo o a una de las reglas de The Machine
- **Sin aprobación registrada**: no se registró ninguna aprobación. También aparece en nuestros [informes de errores](error-reports.md), para que podamos encontrar qué paso falló.

Los pasos en la web también muestran las ejecuciones de una tarea que hicieron clic o escribieron en una página, junto con lo que permitió cada ejecución. Si un trabajo continúa después de posponerlo, conserva lo que lo había permitido antes de posponerlo.

Las líneas anteriores, de antes de que empezáramos a registrar esta información, conservan sus textos anteriores, como **Tras tu OK**.

## Filtrar la lista

Elige un tipo en la lista de arriba, como **Mensajes** o **Fleet**. **Rechazado o bloqueado** muestra solo lo que no se llevó a cabo y el motivo. **Mostrar más** carga líneas anteriores.

## Otros lugares

El chat de una tarea sigue contando su propia historia; Actividad incluye un enlace. En Fleet, **Actividad** muestra las mismas líneas de tus Fleets y aprendizajes, con la opción **Retirar** para un aprendizaje. En Ajustes, **Seguridad**, **Ver cada revisión en Actividad** abre las revisiones de nuestro equipo.

Actividad solo muestra lo que ocurrió. Nunca cambia lo que The Machine puede hacer.
