---
title: Fleets
area: fleet
summary: Een Werk-Fleet voor je team, een Familie-Fleet voor thuis. Machines die elkaar helpen, volgens jouw deelregels.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 17927ccd0e4aa40d
---
Met een Fleet werkt je Machine samen met de Machines van je team, familie of vrienden via The Machine Network. Alles wat ze elkaar vertellen, is end-to-end versleuteld. Je Machine reageert alleen volgens jouw regels.

## Soorten Fleets

- **Werk-Fleet**: voor je team. Draag werk over, vraag **wie iemand kent**, krijg introducties en een teambriefing.
- **Familie-Fleet**: voor maximaal 6 mensen. Zie wanneer iedereen vrij is, deel to-do's en plannen en stel vragen aan elkaars Machine. Gratis; gehoste Machines in de Fleet hebben een familietarief. Zie [Familie](family.md).
- **Vrienden**: afzonderlijk contact met iedereen op The Machine. Gratis. Zie [Vrienden](friends.md).

## Het tabblad Fleet

Het tabblad verschijnt zodra je deel uitmaakt van een Fleet. Je ziet een paneel voor elke Fleet, gevolgd door Vrienden, Network, Delen en Activiteit. Eigenaren en beheerders zien ook **Beheren**. Een Werk-Fleet die de Graph deelt, heeft ook **Wat gedeeld wordt**.

## Kosten, een Fleet verlaten en een Fleet starten

Onder de naam van elke Fleet laat **Wat het kost** zien hoeveel plaatsen er zijn, wie voor je Machine betaalt en, voor de eigenaar, de betaalkaart en facturen van de Fleet. Met **Deze Fleet verlaten** verlaat je de Fleet. Een eigenaar moet de Fleet eerst aan iemand anders overdragen. Met **Nog een Fleet starten** start je een nieuwe Fleet.

Elk van deze opties opent de betreffende pagina van je account. Als de prijs verandert, zie je eerst het bedrag dat je moet bevestigen. Op een zelfgehoste Machine openen ze je account in een nieuw tabblad, waar je inlogt.

## Stel je Fleet een vraag

Vraag ‘wie kent iemand bij Acme?’ op het tabblad Fleet, of kies **De Fleet vragen** bij een organisatie in de [Graph](graph.md). De Machine van elke teamgenoot antwoordt volgens diens eigen deelregels en vraagt het eerst aan diegene als de regel dat voorschrijft.

Gebruik voor andere vragen **Vraag maar raak** in het paneel van je Werk-Fleet. Elke teamgenoot krijgt een conceptantwoord op basis van diens eigen werkaccounts. Het antwoord wordt pas gedeeld als diegene het verstuurt. Het concept bevat alleen informatie waarover diegene heeft geschreven of heeft gesproken tijdens meetings. Mail die alleen is binnengekomen, zoals een nieuwsbrief of een CC, wordt wel gevonden, maar levert geen concept op.

## Automatische antwoorden in een Werk-Fleet

In een standaard Werk-Fleet beantwoordt je Machine zelf drie soorten vragen van teamgenoten: **wie iemand kent**, **meetingcontext** (‘wie is deze gast?’) en **wie gedeelde e-mails afhandelt**. Je Machine gebruikt alleen informatie die de [Team-Graph](team-graph.md) al met je team deelt, nooit privé-, persoonlijke of gevoelige gesprekken. Elk antwoord verschijnt op het tabblad Fleet, onder **Activiteit**.

Wil je een antwoord stoppen, stel dan **Nooit** in onder **Delen**. Een regel die is ingesteld op **Vraag het me eerst**, werkt hetzelfde als **Altijd**. Als delen via Team Graph uitstaat, vraagt je Machine je eerst wie iemand kent en naar meetingcontext.

Voorzichtige Werk-Fleets, Vrienden en Familie vragen het nog steeds eerst aan je. Voor warme introducties, overdrachten en gratis vragen gelden hun eigen regels.

## Inzichten van het team

