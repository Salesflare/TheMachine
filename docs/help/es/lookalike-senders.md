---
title: Remitentes que imitan a otros
area: security
summary: Los correos de una dirección que imita a alguien con quien tratas se marcan en su tarea, y los borradores nunca se envían a esa dirección.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 457e3111d2e26dd6
---
## Qué detecta

Algunas estafas vienen de una dirección que se parece a una que conoces: `examp1e.com` para `example.com`, `example-billing.com`, o con una letra cambiada. The Machine compara el dominio de cada remitente con los de las personas con quienes ya tratas. Si una dirección nueva solo se parece a una conocida, la considera una imitación.

El mismo nombre con otra terminación, como `example.nl` junto a `example.com`, corresponde a la misma organización, no es una imitación. Las cuentas de correo gratuitas, como gmail.com, nunca cuentan.

## En una tarea

Una tarea sobre uno de estos mensajes lo indica claramente, por ejemplo: «Este no es Alex. El mensaje viene de examp1e.com, no de example.com». El remitente aparece como la dirección sola, sin foto ni enlace a la persona a la que imita.

## Lo que The Machine no hará

- Nunca asigna un rol en tu Graph a un remitente que imita a otra persona.
- Nunca lo combina con la persona a la que imita ni lo sugiere en **¿Misma persona?**.
- Las respuestas que prepara se envían a la dirección registrada, no a la dirección que imita a otra persona.

Tu decisión siempre prevalece: puedes asignarle un rol, combinarlo con otra persona o escribir a cualquier dirección.
