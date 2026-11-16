---
title: De mobiele app
area: getting-started
summary: The Machine als app op iPhone en Android: meldingen voor je to-do's en delen vanuit elke app met The Machine.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 0d4d41134db91fcc
---
De mobiele app opent je eigen dashboard, met dezelfde aanmelding als op het web. Download de app in de [App Store](https://apps.apple.com/app/id6829875215) voor iPhone en iPad, of op [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) voor Android.

De to-do **Haal meer uit The Machine** bovenaan To-do's raadt de app aan. In de browser op een telefoon opent **Downloaden** de appwinkel. Op een telefoon die desktopwebsites weergeeft, zie je links naar beide appwinkels. Op een computer zie je een QR-code die je met je telefoon kunt scannen, plus links naar beide appwinkels.

Op elke telefoon opent [themachine.computer/app](https://themachine.computer/app) de juiste appwinkel. In **Instellingen** > **Apps** staan beide appwinkels bovenaan, of alleen de appwinkel van je telefoon als je een telefoon gebruikt. Op een computer installeert **Computer** het dashboard als app: zie [De app installeren](phone-app.md).

## Verbinden

Op een gehoste Machine meld je je met je account aan in de app. Gebruik je een zelf gehoste Machine, open dan op een computer **Instellingen** > **Apps**. Onder de appwinkels staat **Niet op het Network?** met een code. Installeer de app en scan de code met de camera van je telefoon, of typ het adres dat eronder staat in de app. De app vraagt om toestemming voordat hij verbinding maakt. De eigen aanmelding van je Machine blijft ook vereist.

## Meldingen

De app vraagt bij de eerste keer openen of meldingen zijn toegestaan. Tik op een melding om te zien waar die over gaat: een to-do verschijnt gemarkeerd in je lijst, het ochtendoverzicht opent vandaag in **Agenda**, de teambrief opent To-do's en een Fleet-vraag opent de bijbehorende to-do. De tekst van een to-do gaat niet via Apple, Google of de service van The Machine. Die diensten geven alleen een vaste melding door, zoals 'Een to-do heeft je nodig'.

Vervolgens vraagt de app de titel en volgende stap van de to-do op bij je eigen Machine, bijvoorbeeld 'Sam antwoorden' met 'Stuur Sam: dinsdag om 10.00 uur komt goed'. Het ochtendoverzicht toont wat er op je wacht en het tijdstip van je eerste afspraak, de teambrief de eerste items en een Fleet-update wat er is gebeurd. Kan de app je Machine niet bereiken, dan blijft de vaste melding staan. Op Android staat erbij hoeveel to-do's op je wachten, bijvoorbeeld '2 to-do's hebben je nodig'.

Een melding heeft **Snoozen** (tot morgen) en **Markeer als gedaan**, en bij een to-do waaraan je nog niet bent begonnen ook **Doe het**. Deze acties werken nadat je je telefoon hebt ontgrendeld, zonder dat je de app hoeft te openen. Voor verzenden en de laatste stappen wordt de app altijd geopend. Er is één melding per to-do: 'Wordt voorbereid' verandert in 'Klaargezet'. De melding verdwijnt zodra de to-do is gedaan of gesnoozed, in de app of ergens anders.

Als een stap die je hebt bevestigd is uitgevoerd, laat de melding **Gedaan** zien, met wat er is gebeurd. De melding blijft staan totdat je in To-do's op **Begrepen** tikt. Op iPhone kan dat wachten tot je de app de volgende keer opent.

Als **Tekst in meldingen** uitstaat in **Instellingen** > **Beveiliging**, blijft de vaste meldingstekst staan. Dat geldt ook als je vergrendelscherm de inhoud van meldingen verbergt. Als er niets te tonen is, staat er 'Tik om te openen'. Kan je telefoon je Machine niet bereiken wanneer een melding binnenkomt, dan verschijnen de details zodra de verbinding is hersteld.

Dezelfde regels gelden als voor pushmeldingen op het web: wat je per soort hebt ingesteld in [Meldingen](notifications.md), je [werkuren](work-hours.md) en geen meldingen terwijl je een dashboard gebruikt.

Elke telefoon met de app staat in **Instellingen** > **Meldingen** als **Telefoon met de app**. Met **Verwijderen** zet je de meldingen voor die telefoon uit. Voor meldingen op een zelf gehoste Machine is The Machine Network nodig. De app werkt ook zonder meldingen.

## Delen met The Machine

Tik in een app op Delen en kies The Machine. Er wordt een **Nieuwe to-do** geopend met de tekst, link of bestanden die je hebt gedeeld. Controleer de inhoud, voeg desgewenst een datum toe en voeg de to-do toe. Er wordt pas iets toegevoegd als je dat doet.

Je kunt ook alleen een bestand delen, zoals een factuur of brief. Je Machine leest de tekst in een pdf en vult de to-do aan: wat het bestand is, de volgende stap en de datum. Het bestand gaat rechtstreeks naar je Machine en blijft daar.

Ook het dashboard dat als app op Android is geïnstalleerd, kan gedeelde items ontvangen. Kies het op dezelfde manier in het deelmenu.

Abonnementen en facturering worden niet in de app weergegeven. In **Instellingen** blijft **Account openen** beschikbaar, zodat je je account kunt verwijderen.
