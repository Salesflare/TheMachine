---
title: Gmail
area: connections
summary: Leest je e-mail en maakt conceptantwoorden in jouw stijl. Verstuurde e-mails pas nadat je ze hebt goedgekeurd.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## Wat hij leest

Al je e-mail: de laatste 7 dagen wanneer je verbinding maakt, en daarna alle nieuwe berichten, inkomend en uitgaand. Ook berichten die je verstuurt tellen mee, zodat hij leert hoe je schrijft en wat je hebt beloofd.

Berichten uit Reclame, nieuwsbrieven, Updates en Forums worden eerst kort bekeken: de afzender, het onderwerp en een paar woorden, vaak meerdere tegelijk. Als een bericht belangrijk is, wordt het helemaal gelezen en kan het een to-do worden. Niets wordt ongemerkt overgeslagen.

## Wat hij kan versturen

Een e-mail vanuit een to-do, en pas nadat je die hebt goedgekeurd. **Doe het** maakt een concept. Met **Nakijken en versturen** open je het concept om het aan te passen. Er wordt pas iets verstuurd als je op **Nu versturen** drukt. **Inloggen met Google** vraagt Google ook om toestemming om e-mail te versturen. Gebruik je je eigen app op je eigen computer, dan is de toegang alleen-lezen totdat je zelf versturen instelt.

**Van** in het controlescherm is een kleine keuzelijst als Gmail deze mailbox e-mail kan laten versturen als een alias van jou (een alias met **Van mij** in Instellingen, [Je adressen](settings.md#your-addresses)). Een antwoord op e-mail die naar die alias is gestuurd, wordt vanaf die alias verstuurd. Nieuwe e-mail wordt vanaf het adres van je mailbox verstuurd. Vlak voor het versturen vraagt Gmail het opnieuw na. Bevestigt Gmail het adres niet, dan wordt er niets verstuurd.

Een antwoord komt in de thread van de e-mail waarop je reageert. Als het antwoord wordt verstuurd vanuit een andere mailbox dan de mailbox waarop die e-mail binnenkwam, staat dat in de to-do voordat je verstuurt. Het antwoord komt nog steeds in hun thread terecht.

Nadat een antwoord is verstuurd, verdwijnt de thread een paar dagen uit je inbox onder het label Gesnoozed (3 dagen, tenzij de to-do iets anders aangeeft). Daarna komt de thread terug, of eerder als iemand antwoordt. Dat staat in het controlescherm voordat je verstuurt. Zo werkt je mailbox: blijft een antwoord alleen een belofte om het werk te doen, dan blijft de to-do open.

## Verbinden

Op een gehoste Machine:

1. Open je instellingenpagina op app.themachine.computer/setup.
2. Klik onder **E-mail en agenda** op **Google verbinden** en log in. Op het scherm van Google staat Salesflare, de maker van The Machine.
3. Gmail en Google Calendar worden samen verbonden.

Heb je je aangemeld met Google en op dat scherm toegang gegeven tot Gmail en Calendar? Dan worden ze automatisch verbonden. Er wordt alleen iets verstuurd als je op Versturen drukt.

Of via het dashboard: **Koppelingen**, **E-mail**, kies Gmail en klik op **Inloggen met Google**. Als je klaar bent, ga je terug naar het dashboard.

Op je eigen computer, zodra die [aan je account is gekoppeld](friends.md#a-machine-on-your-own-computer):

1. Open in het dashboard **Koppelingen**, daarna **E-mail**, en kies Gmail.
2. Klik op **Inloggen met Google** en log in op het tabblad dat wordt geopend. Gmail en Google Calendar worden samen verbonden.

Niet gekoppeld, of gebruik je je eigen Google OAuth-client? Open daar **Je eigen app gebruiken** of voer `assistant connect gmail` uit. Klik op **Open Google**, log in en plak daarna het adres waar Google je naartoe stuurt. Google Calendar voor hetzelfde adres wordt ook verbonden.

Een Google Workspace-beheerder moet de app mogelijk eerst toestaan in de Admin-console.

## Loskoppelen

- Op een gehoste Machine: klik op **Ontkoppelen** naast het adres op je instellingenpagina. Gmail en Calendar voor dat adres worden verwijderd en je Machine vergeet de inloggegevens. Je andere Machines behouden hun verbinding. Via **Ontkoppelen ↗** bij Koppelingen ga je ernaartoe. Met **Opnieuw verbinden** log je daar opnieuw in zonder het dashboard te verlaten.
- Op je eigen computer: open **Koppelingen**, kies Gmail, klik op **Details** en daarna op **Ontkoppelen**. De e-mail wordt niet meer gelezen. Wat al is opgehaald, blijft staan. Als niets anders die Google-inloggegevens gebruikt, vergeet hij ze. Je andere Machines behouden hun verbinding.

## Verwijderen bij Google

Open in je Google-account Beveiliging en daarna Je verbindingen met apps en services van derden. Verwijder Salesflare (Inloggen met Google of gehost) of je eigen app.
