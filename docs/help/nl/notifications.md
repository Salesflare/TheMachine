---
title: Meldingen
area: settings
summary: Wat je bereikt, waar en wanneer: alleen wat niet kan wachten geeft een melding. De rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: febea6f9eb2c331a
---
Wil je minder meldingen of andere meldingen? Kies in **Instellingen** > **Meldingen** waar je elk soort melding wilt ontvangen:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met een deadline vandaag of iets urgents.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een taak waarvoor je moet inloggen of een vraag van Fleet.
- **Herinneringen**: gesnoozede to-do's en antwoorden waarop je wacht die weer terugkomen.
- **Ochtendoverzicht**: één kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat je vandaag hebt afgerond en wat er morgen nog openstaat. Zie hieronder.

Voor elk soort melding kun je meldingen aan- of uitzetten via **Push** (de app op je telefoon of computer), **Telegram** zodra dat is ingesteld en **E-mail** op een gehoste Machine of een Machine op The Machine Network. Alles staat aan, behalve de overzichten via Telegram.

Je **Werkuren** staan in hetzelfde tabblad: werkdagen, wanneer meldingen kunnen binnenkomen, wanneer snoozes terugkomen, de tijden van de overzichten en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Een pushmelding, een Telegram-melding of een e-mail krijg je alleen voor:

- een to-do met een deadline vandaag of die als urgent is gemarkeerd;
- een antwoord waarop iemand wacht, als concept opgesteld en klaar om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het tijdstip dat je hebt gekozen.

