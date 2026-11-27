---
title: Browsen via je desktopapp
area: troubleshooting
summary: Laat de browser van je gehoste Machine via de computer waarop de desktopapp draait het internet op gaan. Zo zien websites je eigen internetverbinding.
code: desktop/src/exit.rs, desktop/src/settings.rs
keywords: desktop app, exit node, home internet, office, ip address, linkedin, sign in, proxy
order: 5
translated: 6da69c78d7e60574
---
Sommige sites, zoals LinkedIn, weigeren inlogpogingen vanuit een browser in de cloud. Als je in de [desktopapp](desktop-app.md) bent ingelogd, kan de browser van je gehoste Machine het internet op gaan via die computer. Websites zien dan je thuis- of kantoorverbinding, niet die van een datacenter.

## Inschakelen

Deze functie staat standaard aan zodra je Machine die heeft. In de Instellingen van de desktopapp staat de schakelaar **Mijn Machine via deze computer laten browsen** aan. Zet hem uit en de browser van je Machine gaat meteen weer rechtstreeks het internet op.

Als de browser van je Machine deze functie gebruikt, staat in het robotvakje en op het appicoon in de menubalk of taakbalk: **Je Machine gebruikt deze computer om te browsen**.

## Wat erdoorheen gaat

Alleen het browserverkeer van je Machine naar websites: poorten 80 en 443 op openbare internetadressen. De app maakt nooit zelf verbinding met deze computer, je thuis- of kantoornetwerk of andere privéadressen, en opent geen poorten op je computer. Het verkeer is beperkt tot 4 MB/s download, 1 MB/s upload en 2 GB per dag.

## Als de computer uitstaat

De browser van je Machine gaat rechtstreeks via je Machine het internet op. Zodra de app weer draait, gaat het verkeer weer via de computer.
