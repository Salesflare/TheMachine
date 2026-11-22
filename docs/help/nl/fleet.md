---
title: Fleets
area: fleet
summary: Een Werk-Fleet voor je team, een Familie-Fleet voor thuis. Machines die elkaar helpen, volgens jullie deelregels.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 974bbbb54608efc3
---
Met een Fleet kan je Machine via The Machine Network samenwerken met de Machines van je team, familie of vrienden. Wat ze elkaar vertellen, is end-to-end versleuteld. Je Machine antwoordt alleen volgens jouw regels.

## Soorten Fleets

- **Werk-Fleet**: je team. Draag werk over, vraag **wie iemand kent**, krijg introducties en een teambriefing.
- **Familie-Fleet**: maximaal 6 personen. Gedeelde to-do's en plannen voor wanneer iedereen tijd heeft. Gratis; voor gehoste Machines geldt een familietarief. Bekijk [Familie](family.md).
- **Vrienden**: iedereen op The Machine, één voor één. Gratis. Bekijk [Vrienden](friends.md).

## Het tabblad Fleet

Dit tabblad verschijnt zodra je deelneemt aan een Fleet. Je ziet een paneel voor elke Fleet, gevolgd door Vrienden, Network, Delen en Activiteit. Eigenaren en beheerders zien ook **Beheren**. Een Werk-Fleet die zijn Graph deelt, heeft ook **Wat gedeeld wordt**.

## Kosten, een Fleet verlaten en een Fleet starten

Onder de naam van elke Fleet toont **Wat het kost** de plaatsen, wie betaalt voor je Machine en, voor de eigenaar, de kaart en facturen van de Fleet. Met **Deze Fleet verlaten** verlaat je de Fleet. Een eigenaar moet de Fleet eerst aan iemand anders overdragen. Met **Nog een Fleet starten** start je een nieuwe Fleet.

Elk van deze opties opent het betreffende deel van je account. Als de prijs verandert, zie je eerst het bedrag dat je moet bevestigen. Op een zelfgehoste Machine wordt je account geopend in een nieuw tabblad, waar je kunt inloggen.

## Stel je Fleet een vraag

Vraag 'wie kent iemand bij Acme?' vanaf het tabblad Fleet, of kies **De Fleet vragen** bij een organisatie in de [Graph](graph.md). De Machine van elk teamlid antwoordt volgens diens eigen deelregels en vraagt het eerst aan diegene als de regel dat voorschrijft.

Gebruik voor andere vragen **Vraag maar raak** in het paneel van je Werk-Fleet. Elk teamlid krijgt een conceptantwoord op basis van diens eigen werkaccounts. Er komt pas iets terug als diegene het verstuurt.

## Automatische antwoorden in een Werk-Fleet

In een standaard Werk-Fleet beantwoordt je Machine zelfstandig drie soorten vragen van teamleden: **wie iemand kent**, **meetingcontext** ('wie is deze gast?') en **wie gedeelde e-mails afhandelt**. Je Machine gebruikt alleen wat de [Team-Graph](team-graph.md) al met je team deelt, nooit privé-, persoonlijke of gevoelige gesprekken. Elk antwoord verschijnt op het tabblad Fleet, onder **Activiteit**.

Je kunt deze functie voor een vraagtype uitschakelen door het onder **Delen** op **Nooit** te zetten. Een regel die is ingesteld op **Vraag het me eerst**, werkt als **Altijd**. Als delen via Team-Graph is uitgeschakeld, vraagt je Machine het je eerst bij wie iemand kent en meetingcontext.

Voorzichtige Werk-Fleets, Vrienden en Familie vragen het je nog steeds eerst. Voor warme introducties, overdrachten en vrije vragen gelden hun eigen regels.

## Inzichten van het team

Je Machine legt maximaal één keer per dag vast hoe je team werkt, op basis van klantgesprekken die de Team-Graph al deelt. Bijvoorbeeld: 'Terugbetalingsverzoeken worden beantwoord vanuit de supportinbox met de terugbetalingssjabloon.' Iedereen in de Fleet ziet ze in het paneel van je Werk-Fleet onder **Inzichten van het team**. Elk inzicht wordt ook vastgelegd onder **Activiteit**. Er wordt niets eerst aan je gevraagd.

