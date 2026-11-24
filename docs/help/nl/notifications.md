---
title: Meldingen
area: settings
summary: Wat je bereikt, waar en wanneer: alleen wat niet kan wachten geeft een melding, de rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3c469ec1032f6bea
---
Minder meldingen, of andere? Kies in **Instellingen**, **Meldingen** waar je elk soort melding wilt ontvangen:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met deadline vandaag of iets dringends.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een login die een taak nodig heeft of een vraag van Fleet.
- **Herinneringen**: gesnoozede to-do's en antwoorden waarop je wacht die terugkomen.
- **Ochtendoverzicht**: één kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat je vandaag hebt gedaan en wat morgen nog openstaat. Zie hieronder.

Voor elk soort melding kun je kiezen voor **Push** (de app op je telefoon of computer), **Telegram** zodra dat is ingesteld en **E-mail** op een gehoste Machine of een Machine op The Machine Network. Alles staat aan, behalve de overzichten op Telegram.

Je **Werkuren** staan in hetzelfde tabblad: werkdagen, wanneer meldingen kunnen binnenkomen, wanneer gesnoozede items terugkomen, de tijden van de overzichten en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Je krijgt alleen een pushmelding, een melding op Telegram of een e-mail voor:

- een to-do met deadline vandaag of met de markering dringend;
- een antwoord waarop iemand wacht, als concept opgesteld en klaar om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het tijdstip dat je hebt gekozen.

