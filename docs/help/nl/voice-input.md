---
title: Spraakinvoer
area: cards
summary: Praat in plaats van te typen. Wat je zegt, verschijnt in het berichtvak zodat je het kunt controleren. Er wordt niets verstuurd.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
translated: f311b21bb4996eb4
---
## Praat in plaats van te typen

Tik op de microfoon in een berichtvak: in de chat van een to-do, bij **Nieuwe to-do**, **Help** of in het vak om een concept aan te passen. Praat en tik daarna op het vinkje. Of houd de microfoon ingedrukt terwijl je praat en laat los als je klaar bent.

Terwijl de microfoon luistert, zie je in het vak een timer en wat hij tot dan toe heeft verstaan. Tik op het kruisje om te stoppen zonder iets te bewaren. Een opname stopt vanzelf na 2 minuten.

De tekst verschijnt in het vak, op de plek van je cursor. Er wordt niets verstuurd: lees de tekst na, pas aan wat je wilt en verstuur hem zelf.

## Waar je stem naartoe gaat

Kies dit onder **Instellingen** > **Algemeen** bij **Spraakinvoer**. Daar staat kort vermeld welke optie actief is.

- **Automatisch** (de standaardinstelling): OpenAI zet je spraak om in tekst als je Machine OpenAI gebruikt (een OpenAI-sleutel of een ChatGPT-abonnement met audio). Anders doet je Machine dit zelf en verlaat de opname je Machine niet.
- **Op deze Machine**: altijd op je Machine, ook als OpenAI is ingesteld.
- **Met OpenAI**: altijd via OpenAI.

Een opname wordt verwijderd zodra de tekst klaar is.

## Klaarmaken

Om spraak zelf om te zetten in tekst, downloadt je Machine eerst op de achtergrond een spraakmodel (150 tot 500 MB), wanneer het rustig is. In de tussentijd staat er in Instellingen **Klaarmaken (op de achtergrond)**. Dit gebeurt niet als OpenAI wordt gebruikt.

Tot die tijd gebruikt **Automatisch** de spraakherkenning van je browser, als die beschikbaar is. Dat staat onder het vak. Sommige browsers sturen je spraak naar de maker van de browser. Als **Op deze Machine** is gekozen, wacht je opname en staat er in het vak ‘Spraak wordt klaargemaakt…’ met de resterende tijd.

## Instellingen

- **Omgezet naar tekst**: **Automatisch**, **Op deze Machine** of **Met OpenAI**.
- **Nauwkeurigheid** (alleen op je Machine): **Nauwkeuriger** werkt het best voor de meeste talen. **Sneller** is sneller, maar maakt meer fouten. Dit is de standaardinstelling op een Standaard Machine.
- **Taal**: **Herkennen** werkt voor elke taal van de app. Je eigen taal kiezen is iets sneller.

Wil je in plaats daarvan hardop met The Machine praten? Bekijk [Live praten](talk-live.md).

## Als het niet werkt

- **De microfoon is geblokkeerd**: geef deze site toestemming om je microfoon te gebruiken in de instellingen van je browser. In de telefoonapp vind je dit bij de appmachtigingen.
- **Geen microfoon gevonden**: sluit een microfoon aan en probeer het opnieuw.
- **Kan je Machine niet bereiken**: je opname wordt bewaard en uitgeschreven zodra je Machine weer beschikbaar is. Tik op **Nu proberen** om het eerder te proberen.
- **Ik heb niets verstaan**: praat dichter bij de microfoon of iets langer.
