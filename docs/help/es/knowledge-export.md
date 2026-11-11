---
title: Conocimiento para otra IA
area: settings
summary: Lleva lo que tu Machine ha aprendido a cualquier otra IA, en archivos sencillos Markdown, JSONL y CSV.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
---
Todo lo que aprende tu Machine es tuyo. Llévalo a otra IA, o guárdalo, aunque dejes de usar The Machine.

## Exportar

1. En **Ajustes** › **General**, pulsa **Exportar** junto a **Conocimiento para otra IA**.
2. Deja **Texto de los mensajes** desactivado para exportar solo de dónde vino cada cosa, y cuándo. Actívalo para añadir el texto.
3. **Privado y Prudente** sigue desactivado, salvo que quieras incluir también los proyectos solo para ti, las conversaciones privadas y los Fleets en Prudente.
4. Si quieres, pon una **Frase de contraseña** de al menos 10 caracteres para cifrar el archivo.
5. Pulsa **Descargar**. El archivo se crea en tu Machine y se puede descargar una vez.

En una Machine alojada funciona igual, desde los Ajustes de tu propia Machine. En tu propio ordenador, `assistant export-knowledge` crea el mismo archivo.

## Qué contiene

- Personas, organizaciones y proyectos: una página Markdown para cada uno, con cómo se relacionan.
- Datos y preferencias: lo que sabe tu Machine, sobre ti y sobre ellos.
- Datos anteriores: lo que ya no vale (terminado, apartado o sustituido), con lo que lo sustituyó. Los datos que quitaste quedan fuera.
- Reglas, cómo escribes y firmas: lo que siguen tus borradores.
- Habilidades: tus guías, activas o no.
- Contexto: resúmenes del equipo, líneas de resumen, promesas y tareas abiertas.
- Fuentes: de dónde vino cada cosa, con id y fecha.

Los registros son JSONL, los contactos y las tareas también CSV. Un README.md arriba explica la estructura y le dice a una IA cómo usarlo. Dale la carpeta, o el zip, a la IA como archivo de conocimiento o proyecto.

## Qué queda fuera

Contraseñas, claves e inicios de sesión nunca entran. Lo que parece una clave se reemplaza. Los datos de compañeros y de otras Machines, los ajustes y las fotos también quedan fuera. Para una copia completa con la que mudar tu Machine, consulta [Pásate a tu propio ordenador](moving.md).

El formato es abierto y tiene versiones: consulta [el esquema](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