- Alleen gesprekken waaraan iemand uit je team heeft meegeschreven. Nooit privé-, persoonlijke of gevoelige gesprekken.
- Alleen informatie die voor meerdere klanten geldt: een proces, een tool, een schrijfstijl of wie wat afhandelt. Nooit iets over één klant, nooit feedback over je eigen product en nooit namen, adressen, nummers of citaten.
- Inzichten waar je Machine niet zeker van is, worden weggelaten.

Je Machine gebruikt relevante inzichten wanneer hij een Werk-to-do voor dit bedrijf voorbereidt. Je eigen feiten, regels en skills gaan voor. Privé-to-do's gebruiken ze nooit. Bij een to-do waarin een inzicht is gebruikt, staat dat erbij, bijvoorbeeld: 'Teaminzicht gebruikt: terugbetalingen worden verstuurd vanuit de supportinbox.' Tik daar op **Verwijderen** om het inzicht voor de hele Fleet te verwijderen.

Iedereen in de Fleet kan een inzicht **Verwijderen**. Het verdwijnt dan voor iedereen en wordt niet opnieuw aangemaakt. Zet **Aanbieden om inzichten te delen** uit via Instellingen, Beveiliging om dit uit te schakelen. Voorzichtige Werk-Fleets krijgen geen inzichten.

## Teambriefing

Kies **Dagelijks** of **Wekelijks** bij **Teambriefing** op het tabblad Fleet, onder **Delen**. Je Machine vraagt dan de Machines van je teamgenoten om aantallen en datums. Wat aandacht nodig heeft, komt bij To-do's onder Werk te staan: een klant die op een teamgenoot wacht, een bedrijf waar al twee weken of langer niets is gebeurd, twee teamleden die dezelfde mensen benaderen of een gedeelde meeting.

- Een to-do vermeldt op wie iets wacht, sinds wanneer, wat diegene heeft gevraagd en wat er op het spel staat, zoals een lopend project. Als er niets concreets te melden is, blijft het een regel in de briefing en wordt het geen to-do.
- Het bedrijf en de teamgenoten linken naar hun pagina's. **Details** toont wat ze hebben geschreven (tik erop om het te lezen), wat er op het spel staat, wie uit het team contact heeft en hun nieuwste gesprekken. Dit is alleen informatie die de [Team-Graph](team-graph.md) deelt.
- Als wat ze hebben geschreven alleen in de e-mail van een teamgenoot staat, vermeldt de to-do aan wie je het kunt vragen.
- Met **Het team vragen** stuur je hun een vooraf ingevulde vraag hierover. Hun antwoorden verschijnen bij de to-do.
- **Niet nodig** sluit de to-do af en de briefing leert hiervan. De to-do komt alleen terug als er iets nieuws is.
- Zodra iemand antwoordt of het oppakt, wordt de to-do automatisch gesloten. Een to-do over een bedrijf waarvoor je al een to-do hebt, wordt daaraan toegevoegd.

## Briefingverzoeken

Een teamgenoot met de teambriefing ingeschakeld vraagt je Machine elke ochtend om aantallen en datums. In een Werk-Fleet antwoordt je Machine zelfstandig, uitsluitend met informatie die de [Team-Graph](team-graph.md) al deelt. Je Machine antwoordt niet als delen via Team-Graph is uitgeschakeld. Elk antwoord verschijnt op het tabblad Fleet, onder **Activiteit**, nooit als to-do of melding.

Zet **Mijn briefingfeiten delen met het team** uit op het tabblad Fleet, onder **Delen**, om dit te stoppen. In hun briefing staat dan dat je niet hebt geantwoord.

In een Voorzichtige Fleet staan verzoeken op het tabblad Fleet onder **Briefingverzoeken**. Kies **Eén keer delen**, **Altijd delen**, **Weigeren** of **Nooit**. Er wordt niets gedeeld voordat je een keuze maakt. Verzoeken waarop je niet reageert, verlopen.

