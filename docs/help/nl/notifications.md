---
title: Meldingen
area: settings
summary: Wat je bereikt, waar en wanneer: alleen wat niet kan wachten geeft een melding. De rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: bdb4ecec9446aa5e
---
Wil je minder meldingen of andere meldingen? Kies in **Instellingen** bij **Meldingen** waar je elk soort melding wilt ontvangen:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met een deadline vandaag of iets urgents.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een login die een taak nodig heeft of een vraag over Fleet.
- **Herinneringen**: to-do's die gesnoozed zijn en antwoorden waarop je wacht en die terugkomen.
- **Ochtendoverzicht**: één kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat je vandaag hebt gedaan en wat er morgen nog openstaat. Zie hieronder.

Voor elk soort melding kun je meldingen aan- of uitzetten via **Push** (de app op je telefoon of computer), **Telegram** zodra dat is ingesteld en **E-mail** op een gehoste Machine of een Machine op The Machine Network. Alles staat aan, behalve de overzichten op Telegram.

Je **Werkuren** staan in hetzelfde tabblad: werkdagen, wanneer meldingen mogen worden verstuurd, wanneer gesnoozede items terugkomen, de tijden van de overzichten en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Je krijgt alleen een pushmelding, een Telegram-melding of een e-mail voor:

- een to-do met een deadline vandaag of die als urgent is gemarkeerd;
- een antwoord waarop iemand wacht, dat als concept klaarstaat om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het door jou gekozen tijdstip.

