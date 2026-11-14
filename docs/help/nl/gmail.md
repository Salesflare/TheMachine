---
title: Gmail
area: connections
summary: Leest je e-mail en maakt conceptantwoorden in jouw stijl. Verstuurd wordt er pas nadat je akkoord hebt gegeven.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: e06946aaa6ad0e1a
---
## Wat hij leest

Al je e-mail: de laatste 7 dagen wanneer je verbinding maakt, daarna alle nieuwe berichten, zowel inkomende als uitgaande. Ook e-mail die je verstuurt telt mee. Zo leert hij hoe je schrijft en wat je hebt beloofd.

Promoties, nieuwsbrieven en e-mail uit Updates en Forums bekijkt hij eerst vluchtig: de afzender, het onderwerp en een paar woorden, van veel berichten tegelijk. Als een bericht belangrijk is, leest hij het helemaal en kan het een to-do worden. Hij slaat niets over zonder het te bekijken.

## Wat hij kan versturen

Een e-mail vanuit een to-do, en alleen nadat je akkoord hebt gegeven. **Doe het** maakt een concept. **Nakijken en versturen** opent het concept zodat je het kunt bewerken. Er wordt pas iets verstuurd als je op **Nu versturen** drukt. **Inloggen met Google** vraagt Google ook om toestemming om e-mail te versturen. Gebruik je je eigen app op je eigen computer, dan kan die na het inloggen alleen e-mail lezen, totdat je zelf verzenden instelt.

**Van** is in het controlevenster een kleine keuzelijst, als Gmail toestaat dat deze mailbox e-mail verstuurt als een alias van jou (een alias met het label **Van mij** in Instellingen, [Je adressen](settings.md#your-addresses)). Een antwoord op e-mail die naar die alias is gestuurd, wordt vanaf dat adres verstuurd. Nieuwe e-mail wordt vanaf het adres van je mailbox verstuurd. Vlak voor het versturen vraagt hij het opnieuw aan Gmail. Bevestigt Gmail het adres niet, dan wordt er niets verstuurd.

Een antwoord komt in de e-mailthread waarop je reageert. Als het antwoord wordt verstuurd vanuit een andere mailbox dan die waarin de oorspronkelijke e-mail is binnengekomen, staat dat in de to-do voordat je verstuurt. Het antwoord komt nog steeds in hun thread terecht.

## Verbinden

Op een gehoste Machine:

1. Open je installatiepagina op app.themachine.computer/setup.
2. Klik onder **Mail en Agenda** op **Google verbinden** en log in. Op het Google-scherm staat Salesflare, de maker van The Machine.
3. Gmail en Google Calendar worden samen verbonden.

Heb je je aangemeld met Google en op dat scherm toestemming gegeven voor Gmail en Calendar? Dan worden ze automatisch verbonden. Er wordt alleen iets verstuurd als je op Nu versturen drukt.

Of ga in het dashboard naar **Koppelingen**, **E-mail**, kies Gmail en klik op **Inloggen met Google**. Als je klaar bent, keer je terug naar het dashboard.

Op je eigen computer, nadat die [aan je account is gekoppeld](friends.md#a-machine-on-your-own-computer):

1. Open in het dashboard **Koppelingen**, daarna **E-mail**, en kies Gmail.
2. Klik op **Inloggen met Google** en log in op het tabblad dat wordt geopend. Gmail en Google Calendar worden samen verbonden.

Niet gekoppeld, of gebruik je je eigen Google OAuth-client? Open daar **Je eigen app gebruiken** of voer `assistant connect gmail` uit. Klik op **Open Google**, log in en plak daarna het adres waar Google je naartoe stuurt. Google Calendar voor hetzelfde adres wordt ook verbonden.

Een Google Workspace-beheerder moet de app mogelijk eerst toestaan in de Admin-console.

## Verwijderen

- Op een gehoste Machine: klik naast het adres op **Ontkoppelen** op je installatiepagina. Gmail en Calendar voor dat adres worden verwijderd en je Machine vergeet de aanmeldgegevens. Je andere Machines behouden die van hen. Klik in het dashboard bij Koppelingen op **Ontkoppelen ↗** om naar die pagina te gaan. Met **Opnieuw verbinden** log je daar opnieuw in zonder het dashboard te verlaten.
- Op je eigen computer: ga naar **Koppelingen**, open Gmail, klik op **Details** en daarna op **Ontkoppelen**. De e-mail wordt dan niet meer gelezen. Wat al is binnengehaald, blijft staan. Als niets anders die Google-aanmelding gebruikt, vergeet hij die. Je andere Machines behouden die van hen.

## Verwijderen bij Google

Open in je Google-account Beveiliging, ga naar Je verbindingen met apps en services van derden en verwijder Salesflare (Inloggen met Google of gehost) of je eigen app.
