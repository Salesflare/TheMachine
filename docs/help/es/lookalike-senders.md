---
title: Remitentes que se hacen pasar por otros
area: security
summary: Los correos de una dirección que imita a alguien con quien tratas se señalan en la tarea correspondiente, y los borradores nunca se envían a esa dirección.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 15a6a5dafcfa807b
---
## Qué detecta

Algunas estafas llegan desde una dirección que se parece a otra que conoces: `examp1e.com` en lugar de `example.com`, `example-billing.com`, con una letra distinta o con dos letras intercambiadas. The Machine compara el dominio de cada remitente con los de las personas con quienes ya tratas.

Cuando dos direcciones se parecen, la auténtica es aquella a la que ya le has escrito, a cuyo remitente has conocido o que has configurado tú, aunque la otra haya escrito primero. Si ninguna destaca por esos motivos, la más reciente se considera la imitación.

El mismo nombre con otra terminación, como `example.nl` y `example.com`, corresponde a la misma organización, no a una imitación. Las cuentas de correo gratuitas, como gmail.com, nunca cuentan.

## En una tarea

Una tarea sobre un mensaje de este tipo lo indica claramente, por ejemplo: «No es Alex. El mensaje viene de examp1e.com, no de example.com». El remitente aparece solo como dirección, sin foto ni enlace a la persona a la que imita.

## Lo que The Machine no hará

- Nunca asigna un rol al remitente que imita a otra persona en tu Graph, ni convierte su dominio en la organización de un proyecto.
- Nunca lo fusiona con la persona a la que imita, ni siquiera si escribe en la misma conversación con el mismo nombre, y nunca te lo sugiere en **¿Misma persona?**.
- Si prepara una respuesta, la envía a la dirección registrada, no a la de quien imita a otra persona.

Tu decisión siempre prevalece: puedes asignarle un rol, fusionarlo o escribir a cualquier dirección.
