---
title: Meldingen
area: settings
summary: Wat je bereikt, waar en wanneer: alleen wat niet kan wachten geeft een melding, de rest staat in één ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
Kies in **Instellingen**, **Meldingen** per soort waar die je bereikt:

- **Nieuwe to-do's**: alleen wat niet kan wachten, zoals iets voor vandaag of iets dringends.
- **Resultaten en vragen**: een antwoord dat klaarstaat om te versturen, een taak die een login nodig heeft, een vraag uit je Fleet.
- **Herinneringen**: snoozes en wachttijden die terugkomen.
- **Ochtendoverzicht**: één kort overzicht van je dag. Zie hieronder.
- **Avondoverzicht**: wat vandaag gedaan is en wat morgen open staat. Zie hieronder.

Elk heeft een schakelaar voor **Push** (de app op je telefoon of computer), **Telegram** als dat ingesteld is, en **E-mail** op een gehoste Machine of een Machine op The Machine Network. Alles staat aan, behalve de overzichten op Telegram.

**Werkuren** staan in hetzelfde tabblad: je werkdagen, de uren waarin meldingen mogen weggaan, wanneer snoozes terugkomen, het tijdstip van het overzicht en je tijdzone. Zie [Werkuren](work-hours.md).

## Alleen wat niet kan wachten

Een push, een melding in Telegram of een e-mail gaat alleen voor:

- een to-do voor vandaag, of een dringende;
- een antwoord waarop iemand wacht, klaargezet om te versturen;
- een taak waarvoor je moet inloggen;
- een snooze die terugkomt op het uur dat je koos.

Al de rest komt stil op het dashboard (en zonder geluid in Telegram) en wacht op het ochtendoverzicht. Op een vrije dag geeft alleen iets dringends of iets voor vandaag een melding. Hoogstens 8 pushes per dag. Na 3 dagen zonder het dashboard te openen komt alleen nog het ochtendoverzicht, tot je terug bent.

## Wanneer je een melding krijgt

Net als Slack kijkt het of je het dashboard gebruikt, niet alleen of het open staat:

- In gebruik: het dashboard staat voor je, in focus, en je klikte, typte, scrolde of tikte erop in de laatste 10 minuten. Er trilt niets. Telegram komt zonder geluid binnen.
- Weg: het dashboard staat op de achtergrond, is geminimaliseerd of gesloten, of is 10 minuten niet gebruikt. Een push gaat een minuut nadat je wegging, tenzij je terugkwam en het eerst zag.
- 15 minuten later nog niet gezien, en het kan niet wachten: één e-mail ervoor, hoogstens één per uur. Wat je intussen afhandelde, staat er niet in. Meestal is het ochtendoverzicht de enige e-mail.
- Buiten je werkuren: niets. Het ochtendoverzicht bevat wat er binnenkwam.
- Een nieuwe werk-to-do die op een vrije dag binnenkomt, wacht tot het overzichtsuur van je volgende werkdag. De to-do toont waar en wanneer die je bereikt, zoals Melding ma 2 nov · 08:30, volgens de rij **Nieuwe to-do's**. Staan Push en Telegram daar allebei uit, dan staat er niets.

Alleen wat jou nodig heeft, geeft een melding. Voortgang en wijzigingen niet. Een nieuwer resultaat op een to-do die je nog niet zag, werkt die bij zonder nieuwe melding. Een reeks meldingen trilt één keer. Het icoon van de app toont hoeveel to-do's jou nodig hebben.

## Knoppen op meldingen

Elke melding heeft knoppen voor de volgende stap. In de app op je telefoon:

- Nieuwe to-do: Doe het, Snoozen, Markeer als gedaan.
- Concept klaar: Concept openen, Snoozen, Markeer als gedaan.
- Resultaat klaar: Openen, Markeer als gedaan, Snoozen.
- Vraag, vastgelopen of inloggen nodig: Antwoorden, Openen of Inloggen, dan Snoozen en Markeer als gedaan.
- Herinnering: Markeer als gedaan, Snoozen, Openen.
- Ochtendoverzicht: tik erop om het te openen.

