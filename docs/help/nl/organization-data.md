---
title: Gegevens van organisaties
area: graph
summary: Sector, grootte, locatie en een logo bij elke organisatie, opgezocht via het webadres.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 2
---
## Waar ze vandaan komen

- Op een gehoste Machine worden de gegevens van organisaties gratis voor je opgezocht.
- Op je eigen computer staat het uit tot je een sleutel toevoegt voor een opzoekdienst die je gebruikt, zoals Apollo, People Data Labs of Hunter. Zie de [configuratiegids](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Alleen het webadres van een organisatie wordt verstuurd, nooit je berichten of wie je daar kent. Er worden er een paar tegelijk opgezocht, maximaal 50 per dag, en ze worden elke 90 dagen ververst. Personen worden apart opgezocht: zie [Functie en foto](graph.md#job-title-and-photo). Gedeelde hosts en mailproviders, zoals google.com, sites.google.com of gmail.com, worden nooit opgezocht: ze zijn niet de website van één bedrijf.

Heeft de opzoeking geen logo, of is er geen opzoeking, dan komt het logo van de eigen website van de organisatie: het icoon dat de homepage noemt. Het wordt op je Machine bewaard, zodat geen logodienst te weten komt met wie je te maken hebt. Een site zonder icoon wordt na 30 dagen opnieuw gevraagd. Vond de opzoeking de organisatie maar geen logo, dan wordt ze na een week nog één keer gedaan, en een logo dat ze dan vindt, vervangt het icoon van de site.

## Een foute corrigeren

Op de pagina van de organisatie:

- **Bewerken** om de naam, sector, grootte, locatie, oprichtingsjaar, beschrijving, website, LinkedIn en wat ze voor jou is te wijzigen. Je wijzigingen blijven. Maak een veld leeg om weer de opgezochte waarde te gebruiken.
- **Verkeerd bedrijf, details wissen** als het verkeerde bedrijf gekozen is.
- **Opnieuw opzoeken** om verse gegevens op te halen.
