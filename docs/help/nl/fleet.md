---
title: Fleets
area: fleet
summary: Een Werk-Fleet voor je team, een Familie-Fleet voor thuis. Machines die elkaar helpen, volgens jouw deelregels.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: f75a79e685f3a0cc
---
Met een Fleet kan je Machine via The Machine Network samenwerken met de Machines van je team, familie of vrienden. Wat ze elkaar vertellen, is end-to-end versleuteld. Je Machine antwoordt alleen volgens jouw regels.

## Soorten Fleets

- **Werk-Fleet**: je team. Draag werk over, vraag **wie iemand kent**, laat je in contact brengen en ontvang een teambrief.
- **Familie-Fleet**: voor maximaal 6 mensen. Zie wanneer iedereen vrij is, deel to-do's en plannen en stel vragen aan elkaars Machine. Gratis; voor gehoste Machines in de Fleet geldt een familietarief. Zie [Familie](family.md).
- **Vrienden**: iedereen op The Machine, één voor één. Gratis. Zie [Vrienden](friends.md).

## Het Fleet-tabblad

Je ziet dit tabblad zodra je in een Fleet zit. Er is een paneel voor elke Fleet, gevolgd door Vrienden, Network, Delen en Activiteit. Eigenaren en admins zien ook **Beheren**. Een Werk-Fleet die zijn Graph deelt, toont ook **Wat gedeeld wordt**.

## Kosten, een Fleet verlaten en een Fleet starten

Onder de naam van elke Fleet toont **Wat het kost** het aantal plaatsen, wie voor je Machine betaalt en, voor de eigenaar, de kaart en facturen van de Fleet. Met **Deze Fleet verlaten** verlaat je de Fleet. Een eigenaar moet de Fleet eerst aan iemand anders overdragen. Met **Nog een Fleet starten** start je een nieuwe Fleet.

Elke optie opent die stap in je account. Bij een prijswijziging zie je eerst het bedrag dat je moet bevestigen. Op een zelfgehoste Machine openen ze je account in een nieuw tabblad, waar je inlogt.

## Stel je Fleet een vraag

Vraag 'wie kent iemand bij Acme?' via het Fleet-tabblad, of kies **De Fleet vragen** bij een organisatie in de [Graph](graph.md). De Machine van elke teamgenoot antwoordt volgens diens eigen deelregels en vraagt het eerst aan diegene als de regel dat voorschrijft.

Gebruik voor andere vragen **Vraag maar raak** in het paneel van je Werk-Fleet. Elke teamgenoot krijgt een conceptantwoord op basis van diens eigen werkaccounts. Er komt pas iets terug als diegene het verstuurt.

## Automatische antwoorden in een Werk-Fleet

In een Standard Werk-Fleet beantwoordt je Machine zelf drie soorten vragen van teamgenoten: **wie iemand kent**, **meetingcontext** ('wie is deze gast?') en **wie gedeelde e-mails afhandelt**. Je Machine gebruikt alleen wat de [Team-Graph](team-graph.md) al met je team deelt, nooit privé-, persoonlijke of gevoelige gesprekken. Elk antwoord verschijnt in het Fleet-tabblad, onder **Activiteit**.

Je kunt een soort vraag uitschakelen door die onder **Delen** op **Nooit** te zetten. Een regel die is ingesteld op **Vraag het me eerst**, werkt als **Altijd**. Als delen via de Team-Graph uitstaat, vraagt je Machine eerst aan jou wie iemand kent en de meetingcontext.

In Voorzichtige Werk-Fleets, Vrienden en Familie-Fleets wordt het nog steeds eerst aan jou gevraagd. Voor warme introducties, overdrachten en gratis vragen gelden hun eigen regels.

## Inzichten van het team

Je Machine legt vast hoe je team werkt, op basis van klantgesprekken die de Team-Graph al deelt. Dat gebeurt hooguit één keer per dag. Bijvoorbeeld: 'Terugbetalingsverzoeken worden beantwoord vanuit de supportinbox met de terugbetalingssjabloon.' Ze verschijnen in het paneel van je Werk-Fleet, onder **Inzichten van het team**, en zijn zichtbaar voor iedereen in de Fleet. Elk inzicht wordt ook geregistreerd onder **Activiteit**. Er wordt niets eerst aan je gevraagd.

