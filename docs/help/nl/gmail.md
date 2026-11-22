---
title: Gmail
area: connections
summary: Leest je e-mail en schrijft conceptantwoorden in jouw stijl. Verstuur pas een e-mail nadat je die hebt goedgekeurd.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## Wat het leest

Al je e-mail: de afgelopen 7 dagen op het moment dat je koppelt, en daarna alle nieuwe e-mail, inkomend en uitgaand. Ook de e-mail die je verstuurt telt mee, zodat hij leert hoe je schrijft en wat je hebt beloofd.

Promoties, nieuwsbrieven en e-mail uit Updates en Forums worden eerst snel bekeken: de afzender, het onderwerp en een paar woorden, vaak meerdere tegelijk. Als er iets belangrijks tussen zit, wordt die e-mail helemaal gelezen en kan er een to-do van worden gemaakt. Er wordt niets overgeslagen zonder dat het is bekeken.

## Wat het kan versturen

Een e-mail op basis van een to-do, en alleen nadat je die hebt goedgekeurd. **Doe het** maakt een concept; **Nakijken en versturen** opent het zodat je het kunt aanpassen. Er wordt pas iets verstuurd als je op **Nu versturen** drukt. **Inloggen met Google** vraagt Google ook om toestemming om e-mail te versturen. Als je je eigen app op je eigen computer gebruikt, kan die na het inloggen alleen e-mail lezen. Versturen moet je zelf nog instellen.

Bij **Van** vind je in de controleweergave een kleine keuzelijst als Gmail deze mailbox e-mail kan laten versturen als een alias van jou. Daar staat er één met **Van mij** bij in Instellingen, [Je adressen](settings.md#your-addresses). Als je antwoordt op e-mail die naar die alias is gestuurd, wordt die alias als afzender gebruikt. Nieuwe e-mail wordt verstuurd vanaf het adres van je mailbox. Vlak voor het versturen wordt het nog een keer aan Gmail gevraagd. Bevestigt Gmail het adres niet, dan wordt er niets verstuurd.

Een antwoord komt in de thread van de e-mail waarop je reageert. Als het antwoord wordt verstuurd vanuit een andere mailbox dan die waarin de e-mail is binnengekomen, staat dat in de to-do voordat je verstuurt. Het antwoord komt nog steeds in de thread van de oorspronkelijke e-mail terecht.

Nadat je een antwoord hebt verstuurd, verdwijnt de thread een paar dagen uit je inbox onder het label Gesnoozed. Dat is 3 dagen, tenzij de to-do iets anders aangeeft. Daarna komt de thread terug, of eerder als iemand antwoordt. Je ziet dit voordat je verstuurt. Zo werkt je mailbox: als een antwoord alleen belooft dat het werk wordt gedaan, blijft de to-do openstaan.

## Koppelen

Op een gehoste Machine:

1. Open je instellingenpagina op app.themachine.computer/setup.
2. Druk onder **E-mail en agenda** op **Google verbinden** en log in. Op het Google-scherm staat Salesflare, de maker van The Machine.
3. Gmail en Google Agenda worden samen gekoppeld.

Heb je je aangemeld met Google en op dat scherm Gmail en Agenda toegestaan? Dan worden ze automatisch gekoppeld. Er wordt pas iets verstuurd als je op Verzenden drukt.

Of open in het dashboard **Koppelingen**, kies **E-mail**, selecteer Gmail en druk op **Inloggen met Google**. Daarna keer je terug naar het dashboard.

Op je eigen computer, zodra hij [aan je account is gekoppeld](friends.md#a-machine-on-your-own-computer):

1. Open in het dashboard **Koppelingen**, ga naar **E-mail** en selecteer Gmail.
2. Druk op **Inloggen met Google** en log in op het tabblad dat wordt geopend. Gmail en Google Agenda worden samen gekoppeld.

Is de Machine niet gekoppeld, of gebruik je je eigen Google OAuth-client? Open daar **Je eigen app gebruiken** of voer `assistant connect gmail` uit. Druk op **Open Google**, log in en plak daarna het adres waar Google je naartoe stuurt. Google Agenda voor hetzelfde adres wordt ook gekoppeld.

Een Google Workspace-beheerder moet de app mogelijk eerst toestaan in de Admin-console.

## Koppeling verwijderen

- Op een gehoste Machine: druk op **Ontkoppelen** naast het adres op je instellingenpagina. Gmail en Agenda worden voor dat adres ontkoppeld en je Machine vergeet de inloggegevens. Je andere Machines behouden hun eigen koppelingen. Met **Ontkoppelen ↗** bij Koppelingen ga je erheen. Met **Opnieuw verbinden** kun je daar opnieuw inloggen zonder het dashboard te verlaten.
- Op je eigen computer: open **Koppelingen**, selecteer Gmail, kies **Details** en druk op **Ontkoppelen**. De e-mail wordt dan niet meer gelezen. Alles wat al is opgehaald, blijft staan. Als geen andere functie die Google-inloggegevens nog gebruikt, vergeet je Machine ze. Je andere Machines behouden hun eigen koppelingen.

## Verwijderen bij Google

Open in je Google-account Beveiliging en daarna Je verbindingen met apps en services van derden. Verwijder daar Salesflare (Inloggen met Google of gehost) of je eigen app.