Al het andere komt stil op het dashboard (en zonder geluid in Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen een melding voor iets urgents of met een deadline vandaag. Je krijgt maximaal 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, krijg je alleen het ochtendoverzicht totdat je terug bent.

## Wanneer je meldingen krijgt

Er wordt gecontroleerd of je het dashboard echt gebruikt, niet alleen of het openstaat:

- Als je het gebruikt (op de voorgrond en je hebt de afgelopen 10 minuten geklikt, getypt of gescrold): geen meldingen. Telegram komt zonder geluid binnen. Alleen openen of opnieuw laden telt niet.
- Als je weg bent (het dashboard staat op de achtergrond, is gesloten of is 10 minuten inactief): een minuut nadat je weg bent, krijg je een pushmelding, tenzij je terug bent gekomen en die hebt gezien.
- Is de melding 15 minuten later nog niet gezien en kan die niet wachten? Dan krijg je er één e-mail over, maximaal één per uur. Wat je al hebt afgehandeld, wordt weggelaten. Elke to-do staat er één keer in, zoals die er op dat moment uitziet. De meeste dagen is het ochtendoverzicht de enige e-mail.
- Als een teamgenoot je een to-do geeft en je Machine geen telefoon of Telegram heeft om je te bereiken: één e-mail met de titel en een link, na 15 minuten als je de to-do dan nog niet hebt gezien. Zet **E-mail** voor **Resultaten en vragen** uit om dit uit te schakelen.
- Buiten je werkuren krijg je geen meldingen. De to-do staat in het ochtendoverzicht.
- Een nieuwe werkgerelateerde to-do op een vrije dag wacht tot het tijdstip van het overzicht op je volgende werkdag. Bij de to-do staat wanneer je die krijgt, bijvoorbeeld: Melding ma 2 nov · 08:30.

Voortgang en bewerkingen geven nooit een melding. Een nieuw resultaat voor een to-do die je nog niet hebt gezien, werkt de bestaande melding bij zonder een nieuwe melding te sturen. Een reeks meldingen geeft één melding. Het pictogram van de app toont hoeveel to-do's je aandacht nodig hebben.

## Knoppen in meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoonapp:

- Nieuwe to-do: **Doe het**, **Snoozen**, **Als gedaan markeren**.
- Concept klaar: **Concept openen**, **Snoozen**, **Als gedaan markeren**.
- Resultaat klaar: **Openen**, **Als gedaan markeren**, **Snoozen**.
- Vraag, probleem of inlogverzoek: **Beantwoorden**, **Openen** of **Inloggen**, gevolgd door **Snoozen** en **Als gedaan markeren**.
- Herinnering: **Als gedaan markeren**, **Snoozen**, **Openen**.
- Ochtendoverzicht: tik erop om het te openen.

In een browser en in Telegram zie je twee van deze knoppen. Bij Fleet-vragen blijven **Beantwoorden** en **Afwijzen** beschikbaar.

Via een melding wordt niets verstuurd, betaald of ingediend. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met **Concept openen** zie je de to-do in je lijst, inclusief het volledige concept. **Doe het** start alleen het werk aan een nieuwe to-do.

In de telefoonapp moet je eerst ontgrendelen om **Snoozen** of **Als gedaan markeren** te gebruiken. In een browser wordt het dashboard geopend. Daar wordt de actie uitgevoerd en zie je **Ongedaan maken**. Met **Snoozen** komt de to-do over twee uur terug, of de volgende ochtend als het om een herinnering gaat.

E-mails bevatten links om iets te openen (en voor iets waarop je wacht ook een link om het te snoozen). Die openen alleen het dashboard.

Als je op een melding tikt of in een e-mail of Telegram op **Openen** tikt, zie je de to-do uitgelicht in je lijst, waar die nu ook staat: **Net gedaan**, **Gedaan**, **Komt later terug** of een andere weergave. De chat wordt nooit geopend. Als de pagina nog niet is bijgewerkt, volgt die de to-do zodra dat wel het geval is.

## Het ochtendoverzicht

Je krijgt het op werkdagen op het tijdstip van **Ochtendoverzicht**, tenzij er niets te melden is. Als dat tijdstip vóór **Gesnoozede items komen terug om** valt, wacht het overzicht tot 5 minuten daarna, zodat de to-do's die die ochtend terugkomen erin staan. Met **Voorbeeld** kun je het bekijken zonder het te versturen. Standaard krijg je een pushmelding en een e-mail, kort genoeg om in één oogopslag te lezen:

- een begroeting met wat er vandaag belangrijk is, zoals ‘Goedemorgen Sam, 2 antwoorden staan klaar om te versturen’ of, bij één to-do, ‘Goedemorgen Sam, klaar voor je akkoord: het bestelformulier versturen’. Alleen to-do's met een concept of resultaat dat je moet goedkeuren tellen als klaar. Een to-do waarvoor eerst jouw antwoord nodig is, telt niet mee;
- de to-do's die in de begroeting worden geteld, elk met een link om ze te openen, en wat vandaag een deadline heeft. Anders staan er maximaal drie dingen om te doen;
- maximaal vijf to-do's die je zelf hebt toegevoegd en die op jou wachten, ongeacht wat er in de begroeting wordt geteld;
- hoeveel andere to-do's kunnen wachten en hoelang je er op jouw tempo over doet, bijvoorbeeld: ‘Er kunnen nog 12 wachten, ongeveer 5 min om ze af te handelen.’ To-do's die op jouw antwoord wachten, tellen niet mee voor die tijd. Een to-do met een deadline vandaag die tot later is gesnoozed, of waaraan The Machine nog werkt, telt pas mee als die op jou wacht. Het aantal komt overeen met de to-do's die in je lijst op je wachten.
- je meetings op één regel.

Met **Openen** zie je de to-do uitgelicht in je lijst, ook als die gedaan of gesnoozed is. Een belofte opent de bijbehorende to-do, of de eigen pagina als er nog geen to-do is.

De pushmelding bevat hetzelfde, maar zonder links. Tik erop of op de link aan het einde van de e-mail om dit overzicht opnieuw te bekijken in **To-do's**.

## Het avondoverzicht

Je krijgt het één keer op werkdagen, op het tijdstip dat hiervoor is ingesteld bij **Werkuren**. Standaard is dat 15 minuten voor **Tot**, via de manieren die je in de rij hierboven hebt gekozen. Je krijgt het alleen op een dag waarop je actief was: je hebt het dashboard gebruikt of daar, in Telegram, in de chat of met je stem een keuze gemaakt over een to-do. Als je die dag geen to-do hebt afgerond en geen meeting hebt gehad, krijg je het niet.

Het begint met een telling van je dag, zoals ‘Goedenavond Sam, vandaag 4 to-do's gedaan’, gevolgd door een onderdeel **Werk** en een onderdeel **Privé**. Een onderdeel zonder inhoud wordt weggelaten. Beide bevatten:

- **Vandaag gedaan**: maximaal drie to-do's die jij of je Machine hebt afgerond, gevolgd door ‘+12 meer’ en de meetings van die dag, zoals ‘+3 meetings: gesprek over prijzen en nog 2’;
- **Open voor morgen** (op vrijdag: je volgende werkdag): de eerste meetings en wat een deadline heeft.

Tot slot staat er hoeveel to-do's nog op jou wachten. Tik op de pushmelding of op de link aan het einde van de e-mail om het overzicht opnieuw te bekijken, met **Werk kopiëren** en **Privé kopiëren**. Zet de bijbehorende rij uit om het overzicht stop te zetten.

## Privacy

Pushmeldingen gaan rechtstreeks van je Machine naar je apparaat en zijn daarvoor versleuteld. E-mail gaat via de mailserver van The Machine en je e-mailprovider. Als [Zorgvuldig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Zet **E-mail** voor een soort melding uit om die niet via e-mail te krijgen.

Zet pushmeldingen voor een apparaat aan via **Dit apparaat**, of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) stuurt een gewone melding via Apple of Google en vraagt daarna je Machine om de titel en de volgende stap.
