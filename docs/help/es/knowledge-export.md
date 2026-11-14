---
title: Conocimiento para otra IA
area: settings
summary: Llévate lo que ha aprendido tu Machine a cualquier otra IA en archivos sencillos que cualquier IA puede leer.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: 6a917f8ee2aabaa9
---
Todo lo que aprende tu Machine es tuyo. Puedes compartirlo con otra IA, como ChatGPT o Claude, o guardarlo.

## Exportarlo

1. En **Ajustes** › **General** › **Exportar**, pulsa **Exportar** junto a **Conocimiento para otra IA**.
2. **Texto de los mensajes** está desactivado de forma predeterminada: solo se incluye de dónde viene cada elemento y cuándo. Actívalo para incluir el texto.
3. Activa **Privado y Prudente** solo para incluir proyectos solo tuyos, hilos privados y Fleets con **Privado y Prudente** activado.
4. Si quieres, configura una **Frase de contraseña** (de al menos 10 caracteres) para cifrar el archivo.
5. Pulsa **Descargar**. El archivo solo se puede descargar una vez.

Funciona igual en una Machine alojada y en tu propio ordenador.

## Qué incluye

- Personas, organizaciones y proyectos: una página Markdown para cada uno, con sus relaciones.
- Datos y preferencias: lo que sabe tu Machine sobre ti y sobre los demás.
- Datos anteriores: lo que ya no es válido (porque terminó, se dejó de lado o se reemplazó), junto con lo que lo reemplazó. Los datos que eliminaste no se incluyen.
- Reglas, estilo de escritura y firmas: lo que siguen tus borradores.
- Habilidades: tus instrucciones, activas e inactivas.
- Contexto: información para el equipo, resúmenes, promesas y tareas pendientes.
- Fuentes: de dónde viene cada elemento, por ID y fecha.

Los contactos y las tareas también se incluyen en hojas de cálculo (CSV). En la parte superior, un README explica a la IA cómo leerlo todo. Sube el archivo zip a la IA como archivo de conocimiento o proyecto.

## Qué no incluye

Nunca se incluyen contraseñas, claves ni datos de inicio de sesión. Tampoco se incluyen los datos, ajustes ni fotos de tus compañeros de equipo. Para trasladar toda tu Machine, consulta [Cómo cambiar de ordenador](moving.md).

Para desarrolladores: [el formato del archivo](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
