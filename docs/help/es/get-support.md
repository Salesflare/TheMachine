---
title: Contactar con soporte
area: troubleshooting
summary: Informa de un error desde el panel, escríbenos o deja que nuestro equipo revise tu Machine durante un día.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
translated: 419a75e887b25e20
---
## Escríbenos

Escribe a support@themachine.computer. Te responderá una persona.

En una Machine alojada, el pie de página del panel incluye **¿Algo va mal?**, que abre el formulario de **Informar de un problema** de tu cuenta.

## Informar de un error

Abre **Ayuda** y luego **Informar de un error**. Los mensajes de error también incluyen el botón **Informar de un error**.

1. Cuéntanos qué ha pasado.
2. Añade una captura de pantalla si sirve de ayuda: **Hacer una captura** del panel o **Adjuntar una imagen**.
3. Si puedes, deja activada la opción **Incluir un informe de soporte**. Añade versiones, comprobaciones y errores recientes, pero no mensajes, claves ni direcciones. También permite que nuestro equipo lea los registros y los ajustes de tu Machine durante 24 horas. Consulta [Acceso de soporte](get-support.md#support-access). Si la desmarcas, solo se envían lo que has escrito y la captura.
4. Toca **Enviar**. El formulario se cierra enseguida y el informe de soporte se envía automáticamente.

Nos ocupamos del resto. Una Machine autoalojada puede enviar un informe cuando está en la Network. Si no, escríbenos.

También puedes decirle a tu Machine por el chat que algo va mal. Abrirá **Informar de un error** por ti, con lo que has escrito y un breve resumen ya incluidos. No se envía nada hasta que toques **Enviar**.

Cuando corregimos un error que has informado y tu Machine aplica la solución, te avisamos una vez: con una frase breve en el panel y un correo breve. Una Machine autoalojada se entera cuando está en la Network.

La frase te pregunta si ya funciona. Toca **Ya funciona** o **Aún no está bien** para contarnos qué sigue fallando. Si sirve de ayuda, puedes añadir una imagen. Se nos envía como un informe nuevo, vinculado al primero. **×** cierra el aviso sin responder.

¿Estás sin conexión o has enviado varios informes seguidos? No se pierde ninguno. Tu Machine los guarda y los envía automáticamente más tarde. Mientras tanto, aparecen en **Esperando para salir**.

## Acceso de soporte

Nuestro equipo puede revisar tu Machine por ti, pero solo si le das permiso. Si informas de un error con **Incluir un informe de soporte** activado, el acceso se habilita al tocar **Enviar**. Si usas tu propio ordenador, tienes que tener tu Machine [vinculada a tu cuenta](friends.md).

- Solo lectura: registros, ajustes, versiones, cómo se sincroniza cada conexión y errores recientes, con los mismos datos ocultos que en el informe de soporte. Nunca incluye tus mensajes, claves, contraseñas ni quiénes son tus contactos.
- El acceso termina automáticamente al cabo de 24 horas. Mientras está activo, puedes verlo en **Ajustes**, **Seguridad**. Toca **Desactivar** para terminarlo ahora.
- Cada revisión aparece en **Ajustes**, **Actividad**, con la fecha y la hora. Consulta [Actividad](activity.md).

## Desde tu propio ordenador

Ejecuta `assistant support-bundle`. Se guardará un archivo con las versiones, las comprobaciones de `assistant doctor`, los registros recientes y tus ajustes, sin claves, tokens, contraseñas ni direcciones. Revísalo y luego envíaselo a quien te esté ayudando.

Si encuentras un error en la aplicación de código abierto, abre una incidencia en [GitHub](https://github.com/Salesflare/TheMachine/issues) y usa solo datos inventados.
