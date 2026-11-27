---
title: Meldingen
area: settings
summary: Wat je bereikt, waar en wanneer: alleen wat niet kan wachten geeft een melding, de rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: dc56a77907df5da0
---
Minder meldingen, of andere? Kies in **Instellingen** bij **Meldingen** waar je elk soort melding wilt ontvangen:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met deadline vandaag of iets urgents.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een login die voor een taak nodig is of een vraag van Fleet.
- **Herinneringen**: gesnoozede to-do's en antwoorden waarop je wacht die weer terugkomen.
- **Ochtendoverzicht**: één kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat je vandaag hebt gedaan en wat er morgen nog openstaat. Zie hieronder.

Voor elk soort melding kun je **Push** inschakelen (de app op je telefoon of computer), **Telegram** zodra dat is ingesteld en **E-mail** voor een gehoste Machine of een Machine op The Machine Network. Alles staat aan, behalve de overzichten via Telegram.

Je **Werkuren** staan in hetzelfde tabblad: werkdagen, wanneer meldingen mogen binnenkomen, wanneer snoozes terugkomen, de tijden van de overzichten en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Je krijgt alleen een pushmelding, een Telegram-melding of een e-mail voor:

- een to-do met deadline vandaag of die als urgent is gemarkeerd;
- een antwoord waarop iemand wacht, dat als concept klaarstaat om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het tijdstip dat je hebt gekozen.