Een browser en Telegram tonen er twee. Fleet-vragen houden Eén keer antwoorden en Weigeren.

Vanuit een melding wordt nooit iets verstuurd, betaald of ingediend. Een concept opent altijd eerst, zodat je het ziet voor het vertrekt. Concept openen toont de to-do in je lijst met het hele concept. Doe het start alleen het werk aan een nieuwe to-do.

In de app vragen Snoozen en Markeer als gedaan eerst om te ontgrendelen. In een browser openen ze het dashboard, dat het doet en Ongedaan maken toont. Snoozen brengt de to-do over twee uur terug, of morgenochtend bij een herinnering.

Mails met wat op je wacht hebben de links Openen en Snoozen. Die openen alleen het dashboard.

## Het ochtendoverzicht

Het komt op werkdagen op je tijdstip bij **Ochtendoverzicht**, tenzij er niets te melden is. Valt dat vóór **Gesnoozede items komen terug om**, dan wacht het tot 5 minuten daarna, zodat de to-do's die die ochtend terugkomen erin staan. **Voorbeeld**, in de rij ervan, toont het zonder het te versturen. Standaard is het een push en een e-mail, kort genoeg om in één blik te lezen:

- een groet met wat vandaag telt, zoals "Goeiemorgen Sam, 2 antwoorden staan klaar om te versturen" of, voor één to-do, "Goeiemorgen Sam, klaargezet voor je akkoord: Stuur het bestelformulier";
- hoogstens drie dingen om te doen, elk met een link Openen: eerst klaargezette concepten en beloftes voor vandaag;
- hoeveel er nog kan wachten en hoe lang dat op jouw tempo duurt, zoals "12 andere kunnen wachten, ongeveer 5 min werk." To-do's die op je antwoord wachten, tellen niet mee in die tijd.
- je afspraken in één regel.

Openen toont die to-do gemarkeerd in je lijst. Is hij klaar, gesnoozed of in een andere weergave, dan opent zijn chat. Een belofte opent haar to-do, of haar eigen pagina als er nog geen is.

De push zegt hetzelfde zonder links. Tik erop om vandaag te openen in de **Agenda**.

Onderaan staan je overzichten voor **Werk** en **Privé**, dezelfde tekst die **Overzicht** bij To-do's kopieert. Is de tekst van to-do's verborgen in meldingen, dan vallen ze weg.

## Het avondoverzicht

Het komt één keer op werkdagen op zijn tijdstip in **Werkuren**, standaard 15 minuten voor **Tot**, via de manieren die je hierboven in zijn rij kiest. Een dag zonder afgewerkte to-do of gehouden afspraak krijgt er geen. Het begint met je dag in een getal, zoals "Goeienavond Sam, vandaag 4 to-do's gedaan", en dan een deel **Werk** en een deel **Privé**. Een leeg deel valt weg. Elk deel heeft:

- **Vandaag gedaan**: tot drie to-do's die jij of je Machine afwerkte, hoeveel nog meer, en je afspraken, zoals "3 afspraken: Prijsgesprek en nog 2.";
- **Open voor morgen** (op vrijdag je volgende werkdag): de eerste afspraken en wat dan moet.

Het eindigt met hoeveel to-do's nog op je wachten. Tik op de push om je to-do's te openen. Wil je het niet, zet dan zijn rij uit.

## Privacy

Push gaat van je Machine rechtstreeks naar je apparaat, versleuteld voor dat apparaat. Het control plane ziet het nooit. E-mail wordt verstuurd door de mailserver van The Machine naar het adres van je account, dus de tekst gaat langs die server en de mailprovider. Als [Voorzichtig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Zet **E-mail** uit voor een soort om die helemaal uit je e-mail te houden.

Zet push aan voor een apparaat in **Dit apparaat**, of zie [De app installeren](phone-app.md).
