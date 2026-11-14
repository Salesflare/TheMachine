---
title: Fleets
area: fleet
summary: Een Work Fleet voor je team, een Family Fleet voor thuis. Machines die elkaar helpen, volgens jouw deelregels.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: c9650fc4ffe00e16
---
Met een Fleet kan je Machine via The Machine Network samenwerken met de Machines van je team, familie of vrienden. Wat ze elkaar vertellen, is end-to-end versleuteld. Je Machine antwoordt alleen volgens jouw regels.

## Soorten Fleet

- **Work Fleet**: je team. Draag werk over, vraag wie iemand kent, krijg introducties en een teambrief.
- **Family Fleet**: maximaal 6 mensen. Gedeelde to-do's en plannen voor wanneer iedereen tijd heeft. Gratis. Bekijk [Family](family.md).
- **Vrienden**: één voor één iedereen op The Machine. Gratis. Bekijk [Vrienden](friends.md).

## Het tabblad Fleet

Dit tabblad verschijnt zodra je lid bent van een Fleet. Elke Fleet heeft een eigen paneel, met Family, Vrienden, Network, Delen en Activiteit.

## Wat het kost, een Fleet verlaten en een Fleet starten

Onder de naam van elke Fleet toont **Wat het kost** het aantal plekken, wie voor je Machine betaalt en, voor de eigenaar, de betaalkaart en facturen van de Fleet. Met **Deze Fleet verlaten** verlaat je de Fleet. Een eigenaar moet de Fleet eerst aan iemand anders overdragen. Met **Nog een Fleet starten** start je een nieuwe Fleet.

Elk van deze opties opent het bijbehorende onderdeel van je account. Als de prijs verandert, zie je eerst het bedrag dat je moet bevestigen. Op een zelf gehoste Machine openen ze je account in een nieuw tabblad, waar je inlogt.

## Je Fleet iets vragen

Vraag in het tabblad Fleet 'wie kent iemand bij Acme?' of kies **De Fleet vragen** bij een organisatie in de [Graph](graph.md). De Machine van elk teamlid antwoordt volgens diens eigen deelregels en vraagt het teamlid eerst om toestemming als de regel dat voorschrijft.

## Automatische antwoorden in een Work Fleet

In een Standard Work Fleet beantwoordt je Machine zelf drie soorten vragen van teamgenoten: **wie iemand kent**, **context over afspraken** ('wie is deze gast?') en **wie gedeelde e-mails afhandelt**. Hij gebruikt alleen wat de [Team Graph](team-graph.md) al met je team deelt, nooit privé-, persoonlijke of gevoelige gesprekken. Elk antwoord verschijnt in het tabblad Fleet, onder **Activiteit**.

Je kunt een antwoordtype uitschakelen door het onder **Delen** op **Nooit** te zetten. Een regel die is ingesteld op **Vraag het me eerst**, werkt als **Altijd**. Zolang delen via Team Graph is uitgeschakeld, vraagt je Machine je eerst wie iemand kent en naar context over afspraken.

In voorzichtige Work Fleets, Vrienden en Family vraagt je Machine je nog steeds eerst. Voor warme introducties, overdrachten en gratis vragen gelden hun eigen regels.

## Inzichten van het team

Je Machine noteert hoe je team werkt op basis van klantgesprekken die de Team Graph al deelt, hooguit één keer per dag. Bijvoorbeeld: 'Terugbetalingsverzoeken worden beantwoord vanuit de supportinbox met de terugbetalingssjabloon.' De inzichten verschijnen in het paneel van je Work Fleet, onder **Inzichten van het team**, en zijn zichtbaar voor iedereen in de Fleet. Elk inzicht wordt ook geregistreerd onder **Activiteit**. Er wordt niemand eerst om toestemming gevraagd.

- Alleen gesprekken waaraan iemand uit je team heeft bijgedragen. Nooit privé-, persoonlijke of gevoelige gesprekken.
- Alleen informatie die voor meerdere klanten geldt: een proces, tool, schrijfstijl of wie wat afhandelt. Nooit iets over één klant, feedback op je eigen product, namen, adressen, nummers of citaten.
- Inzichten waar je Machine niet zeker van is, worden weggelaten.

Je Machine gebruikt relevante inzichten wanneer hij een Work-to-do voor dit bedrijf maakt. Je eigen feiten, regels en skills gaan voor, en persoonlijke to-do's maken er nooit gebruik van. Bij een to-do waarin een inzicht is gebruikt, staat dat erbij, bijvoorbeeld: 'Teaminzicht gebruikt: terugbetalingen worden afgehandeld vanuit de supportinbox.' Tik daar op **Verwijderen** om het inzicht voor de hele Fleet te verwijderen.

Iedereen in de Fleet kan een inzicht **Verwijderen**. Het is dan voor iedereen weg en wordt niet opnieuw aangemaakt. Je kunt dit uitschakelen met **Aanbieden om inzichten te delen** onder Instellingen, Beveiliging. Voorzichtige Work Fleets ontvangen geen inzichten.

## Teambrief

Kies **Dagelijks** of **Wekelijks** voor **Teambrief** in het tabblad Fleet, onder **Delen**. Je Machine vraagt dan de Machines van je teamgenoten om aantallen en datums. Zaken die je aandacht nodig hebben, verschijnen bij To-do's onder Werk: een klant die op een teamgenoot wacht, een bedrijf waar twee weken of langer niets is gebeurd, twee teamleden die dezelfde mensen mailen of een gedeelde afspraak.

