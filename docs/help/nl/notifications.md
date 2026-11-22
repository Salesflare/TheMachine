---
title: Meldingen
area: settings
summary: Wat je ontvangt, waar en wanneer: alleen wat niet kan wachten geeft een melding. De rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: aab523e3a774400b
---
Wil je minder meldingen of andere meldingen? Kies in **Instellingen** bij **Meldingen** waar je elk type wilt ontvangen:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met een deadline vandaag of iets urgents.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een taak waarvoor je moet inloggen of een vraag van Fleet.
- **Herinneringen**: gesnoozede to-do's en antwoorden waarop je wacht, zodra ze terugkomen.
- **Ochtendoverzicht**: één kort overzicht van je dag. Meer lees je hieronder.
- **Avondoverzicht**: wat je vandaag hebt afgerond en wat er morgen nog openstaat. Meer lees je hieronder.

Voor elk type kun je **Push** (de app op je telefoon of computer), **Telegram** zodra je dat hebt ingesteld, en **E-mail** op een gehoste Machine of een Machine op The Machine Network aan- of uitzetten. Alles staat aan, behalve de overzichten op Telegram.

Je **Werkuren** staan in hetzelfde tabblad: werkdagen, wanneer meldingen mogen worden verstuurd, wanneer gesnoozede items terugkomen, de tijden van de overzichten en je tijdzone. Bekijk [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Je krijgt alleen een pushmelding, een Telegram-melding of een e-mail voor:

- een to-do met een deadline vandaag of met het label urgent;
- een antwoord waarop iemand wacht, als concept opgesteld en klaar om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het tijdstip dat je hebt gekozen.

Al het andere verschijnt stil op het dashboard (en zonder melding in Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen een melding voor iets urgents of met een deadline vandaag. Je krijgt maximaal 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, ontvang je alleen het ochtendoverzicht totdat je terug bent.

## Wanneer je een melding krijgt

The Machine kijkt of je het dashboard echt gebruikt, niet alleen of het openstaat:

- Als je het gebruikt (het staat vooraan en je hebt de afgelopen 10 minuten geklikt, getypt of gescrold), krijg je geen melding. Telegram-berichten komen stil binnen. Alleen het dashboard openen of herladen telt niet.
- Ben je weg (het dashboard staat op de achtergrond, is gesloten of is 10 minuten inactief), dan krijg je een minuut nadat je bent weggegaan een pushmelding, tenzij je terug bent gekomen en die al hebt gezien.
- Is de melding 15 minuten later nog steeds niet gezien en kan die niet wachten? Dan krijg je er één e-mail over, maximaal één per uur. Wat je al hebt afgehandeld, wordt weggelaten. De meeste dagen is het ochtendoverzicht de enige e-mail.
- Geeft een teamgenoot je een to-do en kan je Machine je niet bereiken via je telefoon of Telegram? Dan krijg je één e-mail met de titel en een link, 15 minuten later als je de to-do nog niet hebt gezien. Zet **E-mail** voor **Resultaten en vragen** uit om dit te stoppen.
- Buiten je werkuren krijg je geen meldingen. Het ochtendoverzicht bevat de informatie.
- Een nieuwe werk-to-do op een vrije dag wacht tot de tijd van het overzicht op je volgende werkdag. Bij de to-do staat wanneer je die ontvangt, bijvoorbeeld Melding ma 2 nov · 08:30.

Voortgang en wijzigingen geven nooit een melding. Een nieuw resultaat bij een to-do die je nog niet hebt gezien, werkt de bestaande melding bij zonder een nieuwe te sturen. Een reeks meldingen geeft één melding. Het appicoon laat zien hoeveel to-do's aandacht nodig hebben.

## Knoppen in meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoonapp:

- Nieuwe to-do: Doe het, Snoozen, Markeren als gedaan.
- Concept klaar: Concept openen, Snoozen, Markeren als gedaan.
- Resultaat klaar: Openen, Markeren als gedaan, Snoozen.
- Vraag, vastgelopen taak of verzoek om in te loggen: Beantwoorden, Openen of Inloggen, daarna Snoozen en Markeren als gedaan.
- Herinnering: Markeren als gedaan, Snoozen, Openen.
- Ochtendoverzicht: tik erop om het te openen.

In een browser en op Telegram zie je er twee. Bij Fleet-vragen blijven Beantwoorden en Afwijzen staan.

Er wordt niets verstuurd, betaald of ingediend vanuit een melding. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met Concept openen zie je de to-do in je lijst, inclusief het volledige concept. Doe het start alleen het werk aan een nieuwe to-do.

In de telefoonapp moet je eerst ontgrendelen om op Snoozen of Markeren als gedaan te tikken. In een browser wordt het dashboard geopend, waar de actie wordt uitgevoerd en je Ongedaan maken ziet. Met Snoozen komt de to-do over twee uur terug, of de volgende ochtend als het om een herinnering gaat.

E-mails bevatten Openen-links (en Snoozen voor zaken waarop je wacht). Ze openen alleen het dashboard.

Als je op een melding tikt, of op Openen in een e-mail of op Telegram, zie je de to-do gemarkeerd in je lijst, waar die op dat moment ook staat: **Net gedaan**, **Gedaan**, **Komt later terug** of een ander overzicht. De chat wordt nooit geopend. Als de pagina nog niet is bijgewerkt, wordt de to-do gevolgd zodra dat wel zo is.

## Het ochtendoverzicht

Je ontvangt het op werkdagen op het tijdstip voor **Ochtendoverzicht**, tenzij er niets te melden is. Valt dat tijdstip vóór **Gesnoozede items komen terug om**, dan wacht het overzicht tot 5 minuten daarna, zodat de to-do's die die ochtend terugkomen erin staan. Met **Voorbeeld** bekijk je het zonder het te versturen. Standaard krijg je een pushmelding en een e-mail. Het overzicht is kort genoeg om in één oogopslag te lezen:

- een begroeting met wat vandaag belangrijk is, zoals "Goedemorgen Sam, er staan 2 antwoorden klaar om te versturen" of, bij één to-do, "Goedemorgen Sam, wacht op jouw akkoord: Bestelformulier versturen";
- de to-do's waarop de begroeting slaat, elk met een Openen-link, en wat vandaag een deadline heeft; anders maximaal drie dingen om te doen;
- maximaal vijf to-do's die je zelf hebt toegevoegd en waarvoor jij aan zet bent, ongeacht waarop de begroeting slaat;
- hoeveel andere zaken nog kunnen wachten en hoe lang ze op jouw tempo duren, zoals "12 andere zaken kunnen wachten, ongeveer 5 min om af te handelen." To-do's die op jouw antwoord wachten, tellen niet mee voor die tijd. Een to-do met een deadline vandaag die je tot later hebt gesnoozed, of waaraan The Machine nog werkt, telt pas mee als jij aan zet bent. Het aantal komt overeen met de to-do's waarop je lijst wacht.
- je afspraken op één regel.

Met Openen zie je de to-do gemarkeerd in je lijst, ook als die is afgerond of gesnoozed. Een belofte opent de bijbehorende to-do, of de eigen pagina als die nog geen to-do heeft.

De pushmelding bevat hetzelfde overzicht, maar zonder links. Tik erop of op de link aan het einde van de e-mail om het overzicht opnieuw te bekijken bij **To-do's**.

## Het avondoverzicht

Je ontvangt het één keer op werkdagen, op het tijdstip dat je hebt ingesteld bij **Werkuren**. Standaard is dat 15 minuten vóór **Tot**, via de kanalen die je in de rij hierboven hebt gekozen. Je ontvangt het alleen op een dag waarop je aanwezig was: je hebt het dashboard gebruikt of een keuze gemaakt bij een to-do op het dashboard, in Telegram, in de chat of met je stem. Krijg je die dag geen to-do af en houd je geen afspraak, dan ontvang je geen overzicht.

Het begint met een samenvatting van je dag, zoals "Goedenavond Sam, vandaag 4 to-do's gedaan", gevolgd door een onderdeel **Werk** en een onderdeel **Privé**. Een leeg onderdeel wordt weggelaten. Elk onderdeel bevat:

- **Vandaag gedaan**: maximaal drie to-do's die jij of je Machine heeft afgerond, gevolgd door "+12 andere" en de afspraken van die dag, zoals "+3 afspraken: Prijsgesprek en nog 2";
- **Open voor morgen** (op vrijdag voor je eerstvolgende werkdag): de eerste afspraken en wat een deadline heeft.

Aan het einde staat hoeveel to-do's nog op jou wachten. Tik op de pushmelding of op de link aan het einde van de e-mail om het overzicht opnieuw te bekijken, met **Werk kopiëren** en **Privé kopiëren**. Zet de rij van het overzicht uit om het niet meer te ontvangen.

## Privacy

Pushmeldingen gaan rechtstreeks van je Machine naar je apparaat en zijn daarvoor versleuteld. E-mail gaat via de mailserver van The Machine en je e-mailprovider. Als [Voorzichtig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Zet **E-mail** voor een type uit om daarvoor geen e-mail meer te krijgen.

Zet pushmeldingen voor een apparaat aan bij **Dit apparaat**, of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) stuurt via Apple of Google een gewone melding en vraagt daarna je Machine om de titel en de volgende stap.
