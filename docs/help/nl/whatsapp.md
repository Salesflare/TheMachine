---
title: WhatsApp
area: connections
summary: Je WhatsApp-chats, ingelezen als gekoppeld apparaat. Antwoorden pas nadat je ze goedkeurt.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 9446d22f96229653
---
## Wat wordt ingelezen

Je WhatsApp-chats, als gekoppeld apparaat van WhatsApp op je telefoon, net als WhatsApp op een computer. Als je verbinding maakt, stuurt WhatsApp ook je oudere chats mee, vaak van jaren terug. Je Machine bewaart alles en alleen berichten van de afgelopen 7 dagen worden to-do's.

Een foto, spraakbericht of bestand zonder bijschrift wordt weergegeven als wat het is, bijvoorbeeld ‘Foto’, met het bijbehorende pictogram. Berichten van WhatsApp zelf, zoals de melding over versleuteling of dat iemand lid wordt van een groep, bevatten geen tekst en worden overgeslagen.

## Foto’s lezen

Deze functie staat uit totdat je hem aanzet. Open WhatsApp in **Koppelingen** en daarna **Details**. Zet **Foto’s lezen** aan, zodat The Machine de foto's in je werkchats leest: een bon, screenshot, foto van een brief of formulier. Met **Ook in privéchats** worden ook foto's in je privéchats gelezen. Of een chat werk of privé is, wordt bepaald zoals bij delen. Een chat met familie blijft dus privé.

The Machine downloadt elke foto één keer en bewaart die op je Machine, net als een e-mailbijlage: versleuteld als berichtbeveiliging aanstaat en verwijderd zodra het bijbehorende bericht wordt verwijderd. Het eigen model leest wat er op de foto staat en welke tekst erop staat. Dat telt als onderdeel van het bericht, nooit als instructies. JPEG, PNG en WebP tot 5 MB. Een eenmalige code op een foto wordt overgeslagen.

De to-do en het bericht tonen de foto. Tik erop om de foto op groot formaat te bekijken.

## Wat je kunt versturen

Een tekst of één bestand met eventueel een bijschrift, in een bestaande chat en pas nadat je het in de to-do hebt goedgekeurd. Voordat je het verstuurt, toont de to-do het bestand en kun je het openen. Een bestand mag maximaal 18 MB zijn. Als je reageert op het WhatsApp-bericht waar een to-do vandaan komt, wordt dat bericht geciteerd als er daarna nog iets is gezegd of als het in een groep was. Het concept vermeldt **Als antwoord**.

Als een to-do via e-mail binnenkwam, maar je met die persoon op WhatsApp praat, zeg dat dan in de chat van de to-do. The Machine zoekt de bestaande chat met die persoon en schakelt het concept over naar WhatsApp, zodat je het kunt controleren en versturen. Er wordt nooit een nieuwe chat gestart.

WhatsApp biedt hiervoor geen officiële manier. Lezen en af en toe een antwoord versturen dat je hebt goedgekeurd, levert zeer waarschijnlijk geen problemen op. Massaal of automatisch versturen kan ertoe leiden dat een account wordt geblokkeerd.

## Verbinding maken

Op een gehoste Machine:

1. Open **Koppelingen** in het dashboard, daarna **Chat**, en kies WhatsApp.
2. Druk op **Toon de QR-code**.
3. Open WhatsApp op je telefoon, ga naar **Instellingen**, **Gekoppelde apparaten**, **Een apparaat koppelen** en scan de QR-code.
4. Binnen een minuut wordt WhatsApp als verbonden weergegeven. Daarna blijft je chatgeschiedenis binnenkomen. Op de kaart zie je hoeveel berichten er binnenkomen.
   Duurt het verbinden te lang, dan krijg je na een paar minuten een melding. Druk op **Opnieuw proberen** om verder te gaan waar het was gebleven.

Stel je het in op je telefoon en heb je geen tweede scherm om mee te scannen? Open **Op je telefoon? Koppel met een code**, voer je nummer in en druk op **Code ophalen**. WhatsApp vraagt daarna om die code.

Op je eigen computer: open **Koppelingen**, daarna **Chat**, kies WhatsApp, voer je telefoonnummer met landcode in en druk op **Verbinden**. Er verschijnt een code. Open WhatsApp op je telefoon, ga naar **Instellingen**, **Gekoppelde apparaten**, **Een apparaat koppelen** en vervolgens **Koppelen met telefoonnummer**. Voer de code in.

Je kunt ook `assistant connect whatsapp` uitvoeren en de code scannen die in de terminal verschijnt. De eerste keer krijg je de optie om de WhatsApp-connector te installeren, een vastgezette build die met de checksum is gecontroleerd ([bron](https://github.com/Salesflare/wacli)).

Onder Gekoppelde apparaten wordt hij weergegeven als The Machine. Een Machine die eerder is gekoppeld, behoudt daar de oude naam totdat je hem opnieuw koppelt.

Als WhatsApp je Machine afmeldt, staat op de kaart **WhatsApp heeft de koppeling met deze Machine verbroken**. Druk op **Opnieuw verbinden** en koppel hem opnieuw.

## Profielfoto’s

The Machine vraagt WhatsApp om profielfoto's van mensen in je Graph die er geen hebben, maximaal 50 per dag. Dat gebeurt via de synchronisatie die WhatsApp up-to-date houdt. Er wordt niets naar die mensen verstuurd. Als iemand zijn of haar foto voor jou verbergt, blijft diegene er geen hebben.

## Verwijderen

- Op een gehoste Machine: druk op **Verwijderen** ernaast op je instellingenpagina. Je Machine verbreekt zelf de koppeling en verwijdert wat hij voor WhatsApp heeft bewaard.
- Op je eigen computer: open WhatsApp in **Koppelingen**, daarna **Details**, en druk op **Ontkoppelen**. Verbreek daarna ook de koppeling op je telefoon.

## Koppeling verbreken in WhatsApp

Open WhatsApp op je telefoon, ga naar **Instellingen**, **Gekoppelde apparaten**, tik op je Machine en kies **Uitloggen**.
