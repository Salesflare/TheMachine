---
title: Spraakinvoer
area: cards
summary: Praat in plaats van te typen. Wat je zegt komt in het berichtvak, zodat je het kunt nakijken. Er wordt niets verstuurd.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
---
## Praten in plaats van typen

Tik op de microfoon in een berichtvak: de chat van een to-do, **Nieuwe to-do**, **Help**, of het vak om een concept aan te passen. Praat, en tik dan op het vinkje. Of hou de microfoon ingedrukt terwijl je praat en laat los als je klaar bent.

Terwijl hij luistert, toont het vak een timer. Tik op het kruisje om te stoppen zonder iets te houden. Een opname duurt hoogstens 2 minuten; na 2 minuten stopt hij vanzelf en schrijft hij uit wat je zei.

Wat je zei komt in het vak, waar je cursor stond. Er wordt niets verstuurd: lees het, pas aan wat je wilt en verstuur het zelf.

## Waar je stem naartoe gaat

In **Instellingen**, **Algemeen**, onder **Spraakinvoer**, zegt één korte regel welke er gebruikt wordt.

- **Automatisch** (standaard): als OpenAI is ingesteld in OpenClaw, zet OpenAI je opname om naar tekst. Dat is een API-sleutel, of een ChatGPT-login als je abonnement audio toelaat. Zonder OpenAI wordt ze op je Machine zelf omgezet naar tekst en verlaat ze hem nooit.
- **Op deze Machine**: altijd op je Machine, ook als OpenAI is ingesteld.
- **Met OpenAI**: altijd OpenAI.

Een opname wordt gewist zodra de tekst terug is.

## Klaarzetten

Om spraak zelf om te zetten naar tekst heeft je Machine een spraakmodel nodig, 150 tot 500 MB. Hij downloadt het op de achtergrond, met lage prioriteit, zodra hij is ingesteld, zijn eerste review klaar is en het een tijdje rustig is geweest. Intussen toont Instellingen **Wordt klaargezet (op de achtergrond)**. Als OpenAI gebruikt wordt, doet hij dat nooit.

Tot hij klaar is, gebruikt **Automatisch** de eigen spraakherkenning van je browser, als je browser die heeft, en zegt dat onder het vak. Sommige browsers sturen dat naar hun maker. Met **Op deze Machine** gekozen wacht je opname, en toont het vak "Spraak klaarzetten…" met de resterende tijd.

## Instellingen

- **Omgezet naar tekst**: **Automatisch**, **Op deze Machine** of **Met OpenAI**.
- **Nauwkeurigheid** (alleen op je Machine): **Nauwkeuriger** werkt het best voor de meeste talen. **Sneller** is vlugger, maar met meer foute woorden. Op een Standard-server, die minder geheugen heeft, staat **Sneller** standaard aan.
- **Taal**: **Herkennen** werkt voor elke taal van de app. Je eigen taal kiezen is iets sneller.

Wil je liever hardop met The Machine praten, zie dan [Live praten](talk-live.md).

## Als het niet werkt

- **De microfoon is geblokkeerd**: sta de microfoon toe voor deze site in de instellingen van je browser. In de telefoonapp staat dat bij de rechten van de app.
- **Geen microfoon gevonden**: sluit er een aan en probeer het opnieuw.
- **Je Machine is niet bereikbaar**: je opname blijft bewaard en wordt uitgeschreven zodra je Machine terug is. Wil je het eerder proberen, tik dan op **Nu proberen**.
- **Ik heb niets verstaan**: praat wat dichter bij de microfoon, of langer.
