# Glossary

How The Machine's product terms read in each language. Every catalog in this folder follows it, and
`tests/test_i18n.py` checks that: when an English string uses a term from the **Terms** table, its translation uses one
of the forms listed for that language (any of the forms after the first are inflections the check also accepts). A
capitalized term (Ready, Settings) is the name of a status or a screen and only counts capitalized; a lowercase one
counts in any case. File names (.skill, SKILL.md) don't count.

Tone: short UI copy, the way a native product says it, never word for word. Dutch uses *je*, French *vous*, German *du*,
Spanish *tú*. No em dashes. Placeholders (`{}`, `{0}`, `{1}`) stay; reorder with `{0}`, `{1}` when the sentence needs it.

## Names

Product and brand names stay exactly as they are in every language, and the check requires them verbatim:

The Machine, Machine (an owner's own Machine: "your Machine"), The Machine Network, Network, Graph, Fleet, Telegram,
Gmail, Google, Outlook, Microsoft, Slack, WhatsApp, LinkedIn, Intercom, Zoom, Stripe, GitHub, Salesflare, OpenClaw,
ClawHub, Claude, Claude Code, Codex, ChatGPT, Trello, Shortcut.

## Terms

| English | nl | fr | de | es |
|---|---|---|---|---|
| to-do | to-do, to-do's | tâche, tâches | Aufgabe, Aufgaben | tarea, tareas |
| snooze | snooze, snoozen, gesnoozed | mettre en attente, en attente, attente | zurückstellen, zurückgestellt, Zurückstellen | posponer, pospuesto, pospuesta, pospón |
| hand off | overdragen, overdracht, draag over | transférer, transfert, transférez | übergeben, Übergabe, übergib | pasar, traspaso, pasa |
| handoff | overdracht, overdragen | transfert, transférer | Übergabe, übergeben | traspaso, pasar |
| Ready | Klaar | Prêt, Prête, Prêts | Bereit | Listo, Lista, Listos |
| To decide | Te beslissen | À décider | Zu entscheiden | Por decidir |
| Not needed | Niet nodig | Pas nécessaire | Nicht nötig | No hace falta |
| signal | signaal, signalen | signal, signaux | Signal, Signale | señal, señales |
| draft | concept, concepten | brouillon, brouillons | Entwurf, Entwürfe | borrador, borradores |
| skill | skill, skills | compétence, compétences | Skill, Skills | habilidad, habilidades |
| Connections | Koppelingen | Connexions | Verbindungen | Conexiones |
| Settings | Instellingen | Paramètres | Einstellungen | Ajustes |
| Suggestions | Suggesties | Suggestions | Vorschläge | Sugerencias |
| saved sign-in | opgeslagen login, opgeslagen logins | identifiant enregistré, identifiants enregistrés | gespeicherte Anmeldung, gespeicherte Anmeldungen, gespeicherten Anmeldungen | inicio de sesión guardado, inicios de sesión guardados |
| work hours | werkuren | heures de travail | Arbeitszeiten | horario laboral |
| digest | overzicht | récap | Zusammenfassung | resumen |
| promise | belofte, beloftes, beloofd | promesse, promesses, promis | Versprechen, versprochen | promesa, promesas, prometido, prometiste, prometió, prometieron |
| learning | inzicht, inzichten | apprentissage, apprentissages | Erkenntnis, Erkenntnisse | aprendizaje, aprendizajes |

## Exceptions

English strings the check skips, with why:

- `Claude sends its result back through The Machine connector. Add it once in claude.ai, Settings, Connectors, Add custom connector:` names claude.ai's own menus, which read in English.

## Not checked, but use these

| English | nl | fr | de | es |
|---|---|---|---|---|
| Done (a to-do) | Gedaan | Fait | Erledigt | Hecho |
| Do it | Doe het | Faire | Ausführen | Hazlo |
| Work / Personal | Werk / Privé | Travail / Perso | Arbeit / Privat | Trabajo / Personal |
| People / Organizations / Projects | Personen / Organisaties / Projecten | Personnes / Organisations / Projets | Personen / Organisationen / Projekte | Personas / Organizaciones / Proyectos |
| board | bord | tableau | Board | tablero |
| chat | chat | chat | Chat | chat |
| Careful / Standard (security) | Voorzichtig / Standaard | Prudent / Standard | Vorsichtig / Standard | Prudente / Estándar |
| Fleet rules | Fleet-regels | règles Fleet | Fleet-Regeln | reglas de Fleet |
| sign in / sign out | inloggen / uitloggen | se connecter / se déconnecter | anmelden / abmelden | iniciar sesión / cerrar sesión |

## Open questions for Jeroen

- *to-do*: kept as "to-do" in Dutch (it is what Dutch speakers say), translated elsewhere. Keep it English everywhere?
- German *du* and French *vous*: right register for the customers?
- *skill*: kept in Dutch and German, translated in French and Spanish.
