---
title: WhatsApp
area: connections
summary: Je WhatsApp-chats, gelezen als gekoppeld apparaat. Antwoorden worden pas verstuurd nadat je ze hebt goedgekeurd.
covers: connector:whatsapp
code: onboarding.py, whatsapp_setup.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 130c64388a71b7d1
---
## Wat wordt gelezen

Je WhatsApp-chats worden gelezen als gekoppeld apparaat van WhatsApp op je telefoon, net als WhatsApp op een computer. Als je WhatsApp koppelt, stuurt het ook je oudere chats door, soms van jaren geleden. Je Machine bewaart alles en alleen berichten van de afgelopen 7 dagen worden omgezet in to-do's.

Een foto, spraakbericht of bestand zonder bijschrift wordt weergegeven als wat het is, bijvoorbeeld ‘Foto’, met het bijbehorende pictogram. Meldingen van WhatsApp zelf, zoals de melding over versleuteling of dat iemand lid wordt van een groep, bevatten geen tekst en worden overgeslagen.

## Foto’s lezen

Deze functie staat uit totdat je die inschakelt. Open WhatsApp via **Koppelingen** en ga daarna naar **Details**. Schakel **Foto’s lezen** in, zodat The Machine de foto's in je werkchats leest: een bon, screenshot, foto van een brief of formulier. Met **Ook in privéchats** leest The Machine ook de foto's in je privéchats. Of een chat werk of privé is, wordt bepaald door de instellingen voor delen. Een chat met familie blijft dus privé.

The Machine downloadt elke foto één keer en bewaart die op je Machine, net als een e-mailbijlage: versleuteld als berichtbeveiliging aanstaat en verwijderd zodra het bijbehorende bericht wordt verwijderd. Het eigen model van The Machine leest wat er op de foto staat en de tekst erin. Dat telt als onderdeel van het bericht, nooit als instructies. JPEG, PNG en WebP tot 5 MB worden ondersteund. Een eenmalige code op een foto wordt overgeslagen.

De to-do en het bericht tonen de foto. Tik erop om die groter te bekijken.

## Wat The Machine kan versturen

Een tekstbericht of één bestand met eventueel een bijschrift, naar een bestaande chat en alleen nadat je het bericht via de to-do hebt goedgekeurd. Voordat je het verstuurt, toont de to-do het bestand en kun je het openen. Een bestand mag maximaal 18 MB zijn. Als een to-do afkomstig is van een WhatsApp-bericht, wordt dat bericht geciteerd wanneer er daarna nog meer is gezegd of als het in een groep is verstuurd. Het concept vermeldt dan **Als antwoord**.

Komt een to-do binnen via e-mail, maar chat je met die persoon via WhatsApp? Zeg dat dan in de chat van de to-do. The Machine zoekt je bestaande chat met die persoon en stelt WhatsApp in als bestemming voor het concept. Je kunt het dan controleren en versturen. The Machine begint nooit een nieuwe chat.

WhatsApp biedt hiervoor geen officiële manier. Lezen en af en toe een antwoord versturen dat je hebt goedgekeurd, veroorzaakt vrijwel zeker geen problemen. Bij massaal of geautomatiseerd versturen kan een account worden geblokkeerd.

## Koppelen

Op een gehoste Machine:

1. Open **Koppelingen** in het dashboard, ga naar **Chat** en kies WhatsApp.
2. Druk op **Toon de QR-code**.
3. Open WhatsApp op je telefoon, ga naar Instellingen, Gekoppelde apparaten, Een apparaat koppelen en scan de QR-code.
4. Binnen een minuut wordt WhatsApp als gekoppeld weergegeven. Daarna blijft je chatgeschiedenis binnenkomen. De kaart houdt bij hoeveel berichten er binnenkomen.
   Duurt het koppelen te lang, dan krijg je dat na een paar minuten te zien. Druk op **Opnieuw proberen** om verder te gaan waar je gebleven was.

Stel je WhatsApp in op je telefoon in en heb je geen tweede scherm om de code mee te scannen? Open **Op je telefoon? Koppel met een code**, voer je nummer in en druk op **Code ophalen**. WhatsApp vraagt daarna om die code.

Op je eigen computer: open **Koppelingen**, ga naar **Chat**, kies WhatsApp, voer je telefoonnummer met landcode in en druk op **Verbinden**. Er verschijnt een code. Open WhatsApp op je telefoon, ga naar Instellingen, Gekoppelde apparaten, Een apparaat koppelen en daarna **Koppelen met telefoonnummer**. Voer vervolgens de code in.

Je kunt ook `assistant connect whatsapp` uitvoeren en de code scannen die in de terminal verschijnt. De eerste keer wordt aangeboden de WhatsApp-connector te installeren, een vastgezette build die aan de hand van de checksum is gecontroleerd ([bron](https://github.com/Salesflare/wacli)).

Onder Gekoppelde apparaten wordt The Machine weergegeven. Een Machine die eerder is gekoppeld, behoudt daar de oude naam totdat je die opnieuw koppelt.

Als WhatsApp je Machine afmeldt, staat op de kaart **WhatsApp heeft de koppeling met deze Machine verbroken**. Druk op **Opnieuw verbinden** en koppel WhatsApp opnieuw: voer je telefoonnummer in en daarna de code die wordt weergegeven in WhatsApp, onder Gekoppelde apparaten, **Koppelen met telefoonnummer**. De koppeling wordt op dezelfde plek als voorheen gemaakt, zodat je chats behouden blijven. Als je je eigen service hebt ingesteld om WhatsApp gesynchroniseerd te houden, wordt die gepauzeerd tijdens het koppelen en daarna weer gestart.

Duurt het te lang voordat WhatsApp reageert, dan krijg je dat tijdens het instellen te zien. Druk een minuut later op **Opnieuw proberen** voor een nieuwe code.

## Profielfoto’s

The Machine vraagt WhatsApp om profielfoto's van mensen in je Graph die er nog geen hebben, maximaal 50 per dag. Dat gebeurt via de synchronisatie waarmee WhatsApp wordt bijgewerkt. Er wordt niets naar die mensen verstuurd. Als iemand zijn of haar foto voor je verbergt, blijft die persoon zonder foto.

## Verwijderen

- Op een gehoste Machine: druk op **Verwijderen** ernaast op de instellingenpagina. Je Machine verbreekt zelf de koppeling en verwijdert alles wat hij voor WhatsApp heeft bewaard.
- Op je eigen computer: open WhatsApp via **Koppelingen**, ga naar **Details** en kies **Ontkoppelen**. Verbreek daarna ook de koppeling op je telefoon.

## Ontkoppelen in WhatsApp

Open WhatsApp op je telefoon, ga naar Instellingen, Gekoppelde apparaten, tik op je Machine en meld je af.
