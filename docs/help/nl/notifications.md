---
title: Meldingen
area: settings
summary: Wat je bereikt, waar en wanneer: alleen wat niet kan wachten geeft een melding. De rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4a782ad03270e7b0
---
Minder meldingen, of andere? Kies in **Instellingen**, **Meldingen** waar je elk soort melding ontvangt:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met deadline vandaag of iets urgents.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een login die een taak nodig heeft, een vraag van Fleet.
- **Herinneringen**: to-do's die gesnoozed zijn en antwoorden waar je op wacht, die weer terugkomen.
- **Ochtendoverzicht**: één kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat er vandaag is gedaan en wat er morgen nog openstaat. Zie hieronder.

Voor elk soort melding kun je **Push** (de app op je telefoon of computer), **Telegram** zodra dat is ingesteld en **E-mail** op een gehoste Machine of een Machine op The Machine Network in- of uitschakelen. Alles staat aan, behalve de overzichten op Telegram.

Je **Werkuren** vind je in hetzelfde tabblad: werkdagen, wanneer meldingen verstuurd mogen worden, wanneer gesnoozede items terugkomen, de tijden van de overzichten en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Een pushmelding, een Telegram-melding of een e-mail wordt alleen verstuurd voor:

- een to-do met deadline vandaag of gemarkeerd als urgent;
- een antwoord waar iemand op wacht, als concept opgesteld en klaar om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het tijdstip dat je hebt gekozen.

