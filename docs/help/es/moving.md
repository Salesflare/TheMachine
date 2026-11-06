---
title: Pásate a otro ordenador
area: getting-started
summary: Exporta todo lo que sabe tu Machine en un solo archivo cifrado e impórtalo en otra Machine, alojada o la tuya.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
---
Todo lo que aprende tu IA es tuyo: mensajes, conversaciones, tareas con su historial, borradores, el Graph, recuerdos, habilidades y trabajos de agentes. Puedes llevártelo todo, también si dejas de usar The Machine.

## Exportar

En tu propio ordenador:

1. En **Ajustes** › **General** › **Exportar**, pulsa **Exportar** junto a Todo.
2. Si quieres, elige una frase de contraseña. Sin ella, recibes un código de exportación: apúntalo, la importación lo necesita.
3. Si quieres, activa **Incluir claves y tokens** (necesita una frase de contraseña) para no tener que volver a conectar tus fuentes.
4. Pulsa **Empezar exportación** y luego **Descargar**. El archivo se elimina a las 24 horas, o al momento con **Eliminar**.

En una Machine alojada, **Exportar** junto a Todo abre la página de tu cuenta. Pulsa **Exportar todo** y luego **Descargar**. Tu Machine elimina el archivo a las 24 horas, o al momento con **Eliminarlo ahora**.

El archivo siempre va cifrado. Tras una exportación, Ajustes muestra lo que incluye, con cifras, y lo que no incluye y por qué. Los inicios de sesión en Google y Microsoft a través del servicio alojado siempre piden iniciar sesión de nuevo en el otro lado.

## Importar

1. En **Ajustes** › **General** › **Exportar**, pulsa **Elegir archivo** junto a Importar y elige la exportación.
2. Escribe su frase de contraseña o código de exportación y pulsa **Abrir**. The Machine revisa primero todo el archivo.
3. Alojada: pulsa **Importar ahora**. The Machine se reinicia con ella en unos minutos. En tu propio ordenador: pulsa **Reemplazar con esta exportación** y luego **Reemplazar**. The Machine se reinicia con ella en un par de minutos, y Ajustes muestra **Importada**.

La importación sustituye lo que tiene esa Machine ahora y antes guarda una copia. Nada de lo que esperaba sale por sí solo: los envíos en cola esperan a que los vuelvas a enviar.

Avanzado: en un ordenador donde The Machine funciona sin gestor de servicios, Ajustes muestra los comandos. También puedes ejecutarlos tú: `assistant service stop`, `assistant import --staged --force`, `assistant service start`.

En un ordenador nuevo, [instala primero The Machine](self-hosted-setup.md). Después cancela tu plan alojado si ya no lo necesitas: consulta [Cancelar o eliminar](cancel-and-delete.md).
