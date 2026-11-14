---
title: WhatsApp
area: connections
summary: Je WhatsApp-chats worden gelezen als op een gekoppeld apparaat. Antwoorden worden pas verstuurd nadat je ze hebt goedgekeurd.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 881c555219a98f0f
---
## Wat hij leest

Je WhatsApp-chats, zoals op een gekoppeld apparaat van WhatsApp op je telefoon, net als WhatsApp op een computer. Wanneer je de koppeling maakt, stuurt WhatsApp ook je oudere chats door, vaak van jaren terug. Je Machine bewaart alles, maar alleen berichten van de afgelopen 7 dagen worden to-do's.

Een foto, spraakbericht of bestand zonder bijschrift wordt getoond als wat het is, bijvoorbeeld als "Foto", met het bijbehorende pictogram. WhatsApp-meldingen, zoals de melding over versleuteling of dat iemand lid wordt van een groep, bevatten geen tekst en worden niet meegenomen.

## Foto’s lezen

Deze functie staat uit totdat je die inschakelt. Open WhatsApp onder **Koppelingen** en vervolgens **Details**. Schakel **Foto’s lezen** in, dan leest The Machine foto's in je werkchats, zoals een bon, screenshot, foto van een brief of formulier. Met **Ook in privéchats** leest hij ook de foto's in je privéchats. Of een chat werk of privé is, hangt af van hoe die gedeeld wordt. Een chat met familie blijft dus privé.

The Machine downloadt elke foto één keer en bewaart die op je Machine, net als een e-mailbijlage: versleuteld als berichtbeveiliging is ingeschakeld en verwijderd zodra het bijbehorende bericht verdwijnt. Het eigen model leest wat er op de foto staat en de tekst erin. Dat geldt als onderdeel van het bericht, nooit als instructies. JPEG, PNG en WebP tot 5 MB. Een eenmalige code op een foto wordt niet meegenomen.

De to-do en het bericht tonen de foto. Tik erop om hem groter te bekijken.

## Wat hij kan versturen

Een tekstbericht in een bestaande chat, maar alleen nadat je het via de to-do hebt goedgekeurd. Een antwoord op het WhatsApp-bericht waar een to-do vandaan komt, vermeldt dat bericht als er daarna nog meer is gezegd of als het om een groepschat gaat. In het concept staat **Als antwoord**.

Als een to-do via e-mail binnenkomt, maar je met die persoon via WhatsApp praat, zeg dat dan in de chat van de to-do. The Machine zoekt je bestaande chat met die persoon en schakelt het concept over naar WhatsApp, zodat je het kunt controleren en versturen. Hij begint nooit een nieuwe chat.

WhatsApp biedt hier geen officiële manier voor. Lezen en af en toe een goedgekeurd antwoord versturen veroorzaakt zeer waarschijnlijk geen problemen. Door massaal of automatisch berichten te versturen kan een account worden geblokkeerd.

## Koppelen

Op een gehoste Machine:

1. Open in het dashboard **Koppelingen**, daarna **Chat**, en kies WhatsApp.
2. Druk op **Toon de QR-code**.
3. Open op je telefoon WhatsApp, ga naar Instellingen, Gekoppelde apparaten, Een apparaat koppelen en scan de QR-code.
4. Binnen een minuut wordt WhatsApp als gekoppeld weergegeven. Daarna blijft je chatgeschiedenis binnenkomen. De kaart telt ondertussen de berichten.
   Duurt het koppelen te lang, dan krijg je na een paar minuten een melding. Druk op **Opnieuw proberen** om verder te gaan waar het proces is gestopt.

Stel je dit in op je telefoon en heb je geen tweede scherm om de code mee te scannen? Open **Op je telefoon? Koppel met een code**, voer je nummer in en druk op **Code ophalen**. WhatsApp vraagt daarna om die code.

Op je eigen computer: open **Koppelingen**, daarna **Chat**, kies WhatsApp, voer je telefoonnummer met landcode in en druk op **Verbinden**. Er verschijnt een code. Open op je telefoon WhatsApp, ga naar Instellingen, Gekoppelde apparaten, Een apparaat koppelen, kies **In plaats daarvan koppelen met telefoonnummer** en voer de code in.

Je kunt ook `assistant connect whatsapp` uitvoeren en de code scannen die in de terminal verschijnt. De eerste keer biedt The Machine aan de WhatsApp-connector te installeren, een vastgezette build die aan de hand van de checksum is gecontroleerd ([bron](https://github.com/Salesflare/wacli)).

Bij Gekoppelde apparaten wordt hij weergegeven als The Machine. Een Machine die je eerder hebt gekoppeld, houdt daar zijn oude naam totdat je hem opnieuw koppelt.

## Foto’s

The Machine vraagt WhatsApp om profielfoto's van mensen in je Graph die er nog geen hebben, met een maximum van 50 per dag. Dit gebeurt via de synchronisatie die WhatsApp up-to-date houdt. Er wordt niets naar die mensen gestuurd. Als iemand zijn foto voor jou verbergt, blijft diegene er geen hebben.

## Verwijderen

- Op een gehoste Machine: druk op **Verwijderen** naast WhatsApp op je installatiepagina. Je Machine verbreekt de koppeling en verwijdert alles wat hij voor WhatsApp heeft bewaard.
- Op je eigen computer: open WhatsApp onder **Koppelingen**, ga naar **Details** en kies **Ontkoppelen**. Verbreek daarna ook de koppeling op je telefoon.

## Ontkoppelen in WhatsApp

Open WhatsApp op je telefoon, ga naar Instellingen, Gekoppelde apparaten, tik op je Machine en log uit.
