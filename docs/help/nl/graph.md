---
title: De Graph
area: graph
summary: De personen, organisaties en projecten in je berichten, vanzelf up-to-date gehouden.
covers: tab:people
code: graph.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, enrichment.py, dashboard.html
order: 1
---
Je Machine bouwt een kaart van met wie je te maken hebt en wat er speelt, uit je berichten, afspraken en beslissingen. Je hoeft niets in te stellen, en alles blijft op je Machine.

## Personen

Iedereen met wie je contact hebt, de naaste eerst. De pagina van een persoon begint met de foto, naam, functie, organisatie en plaats, en één regel over hoe jullie contact hebben ("Praten dagelijks · laatst vr 23 okt · volgende afspraak di 27 okt"). Daaronder:

- **Contact**: telefoonnummers en e-mailadressen. Tik erop om te bellen of te schrijven, of **Kopiëren**.
- **Met jou**: wat die persoon voor jou is, Werk- of Privécontact, en je Familie of Fleet, met **Bekijk in Fleet**.
- **Ook op**: de andere plekken waar jullie praten. **Slack** opent die persoon in Slack, of je nieuwste Slack-thread met die persoon.
- **Personen** en **Projecten** waar die persoon bij hoort, **Open tussen jullie** (beloftes in beide richtingen, met **Gedaan** en **Laten vallen**), en de **Tijdlijn**.

De adressen en chats van iemand worden vanzelf samengevoegd als duidelijk is dat het één persoon is, zoals een werkadres met het eigen adres in CC.

De tabbladen **Werk** en **Privé** tonen alleen die contacten. **CSV downloaden**, onder het sorteermenu, bewaart het tabblad waarop je bent als spreadsheet, ook voor Organisaties en Projecten.

### Tijdlijn

Elke pagina van een persoon en organisatie heeft er een, nieuwste eerst: e-mail, afspraken en hun Zoom-samenvattingen, Intercom-gesprekken (open of gesloten, met **Openen in Intercom**), chats op WhatsApp, Telegram, Slack, LinkedIn en X, to-do's, beloftes en verplaatsingen van projecten. De labels bovenaan tonen één bron tegelijk. **Meer tonen** laadt oudere items.

Afspraken die nog moeten komen, staan apart bovenaan onder **Binnenkort**, de eerstvolgende eerst; **Alles wat eraan komt tonen** toont de rest. Een afspraak in meer dan één van je agenda's staat er één keer.

De tijdlijn van een organisatie heeft de berichten van de mensen daar en de Intercom-gesprekken van het domein. Je tijdlijnen zijn van jou: de Graph van het team toont alleen wat je deelregels toelaten.

Staat er op een pagina **Deze pagina kon niet laden.**, tik dan op **Opnieuw proberen**. Blijft dat zo, gebruik dan **Klopt er iets niet?** onderaan de pagina.

## Filteren en sorteren

**Filteren**, naast de tabbladen op Personen, Organisaties en Projecten, beperkt de lijst op eigenaar, tag, bord, fase, organisatie, waarde, verwachte sluitdatum en **Geen antwoord in 10+ dagen**. Personen en organisaties komen overeen via hun open projecten. Bij Projecten delen de lijst en het bord één filter.

De filters die je koos, staan boven de lijst, met **Wissen**. Het sorteermenu sorteert ook op **Waarde** en **Sluitdatum**. Je Machine doet het filteren, dus lange lijsten blijven snel. Op een telefoon openen de filters als een paneel.

## Team

**Team**, naast Van mij, toont wat je teamgenoten delen. Het heeft dezelfde tabbladen, hetzelfde sorteermenu en **Nieuwe persoon** of **Nieuwe organisatie** als Van mij; wat je toevoegt, is van jou. **Filteren** beperkt het op wie het deelde, een organisatie (Personen) of een status (Projecten). Bij Projecten kiezen **Van mij**, **Wacht op mij** en **Alle** dezelfde projecten als op een gedeeld bord.

## Eigenaar

