---
title: Meldingen
area: settings
summary: Wat je ontvangt, waar en wanneer: alleen wat niet kan wachten laat van zich horen. De rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 334224e0b479ef47
---
Wil je minder meldingen of andere meldingen? Kies in **Instellingen** > **Meldingen** waar je elk soort melding ontvangt:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met een deadline vandaag of iets dringends.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een taak waarvoor je moet inloggen of een vraag van Fleet.
- **Herinneringen**: to-do's die je hebt gesnoozed en antwoorden waarop je wacht, komen weer terug.
- **Ochtendoverzicht**: één kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat je vandaag hebt gedaan en wat er voor morgen openstaat. Zie hieronder.

Voor elk soort melding kun je **Push** (de app op je telefoon of computer), **Telegram** zodra dat is ingesteld, en **E-mail** inschakelen. **E-mail** is beschikbaar op een gehoste Machine of een Machine op The Machine Network. Alles staat aan, behalve de overzichten op Telegram.

Je **Werkuren** vind je in hetzelfde tabblad: werkdagen, wanneer meldingen mogen binnenkomen, wanneer gesnoozede items terugkomen, de tijden van je overzichten en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Je krijgt alleen een pushmelding, een melding op Telegram of een e-mail voor:

- een to-do met een deadline vandaag of met de markering dringend;
- een antwoord waarop iemand wacht, dat klaarstaat om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het tijdstip dat je hebt gekozen.

