---
title: Fleets
area: fleet
summary: Een Werk-Fleet voor je team, een Familie-Fleet voor thuis. Machines die elkaar helpen, met jouw ja op elk antwoord.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV
order: 1
---
The Machine Network verbindt Machines. Wat ze elkaar vertellen, is end-to-end versleuteld, en elke Machine antwoordt alleen volgens jouw regels.

## Soorten Fleet

- **Werk-Fleet**: je team. Draag werk over, vraag wie iemand kent, krijg introducties en een teambriefing.
- **Familie-Fleet**: maximaal 6 mensen. Wanneer iedereen vrij is, gedeelde to-do's en plannen. Gratis. Zie [Familie](family.md).
- **Vrienden**: iedereen op The Machine, een voor een. Gratis. Zie [Vrienden](friends.md).

## Het tabblad Fleet

Het verschijnt zodra je in een Fleet zit, met een paneel voor elke Fleet, Familie, Vrienden, Network, Delen en Activiteit.

## Vraag het je Fleet

Vraag "wie kent iemand bij Acme?" vanuit het tabblad Fleet, of met **Vraag het de Fleet** op een organisatie in de [Graph](graph.md). De Machine van elke teamgenoot antwoordt volgens diens eigen deelregels, en vraagt het die teamgenoot eerst als de regel dat zegt.

## Briefverzoeken

Een teamgenoot met de teambrief aan vraagt je Machine elke ochtend om aantallen en datums. Dat wordt nooit een to-do. Het wacht in het tabblad Fleet, in het paneel van je Werk-Fleet, onder **Briefverzoeken**: **Eén keer delen**, **Altijd delen**, **Weigeren** of **Nooit**. Alleen de laatste vraag per teamgenoot wacht, en onbeantwoorde vragen verlopen. Er wordt niets gedeeld tot je kiest.

## Team-Graph

In een Werk-Fleet wordt werk voor klanten gedeeld met je team, nadat je het hebt nagekeken. Zie [Team-Graph](team-graph.md).

## Wat je Machine antwoordt

Stel het per Fleet in, in het paneel Delen. Zie [Deelregels](sharing-rules.md). **Instellingen** heeft een snelkoppeling: **Fleet-regels**.

## Bedrijfslogin

Voor een gehoste Werk-Fleet. Een eigenaar of beheerder die ingelogd is met een Google Workspace- of Microsoft 365-account van het bedrijf, kan **Bedrijfslogin** aanzetten op de pagina Account. Het gebruikt het domein van dat account.

Teamgenoten die inloggen met een account op dat domein, zien dan **Vragen om lid te worden**. Een eigenaar of beheerder moet elk verzoek **Goedkeuren**. Persoonlijke Gmail- en Outlook.com-accounts tellen nooit mee.

Wie je uit de Fleet verwijdert, wordt overal uitgelogd.

Om lid te worden van een Fleet, er een te starten of een Machine op je eigen computer te koppelen, zie [Abonnementen en facturatie](plans-and-billing.md) en [Vrienden en het Network](friends.md).

## Voor eigenaars en beheerders

Het Fleet-deel van je accountpagina toont nog twee dingen:

- **Onlangs verwijderd**: elke persoon die verwijderd is of vertrokken is. Er staat **Verwijderd, bevestigd** zodra hun Machine de werkgegevens verwijderd heeft, Google het uitloggen bevestigd heeft en elk gedeeld token dat ze hadden vervangen is. Tot dan staat er **In behandeling** en waarom.
- **Activiteit**: wie wat deed en wanneer. Uitnodigingen, nieuwe leden, verwijderingen, rollen, servers en facturatie, gedeelde connectors en goedkeuringen. Het toont ook elke keer dat ons team de server of de logboeken van een lid geopend heeft. Nooit de inhoud van berichten. **CSV downloaden** exporteert het. 12 maanden bewaard.

Na **Stoppen met delen** toont een gedeelde connector **Verwijderd, bevestigd** zodra elke Machine het token verwijderd heeft.
