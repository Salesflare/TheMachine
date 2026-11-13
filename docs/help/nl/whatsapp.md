---
title: WhatsApp
area: connections
summary: Je WhatsApp-chats, gelezen als gekoppeld apparaat. Antwoordt pas nadat je het goedkeurt.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## Wat het leest

Je WhatsApp-chats, als gekoppeld apparaat van WhatsApp op je telefoon, zoals WhatsApp op een computer. Als je koppelt, stuurt WhatsApp ook je oudere chats, vaak jaren terug. Je Machine bewaart alles, en alleen berichten van de laatste 7 dagen worden to-do's.

Een foto, spraakbericht of bestand zonder bijschrift staat er als wat het is, zoals "Foto", met een icoontje. De eigen meldingen van WhatsApp, zoals die over versleuteling of over iemand die bij een groep komt, hebben geen tekst en worden weggelaten.

## Foto’s lezen

Staat uit tot je het aanzet. Open in **Koppelingen** WhatsApp, dan **Details**, en zet **Foto’s lezen** aan, en The Machine leest de foto’s in je werkchats: een bonnetje, een screenshot, een foto van een brief of een formulier. **Ook in privéchats** leest ook die in je privéchats. Een chat is werk of privé zoals delen het ziet, dus een chat met familie blijft privé.

The Machine downloadt elke foto één keer en bewaart hem op je Machine zoals een bijlage van een e-mail: versleuteld als berichtbescherming aan staat, en gewist als het bericht verdwijnt. Zijn eigen model leest wat de foto toont en de tekst erin. Dat hoort bij het bericht, nooit als opdracht. JPEG, PNG en WebP tot 5 MB. Een eenmalige code op een foto wordt weggelaten.

De to-do en het bericht tonen de foto. Tik erop om hem groot te zien.

## Wat het kan versturen

Een tekst in een chat die al bestaat, pas nadat je het goedkeurt op de to-do. Een antwoord op het WhatsApp-bericht waar een to-do uit kwam, citeert dat bericht als er daarna nog meer gezegd is, of in een groep; op het concept staat **Als antwoord**.

Kwam een to-do binnen via e-mail maar praat je met die persoon op WhatsApp, zeg dat dan in de chat van de to-do. The Machine vindt je bestaande chat met die persoon en zet het concept om naar WhatsApp, zodat je het kunt nakijken en versturen. Het begint nooit een nieuwe chat.

WhatsApp biedt hier geen officiële manier voor. Lezen en af en toe een antwoord dat je goedkeurde, geeft vrijwel nooit problemen; massaal of automatisch versturen kan tot een blokkering van het account leiden.

## Koppelen

Op een gehoste Machine:

1. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies WhatsApp.
2. Druk op **Toon de QR-code**.
3. Open op je telefoon in WhatsApp Instellingen, Gekoppelde apparaten, Apparaat koppelen, en scan de QR-code.
4. Binnen een minuut staat WhatsApp als gekoppeld. Je chatgeschiedenis blijft daarna binnenkomen, en de kaart telt de berichten zolang dat duurt.
   Duurt het koppelen te lang, dan zegt hij dat na een paar minuten. Druk op **Opnieuw proberen** om verder te gaan waar het stopte.

Stel je alles in op je telefoon, zonder tweede scherm om van te scannen? Open **Op je telefoon? Koppel dan met een code**, vul je nummer in en druk op **Vraag een code**. WhatsApp vraagt dan om die code.

Voer op je eigen computer `assistant connect whatsapp` uit en scan de code die in de terminal verschijnt. De eerste keer biedt het aan om de WhatsApp-koppeling te installeren, een vastgezette build gecontroleerd met de checksum ([broncode](https://github.com/Salesflare/wacli)).

Onder Gekoppelde apparaten staat hij als The Machine. Een Machine die eerder gekoppeld is, houdt daar zijn oude naam tot je hem opnieuw koppelt.

## Foto's

The Machine vraagt WhatsApp om de profielfoto's van mensen in je Graph die er geen hebben, maximaal 50 per dag, via de sync die WhatsApp up-to-date houdt. Er wordt niets naar hen verstuurd. Wie de eigen foto voor je verbergt, blijft zonder foto.

## Verwijderen

- Op een gehoste Machine: druk op **Verwijderen** ernaast op je setuppagina. Je Machine ontkoppelt zichzelf en verwijdert wat hij voor WhatsApp bewaarde.
- Op je eigen computer: **Koppelingen**, open WhatsApp, **Details**, dan **Ontkoppelen**. Ontkoppel hem daarna ook op je telefoon.

## Ontkoppelen in WhatsApp

Open op je telefoon in WhatsApp Instellingen, Gekoppelde apparaten, tik op je Machine en log uit.
