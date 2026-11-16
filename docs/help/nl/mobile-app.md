---
title: De mobiele app
area: getting-started
summary: The Machine als app op iPhone en Android: meldingen over je to-do's en delen met The Machine vanuit elke app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: f622bdc266f69965
---
De mobiele app opent je eigen dashboard, ingelogd zoals op het web. Download de app in de [App Store](https://apps.apple.com/app/id6829875215) voor iPhone en iPad, of op [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) voor Android.

De to-do **Haal meer uit The Machine** bovenaan To-do's raadt de app aan. In de browser op een telefoon opent **Downloaden** de appstore. Op een telefoon die desktopwebsites weergeeft, zie je links naar beide appstores. Op een computer zie je een QR-code die je met je telefoon kunt scannen, plus links naar beide appstores.

Op elke telefoon opent [themachine.computer/app](https://themachine.computer/app) de juiste appstore. Bovenaan **Instellingen**, **Apps** staan links naar beide appstores, of alleen naar de appstore van je telefoon als je een telefoon gebruikt. Op een computer installeer je het dashboard als app met **Computer**: zie [De app installeren](phone-app.md).

## Verbinden

Op een gehoste Machine logt de app in met je account. Open op een zelfgehoste Machine op een computer **Instellingen**, **Apps**: onder de appstores staat onder **Niet op het Network?** een code. Installeer de app en scan de code met de camera van je telefoon, of typ het adres eronder in de app. De app vraagt toestemming voordat hij verbinding maakt. De eigen inloggegevens van je Machine blijven ook nodig.

Met **Inloggen met** een dienst onder **Koppelingen** (Shortcut, Notion, Slack, Zoom en de andere) open je het inlogscherm van je telefoon. Als je daar klaar bent, ben je terug in de app en verschijnt de nieuwe koppeling vanzelf onder **Koppelingen**.

## Meldingen

De app vraagt bij de eerste keer openen of meldingen zijn toegestaan. Tik op een melding om te openen waar die over gaat: een to-do verschijnt gemarkeerd in je lijst, de ochtendbriefing opent vandaag in de **Agenda**, de teambrief opent To-do's en een Fleet-vraag opent de bijbehorende to-do. De tekst van een to-do gaat niet via Apple, Google of de dienst van The Machine. Zij geven alleen een vaste melding door, zoals 'Er is een to-do voor je'.

Vervolgens vraagt de app bij je eigen Machine de titel en volgende stap van de to-do op, zoals 'Reageer op Sam' met 'Stuur Sam: dinsdag om 10.00 uur komt goed'. De ochtendbriefing haalt op wat er op je wacht en het tijdstip van je eerste vergadering, de teambrief de eerste punten en een Fleet-update wat er is gebeurd. Als de app geen verbinding met je Machine kan maken, blijft de vaste melding staan. Op Android staat erbij hoeveel to-do's er zijn, zoals '2 to-do's wachten op je'.

Een melding heeft **Snoozen** (tot morgen) en **Markeer als gedaan**, en **Doe het** voor een to-do waar je nog niet aan bent begonnen. Je kunt ze gebruiken zodra je je telefoon hebt ontgrendeld, zonder de app te openen. Voor verzenden en de laatste stappen wordt de app altijd geopend. Je krijgt één melding per to-do: 'Wordt klaargemaakt' verandert in 'Klaargezet'. De melding verdwijnt zodra de to-do is afgerond of gesnoozed, in de app of ergens anders.

Als een bevestigde stap is uitgevoerd, vermeldt de melding **Gedaan** en wat er is gebeurd. Die blijft staan tot je op To-do's op **Begrepen** tikt. Op iPhone kan dat wachten tot je de app de volgende keer opent.

Als **Tekst in meldingen** is uitgeschakeld onder **Instellingen**, **Beveiliging**, blijft de vaste melding staan. Hetzelfde geldt als je vergrendelscherm de inhoud van meldingen verbergt. Als er niets getoond mag worden, staat er 'Tik om te openen'. Kan je telefoon op het moment dat een melding binnenkomt geen verbinding maken met je Machine, dan toont hij de details zodra hij weer online is.

Meldingen volgen dezelfde regels als pushmeldingen op het web: wat je per soort hebt gekozen onder [Meldingen](notifications.md), je [werkuren](work-hours.md) en geen meldingen terwijl je een dashboard gebruikt.

Elke telefoon met de app staat onder **Instellingen**, **Meldingen** als **Telefoon met de app**. Met **Verwijderen** zet je de meldingen voor die telefoon uit. Voor meldingen op een zelfgehoste Machine is The Machine Network nodig. De app werkt ook zonder.

## Delen met The Machine

Tik in een app op Delen en kies The Machine. Er opent een **Nieuwe to-do** met de tekst, link of bestanden die je hebt gedeeld. Controleer de inhoud, voeg eventueel een datum toe en voeg de to-do toe. Er wordt pas iets toegevoegd als je dat doet.

Alleen een bestand is ook genoeg, zoals een factuur of brief. Je Machine leest de tekst in een PDF en vult de to-do in: wat het is, de volgende stap en de datum. Het bestand gaat rechtstreeks naar je Machine en blijft daar.

Je kunt ook delen met het dashboard dat als app op Android is geïnstalleerd: kies het op dezelfde manier in het deelmenu.

Abonnementen en facturering zijn niet zichtbaar in de app. **Account openen** onder **Instellingen** blijft beschikbaar, zodat je je account kunt verwijderen.