In een Werk-Fleet heeft elke persoon, organisatie en elk project een eigenaar: **Eigenaar** onder Met jou op de pagina. Dat ben jij, tenzij je iemand uit je Werk-Fleet kiest. **Eigenaar** in Filteren toont alleen de jouwe, in de lijst en op het bord. Een kaart op een bord toont de naam van de eigenaar. Elke wijziging staat in de tijdlijn. Een record dat met je team gedeeld is, neemt de eigenaar mee, volgens dezelfde deelregels als de rest.

## Velden en tags

Klik onder Velden bij een persoon, organisatie of project op een waarde om ze te wijzigen: **Opslaan** of Enter bewaart ze, **Annuleren** of Escape laat ze zoals ze was, **Verwijderen** maakt ze leeg. **Velden beheren** voegt velden toe of verwijdert ze: **Nieuw veld** voegt er een toe voor alles van die soort: tekst, getal, datum of een keuze uit een lijst. **Verwijderen** haalt een veld weg voor allemaal.

**+ Tag** voegt een tag toe, zoals VIP of partner; **×** haalt hem weg. Tags staan in de lijsten en **Filteren** vindt ze. Een record dat met je team gedeeld is, neemt de velden en tags mee.

## Een spreadsheet importeren

**CSV importeren…**, onder het sorteermenu van Personen, Organisaties of Projecten, voegt een spreadsheet toe die als CSV bewaard is. Je Machine raadt welke kolom welke is uit de koppen en wat erin staat; je kunt elke kolom wijzigen.

Als je model kan draaien, controleert het de kolommen ook, in elke taal en hoe de koppen ook gespeld zijn, met een korte reden waar het niet zeker is. Het ziet alleen de koppen, een paar waarden per kolom en de cellen die de regels niet konden lezen, op je Machine zoals een review. Zonder model blijft de gok uit de koppen staan.

**Nakijken**, naast de voorgestelde correcties, toont eenvoudige correcties als voor en na: extra spaties, namen in hoofdletters, telefoonnummers in internationale vorm, tikfouten in e-mailadressen (gmial.com), websites als hun domein, datums en waarden in elk formaat ("€12k" is 12000), meerdere tags in één cel, een fase die anders gespeld is dan op het bord, en dezelfde rij twee keer.

Vink een soort of een enkele rij uit om ze te laten zoals ze is. Er wordt niets gecorrigeerd tenzij het aangevinkt is.

Het voorbeeld toont elke rij als nieuw, als overeenkomend met een rij die al in je Graph staat, of als overgeslagen, met waarom. Een overeenkomst is hetzelfde e-mailadres voor een persoon (anders dezelfde naam bij dezelfde organisatie), dezelfde website of naam voor een organisatie, en dezelfde naam voor een project.

**Importeren** voegt de nieuwe toe en vult de overeenkomsten aan; een lege cel verandert niets. **Ongedaan maken** meteen erna, of **Laatste import ongedaan maken** onder het sorteermenu, draait de laatste import terug zolang die records sindsdien niet gewijzigd zijn. Latere correcties blijven: als Ongedaan maken er een zou overschrijven, legt het uit waarom in plaats daarvan. Het bestand blijft op je Machine.

## Eén organisatie, meerdere websites

**⋯**, **Zelfde organisatie als…** op de pagina van een organisatie maakt ze deel van een andere, met haar personen, projecten en notities. **Website toevoegen…** voegt nog een website van haar toe, zoals haar .io naast haar .com: personen met een adres daar komen erbij, en de gegevens worden voor elke website opgezocht.

Ze staan onder **Websites**, elk met **Afsplitsen** om het ongedaan te maken. Latere wijzigingen aan de samengevoegde organisatie blijven. Organisaties die op dubbels lijken, staan onder **Zelfde organisatie?**: **Samenvoegen** of **Niet dezelfde**.

## Iemand of een organisatie toevoegen

**Nieuwe persoon** bovenaan Personen, **Nieuwe organisatie** bovenaan Organisaties, of op een telefoon **+** in de bovenste balk. Geef een naam, en voor een persoon een e-mailadres en organisatie als je die hebt; voor een organisatie de website. Staat er al iemand zoals die in je Graph, dan toont het formulier die eerst, zodat je die in plaats daarvan kunt openen. **Toevoegen** opent de nieuwe pagina.

