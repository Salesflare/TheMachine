# Glossary

How The Machine's product terms read in each language. Every catalog in this folder follows it, and
`tests/test_i18n.py` checks that: when an English string uses a term from the **Terms** table, its translation uses one
of the forms listed for that language (any of the forms after the first are inflections the check also accepts). A
capitalized term (Ready, Settings) is the name of a status or a screen and only counts capitalized; a lowercase one
counts in any case. File names (.skill, SKILL.md) don't count.

Tone: short UI copy, the way a native product says it, never word for word. Dutch uses *je*, French *vous*, German *du*,
Spanish *tú*, Italian *tu*, Brazilian Portuguese *você*. No em dashes. Placeholders (`{}`, `{0}`, `{1}`) stay; reorder with `{0}`, `{1}` when the sentence needs it.

## Names

Product and brand names stay exactly as they are in every language, and the check requires them verbatim:

The Machine, Machine (an owner's own Machine: "your Machine"), The Machine Network, Network, Graph, Fleet, Telegram,
Gmail, Google, Outlook, Microsoft, Slack, WhatsApp, LinkedIn, Intercom, Zoom, Stripe, GitHub, Salesflare, OpenClaw,
ClawHub, Claude, Claude Code, Codex, ChatGPT, Trello, Shortcut.

## Terms

| English | nl | fr | de | es | it | pt-BR |
|---|---|---|---|---| --- | --- |
| to-do | to-do, to-do's | tâche, tâches | Aufgabe, Aufgaben | tarea, tareas | attività | tarefa, tarefas |
| snooze | snooze, snoozen, gesnoozed | mettre en attente, en attente, attente | zurückstellen, zurückgestellt, Zurückstellen | posponer, pospuesto, pospuesta, pospón | posticipa, posticipare, posticipata, posticipato, posticipate, posticipati, posticipo, posticipi | adiar, adiada, adiado, adiadas, adiados, adie, adia |
| hand off | overdragen, overdracht, draag over | transférer, transfert, transférez | übergeben, Übergabe, übergib | pasar, traspaso, pasa | passa, passare, passala, passalo, passaggio | passar, passe, repasse, repassar |
| handoff | overdracht, overdragen | transfert, transférer | Übergabe, übergeben | traspaso, pasar | passaggio, passare | repasse, passar |
| Ready | Klaar | Prêt, Prête, Prêts | Bereit | Listo, Lista, Listos | Pronto, Pronta, Pronti, Pronte | Pronto, Pronta, Prontos, Prontas |
| To decide | Te beslissen | À décider | Zu entscheiden | Por decidir | Da decidere | A decidir |
| Not needed | Niet nodig | Pas nécessaire | Nicht nötig | No hace falta | Non serve | Não precisa |
| signal | signaal, signalen | signal, signaux | Signal, Signale | señal, señales | segnale, segnali | sinal, sinais |
| draft | concept, concepten | brouillon, brouillons | Entwurf, Entwürfe | borrador, borradores | bozza, bozze | rascunho, rascunhos |
| skill | skill, skills | compétence, compétences | Skill, Skills | habilidad, habilidades | skill | habilidade, habilidades |
| Connections | Koppelingen | Connexions | Verbindungen | Conexiones | Connessioni | Conexões |
| Settings | Instellingen | Paramètres | Einstellungen | Ajustes | Impostazioni | Configurações |
| Suggestions | Suggesties | Suggestions | Vorschläge | Sugerencias | Suggerimenti | Sugestões |
| saved sign-in | opgeslagen login, opgeslagen logins | identifiant enregistré, identifiants enregistrés | gespeicherte Anmeldung, gespeicherte Anmeldungen, gespeicherten Anmeldungen | inicio de sesión guardado, inicios de sesión guardados | accesso salvato, accessi salvati | login salvo, logins salvos |
| work hours | werkuren | heures de travail | Arbeitszeiten | horario laboral | orario di lavoro | horário de trabalho |
| digest | overzicht | récap | Zusammenfassung | resumen | riepilogo | resumo |
| promise | belofte, beloftes, beloofd | promesse, promesses, promis | Versprechen, versprochen | promesa, promesas, prometido, prometiste, prometió, prometieron | promessa, promesse, promesso, promessi | promessa, promessas, prometeu, prometido, prometi, prometeram |
| learning | inzicht, inzichten | apprentissage, apprentissages | Erkenntnis, Erkenntnisse | aprendizaje, aprendizajes | apprendimento, apprendimenti | aprendizado, aprendizados |
| error report | foutrapport, foutrapporten | rapport d’erreur, rapports d’erreur | Fehlerbericht, Fehlerberichte | informe de errores, informes de errores | segnalazione di errore, segnalazioni di errore | relatório de erro, relatórios de erro |

## Exceptions

English strings the check skips, with why:

- `Claude sends its result back through The Machine connector. Add it once in claude.ai, Settings, Connectors, Add custom connector:` names claude.ai's own menus, which read in English.
- `Zoom in` is the browser viewer's zoom button, not the Zoom app.
- `Zoom out` is the browser viewer's zoom button, not the Zoom app.

## Not checked, but use these

The user-facing name is *to-do* (decided 2026-10-26): Dutch keeps "to-do", the others use their own word, the same one every time.

| English | nl | fr | de | es | it | pt-BR |
|---|---|---|---|---| --- | --- |
| Done (a to-do) | Gedaan | Fait | Erledigt | Hecho | Fatto | Feito |
| Due (a to-do's date) | Deadline (never "Te doen": that means to do) | Échéance | Fällig | Vence | Scadenza | Vence, Prazo |
| Do it | Doe het | Faire | Ausführen | Hazlo | Fallo | Fazer |
| task, Tasks (when it means a to-do: "All tasks", "View task") | to-do, To-do's | tâche, Tâches | Aufgabe, Aufgaben | tarea, Tareas | attività, Attività | tarefa, Tarefas |
| task (an agent's job: "your agent can use it in any task") | taak | tâche | Aufgabe | tarea | compito | tarefa |
| task page (the shared page for someone outside) | taakpagina | page de tâche | Aufgabenseite | página de tarea | pagina attività | página de tarefa |
| Close / Regular / Occasional / Faint (closeness) | Hecht / Regelmatig / Af en toe / Zwak | Proche / Régulier / Occasionnel / Faible | Eng / Regelmäßig / Gelegentlich / Schwach | Cercano / Habitual / Ocasional / Débil | Stretto / Regolare / Occasionale / Debole | Próximo / Regular / Ocasional / Fraco |
| Only about (a sharing limit) | Alleen over | Seulement à propos de | Nur über | Solo sobre | Solo su | Só sobre |
| Previous / Next (week, month, days) | one whole string per step ("Vorige week"), never "Previous {}": the word agrees with the noun | | | | | |
| Work / Personal | Werk / Privé | Travail / Perso | Arbeit / Privat | Trabajo / Personal | Lavoro / Personale | Trabalho / Pessoal |
| People / Organizations / Projects | Personen / Organisaties / Projecten | Personnes / Organisations / Projets | Personen / Organisationen / Projekte | Personas / Organizaciones / Proyectos | Persone / Organizzazioni / Progetti | Pessoas / Organizações / Projetos |
| board | bord | tableau | Board | tablero | bacheca | quadro |
| chat | chat | chat | Chat | chat | chat | chat |
| Careful / Standard (security) | Voorzichtig / Standaard | Prudent / Standard | Vorsichtig / Standard | Prudente / Estándar | Prudente / Standard | Cuidadoso / Padrão |
| Fleet rules | Fleet-regels | règles Fleet | Fleet-Regeln | reglas de Fleet | regole Fleet | regras do Fleet |
| sign in / sign out | inloggen / uitloggen | se connecter / se déconnecter | anmelden / abmelden | iniciar sesión / cerrar sesión | accedi / esci | entrar / sair |
| thinking (a model's level) | denkwerk | réflexion | Nachdenken | razonamiento | ragionamento | raciocínio |

## Open questions for Jeroen

- German *du* and French *vous*: right register for the customers?
- *skill*: kept in Dutch and German, translated in French and Spanish.
- Italian uses informal *tu*, like Apple, Google and Spotify in Italian. Keeps "skill" in English, like Dutch and German.
- Brazilian Portuguese uses *você*. Settings reads "Configurações" (Android and web apps); iOS says "Ajustes".
- Portuguese from Portugal (and plain pt) reads Brazilian Portuguese until it has its own catalog.
