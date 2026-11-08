---
title: Mistral
area: connections
summary: Haz que tu Machine funcione con los modelos de Mistral, con una clave de API de Mistral. Le Chat Pro incluye créditos de API.
covers: mistral
code: docs/models.md, dashboard/settings-models.js
site: Other AI services, Save key
---
## Para qué sirve

Mistral es un proveedor europeo de IA. Con una clave de API de Mistral, tu Machine lee y redacta con los modelos de Mistral. The Machine no tiene IA propia: las peticiones van directamente a Mistral, con tu cuenta y según sus condiciones.

## Consigue una clave

Mistral no tiene inicio de sesión para otras apps, así que funciona con una clave de API. En la [consola de Mistral](https://console.mistral.ai/), abre API keys y crea una. Le Chat Pro incluye créditos de API cada mes; después, Mistral cobra por uso.

## Conéctalo

En una Machine alojada, abre tu página de configuración, ve a Tu IA y abre **Otros servicios de IA**. Elige Mistral como proveedor, pega la clave y pulsa **Guardar clave**. Tu Machine prueba antes la clave con una petición mínima. Si la clave está mal, lo ves ahí mismo y no se guarda nada.

Mistral Large pasa a ser el modelo principal. Mistral Small también está, como opción más barata para los chats o como respaldo.

En tu propio ordenador, mira la [guía de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).

## Uso

**Ajustes**, **Modelo** dice "Usa tu clave de API de Mistral". Una clave de API no tiene límites de uso, así que el trabajo en segundo plano nunca se pausa por ella. Mira [Modelo](model.md).

## Quítalo

Elige otro modelo principal en tu página de configuración. Para detener la clave, bórrala en la consola de Mistral.
