---
title: Personen
area: graph
summary: Iedereen met wie je contact hebt: hun pagina, samenvatting en tijdlijn, en hoe je iemand toevoegt, bewerkt, samenvoegt of verwijdert.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Iedereen met wie je contact hebt, op volgorde van hoe dichtbij jullie staan, op basis van je berichten en vergaderingen. Nieuwsbrieven, bonnetjes en andere mailings voegen pas iemand toe als je terugschrijft. Ze staan onder Verborgen afzenders, onderaan de lijst. Met **Als persoon tonen** voeg je iemand toe. Velden, tags en import werken hetzelfde in alle drie de lijsten, en elke lijst heeft eigen filters: zie [The Graph](graph.md).

Een gedeelde inbox (info@, klantenservice, de eigen naam van een winkel) hoort bij de organisatie, niet bij een persoon, ook niet nadat je ernaar hebt geschreven.

## Pagina van iemand

Bovenaan staan hun foto, naam, functie, organisatie en locatie, plus één regel over jullie contact ("Dagelijks contact · laatst contact gisteren · volgende vergadering di. 27 okt."). Recent contact wordt weergegeven als "zojuist", "3 uur geleden", "gisteren" of "3 dagen geleden". Ouder contact wordt als datum weergegeven. Beweeg de aanwijzer erover voor de exacte datum. Daaronder vind je:

