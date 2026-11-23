---
title: Meldingen
area: settings
summary: Wat je bereikt, waar en wanneer: alleen wat niet kan wachten geeft een melding, de rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3faac166e8f9fa3d
---
Minder meldingen, of andere? Kies in **Instellingen** bij **Meldingen** waar je elk soort melding ontvangt:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets met een deadline vandaag of iets urgents.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een taak waarvoor je moet inloggen of een vraag van Fleet.
- **Herinneringen**: to-do's die je hebt gesnoozed en antwoorden waarop je wacht en die terugkomen.
- **Ochtendoverzicht**: een kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat er vandaag is gedaan en wat er morgen nog openstaat. Zie hieronder.

Voor elk soort melding kun je **Push** instellen (de app op je telefoon of computer), **Telegram** zodra dat is ingesteld en **E-mail** op een gehoste Machine of een Machine op The Machine Network. Alles staat aan, behalve de overzichten op Telegram.

Je **Werkuren** staan in hetzelfde tabblad: werkdagen, wanneer meldingen kunnen binnenkomen, wanneer gesnoozede items terugkomen, de tijden van de overzichten en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Je krijgt alleen een pushmelding, een melding op Telegram of een e-mail voor:

- een to-do met een deadline vandaag of die als urgent is gemarkeerd;
- een antwoord waarop iemand wacht, als concept opgesteld en klaar om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het tijdstip dat je hebt gekozen.

Al het andere verschijnt stil op het dashboard (en zonder melding op Telegram) en wacht op het ochtendoverzicht. Op een vrije dag krijg je alleen een melding voor iets urgents of met een deadline vandaag. Je krijgt maximaal 8 pushmeldingen per dag. Als je het dashboard 3 dagen niet opent, krijg je alleen het ochtendoverzicht totdat je terug bent.

## Wanneer je meldingen krijgt

Er wordt gekeken of je het dashboard echt gebruikt, niet alleen of het openstaat:

- In gebruik (op de voorgrond, en je hebt in de afgelopen 10 minuten geklikt, getypt of gescrold): je krijgt geen melding. Telegram komt zonder geluid binnen. Alleen openen of opnieuw laden telt niet.
- Niet in gebruik (op de achtergrond, gesloten of 10 minuten inactief): een minuut nadat je weg bent, krijg je een pushmelding, tenzij je terug bent gekomen en die hebt gezien.
- Nog steeds niet gezien na 15 minuten, en het kan niet wachten: je krijgt er één e-mail over, met maximaal één e-mail per uur. Wat je al hebt afgehandeld, wordt weggelaten. Elke to-do staat er één keer in, met de huidige status. Op de meeste dagen is het ochtendoverzicht de enige e-mail.
- Een teamgenoot geeft je een to-do en je Machine heeft geen telefoon of Telegram waarop die je kan bereiken: je krijgt één e-mail met de titel en een link, na 15 minuten als je de to-do nog niet hebt gezien. Zet **E-mail** voor **Resultaten en vragen** uit om dit uit te schakelen.
- Buiten je werkuren krijg je niets. Het ochtendoverzicht vermeldt het.
- Een nieuwe werkgerelateerde to-do op een vrije dag wacht tot het tijdstip van het overzicht op je volgende werkdag. Bij de to-do staat wanneer je de melding krijgt, bijvoorbeeld Melding ma 2 nov · 08:30.

Voortgang en wijzigingen geven nooit een melding. Een nieuw resultaat voor een to-do die je nog niet hebt gezien, wordt bijgewerkt zonder nieuwe melding. Een reeks meldingen geeft één melding. Op het pictogram van de app zie je hoeveel to-do's je aandacht nodig hebben.

## Knoppen in meldingen

Elke melding heeft knoppen voor de volgende stap. In de telefoonapp:

- Nieuwe to-do: **Doe het**, **Snoozen**, **Als gedaan markeren**.
- Concept klaar: **Concept openen**, **Snoozen**, **Als gedaan markeren**.
- Resultaat klaar: **Openen**, **Als gedaan markeren**, **Snoozen**.
- Antwoord nodig, vastgelopen of inloggen vereist: **Beantwoorden**, **Openen** of **Inloggen**, gevolgd door **Snoozen** en **Als gedaan markeren**.
- Herinnering: **Als gedaan markeren**, **Snoozen**, **Openen**.
- Ochtendoverzicht: tik erop om het te openen.

In een browser en op Telegram zie je er twee. Bij vragen van Fleet blijven **Beantwoorden** en **Afwijzen** beschikbaar.

Via een melding wordt niets verstuurd, betaald of ingediend. Een concept wordt altijd eerst geopend, zodat je het kunt bekijken voordat het wordt verstuurd. Met **Concept openen** zie je de to-do in je lijst, met het volledige concept. **Doe het** start alleen het werk aan een nieuwe to-do.

