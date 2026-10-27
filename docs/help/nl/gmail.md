---
title: Gmail
area: connections
summary: Leest je mail en schrijft antwoorden in jouw stijl. Verstuurt een e-mail pas nadat je hem goedkeurt.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
---
## Wat het leest

Al je mail: de laatste 7 dagen als je koppelt, daarna alles wat nieuw is, inkomend en uitgaand. Mail die je verstuurt telt ook mee, zodat hij leert hoe je schrijft en wat je beloofd hebt.

Mail in Promoties, nieuwsbrieven, Updates en Forums krijgt eerst een snelle blik: afzender, onderwerp en een paar woorden, veel tegelijk. Als er een belangrijk is, wordt die volledig gelezen en kan die een to-do worden. Niets wordt ongezien overgeslagen.

## Wat het kan versturen

Een e-mail vanuit een to-do, en pas nadat je hem goedkeurt. **Doe het** bereidt een concept voor; **Nakijken en versturen** opent het, klaar om te bewerken, en er gaat niets weg tot je op **Nu versturen** drukt. **Inloggen met Google** vraagt Google ook om te mogen versturen. Met je eigen app op je eigen computer is de login alleen-lezen tot je versturen zelf toevoegt.

## Koppelen

Op een gehoste Machine:

1. Open je setuppagina op app.themachine.computer/setup.
2. Druk onder **Mail en agenda** op **Google koppelen** en log in. Het scherm van Google noemt Salesflare, dat The Machine maakt.
3. Gmail en Google Calendar worden samen gekoppeld.

Op je eigen computer, zodra hij [aan je account gekoppeld is](fleet.md):

1. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies Gmail.
2. Druk op **Inloggen met Google** en log in in het tabblad dat opent. Gmail en Google Calendar worden samen gekoppeld.

Niet gekoppeld, of met je eigen Google OAuth-client: open daar **Je eigen app gebruiken**, of voer `assistant connect gmail` uit. Dat gebruikt gog. Open het adres dat het toont en log in.

Een beheerder van Google Workspace moet de app misschien eerst toestaan, in de Admin-console.

## Verwijderen

- Op een gehoste Machine: druk op **Ontkoppelen** naast het adres op je setuppagina. Dat verwijdert Gmail en Agenda voor dat adres en trekt de login bij Google in. In het dashboard brengt **Opnieuw koppelen of ontkoppelen ↗** op Koppelingen je daarheen.
- Op je eigen computer: **Koppelingen**, open Gmail, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft. Gebruikt niets anders die Google-login nog, dan wordt hij bij Google ingetrokken.

## Verwijderen bij Google

Open in je Google-account Beveiliging, dan Je verbindingen met apps en services van derden, en verwijder Salesflare (Inloggen met Google, of gehost) of je eigen app.
