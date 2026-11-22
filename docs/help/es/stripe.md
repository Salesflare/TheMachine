---
title: Stripe
area: connections
summary: Pagos fallidos, disputas, cancelaciones y suscripciones nuevas de importe elevado. Solo lee datos.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 6e7ca235dc502297
---
## Qué lee

Eventos de tu cuenta de Stripe que pueden requerir tu atención: pagos fallidos, disputas, cancelaciones y suscripciones nuevas de importe elevado, junto con el cliente al que corresponden. El correo del cliente vincula el evento con esa persona y su organización en [Graph](graph.md).

## Qué puede hacer

No hace nada en Stripe. Nunca emite reembolsos, reintenta pagos ni cambia nada. Solo solicita acceso de lectura, y Stripe te lo muestra antes de que la instales.

## Conectarla

Inicia sesión con Stripe, la forma más sencilla:

1. En el panel: **Conexiones**, **Clientes**, Stripe. O, en la página de configuración de una Machine alojada, en app.themachine.computer/setup: **Más fuentes**, Stripe. En tu propio ordenador, primero vincúlala a tu cuenta.
2. Pulsa **Iniciar sesión con Stripe**. Stripe te pregunta qué cuenta quieres usar y te muestra qué puede leer The Machine.
3. Pulsa **Instalar**. Volverás al punto de partida y Stripe quedará conectada.

En tu propio ordenador, también puedes pegar una clave restringida:

1. En Stripe, crea una clave restringida con permiso de lectura en Events, Customers y Account, y sin permisos en todo lo demás.
2. Busca el ID de tu cuenta (acct_...) en Ajustes, Business details.
3. Abre Stripe como se indica arriba (o ejecuta `assistant connect stripe`), abre **O pega una clave restringida**, pega el ID de la cuenta y la clave, y pulsa **Conectar**.

En tu propio ordenador, si todavía no está disponible la opción para iniciar sesión con Stripe, Conexiones te lo indica y abre este formulario directamente.

## Conectarla una vez para todo el equipo

En un Fleet de trabajo, una persona propietaria o administradora conecta Stripe una vez y la comparte con el equipo:

1. Conecta Stripe en tu propia Machine (arriba). El recuadro **Conexiones compartidas** de la pestaña Fleet también tiene la opción **Conectar Stripe**.
2. En la pestaña Fleet, abre **Compartir Stripe**. Todos aparecen seleccionados; desmarca a quien no deba tener acceso. Pulsa **Compartir**.

Las Machines de tus compañeros también podrán leer los datos. Conexiones muestra quién la compartió, y solo los administradores del Fleet pueden cambiarla o detenerla. Tu Machine renueva su acceso cada hora, así que, mientras esté apagada, su acceso a Stripe se pausa. Nadie recibe tu inicio de sesión. Más información: [Fleets](fleet.md).

Si un compañero también conecta por su cuenta la misma cuenta de Stripe, solo la lee una vez: la conexión compartida queda en pausa.

No se puede compartir una conexión de Stripe configurada mediante un servicio cuya clave también da acceso a otras aplicaciones. En su lugar, conecta Stripe directamente para el equipo.

## Quitarla

- En el panel: **Conexiones**, abre Stripe, **Detalles** y luego **Desconectar**. Los datos que ya haya incorporado se mantienen.
- En una Machine alojada, Stripe muestra **Desconectar ↗** si iniciaste sesión. Esta opción abre tu página de configuración: pulsa **Quitar** junto a Stripe.
- Si la compartiste con un Fleet, primero pulsa **Dejar de compartir** en la pestaña Fleet.

## Revocar el acceso en Stripe

- Si iniciaste sesión con Stripe: en Stripe, abre Ajustes, Installed apps y elimina The Machine.
- Si usaste una clave restringida: en Stripe, abre Developers, API keys y elimina o rota la clave.
