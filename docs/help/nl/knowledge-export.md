---
title: Kennis voor een andere AI
area: settings
summary: Neem mee wat je Machine heeft geleerd naar een andere AI, in gewone bestanden die elke AI kan lezen.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: 6a917f8ee2aabaa9
---
Alles wat je Machine leert, is van jou. Geef het aan een andere AI, zoals ChatGPT of Claude, of bewaar het zelf.

## Exporteren

1. Ga naar **Instellingen** › **Algemeen** › **Exporteren** en klik naast **Kennis voor een andere AI** op **Exporteren**.
2. **Tekst van berichten** staat standaard uit: je ziet alleen waar elk item vandaan komt en wanneer. Zet dit aan om de tekst toe te voegen.
3. Zet **Privé en Voorzichtig** alleen aan om projecten die alleen voor jou zijn, privégesprekken en Voorzichtige Fleets toe te voegen.
4. Stel eventueel een **Wachtzin** in (minimaal 10 tekens) om het bestand te versleutelen.
5. Klik op **Downloaden**. Je kunt het bestand maar één keer downloaden.

Dit werkt hetzelfde op een gehoste Machine en op je eigen computer.

## Wat erin staat

- Mensen, organisaties en projecten: voor elk één Markdown-pagina, met hun onderlinge relaties.
- Feiten en voorkeuren: wat je Machine over jou en over anderen weet.
- Feiten uit het verleden: wat niet meer geldt (beëindigd, opzijgezet of vervangen), met wat ervoor in de plaats kwam. Feiten die je hebt verwijderd, blijven achterwege.
- Regels, hoe je schrijft en handtekeningen: waar je concepten zich aan houden.
- Skills: je handleidingen, aan en uit.
- Context: teamoverzichten, samenvattingsregels, beloftes en openstaande to-do's.
- Bronnen: waar elk item vandaan komt, met id en datum.

Contacten en to-do's staan ook in spreadsheets (CSV). Bovenaan vertelt een README de AI hoe die alles moet lezen. Upload het zipbestand naar de AI als kennisbestand of project.

## Wat er niet in staat

Wachtwoorden, sleutels en aanmeldgegevens worden nooit opgenomen. Gegevens, instellingen en foto's van teamgenoten blijven er ook buiten. Bekijk [Verplaatsen naar een andere computer](moving.md) als je je hele Machine wilt verplaatsen.

Voor ontwikkelaars: [de bestandsindeling](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
