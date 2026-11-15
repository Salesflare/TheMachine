---
title: WhatsApp
area: connections
summary: Je WhatsApp-chats, gelezen als gekoppeld apparaat. Antwoorden pas nadat je ze goedkeurt.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 4ceded6544e535eb
---
## Wat The Machine leest

Je WhatsApp-chats, als gekoppeld apparaat bij WhatsApp op je telefoon, net als WhatsApp op een computer. Als je WhatsApp koppelt, stuurt WhatsApp ook je oudere chats door, soms van jaren geleden. Je Machine bewaart alles, maar alleen berichten van de afgelopen 7 dagen worden to-do's.

Een foto, spraakbericht of bestand zonder bijschrift wordt weergegeven als wat het is, bijvoorbeeld "Foto", met het bijbehorende pictogram. Eigen meldingen van WhatsApp, zoals de melding over versleuteling of dat iemand lid wordt van een groep, bevatten geen tekst en worden overgeslagen.

## Foto’s lezen

Deze optie staat uit totdat je hem aanzet. Open WhatsApp via **Koppelingen**, ga naar **Details** en zet **Foto’s lezen** aan. The Machine leest dan foto's in je werkchats, zoals een bon, screenshot, foto van een brief of formulier. Met **Ook in privéchats** leest hij ook foto's in je privéchats. Of een chat werk of privé is, hangt af van hoe delen die ziet. Een chat met familie blijft dus privé.

The Machine downloadt elke foto één keer en bewaart die op je Machine, net als een e-mailbijlage: versleuteld als berichtbeveiliging aanstaat en verwijderd zodra het bijbehorende bericht verdwijnt. Het eigen model van The Machine leest wat er op de foto staat en welke tekst erop staat. Dat geldt als onderdeel van het bericht, nooit als instructies. JPEG, PNG en WebP tot 5 MB. Een eenmalige code in een foto wordt overgeslagen.

De to-do en het bericht tonen de foto. Tik erop om hem groter te zien.

## Wat The Machine kan versturen

Een tekstbericht of één bestand met eventueel een bijschrift, in een bestaande chat en pas nadat je het hebt goedgekeurd bij de to-do. Voordat je het verstuurt, toont de to-do het bestand en kun je het openen. Een bestand mag maximaal 18 MB zijn. Een antwoord op het WhatsApp-bericht waar een to-do vandaan komt, citeert dat bericht als er daarna nog iets is gezegd of als het in een groep was. Het concept vermeldt **Als antwoord**.

Als een to-do via e-mail binnenkwam, maar je met die persoon via WhatsApp praat, zeg dat dan in de chat van de to-do. The Machine vindt de bestaande chat met die persoon en zet het concept om naar WhatsApp, zodat je het kunt controleren en versturen. Hij begint nooit een nieuwe chat.

WhatsApp biedt hier geen officiële manier voor. Lezen en af en toe een antwoord versturen dat je hebt goedgekeurd, leidt zeer waarschijnlijk niet tot problemen. Massaal of automatisch versturen kan ervoor zorgen dat een account wordt geblokkeerd.

## WhatsApp koppelen

Op een gehoste Machine:

1. Open in het dashboard **Koppelingen**, ga naar **Chat** en kies WhatsApp.
2. Druk op **Toon de QR-code**.
3. Open op je telefoon WhatsApp, ga naar **Instellingen**, **Gekoppelde apparaten**, **Apparaat koppelen** en scan de QR-code.
4. WhatsApp wordt binnen een minuut als gekoppeld weergegeven. Daarna blijft je chatgeschiedenis binnenkomen. Op de kaart zie je hoeveel berichten er binnenkomen.
   Duurt het koppelen te lang, dan krijg je dat na een paar minuten te zien. Druk op **Opnieuw proberen** om verder te gaan waar het misging.

Stel je WhatsApp in op je telefoon in, zonder tweede scherm om de code mee te scannen? Open **Op je telefoon? Koppel met een code**, voer je nummer in en druk op **Code ophalen**. WhatsApp vraagt daarna om die code.

Op je eigen computer: open **Koppelingen**, ga naar **Chat**, kies WhatsApp, voer je telefoonnummer met landcode in en druk op **Verbinden**. Er verschijnt een code. Open op je telefoon WhatsApp, ga naar **Instellingen**, **Gekoppelde apparaten**, **Apparaat koppelen** en daarna **In plaats daarvan koppelen met telefoonnummer**. Voer de code in.

Je kunt ook `assistant connect whatsapp` uitvoeren en de code scannen die in de terminal verschijnt. De eerste keer biedt The Machine aan de WhatsApp-connector te installeren: een vastgezette build die aan de hand van de checksum is gecontroleerd ([bron](https://github.com/Salesflare/wacli)).

Onder **Gekoppelde apparaten** wordt hij weergegeven als The Machine. Een eerder gekoppelde Machine blijft daar onder de oude naam staan totdat je hem opnieuw koppelt.

## Profielfoto's

The Machine vraagt WhatsApp om profielfoto's van mensen in je Graph die er geen hebben, maximaal 50 per dag. Dat gebeurt via de synchronisatie waarmee WhatsApp wordt bijgewerkt. Er wordt niets naar die mensen verstuurd. Als iemand zijn foto voor jou verbergt, blijft die persoon zonder foto.

## WhatsApp verwijderen

- Op een gehoste Machine: druk op **Verwijderen** ernaast op je instellingenpagina. Je Machine ontkoppelt zichzelf en verwijdert wat hij voor WhatsApp heeft bewaard.
- Op je eigen computer: open WhatsApp via **Koppelingen**, ga naar **Details** en druk op **Ontkoppelen**. Ontkoppel WhatsApp daarna ook op je telefoon.

## Ontkoppelen in WhatsApp

Open op je telefoon WhatsApp, ga naar **Instellingen**, **Gekoppelde apparaten**, tik op je Machine en log uit.