Iemand die je toevoegt, blijft, ook zonder berichten. Het eerste bericht wordt aan die persoon gekoppeld. Een organisatie die je toevoegde, kun je verwijderen via het menu **⋯** zolang er niemand in zit.

## Over jou

Je eigen adressen en nummers, ook aliassen, zijn altijd jij, nooit iemand in je Graph. Zoek je naar jezelf, of voeg je een persoon toe met een van je adressen, dan opent **Over jou**, en een import slaat je eigen rij over.

Over jou toont je adressen met waar elk vandaan kwam; wijzig ze in **Instellingen**, onder Account. Een persoon die eerder van je eigen adres gemaakt is, gaat vanzelf naar Over jou, met een back-up op je Machine.

Om je eigen kaartje naar een teamgenoot of vriend te sturen, kies je **Mijn contactgegevens delen**. Zie [Een contact delen](share-contact.md).

## Foto

Klik op de foto op de pagina van een persoon of organisatie om ze te wijzigen: **Afbeelding uploaden**, kies er een die voor hen gevonden is, of **Foto verwijderen**. Ze blijft op je Machine.

## Notities

**Bewerken** op de pagina van een persoon of organisatie heeft een veld **Notities**, voor alles wat je wilt onthouden. Notities staan op de pagina en blijven bij samenvoegen.

## Iemand bewerken

**Bewerken**, bovenaan de pagina, wijzigt de naam, functie, organisatie, locatie, LinkedIn, telefoonnummers en e-mailadressen, wat die persoon voor jou is, en Werk of Privé. **Opslaan** bewaart het, **Annuleren** laat het zoals het was.

Je wijzigingen blijven, ook als de gegevens opnieuw opgezocht worden of een review iets anders leest, en bij **Samenvoegen** en **Ongedaan maken**. Maak een veld leeg om weer de opgezochte waarde te gebruiken. Een lege naam brengt de naam uit de berichten terug.

## Zelfde persoon?

Als twee personen misschien één persoon zijn, vraagt hun pagina of het dezelfde persoon is, en Personen toont ze onder **Zelfde persoon?**. **Samenvoegen** voegt ze samen, met al hun berichten, notities, rollen en projecten. **Niet dezelfde** houdt ze voorgoed apart.

**Alles samenvoegen** voegt elk paar in de lijst in één keer samen, behalve die je als **Niet dezelfde** markeerde. **Ongedaan maken** meteen erna splitst ze allemaal weer.

De pagina van een samengevoegde persoon toont waarom onder **Samengevoegd uit**. **Ongedaan maken** splitst ze weer.

Om zelf twee personen samen te voegen, open je er een, dan **⋯**, **Zelfde persoon als…** en kies je de andere.

## Functie en foto

Personen met een bedrijfsadres krijgen een functie, foto, LinkedIn en stad, opgezocht zoals [gegevens van organisaties](organization-data.md). Op een gehoste Machine worden alleen hun naam en het domein van hun bedrijf verstuurd. Zet het uit in **Instellingen**, onder Beveiliging: **Werkcontacten opzoeken**.

Je koppelingen vullen meer aan terwijl ze draaien, met wat ze al lazen en zonder iets extra te vragen: een functie, telefoonnummer en tijdzone uit Slack, een bio, plaats en website uit X, een kopregel en foto uit LinkedIn, en functies uit Google-contacten en Salesflare. Wat iemand over zichzelf zegt, gaat voor. Ga met de muis over de regel onder de naam om te zien waar het vandaan kwam. Alles blijft op je Machine.

Foto's van WhatsApp komen via je WhatsApp-sync die altijd aanstaat, als die het toelaat: maximaal 50 per dag, alleen voor mensen die al in je Graph staan. Er wordt niets naar hen verstuurd.

## Iemand definitief verwijderen

