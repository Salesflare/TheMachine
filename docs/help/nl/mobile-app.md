---
title: De mobiele app
area: getting-started
summary: The Machine als app op iPhone en Android: meldingen voor je to-do's en delen vanuit elke app met The Machine.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 3865fe910a5427fb
---
De mobiele app opent je eigen dashboard, met dezelfde account waarmee je op het web bent ingelogd. Download de app in de [App Store](https://apps.apple.com/app/id6829875215) voor iPhone en iPad, of via [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) voor Android.

De to-do **Haal meer uit The Machine** bovenaan bij To-do's raadt de app aan. In de browser op je telefoon opent **Downloaden** de store. Staat je telefoon ingesteld op desktopwebsites, dan zie je links naar beide stores. Op een computer zie je een QR-code die je met je telefoon kunt scannen en links naar beide stores.

Op elke telefoon opent [themachine.computer/app](https://themachine.computer/app) de juiste store. In **Instellingen** bij **Apps** staan beide stores bovenaan, of alleen de store voor je telefoon als je op een telefoon zit. Op een computer installeert **Computer** het dashboard als app: zie [De app installeren](phone-app.md).

## Verbinden

Op een gehoste Machine logt de app in met je account. Gebruik je een zelf gehoste Machine, open dan op een computer **Instellingen** en **Apps**. Onder de stores toont **Niet op het Network?** een code. Installeer de app en scan de code met de camera van je telefoon, of typ het adres eronder in de app. De app vraagt toestemming voordat hij verbinding maakt. De eigen inloggegevens van je Machine blijven ook nodig.

## Meldingen

De app vraagt bij de eerste keer openen of hij meldingen mag sturen. Tik op een melding om te openen waar die over gaat: een to-do opent de chat, de ochtendmelding opent vandaag in **Agenda**, de teambrief opent To-do's en een vraag van Fleet opent de bijbehorende to-do. De tekst van een to-do gaat niet via Apple, Google of de service van The Machine. Die vervoeren alleen een vaste tekst, zoals "Een to-do heeft je nodig".

Daarna vraagt de app bij je eigen Machine de titel en volgende stap van de to-do op, zoals "Sam antwoorden" met "Stuur Sam: dinsdag 10:00 komt goed". De ochtendmelding bevat wat er op je wacht en het tijdstip van je eerste vergadering, de teambrief de eerste items en een Fleet-update wat er is gebeurd. Als de app je Machine niet kan bereiken, blijft de vaste tekst staan. Op Android staat erbij hoeveel to-do's er op je wachten, zoals "Je hebt 2 to-do's".

Een melding heeft **Snoozen** (tot morgen) en **Markeer als gedaan**, en **Doe het** voor een to-do waar je nog niet aan bent begonnen. Je kunt deze acties uitvoeren nadat je je telefoon hebt ontgrendeld, zonder de app te openen. Bij verzenden en definitieve stappen opent de app altijd. Er is één melding per to-do: "Wordt voorbereid" verandert in "Klaargezet" en de melding verdwijnt zodra de to-do is afgerond of gesnoozed, in de app of ergens anders.

Als een bevestigde stap is uitgevoerd, toont de melding **Gedaan** en wat er is gebeurd, totdat je bij To-do's op **Begrepen** tikt. Op iPhone kan dat wachten tot je de app weer opent.

Als **Tekst in meldingen** is uitgeschakeld bij **Instellingen** en **Beveiliging**, blijft de vaste tekst staan. Dat geldt ook voor een vergrendelscherm dat de inhoud van meldingen verbergt. Als er niets te tonen is, staat er "Tik om te openen". Kan je telefoon je Machine niet bereiken wanneer een melding binnenkomt, dan toont hij de details zodra hij weer online is.

Meldingen volgen dezelfde regels als pushmeldingen op het web: je keuzes per type in [Meldingen](notifications.md), je [werkuren](work-hours.md) en geen meldingen zolang je een dashboard gebruikt.

Elke telefoon met de app staat bij **Instellingen** en **Meldingen** als **Telefoon met de app**. Met **Verwijderen** stop je de meldingen op die telefoon. Voor meldingen op een zelf gehoste Machine is The Machine Network nodig. De app werkt ook zonder meldingen.

## Delen met The Machine

Tik in een app op Delen en kies The Machine. Er opent een **Nieuwe to-do** met de tekst, link of bestanden die je hebt gedeeld. Controleer de inhoud, voeg eventueel een datum toe en voeg de to-do toe. Er wordt niets toegevoegd voordat je dat doet.

Een bestand is ook genoeg, zoals een factuur of brief. Je Machine leest de tekst uit een pdf en vult de to-do in: wat het bestand is, de volgende stap en de datum. Het bestand gaat rechtstreeks naar je Machine en blijft daar.

Op Android kun je ook delen met het dashboard dat als app is geïnstalleerd: kies het op dezelfde manier in het deelmenu.

Abonnementen en facturering zijn niet zichtbaar in de app. **Account openen** staat nog wel bij **Instellingen**, zodat je je account kunt verwijderen.
