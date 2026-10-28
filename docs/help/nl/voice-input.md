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

## De eerste keer

De eerste keer dat je op de microfoon tikt, zet je Machine spraak klaar. Hij downloadt het spraakmodel één keer, ongeveer 600 MB, en toont "Spraak klaarzetten…" met hoe ver hij is. Dat duurt een paar minuten. Je opname wacht en wordt uitgeschreven zodra het klaar is.

## Waar je stem naartoe gaat

Standaard wordt je opname op je Machine zelf omgezet naar tekst. Ze verlaat hem nooit, en ze wordt gewist zodra de tekst er is. De eigen spraakherkenning van je browser wordt niet gebruikt, omdat sommige browsers je stem dan naar de maker van de browser sturen.

In **Instellingen**, **Algemeen**, onder **Spraakinvoer**, kun je kiezen:

- **Omgezet naar tekst**: **Op deze Machine**, of **Met OpenAI**. OpenAI is sneller op een kleine server, maar je opname gaat naar OpenAI, met je eigen sleutel. Daarvoor is een OpenAI API-sleutel in OpenClaw nodig. Een ChatGPT-login is niet genoeg.
- **Nauwkeurigheid**: **Nauwkeuriger** werkt het best voor de meeste talen en duurt op een kleine server ongeveer even lang als je praatte. **Sneller** is vlugger, maar met meer foute woorden.
- **Taal**: **Herkennen** werkt voor elke taal van de app. Je eigen taal kiezen is iets sneller.

## Als het niet werkt

- **De microfoon is geblokkeerd**: sta de microfoon toe voor deze site in de instellingen van je browser. In de telefoonapp staat dat bij de rechten van de app.
- **Geen microfoon gevonden**: sluit er een aan en probeer het opnieuw.
- **Je Machine is niet bereikbaar**: je opname blijft bewaard. Tik op **Opnieuw proberen** als je Machine terug is.
- **Ik heb niets verstaan**: praat wat dichter bij de microfoon, of langer.