Open op de pagina het menu ⋯ en kies **Definitief verwijderen…**, dan **Verwijderen**. Dat verwijdert de persoon en wat je Machine over hem of haar weet: de vermelding, adressen, opgezochte gegevens, de berichten alleen tussen jullie twee, en notities over die persoon. To-do's waarbij die persoon betrokken is, blijven, met de naam eruit gehaald. Die persoon wordt niet opnieuw toegevoegd. Dit kun je niet ongedaan maken.

## Wie is wie

Rollen die je Machine in je berichten las, die wachten op jouw woord. **✓ Klopt** bevestigt er een; **Bewerken** opent de pagina in Bewerken. Hij leert van je wijzigingen. Dit verschijnt alleen als er rollen wachten.

## In een Werk-Fleet

Werk voor klanten wordt gedeeld met de Machines van je teamgenoten, en dat van hen staat in de jouwe. Elke thread toont **Team** of **Alleen jij**. Zie [Team-Graph](team-graph.md).

## Organisaties

Bedrijven, uit de adressen en namen in je berichten. Zie [Gegevens van organisaties](organization-data.md).

De pagina van een organisatie is opgebouwd zoals die van een persoon: het logo, de naam en wat ze doet, één regel over hoe jullie contact hebben, dan **Contact** (website en LinkedIn), **Met jou** (wat ze voor jou is), de personen daar en de **Tijdlijn**.

De **Projecten** tonen eerst de open projecten, elk met de fase. Hun verplaatsingen staan in de tijdlijn. **Bewerken** bovenaan wijzigt de gegevens en wat ze voor jou is. **Vraag de Fleet wie ze kent** vindt een ingang via je Fleet.

Mail van tools voor e-mailopwarming wordt buiten gehouden, onder "Verborgen als opwarming", met **Ongedaan maken** per domein.

## Projecten

Je Machine geeft ze een naam op basis van waar je berichten over gaan. Signalen die erbij lijken te horen, staan als "hoort er waarschijnlijk bij". Hernoem je een project naar de naam van een ander project, dan worden ze samengevoegd.

Of beheer ze met de hand, zoals deals in een CRM:

- **Nieuw project**: bovenaan een bord, **+ Toevoegen** onder een fase, **Nieuw project** bovenaan de lijst, **+** in de bovenste balk op een telefoon, of vanaf de pagina van een persoon of organisatie. Geef een naam, een bord en fase, een organisatie (zoek in je Graph, of **Toevoegen** van een nieuwe), een waarde, een verwachte sluitdatum, personen en notities. Projecten die al in je Graph staan met een gelijkaardige naam, verschijnen eerst.
- **Bewerken** op de pagina van een project, of **Bewerken** in het menu **⋯** van een kaart op het bord (of druk op E op een kaart). Dat wijzigt al het bovenstaande.
- **Gewonnen** of **Verloren**, met waarom. Gewonnen verplaatst het naar de laatste fase van het bord, Verloren naar Vastgelopen of afgewezen. **Heropenen** draait het terug.
- **Archiveren** haalt het van het bord en uit de lijsten; een nieuw bericht erover brengt het terug. **Verwijderen** verwijdert het voorgoed; de berichten en personen blijven.
- Verplaats een kaart door ze te slepen, of met **⋯**, **Verplaatsen naar** op een telefoon. Je verplaatsing blijft staan tot een nieuwer bericht ze verplaatst.
- **Fases**, bovenaan een bord, toont alleen de fases die je kiest, per bord. **Wissen** toont ze weer allemaal.
- "4 met geen antwoord in 10+ dagen" onder een fase: tik erop om alleen die te tonen, op het bord en in de lijst. Tik nog eens om alles te tonen.

### De to-do's van een project

Een to-do kan bij één project horen. Je Machine kiest het als de thread of de personen waar het over gaat bij één open project horen, en de to-do toont de naam onder de titel. **Project wijzigen** onder **Meer** op de to-do, of **Aan een project koppelen** in het opdrachtmenu (Ctrl K), wijzigt het of haalt het weg. Je keuze blijft.

De pagina van een project toont de to-do's onder **To-do’s**, open to-do's eerst, en de kaart op het bord zegt hoeveel er open zijn. Een to-do koppelen aan een gedeeld project deelt verder niets: je team ziet nog altijd alleen wat uit gedeelde berichten kwam.