Al het andere verschijnt stil op het dashboard (en zonder geluid op Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen een melding voor iets dringends of met een deadline vandaag. Je krijgt maximaal 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, ontvang je alleen het ochtendoverzicht totdat je terug bent.

## Wanneer je een melding krijgt

The Machine controleert of je het dashboard echt gebruikt, niet alleen of het openstaat:

- In gebruik (op de voorgrond, en je hebt de afgelopen 10 minuten geklikt, getypt of gescrold): je krijgt geen melding. Telegram-meldingen komen zonder geluid binnen.
- Niet actief (op de achtergrond, gesloten of 10 minuten inactief): een pushmelding komt een minuut nadat je bent weggegaan, tenzij je terugkomt en de melding ziet.
- Nog steeds niet bekeken na 15 minuten en het kan niet wachten: je krijgt er één e-mail voor, maximaal één per uur. Wat je al hebt afgehandeld, wordt weggelaten. Op de meeste dagen is het ochtendoverzicht de enige e-mail.
- Een teamgenoot wijst je een to-do toe en je Machine kan je niet bereiken via je telefoon of Telegram: je krijgt één e-mail met de titel en een link, 15 minuten later als je de to-do dan nog niet hebt gezien. Schakel **E-mail** voor **Resultaten en vragen** uit om dit te stoppen.
- Buiten je werkuren: je krijgt niets. Het staat in het ochtendoverzicht.
- Een nieuwe werk-to-do op een vrije dag wacht tot het tijdstip van het overzicht op je volgende werkdag. Bij de to-do staat wanneer je de melding krijgt, bijvoorbeeld Melding ma 2 nov · 08:30.

Je krijgt geen meldingen over voortgang en bewerkingen. Een nieuw resultaat bij een to-do die je nog niet hebt gezien, wordt bijgewerkt zonder nieuwe melding. Een reeks meldingen geeft één melding. Het app-icoon toont hoeveel to-do's je aandacht nodig hebben.

## Knoppen in meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoonapp:

- Nieuwe to-do: **Doe het**, **Snooze**, **Markeer als gedaan**.
- Concept klaar: **Concept openen**, **Snooze**, **Markeer als gedaan**.
- Resultaat klaar: **Openen**, **Markeer als gedaan**, **Snooze**.
- Vraag, probleem of inlogverzoek: **Beantwoorden**, **Openen** of **Inloggen**, daarna **Snooze** en **Markeer als gedaan**.
- Herinnering: **Markeer als gedaan**, **Snooze**, **Openen**.
- Ochtendoverzicht: tik erop om het te openen.

In een browser en op Telegram zie je twee van deze knoppen. Bij vragen van Fleet blijven **Eenmalig beantwoorden** en **Weigeren** staan.

Vanuit een melding wordt er niets verstuurd, betaald of ingediend. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met **Concept openen** zie je de to-do in je lijst, met het volledige concept erbij. **Doe het** start alleen het werk aan een nieuwe to-do.

In de telefoonapp vragen **Snooze** en **Markeer als gedaan** je eerst om te ontgrendelen. In een browser openen ze het dashboard, waar de actie wordt uitgevoerd en je **Ongedaan maken** ziet. Met **Snooze** komt de to-do over twee uur terug, of de volgende ochtend bij een herinnering.

E-mails bevatten links om iets te **Openen** (en **Snooze** voor items waarop je wacht). Ze openen alleen het dashboard.

Als je op een melding tikt of in een e-mail of op Telegram op **Openen** tikt, zie je de to-do uitgelicht in je lijst. Is de to-do gedaan, gesnoozed of staat die in een andere weergave, dan wordt de chat geopend.

## Het ochtendoverzicht

Je ontvangt het op werkdagen op het tijdstip van je **Ochtendoverzicht**, tenzij er niets te melden is. Valt dat tijdstip vóór **Gesnoozede items komen terug om**, dan wacht het overzicht tot 5 minuten daarna. Zo staan de to-do's die die ochtend terugkomen erin. Met **Voorbeeld** bekijk je het zonder het te versturen. Standaard krijg je het als pushmelding en e-mail. Het is kort genoeg om in één oogopslag te lezen:

- een begroeting met wat vandaag belangrijk is, zoals "Goedemorgen Sam, 2 antwoorden staan klaar om te versturen" of, bij één to-do, "Goedemorgen Sam, klaar voor je akkoord: het bestelformulier versturen";
- de to-do's waarop de begroeting is gebaseerd, elk met een link om ze te openen, en wat er vandaag een deadline heeft. Zijn er geen deadlines, dan staan er maximaal drie dingen die je kunt doen;
- hoeveel andere dingen nog kunnen wachten en hoelang ze duren in jouw tempo, zoals "12 andere dingen kunnen wachten, ongeveer 5 min om af te handelen." To-do's die op jouw antwoord wachten, tellen niet mee voor die tijd;
- je afspraken op één regel.

Met **Openen** zie je die to-do uitgelicht in je lijst. Is die gedaan, gesnoozed of staat die in een andere weergave, dan wordt de chat geopend. Een belofte opent de bijbehorende to-do, of de eigen pagina als die nog geen to-do heeft.

De pushmelding bevat hetzelfde, maar zonder links. Tik erop of op de link aan het einde van de e-mail om dit overzicht opnieuw te bekijken in **To-do's**.

## Het avondoverzicht

Je ontvangt het eenmaal op werkdagen, op het tijdstip dat je ervoor hebt ingesteld bij **Werkuren**. Standaard is dat 15 minuten vóór **Tot**. Je ontvangt het via de kanalen die je in de rij hierboven hebt gekozen. Op een dag waarop geen to-do is afgerond en geen afspraak heeft plaatsgevonden, krijg je geen overzicht. Het begint met een telling van je dag, zoals "Goedenavond Sam, vandaag 4 to-do's gedaan". Daarna volgen een deel **Werk** en een deel **Privé**. Een deel zonder inhoud wordt weggelaten. Elk deel bevat:

- **Vandaag gedaan**: maximaal drie to-do's die jij of je Machine heeft afgerond, gevolgd door "+12 meer" en de afspraken van die dag, bijvoorbeeld "+3 afspraken: prijsbespreking en nog 2";
- **Open voor morgen** (op vrijdag voor je volgende werkdag): de eerste afspraken en wat een deadline heeft.

Het eindigt met het aantal to-do's dat nog je aandacht nodig heeft. Tik op de pushmelding of op de link aan het einde van de e-mail om het opnieuw te bekijken, met **Werk kopiëren** en **Privé kopiëren**. Schakel de rij uit om het overzicht niet meer te ontvangen.

## Privacy

**Push** wordt rechtstreeks en versleuteld van je Machine naar je apparaat verstuurd. E-mail gaat via de mailserver van The Machine en je e-mailprovider. Als [Voorzichtig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Schakel **E-mail** voor een soort melding uit om die niet meer via e-mail te ontvangen.

Schakel pushmeldingen voor een apparaat in bij **Dit apparaat**, of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) ontvangt een gewone regel via Apple of Google en vraagt daarna je Machine om de titel en de volgende stap.