Al het andere verschijnt stil op het dashboard (en zonder melding in Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen een melding voor iets urgents of met deadline vandaag. Je krijgt maximaal 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, krijg je alleen het ochtendoverzicht, totdat je terug bent.

## Wanneer je een melding krijgt

Er wordt gecontroleerd of je het dashboard echt gebruikt, niet alleen of het openstaat:

- Je gebruikt het dashboard (het staat vooraan en je hebt in de afgelopen 10 minuten geklikt, getypt of gescrold): je krijgt geen melding. Telegram-berichten komen stil binnen. Alleen openen of herladen telt niet.
- Je bent weg (het dashboard staat op de achtergrond, is gesloten of is 10 minuten niet gebruikt): een minuut nadat je bent weggegaan, krijg je een pushmelding, tenzij je terug bent gekomen en die hebt gezien.
- Je hebt 15 minuten later nog niets ontvangen en het kan niet wachten: je krijgt er één e-mail voor, maximaal één per uur. Wat je al hebt gezien of afgehandeld, wordt weggelaten. Elke to-do staat er één keer in, met de huidige status. Op de meeste dagen is het ochtendoverzicht de enige e-mail.
- Ontvangen betekent dat er een melding op je telefoon of in je browser is getoond, of dat Telegram het bericht heeft ontvangen. Een telefoon die uitstaat, offline is of meldingen uit heeft staan, telt niet mee. Telegram telt ook niet mee als je het dashboard gebruikt. Als een melding alleen op een computer is getoond, krijg je wat urgent is of deadline vandaag heeft toch per e-mail: misschien ben je niet bij je computer.
- Heb je geen telefoonapp, browsermeldingen of Telegram? Dan krijg je voor alles hierboven een e-mail.
- Telegram is niet bereikbaar: de pushmelding wordt toch één keer verstuurd en Telegram wordt vanzelf opnieuw geprobeerd.
- Een teamgenoot geeft je een to-do en je Machine kan je niet bereiken via je telefoon of Telegram: als je de to-do na 15 minuten nog niet hebt gezien, krijg je één e-mail met de titel en een link. Met **E-mail** voor **Resultaten en vragen** schakel je dit uit.
- Je Claude-login verloopt binnen 3 dagen of is verlopen: je krijgt één e-mail met **Opnieuw inloggen**, één keer per login. Met **E-mail** voor **Resultaten en vragen** schakel je dit uit.
- Buiten je werkuren: je krijgt niets. Het staat in het ochtendoverzicht.
- Een nieuwe werk-to-do op een vrije dag wacht op het tijdstip van je overzicht op de eerstvolgende werkdag. Bij de to-do staat wanneer je de melding krijgt, bijvoorbeeld: Melding ma 2 nov · 08:30.

Voortgang en wijzigingen geven nooit een melding. Een nieuw resultaat bij een to-do die je nog niet hebt gezien, wordt bijgewerkt zonder nieuwe melding. Bij meerdere meldingen kort na elkaar krijg je er maar één. Het appicoon toont hoeveel to-do's aandacht nodig hebben.

## Knoppen in meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoonapp:

- Nieuwe to-do: **Doe het**, **Snoozen**, **Als gedaan markeren**.
- Concept staat klaar: **Concept openen**, **Snoozen**, **Als gedaan markeren**.
- Resultaat staat klaar: **Openen**, **Als gedaan markeren**, **Snoozen**.
- Je antwoord is nodig, iets zit vast of je moet inloggen: **Beantwoorden**, **Openen** of **Inloggen**, gevolgd door **Snoozen** en **Als gedaan markeren**.
- Herinnering: **Als gedaan markeren**, **Snoozen**, **Openen**.
- Ochtendoverzicht: tik erop om het te openen.

In een browser en op Telegram zie je twee van deze knoppen. Bij vragen van Fleet blijven **Beantwoorden** en **Weigeren** staan.

Via een melding wordt nooit iets verstuurd, betaald of ingediend. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met **Concept openen** zie je de to-do in je lijst met het volledige concept. **Doe het** start het werk alleen bij een nieuwe to-do.

In de telefoonapp moet je eerst ontgrendelen om **Snoozen** of **Als gedaan markeren** te kiezen. In een browser wordt het dashboard geopend, waar de actie wordt uitgevoerd en je **Ongedaan maken** ziet. Een gesnoozede to-do komt na twee uur terug, of de volgende ochtend als het om een herinnering gaat.

E-mails bevatten links om iets te openen (en om te snoozen als je ergens op wacht). Ze openen alleen het dashboard.

Als je op een melding tikt, of op **Openen** in een e-mail of Telegram, zie je de to-do uitgelicht in je lijst, waar die nu ook staat: **Net gedaan**, **Gedaan**, **Komt later terug** of een andere weergave. De chat wordt nooit geopend. Als de pagina de laatste informatie nog niet heeft geladen, wordt de to-do gevolgd zodra dat wel zo is.

## Het ochtendoverzicht

Je krijgt het op werkdagen op het tijdstip van **Ochtendoverzicht**, tenzij er niets te melden is. Valt dat tijdstip vóór **Gesnoozede items komen terug om**, dan wacht het overzicht tot 5 minuten daarna. Zo staan de to-do's die die ochtend terugkomen erin. Met **Voorbeeld** bekijk je het zonder het te versturen. Standaard krijg je een pushmelding en een e-mail, kort genoeg om in één oogopslag te lezen:

- een begroeting met wat vandaag belangrijk is, zoals "Goedemorgen Sam, er staan 2 antwoorden klaar om te versturen" of, bij één to-do, "Goedemorgen Sam, klaar voor je akkoord: het bestelformulier versturen". Alleen to-do's met een concept of resultaat dat je moet goedkeuren tellen als klaar. Een to-do waarvoor eerst je antwoord nodig is, telt niet mee;
- de to-do's die in de begroeting worden genoemd, elk met een link om ze te openen, en wat vandaag een deadline heeft; anders maximaal drie dingen om te doen;
- maximaal vijf to-do's die je zelf hebt toegevoegd en waar jij nog iets mee moet, ongeacht wat in de begroeting wordt genoemd;
- hoeveel andere dingen kunnen wachten en hoelang je er op jouw tempo mee bezig bent, zoals "12 andere dingen kunnen wachten, ongeveer 5 min om af te handelen". To-do's waarop nog je antwoord nodig is, tellen niet mee voor die tijd. Een to-do met deadline vandaag die tot later is gesnoozed, of waaraan The Machine nog werkt, telt pas mee als jij ermee aan de slag moet. Het aantal komt overeen met de to-do's die in je lijst op je wachten;
- je meetings op één regel.

Met **Openen** zie je de to-do uitgelicht in je lijst, ook als die al gedaan of gesnoozed is. Een belofte opent de bijbehorende to-do, of de eigen pagina als die to-do er nog niet is.

De pushmelding bevat hetzelfde, maar zonder links. Tik erop of op de link onderaan de e-mail om dit overzicht opnieuw te bekijken bij **To-do's**.

## Het avondoverzicht

Je krijgt het eenmaal op werkdagen, op het tijdstip dat je hebt ingesteld bij **Werkuren**. Standaard is dat 15 minuten vóór **Tot**, via de kanalen die je in de rij hierboven hebt gekozen. Je krijgt het alleen op een dag waarop je actief was: je hebt het dashboard gebruikt of een keuze gemaakt bij een to-do, in Telegram, in de chat of met je stem. Op een dag waarop je geen to-do hebt afgerond en geen meeting hebt gehad, krijg je het niet.

Het begint met een telling van je dag, zoals "Goedenavond Sam, vandaag 4 to-do's gedaan", gevolgd door een onderdeel **Werk** en een onderdeel **Privé**. Een onderdeel zonder inhoud wordt weggelaten. Een melding over je Machine zelf staat in geen van beide. Elk onderdeel bevat:

- **Vandaag gedaan**: maximaal drie to-do's die jij of je Machine hebt afgerond, gevolgd door "+12 meer" en de meetings van die dag, zoals "+3 meetings: prijsoverleg en nog 2";
- **Open voor morgen** (op vrijdag voor je eerstvolgende werkdag): de eerste meetings en wat een deadline heeft.

Aan het einde staat hoeveel to-do's nog aandacht nodig hebben. Tik op de pushmelding of op de link onderaan de e-mail om het overzicht opnieuw te bekijken, met **Werk kopiëren** en **Privé kopiëren**. Schakel de rij uit om het overzicht niet meer te ontvangen.

## Privacy

Pushmeldingen gaan versleuteld rechtstreeks van je Machine naar je apparaat. E-mail loopt via de mailserver van The Machine en je e-mailprovider. Als [Zorgvuldig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Schakel **E-mail** voor een soort melding uit om die niet per e-mail te ontvangen.

Schakel pushmeldingen voor een apparaat in bij **Dit apparaat**, of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) ontvangt via Apple of Google een gewone regel tekst en vraagt je Machine daarna om de titel en de volgende stap.
