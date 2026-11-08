---
title: De thuisverbinding van je browser
area: troubleshooting
summary: Laat de browser van je gehoste Machine via je internet thuis naar buiten gaan met Tailscale, zodat sites zijn aanmeldingen aanvaarden.
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
---
Sommige sites, zoals LinkedIn, X en sites achter een Cloudflare-controle, weigeren aanmeldingen van een browser in de cloud. Je setuppagina kan de browser van je gehoste Machine in plaats daarvan via je internet thuis laten gaan, met Tailscale. Het is gratis, duurt ongeveer 10 minuten en het meeste gebeurt vanzelf.

## Instellen

1. Kies op je setuppagina, bij de browser van je Machine, **Tailscale** en druk op **Inloggen bij Tailscale**. Log in, of maak daar een gratis account.
2. Installeer Tailscale op een computer thuis die aan blijft, en log daar in met hetzelfde account. Geen telefoon: die slaapt.
3. Maak van die computer een exit node. De setuppagina toont het menu voor zijn systeem. Op Linux voer je `sudo tailscale set --advertise-exit-node` uit.
4. Druk op **Open hem in Tailscale** en sta hem toe: Machine settings, Edit route settings, Use as exit node, Save. Kies in hetzelfde menu Disable key expiry.

De setuppagina vinkt elke stap zelf af. Met één exit node begint je browser hem meteen te gebruiken. Met meer kies je er een en druk je op **Deze exit node gebruiken**.

## Controleren

Druk op **Testen**. De pagina toont waar het web je browser ziet: je stad en je internetprovider.

## Als je computer thuis uit staat

Je browser gaat dan rechtstreeks vanaf je Machine naar buiten, en weer via thuis zodra de computer terug aan staat. Afgemeld bij Tailscale? Druk op **Opnieuw aanmelden**. Tailscale meldt toestellen na 6 maanden af, tenzij key expiry uit staat. De setuppagina toont de datum.

## Stoppen

Druk op **Niet meer gebruiken** om weer rechtstreeks te gaan. **Meld hem ook af bij Tailscale** meldt de browser van je Machine ook af bij Tailscale. De admin console van Tailscale toont hem dan als Expired, en daar kun je hem verwijderen.
