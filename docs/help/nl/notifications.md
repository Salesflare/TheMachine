---
title: Meldingen
area: settings
summary: Wat je krijgt, waar en wanneer: alleen wat niet kan wachten geeft een seintje, de rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4f777fac22dba7c0
---
Minder meldingen, of andere? Kies in **Instellingen** > **Meldingen** waar je elke soort ontvangt:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met een deadline vandaag of iets urgents.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een aanmelding die nodig is voor een taak, een vraag van Fleet.
- **Herinneringen**: gesnoozede to-do's en antwoorden waarop je wacht.
- **Ochtendoverzicht**: één kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat er vandaag is gedaan en wat er morgen nog openstaat. Zie hieronder.

Voor elke soort kun je meldingen aan- of uitzetten via **Push** (de app op je telefoon of computer), **Telegram** als je dat hebt ingesteld, en **E-mail** op een gehoste Machine of een Machine op The Machine Network. Alles staat aan, behalve de overzichten via Telegram.

Je **Werkuren** vind je in hetzelfde tabblad: werkdagen, wanneer meldingen mogen worden verstuurd, wanneer snoozes terugkomen, de tijden van de overzichten en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Je krijgt alleen een pushmelding, een Telegram-seintje of een e-mail voor:

- een to-do met een deadline vandaag of die als urgent is gemarkeerd;
- een antwoord waarop iemand wacht, als concept klaargezet om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het tijdstip dat je hebt gekozen.