- **Contact**: hun telefoonnummers en e-mailadressen. Tik op een nummer of adres om te bellen of te schrijven, of tik op **Kopiëren**. Hun **Verjaardag** staat hier ook, met de bron erbij (Google-contacten, Google Calendar, Facebook of jij): zie [The Graph](graph.md#birthday).
- **Met jou**: wat voor contact ze voor je zijn, Werk- of Privécontact, en je Familie of Fleet, met **Bekijk in Fleet**.
- **Ook op**: de andere plekken waar jullie contact hebben. **Slack** opent hun profiel in Slack of jullie recentste Slack-gesprek.
- De **Personen** en **Projecten** waar ze bij horen, **Open tussen jullie** (beloftes over en weer, met **Markeer als gedaan** en **Laten vallen**) en hun **Tijdlijn**.

Adressen en chats van iemand worden automatisch samengevoegd wanneer duidelijk is dat ze bij dezelfde persoon horen, bijvoorbeeld een werkmail met het eigen adres van die persoon in CC.

Krijg je de melding **Deze pagina kon niet worden geladen.**? Tik op **Opnieuw proberen**. Blijft de melding staan, gebruik dan **Klopt er iets niet?** onderaan de pagina.

## Samenvatting

Een paar korte regels bovenaan iemands pagina over wat er is besloten, gevraagd, gepland of beloofd, met alle betrokkenen erbij. The Machine schrijft de samenvatting opnieuw als er iets nieuws is, alleen voor mensen met wie je echt contact hebt. Hij controleert elke regel eerst. Meestal gebeurt dat eenmaal per dag. Als er iets verandert aan een kwestie met die persoon, zoals een nieuwe deadline of een ingetrokken verzoek, gebeurt het binnen een paar uur.

Een vage regel wordt weggelaten. Is er niets concreets te melden, dan is er geen samenvatting. Elke regel linkt naar de bron. Berichten van één dag delen één datum met het aantal berichten; ze klappen samen open.

Met **Bewerken** kun je het in je eigen woorden zetten. Als er nieuws is, toont The Machine een **Voorgestelde update** met **Gebruiken** en **Mijn versie houden**. Met **Laat The Machine het schrijven** laat je het weer aan The Machine over.

Voorbereidingen voor vergaderingen gebruiken deze samenvatting, maar alleen de regels aan de kant van die to-do (Werk of Privé). De samenvatting blijft op jouw Machine; je team ziet hem nooit.

## Tijdlijn

Elke pagina van een persoon of organisatie heeft een tijdlijn, met het nieuwste bovenaan: e-mail, vergaderingen en hun Zoom-samenvattingen, Intercom-gesprekken (met **Openen in Intercom**), WhatsApp-, Telegram-, Slack-, LinkedIn- en X-chats, to-do's, beloftes en projectverplaatsingen. Met de filters bovenaan bekijk je één bron tegelijk. Met **Meer tonen** laad je oudere items.

Vergaderingen die nog moeten plaatsvinden staan bovenaan onder **Binnenkort**, van vroeg naar laat. Met **Alles wat eraan komt tonen** zie je de rest. Bij een vergadering staat wie erbij was, elke persoon één keer. Een vergadering met notities of een transcript heeft het label **Notities** of **Transcript**. Klik erop om ze te lezen.

Je tijdlijnen zijn privé: de Graph van je team toont alleen wat je deelinstellingen toestaan. Met **Team** boven de tijdlijn van een pagina zie je wat teamgenoten hebben gedeeld, met bij elk item wie het heeft gedeeld. **Van mij** toont alleen jouw items.

## Werk en Privé

De tabbladen **Werk** en **Privé** tonen mensen op basis van hun Type, dat op hun pagina staat. Jouw keuze (**Bewerken**) gaat voor. Anders vallen je Familie en Vrienden, en familieleden of vrienden van jou (een vrouw, een vader), onder Privé, ongeacht vanaf welk adres ze schrijven. Je team krijgt je privécontacten nooit te zien.

## Iemand toevoegen

Kies **Nieuwe persoon** bovenaan Personen, of **+** in de bovenbalk op een telefoon. Vul een naam in, en eventueel een e-mailadres en organisatie. Staat iemand die hierop lijkt al in je Graph, dan toont het formulier diegene eerst, zodat je die pagina kunt openen. Met **Toevoegen** open je de nieuwe pagina.

Iemand die je toevoegt blijft staan, ook als er nog geen berichten zijn. Het eerste bericht wordt automatisch aan die persoon gekoppeld.

## Iemand bewerken

Met **Bewerken** bovenaan hun pagina kun je hun naam, functie, organisatie, locatie, LinkedIn, telefoonnummers en e-mailadressen wijzigen, aangeven wat ze voor je zijn en kiezen tussen Werk en Privé. Het veld **Notities** is bedoeld voor alles wat je wilt onthouden. Notities blijven behouden bij samenvoegen. Met **Opslaan** bewaar je de wijzigingen; met **Annuleren** laat je alles zoals het was.

Je wijzigingen blijven behouden, ook wanneer hun gegevens opnieuw worden opgezocht en na **Samenvoegen** en **Ongedaan maken**. Maak een veld leeg om de opgezochte waarde weer te gebruiken. Maak je de naam leeg, dan wordt de naam uit hun berichten weer ingevuld.

Klik op hun foto om die te wijzigen: **Afbeelding uploaden**, een gevonden foto kiezen of **Foto verwijderen**. De foto blijft op jouw Machine.

## Twee personen samenvoegen

Als twee personen misschien dezelfde zijn, vraagt hun pagina of het om dezelfde persoon gaat. Personen toont ze dan onder **Zelfde persoon?**. Met **Samenvoegen** voeg je ze samen, inclusief al hun berichten, notities, rollen en projecten. Met **Niet dezelfde** houd je ze voorgoed apart. Je antwoord wordt even bij het paar getoond, daarna verdwijnt het paar uit de lijst. De lijst verdwijnt zodra er niets meer te beoordelen is.

Iemand met een adres dat alleen lijkt op een adres dat je kent, zoals acme-corp.example naast acmecorp.example, wordt nooit voorgesteld als dezelfde persoon. Alleen jij kunt diegene een rol geven.

Een gedeeld adres, zoals info@ of een mailinglijst, wordt nooit samengevoegd met de mensen die er via schrijven. Een werkcontact buiten je bedrijf en een privéchat met alleen een naam gemeen worden niet automatisch samengevoegd. Ze worden als vraag getoond.

Met **Alles samenvoegen** voeg je alle paren in de lijst tegelijk samen, behalve de paren die je als **Niet dezelfde** hebt gemarkeerd. Met **Ongedaan maken** maak je dit meteen voor alle paren ongedaan.

Wil je zelf twee personen samenvoegen? Open een van hen, kies **⋯**, **Zelfde persoon als…** en selecteer de ander. Op de pagina van de samengevoegde persoon staat onder **Samengevoegd vanuit** waarom ze zijn samengevoegd. Met **Ongedaan maken** splits je ze weer op.

## Iemand definitief verwijderen

Open op hun pagina het menu ⋯ en kies **Definitief verwijderen…**, gevolgd door **Verwijderen**. Hiermee verwijder je die persoon en alles wat je Machine over hen weet: hun profiel, adressen, opgezochte gegevens, berichten die alleen tussen jullie twee zijn uitgewisseld en notities over hen.

To-do's waar ze bij betrokken zijn blijven staan, maar hun naam wordt verwijderd. Ze worden niet opnieuw toegevoegd, ook niet via een import of een to-do over Facebook-verjaardagen met hun naam of adres. Dit kan niet ongedaan worden gemaakt.

## Niet bezorgd

Als een e-mail aan iemand niet aankomt, staat **Niet bezorgd** met de datum bij hun adres en komt een ander adres van die persoon bovenaan. Nieuwe concepten worden nooit naar dat adres gestuurd als er een ander adres bekend is. Is het hun enige adres, dan waarschuwt het verzendvenster je, maar je kunt de e-mail nog steeds versturen.

Een e-mail wordt als niet bezorgd beschouwd als de mailserver zegt dat het adres niet bestaat, of na 3 tijdelijke fouten binnen een week. De melding verdwijnt als ze weer vanaf dat adres schrijven of als een e-mail naar dat adres wel aankomt.

## Functie en foto

Mensen met een bedrijfsadres krijgen een functie, foto, LinkedIn-profiel en woonplaats, die worden opgezocht zoals [organisatiegegevens](organization-data.md). Op een gehoste Machine worden alleen hun naam en het domein van hun bedrijf opgezocht. Voor een foto krijgt Gravatar een hash van hun werkadres, nooit het adres zelf. Je kunt dit uitschakelen via **Instellingen**, onder Beveiliging: **Werkcontacten opzoeken**.

Als hun gegevens zijn gevonden, toont hun pagina ook hun biotekst, hoe lang ze hun huidige functie al hebben en hun twee vorige functies. Voorbereidingen gebruiken deze informatie ook. De biotekst wordt alleen gebruikt als iemand zelf geen bio heeft.

Je koppelingen vullen profielen verder aan met informatie die ze al hebben gelezen: een functie, telefoonnummer en tijdzone uit Slack, een bio en locatie uit X, een kopregel en foto uit LinkedIn, functies uit Google-contacten en Salesflare, en een contactfoto uit Salesflare als Salesflare die zelf heeft bewaard. Beweeg de aanwijzer over de regel onder hun naam om te zien waar de informatie vandaan komt.

Outlook voegt foto's toe van collega's bij je organisatie en van je Outlook-contacten, plus de functies en bedrijven van je contacten ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

WhatsApp- en Telegram-foto's worden opgehaald via je WhatsApp-synchronisatie en je Telegram-chatkoppeling: maximaal 50 per dag per dienst, alleen voor mensen die al in je Graph staan. Er wordt niets naar hen verstuurd. Bij een import van Facebook-verjaardagen wordt de profielfoto toegevoegd van iemand die nog geen foto heeft, wanneer je die persoon opslaat ([Routines](routines.md)). Alles blijft op jouw Machine.

In de [Team Graph](team-graph.md) van een Fleet voor werk wordt een kleine kopie van een werkfoto meegedeeld in het gedeelde profiel van iemand. Foto's uit Google-contacten, WhatsApp, Telegram of Facebook, en foto's die je hebt gewijzigd of verwijderd, worden nooit meegedeeld.

## Over jou

Je eigen adressen en nummers, ook je aliassen, zijn altijd van jou en nooit van iemand in je Graph. Als je naar jezelf zoekt of iemand toevoegt met een van je adressen, wordt **Over jou** geopend. Bij een import wordt je eigen rij overgeslagen.

Onder Over jou staan je adressen en de bron van elk adres. Je wijzigt ze via **Instellingen**, onder Account. Kies **Mijn contactgegevens delen** om je contactgegevens met een teamgenoot of vriend te delen. Zie [Een contact delen](share-contact.md).

## Wat iemand voor je is

Rollen die je Machine uit je berichten haalt, staan op hun pagina onder **Voor jou**, met de regel waaruit de rol is afgeleid. Je hoeft niets te bevestigen. Klopt er iets niet? Corrigeer het met **Bewerken** op hun pagina of met **⋯** bij de regel onder **Recente wijzigingen**. Je Machine leert van je wijzigingen.

## Wat je Machine over iemand weet

Feiten over iemand staan op hun pagina onder **Bekend over**. Onder **Leren** staan algemene feiten. Met **Toevoegen** voeg je een feit in je eigen woorden toe. Elk feit heeft een menu:

- **Bewerken** wijzigt het feit meteen.
- Met **Niet over deze persoon** maak je er weer een algemeen feit van, onder **Leren**, **Feiten**.
- Met **Verwijderen** verwijder je het overal.

## Recente wijzigingen

Onder **Recente wijzigingen**, ingeklapt net boven de tijdlijn van een persoon, organisatie of project, staat wat je Machine over hen heeft gewijzigd of geleerd: een rol, waar iemand werkt, hoe twee mensen aan elkaar verwant zijn, een feit of een projectverplaatsing. Elke regel toont de datum en de bron. Tik op de bron om het bericht te lezen.

Klopt een regel niet? Met **⋯** kun je die meteen aanpassen: **Bewerken**, **Verwijderen**, **Niet over deze persoon** of **Ongedaan maken** om een project terug te zetten naar de vorige plek. Er worden drie regels getoond; met **Meer tonen** zie je de rest.

Iemand van wie je Machine vandaag iets heeft bijgewerkt, krijgt een stip in de lijst Personen. Bovenaan de lijst staat **Vandaag 4 personen bijgewerkt**, met hun namen erbij. Zie [The Graph](graph.md).

## Een to-do over iemand

Met **Nieuwe to-do** in het menu **⋯** van een persoon, organisatie of project maak je een to-do over diegene.
