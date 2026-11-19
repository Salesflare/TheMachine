---
title: Actividad
area: settings
summary: Una lista de todo lo que hizo The Machine por ti, de lo más reciente a lo más antiguo: mensajes, documentos, respuestas de Fleet, aprendizajes, conexiones y más.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: ebb6a4cf0474a020
---
## Qué muestra

Abre **Ajustes** y **Actividad**. Cada línea muestra algo que hizo The Machine, ordenado por día, de lo más reciente a lo más antiguo:

- qué hizo y cómo terminó: se envió, se rechazó, falló o se deshizo
- cuándo, qué cuenta o app usó y [qué lo permitió](activity.md#what-allowed-it)
- un enlace a la tarea, si la hay
- si se trata de una IA que conectaste, como ChatGPT o Claude: su nombre seguido de **(IA conectada)**, para que puedas distinguirla de The Machine

Aquí aparecen los mensajes y las respuestas, los cambios en documentos y calendarios, los pasos en la web, los arreglos que fusionó, los agentes de programación, las preguntas y respuestas de Fleet, los aprendizajes que envió al equipo de The Machine, las habilidades, las importaciones de Graph, los datos que le pediste a tu chat que olvidara (con **Deshacer**), las conexiones que se añadieron o quitaron y cada revisión de nuestro equipo en [Acceso de soporte](get-support.md#support-access), incluidas las que se rechazaron.

## Qué lo permitió

Cada mensaje, cambio en un documento o calendario, paso en la web y arreglo fusionado indica qué permitió que se llevara a cabo:

- **Aprobado en la tarea** o **Aprobado en Telegram**: tocaste **Enviar**, **Confirmar** o **Fusionar**
- **Aprobado por voz**: dijiste que sí en Hablar
- **Se tocó «Hazlo»**: tocaste Hazlo en la tarea
- **Pedido en el chat**: lo pediste con palabras. Se muestra el inicio de tu mensaje entre comillas. La cita solo aparece mientras esas palabras sigan en tu mensaje.
- **Seguimiento que envió por sí sola**, **Arreglo pequeño, fusionado por sí sola**, **Documento privado nuevo, creado por sí sola** o **Preparado con antelación, por sí sola**: lo permitió un ajuste tuyo o una de las reglas de The Machine
- **Sin aprobación registrada**: no se registró nada que lo autorizara. También se envía a nuestros [informes de errores](error-reports.md), para que podamos encontrar qué falló en el proceso.

En los pasos en la web también aparece la ejecución de una tarea que hizo clic o escribió en una página, junto con lo que la permitió. Si el trabajo continúa después de posponerlo, mantiene la autorización que tenía antes de posponerlo.

Las líneas antiguas, de antes de que empezáramos a registrar esto, conservan sus textos anteriores, como **Tras tu OK**.

## Filtrarla

Elige un tipo en la lista de arriba, como **Mensajes** o **Fleet**. **Rechazado o bloqueado** muestra solo lo que no se llevó a cabo y el motivo. Toca **Mostrar más** para cargar líneas anteriores.

## Otros lugares

El chat de una tarea sigue contando su propia historia; Actividad incluye un enlace. En Fleet, **Actividad** muestra las mismas líneas de tus Fleet y tus aprendizajes, con **Retirar** para quitar un aprendizaje. En Ajustes, **Seguridad** y **Ver cada revisión en Actividad** te llevan a las revisiones de nuestro equipo.

Actividad solo muestra lo que pasó. No cambia lo que puede hacer The Machine.
