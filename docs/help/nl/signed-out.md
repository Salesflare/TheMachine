---
title: Afgemeld bij een site
area: troubleshooting
summary: LinkedIn of X heeft je Machine afgemeld. Log opnieuw in, eenmalig of blijvend.
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
translated: da165847c9a9d091
---
Je Machine leest sites zoals LinkedIn en X in zijn eigen browser. Soms meldt een site hem af.

## Opnieuw inloggen

Bij **Koppelingen** en bovenaan je to-do's zie je dat hij is afgemeld. Kies **Log hier in** en log in via een klein venster op het dashboard.

Vink **Bewaren voor de volgende keer** aan om de volgende keer met één tik weer in te loggen. Het wachtwoord blijft versleuteld op je Machine en de AI ziet het nooit.

## Wachtwoorden en codes

Voer wachtwoorden zelf in. Tweestapscodes moet je ook zelf invoeren.

Opgeslagen logins vind je onder **Koppelingen**, **Logins**. Met **Vergeten** verwijder je een login.

## Als de site je niet binnenlaat of een robotcheck vraagt

LinkedIn, X en sites met een Cloudflare-controle weigeren vaak inloggen via een browser in de cloud. Op een gehoste Machine zie je dan **Inloggen via je thuisverbinding**. Hiermee open je de instellingenpagina, waar de browser van je Machine via Tailscale of je eigen proxy verbinding kan maken met internet via je thuisverbinding. Log daarna opnieuw in.

Op je eigen computer heb je dit niet nodig: de browser is daar al thuis.
