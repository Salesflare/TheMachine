---
title: Kennis voor een andere AI
area: settings
summary: Neem de kennis van je Machine mee naar een andere AI, als gewone bestanden die elke AI kan lezen.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: db1c7f4768a71630
---
Alles wat je Machine leert, is van jou. Geef die kennis aan een andere AI, zoals ChatGPT of Claude, of bewaar die zelf.

## Exporteren

1. Ga naar **Instellingen** › **Algemeen** › **Exporteren** en kies **Exporteren** naast **Kennis voor een andere AI**.
2. **Tekst van berichten** staat standaard uit: je ziet alleen waar elk item vandaan komt en wanneer. Schakel deze optie in om ook de tekst toe te voegen.
3. Schakel **Privé en Voorzichtig** alleen in als je projecten die alleen voor jou zijn, privéthreads en Voorzichtige Fleets wilt toevoegen.
4. Stel eventueel een **Wachtwoordzin** in (minstens 10 tekens) om het bestand te versleutelen.
5. Kies **Downloaden**. Je kunt het bestand maar één keer downloaden.

Dit werkt hetzelfde met een gehoste Machine en op je eigen computer.

## Wat erin staat

- Personen, organisaties en projecten: voor elk een Markdown-pagina, met hun onderlinge relaties.
- Feiten en voorkeuren: wat je Machine over jou en anderen weet.
- Feiten uit het verleden: wat niet meer geldt (omdat het is beëindigd of vervangen), en waardoor het is vervangen. Verwijderde feiten blijven achterwege.
- Regels, je schrijfstijl en handtekeningen: waar je concepten zich aan houden.
- Skills: je handleidingen, zowel ingeschakeld als uitgeschakeld.
- Context: teamoverzichten, samenvattingen, beloftes en openstaande to-do's.
- Bronnen: waar elk item vandaan komt, met id en datum.

Contacten en to-do's worden ook als spreadsheets (CSV) meegeleverd. Bovenaan staat een README met uitleg voor de AI over hoe die alles moet lezen. Upload het zipbestand naar de AI als kennisbestand of project.

## Wat er niet in staat

Wachtwoorden, sleutels en logins worden nooit opgenomen. Ook gegevens, instellingen en foto's van teamgenoten blijven achterwege. Lees [Verplaatsen naar een andere computer](moving.md) als je je hele Machine wilt verplaatsen.

Voor ontwikkelaars: [de bestandsindeling](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
