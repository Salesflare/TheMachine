---
title: Remitentes que se hacen pasar por otros
area: security
summary: Los correos de una dirección que imita a alguien con quien tratas se señalan en la tarea correspondiente, y los borradores nunca se envían a esa dirección.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 6a2d62a74cec9ee4
---
## Qué detecta

Algunas estafas llegan desde una dirección que se parece a una que conoces: `examp1e.com` en lugar de `example.com`, `example-billing.com` o con una letra distinta. The Machine compara el dominio de cada remitente con los dominios con los que ya tratas. Si la dirección nueva solo se parece a una conocida, la considera una imitación.

El mismo nombre con otra terminación, como `example.nl` junto a `example.com`, corresponde a la misma organización, no es una imitación. El correo gratuito, como gmail.com, nunca cuenta.

## En una tarea

Una tarea sobre un mensaje así lo indica claramente, por ejemplo: "Este no es Alex. El mensaje viene de examp1e.com, no de example.com". El remitente aparece solo con su dirección, sin foto ni enlace a la persona a la que imita.

## Lo que The Machine no hará

- Nunca asigna a un remitente que imita a alguien un rol en tu Graph.
- Nunca lo fusiona con la persona a la que imita ni te lo sugiere en **¿Misma persona?**.
- Si prepara una respuesta, la envía a la dirección registrada, no a la que imita.

Tu decisión siempre prevalece: puedes asignarle un rol, fusionarlo o escribir a cualquier dirección.
