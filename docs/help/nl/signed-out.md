---
title: Uitgelogd bij een site
area: troubleshooting
summary: LinkedIn of X heeft je Machine uitgelogd. Log opnieuw in, voor één keer of blijvend.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js, dashboard/connections-login-import.js
order: 2
translated: 9a9b91270954c031
---
Sites zoals LinkedIn en X worden bekeken in de eigen browser van je Machine. Soms logt een site hem uit.

## Opnieuw inloggen

Bij **Koppelingen** en bovenaan je to-do's zie je dat je Machine is uitgelogd. Klik op **Log hier in** en log in via het kleine venster op het dashboard.

Vink **Bewaren voor de volgende keer** aan om de volgende keer met één tik weer in te loggen. Het wachtwoord blijft versleuteld op je Machine en de AI ziet het nooit. Heb je meerdere accounts op één site, dan geef je dit account met **Opslaan als** een naam (Werk, Privé). Als de to-do niet aangeeft welk account je moet gebruiken, vraagt het dialoogvenster dat.

## Wachtwoorden en codes

Voer wachtwoorden zelf in. Ook codes voor tweestapsverificatie moet je zelf invoeren.

Opgeslagen logins vind je onder **Koppelingen** en **Logins**. Met **Vergeten** verwijder je een login. Met **Importeren** haal je logins uit een wachtwoordmanager, via de eigen exportpagina daarvan in de browser van je Machine of via een exportbestand.

## Als de site je weigert of om een robotcheck vraagt

LinkedIn, X en sites met een Cloudflare-check weigeren vaak inloggen via een browser in de cloud. Op een gehoste Machine verschijnt dan **Inloggen via je thuisverbinding**. Daarmee open je je installatiepagina, waar de browser van je Machine via Tailscale of je eigen proxy verbinding kan maken via je thuisinternet. Log daarna opnieuw in.

Op je eigen computer is dit niet nodig: de browser gebruikt al je thuisverbinding.
