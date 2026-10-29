---
title: Amigos y la Network
area: fleet
summary: Añade amigos por nombre de usuario, encuentra a gente que conoces que tiene una Machine y vincula una Machine en tu propio ordenador.
covers: friends
code: friends.py, network.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
---
## Amigos

Añade a alguien por su nombre de usuario exacto, en la pestaña **Fleet**, en Amigos. Los amigos pueden preguntar quién conoce a alguien, recibir contexto para reuniones y presentaciones cercanas, y ver cuándo estás ocupado (solo las horas ocupadas, nunca qué haces). Quita o bloquea a un amigo cuando quieras.

## Encuentra a gente que conoces

En el panel Network:

- "Ver cuáles de mis contactos tienen una Machine" te sugiere gente que conoces.
- "Dejar que me encuentren quienes tienen mi correo" permite que te encuentren.

Los dos están activados por defecto, y desactivados en el nivel de seguridad Prudente. Desactiva cualquiera cuando quieras; tu elección se mantiene.

La gente que conoces y está en la Network se te sugiere en cuanto la activas, y cuando alguien se une más tarde. Cada coincidencia viene con Conectar, Ahora no o **No sugerir nunca**. **Salir de la Network** te saca de ella.

## Una Machine en tu propio ordenador

Para unirte a la Network desde una Machine que gestionas tú:

1. En la página de tu cuenta en app.themachine.computer, pulsa **Vincular una Machine autoalojada**. El código funciona una vez, durante 15 minutos.
2. En tu ordenador, ejecuta `assistant fleet-pair` con el código y reinicia.

Hasta 5 Machines por cuenta. Cada una se puede desconectar desde ahí.
