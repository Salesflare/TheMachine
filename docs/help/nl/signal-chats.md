---
title: Signal-chats
area: connections
summary: Je Signal-chats en groepen, gelezen als gekoppeld apparaat van je telefoon. Antwoordt pas na je goedkeuring.
covers: connector:signal
code: onboarding.py, signal_setup.py, signal_mirror.py, signal_store.py, signal_send.py
keywords: Signal, linked device, QR code
---
## Wat hij leest

Je chats en groepen, als gekoppeld apparaat van je telefoon, zoals Signal Desktop. Signal geeft een nieuw gekoppeld apparaat geen oudere berichten, dus hij leest vanaf het moment dat je hem koppelt.

Foto's, spraakberichten en bestanden staan er als wat ze zijn ("Stuurde een foto"), nooit met hun inhoud. Eenmalig bekijken bewaart helemaal geen inhoud. Bewerkingen en verwijderingen volgen wat er op je telefoon gebeurde, en verdwijnende berichten gaan van je Machine zodra hun tijd om is.

Verhalen, reacties, oproepen en Notitie aan mezelf slaat hij over. Niets wordt als gelezen gemarkeerd.

## Wat hij kan versturen

Een tekst in een chat die al bestaat, pas nadat je hem op de to-do goedkeurt. Een antwoord citeert het bericht waarop het reageert als dat helpt. Berichten gaan één voor één de deur uit, met een pauze ertussen.

Kwam een to-do binnen per e-mail maar praat je met die persoon op Signal, zeg het dan in de chat van de to-do. The Machine zoekt je bestaande chat met hen en zet het concept om naar Signal, zodat jij het nakijkt en verstuurt. Hij begint nooit een nieuwe chat.

## Koppelen

1. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies Signal-chats.
2. Open op je telefoon in Signal Instellingen, **Gekoppelde apparaten**, **Nieuw apparaat koppelen**, en scan de code.

Je hebt een tweede scherm nodig om van te scannen: Signal koppelt een apparaat alleen met een QR-code. Of voer `assistant connect signal` uit in een terminal en scan de code die daar verschijnt.

Je Machine bewaart de sleutels van het gekoppelde apparaat bij zichzelf. Ze verlaten hem nooit.

## Als hij stopt

Het gebruikt signal-cli, een onofficiële Signal-client. Je Machine downloadt een vaste release en controleert de checksum voor hij draait. Signal kan hem op elk moment niet meer aanvaarden.

- **Signal heeft deze Machine ontkoppeld**: je hebt hem op je telefoon verwijderd, of Signal heeft de koppeling beëindigd. Tik in **Koppelingen** op **Opnieuw verbinden** en scan een nieuwe code.
- **Werk The Machine bij voor Signal**: Signal aanvaardt de Signal-client van deze Machine niet meer. Werk The Machine bij.

## Verwijderen

**Koppelingen**, open Signal-chats, **Details**, dan **Ontkoppelen**. Je Machine verwijdert de sleutels en wat hij voor Signal bewaarde. Verwijder hem daarna ook op je telefoon: Signal, Instellingen, **Gekoppelde apparaten**, tik op The Machine en ontkoppel.
