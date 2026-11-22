---
title: Gmail
area: connections
summary: Leest je e-mail en maakt conceptantwoorden in jouw stijl. Verstuurt een e-mail pas nadat je die goedkeurt.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## Wat hij leest

Al je e-mail: de laatste 7 dagen wanneer je koppelt, daarna alle nieuwe e-mail, zowel inkomend als uitgaand. Ook e-mail die je zelf verstuurt telt mee. Zo leert hij hoe je schrijft en wat je hebt beloofd.

Promoties, nieuwsbrieven en e-mail uit Updates en Forums bekijkt hij eerst kort: de afzender, het onderwerp en een paar woorden, veel tegelijk. Als iets belangrijk is, leest hij het helemaal en kan het een to-do worden. Er wordt niets overgeslagen zonder dat het is bekeken.

## Wat hij kan versturen

Een e-mail vanuit een to-do, en alleen nadat je toestemming geeft. **Doe het** maakt een concept. Met **Nakijken en versturen** open je het concept om het aan te passen. Er wordt pas iets verstuurd wanneer je op **Nu versturen** drukt. **Inloggen met Google** vraagt Google ook om toestemming voor versturen. Gebruik je je eigen app op je eigen computer, dan is de toegang alleen-lezen totdat je zelf versturen toevoegt.

**Van** is in het nakijkscherm een kleine keuzelijst als Gmail deze mailbox laat versturen als een alias van jou (een adres dat als **Van mij** is gemarkeerd in Instellingen, [Je adressen](settings.md#your-addresses)). Een antwoord op e-mail die naar die alias is gestuurd, wordt vanaf dat adres verstuurd. Nieuwe e-mail wordt verstuurd vanaf het adres van je mailbox. Vlak voor het versturen vraagt hij het nog een keer aan Gmail. Als Gmail het adres niet bevestigt, wordt er niets verstuurd.

Een antwoord komt in de thread van de e-mail waarop je reageert. Als je antwoord wordt verstuurd vanuit een andere mailbox dan die waarin de e-mail binnenkwam, staat dat in de to-do voordat je verstuurt. Het antwoord komt wel in hun thread terecht.

Nadat een antwoord is verstuurd, verdwijnt de thread een paar dagen uit je inbox onder het label Gesnoozed. Dat is 3 dagen, tenzij de to-do iets anders vermeldt. Daarna komt de thread terug, of eerder als iemand antwoordt. Dat staat in het nakijkscherm voordat je verstuurt. Dat geldt voor je mailbox: een antwoord dat het werk alleen belooft, houdt de to-do open.

## Koppelen

Op een gehoste Machine:

1. Open je installatiepagina op app.themachine.computer/setup.
2. Ga naar **Mail en agenda**, druk op **Google koppelen** en log in. Op het scherm van Google staat Salesflare, de maker van The Machine.
3. Gmail en Google Agenda worden samen gekoppeld.

Heb je je aangemeld met Google en Gmail en Agenda op dat scherm toegestaan? Dan worden ze automatisch gekoppeld. Er wordt pas iets verstuurd wanneer je op Versturen drukt.

Of open het dashboard: **Koppelingen**, **E-mail**, kies Gmail en druk op **Inloggen met Google**. Daarna ga je terug naar het dashboard.

Op je eigen computer, nadat die [aan je account is gekoppeld](friends.md#a-machine-on-your-own-computer):

1. Open in het dashboard **Koppelingen**, ga naar **E-mail** en kies Gmail.
2. Druk op **Inloggen met Google** en log in in het tabblad dat opent. Gmail en Google Agenda worden samen gekoppeld.

Niet gekoppeld, of gebruik je je eigen Google OAuth-client? Open daar **Je eigen app gebruiken** of voer `assistant connect gmail` uit. Druk op **Google openen**, log in en plak daarna het adres waar Google je naartoe stuurt. Google Agenda voor hetzelfde adres wordt ook gekoppeld.

Een Google Workspace-beheerder moet de app mogelijk eerst toestaan in de Beheerdersconsole.

## Koppeling verwijderen

- Op een gehoste Machine: druk op **Ontkoppelen** naast het adres op je installatiepagina. Gmail en Agenda voor dat adres worden verwijderd en je Machine vergeet de login. Je andere Machines behouden hun login. Met **Ontkoppelen ↗** bij Koppelingen in het dashboard ga je naar die pagina. Met **Opnieuw koppelen** log je daar opnieuw in zonder het dashboard te verlaten.
- Op je eigen computer: ga naar **Koppelingen**, open Gmail, kies **Details** en druk op **Ontkoppelen**. Hij stopt met lezen. Wat hij al heeft binnengehaald, blijft staan. Als niets anders die Google-login gebruikt, vergeet hij die. Je andere Machines behouden hun login.

## Verwijderen bij Google

Open in je Google-account Beveiliging, ga naar Je verbindingen met apps en services van derden en verwijder Salesflare (Inloggen met Google of gehost) of je eigen app.
