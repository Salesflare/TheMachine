---
title: Gmail
area: connections
summary: Leest je e-mail en maakt conceptantwoorden in jouw stijl. Er wordt pas een e-mail verstuurd nadat je die hebt goedgekeurd.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: f0565a7bf839f49f
---
## Wat Gmail leest

Al je e-mail: de afgelopen 7 dagen op het moment dat je koppelt, en daarna alle nieuwe e-mails, inkomend en uitgaand. E-mails die je verstuurt tellen ook mee. Zo leert Gmail hoe je schrijft en wat je hebt beloofd.

E-mails uit Promoties, nieuwsbrieven, Updates en Forums worden eerst snel bekeken: de afzender, het onderwerp en een paar woorden, vaak meerdere tegelijk. Als een e-mail belangrijk is, wordt die helemaal gelezen en kan die een to-do worden. Er wordt niets overgeslagen zonder dat het is bekeken.

## Wat Gmail kan versturen

Een e-mail vanuit een to-do, en alleen nadat je die hebt goedgekeurd. **Doe het** maakt een concept. **Nakijken en versturen** opent het concept zodat je het kunt aanpassen. Er wordt pas iets verstuurd als je op **Nu versturen** klikt. **Inloggen met Google** vraagt Google ook toestemming om e-mails te versturen. Als je je eigen app op je eigen computer gebruikt, is de login alleen-lezen totdat je zelf toestemming geeft om e-mails te versturen.

Bij **Van** in het overzicht kun je een afzender kiezen als Gmail voor deze mailbox toestaat dat je e-mails verstuurt vanuit een alias van jezelf, eentje die in Instellingen is gemarkeerd als **Van mij** ([Je adressen](settings.md#your-addresses)). Een antwoord op e-mail die naar die alias is gestuurd, wordt vanuit die alias verstuurd. Nieuwe e-mail wordt vanuit het adres van je mailbox verstuurd. Vlak voor het versturen wordt het nogmaals aan Gmail gevraagd. Bevestigt Gmail het adres niet, dan wordt er niets verstuurd.

Een antwoord komt in het gesprek terecht waarop je reageert. Als je het verstuurt vanuit een andere mailbox dan de mailbox waarop de oorspronkelijke e-mail binnenkwam, staat dat vóór het versturen in de to-do. Het antwoord komt nog steeds in hun gesprek terecht.

Nadat je een antwoord hebt verstuurd, verdwijnt het gesprek een paar dagen uit je inbox onder het label Gesnoozed (3 dagen, tenzij de to-do iets anders aangeeft). Daarna komt het terug, of eerder als iemand antwoordt. Het blijft nooit langer weg dan tot de deadline van de to-do: het komt de werkdag ervoor terug. Als de deadline vandaag is, blijft het in je inbox. In het overzicht staat dit voordat je verstuurt. Dit is jouw mailbox: als een antwoord alleen belooft dat het werk wordt gedaan, blijft de to-do open.

## Koppelen

Op een gehoste Machine:

1. Open je installatiepagina op app.themachine.computer/setup.
2. Klik onder **Mail en agenda** op **Google koppelen** en log in. Op het scherm van Google staat Salesflare, de maker van The Machine.
3. Gmail en Google Calendar worden samen gekoppeld.

Als je je hebt aangemeld met Google en op dat scherm toegang tot Gmail en Calendar hebt toegestaan, worden ze automatisch gekoppeld. Er wordt pas iets verstuurd als je op Versturen klikt.

Je kunt ook naar het dashboard gaan: **Koppelingen**, **E-mail**, kies Gmail en klik op **Inloggen met Google**. Als je klaar bent, ga je terug naar het dashboard.

Op je eigen computer, nadat je die [aan je account hebt gekoppeld](friends.md#a-machine-on-your-own-computer):

1. Open in het dashboard **Koppelingen**, ga naar **E-mail** en kies Gmail.
2. Klik op **Inloggen met Google** en log in op het tabblad dat wordt geopend. Gmail en Google Calendar worden samen gekoppeld.

Niet gekoppeld, of gebruik je je eigen Google OAuth-client? Open daar **Je eigen app gebruiken** of voer `assistant connect gmail` uit. Klik op **Google openen**, log in en plak daarna het adres waar Google je naartoe stuurt. Google Calendar voor hetzelfde adres wordt ook gekoppeld.

Een Google Workspace-beheerder moet de app mogelijk eerst toestaan in de Admin-console.

## Gmail verwijderen

- Op een gehoste Machine: klik naast het adres op je installatiepagina op **Ontkoppelen**. Gmail en Calendar worden dan voor dat adres ontkoppeld en je Machine vergeet de login. Je andere Machines behouden hun koppeling. Met **Ontkoppelen ↗** bij Koppelingen in het dashboard ga je naar die pagina. Daar kun je met **Opnieuw koppelen** weer inloggen zonder het dashboard te verlaten.
- Op je eigen computer: open **Koppelingen**, open Gmail, klik op **Details** en daarna op **Ontkoppelen**. Gmail wordt dan niet meer gelezen. Alles wat al is binnengehaald, blijft staan. Als geen andere dienst deze Google-login nog gebruikt, vergeet je Machine die login. Je andere Machines behouden hun koppeling.

## Gmail verwijderen bij Google

Open in je Google-account Beveiliging en daarna Je verbindingen met apps en services van derden. Verwijder Salesflare (de versie met Inloggen met Google of de gehoste versie) of je eigen app.
