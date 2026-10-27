---
title: Stripe
area: connections
summary: Pagos fallidos, disputas, cancelaciones y suscripciones nuevas grandes. Solo lee.
covers: connector:stripe
code: connectors/stripe.py
site: Connect, More sources, Remove
---
## Qué lee

Eventos de tu cuenta de Stripe que pueden necesitarte: pagos fallidos, disputas, cancelaciones y suscripciones nuevas grandes, con el cliente al que pertenecen.

## Qué puede hacer

Nada en Stripe. Nunca escribe, reembolsa ni reintenta un pago.

## Conéctalo

1. En Stripe, crea una clave restringida con Read en Events, Customers y Account, y None en todo lo demás.
2. Busca el ID de tu cuenta (acct_...) en Settings, Business details.
3. En una Machine alojada: abre tu página de configuración en app.themachine.computer/setup, ve a **Más fuentes** y abre Stripe. En tu propio ordenador: **Conexiones**, **+ Añadir**, Stripe, o `assistant connect stripe`.
4. Pega el ID de la cuenta y la clave; luego pulsa **Conectar**.

## Quítalo

- En el panel: **Conexiones**, abre Stripe, **Detalles** y luego **Desconectar**. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Revócalo en Stripe

En Stripe, abre Developers, API keys, y elimina o rota la clave restringida.
