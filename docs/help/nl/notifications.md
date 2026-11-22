---
title: Meldingen
area: settings
summary: Wat je te horen krijgt, waar en wanneer: alleen wat niet kan wachten geeft een melding. De rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4a782ad03270e7b0
---
Minder meldingen, of andere? Kies in **Instellingen** > **Meldingen** waar je elke soort wilt ontvangen:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met een deadline vandaag of iets urgents.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een taak waarvoor je moet inloggen, of een vraag van Fleet.
- **Herinneringen**: gesnoozede to-do's en antwoorden waarop je wacht, zodra ze terugkomen.
- **Ochtendoverzicht**: een kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat je vandaag hebt gedaan en wat er morgen nog openstaat. Zie hieronder.

Voor elke soort kun je **Push** inschakelen (de app op je telefoon of computer), **Telegram** zodra dat is ingesteld, en **E-mail** op een gehoste Machine of een Machine op The Machine Network. Alles staat aan, behalve de overzichten via Telegram.

Je **Werkuren** staan in hetzelfde tabblad: werkdagen, wanneer meldingen kunnen binnenkomen, wanneer gesnoozede items terugkomen, de tijden van de overzichten en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Je krijgt alleen een pushmelding, een melding via Telegram of een e-mail voor:

- een to-do met een deadline vandaag of met de markering urgent;
- een antwoord waarop iemand wacht, als concept opgesteld en klaar om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het tijdstip dat je hebt gekozen.

