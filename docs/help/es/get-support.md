---
title: Obtener ayuda
area: troubleshooting
summary: Informa de un error desde tu panel, escríbenos o deja que nuestro equipo mire tu Machine durante un día.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
---
## Escríbenos

Escribe a support@themachine.computer. Te responde una persona.

En una Machine alojada, el pie del panel tiene "¿Algo va mal?", que abre el formulario **Informar de un problema** de tu cuenta.

## Informa de un error

Abre **Ayuda** y luego **Informar de un error**. Un mensaje de error también tiene un botón **Informar de un error**.

1. Cuenta qué falló.
2. Añade una captura si ayuda: **Hacer una captura** del panel, o **Adjuntar una imagen**.
3. Deja activado **Incluir el informe de soporte**, salvo que prefieras que no: versiones, comprobaciones y errores recientes, sin mensajes, claves ni direcciones.
   Si podemos necesitar mirar más de cerca, marca también **Deja que soporte mire durante 24 horas**. Consulta [Acceso de soporte](get-support.md#support-access).
4. Toca **Revisar**. Muestra todo lo que se envía, tal como se envía.
5. Toca **Enviar**. No se envía nada antes.

Respondemos por correo. Una Machine autoalojada puede enviar uno cuando está en la Network; si no, escríbenos.

Cuando corregimos un error que reportaste y tu Machine ya tiene la corrección, te lo decimos una vez: una línea corta en tu panel (**Entendido** la cierra) y un correo corto. Una Machine autoalojada se entera cuando está en la Network.

Si un informe no puede salir enseguida (no tienes conexión o enviaste muchos en poco tiempo), no se pierde. Tu Machine lo guarda, te dice cuándo sale y lo envía sola. Los informes que aún esperan aparecen en **Esperando para salir**.

## Acceso de soporte

Nuestro equipo puede revisar tu Machine por ti, pero solo cuando lo permitas. Cuando informes de un error, marca **Deja que soporte mire durante 24 horas**. Se activa cuando pulsas **Enviar**. En tu propio ordenador, tu Machine tiene que estar [vinculada a tu cuenta](friends.md).

- Solo lectura: registros, ajustes, versiones, cómo se sincroniza cada conexión y errores recientes, limpiados como el informe de soporte. Nunca tus mensajes, claves, contraseñas ni quiénes son tus contactos.
- Termina solo a las 24 horas. Mientras está activo, **Ajustes**, **Seguridad** lo muestra: **Desactivar** lo termina ahora.
- Cada revisión aparece listada ahí, con la hora.

## Desde tu propio ordenador

Ejecuta `assistant support-bundle`. Guarda un archivo con versiones, las comprobaciones de `assistant doctor`, registros recientes y tus ajustes, sin claves, tokens, contraseñas ni direcciones. Revísalo y luego envíalo a quien te ayude.

Para un error en la app de código abierto, abre un issue en [GitHub](https://github.com/Salesflare/TheMachine/issues), solo con datos inventados.
