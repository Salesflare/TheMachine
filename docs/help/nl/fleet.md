---
title: Fleets
area: fleet
summary: Een Werk-Fleet voor je team, een Familie-Fleet voor thuis. Machines die elkaar helpen, volgens je deelregels.
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

## Zelf beantwoord in een Werk-Fleet

In een standaard Werk-Fleet beantwoordt je Machine zelf vragen van een teamgenoot over **wie iemand kent**, **context over afspraken** ("wie is deze gast?") en **wie gedeelde e-mails afhandelt**. Hij gebruikt alleen wat de [Team-Graph](team-graph.md) al met je team deelt. Privé-, persoonlijke en gevoelige threads tellen nooit mee, en hij noemt alleen mensen die de Team-Graph al deelt.

Elk antwoord staat in het tabblad Fleet, onder **Activiteit**. Om er een te stoppen, zet je het op **Nooit** onder **Delen**. Een regel die bewaard is als **Vraag het me eerst**, werkt nu als **Altijd**. Zolang delen via de Team-Graph van je Fleet uit staat, blijven wie iemand kent en context over afspraken het je eerst vragen.

Voorzichtige Werk-Fleets, Vrienden en Familie vragen het je nog steeds eerst. Warme introducties, overdrachten, gedeelde opvolging en vrije vragen houden hun eigen regels.

## Inzichten van het team

Hooguit één keer per dag leest je Machine een paar klantthreads die de Team-Graph al met je team deelt, en schrijft op hoe het team werkt. Bijvoorbeeld: "Terugbetalingen worden beantwoord vanuit de supportinbox met de sjabloon voor terugbetalingen." Ze staan in het paneel van je Werk-Fleet onder **Inzichten van het team**, voor de hele Fleet, en elk ook onder **Activiteit**. Niemand wordt eerst iets gevraagd.

- Alleen threads waarin iemand van je team schreef. Nooit privé-, persoonlijke of gevoelige.
- Alleen wat geldt over meerdere klanten heen: een werkwijze, een tool, een schrijfstijl, of wie wat afhandelt. Nooit iets over één klant, nooit feedback op je eigen product, en nooit namen, adressen, nummers of citaten.
- Elk ervan heeft een label: wat voor soort het is, dat het uit gesprekken van het team komt, en dat het voor deze Fleet is. Inzichten waar hij niet zeker van is, vallen weg.

Als één persoon iets leert, leert iedereen het. Als je Machine een werk-to-do voor dit bedrijf opstelt of voorbereidt, gebruikt hij de inzichten van het team die passen, na je eigen feiten, regels en skills. Nooit bij persoonlijke to-do's. Een to-do die er een gebruikte, zegt dat, bijvoorbeeld "Een inzicht van het team gebruikt: terugbetalingen gaan uit vanuit de supportinbox." Tik daar op **Verwijderen** om het voor de hele Fleet weg te halen.

Iedereen in de Fleet kan een inzicht **Verwijderen**. Het is dan weg voor iedereen en wordt niet opnieuw gemaakt. Om te stoppen, zet je **Aanbieden om inzichten te delen** uit in Instellingen, Beveiliging. Voorzichtige Werk-Fleets krijgen er geen.

## Briefverzoeken

Een teamgenoot met de teambrief aan vraagt je Machine elke ochtend om aantallen en datums. In een Werk-Fleet antwoordt hij zelf, met alleen wat de [Team-Graph](team-graph.md) al met je team deelt. Privé- en persoonlijke threads tellen nooit mee, en er gaat niets weg zolang delen via de Team-Graph uit staat. Elk antwoord staat in het tabblad Fleet, onder **Activiteit**. Het wordt nooit een to-do of een melding.

Om te stoppen, zet je **Mijn briefingfeiten delen met het team** uit in het tabblad Fleet, onder **Delen**. Hun brief toont jou dan als niet beantwoord.

In een voorzichtige Fleet wachten vragen op je in het tabblad Fleet onder **Briefverzoeken**: **Eén keer delen**, **Altijd delen**, **Weigeren** of **Nooit**. Alleen de laatste vraag per teamgenoot wacht, en onbeantwoorde vragen verlopen. Er wordt niets gedeeld tot je kiest.

## Team-Graph

In een Werk-Fleet wordt werk voor klanten gedeeld met je team, nadat je het hebt nagekeken. Zie [Team-Graph](team-graph.md).

## Gedeelde koppelingen

Een eigenaar of beheerder kan Stripe of Intercom één keer koppelen en met het team delen, vanuit het vak **Gedeelde koppelingen** in het tabblad Fleet. De Machines van teamgenoten lezen het, alleen lezen, en zien wie het deelde. Alleen beheerders wijzigen of stoppen het. Zie [Stripe](stripe.md) en [Intercom](intercom.md).

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
- **Activiteit**: wie wat deed en wanneer. Uitnodigingen, nieuwe leden, verwijderingen, rollen, gehoste Machines en facturatie, gedeelde connectors en goedkeuringen. Het toont ook elke keer dat ons team de Machine of de logboeken van een lid geopend heeft. Nooit de inhoud van berichten. **CSV downloaden** exporteert het. 12 maanden bewaard.

Na **Stoppen met delen** toont een gedeelde connector **Verwijderd, bevestigd** zodra elke Machine het token verwijderd heeft.
