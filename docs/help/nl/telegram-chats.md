---
title: Telegram-chats
area: connections
summary: Je Telegram-chats en kleine groepen, gelezen als een apparaat van je eigen account. Antwoordt pas na je goedkeuring.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
---
## Wat hij leest

Je privéchats en groepen tot 50 mensen, als ingelogd apparaat van je eigen Telegram-account, zoals Telegram Desktop. Bij het koppelen leest hij de laatste 7 dagen, daarna wat er binnenkomt.

Kanalen, bots, Bewaarde berichten en de eigen servicemeldingen van Telegram leest hij nooit. Gedempte en gearchiveerde chats slaat hij ook over.

Je gelezen- en onlinestatus blijft ongemoeid: niets wordt als gelezen gemarkeerd, en je telefoon toont nieuwe berichten nog steeds als nieuw.

Dit staat los van [Telegram](telegram.md), waar je eigen bot je je to-do's stuurt.

## Wat hij kan versturen

Een tekst in een chat die al bestaat, pas nadat je die op de to-do goedkeurt. Berichten gaan er één voor één uit, met een pauze ertussen.

Kwam een to-do binnen via e-mail maar praat je met die persoon op Telegram, zeg dat dan in de chat van de to-do. The Machine vindt je bestaande chat met die persoon en zet het concept om naar Telegram, zodat je het kunt nakijken en versturen. Hij begint nooit een nieuwe chat.

## Koppelen

1. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies Telegram-chats.
2. Kies **Scan een QR-code in Telegram op je telefoon**.
3. Open op je telefoon in Telegram Instellingen, Apparaten, **Link Desktop Device**, en scan de code.
4. Heeft je account een cloudwachtwoord, typ het dan als erom gevraagd wordt. Het gaat naar Telegram en wordt nooit bewaard.

Stel je alles in op je telefoon, zonder tweede scherm om van te scannen? Kies dan **Krijg een code in Telegram voor je telefoonnummer**. Het formulier zegt waar Telegram de code heen stuurde: naar je Telegram-app op een ander apparaat, per sms of naar je inlog-e-mail. Geen code? Druk op **Code opnieuw sturen**.

Op je eigen computer heb je ook een eigen Telegram-app-ID nodig. Maak er een aan op [my.telegram.org](https://my.telegram.org), onder API development tools, en vul de api_id en api_hash in het formulier in.

Of voer `assistant connect telegram` uit in een terminal en scan de code die daar verschijnt.

## Als hij stopt

- **Uitgelogd bij Telegram**: Telegram heeft de login van dit apparaat beëindigd, of je hebt het uitgelogd op je telefoon. Druk op **Opnieuw verbinden** op de kaart.
- **Telegram accepteert de app-ID niet meer**: Telegram accepteert de app-ID die deze Machine gebruikt niet meer. Er wordt niets gelezen of verstuurd tot je op **Opnieuw verbinden** drukt en een eigen app-ID toevoegt.

The Machine gebruikt hiervoor de API van Telegram. Telegram kan logins van apps zoals hem beperken of beëindigen.

## Foto's

The Machine vraagt Telegram om de profielfoto's van mensen in je Graph die er geen hebben, maximaal 50 per dag, via dezelfde login die je chats leest, en alleen voor mensen uit chats die hij leest. Er wordt niets naar hen verstuurd. Wie de eigen foto voor je verbergt, blijft zonder foto.

## Verwijderen

**Koppelingen**, open Telegram-chats, **Details**, dan **Ontkoppelen**. Je Machine logt zichzelf uit bij Telegram en verwijdert wat hij voor Telegram bewaarde.

Of beëindig het op je telefoon: open in Telegram Instellingen, Apparaten, tik op The Machine en beëindig de sessie.
