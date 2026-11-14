---
title: Personen
area: graph
summary: Iedereen met wie je contact hebt: hun pagina, samenvatting en tijdlijn, en hoe je iemand toevoegt, bewerkt, samenvoegt of verwijdert.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Iedereen met wie je contact hebt, op volgorde van wie het dichtst bij je staat, op basis van je berichten en vergaderingen. Nieuwsbrieven, bonnetjes en andere mailings voegen pas iemand toe als je terugschrijft. Ze staan onder Verborgen afzenders, onder de lijst: **Als persoon weergeven** voegt iemand toe. Velden, tags en import werken hetzelfde in alle drie de lijsten. Elke lijst heeft eigen filters: zie [The Graph](graph.md).

Een gedeelde inbox (info@, klantenservice, de eigen naam van een winkel) telt voor de organisatie, niet als persoon. Dat blijft zo, ook nadat je ernaar hebt gemaild.

## Pagina van iemand

Bovenaan staan de foto, naam, functie, organisatie en plaats, plus één regel over jullie contact ("Dagelijks contact · laatst contact gisteren · volgende vergadering di 27 okt"). Recent contact wordt weergegeven als "zojuist", "3 uur geleden", "gisteren" of "3 dagen geleden". Ouder contact wordt als datum weergegeven. Beweeg de aanwijzer erover om de exacte datum te zien. Daaronder:

