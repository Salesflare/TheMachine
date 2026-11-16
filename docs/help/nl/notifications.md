---
title: Meldingen
area: settings
summary: Wat je bereikt, waar en wanneer: alleen wat niet kan wachten geeft een seintje. De rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: ee3ba81a8441704f
---
Minder meldingen, of andere? Kies in **Instellingen** bij **Meldingen** waar je elk soort melding wilt ontvangen:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met een deadline vandaag of iets dringends.
- **Resultaten en vragen**: een concept dat klaar is om te versturen, een taak waarvoor je moet inloggen of een vraag van Fleet.
- **Herinneringen**: gesnoozede to-do's en antwoorden waar je op wacht, zodra ze terugkomen.
- **Ochtendoverzicht**: één kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat je vandaag hebt gedaan en wat er voor morgen openstaat. Zie hieronder.

Voor elk soort melding kun je **Push** (de app op je telefoon of computer), **Telegram** zodra dat is ingesteld en **E-mail** op een gehoste Machine of een Machine op The Machine Network in- of uitschakelen. Alles staat aan, behalve de overzichten op Telegram.

Je **Werkuren** vind je in hetzelfde tabblad: werkdagen, wanneer meldingen mogen worden verstuurd, wanneer gesnoozede items terugkomen, de tijden van je overzichten en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Een pushmelding, Telegram-seintje of e-mail wordt alleen verstuurd voor:

- een to-do met een deadline vandaag of met het label dringend;
- een antwoord waar iemand op wacht, dat klaarstaat om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het tijdstip dat je hebt gekozen.

