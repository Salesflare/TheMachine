---
title: Granola
area: connections
summary: Notas y transcripciones de tus reuniones en Granola. Solo lee.
covers: connector:granola
code: connectors/granola.py, meeting_notes.py, onboarding.py
site: Connect, More sources, Remove
translated: fb6244142af7800d
---
## Qué lee

Las notas y transcripciones de las reuniones en las que participaste, de los últimos 7 días al conectarla y, después, las nuevas a medida que llegan. Las notas que aún se están redactando se importan cuando Granola termina de prepararlas.

Cada elemento se añade a la reunión correspondiente de tu Calendario, la que indica Granola o, si no, la reunión que coincide en horario. Las notas de Granola aparecen en Notas y la transcripción, en Transcripción, con la marca **De Granola**. Lo que hayas añadido tú se conserva.

Después de la reunión, The Machine lee las notas y transcripciones para identificar lo prometido, lo decidido o lo que aún queda pendiente, como «Enviaré la presentación», y crea tareas solo para los próximos pasos claros. Las personas de la reunión se vinculan a tu [Graph](graph.md) mediante su dirección de correo.

## Qué puede hacer

Nada en Granola. Solo lee, nunca modifica, comparte ni elimina una nota.

## Qué necesita

Una clave de API personal de Granola. Granola ofrece claves de API en sus planes Business y Enterprise. La clave permite leer tus notas y las que se hayan compartido contigo, tal como las ves en Granola.

## Conéctala

1. En la aplicación de escritorio de Granola: **Ajustes**, **Conectores**, **Claves de API**. Crea una clave con **Acceso a notas personales** y cópiala.
2. En el panel: **Conexiones**, **Reuniones**, Granola. O, en la página de configuración de una Machine alojada, en app.themachine.computer/setup: **Más fuentes**, Granola. En tu propio ordenador, `assistant connect granola` también te la pedirá.
3. Pega la clave, elige **Trabajo** o **Personal** y pulsa **Conectar**.

La clave se comprueba al instante. Si Granola deja de aceptarla más adelante, Granola te pedirá una clave nueva en **Conexiones**.

## Desconéctala

- En el panel: **Conexiones**, abre Granola y selecciona **Detalles** y, después, **Desconectar**. Lo que ya haya importado se conserva.
- En una Machine alojada, también puedes pulsar **Quitar** junto a Granola en la página de configuración.

## Revoca la clave en Granola

En la aplicación de escritorio de Granola: **Ajustes**, **Conectores**, **Claves de API** y, después, elimina la clave.
