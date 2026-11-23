---
title: De mobiele app
area: getting-started
summary: The Machine als app op iPhone en Android: meldingen voor je to-do's en delen met The Machine vanuit elke app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 927fa395fe97f565
---
In de mobiele app zie je je eigen dashboard, ingelogd zoals op het web. Download de app in de [App Store](https://apps.apple.com/app/id6829875215) voor iPhone en iPad, of op [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) voor Android.

De to-do **Haal meer uit The Machine** bovenaan bij To-do's stelt de app voor. In de browser op je telefoon opent **Downloaden** de appstore. Staat je telefoon ingesteld op desktopwebsites, dan zie je links naar beide appstores. Op een computer zie je een QR-code die je met je telefoon kunt scannen, plus links naar beide appstores.

Op elke telefoon opent [themachine.computer/app](https://themachine.computer/app) de juiste appstore. Bij **Instellingen** > **Apps** staan beide appstores bovenaan, of op een telefoon alleen de appstore voor jouw telefoon. Op een computer installeer je het dashboard als app met **Computer**: zie [De app installeren](phone-app.md).

## Koppelen

Op een gehoste Machine logt de app in met je account. Open bij een zelfgehoste Machine op een computer **Instellingen** > **Apps**: onder de appstores vind je bij **Niet op het Network?** een code. Installeer de app en scan de code met de camera van je telefoon, of typ het adres eronder in de app. De app vraagt eerst om toestemming om te koppelen. Je moet nog steeds inloggen op je eigen Machine.

Met **Inloggen met** een dienst onder **Koppelingen** (Shortcut, Notion, Slack, Zoom en de rest) open je het inlogscherm op je telefoon. Als je daar klaar bent, keer je terug naar de app. De nieuwe koppeling verschijnt vanzelf bij **Koppelingen**.

Als de app je Machine niet kan bereiken, krijg je dat te zien en probeert de app het vanzelf opnieuw. Op een Mac opent de app de pagina ook vanzelf opnieuw als het venster na de slaapstand leeg terugkomt. Ook komt een chatbericht dat je aan het typen was dan weer terug. Op een Mac of iPad met toetsenbord laad je de pagina opnieuw met Cmd+R.

## Meldingen

De app vraagt bij de eerste keer openen of meldingen zijn toegestaan. Tik op een melding om te zien waar die over gaat: een to-do verschijnt gemarkeerd in je lijst, de ochtendmelding opent vandaag in **Agenda**, de teambrief opent To-do's en een Fleet-vraag opent de bijbehorende to-do. De tekst van een to-do gaat niet via Apple, Google of de dienst van The Machine. Die versturen alleen een vaste tekst, zoals ‘Je aandacht is nodig voor een to-do’.

De app vraagt daarna bij je eigen Machine de titel en volgende stap van de to-do op, zoals ‘Sam antwoorden’ met ‘Stuur Sam: dinsdag om 10:00 komt goed uit’. De ochtendmelding bevat wat er op je wacht en het tijdstip van je eerste meeting, de teambrief de eerste items en een Fleet-update wat er is gebeurd. Als de app je Machine niet kan bereiken, blijft de vaste tekst staan. Op Android staat erbij hoeveel to-do's op je wachten, bijvoorbeeld ‘2 to-do's vragen je aandacht’.

Een melding bevat **Snoozen** (tot morgen) en **Als gedaan markeren**, plus **Doe het** voor een to-do waar je nog niet aan bent begonnen. Deze opties werken nadat je je telefoon hebt ontgrendeld, zonder dat je de app hoeft te openen. Versturen en de laatste stappen openen altijd de app. Er is één melding per to-do: ‘Wordt klaargezet’ verandert in ‘Klaargezet’. De melding verdwijnt zodra de to-do is afgerond of gesnoozed, in de app of ergens anders.

Als een bevestigde stap is uitgevoerd, staat in de melding **Gedaan** en wat er is gebeurd. Die melding blijft staan tot je bij To-do's op **Begrepen** tikt. Op iPhone kan dat wachten tot je de app weer opent.

Als **Tekst in meldingen** is uitgeschakeld bij **Instellingen** > **Beveiliging**, blijft de vaste tekst staan. Hetzelfde geldt als het toegangsscherm de inhoud van meldingen verbergt. Als er niets getoond kan worden, staat er ‘Tik om te openen’. Als je telefoon je Machine niet kan bereiken wanneer een melding binnenkomt, zie je de details zodra je weer online bent.

Meldingen volgen dezelfde regels als pushmeldingen op het web: wat je per soort hebt gekozen bij [Meldingen](notifications.md), je [werkuren](work-hours.md) en geen meldingen terwijl je een dashboard gebruikt.

Elke telefoon met de app staat bij **Instellingen** > **Meldingen** als **Telefoon met de app**. Met **Verwijderen** stop je de meldingen op die telefoon. Voor meldingen op een zelfgehoste Machine is The Machine Network nodig. De app werkt ook zonder meldingen.

## Delen met The Machine

Tik in een app op Delen en kies The Machine. Er opent een **Nieuwe to-do** met de tekst, link of bestanden die je hebt gedeeld. Controleer de inhoud, voeg eventueel een datum toe en voeg de to-do toe. Er wordt pas iets toegevoegd als je dat doet.

Je kunt ook alleen een bestand delen, zoals een factuur of brief. Je Machine leest de tekst in een pdf en vult de to-do in: wat het is, de volgende stap en de datum. Het bestand gaat rechtstreeks naar je Machine en blijft daar.

Je kunt ook iets delen naar het dashboard dat als app is geïnstalleerd op Android: kies het op dezelfde manier in het deelmenu.

Abonnementen en facturering worden niet in de app getoond. **Account openen** staat wel bij **Instellingen**, zodat je je account kunt verwijderen.