Al het andere komt stil op het dashboard (en zonder geluid op Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen een seintje voor dringende to-do's of to-do's met een deadline vandaag. Je krijgt maximaal 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, krijg je alleen het ochtendoverzicht, totdat je terug bent.

## Wanneer je een melding krijgt

Er wordt gekeken of je het dashboard echt gebruikt, niet alleen of het openstaat:

- In gebruik (op de voorgrond, en je hebt de afgelopen 10 minuten geklikt, getypt of gescrold): je krijgt geen seintje. Telegram-meldingen komen stil binnen.
- Niet aanwezig (op de achtergrond, gesloten of 10 minuten inactief): een minuut nadat je weg bent, krijg je een pushmelding, tenzij je terugkomt en de melding ziet.
- Nog steeds niet gezien na 15 minuten, en het kan niet wachten: je krijgt er één e-mail over, maximaal één per uur. Wat je al hebt afgehandeld, wordt weggelaten. Op de meeste dagen is het ochtendoverzicht de enige e-mail.
- Een teamgenoot wijst je een to-do toe en je Machine kan je niet bereiken via telefoon of Telegram: als je de to-do na 15 minuten nog niet hebt gezien, krijg je één e-mail met de titel en een link. Schakel **E-mail** voor **Resultaten en vragen** uit om dit uit te zetten.
- Buiten je werkuren: je krijgt niets. De melding staat in het ochtendoverzicht.
- Een nieuwe werk-to-do op een vrije dag wacht tot het tijdstip van het overzicht op je eerstvolgende werkdag. Bij de to-do staat wanneer je de melding krijgt, bijvoorbeeld Melding ma 2 nov · 08:30.

Voortgang en bewerkingen geven nooit een melding. Een nieuw resultaat bij een to-do die je nog niet hebt gezien, wordt bijgewerkt zonder nieuwe melding. Bij een reeks meldingen krijg je één seintje. Het app-icoon toont hoeveel to-do's je aandacht nodig hebben.

## Knoppen in meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoonapp:

- Nieuwe to-do: **Doe het**, **Snooze**, **Markeer als gedaan**.
- Concept klaar: **Concept openen**, **Snooze**, **Markeer als gedaan**.
- Resultaat klaar: **Openen**, **Markeer als gedaan**, **Snooze**.
- Vraag, vastgelopen taak of inlogverzoek: **Beantwoorden**, **Openen** of **Inloggen**, en daarna **Snooze** en **Markeer als gedaan**.
- Herinnering: **Markeer als gedaan**, **Snooze**, **Openen**.
- Ochtendoverzicht: tik erop om het te openen.

In een browser en op Telegram zie je twee van deze knoppen. Bij Fleet-vragen blijven **Eenmalig beantwoorden** en **Weigeren** beschikbaar.

Via een melding wordt niets verstuurd, betaald of ingediend. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met **Concept openen** zie je de to-do in je lijst, inclusief het volledige concept. **Doe het** start alleen het werk aan een nieuwe to-do.

In de telefoonapp moet je eerst ontgrendelen om **Snooze** of **Markeer als gedaan** te gebruiken. In een browser wordt het dashboard geopend. Daar wordt de actie uitgevoerd en zie je de optie Ongedaan maken. Met **Snooze** komt de to-do over twee uur terug, of de volgende ochtend als het om een herinnering gaat.

E-mails bevatten links om items te openen (en een link om te snoozen bij items waar je op wacht). Ze openen alleen het dashboard.

Als je op een melding tikt, of op **Openen** in een e-mail of op Telegram, zie je de to-do gemarkeerd in je lijst, waar die nu ook staat: **Net gedaan**, **Gedaan**, **Komt later terug** of een ander overzicht. De chat wordt nooit geopend. Als de pagina nog niet is bijgewerkt, wordt de to-do gevolgd zodra dat wel zo is.

## Het ochtendoverzicht

Het overzicht komt op werkdagen op het tijdstip dat je hebt ingesteld bij **Ochtendoverzicht**, tenzij er niets te melden is. Als dat tijdstip valt vóór **Gesnoozede items komen terug om**, wacht het overzicht tot 5 minuten daarna. Zo staan de to-do's die die ochtend terugkomen erin. Met **Voorbeeld** kun je het bekijken zonder het te versturen. Standaard krijg je het als pushmelding en per e-mail. Het is kort genoeg om in één oogopslag te lezen:

- een begroeting met wat vandaag belangrijk is, zoals "Goedemorgen Sam, er staan 2 antwoorden klaar om te versturen" of, als het om één to-do gaat, "Goedemorgen Sam, klaar voor je akkoord: het bestelformulier versturen";
- de to-do's die in de begroeting worden geteld, elk met een link om ze te openen, en wat vandaag een deadline heeft; anders maximaal drie dingen om te doen;
- maximaal vijf to-do's die je zelf hebt toegevoegd en waarop je actie moet ondernemen, ongeacht wat er in de begroeting wordt geteld;
- hoeveel andere dingen kunnen wachten en hoelang ze op jouw tempo duren, zoals "12 andere kunnen wachten, ongeveer 5 min om ze af te handelen." To-do's die op jouw antwoord wachten, tellen niet mee voor die tijd. Een gesnoozede to-do met een deadline vandaag telt pas mee zodra die terugkomt.
- je afspraken, op één regel.

Met **Openen** zie je de to-do gemarkeerd in je lijst, ook als die al gedaan of gesnoozed is. Een belofte opent de bijbehorende to-do, of de eigen pagina als die nog geen to-do heeft.

De pushmelding bevat dezelfde tekst, maar zonder links. Tik erop of op de link onderaan de e-mail om het overzicht opnieuw te lezen bij **To-do's**.

## Het avondoverzicht

Het overzicht komt op werkdagen één keer op het tijdstip dat je hebt ingesteld bij **Werkuren**. Standaard is dat 15 minuten voor **Tot**, via de manieren die je hierboven in de rij hebt gekozen. Als je die dag geen to-do hebt afgerond en geen afspraak hebt gehad, krijg je geen overzicht. Het begint met een samenvatting van de dag, zoals "Goedenavond Sam, vandaag 4 to-do's gedaan", gevolgd door een onderdeel **Werk** en een onderdeel **Privé**. Een onderdeel zonder inhoud wordt weggelaten. Beide onderdelen bevatten:

- **Vandaag gedaan**: maximaal drie to-do's die jij of je Machine heeft afgerond, gevolgd door "+12 meer" en de afspraken van die dag, zoals "+3 afspraken: gesprek over prijzen en 2 meer";
- **Open voor morgen** (op vrijdag is dat je eerstvolgende werkdag): de eerste afspraken en wat een deadline heeft.

Aan het einde staat hoeveel to-do's nog op jou wachten. Tik op de pushmelding of op de link onderaan de e-mail om het overzicht opnieuw te lezen. Daar vind je ook **Werk kopiëren** en **Privé kopiëren**. Zet de rij uit om het overzicht stop te zetten.

## Privacy

Pushmeldingen gaan rechtstreeks van je Machine naar je apparaat en zijn daarvoor versleuteld. E-mail loopt via de mailserver van The Machine en je e-mailprovider. Als [Voorzichtig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Schakel **E-mail** voor een soort melding uit om die niet meer per e-mail te ontvangen.

Schakel pushmeldingen voor een apparaat in bij **Dit apparaat**, of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) stuurt eerst een gewone melding via Apple of Google en vraagt daarna je Machine om de titel en de volgende stap.