Al het andere komt stil op het dashboard te staan (en zonder melding in Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen een melding voor iets urgents of met een deadline vandaag. Je krijgt maximaal 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, krijg je alleen het ochtendoverzicht totdat je terug bent.

## Wanneer je een melding krijgt

Er wordt gecontroleerd of je het dashboard echt gebruikt, niet alleen of het openstaat:

- Je gebruikt het (het staat op de voorgrond en je hebt de afgelopen 10 minuten geklikt, getypt of gescrold): je krijgt geen melding. Telegram-meldingen komen stil binnen. Alleen openen of herladen telt niet.
- Je bent weg (het dashboard staat op de achtergrond, is gesloten of is 10 minuten inactief): een minuut nadat je bent weggegaan, krijg je een pushmelding, tenzij je terug bent gekomen en die hebt gezien.
- Na 15 minuten heb je de melding nog steeds niet gezien en kan die niet wachten: je krijgt er één e-mail over, maximaal één per uur. Wat je al hebt afgehandeld, wordt weggelaten. Op de meeste dagen is het ochtendoverzicht de enige e-mail.
- Een teamgenoot geeft je een to-do en je Machine kan je niet bereiken via telefoon of Telegram: als je de to-do na 15 minuten nog niet hebt gezien, krijg je één e-mail met de titel en een link. Schakel **E-mail** voor **Resultaten en vragen** uit om dit uit te zetten.
- Buiten je werkuren: je krijgt niets. Het ochtendoverzicht bevat het.
- Een nieuwe werk-to-do op een vrije dag wacht tot het tijdstip van het overzicht op je eerstvolgende werkdag. Bij de to-do staat wanneer je die krijgt, bijvoorbeeld: Melding ma 2 nov · 08:30.

Voortgang en wijzigingen geven nooit meldingen. Een nieuwer resultaat voor een to-do die je nog niet hebt gezien, wordt bijgewerkt zonder nieuwe melding. Een reeks meldingen geeft één melding. Het appicoon toont hoeveel to-do's je aandacht nodig hebben.

## Knoppen bij meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoonapp:

- Nieuwe to-do: **Doe het**, **Snoozen**, **Markeren als gedaan**.
- Concept klaar: **Concept openen**, **Snoozen**, **Markeren als gedaan**.
- Resultaat klaar: **Openen**, **Markeren als gedaan**, **Snoozen**.
- Vraag, vastgelopen taak of inlogverzoek: **Beantwoorden**, **Openen** of **Inloggen**, daarna **Snoozen** en **Markeren als gedaan**.
- Herinnering: **Markeren als gedaan**, **Snoozen**, **Openen**.
- Ochtendoverzicht: tik erop om het te openen.

In een browser en op Telegram zie je twee knoppen. Bij Fleet-vragen blijven **Beantwoorden** en **Weigeren** beschikbaar.

Je verstuurt, betaalt of verzendt niets vanuit een melding. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met **Concept openen** zie je de to-do in je lijst, met het volledige concept erbij. **Doe het** start alleen het werk aan een nieuwe to-do.

In de telefoonapp moet je eerst ontgrendelen om **Snoozen** of **Markeren als gedaan** te gebruiken. In een browser openen deze knoppen het dashboard, waar de actie wordt uitgevoerd en je **Ongedaan maken** ziet. Met snoozen komt de to-do over twee uur terug, of morgenochtend als het om een herinnering gaat.

E-mails bevatten links om iets te openen (en om te snoozen als je ergens op wacht). Ze openen alleen het dashboard.

Als je op een melding tikt, of op **Openen** in een e-mail of op Telegram, zie je de to-do uitgelicht in je lijst, waar die nu ook staat: **Net gedaan**, **Gedaan**, **Komt later terug** of een andere weergave. De chat wordt nooit geopend. Als de pagina nog niet was bijgewerkt, volgt die de to-do zodra dat wel zo is.

## Het ochtendoverzicht

Je krijgt het op werkdagen op het tijdstip van **Ochtendoverzicht**, tenzij er niets te melden is. Valt dat tijdstip vóór **Gesnoozede items komen terug om**, dan wacht het overzicht tot 5 minuten daarna, zodat de to-do's die die ochtend terugkomen erin staan. Met **Voorbeeld** bekijk je het zonder het te versturen. Standaard krijg je een pushmelding en een e-mail. Het overzicht is kort genoeg om snel te lezen:

- een begroeting met wat vandaag belangrijk is, zoals "Goedemorgen Sam, 2 antwoorden staan klaar om te versturen" of, bij één to-do, "Goedemorgen Sam, klaar voor je akkoord: het bestelformulier versturen". Alleen to-do's met een concept of resultaat dat je moet goedkeuren, tellen als klaar. Een to-do waarvoor je eerst antwoord moet geven, telt niet mee;
- de to-do's die in de begroeting worden genoemd, elk met een link om ze te openen, en wat vandaag een deadline heeft. Als er niets met een deadline is, staan er maximaal drie dingen om te doen;
- maximaal vijf to-do's die je zelf hebt toegevoegd en die op jou wachten, ongeacht wat de begroeting noemt;
- hoeveel andere dingen kunnen wachten en hoelang ze duren in jouw tempo, bijvoorbeeld: "Er kunnen nog 12 dingen wachten, ongeveer 5 min om af te handelen." To-do's die op je antwoord wachten, tellen niet mee voor die tijd. Een to-do met een deadline vandaag die tot later is gesnoozed, of waaraan The Machine nog werkt, telt pas mee als die op jou wacht. Het aantal komt overeen met de to-do's die in je lijst op je wachten.
- je afspraken, op één regel.

Met **Openen** zie je die to-do uitgelicht in je lijst, ook als die is afgerond of gesnoozed. Een belofte opent de bijbehorende to-do, of de eigen pagina als er nog geen to-do is.

De pushmelding bevat dezelfde informatie, zonder links. Tik erop, of op de link onderaan de e-mail, om dit overzicht opnieuw te lezen in **To-do's**.

## Het avondoverzicht

Je krijgt het één keer op werkdagen, op het tijdstip dat je hebt ingesteld bij **Werkuren**. Standaard is dat 15 minuten vóór **Tot**, via de manieren die je in de rij hierboven hebt gekozen. Je krijgt het alleen op een dag waarop je aanwezig was: je gebruikte het dashboard of maakte daar, op Telegram, in de chat of met je stem een keuze bij een to-do. Op een dag waarop je geen to-do hebt afgerond en geen afspraak hebt gehad, krijg je het niet.

Het begint met een telling van je dag, zoals "Goedenavond Sam, vandaag 4 to-do's gedaan", gevolgd door een deel **Werk** en een deel **Privé**. Een deel zonder inhoud wordt weggelaten. Beide delen bevatten:

- **Vandaag gedaan**: maximaal drie to-do's die jij of je Machine heeft afgerond, gevolgd door "+12 meer" en de afspraken van die dag, zoals "+3 afspraken: prijsbespreking en nog 2";
- **Open voor morgen** (op vrijdag: je eerstvolgende werkdag): de eerste afspraken en wat een deadline heeft.

Het eindigt met het aantal to-do's dat nog op jou wacht. Tik op de pushmelding of op de link onderaan de e-mail om het opnieuw te lezen, met **Werk kopiëren** en **Privé kopiëren**. Zet de rij uit om het niet meer te krijgen.

## Privacy

Pushmeldingen gaan rechtstreeks van je Machine naar je apparaat en zijn daarvoor versleuteld. E-mail gaat via de mailserver van The Machine en je e-mailprovider. Als [Zorgvuldig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Schakel **E-mail** uit voor een soort meldingen om die niet meer via e-mail te krijgen.

Schakel pushmeldingen voor een apparaat in via **Dit apparaat**, of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) stuurt via Apple of Google een gewone regel tekst en vraagt daarna je Machine om de titel en volgende stap.
