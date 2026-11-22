---
title: Telegram-chats
area: connections
summary: Je Telegram-chats en kleine groepen, gelezen via een ingelogd apparaat op je eigen account. Antwoorden worden pas verstuurd nadat je ze goedkeurt.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
translated: da17aef29a380002
---
## Wat The Machine leest

Je privéchats en groepen met maximaal 50 personen, via een ingelogd apparaat op je eigen Telegram-account, net als Telegram Desktop. Zodra je verbinding maakt, leest The Machine de afgelopen 7 dagen en daarna nieuwe berichten.

The Machine leest nooit kanalen, bots, Opgeslagen berichten of serviceberichten van Telegram zelf. Gedempte en gearchiveerde chats worden ook overgeslagen.

Je lees- en onlinestatus blijven ongemoeid: niets wordt als gelezen gemarkeerd en je telefoon blijft nieuwe berichten als nieuw weergeven.

Dit staat los van [Telegram](telegram.md), waar je eigen bot je to-do's stuurt.

## Wat The Machine kan versturen

Een bericht naar een bestaande chat, maar alleen nadat je het bij de to-do hebt goedgekeurd. Berichten worden één voor één verstuurd, met telkens een pauze ertussen.

Kwam een to-do binnen via e-mail, maar praat je met die persoon op Telegram? Zeg dat dan in de chat van de to-do. The Machine zoekt je bestaande chat met die persoon en zet het concept om naar Telegram, zodat je het kunt bekijken en versturen. Er wordt nooit een nieuwe chat gestart.

## Verbinden

1. Open in het dashboard **Koppelingen**, daarna **Chat**, en kies Telegram-chats.
2. Kies **Een QR-code scannen met Telegram op een ander apparaat**.
3. Open op je telefoon Telegram en ga naar Instellingen, Apparaten, **Desktopapparaat koppelen**. Scan daarna de code.
4. Heeft je account een cloudwachtwoord? Vul het in wanneer daarom wordt gevraagd. Het wordt naar Telegram gestuurd en nooit opgeslagen.

Op een telefoon staat **Een code aanvragen voor je telefoonnummer** bovenaan het formulier, omdat je geen QR-code kunt scannen vanaf hetzelfde scherm. Je ziet waar Telegram de code naartoe heeft gestuurd: je Telegram-app op een ander apparaat, een sms of je inlogmailadres. Geen code ontvangen? Druk op **Code opnieuw sturen**.

Op je eigen computer heb je ook een eigen Telegram-app-ID nodig. Maak er een aan op [my.telegram.org](https://my.telegram.org), onder API development tools, en vul de api_id en api_hash in het formulier in.

Of voer `assistant connect telegram` uit in een terminal en scan de code die daar verschijnt.

## Als de verbinding wegvalt

- **Uitgelogd bij Telegram**: Telegram heeft de login van dit apparaat beëindigd, of je hebt het apparaat uitgelogd op je telefoon. Druk in **Koppelingen** op **Opnieuw verbinden**.
- **Telegram accepteert de app-ID niet meer**: Telegram accepteert de app-ID van deze Machine niet meer. Er wordt niets gelezen of verstuurd totdat je op **Opnieuw verbinden** drukt en een eigen app-ID toevoegt.

Telegram kan logins van apps zoals The Machine beperken of beëindigen.

## Profielfoto's

The Machine vraagt Telegram om profielfoto's van mensen in je Graph die er nog geen hebben, maximaal 50 per dag. Dat gebeurt via dezelfde login waarmee je chats worden gelezen, en alleen voor mensen in chats die The Machine leest. Er wordt hun niets gestuurd. Wie zijn of haar foto voor je verbergt, blijft zonder foto.

## Loskoppelen

Open **Koppelingen**, open Telegram-chats en kies **Details** en daarna **Ontkoppelen**. Je Machine meldt zich af bij Telegram en verwijdert wat hij voor Telegram heeft bewaard.

Je kunt de verbinding ook op je telefoon beëindigen: open Telegram, ga naar Instellingen en Apparaten, tik op The Machine en beëindig de sessie.
