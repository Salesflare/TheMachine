---
title: Conocimiento para otra IA
area: settings
summary: Lleva lo que ha aprendido tu Machine a cualquier otra IA, en archivos de texto que cualquier IA puede leer.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: db1c7f4768a71630
---
Todo lo que aprende tu Machine te pertenece. Compártelo con otra IA, como ChatGPT o Claude, o guárdalo.

## Expórtalo

1. En **Ajustes** › **General** › **Exportar**, pulsa **Exportar** junto a **Conocimiento para otra IA**.
2. **Texto de los mensajes** está desactivado de forma predeterminada: solo se incluyen el origen de cada elemento y la fecha. Actívalo para añadir el texto.
3. Activa **Privado y Prudente** solo si quieres incluir proyectos solo tuyos, hilos privados y Fleets prudentes.
4. Si quieres, añade una **Frase de contraseña** (de al menos 10 caracteres) para cifrar el archivo.
5. Pulsa **Descargar**. El archivo solo se puede descargar una vez.

Funciona igual en una Machine alojada y en tu propio ordenador.

## Qué contiene

- Personas, organizaciones y proyectos: una página Markdown para cada uno, con sus relaciones.
- Datos y preferencias: lo que tu Machine sabe sobre ti y sobre los demás.
- Datos anteriores: lo que ya no se cumple porque terminó o se sustituyó, y qué lo sustituyó. Los datos que eliminaste no se incluyen.
- Reglas, tu forma de escribir y firmas: lo que siguen tus borradores.
- Habilidades: tus guías prácticas, activas o desactivadas.
- Contexto: resúmenes del equipo, frases de resumen, promesas y tareas abiertas.
- Fuentes: el origen de cada elemento, con su ID y fecha.

Los contactos y las tareas también se incluyen en hojas de cálculo (CSV). Al principio, encontrarás un README que explica a la IA cómo leerlo todo. Sube el archivo ZIP a la IA como archivo de conocimiento o proyecto.

## Qué no se incluye

Nunca se incluyen contraseñas, claves ni datos de inicio de sesión. Tampoco se incluyen los datos, los ajustes ni las fotos de tus compañeros de equipo. Para trasladar toda tu Machine, consulta [Pasar a otro ordenador](moving.md).

Para desarrolladores: [el formato de archivo](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