Al het andere verschijnt stil op het dashboard (en zonder geluid in Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen meldingen voor urgente items of items met deadline vandaag. Je krijgt maximaal 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, krijg je alleen het ochtendoverzicht totdat je terug bent.

## Wanneer je een melding krijgt

Er wordt gecontroleerd of je het dashboard echt gebruikt, niet alleen of het openstaat:

- Je gebruikt het dashboard (het staat vooraan en je hebt de afgelopen 10 minuten geklikt, getypt of gescrold): er klinkt geen melding. Telegram-meldingen komen zonder geluid binnen. Alleen openen of opnieuw laden telt niet.
- Je bent weg (het dashboard staat op de achtergrond, is gesloten of is 10 minuten inactief): een pushmelding wordt een minuut nadat je bent weggegaan verstuurd, tenzij je terugkomt en de melding ziet.
- Als de melding 15 minuten later nog niet is gezien en niet kan wachten, krijg je er één e-mail over, met maximaal één e-mail per uur. Wat je al hebt afgehandeld, wordt weggelaten. Op de meeste dagen is het ochtendoverzicht de enige e-mail.
- Als een teamgenoot een to-do aan je overdraagt en je Machine geen telefoon of Telegram heeft om je te bereiken, krijg je één e-mail met de titel en een link, 15 minuten later als je de melding dan nog niet hebt gezien. Schakel **E-mail** voor **Resultaten en vragen** uit om dit te stoppen.
- Buiten je werkuren krijg je niets. Het ochtendoverzicht bevat de melding.
- Een nieuwe werk-to-do op een vrije dag wacht tot het tijdstip van het overzicht op je volgende werkdag. Bij de to-do staat wanneer je de melding krijgt, bijvoorbeeld Melding ma 2 nov · 08:30.

Voortgang en bewerkingen geven nooit een melding. Een nieuw resultaat voor een to-do die je nog niet hebt gezien, werkt de melding bij zonder een nieuwe melding te sturen. Een reeks meldingen geeft één melding. Het app-icoon laat zien hoeveel to-do's je aandacht nodig hebben.

## Knoppen in meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoonapp:

- Nieuwe to-do: **Doe het**, **Snoozen**, **Als gedaan markeren**.
- Concept klaar: **Concept openen**, **Snoozen**, **Als gedaan markeren**.
- Resultaat klaar: **Openen**, **Als gedaan markeren**, **Snoozen**.
- Vraag, vastgelopen of inlogverzoek: **Antwoorden**, **Openen** of **Inloggen**, gevolgd door **Snoozen** en **Als gedaan markeren**.
- Herinnering: **Als gedaan markeren**, **Snoozen**, **Openen**.
- Ochtendoverzicht: tik erop om het te openen.

Een browser en Telegram tonen er twee. Bij Fleet-vragen blijven **Eén keer antwoorden** en **Weigeren** beschikbaar.

Vanuit een melding wordt niets verstuurd, betaald of ingediend. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met **Concept openen** zie je de to-do in je lijst, met het volledige concept. **Doe het** start alleen het werk aan een nieuwe to-do.

In de telefoonapp vragen **Snoozen** en **Als gedaan markeren** je eerst om te ontgrendelen. In een browser openen ze het dashboard. Daar wordt de actie uitgevoerd en kun je die ongedaan maken. Met **Snoozen** komt de to-do over twee uur terug, of de volgende ochtend als het om een herinnering gaat.

E-mails bevatten links om items te openen (en een link om items waar je op wacht te snoozen). De links openen alleen het dashboard.

Als je op een melding tikt, of op **Openen** in een e-mail of op Telegram, wordt de to-do gemarkeerd weergegeven in je lijst, waar hij op dat moment ook staat: **Net gedaan**, **Gedaan**, **Komt later terug** of een andere weergave. De chat wordt nooit geopend. Als de pagina nog niet was bijgewerkt, volgt de melding de to-do zodra dat wel zo is.

## Het ochtendoverzicht

Je krijgt het op werkdagen op het tijdstip van **Ochtendoverzicht**, tenzij er niets te melden is. Valt dat tijdstip vóór **Gesnoozede items komen terug om**, dan wacht het overzicht tot 5 minuten daarna, zodat de to-do's die die ochtend terugkomen erin staan. Met **Voorbeeld** bekijk je het overzicht zonder het te versturen. Standaard krijg je een pushmelding en een e-mail, kort genoeg om in één oogopslag te lezen:

- een begroeting met wat vandaag belangrijk is, zoals "Goedemorgen Sam, er staan 2 antwoorden klaar om te versturen" of, bij één to-do, "Goedemorgen Sam, wacht op je akkoord: het bestelformulier versturen". Alleen to-do's met een concept of resultaat om goed te keuren tellen als klaargezet; een to-do die eerst je antwoord nodig heeft, telt niet mee;
- de to-do's waar de begroeting naar verwijst, elk met een link om de to-do te openen, en wat er vandaag een deadline heeft; anders staan er maximaal drie dingen om te doen;
- to-do's die je zelf hebt toegevoegd en die op jou wachten, maximaal vijf, ongeacht waar de begroeting naar verwijst;
- hoeveel andere items nog kunnen wachten en hoelang je er in jouw tempo over doet, bijvoorbeeld "Er kunnen nog 12 items wachten, je bent ongeveer 5 min bezig om ze af te handelen." To-do's die op jouw antwoord wachten, tellen niet mee voor die tijd. Een to-do met deadline vandaag die je tot later hebt gesnoozed, of waaraan The Machine nog werkt, telt pas mee als die op jou wacht. Het aantal komt overeen met de to-do's die in je lijst op je wachten.
- je meetings, op één regel.

Met **Openen** wordt de to-do gemarkeerd weergegeven in je lijst, ook als die is afgerond of gesnoozed. Een belofte opent de bijbehorende to-do, of de eigen pagina als er nog geen to-do is.

De pushmelding bevat dezelfde informatie, maar zonder links. Tik erop, of op de link onderaan de e-mail, om dit overzicht opnieuw te lezen bij **To-do's**.

## Het avondoverzicht

Je krijgt het eenmaal op werkdagen, op het tijdstip dat je hebt ingesteld bij **Werkuren**. Standaard is dat 15 minuten voor **Tot**, via de manieren die je in de rij hierboven hebt gekozen. Je krijgt het alleen op een dag dat je er was: je hebt het dashboard gebruikt, of een keuze gemaakt bij een to-do, daar, in Telegram, in de chat of met je stem. Op een dag waarop geen to-do is afgerond en geen meeting heeft plaatsgevonden, krijg je geen overzicht.

Het begint met een telling van je dag, zoals "Goedenavond Sam, vandaag zijn 4 to-do's afgerond", gevolgd door een onderdeel **Werk** en een onderdeel **Privé**. Een onderdeel zonder items wordt weggelaten. Beide bevatten:

- **Vandaag gedaan**: maximaal drie to-do's die jij of je Machine hebben afgerond, gevolgd door "+12 meer" en de meetings van die dag, zoals "+3 meetings: Prijsgesprek en 2 andere";
- **Open voor morgen** (op vrijdag: je volgende werkdag): de eerstvolgende meetings en wat er een deadline heeft.

Het overzicht eindigt met het aantal to-do's dat nog op jou wacht. Tik op de pushmelding of op de link onderaan de e-mail om het opnieuw te lezen, met **Werk kopiëren** en **Privé kopiëren**. Schakel de rij uit om het overzicht stop te zetten.

## Privacy

Pushmeldingen gaan rechtstreeks en versleuteld van je Machine naar je apparaat. E-mail gaat via de mailserver van The Machine en je e-mailprovider. Als [Voorzichtig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Schakel **E-mail** voor een bepaald soort melding uit om die meldingen niet meer per e-mail te ontvangen.

Schakel pushmeldingen voor een apparaat in bij **Dit apparaat**, of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) krijgt een gewone melding via Apple of Google en vraagt daarna je Machine om de titel en de volgende stap.