In de telefoonapp moet je eerst ontgrendelen om **Snoozen** of **Als gedaan markeren** te kiezen. In een browser openen deze knoppen het dashboard, waar de actie wordt uitgevoerd en je de optie Ongedaan maken ziet. Met **Snoozen** komt de to-do over twee uur terug, of de volgende ochtend als het om een herinnering gaat.

E-mails bevatten links om items te openen (en om items waarop je wacht te snoozen). Ze openen alleen het dashboard.

Als je op een melding tikt, of op **Openen** in een e-mail of op Telegram, zie je de to-do gemarkeerd in je lijst, waar die nu ook staat: **Net gedaan**, **Gedaan**, **Komt later terug** of een ander overzicht. De chat wordt nooit geopend. Als de pagina nog niet was bijgewerkt, wordt de to-do gevolgd zodra dat wel zo is.

## Het ochtendoverzicht

Je krijgt het op werkdagen op het tijdstip van **Ochtendoverzicht**, tenzij er niets te melden is. Valt dat tijdstip vóór **Gesnoozede items komen terug om**, dan wacht het overzicht tot 5 minuten daarna. Zo staan de to-do's die die ochtend terugkomen erin. Met **Voorbeeld** bekijk je het zonder het te versturen. Standaard krijg je een pushmelding en een e-mail, kort genoeg om in één oogopslag te lezen:

- een begroeting met wat vandaag belangrijk is, zoals "Goedemorgen Sam, 2 antwoorden staan klaar om te versturen" of, bij één to-do, "Goedemorgen Sam, klaar voor je akkoord: het bestelformulier versturen". Alleen to-do's met een concept of resultaat dat moet worden goedgekeurd, tellen als klaar. Een to-do waarvoor je eerst antwoord moet geven, telt niet mee;
- de to-do's die in de begroeting meetellen, elk met een link om ze te openen, en wat vandaag een deadline heeft; anders staan er maximaal drie dingen om te doen;
- maximaal vijf to-do's die je zelf hebt toegevoegd en waarop je moet wachten, ongeacht wat er in de begroeting wordt meegeteld;
- hoeveel andere to-do's kunnen wachten en hoelang je eraan bezig bent op jouw tempo, bijvoorbeeld "Er kunnen nog 12 wachten, ongeveer 5 min om af te handelen." To-do's waarvoor jouw antwoord nodig is, tellen niet mee in die tijd. Een to-do met een deadline vandaag die tot later is gesnoozed, of waaraan The Machine nog werkt, telt pas mee als jij aan zet bent. Het aantal komt overeen met de to-do's die in je lijst op je wachten.
- je meetings op één regel.

Met **Openen** zie je de to-do gemarkeerd in je lijst, ook als die is afgerond of gesnoozed. Een belofte opent de bijbehorende to-do, of de eigen pagina als die nog geen to-do heeft.

De pushmelding bevat hetzelfde, maar zonder links. Tik erop, of op de link aan het einde van de e-mail, om dit overzicht opnieuw te lezen in **To-do's**.

## Het avondoverzicht

Je krijgt het één keer op werkdagen, op het tijdstip in **Werkuren**, standaard 15 minuten vóór **Tot**, via de kanalen die je in de rij hierboven hebt gekozen. Je krijgt het alleen op een dag waarop je actief was: je hebt het dashboard gebruikt of een keuze gemaakt bij een to-do, op Telegram, in de chat of met je stem. Op een dag waarop geen to-do is afgerond en geen meeting is gehouden, krijg je het niet.

Het begint met een telling van de dag, zoals "Goedenavond Sam, vandaag 4 to-do's gedaan", gevolgd door een onderdeel **Werk** en een onderdeel **Privé**. Een onderdeel zonder inhoud wordt weggelaten. Beide bevatten:

- **Vandaag gedaan**: maximaal drie to-do's die jij of je Machine heeft afgerond, gevolgd door "+12 meer" en de meetings van die dag, zoals "+3 meetings: Prijsgesprek en nog 2";
- **Open voor morgen** (op vrijdag voor je volgende werkdag): de eerste meetings en wat een deadline heeft.

Het eindigt met het aantal to-do's dat nog op jou wacht. Tik op de pushmelding of op de link aan het einde van de e-mail om het opnieuw te lezen, met **Werk kopiëren** en **Privé kopiëren**. Zet de bijbehorende rij uit om het overzicht niet meer te ontvangen.

## Privacy

Pushmeldingen worden versleuteld rechtstreeks van je Machine naar je apparaat verstuurd. E-mail gaat via de mailserver van The Machine en je e-mailprovider. Als [Voorzichtig](security-levels.md) to-do-tekst in meldingen verbergt, bevatten e-mails alleen aantallen. Zet **E-mail** voor een soort melding uit om die niet meer via e-mail te ontvangen.

Zet pushmeldingen voor een apparaat aan via **Dit apparaat**, of bekijk [De app installeren](phone-app.md). De [mobiele app](mobile-app.md) stuurt een gewone melding via Apple of Google en vraagt daarna je Machine om de titel en de volgende stap.