- **Contact**: telefoonnummers en e-mailadressen. Tik op een nummer of adres om te bellen of te schrijven, of tik op **Kopiëren**. De **Verjaardag** staat hier ook, met de bron (Google Contacts, Google Calendar, Facebook of jij): zie [The Graph](graph.md#birthday).
- **Met jou**: wat iemand voor je is, een werk- of privécontact en je familie of Fleet, met **Bekijk in Fleet**.
- **Ook op**: andere plekken waar jullie contact hebben. **Slack** opent die persoon in Slack, of jullie meest recente Slack-gesprek.
- **Personen** en **Projecten** waar iemand deel van uitmaakt, **Open tussen jullie** (beloftes over en weer, met **Markeer als gedaan** en **Laten vallen**) en hun **Tijdlijn**.

Adressen en chats van iemand worden automatisch samengevoegd als duidelijk is dat ze bij één persoon horen, zoals een werkmail met het eigen adres van die persoon in de cc.

Als er **Kan deze pagina niet laden.** staat, tik je op **Opnieuw proberen**. Blijft die melding staan, gebruik dan **Klopt er iets niet?** onderaan de pagina.

## Samenvatting

Een paar korte regels bovenaan iemands pagina: wat er is besloten, gevraagd, gepland of beloofd, met de namen van iedereen die erbij betrokken is. The Machine herschrijft de samenvatting als er iets nieuws is, alleen voor mensen met wie je echt contact hebt, en controleert eerst elke regel. Meestal gebeurt dat één keer per dag. Bij veranderingen in een lopende zaak, zoals een nieuwe deadline of een ingetrokken verzoek, gebeurt het binnen een paar uur.

Een vage regel wordt weggelaten. Is er niets specifieks te melden, dan is er geen samenvatting. Elke regel linkt naar de bron. Berichten van één dag delen één datum, met het aantal berichten erbij, en kunnen samen worden geopend.

**Bewerken** om het op jouw manier te zeggen. Bij nieuws toont The Machine een **Voorgestelde update**, met **Gebruiken** en **Mijn versie houden**. Met **Laat The Machine het schrijven** geef je de tekst weer aan hem terug.

Voorbereidingen voor vergaderingen gebruiken de samenvatting, maar alleen de regels aan de kant van die to-do (Werk of Privé). De samenvatting blijft op je Machine. Je team kan hem nooit zien.

## Tijdlijn

Elke pagina van een persoon of organisatie heeft een tijdlijn, met de nieuwste items bovenaan: e-mail, vergaderingen en hun Zoom-samenvattingen, Intercom-gesprekken (met **Openen in Intercom**), WhatsApp-, Telegram-, Slack-, LinkedIn- en X-chats, to-do's, beloftes en projectwijzigingen. Met de filters bovenaan kies je één bron tegelijk. Met **Meer tonen** laad je oudere items.

Vergaderingen die nog moeten plaatsvinden staan bovenaan onder **Binnenkort**, met de eerstvolgende bovenaan. **Alles wat eraan komt tonen** toont de rest. Bij een vergadering zie je wie erbij was, met elke persoon één keer. Bij een vergadering met notities of een transcript staat **Notities** of **Transcript**. Klik erop om ze te lezen.

Je tijdlijnen zijn van jou: de Graph van je team toont alleen wat volgens je deelregels mag worden gedeeld. Met **Team** boven de tijdlijn op een pagina zie je wat teamgenoten hebben gedeeld. Bij elk item staat van wie het komt. **Van mij** toont alleen jouw items.

## Werk en privé

De tabbladen **Werk** en **Privé** tonen mensen op basis van hun Type, zoals vermeld op hun pagina. Jouw keuze (**Bewerken**) gaat voor. Anders vallen je familie en vrienden, en familie of vrienden van jou (een echtgenote, een vader), onder Privé, ongeacht vanaf welk adres ze schrijven. Je team krijgt nooit privécontacten te zien.

## Iemand toevoegen

Kies **Nieuwe persoon** bovenaan Personen, of tik op **+** in de bovenbalk op een telefoon. Vul een naam in, en eventueel een e-mailadres en organisatie. Als er al iemand in je Graph staat die erop lijkt, toont het formulier die persoon eerst. Zo kun je die pagina openen. Met **Toevoegen** open je de nieuwe pagina.

Iemand die je toevoegt blijft staan, ook als er nog geen berichten zijn. Het eerste bericht wordt aan die persoon gekoppeld.

## Iemand bewerken

Met **Bewerken** bovenaan iemands pagina kun je de naam, functie, organisatie, locatie, LinkedIn, telefoonnummers en e-mailadressen wijzigen, net als wat iemand voor je is en of diegene Werk of Privé is. Het veld **Notities** is voor alles wat je wilt onthouden. Notities blijven behouden bij samenvoegen. Met **Opslaan** bewaar je de wijzigingen. Met **Annuleren** laat je alles zoals het was.

Je wijzigingen blijven behouden, ook als de gegevens later opnieuw worden opgezocht en bij **Samenvoegen** en **Ongedaan maken**. Maak een veld leeg om de opgezochte waarde weer te gebruiken. Als je de naam wist, wordt de naam uit iemands berichten weer ingevuld.

Klik op de foto om die te wijzigen: **Afbeelding uploaden**, kies een foto die voor die persoon is gevonden, of **Foto verwijderen**. De foto blijft op je Machine.

## Twee personen samenvoegen

Als twee personen misschien dezelfde zijn, vraagt hun pagina of het om dezelfde persoon gaat. Personen toont ze ook onder **Zelfde persoon?**. Met **Samenvoegen** voeg je ze samen, inclusief al hun berichten, notities, rollen en projecten. Met **Niet dezelfde** houd je ze voorgoed apart. Je antwoord wordt even bij het paar weergegeven, daarna verdwijnt het uit de lijst. De lijst verdwijnt zodra er niets meer te vragen is.

Iemand met een adres dat alleen lijkt op een adres dat je kent, zoals acme-corp.example tegenover acmecorp.example, wordt nooit voorgesteld als dezelfde persoon. Alleen jij kunt diegene een rol geven.

Een gedeeld adres, zoals info@ of een mailinglijst, wordt nooit samengevoegd met de mensen die via dat adres schrijven. Een werkcontact van buiten je bedrijf en een privéchat met alleen een naam gemeen worden niet automatisch samengevoegd. Ze worden als mogelijke match weergegeven.

Met **Alles samenvoegen** voeg je alle paren in de lijst in één keer samen, behalve de paren die je als **Niet dezelfde** hebt gemarkeerd. Met **Ongedaan maken** maak je die samenvoegingen meteen weer ongedaan.

Wil je zelf twee personen samenvoegen, open dan een van hun pagina's en kies **⋯**, **Zelfde persoon als…** en vervolgens de andere persoon. Op de pagina van een samengevoegde persoon staat onder **Samengevoegd vanuit** waarom. Met **Ongedaan maken** kun je de samenvoeging weer ongedaan maken.

## Iemand definitief verwijderen

Open op iemands pagina het menu ⋯ en kies **Definitief verwijderen…**. Kies daarna **Verwijderen**. De persoon en alles wat je Machine over diegene weet worden verwijderd: de vermelding, adressen, opgezochte gegevens, berichten die alleen tussen jullie zijn uitgewisseld en notities over die persoon.

To-do's waarbij die persoon betrokken is, blijven staan, maar diens naam wordt verwijderd. De persoon wordt niet opnieuw toegevoegd, ook niet via een import of een to-do voor Facebook-verjaardagen met diens naam of adres. Dit kan niet ongedaan worden gemaakt.

## E-mail teruggestuurd

Als een e-mail aan iemand wordt teruggestuurd, staat **Teruggestuurd** bij het adres, met de datum. Een ander adres van die persoon komt dan eerst. Nieuwe concepten worden nooit naar dat adres gestuurd als een ander adres bekend is. Is dit het enige adres, dan krijg je een waarschuwing in het verzendvenster, maar kun je de e-mail nog steeds versturen.

Een teruggestuurde e-mail telt mee als de mailserver meldt dat het adres niet bestaat, of na 3 tijdelijke fouten binnen een week. De melding verdwijnt als die persoon weer vanaf dat adres schrijft, of als een e-mail naar dat adres wordt bezorgd.

## Functie en foto

Mensen met een bedrijfsadres krijgen een functie, foto, LinkedIn en plaats opgezocht, net als [organisatiegegevens](organization-data.md). Op een gehoste Machine worden alleen hun naam en het domein van hun bedrijf opgezocht. Gravatar ontvangt voor een foto een hash van hun werkadres, nooit het adres zelf. Je kunt dit uitschakelen in **Instellingen**, onder Beveiliging: **Werkcontacten opzoeken**.

Als er gegevens zijn gevonden, toont hun pagina ook hun beschrijving, hoelang ze hun huidige functie hebben en de twee functies daarvoor. Voorbereidingen gebruiken die gegevens ook. De beschrijving wordt alleen gebruikt als iemand geen eigen bio heeft.

Je koppelingen vullen gegevens aan die al bekend zijn: een functie, telefoonnummer en tijdzone uit Slack, een bio en plaats uit X, een kopregel en foto uit LinkedIn, functietitels uit Google Contacts en Salesflare, en een contactfoto uit Salesflare als Salesflare die zelf bewaart. Beweeg de aanwijzer over de regel onder iemands naam om te zien waar de informatie vandaan komt.

Outlook voegt foto's toe van collega's bij je organisatie en van je Outlook-contacten, plus de functietitels en bedrijven van je contacten ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

WhatsApp- en Telegram-foto's worden opgehaald via je WhatsApp-synchronisatie en je Telegram-chatkoppeling: maximaal 50 per dag per dienst, alleen voor mensen die al in je Graph staan. Er wordt niets naar hen verstuurd. Een import van Facebook-verjaardagen voegt de profielfoto toe van iemand die nog geen foto heeft, zodra je die opslaat ([Routines](routines.md)). Alles blijft op je Machine.

In de [Team Graph](team-graph.md) van een Werk-Fleet wordt een kleine kopie van een werkfoto gedeeld met de gedeelde gegevens van die persoon. Foto's uit Google Contacts, WhatsApp, Telegram of Facebook en foto's die je hebt gewijzigd of verwijderd, worden nooit gedeeld.

## Over jou

Je eigen adressen en telefoonnummers, ook aliassen, horen altijd bij jou en zijn nooit iemand in je Graph. Als je jezelf zoekt of iemand toevoegt met een van je adressen, wordt **Over jou** geopend. Bij een import wordt je eigen rij overgeslagen.

Onder Over jou staan je adressen en de bron van elk adres. Je kunt ze wijzigen in **Instellingen**, onder Account. Kies **Mijn contactgegevens delen** om je eigen contactgegevens naar een teamgenoot of vriend te sturen. Zie [Een contact delen](share-contact.md).

## Wat iemand voor je is

Rollen die je Machine in je berichten leest, staan op iemands pagina onder **Voor jou**, met de regel die hij heeft gelezen. Je hoeft niets eerst goed te keuren. Klopt het niet? Met **Bewerken** op de pagina pas je het aan, of gebruik je **⋯** bij de regel onder **Recente wijzigingen**. The Machine leert van je wijzigingen.

## Wat The Machine over iemand weet

Feiten over iemand staan op diens pagina onder **Bekend over**. Bij Leren staan de algemene feiten. Met **Toevoegen** voeg je er een toe in je eigen woorden. Elk feit heeft een menu:

- Met **Bewerken** pas je het direct aan.
- Met **Niet over deze persoon** maak je er weer een algemeen feit van, onder **Leren**, **Feiten**.
- Met **Verwijderen** verwijder je het overal.

## Recente wijzigingen

Onder **Recente wijzigingen**, ingeklapt net boven de tijdlijn van een persoon, organisatie of project, staan de dingen die je Machine over die persoon, organisatie of dat project heeft gewijzigd of geleerd: een rol, waar iemand werkt, hoe twee mensen verwant zijn, een feit of een projectwijziging. Bij elke regel staan de datum en bron. Tik op de bron om het bericht te lezen.

Klopt een regel niet? Met **⋯** pas je die direct aan: **Bewerken**, **Verwijderen**, **Niet over deze persoon** of **Ongedaan maken** om een project terug te zetten naar de vorige plek. Er worden drie regels getoond. Met **Meer tonen** zie je de rest.

Bij iemand die je Machine vandaag heeft bijgewerkt, staat een stip in de lijst Personen. Bovenaan de lijst staat **Vandaag 4 personen bijgewerkt**, met hun namen. Zie [The Graph](graph.md).

## Een to-do over iemand

Met **Nieuwe to-do** in het menu **⋯** van een persoon, organisatie of project maak je een to-do over die persoon, organisatie of dat project.