## Team-Graph

In een Werk-Fleet wordt klantwerk met je team gedeeld nadat je het hebt gecontroleerd. Bekijk [Team-Graph](team-graph.md).

## Gedeelde koppelingen

Een eigenaar of beheerder kan Stripe of Intercom één keer koppelen en deze met het team delen via **Gedeelde koppelingen** op het tabblad Fleet. Teamgenoten kunnen de koppeling bekijken, maar niet wijzigen. Ze zien ook wie deze heeft gedeeld. Alleen beheerders kunnen de koppeling wijzigen of het delen stoppen. Bekijk [Stripe](stripe.md) en [Intercom](intercom.md).

## Wat je Machine beantwoordt

Stel dit per Fleet in via het paneel Delen. Bekijk [Deelregels](sharing-rules.md). In **Instellingen** staat een snelkoppeling: **Fleet-regels**.

## Bedrijfslogin

Laat teamgenoten deelnemen met hun bedrijfsaccount. In een gehoste Werk-Fleet kan een eigenaar of beheerder die is ingelogd met Google Workspace of Microsoft 365 **Bedrijfslogin** inschakelen op de Accountpagina.

Teamgenoten die inloggen met dat bedrijfsdomein zien **Vragen om lid te worden**. Een eigenaar of beheerder moet elke aanvraag **Goedkeuren**. Persoonlijke Gmail- en Outlook.com-accounts tellen nooit mee.

Als je iemand uit de Fleet verwijdert, wordt diegene overal uitgelogd.

Bekijk [Abonnementen en facturering](plans-and-billing.md) en [Vrienden en het Network](friends.md) om deel te nemen aan een Fleet, er een te starten of een Machine op je eigen computer te koppelen.

## Voor eigenaren en beheerders

Onder **Beheren** op het tabblad Fleet staan alle Fleets die je beheert, met de leden, hun rollen en de uitnodigingen. Op een gehoste Machine kun je daar mensen uitnodigen of verwijderen, rollen wijzigen en aanvragen om deel te nemen beantwoorden. Als een wijziging gevolgen heeft voor de prijs, wordt je account geopend zodat je deze eerst kunt bevestigen. Op een zelfgehoste Machine zie je wie er deel van uitmaakt, met een link naar de instellingen van die Fleet in je account. Daar beheer je de leden en uitnodigingen.

**Fleet-instellingen** opent de instellingen van die Fleet in je account. Je vindt deze onder de naam van elke Fleet in het paneel en onder Beheren. Je beheert er gedeelde koppelingen, beveiliging, inloggen met een bedrijfsaccount, welke Machine antwoordt en deze twee onderdelen:

- **Recent verwijderd**: iedereen die is verwijderd of de Fleet heeft verlaten. 'Verwijderd, bevestigd' betekent dat de Machine van die persoon de werkgegevens heeft verwijderd en dat diegene overal is uitgelogd. Tot die tijd staat er **In behandeling**, met de reden.
- **Activiteit**: wie wat heeft gedaan en wanneer: uitnodigingen, deelnames, verwijderingen, rollen, gehoste Machines, facturering, gedeelde koppelingen en goedkeuringen. Ook elke keer dat ons supportteam het rapport of de logboeken van de Machine van een lid heeft gelezen. Nooit de inhoud van berichten. Met **CSV downloaden** exporteer je de gegevens. Ze worden 12 maanden bewaard.

**Vraag het me voor de Machine van een lid start**, voor de eigenaar: staat dit aan, dan wacht de Machine van een nieuw lid op je toestemming, ook in een gratis Fleet. Staat het uit, dan start de Machine in een gratis Fleet meteen en krijg je bericht. Een Machine die geld kost, wacht altijd tot je het bedrag bevestigt.

Na **Stoppen met delen** krijgt een gedeelde koppeling de status 'Verwijderd, bevestigd' zodra elke Machine de toegang ertoe is kwijtgeraakt.
