---
title: De mobiele app
area: getting-started
summary: The Machine als app op iPhone en Android: meldingen voor je to-do's en delen vanuit elke app met The Machine.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: aaf34f864dadf180
---
De mobiele app opent je eigen dashboard, ingelogd zoals op het web. Download de app in de [App Store](https://apps.apple.com/app/id6829875215) voor iPhone en iPad, of via [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) voor Android.

De to-do **Haal meer uit The Machine** bovenaan To-do's verwijst ernaar. In de browser van een telefoon opent **Downloaden** de appstore. Op een telefoon die desktopwebsites toont, verschijnen beide links naar de appstores. Op een computer verschijnt een QR-code die je met je telefoon scant, plus links naar beide appstores.

Op elke telefoon opent [themachine.computer/app](https://themachine.computer/app) de juiste appstore. Bovenaan **Instellingen**, **Apps** staan beide appstores, of alleen die van je telefoon als je een telefoon gebruikt. Op een computer vind je er ook de desktopapp voor Windows, Mac en Linux: zie [De desktopapp](desktop-app.md).

## Koppelen

Op een gehoste Machine logt de app in met je account. Gebruik je een zelfgehoste Machine, open dan op een computer **Instellingen**, **Apps**: onder de appstores toont **Niet op het Network?** een code. Installeer de app en scan de code met de camera van je telefoon, of typ het adres eronder in de app. De app vraagt toestemming voordat hij verbinding maakt. De login van je Machine blijft ook gelden.

Als je onder **Koppelingen** bij een service (Shortcut, Notion, Slack, Zoom en andere) op **Inloggen met** tikt, opent het inlogscherm van je telefoon. Als je klaar bent, keer je terug naar de app en verschijnt de nieuwe koppeling vanzelf bij **Koppelingen**.

Als de app je Machine niet kan bereiken, laat hij dat weten en probeert het vanzelf opnieuw. Op een Mac opent de app de pagina ook vanzelf opnieuw als het venster na de sluimerstand leeg blijft. Een chatbericht dat je aan het typen was, verschijnt dan ook weer. Op een Mac of iPad met een toetsenbord laad je de pagina opnieuw met Cmd+R.

## Meldingen

De app vraagt bij de eerste keer openen of meldingen zijn toegestaan. Tik op een melding om te openen waar die over gaat: een to-do verschijnt gemarkeerd in je lijst, de ochtendmelding opent vandaag in de **Agenda**, de teambrief opent To-do's en een Fleet-vraag opent de bijbehorende to-do. Apple, Google en de service van The Machine ontvangen geen tekst van een to-do. Zij geven alleen een vaste melding door, zoals ‘Je hebt een to-do’.

De app vraagt daarna aan je eigen Machine om de titel en volgende stap van de to-do, zoals ‘Sam antwoorden’ met ‘Stuur Sam: dinsdag om 10.00 uur komt goed’. De ochtendmelding toont wat er op je wacht en het tijdstip van je eerste meeting. De teambrief toont de eerste items en een Fleet-update laat zien wat er is gebeurd. Als de app je Machine niet kan bereiken, blijft de vaste melding staan. Op Android staat erbij hoeveel to-do's op je wachten, zoals ‘2 to-do's wachten op je’.

Een melding heeft **Snoozen** (tot morgen) en **Als gedaan markeren**, en **Doe het** voor een to-do waar je nog niet aan bent begonnen. Ze werken nadat je je telefoon hebt ontgrendeld, zonder dat je de app hoeft te openen. Voor versturen en de laatste stappen moet je altijd de app openen. Elke to-do heeft één melding: ‘Wordt klaargezet’ verandert in ‘Klaargezet’. De melding verdwijnt zodra de to-do is afgerond of gesnoozed, in de app of ergens anders.

Als een stap die je hebt bevestigd is uitgevoerd, toont de melding **Gedaan** en wat er is gebeurd. Die blijft staan totdat je op To-do's op **Begrepen** tikt. Op iPhone kan dat wachten tot je de app de volgende keer opent.

Als **Tekst in meldingen** is uitgeschakeld onder **Instellingen**, **Beveiliging**, blijft de vaste melding staan. Dat geldt ook als je vergrendelscherm de inhoud van meldingen verbergt. Als er niets getoond mag worden, staat er ‘Tik om te openen’. Kan je telefoon je Machine niet bereiken wanneer een melding binnenkomt, dan verschijnen de details zodra je weer online bent.

Meldingen volgen dezelfde regels als pushmeldingen op het web: je keuzes per soort in [Meldingen](notifications.md), je [werkuren](work-hours.md) en geen meldingen terwijl je een dashboard gebruikt.

Elke telefoon met de app staat onder **Instellingen**, **Meldingen** als **Telefoon met de app**. Met **Verwijderen** zet je de meldingen voor die telefoon uit. Een zelfgehoste Machine heeft The Machine Network nodig voor meldingen. De app werkt ook zonder.

## Delen met The Machine

Tik in een app op Delen en kies The Machine. Er opent een **Nieuwe to-do** met de tekst, link of bestanden die je hebt gedeeld. Controleer de inhoud, voeg eventueel een datum toe en voeg de to-do toe. Er wordt pas iets toegevoegd als je dat doet.

Een bestand is genoeg, bijvoorbeeld een factuur of brief. Je Machine leest de tekst in een pdf en vult de to-do in: wat het is, de volgende stap en de datum. Het bestand gaat rechtstreeks naar je Machine en blijft daar.

Je kunt ook delen met het dashboard dat als app op Android is geïnstalleerd: kies het op dezelfde manier in het deelmenu.

Abonnementen en facturering worden niet in de app getoond. Onder **Instellingen** blijft **Account openen** beschikbaar, zodat je je account kunt verwijderen.
