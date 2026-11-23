---
title: Stripe
area: connections
summary: Pagos fallidos, disputas, cancelaciones y nuevas suscripciones importantes. Solo lee.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 85e6e07cca1a8e8d
---
## Qué lee

Eventos de tu cuenta de Stripe que pueden requerir tu atención: pagos fallidos, disputas, cancelaciones y nuevas suscripciones importantes, junto con el cliente al que corresponden. El correo del cliente vincula el evento con esa persona y su organización en [Graph](graph.md).

Un pago fallido indica para qué era (un primer pago, una renovación) y cuándo volverá a intentarlo Stripe. No indica por qué se rechazó la tarjeta: Stripe no incluye ese dato en el evento, así que ábrelo en Stripe para saber el motivo.

## Qué puede hacer

Nada en Stripe. Nunca hace reembolsos, vuelve a intentar pagos ni cambia nada. Solo solicita acceso de lectura, y Stripe te lo muestra antes de instalarla.

## Conectarla

Inicia sesión con Stripe, la forma más fácil:

1. En el panel: **Conexiones**, **Clientes**, Stripe. O, en la página de configuración de una Machine alojada, en app.themachine.computer/setup: **Más fuentes**, Stripe. En tu propio ordenador, primero vincúlala a tu cuenta.
2. Pulsa **Iniciar sesión con Stripe**. Stripe te pregunta qué cuenta quieres usar y te muestra qué puede leer The Machine.
3. Pulsa **Instalar**. Volverás a donde estabas y Stripe quedará conectada.

En tu propio ordenador, también puedes pegar una clave restringida:

1. En Stripe, crea una clave restringida con permiso de Lectura para Eventos, Clientes y Cuenta, y Ninguno para todo lo demás.
2. Busca el ID de tu cuenta (acct_...) en Ajustes, Datos de la empresa.
3. Abre Stripe como se indica arriba (o ejecuta `assistant connect stripe`), abre **O pega una clave restringida**, pega el ID de la cuenta y la clave, y pulsa **Conectar**.

En tu propio ordenador, si todavía no está disponible Iniciar sesión con Stripe, Conexiones te lo indica y abre directamente este formulario.

## Conectarla una vez para todo el equipo

En un Fleet de trabajo, una persona propietaria o administradora conecta Stripe una vez y la comparte con el equipo:

1. Conecta Stripe en tu Machine (arriba). El recuadro **Conexiones compartidas** de la pestaña Fleet también incluye **Conectar Stripe**.
2. En la pestaña Fleet, abre **Compartir Stripe**. Todo el mundo está seleccionado; desmarca a quien no deba tener acceso. Pulsa **Compartir**.

Las Machines de tus compañeros de equipo también podrán leer los datos. En Conexiones se muestra quién la compartió. Solo las personas administradoras del Fleet pueden cambiarla o dejar de compartirla. Tu Machine renueva su acceso cada hora, así que, mientras esté apagada, Stripe dejará de estar disponible para ellos. Nadie obtiene tus credenciales de inicio de sesión. Más información: [Fleets](fleet.md).

Si alguien del equipo también conecta por su cuenta la misma cuenta de Stripe, solo se lee una vez: la conexión compartida queda en pausa.

No se puede compartir una conexión a Stripe hecha mediante un servicio cuya clave también da acceso a otras aplicaciones. En su lugar, conecta Stripe directamente para el equipo.

## Quitarla

- En el panel: **Conexiones**, abre Stripe, **Detalles** y, después, **Desconectar**. Los datos que ya haya importado se conservan.
- En una Machine alojada, Stripe muestra **Desconectar ↗** si has iniciado sesión. Se abrirá tu página de configuración: pulsa **Quitar** junto a Stripe.
- Si la compartes con un Fleet, primero pulsa **Dejar de compartir** en la pestaña Fleet.

## Revocar el acceso en Stripe

- Si has iniciado sesión con Stripe: en Stripe, abre Ajustes, Aplicaciones instaladas y elimina The Machine.
- Si usas una clave restringida: en Stripe, abre Desarrolladores, Claves de API y elimina o rota la clave.