Je Machine legt maximaal één keer per dag vast hoe je team werkt, op basis van klantgesprekken die de Team Graph al deelt. Bijvoorbeeld: ‘Terugbetalingsverzoeken worden beantwoord vanuit de supportinbox met de template voor terugbetalingen.’ De inzichten verschijnen in het paneel van je Werk-Fleet, onder **Inzichten van het team**, en zijn zichtbaar voor iedereen in de Fleet. Elk inzicht wordt ook geregistreerd onder **Activiteit**. Je wordt hier niet eerst om toestemming gevraagd.

- Alleen gesprekken waaraan iemand van je team heeft bijgedragen. Nooit privé-, persoonlijke of gevoelige gesprekken.
- Alleen informatie die voor meerdere klanten geldt: een werkwijze, een tool, een schrijfstijl of wie wat afhandelt. Nooit iets over één klant, feedback over je eigen product of namen, adressen, nummers of citaten.
- Inzichten waar je Machine niet zeker van is, worden weggelaten.

Je Machine gebruikt relevante inzichten wanneer hij een Werk-to-do voor dit bedrijf voorbereidt. Je eigen feiten, regels en skills gaan voor. Persoonlijke to-do's gebruiken deze inzichten nooit. Bij een to-do waarvoor een inzicht is gebruikt, staat dat erbij, bijvoorbeeld: ‘Teaminzicht gebruikt: terugbetalingen worden verstuurd vanuit de supportinbox.’ Tik daar op **Verwijderen** om het inzicht voor de hele Fleet te verwijderen.

Iedereen in de Fleet kan een inzicht **Verwijderen**. Het verdwijnt voor iedereen en wordt niet opnieuw aangemaakt. Wil je dit stoppen, schakel dan **Aanbieden om inzichten te delen** uit via Instellingen, Beveiliging. Voorzichtige Werk-Fleets krijgen geen inzichten.

## Teambriefing

Kies **Dagelijks** of **Wekelijks** voor **Teambriefing** op het tabblad Fleet, onder **Delen**. Je Machine vraagt dan de Machines van je teamgenoten om aantallen en datums. Zaken die aandacht nodig hebben, komen bij To-do's onder Werk te staan: een klant die wacht op een teamgenoot, een bedrijf waarvan al minstens twee weken niets is gehoord, twee teamleden die dezelfde mensen mailen of een gedeelde meeting.

- Een to-do vermeldt op wie je wacht, sinds wanneer, wat diegene heeft gevraagd en wat er op het spel staat, bijvoorbeeld een openstaand project. Als er niets specifieks te melden is, blijft het een regel in de briefing en wordt het geen to-do.
- Het bedrijf en de teamgenoten linken naar hun pagina's. **Details** toont wat ze hebben geschreven (tik erop om het te lezen), wat er op het spel staat, wie van het team contact heeft en de meest recente gesprekken. Alleen informatie die de [Team-Graph](team-graph.md) deelt, wordt getoond.
- Staat wat ze hebben geschreven alleen in de mail van een teamgenoot, dan vermeldt de to-do wie je het kunt vragen.
- Met **Het team vragen** stuur je een vooraf ingevulde vraag. De antwoorden verschijnen bij de to-do.
- Met **Niet nodig** sluit je de to-do. De briefing leert hiervan. De to-do komt alleen terug als er iets nieuws is.
- Zodra iemand antwoordt of de taak oppakt, wordt de to-do automatisch gesloten. Een to-do over een bedrijf waarvoor je al een to-do hebt, wordt daaraan toegevoegd.

## Briefingverzoeken

Elke ochtend vraagt een teamgenoot met de teambriefing ingeschakeld je Machine om aantallen en datums. In een Werk-Fleet antwoordt je Machine automatisch, uitsluitend met informatie die de [Team-Graph](team-graph.md) al deelt. Er wordt niets gedeeld als delen via Team Graph uitstaat. Elk antwoord verschijnt op het tabblad Fleet, onder **Activiteit**, nooit als to-do of melding.

Wil je dit stoppen, schakel dan **Mijn briefingfeiten delen met het team** uit op het tabblad Fleet, onder **Delen**. In de briefing staat dan dat je niet hebt geantwoord.