- Alleen gesprekken waaraan iemand uit je team heeft bijgedragen. Nooit privé-, persoonlijke of gevoelige gesprekken.
- Alleen informatie die voor meerdere klanten geldt: een proces, een tool, een schrijfstijl of wie wat afhandelt. Nooit iets over één klant, feedback op je eigen product, namen, adressen, nummers of citaten.
- Inzichten waar je Machine niet zeker van is, worden weggelaten.

Je Machine gebruikt passende inzichten wanneer hij een Werk-to-do voor dit bedrijf voorbereidt. Je eigen feiten, regels en skills gaan voor. Persoonlijke to-do's maken er nooit gebruik van. Bij een to-do die een inzicht gebruikt, staat dat erbij, bijvoorbeeld: 'Teaminzicht gebruikt: terugbetalingen worden verstuurd vanuit de supportinbox.' Tik daar op **Verwijderen** om het inzicht voor de hele Fleet te verwijderen.

Iedereen in de Fleet kan een inzicht **Verwijderen**. Het verdwijnt dan voor iedereen en wordt niet opnieuw aangemaakt. Je kunt dit uitschakelen via **Aanbieden om inzichten te delen** onder Instellingen, Beveiliging. Voorzichtige Werk-Fleets krijgen geen inzichten.

## Teambrief

Kies **Dagelijks** of **Wekelijks** voor **Teambrief** in het Fleet-tabblad, onder **Delen**. Je Machine vraagt dan de Machines van je teamgenoten om aantallen en datums. Wat je aandacht nodig heeft, verschijnt onder Werk bij je to-do's: een klant die op een teamgenoot wacht, een bedrijf waar al twee weken of langer niets gebeurt, twee teamgenoten die dezelfde mensen mailen, of een gedeelde meeting.

- In een to-do staat op wie of wat er gewacht wordt, sinds wanneer, wat diegene heeft gevraagd en wat er op het spel staat, zoals een lopend project. Als er niets concreets te melden is, blijft het een regel in de teambrief en wordt het geen to-do.
- Het bedrijf en de teamgenoten linken naar hun pagina's. **Details** toont wat ze hebben geschreven (tik erop om het te lezen), wat er op het spel staat, wie uit het team contact heeft en hun recentste gesprekken. Je ziet alleen wat de [Team-Graph](team-graph.md) deelt.
- Als wat diegene heeft geschreven alleen in de e-mail van een teamgenoot staat, vermeldt de to-do aan wie je het kunt vragen.
- Met **Het team vragen** stuur je hun een vooraf ingevulde vraag. Hun antwoorden verschijnen bij de to-do.
- **Niet nodig** sluit de to-do. De teambrief leert hiervan. De to-do komt alleen terug als er iets nieuws is.
- Zodra iemand antwoordt of de taak oppakt, wordt de to-do automatisch gesloten. Een to-do over een bedrijf waarvoor je al een to-do hebt, wordt daaraan toegevoegd.

## Briefingverzoeken

Een teamgenoot met de teambrief ingeschakeld vraagt je Machine elke ochtend om aantallen en datums. In een Werk-Fleet antwoordt je Machine automatisch, alleen met informatie die de [Team-Graph](team-graph.md) al deelt. Als delen via de Team-Graph uitstaat, antwoordt je Machine niet. Elk antwoord verschijnt in het Fleet-tabblad, onder **Activiteit**, nooit als to-do of melding.

Schakel **Mijn briefingfeiten delen met het team** uit in het Fleet-tabblad, onder **Delen**, om dit te stoppen. In hun teambrief staat dan dat je niet hebt geantwoord.

In een Voorzichtige Fleet vind je verzoeken in het Fleet-tabblad, onder **Briefingverzoeken**. Kies **Eén keer delen**, **Altijd delen**, **Weigeren** of **Nooit**. Er wordt niets gedeeld totdat je een keuze maakt. Verzoeken waarop je niet reageert, verlopen.

