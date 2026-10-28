---
title: WhatsApp
area: connections
summary: Je WhatsApp-chats, gelezen als gekoppeld apparaat. Antwoordt pas nadat je het goedkeurt.
covers: connector:whatsapp
code: onboarding.py, next_actions.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## Wat het leest

Je WhatsApp-chats, als gekoppeld apparaat van WhatsApp op je telefoon, zoals WhatsApp op een computer. Als je koppelt, leest het de laatste 7 dagen.

Een foto, spraakbericht of bestand zonder bijschrift staat er als wat het is, zoals "Afbeelding verstuurd". De eigen meldingen van WhatsApp, zoals die over versleuteling of over iemand die bij een groep komt, hebben geen tekst en worden weggelaten.

## Wat het kan versturen

Een tekst in een chat die al bestaat, pas nadat je het goedkeurt op de to-do.

Kwam een to-do binnen via e-mail maar praat je met die persoon op WhatsApp, zeg dat dan in de chat van de to-do. The Machine vindt je bestaande chat met die persoon en zet het concept om naar WhatsApp, zodat je het kunt nakijken en versturen. Het begint nooit een nieuwe chat.

## Koppelen

Op een gehoste Machine:

1. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies WhatsApp.
2. Druk op **Toon de QR-code**.
3. Open op je telefoon in WhatsApp Instellingen, Gekoppelde apparaten, Apparaat koppelen, en scan de QR-code.

Stel je alles in op je telefoon, zonder tweede scherm om van te scannen? Open **Op je telefoon? Koppel dan met een code**, vul je nummer in en druk op **Vraag een code**. WhatsApp vraagt dan om die code.

Voer op je eigen computer `assistant connect whatsapp` uit en scan de code die in de terminal verschijnt. Zonder wacli biedt het aan om de vastgezette build van [Salesflare/wacli](https://github.com/Salesflare/wacli) te installeren, gecontroleerd met de checksum.

## Foto's

The Machine vraagt WhatsApp om de profielfoto's van mensen in je Graph die er geen hebben, maximaal 50 per dag, via de sync die WhatsApp up-to-date houdt. Er wordt niets naar hen verstuurd. Wie de eigen foto voor je verbergt, blijft zonder foto.

## Verwijderen

- Op een gehoste Machine: druk op **Verwijderen** ernaast op je setuppagina. Je server ontkoppelt zichzelf en verwijdert wat hij voor WhatsApp bewaarde.
- Op je eigen computer: **Koppelingen**, open WhatsApp, **Details**, dan **Ontkoppelen**. Ontkoppel hem daarna ook op je telefoon.

## Ontkoppelen in WhatsApp

Open op je telefoon in WhatsApp Instellingen, Gekoppelde apparaten, tik op je Machine en log uit.