In een Voorzichtige Fleet verschijnen verzoeken op het tabblad Fleet, onder **Briefingverzoeken**. Kies **Eén keer delen**, **Altijd delen**, **Weigeren** of **Nooit**. Er wordt niets gedeeld voordat je een keuze maakt. Verzoeken waarop je niet reageert, verlopen.

## Team Graph

In een Werk-Fleet wordt klantwerk met je team gedeeld nadat je het hebt gecontroleerd. Zie [Team-Graph](team-graph.md).

## Gedeelde koppelingen

Een eigenaar of beheerder kan Stripe of Intercom één keer koppelen en vervolgens delen met het team via **Gedeelde koppelingen** op het tabblad Fleet. Teamgenoten kunnen de koppeling bekijken, maar niet wijzigen. Ze zien ook wie hem heeft gedeeld. Alleen beheerders kunnen de koppeling wijzigen of stoppen met delen. Zie [Stripe](stripe.md) en [Intercom](intercom.md).

## Wat je Machine beantwoordt

Stel dit per Fleet in op het tabblad Delen. Zie [Deelregels](sharing-rules.md). **Instellingen** bevat een snelkoppeling: **Fleet-regels**.

## Inloggen met een bedrijfsaccount

Laat teamgenoten deelnemen met hun bedrijfsaccount. In een gehoste Werk-Fleet kan een eigenaar of beheerder die is ingelogd met Google Workspace of Microsoft 365 **Inloggen met bedrijfsaccount** inschakelen op de accountpagina.

Teamgenoten die inloggen met dat bedrijfsdomein zien **Vragen om deel te nemen**. Een eigenaar of beheerder moet ieder verzoek **Goedkeuren**. Persoonlijke Gmail- en Outlook.com-accounts tellen niet mee.

Als je iemand uit de Fleet verwijdert, wordt diegene overal uitgelogd.

Zie [Abonnementen en facturatie](plans-and-billing.md) en [Vrienden en het Network](friends.md) als je wilt deelnemen aan een Fleet, er een wilt starten of een Machine op je eigen computer wilt koppelen.

## Voor eigenaren en beheerders

**Beheren** op het tabblad Fleet toont elke Fleet die je beheert, met de leden, hun rollen en de uitnodigingen. Op een gehoste Machine kun je daar mensen uitnodigen, rollen wijzigen, mensen verwijderen en verzoeken om deel te nemen beantwoorden. Als een wijziging invloed heeft op de prijs, opent je account zodat je die eerst kunt bevestigen. Op een zelfgehoste Machine zie je wie er deel van uitmaakt, met een link naar de instellingen van die Fleet in je account. Daar beheer je de leden en uitnodigingen.

**Fleet-instellingen**, onder de naam van elke Fleet in het paneel en in Beheren, opent de instellingen van die Fleet in je account: gedeelde koppelingen, beveiliging, inloggen met een bedrijfsaccount, welke Machine antwoord geeft en deze twee opties:

- **Recent verwijderd**: iedereen die is verwijderd of de Fleet heeft verlaten. ‘Verwijderd, bevestigd’ betekent dat de Machine van die persoon de werkgegevens heeft verwijderd en dat diegene overal is uitgelogd. Tot die tijd staat er **In behandeling**, met de reden.
- **Activiteit**: wie wat heeft gedaan en wanneer: uitnodigingen, deelnames, verwijderingen, rollen, gehoste Machines, facturering, gedeelde koppelingen en goedkeuringen. Ook elke keer dat ons supportteam het rapport van een lid over diens Machine of de logboeken heeft bekeken. Nooit de inhoud van berichten. Met **CSV downloaden** exporteer je de gegevens. Ze worden 12 maanden bewaard.

**Vraag het me voordat je de Machine van een lid start**, voor de eigenaar: als dit aanstaat, wacht de Machine van een nieuw lid op je goedkeuring, ook in een gratis Fleet. Staat dit uit, dan start de Machine in een gratis Fleet meteen en krijg je bericht. Bij een Machine die geld kost, moet je het bedrag altijd eerst bevestigen.

Na **Stoppen met delen** staat bij een gedeelde koppeling ‘Verwijderd, bevestigd’ zodra alle Machines er geen toegang meer toe hebben.
