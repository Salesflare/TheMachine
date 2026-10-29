---
title: Stripe
area: connections
summary: Pagos fallidos, disputas, cancelaciones y suscripciones nuevas grandes. Solo lee.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
---
## Qué lee

Eventos de tu cuenta de Stripe que pueden necesitarte: pagos fallidos, disputas, cancelaciones y suscripciones nuevas grandes, con el cliente al que pertenecen. El correo de un cliente vincula el evento a esa persona y a su organización en el [Graph](graph.md).

## Qué puede hacer

Nada en Stripe. Nunca escribe, reembolsa ni reintenta un pago. La app de Stripe de The Machine solo pide a Stripe permisos de lectura, y Stripe te los muestra antes de que la instales.

## Conéctalo

Inicia sesión con Stripe, la forma fácil:

1. En el panel: **Conexiones**, **+ Añadir**, Stripe. O en la página de configuración de una Machine alojada, en app.themachine.computer/setup: **Más fuentes**, Stripe. En tu propio ordenador, vincúlalo primero a tu cuenta.
2. Pulsa **Iniciar sesión con Stripe**. Stripe te pregunta qué cuenta, y muestra lo que The Machine puede leer.
3. Pulsa **Instalar**. Vuelves a donde empezaste, y Stripe está conectado.

O pega una clave restringida:

1. En Stripe, crea una clave restringida con Read en Events, Customers y Account, y None en todo lo demás.
2. Busca el ID de tu cuenta (acct_...) en Settings, Business details.
3. Abre Stripe como arriba (o ejecuta `assistant connect stripe`), abre **O pega una clave restringida**, pega el ID de la cuenta y la clave; luego pulsa **Conectar**.

En tu propio ordenador, si iniciar sesión con Stripe aún no está disponible, + Add lo dice y abre este formulario directamente.

## Conéctalo una vez para tu equipo

En un Work Fleet, un propietario o administrador conecta Stripe una vez y lo comparte con el equipo:

1. Conecta Stripe en tu propia Machine (arriba). El cuadro **Conectores compartidos** de la pestaña Fleet también tiene **Conectar Stripe**.
2. En la pestaña Fleet, abre **Compartir Stripe**. Todos están marcados; desmarca a quien no deba recibirlo. Pulsa **Compartir**.

Las Machines de los compañeros también lo leen, solo lectura. En Conexiones dice quién lo compartió, y solo los administradores del Fleet pueden cambiarlo o pararlo. Tu Machine renueva su acceso cada hora, así que mientras está apagada más tiempo, su Stripe se pausa hasta que vuelva. Nadie recibe nunca tu inicio de sesión. Detalles: [Fleets](fleet.md).

Una conexión de Stripe que pasa por otro servicio, con una sola clave para muchas conexiones, no se puede compartir: esa clave abre más que Stripe. Conecta Stripe por separado para el equipo.

## Quítalo

- En el panel: **Conexiones**, abre Stripe, **Detalles** y luego **Desconectar**. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.
- Compartido con un Fleet: primero **Dejar de compartir** en la pestaña Fleet.

## Revócalo en Stripe

- Con sesión iniciada con Stripe: en Stripe, abre Settings, Installed apps, y quita The Machine.
- Clave restringida: en Stripe, abre Developers, API keys, y elimina o rota la clave.
