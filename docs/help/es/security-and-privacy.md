---
title: Seguridad y privacidad
area: security
summary: Tu Machine privada, el correo almacenado cifrado y nada se envía sin tu visto bueno. Resumen breve, con enlaces.
covers:
code: message_seal.py, next_actions.py, SECURITY.md
order: 1
keywords: private, privacy, data, gdpr, encrypted, who can see, safe, stored, keep
translated: 27c910c92b215ad3
---
## En resumen

- Tu propia Machine: si está alojada, funciona en la nube de la UE, solo para ti y nunca se comparte. También puedes ejecutarla en tu propio ordenador.
- No leemos tu correo: los mensajes se almacenan cifrados y nuestras herramientas de asistencia no pueden abrirlos.
- Nada se envía sin tu visto bueno: lee y crea borradores, pero tú decides qué se envía. Consulta [Hazlo](do-it.md).
- No se usa para entrenar IA: no tenemos una IA propia. Tu proveedor trabaja con tu cuenta y según sus condiciones.
- Aprendizajes para el equipo, salvo que los desactives: de vez en cuando, se comparten algunos consejos generales, nada personal, y se revisan antes de enviarlos. Consulta [Compartir aprendizajes](share-learnings.md).
- Informes de errores, salvo que los desactives: cuando algo falla, se envían el tipo de error y el lugar del código donde ocurre. Nunca tus mensajes, nombres ni direcciones. Consulta [Informes de errores](error-reports.md).
- Recuento de uso en una Machine alojada: un recuento diario de lo que has hecho, como tareas abiertas o correos enviados, nunca su contenido, y de cuánto tarda en abrirse tu panel (solo los tiempos de carga, en móvil u ordenador, app o navegador).
- Llévatelo contigo o elimínalo: exporta todo desde **Ajustes** › **General**, o elimina tu Machine y sus copias de seguridad con un solo botón. Consulta [Cancelar o eliminar](cancel-and-delete.md).
- Se registran nuestros accesos: cada vez que nuestro equipo consulta el informe o los registros de tu Machine alojada. Los propietarios y administradores de Fleet pueden verlo en **Actividad**. Consulta [Fleets](fleet.md).

## Copias de seguridad

Una Machine alojada hace una copia de seguridad de tus datos cada noche. La copia se cifra en tu Machine antes de salir de ella y se guarda en Microsoft Azure, en los Países Bajos (UE). Se conservan las 7 copias diarias, las 4 semanales y las 3 mensuales más recientes, es decir, unos 3 meses. Se eliminan cuando se borra tu Machine.

¿Podemos abrirlas? Sí, para restaurar una Machine que haya fallado: guardamos la clave aparte de las copias de seguridad. Los mensajes de una copia se cifran una vez más con una segunda clave que también guardamos, sellada y que nunca está en la copia.

Son una red de seguridad, así que guarda una copia propia de lo que no quieras perder: **Todo**, en **Ajustes** › **General** › **Exportar**. Consulta [Pasar a otro ordenador](moving.md).

En tu propio ordenador no se hacen copias de seguridad automáticamente y nosotros no tenemos ninguna copia. Basta con hacer cada noche una copia cifrada de tu carpeta personal: consulta [Primeros pasos](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md#later).

## Niveles de seguridad

**Estándar** mantiene los ajustes predeterminados actuales. **Prudente** no muestra texto en las notificaciones, no guarda los inicios de sesión y conserva menos datos. El administrador de un Fleet de trabajo puede poner el Fleet en modo **Prudente**. Consulta [Niveles de seguridad](security-levels.md).

## Inicio de sesión

Para acceder a un panel alojado, necesitas una clave de acceso o iniciar sesión con Google o Microsoft y usar un código de autenticación.

## Conexiones

El artículo de cada conexión explica qué lee y qué puede enviar. Puedes desconectarlas cuando quieras: consulta [Conexiones](connections.md).

## Ayuda

La ayuda funciona en tu propia Machine y no puede ver tus datos. Solo se envía al equipo de The Machine el tema de cada pregunta, nunca lo que escribes. Consulta [Pedir ayuda](help-chat.md#what-the-team-sees).

## Más información

- [Seguridad](/security): cómo está diseñada, qué puede y qué no puede ver nuestro personal, y cómo buscamos problemas.
- [Aviso de privacidad](/privacy) y [condiciones de tratamiento de datos](/dpa).
- ¿Has encontrado un problema de seguridad? Consulta la [política de seguridad](https://github.com/Salesflare/TheMachine/blob/main/SECURITY.md).
