---
title: De mobiele app
area: getting-started
summary: The Machine als app op iPhone en Android: meldingen voor je to-do’s en delen met The Machine vanuit elke app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 672364a90f92ef8f
---
De mobiele app opent je eigen dashboard, met dezelfde aanmelding als op het web. Download de app in de [App Store](https://apps.apple.com/app/id6829875215) voor iPhone en iPad, of in [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) voor Android.

De to-do **Haal meer uit The Machine** bovenaan To-do’s raadt de app aan. In de browser op een telefoon opent **Downloaden** de appstore. Op een telefoon die desktopwebsites toont, zie je beide links naar de appstores. Op een computer zie je een QR-code die je met je telefoon scant, en links naar beide appstores.

Op elke telefoon opent [themachine.computer/app](https://themachine.computer/app) de juiste appstore. Bovenaan **Instellingen**, **Apps** staan beide appstores, of alleen die van je telefoon als je op een telefoon zit. Op een computer installeert **Computer** het dashboard als app: zie [De app installeren](phone-app.md).

## Verbinden

Bij een gehoste Machine meld je je in de app aan met je account. Bij een zelfgehoste Machine open je op een computer **Instellingen**, **Apps**. Onder de appstores toont **Niet op het Network?** een code. Installeer de app en scan de code met de camera van je telefoon, of typ het adres dat eronder staat in de app. De app vraagt je toestemming om verbinding te maken. De aanmelding van je Machine blijft ook gelden.

Als je bij een dienst op **Inloggen met** tikt onder **Koppelingen** (Shortcut, Notion, Slack, Zoom en andere), opent het aanmeldscherm van je telefoon. Daarna keer je terug naar de app en staat de nieuwe koppeling vanzelf bij **Koppelingen**.

Als de app je Machine niet kan bereiken, laat hij dat weten en probeert hij het vanzelf opnieuw. Op een Mac of iPad met toetsenbord laad je de pagina opnieuw met Cmd+R.

## Meldingen

De app vraagt bij het eerste openen of meldingen zijn toegestaan. Tik op een melding om te zien waar die over gaat: een to-do verschijnt gemarkeerd in je lijst, de ochtendmelding opent vandaag in de **Agenda**, de teambriefing opent To-do’s en een Fleet-vraag opent de bijbehorende to-do. De tekst van een to-do gaat niet via Apple, Google of de dienst van The Machine: die versturen alleen een vaste tekst, zoals ‘Er is een to-do voor je’.

De app vraagt daarna bij je eigen Machine de titel en volgende stap van de to-do op, bijvoorbeeld ‘Antwoord Sam’ met ‘Stuur Sam: dinsdag om 10.00 uur komt goed’. De ochtendmelding bevat wat er op je wacht en het tijdstip van je eerste afspraak, de teambriefing de eerste items en een Fleet-update wat er is gebeurd. Als de app je Machine niet kan bereiken, blijft de vaste tekst staan. Op Android staat erbij hoeveel to-do’s op je wachten, bijvoorbeeld ‘2 to-do’s wachten op je’.

Een melding heeft de opties **Snoozen** (tot morgen) en **Markeer als gedaan**, en **Doe het** als je nog niet aan de to-do bent begonnen. Ze werken nadat je je telefoon hebt ontgrendeld, zonder dat je de app hoeft te openen. Voor verzenden en de laatste stappen moet je altijd de app openen. Elke to-do heeft één melding: ‘Wordt klaargezet’ verandert in ‘Klaargezet’ en de melding verdwijnt zodra de to-do is gedaan of gesnoozed, in de app of ergens anders.

Als een bevestigde stap is uitgevoerd, toont de melding **Gedaan** en wat er is gebeurd. Dat blijft staan totdat je op To-do’s op **Begrepen** tikt. Op iPhone kan dat wachten tot je de app de volgende keer opent.

Als **Tekst in meldingen** is uitgeschakeld onder **Instellingen**, **Beveiliging**, blijft alleen de vaste tekst staan. Dat geldt ook voor een vergrendelscherm dat de inhoud van meldingen verbergt. Als er niets kan worden getoond, staat er ‘Tik om te openen’. Als je telefoon je Machine niet kan bereiken wanneer een melding binnenkomt, toont hij de details zodra hij weer online is.

Je meldingen volgen dezelfde regels als pushmeldingen op het web: wat je per soort hebt gekozen bij [Meldingen](notifications.md), je [werkuren](work-hours.md) en geen meldingen terwijl je een dashboard gebruikt.

Elke telefoon met de app staat onder **Instellingen**, **Meldingen** als **Telefoon met de app**. Met **Verwijderen** schakel je de meldingen voor die telefoon uit. Voor meldingen op een zelfgehoste Machine is The Machine Network nodig. De app werkt ook zonder die meldingen.

## Delen met The Machine

Tik in een app op Delen en kies The Machine. Er opent een **Nieuwe to-do** met de tekst, link of bestanden die je hebt gedeeld. Controleer de inhoud, voeg eventueel een datum toe en voeg de to-do toe. Er wordt pas iets toegevoegd als je dat doet.

Je kunt ook alleen een bestand delen, zoals een factuur of brief. Je Machine leest de tekst uit een PDF en vult de to-do in: wat het document is, de volgende stap en de datum. Het bestand gaat rechtstreeks naar je Machine en blijft daar.

Op Android kun je ook delen met het dashboard dat als app is geïnstalleerd: kies het op dezelfde manier in het deelmenu.

Abonnementen en facturering worden niet in de app getoond. **Account openen** staat wel onder **Instellingen**, zodat je je account kunt verwijderen.