## Team-Graph

In een Werk-Fleet wordt werk voor klanten met je team gedeeld nadat je het hebt gecontroleerd. Zie [Team-Graph](team-graph.md).

## Gedeelde koppelingen

Een eigenaar of admin kan Stripe of Intercom één keer koppelen en met het team delen via **Gedeelde koppelingen** in het Fleet-tabblad. Teamgenoten kunnen de koppeling bekijken, maar niet aanpassen. Ze zien ook wie hem heeft gedeeld. Alleen admins kunnen hem aanpassen of stoppen. Zie [Stripe](stripe.md) en [Intercom](intercom.md).

## Wat je Machine beantwoordt

Stel dit per Fleet in via het paneel Delen. Zie [Regels voor delen](sharing-rules.md). Onder **Instellingen** vind je een snelkoppeling: **Fleet-regels**.

## Inloggen met je bedrijfsaccount

Laat teamgenoten deelnemen met hun bedrijfsaccount. In een gehoste Werk-Fleet kan een eigenaar of admin die is ingelogd met Google Workspace of Microsoft 365 **Inloggen met bedrijfsaccount** inschakelen op de accountpagina.

Teamgenoten die inloggen met dat bedrijfsdomein zien **Deelname aanvragen**. Een eigenaar of admin moet elke aanvraag **Goedkeuren**. Persoonlijke Gmail- en Outlook.com-accounts tellen nooit mee.

Als je iemand uit de Fleet verwijdert, wordt diegene overal uitgelogd.

Zie [Abonnementen en facturatie](plans-and-billing.md) en [Vrienden en het Network](friends.md) om lid te worden van een Fleet, er een te starten of een Machine op je eigen computer te koppelen.

## Voor eigenaren en admins

Met **Beheren** in het Fleet-tabblad zie je elke Fleet die je beheert, met de leden, hun rollen en de uitnodigingen. Op een gehoste Machine kun je daar mensen uitnodigen, rollen wijzigen, mensen verwijderen en deelnameverzoeken beantwoorden. Als een wijziging gevolgen heeft voor de prijs, wordt je account geopend zodat je die eerst kunt bevestigen. Op een zelfgehoste Machine zie je wie er lid is, met een link naar de instellingen van die Fleet in je account. Daar beheer je de leden en uitnodigingen.

**Fleet-instellingen** staat onder de naam van elke Fleet in het bijbehorende paneel en in Beheren. Hiermee open je de instellingen van die Fleet in je account: gedeelde koppelingen, beveiliging, inloggen met een bedrijfsaccount, welke Machine antwoordt en deze twee onderdelen:

- **Onlangs verwijderd**: iedereen die is verwijderd of de Fleet heeft verlaten. 'Verwijderd, bevestigd' betekent dat diens Machine de werkgegevens heeft verwijderd en diegene overal is uitgelogd. Tot die tijd staat er **In behandeling** met de reden.
- **Activiteit**: wie wat heeft gedaan en wanneer: uitnodigingen, deelname, verwijderingen, rollen, gehoste Machines, facturering, gedeelde koppelingen en goedkeuringen. Ook elke keer dat ons supportteam het Machine-rapport of de logboeken van een lid heeft bekeken. Nooit de inhoud van berichten. Met **CSV downloaden** exporteer je de gegevens. Ze worden 12 maanden bewaard.

**Eerst toestemming vragen voordat de Machine van een lid wordt gestart** is een instelling voor de eigenaar. Staat die aan, dan wacht de Machine van een nieuw lid op je goedkeuring, ook in een gratis Fleet. Staat die uit, dan start de Machine in een gratis Fleet meteen en krijg je een melding. Een Machine die geld kost, wacht altijd op je bevestiging van het bedrag.

Nadat je **Stoppen met delen** hebt gekozen, staat er bij een gedeelde koppeling 'Verwijderd, bevestigd' zodra elke Machine de toegang ertoe kwijt is.