Al het andere verschijnt stil op het dashboard (en zonder geluid in Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen een melding voor iets urgents of met een deadline vandaag. Je krijgt maximaal 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, krijg je alleen het ochtendoverzicht totdat je terug bent.

## Wanneer je een melding krijgt

Er wordt gecontroleerd of je het dashboard echt gebruikt, niet alleen of het openstaat:

- Als je het gebruikt (het staat voor je en je hebt in de afgelopen 10 minuten geklikt, getypt of gescrold), krijg je geen melding. Telegram-meldingen komen zonder geluid binnen. Alleen openen of opnieuw laden telt niet.
- Als je weg bent (het dashboard staat op de achtergrond, is gesloten of is al 10 minuten inactief), krijg je een minuut nadat je weg bent een pushmelding, tenzij je terugkomt en die al ziet.
- Staat de melding 15 minuten later nog ongezien en kan die niet wachten, dan krijg je er één e-mail over, maximaal één per uur. Wat je al hebt afgehandeld, wordt weggelaten. Elke to-do staat er één keer in, met de huidige status. Op de meeste dagen is het ochtendoverzicht de enige e-mail.
- Als een teamgenoot je een to-do geeft en je Machine geen telefoonnummer of Telegram heeft om je te bereiken, krijg je één e-mail met de titel en een link. Die komt na 15 minuten als je de melding dan nog niet hebt gezien. Zet **E-mail** bij **Resultaten en vragen** uit om dit uit te schakelen.
- Buiten je werkuren krijg je geen meldingen. Het ochtendoverzicht bevat de melding.
- Een nieuwe werkgerelateerde to-do op een vrije dag wacht tot het tijdstip van je overzicht op de volgende werkdag. Bij de to-do staat wanneer je de melding krijgt, bijvoorbeeld: Melding ma 2 nov · 08:30.

Voortgang en wijzigingen geven nooit een melding. Een nieuw resultaat voor een to-do die je nog niet hebt gezien, wordt bijgewerkt zonder nieuwe melding. Meerdere meldingen vlak na elkaar geven één melding. Het appicoon laat zien hoeveel to-do's je aandacht nodig hebben.

## Knoppen in meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoonapp:

- Nieuwe to-do: **Doe het**, **Snoozen**, **Als gedaan markeren**.
- Concept klaar: **Concept openen**, **Snoozen**, **Als gedaan markeren**.
- Resultaat klaar: **Openen**, **Als gedaan markeren**, **Snoozen**.
- Je antwoord nodig, iets loopt vast of er is een login nodig: **Antwoorden**, **Openen** of **Inloggen**, daarna **Snoozen** en **Als gedaan markeren**.
- Herinnering: **Als gedaan markeren**, **Snoozen**, **Openen**.
- Ochtendoverzicht: tik erop om het te openen.

In een browser en op Telegram zie je er twee. Bij Fleet-vragen blijven **Antwoorden** en **Weigeren** altijd beschikbaar.

Vanuit een melding wordt er niets verstuurd, betaald of ingediend. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met **Concept openen** zie je de to-do in je lijst, met het volledige concept erbij. **Doe het** start het werk alleen bij een nieuwe to-do.

In de telefoonapp moet je eerst ontgrendelen om **Snoozen** of **Als gedaan markeren** te gebruiken. In een browser wordt het dashboard geopend. Daar wordt de actie uitgevoerd en zie je **Ongedaan maken**. Snoozen laat de to-do over twee uur terugkomen, of de volgende ochtend als het om een herinnering gaat.

E-mails bevatten links om items te openen (en om items waarop je wacht te snoozen). Die openen alleen het dashboard.

Als je op een melding tikt of in een e-mail of op Telegram op **Openen** tikt, zie je de to-do uitgelicht in je lijst, waar die op dat moment ook staat: **Net gedaan**, **Gedaan**, **Komt later terug** of een ander overzicht. De chat wordt nooit geopend. Als de pagina nog niet is bijgewerkt, volgt die de to-do zodra dat wel zo is.

## Het ochtendoverzicht

Je krijgt het op werkdagen op het tijdstip van **Ochtendoverzicht**, tenzij er niets te melden is. Valt dat tijdstip vóór **Gesnoozede items komen terug om**, dan wacht het overzicht tot 5 minuten daarna. Zo staan de to-do's die die ochtend terugkomen erin. Met **Voorbeeld** bekijk je het zonder het te versturen. Standaard krijg je een pushmelding en een e-mail. Het overzicht is kort genoeg om snel te lezen:

- een begroeting met wat vandaag belangrijk is, zoals "Goedemorgen Sam, 2 antwoorden staan klaar om te versturen" of, bij één to-do, "Goedemorgen Sam, klaar voor je akkoord: het bestelformulier versturen". Alleen to-do's met een concept of resultaat dat moet worden goedgekeurd, tellen als klaar. Een to-do waarvoor eerst je antwoord nodig is, telt niet mee;
- de to-do's die in de begroeting worden genoemd, elk met een link om ze te openen, en wat vandaag een deadline heeft; anders maximaal drie dingen om te doen;
- maximaal vijf to-do's die je zelf hebt toegevoegd en die op jou wachten, ongeacht wat er in de begroeting staat;
- hoeveel andere to-do's kunnen wachten en hoelang ze op jouw tempo duren, zoals "Er kunnen nog 12 wachten, ongeveer 5 min om af te handelen." To-do's die op jouw antwoord wachten, tellen niet mee in die tijd. Een to-do met een deadline vandaag die tot later is gesnoozed, of waaraan The Machine nog werkt, telt pas mee als die op jou wacht. Het aantal komt overeen met de to-do's die in je lijst op je wachten.
- je meetings op één regel.

Met **Openen** zie je de to-do uitgelicht in je lijst, ook als die is gedaan of gesnoozed. Een belofte opent de bijbehorende to-do, of de eigen pagina als die nog geen to-do heeft.

De pushmelding bevat hetzelfde, maar zonder links. Tik erop of op de link onderaan de e-mail om het overzicht opnieuw te lezen in **To-do's**.

## Het avondoverzicht

Je krijgt het op werkdagen één keer op het ingestelde tijdstip in **Werkuren**. Standaard is dat 15 minuten vóór **Tot**, via de manieren die je in de rij erboven hebt gekozen. Je krijgt het alleen op een dag waarop je actief was: je gebruikte het dashboard of maakte een keuze bij een to-do op het dashboard, in Telegram, in de chat of met je stem. Op een dag waarop je geen to-do hebt afgerond en geen meeting hebt gehad, krijg je geen overzicht.

Het begint met een telling van je dag, zoals "Goedenavond Sam, vandaag 4 to-do's gedaan", gevolgd door een onderdeel **Werk** en een onderdeel **Privé**. Een leeg onderdeel wordt weggelaten. Een melding over je Machine zelf staat in geen van beide onderdelen. Elk onderdeel bevat:

- **Vandaag gedaan**: maximaal drie to-do's die jij of je Machine heeft afgerond, gevolgd door "+12 meer" en de meetings van die dag, zoals "+3 meetings: prijsgesprek en 2 meer";
- **Open voor morgen** (op vrijdag: je volgende werkdag): de eerste meetings en wat een deadline heeft.

Aan het einde staat hoeveel to-do's nog op jou wachten. Tik op de pushmelding of op de link onderaan de e-mail om het overzicht opnieuw te lezen, met **Werk kopiëren** en **Privé kopiëren**. Zet de rij van het overzicht uit om het stop te zetten.

## Privacy

Pushmeldingen gaan rechtstreeks van je Machine naar je apparaat, versleuteld voor dat apparaat. E-mail gaat via de mailserver van The Machine en je e-mailprovider. Als [Voorzichtig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Zet **E-mail** voor een soort melding uit om die niet meer per e-mail te ontvangen.

Zet pushmeldingen voor een apparaat aan via **Dit apparaat**, of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) ontvangt eerst een gewone regel via Apple of Google en vraagt daarna je Machine om de titel en volgende stap.
