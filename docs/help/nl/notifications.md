---
title: Meldingen
area: settings
summary: Wat je bereikt, waar en wanneer: push, Telegram of e-mail per soort, je werkuren en het ochtendoverzicht.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
Kies in **Instellingen**, **Meldingen** per soort waar die je bereikt:

- **Nieuwe to-do's**: een antwoord waarop iemand wacht, een verzoek, alles wat dringend is.
- **Resultaten en vragen**: een concept dat klaar is om goed te keuren of te versturen, een taak die vastzit of een login nodig heeft, een vraag uit je Fleet.
- **Herinneringen**: snoozes en wachttijden die terugkomen.
- **Ochtendoverzicht**: de afspraken van vandaag, wat moet gebeuren en wat er 's nachts binnenkwam.

Elk heeft een schakelaar voor **Push** (de app op je telefoon of computer), **Telegram** als dat ingesteld is, en **E-mail** op een gehoste Machine of een Machine op The Machine Network. Alles staat aan, behalve het overzicht op Telegram.

**Werkuren** staan in hetzelfde tabblad: je werkdagen, de uren waarin meldingen mogen weggaan, wanneer snoozes terugkomen, het tijdstip van het overzicht en je tijdzone. Zie [Werkuren](work-hours.md).

## Wanneer je een melding krijgt

Net als Slack kijkt het of je het dashboard gebruikt, niet alleen of het open staat:

- In gebruik: het dashboard staat voor je, in focus, en je klikte, typte, scrolde of tikte erop in de laatste 10 minuten. Er trilt niets. Telegram komt zonder geluid binnen.
- Weg: het dashboard staat op de achtergrond, is geminimaliseerd of gesloten, of is 10 minuten niet gebruikt. Een push gaat een minuut nadat je wegging, tenzij je terugkwam en het eerst zag.
- 15 minuten later nog niet gezien: één e-mail met alles wat nog op je wacht. Hoogstens één per uur. Wat je intussen afhandelde, op Telegram of elders, staat er niet in. Het dashboard gebruiken nadat iets binnenkwam, telt als gezien. Op een dag aan het dashboard komt er dus soms geen enkele e-mail.
- Buiten je werkuren: niets. Het ochtendoverzicht bevat wat er binnenkwam.
- Een nieuwe werk-to-do die op een vrije dag binnenkomt, wacht tot het overzichtsuur van je volgende werkdag. De to-do toont waar en wanneer die je bereikt, zoals Melding ma 2 nov · 08:30, volgens de rij **Nieuwe to-do's**. Staan Push en Telegram daar allebei uit, dan staat er niets.

Alleen wat jou nodig heeft, geeft een melding. Voortgang en wijzigingen niet. Een reeks meldingen trilt één keer. Het icoon van de app toont hoeveel to-do's jou nodig hebben.

## Het ochtendoverzicht

Het komt op werkdagen op je tijdstip bij **Ochtendoverzicht**, en wordt overgeslagen als er niets te melden is. **Voorbeeld**, in de rij ervan, toont het op de pagina zonder het te versturen. Standaard is het een push en een e-mail.

## Privacy

Push gaat van je Machine rechtstreeks naar je apparaat, versleuteld voor dat apparaat. Het control plane ziet het nooit. E-mail wordt verstuurd door de mailserver van The Machine naar het adres van je account, dus de tekst gaat langs die server en de mailprovider. Als [Voorzichtig](security-levels.md) de tekst van to-do's in meldingen verbergt, bevatten e-mails alleen aantallen. Zet **E-mail** uit voor een soort om die helemaal uit je e-mail te houden.

Zet push aan voor een apparaat in **Dit apparaat**, of zie [De app installeren](phone-app.md).
