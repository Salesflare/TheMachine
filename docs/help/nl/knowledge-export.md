---
title: Kennis voor een andere AI
area: settings
summary: Neem wat je Machine geleerd heeft mee naar elke andere AI, als gewone Markdown-, JSONL- en CSV-bestanden.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
---
Alles wat je Machine leert, is van jou. Neem het mee naar een andere AI, of bewaar het, ook als je The Machine niet meer gebruikt.

## Exporteren

1. Druk in **Instellingen** › **Algemeen** op **Exporteren** naast **Kennis voor een andere AI**.
2. Laat **Tekst van berichten** uit om alleen te exporteren waar alles vandaan kwam, en wanneer. Zet het aan om de tekst toe te voegen.
3. **Privé en Voorzichtig** blijft uit, tenzij je ook projecten voor alleen jou, privégesprekken en Voorzichtige Fleets erin wilt.
4. Stel eventueel een **Wachtzin** van minstens 10 tekens in om het bestand te versleutelen.
5. Druk op **Downloaden**. Het bestand wordt op je Machine gemaakt en kan één keer gedownload worden.

Op een gehoste Machine werkt het net zo, vanuit de Instellingen van je Machine zelf. Op je eigen computer maakt `assistant export-knowledge` hetzelfde bestand.

## Wat erin zit

- Mensen, organisaties en projecten: elk een Markdown-pagina, met hoe ze met elkaar verbonden zijn.
- Feiten en voorkeuren: wat je Machine weet, over jou en over hen.
- Vroegere feiten: wat niet meer geldt (afgelopen, opzijgezet of vervangen), met wat het verving. Feiten die je verwijderde, blijven erbuiten.
- Regels, hoe je schrijft en handtekeningen: wat je concepten volgen.
- Skills: je handleidingen, aan en uit.
- Context: teambriefings, samenvattingsregels, beloftes en open to-do's.
- Bronnen: waar alles vandaan kwam, met id en datum.

Records zijn JSONL, contacten en to-do's ook CSV. Een README.md bovenaan legt de indeling uit en vertelt een AI hoe het te gebruiken. Geef de map, of de zip, aan de AI als kennisbestand of project.

## Wat erbuiten blijft

Wachtwoorden, sleutels en logins gaan er nooit in. Iets dat op een sleutel lijkt, wordt vervangen. Gegevens van teamgenoten en andere Machines, instellingen en foto's blijven er ook buiten. Voor een volledige kopie om je Machine te verhuizen, zie [Verhuizen naar je eigen computer](moving.md).

Het formaat is open en heeft versies: zie [het schema](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
