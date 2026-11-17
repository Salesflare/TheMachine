---
title: Uitgelogd bij een site
area: troubleshooting
summary: LinkedIn of X heeft je Machine uitgelogd. Log opnieuw in, eenmalig of voorgoed.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js
order: 2
translated: 060f7ca4f870ad0a
---
Sites zoals LinkedIn en X worden geopend in de eigen browser van je Machine. Soms logt een site hem uit.

## Opnieuw inloggen

Bij **Koppelingen** en bovenaan je to-do's staat dat je bent uitgelogd. Klik op **Log hier in** en log in via een klein venster op het dashboard.

Vink **Bewaren voor de volgende keer** aan om de volgende keer met één tik opnieuw in te loggen. Het wachtwoord blijft versleuteld op je Machine en de AI ziet het nooit. Heb je meerdere accounts bij één site, dan geeft **Opslaan als** dit account een naam (Werk, Privé). Als in de to-do niet staat welk account je moet gebruiken, vraagt het venster dat aan je.

## Wachtwoorden en codes

Vul wachtwoorden zelf in. Ook codes voor tweestapsverificatie moet je zelf invoeren.

Opgeslagen logins vind je onder **Koppelingen**, **Logins**. Met **Vergeten** verwijder je een login. Met **Importeren** haal je logins uit een wachtwoordmanager.

## Als de site je toegang weigert of een robotcontrole vraagt

LinkedIn, X en sites met een Cloudflare-controle weigeren vaak inloggen via een browser in de cloud. Op een gehoste Machine zie je dan **Inloggen via je thuisverbinding**. Daarmee open je je instelpagina. Daar kan de browser van je Machine via Tailscale of je eigen proxy verbinding maken via je thuisinternet. Log daarna opnieuw in.

Op je eigen computer is dit niet nodig: de browser gebruikt al je thuisverbinding.