Al het andere komt stil op het dashboard terecht (en zonder geluid op Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen een melding voor iets dringends of met deadline vandaag. Je krijgt hoogstens 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, krijg je alleen het ochtendoverzicht totdat je terug bent.

## Wanneer je een melding krijgt

Er wordt gekeken of je het dashboard echt gebruikt, niet alleen of het openstaat:

- Als je het gebruikt (het staat op de voorgrond en je hebt in de afgelopen 10 minuten geklikt, getypt of gescrold), krijg je geen melding. Telegram-berichten komen zonder geluid binnen. Alleen openen of opnieuw laden telt niet.
- Als je weg bent (het dashboard staat op de achtergrond, is gesloten of is 10 minuten inactief), krijg je een minuut nadat je bent weggegaan een pushmelding, tenzij je terugkwam en die al zag.
- Als je 15 minuten later nog niets hebt ontvangen en het niet kan wachten, krijg je één e-mail, hoogstens één per uur. Wat je al hebt gezien of afgehandeld, wordt weggelaten. Elke to-do staat er één keer in, met de huidige status. Op de meeste dagen is het ochtendoverzicht de enige e-mail.
- Iets is ontvangen als er een melding op je telefoon of in je browser is getoond, of als Telegram het bericht heeft ontvangen. Een telefoon die uitstaat, offline is of meldingen heeft uitgeschakeld, telt niet mee. Telegram telt ook niet mee zolang je het dashboard gebruikt. Als de melding alleen op een computer is getoond, wordt iets dringends of met deadline vandaag alsnog per e-mail verstuurd: misschien ben je niet achter je computer.
- Geen telefoon-app, browsermeldingen of Telegram? Dan krijg je voor alles hierboven een e-mail.
- Telegram is niet bereikbaar: de pushmelding wordt alsnog één keer verstuurd en Telegram wordt vanzelf opnieuw geprobeerd.
- Een teamgenoot geeft je een to-do en je Machine kan je niet bereiken via je telefoon of Telegram: als je de to-do na 15 minuten nog niet hebt gezien, krijg je één e-mail met de titel en een link. Zet **E-mail** bij **Resultaten en vragen** uit om dit te stoppen.
- Buiten je werkuren krijg je geen meldingen. Het ochtendoverzicht bevat deze informatie.
- Een nieuwe werk-to-do op een vrije dag wacht tot het tijdstip van het overzicht op je volgende werkdag. Bij de to-do staat wanneer je die ontvangt, bijvoorbeeld Melding ma 2 nov · 08:30.

Voortgang en wijzigingen geven nooit een melding. Een nieuwer resultaat voor een to-do die je nog niet hebt gezien, wordt bijgewerkt zonder nieuwe melding. Meerdere meldingen kort na elkaar geven samen één melding. Het app-icoon laat zien hoeveel to-do's je aandacht nodig hebben.

## Knoppen in meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoon-app:

- Nieuwe to-do: **Doe het**, **Snoozen**, **Als gedaan markeren**.
- Concept klaar: **Concept openen**, **Snoozen**, **Als gedaan markeren**.
- Resultaat klaar: **Openen**, **Als gedaan markeren**, **Snoozen**.
- Je antwoord nodig, vastgelopen of een login nodig: **Antwoorden**, **Openen** of **Inloggen**, gevolgd door **Snoozen** en **Als gedaan markeren**.
- Herinnering: **Als gedaan markeren**, **Snoozen**, **Openen**.
- Ochtendoverzicht: tik erop om het te openen.

In een browser en op Telegram zie je twee van deze knoppen. Bij vragen van Fleet blijven **Antwoorden** en **Afwijzen** staan.

Er wordt niets verstuurd, betaald of ingediend vanuit een melding. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met **Concept openen** zie je de to-do in je lijst, met het volledige concept. **Doe het** start alleen het werk aan een nieuwe to-do.

In de telefoon-app moet je eerst ontgrendelen om **Snoozen** of **Als gedaan markeren** te gebruiken. In een browser openen ze het dashboard. Daar wordt de actie uitgevoerd en zie je **Ongedaan maken**. Door te snoozen komt de to-do over twee uur terug, of de volgende ochtend als het om een herinnering gaat.

E-mails bevatten links om items te openen (en een link om te snoozen voor items waarop je wacht). De links openen alleen het dashboard.

Als je op een melding tikt of in een e-mail of op Telegram op **Openen** tikt, zie je de to-do uitgelicht in je lijst, waar die nu ook staat: **Net gedaan**, **Gedaan**, **Komt later terug** of een ander overzicht. De chat wordt nooit geopend. Als de pagina nog niet is bijgewerkt, wordt de to-do gevolgd zodra dat wel zo is.

## Het ochtendoverzicht

Het komt op werkdagen op het tijdstip van **Ochtendoverzicht**, tenzij er niets te melden is. Valt dat tijdstip vóór **Gesnoozede items komen terug om**, dan wacht het overzicht tot 5 minuten daarna. Zo staan de to-do's die die ochtend terugkomen erin. Met **Voorbeeld** bekijk je het overzicht zonder het te versturen. Standaard krijg je een pushmelding en een e-mail, kort genoeg om snel te lezen:

- een begroeting met wat vandaag belangrijk is, zoals "Goedemorgen Sam, 2 antwoorden staan klaar om te versturen" of, bij één to-do, "Goedemorgen Sam, klaar voor je akkoord: het bestelformulier versturen". Alleen to-do's met een concept of resultaat dat je moet goedkeuren tellen als klaar. Een to-do waarvoor je eerst antwoord moet geven, telt niet mee;
- de to-do's die in de begroeting zijn meegeteld, elk met een link om ze te openen, en wat vandaag deadline heeft; anders hoogstens drie dingen om te doen;
- to-do's die je zelf hebt toegevoegd en waarop jij moet wachten, tot vijf stuks, ongeacht wat er in de begroeting is meegeteld;
- hoeveel andere to-do's kunnen wachten en hoelang je er in jouw tempo over doet, bijvoorbeeld "12 andere kunnen wachten, het kost ongeveer 5 min om ze af te handelen". To-do's waarop je eerst moet antwoorden tellen niet mee voor de tijd. Een to-do met deadline vandaag die je tot later hebt gesnoozed, of waaraan The Machine nog werkt, telt pas mee als jij aan zet bent. Het aantal komt overeen met de to-do's waarop je lijst op jou wacht.
- je meetings op één regel.

Met **Openen** zie je de to-do uitgelicht in je lijst, ook als die gedaan of gesnoozed is. Een belofte opent de bijbehorende to-do, of de eigen pagina als die nog geen to-do heeft.

De pushmelding bevat dezelfde informatie, zonder links. Tik erop of op de link onderaan de e-mail om dit overzicht opnieuw te lezen in **To-do's**.

## Het avondoverzicht

Het komt op werkdagen eenmaal op het tijdstip dat je ervoor hebt ingesteld bij **Werkuren**, standaard 15 minuten vóór **Tot**, via de manieren die je in de rij hierboven hebt gekozen. Je krijgt het alleen op een dag waarop je actief was: je hebt het dashboard gebruikt of een keuze gemaakt bij een to-do, op Telegram, in de chat of met je stem. Op een dag waarop je geen to-do hebt afgerond en geen meeting hebt gehad, krijg je het niet.

Het begint met een telling van je dag, zoals "Goedenavond Sam, vandaag 4 to-do's gedaan", gevolgd door een onderdeel **Werk** en een onderdeel **Privé**. Een onderdeel zonder inhoud wordt weggelaten. Een melding over je Machine zelf staat in geen van beide. Elk onderdeel bevat:

- **Vandaag gedaan**: hoogstens drie to-do's die jij of je Machine heeft afgerond, gevolgd door "+12 meer" en de meetings van die dag, zoals "+3 meetings: prijsgesprek en 2 andere";
- **Open voor morgen** (op vrijdag voor je volgende werkdag): de eerste meetings en wat deadline heeft.

Het overzicht eindigt met het aantal to-do's dat nog op jou wacht. Tik op de pushmelding of op de link onderaan de e-mail om het opnieuw te lezen, met **Werk kopiëren** en **Privé kopiëren**. Zet de rij voor dit overzicht uit om het te stoppen.

## Privacy

Pushmeldingen gaan vanaf je Machine rechtstreeks en versleuteld naar je apparaat. E-mail gaat via de mailserver van The Machine en je e-mailprovider. Als [Voorzichtig](security-levels.md) to-do-tekst in meldingen verbergt, bevatten e-mails alleen aantallen. Zet **E-mail** voor een soort melding uit om die uit e-mail te houden.

Zet pushmeldingen voor een apparaat aan bij **Dit apparaat** of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) stuurt een gewone regel via Apple of Google en vraagt daarna je Machine om de titel en de volgende stap.
