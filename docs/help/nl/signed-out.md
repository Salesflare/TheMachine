---
title: Uitgelogd op een site
area: troubleshooting
summary: LinkedIn of X heeft je Machine uitgelogd. Log hem opnieuw in, één keer of voorgoed.
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
translated: b77b372b9332ca2b
---
Sites zoals LinkedIn en X worden gelezen in de eigen browser van je Machine. Soms logt een site hem uit.

## Opnieuw inloggen

De bron op **Koppelingen** en de bovenkant van je To-do's melden dat hij is uitgelogd. Druk op **Opnieuw inloggen** en log in, in een klein venster op het dashboard.

Vink **Bewaren voor de volgende keer** aan als je inlogt. De volgende keer dat de site je Machine uitlogt, logt hij met één tik opnieuw in. Het wachtwoord blijft versleuteld op je Machine; de AI ziet het nooit.

## Wachtwoorden en codes

Typ wachtwoorden zelf. Codes voor tweestapsverificatie vul je ook zelf in.

Opgeslagen logins staan onder **Koppelingen**, **Logins**. **Vergeten** verwijdert er een.

## Als de site weigert of een robotcheck wil

LinkedIn, X en sites achter een Cloudflare-check weigeren vaak logins vanuit een browser in de cloud. Op een gehoste Machine toont de login dan **Inloggen via je thuisverbinding**. Dat opent je setuppagina, waar de browser van je Machine via je internet thuis naar buiten kan met Tailscale, of via je eigen proxy. Log daarna opnieuw in.

Op je eigen computer heb je dit niet nodig: die browser staat al thuis.