Al het andere komt stil op het dashboard te staan (en zonder geluid in Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen een seintje voor iets urgents of iets met een deadline vandaag. Je krijgt maximaal 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, krijg je alleen het ochtendoverzicht, totdat je terug bent.

## Wanneer je meldingen krijgt

The Machine kijkt of je het dashboard echt gebruikt, niet alleen of het openstaat:

- In gebruik (op de voorgrond en je hebt in de afgelopen 10 minuten geklikt, getypt of gescrold): je krijgt geen seintjes. Telegram-meldingen komen zonder geluid binnen. Alleen openen of vernieuwen telt niet.
- Niet in gebruik (op de achtergrond, gesloten of 10 minuten inactief): een minuut nadat je bent weggegaan, krijg je een pushmelding, tenzij je bent teruggekomen en die hebt gezien.
- Na 15 minuten nog steeds niet gezien en het kan niet wachten: je krijgt er een e-mail over, maximaal één per uur. Wat je al hebt afgehandeld, wordt weggelaten. Op de meeste dagen is het ochtendoverzicht de enige e-mail.
- Een teamgenoot geeft je een to-do en je Machine kan je niet bereiken via telefoon of Telegram: als je de melding na 15 minuten nog niet hebt gezien, krijg je één e-mail met de titel en een link. Zet **E-mail** voor **Resultaten en vragen** uit om dit uit te schakelen.
- Buiten je werkuren: je krijgt niets. Het staat in het ochtendoverzicht.
- Een nieuwe werkto-do op een vrije dag wacht tot het tijdstip van het overzicht op je eerstvolgende werkdag. Bij de to-do staat wanneer die bij je aankomt, bijvoorbeeld: Melding ma 2 nov · 08:30.

Voortgang en wijzigingen geven nooit een melding. Komt er een nieuw resultaat bij een to-do die je nog niet hebt gezien, dan wordt die bijgewerkt zonder nieuwe melding. Een reeks meldingen geeft één seintje. Het appicoon laat zien hoeveel to-do's je aandacht nodig hebben.

## Knoppen in meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoonapp:

- Nieuwe to-do: **Doe het**, **Snooze**, **Markeer als gedaan**.
- Concept klaar: **Concept openen**, **Snooze**, **Markeer als gedaan**.
- Resultaat klaar: **Openen**, **Markeer als gedaan**, **Snooze**.
- Vraag, probleem of aanmelding: **Beantwoorden**, **Openen** of **Inloggen**, daarna **Snooze** en **Markeer als gedaan**.
- Herinnering: **Markeer als gedaan**, **Snooze**, **Openen**.
- Ochtendoverzicht: tik erop om het te openen.

In een browser en Telegram zie je twee van deze knoppen. Bij Fleet-vragen blijven **Beantwoorden** en **Afwijzen** beschikbaar.

Via een melding wordt niets verstuurd, betaald of ingediend. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met **Concept openen** zie je de to-do in je lijst, inclusief het volledige concept. **Doe het** start alleen het werk aan een nieuwe to-do.

In de telefoonapp moet je eerst ontgrendelen voordat je **Snooze** of **Markeer als gedaan** kunt kiezen. In een browser openen deze knoppen het dashboard, waar de actie wordt uitgevoerd en je **Ongedaan maken** ziet. Met **Snooze** komt de to-do over twee uur terug, of de volgende ochtend als het om een herinnering gaat.

E-mails hebben links om iets te openen (en een link voor **Snooze** bij items waarop je wacht). Ze openen alleen het dashboard.

Als je op een melding tikt, of op **Openen** in een e-mail of Telegram, zie je de to-do gemarkeerd in je lijst, waar die nu ook staat: **Net gedaan**, **Gedaan**, **Komt later terug** of een ander overzicht. De chat wordt nooit geopend. Als de pagina nog niet is bijgewerkt, volgt die de to-do zodra dat wel zo is.

## Het ochtendoverzicht

Je krijgt het op werkdagen op het tijdstip van **Ochtendoverzicht**, tenzij er niets te melden is. Valt dat tijdstip vóór **Gesnoozede items komen terug om**, dan wacht het overzicht tot 5 minuten daarna. Zo staan de to-do's die die ochtend terugkomen erin. Met **Voorbeeld** bekijk je het overzicht zonder het te versturen. Standaard krijg je een pushmelding en een e-mail. Het overzicht is kort genoeg om in één oogopslag te lezen:

- een begroeting met wat er vandaag belangrijk is, zoals ‘Goedemorgen Sam, er staan 2 antwoorden klaar om te versturen’ of, bij één to-do, ‘Goedemorgen Sam, klaar voor je akkoord: het bestelformulier versturen’;
- de to-do's waar de begroeting over gaat, elk met een link om ze te openen, en wat vandaag een deadline heeft; anders maximaal drie dingen om te doen;
- maximaal vijf to-do's die je zelf hebt toegevoegd en waar jij nog iets mee moet, ongeacht waar de begroeting over gaat;
- hoeveel andere dingen kunnen wachten en hoelang je er op jouw tempo over doet, zoals ‘Nog 12 dingen kunnen wachten, ongeveer 5 min om ze af te handelen.’ To-do's die op jouw antwoord wachten, tellen niet mee voor die tijd. Een gesnoozede to-do met een deadline vandaag telt pas mee zodra die terugkomt.
- je afspraken in één regel.

Met **Openen** zie je de to-do gemarkeerd in je lijst, ook als die is gedaan of gesnoozed. Een belofte opent de bijbehorende to-do, of de eigen pagina als die nog geen to-do heeft.

De pushmelding bevat dezelfde tekst, maar zonder links. Tik erop, of op de link onderaan de e-mail, om dit overzicht opnieuw te lezen in **To-do's**.

## Het avondoverzicht

Je krijgt het eenmaal op werkdagen, op het tijdstip dat je hebt ingesteld bij **Werkuren**. Standaard is dat 15 minuten vóór **Tot**, via de manieren die je hierboven hebt gekozen. Op een dag waarop geen to-do is afgerond en geen afspraak heeft plaatsgevonden, krijg je geen overzicht. Het begint met een telling van je dag, zoals ‘Goedenavond Sam, vandaag 4 to-do's gedaan’, gevolgd door een onderdeel **Werk** en een onderdeel **Privé**. Onderdelen zonder inhoud worden weggelaten. Elk onderdeel bevat:

- **Vandaag gedaan**: maximaal drie to-do's die jij of je Machine heeft afgerond, gevolgd door ‘+12 meer’ en de afspraken van die dag, zoals ‘+3 afspraken: prijsgesprek en 2 meer’;
- **Open voor morgen** (op vrijdag: je eerstvolgende werkdag): de eerste afspraken en wat een deadline heeft.

Aan het eind staat hoeveel to-do's nog op jou wachten. Tik op de pushmelding of op de link onderaan de e-mail om het overzicht opnieuw te lezen, met **Werk kopiëren** en **Privé kopiëren**. Zet de bijbehorende rij uit om het overzicht stop te zetten.

## Privacy

Pushmeldingen gaan rechtstreeks van je Machine naar je apparaat en zijn daarvoor versleuteld. E-mail gaat via de mailserver van The Machine en je e-mailprovider. Als [Zorgvuldig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Zet **E-mail** voor een soort melding uit om die niet meer via e-mail te ontvangen.

Zet pushmeldingen voor een apparaat aan via **Dit apparaat**, of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) stuurt een gewone regel via Apple of Google en vraagt daarna je Machine om de titel en de volgende stap.
