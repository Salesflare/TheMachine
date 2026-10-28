---
title: Google Meet
area: connections
summary: Las transcripciones y notas de Gemini de las reuniones de Meet que organizas. Solo lee.
covers: connector:google_meet
code: connectors/google_meet.py
site: Connect, More sources, Remove
---
## Qué lee

Las transcripciones y notas de Gemini de las reuniones de Google Meet que organizaste, en cuanto Meet las crea: los últimos 7 días al conectarlo y luego las nuevas a medida que llegan. Meet las guarda 30 días.

Meet solo las crea si las transcripciones o las notas de Gemini estaban activadas durante la reunión.

Cada una se asocia a la reunión de tu calendario a la misma hora. Las notas de Gemini aparecen en Notas de esa reunión y la transcripción en Transcripción, marcadas **De Google Meet**, junto a lo que añadiste ahí; nunca lo reemplazan.

## Qué puede hacer

Nada en Meet ni en Drive. Solo lee y nunca activa las transcripciones por su cuenta.

## Conéctalo

1. En Google Cloud, activa la API de Google Meet y la API de Google Drive.
2. En el OAuth Playground, consigue un token de acceso con los dos scopes de solo lectura que muestra la pantalla de conexión.
3. En una Machine alojada: abre tu página de configuración en app.themachine.computer/setup, ve a **Más fuentes** y abre Google Meet. En tu propio ordenador: **Conexiones**, **+ Añadir**, Google Meet, o `assistant connect google_meet`.
4. Pega el token y pulsa **Conectar**.

El token caduca tras una hora más o menos. Cuando Conexiones diga que fue rechazado, pega uno nuevo.

## Quítalo

- En el panel: **Conexiones**, abre Google Meet, **Detalles** y luego **Desconectar**. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Revócalo en Google

Abre myaccount.google.com/permissions y quita el acceso del OAuth Playground.