- In een to-do staat op wie je wacht, sinds wanneer, wat diegene heeft gevraagd en wat er op het spel staat, bijvoorbeeld een lopend project. Als er niets specifieks te melden is, blijft het bij een regel in de briefing en wordt het geen to-do.
- Het bedrijf en de teamgenoten linken naar hun pagina's. **Details** toont wat ze hebben geschreven (tik erop om het te lezen), wat er op het spel staat, wie van het team contact heeft en hun recentste gesprekken. Alleen informatie die de [Team Graph](team-graph.md) deelt.
- Staat wat ze hebben geschreven alleen in de e-mail van een teamgenoot, dan staat in de to-do wie je ernaar kunt vragen.
- Met **Het team vragen** stuur je ze een vooraf ingevulde vraag. Hun antwoorden verschijnen bij de to-do.
- Met **Niet nodig** sluit je de to-do. De briefing leert hiervan. De to-do verschijnt alleen opnieuw als er iets nieuws is.
- Zodra iemand antwoordt of de taak oppakt, wordt de to-do automatisch gesloten. Een to-do over een bedrijf waarvoor je al een to-do hebt, wordt daaraan toegevoegd.

## Briefverzoeken

Een teamgenoot met de teambrief ingeschakeld vraagt je Machine elke ochtend om aantallen en datums. In een Work Fleet antwoordt je Machine zelf, met alleen informatie die de [Team Graph](team-graph.md) al deelt. Zolang delen via Team Graph is uitgeschakeld, antwoordt je Machine niet. Elk antwoord verschijnt in het tabblad Fleet, onder **Activiteit**, nooit als to-do of melding.

Je kunt dit uitschakelen met **Mijn briefingfeiten delen met het team** in het tabblad Fleet, onder **Delen**. In de briefing staat dan dat je niet hebt geantwoord.

In een voorzichtige Fleet verschijnen verzoeken in het tabblad Fleet, onder **Briefverzoeken**. Kies **Eén keer delen**, **Altijd delen**, **Weigeren** of **Nooit**. Er wordt niets gedeeld tot je een keuze maakt. Verzoeken waarop je niet reageert, verlopen.

## Team Graph

In een Work Fleet wordt klantwerk met je team gedeeld nadat je het hebt bekeken. Bekijk [Team Graph](team-graph.md).

## Gedeelde koppelingen

Een eigenaar of beheerder kan Stripe of Intercom eenmalig koppelen en delen met het team, via **Gedeelde koppelingen** in het tabblad Fleet. Teamgenoten kunnen de koppeling bekijken, maar niet wijzigen. Ze zien ook wie hem heeft gedeeld. Alleen beheerders kunnen de koppeling wijzigen of het delen stopzetten. Bekijk [Stripe](stripe.md) en [Intercom](intercom.md).

## Wat je Machine beantwoordt

Stel dit per Fleet in via het paneel Delen. Bekijk [Deelregels](sharing-rules.md). **Instellingen** bevat een snelkoppeling: **Fleet-regels**.

## Inloggen met je bedrijfsaccount

Laat teamgenoten deelnemen met hun bedrijfsaccount. In een gehoste Work Fleet kan een eigenaar of beheerder die is ingelogd met Google Workspace of Microsoft 365 **Inloggen met bedrijfsaccount** inschakelen op de Accountpagina.

Teamgenoten die inloggen met het domein van hun bedrijf zien **Aanvragen om deel te nemen**. Een eigenaar of beheerder moet elk verzoek **Goedkeuren**. Persoonlijke Gmail- en Outlook.com-accounts tellen nooit mee.

Als je iemand uit de Fleet verwijdert, wordt diegene overal uitgelogd.

Bekijk [Abonnementen en facturering](plans-and-billing.md) en [Vrienden en het Network](friends.md) om lid te worden van een Fleet, er een te starten of een Machine op je eigen computer te koppelen.

## Voor eigenaren en beheerders

Met **Beheren** in het tabblad Fleet zie je elke Fleet die je beheert, met de leden, hun rollen en de uitnodigingen. Op een gehoste Machine kun je daar mensen uitnodigen, rollen wijzigen, mensen verwijderen en verzoeken om deel te nemen afhandelen. Als een wijziging invloed heeft op de prijs, wordt eerst je account geopend om de wijziging te bevestigen. Op een zelf gehoste Machine zie je wie er lid is, met een link naar de instellingen van die Fleet in je account. Daar beheer je de leden en uitnodigingen.

**Fleet-instellingen**, onder de naam van elke Fleet in het paneel en bij Beheren, opent de instellingen van die Fleet in je account. Daar vind je gedeelde koppelingen, beveiliging, inloggen met je bedrijfsaccount, welke Machine antwoordt en deze twee onderdelen:

- **Recent verwijderd**: iedereen die is verwijderd of de Fleet heeft verlaten. 'Verwijderd, bevestigd' betekent dat hun Machine de werkgegevens heeft verwijderd en dat ze overal zijn uitgelogd. Tot die tijd staat er **In behandeling**, met de reden.
- **Activiteit**: wie wat heeft gedaan en wanneer: uitnodigingen, deelname, verwijderingen, rollen, gehoste Machines, facturering, gedeelde koppelingen en goedkeuringen. Ook elke keer dat ons supportteam een rapport van een lid z'n Machine of de logboeken ervan heeft bekeken. Nooit de inhoud van berichten. Met **CSV downloaden** exporteer je de gegevens. Ze worden 12 maanden bewaard.

**Vraag het me voordat je de Machine van een lid start**, voor de eigenaar: staat dit aan, dan wacht de Machine van een nieuw lid op je toestemming, ook in een gratis Fleet. Staat het uit, dan start de Machine in een gratis Fleet meteen en krijg je een melding. Voor een Machine die geld kost, moet je altijd eerst het bedrag bevestigen.

Na **Stoppen met delen** staat er bij een gedeelde koppeling 'Verwijderd, bevestigd' zodra geen enkele Machine er meer toegang toe heeft.