### De organisatie van een project

Elk project kan aan één organisatie gekoppeld worden. De pagina, de rij en de kaart op het bord tonen ze, en linken ernaar.

Heeft niemand er een gekozen, dan stelt je Machine ze in op basis van de personen in het project en de berichten, zonder je collega's. Dat doet hij alleen als één organisatie duidelijk de andere partij is: persoonlijke e-mail zoals Gmail telt nooit, en een project met meerdere bedrijven blijft zonder. Het projectformulier zegt dan "Op basis van de personen".

Je keuze in **Bewerken** blijft altijd, ook als je ze weghaalt. **Zelfde organisatie als…** verplaatst de projecten van een organisatie mee, en **Afsplitsen** zet ze terug.

### Borden

Projecten van één soort in fases, zoals een pipeline voor evaluaties. **⋯** op een bord: **Bord bewerken** (naam, fases, welke projecten erbij horen), **Openen op dit bord** en **Nieuw bord**. Reviews blijven projecten toevoegen die passen en zetten ze in een fase. Zijn ze niet zeker, dan toont het bord "2 projecten kunnen hier horen": **Toevoegen** of **Weglaten**.

**Opvolging…** in het **⋯** van een bord volgt vanzelf op als iemand niet antwoordt. Zie [Opvolging](follow-ups.md).

Vink er een paar aan, of **Alles selecteren**, om ze in één keer te doen, en **Ongedaan maken** meteen erna als je van gedachten verandert. Een project dat meerdere tegenpartijen bundelt, wordt één project per tegenpartij als je het toevoegt.

**Pipeline**, bovenaan een bord, telt de waarde van de open projecten per fase op, en wat er per maand verwacht wordt te sluiten op basis van de sluitdatums. Gewonnen, verloren en vastgelopen projecten zijn niet open; wat je deze maand won, staat apart. Waarden zijn in euro, tenzij je Machine op een andere munt ingesteld is. Met **Eigenaar** in Filteren telt het alleen de jouwe.

Een nieuw bord, of een voorgesteld bord dat je bewaart, kijkt één keer door je hele geschiedenis. Het vindt projecten en organisaties die passen, maakt één project per organisatie en zet elk in een fase. De kop zegt "Bezig met je geschiedenis doorzoeken…" terwijl het werkt, en daarna hoeveel het toevoegde en hoeveel er wachten tot je ze nakijkt. Een bord voor Alleen jij houdt wat het vindt bij jou.

### Het bord van een teamgenoot

In **Team** staan gedeelde borden van teamgenoten naast de jouwe, met de meeste van je projecten eerst. Elke kaart zegt wat er het laatst gebeurde, met datum, zoals op het bord van de eigenaar: de nieuwste regel gedeeld met het team, anders de laatste verplaatsing. De eigenaar staat er alleen bij als een fase kaarten van meerdere teamgenoten heeft; is één persoon eigenaar van het hele bord, dan staat dat in de kop.

**Van mij**, **Wacht op mij** en **Alle** kiezen wat een gedeeld bord toont, en de Team-lijst van projecten mee. Van mij is waar jij bij betrokken bent: een thread ervan, een project waarvan je eigenaar bent of dat je zelf hebt, of een to-do van jou erover. Wacht op mij is wat op jou wacht: een open to-do erover, of een thread waarin het nieuwste bericht aan jou geschreven is.

De rest van een fase klapt in onder **Nog N tonen**. Projecten die op elkaar lijken, zoals een reeks proefperiodes "… CRM-evaluatie", worden één rij met een aantal; tik erop om ze te openen. Niets hiervan verandert wat er gedeeld wordt.

## Een to-do over iemand

**Nieuwe to-do** in het menu **⋯** van een persoon, organisatie of project begint een to-do over die persoon, organisatie of dat project.

## Wat hij over iemand weet

Onder Bekend over heeft elk feit een menu:

- **Vergeten** verwijdert het overal.
- Niet over deze persoon haalt het alleen van die pagina.
