---
title: Personen
area: graph
summary: Iedereen met wie je contact hebt: hun pagina, samenvatting en tijdlijn, en hoe je iemand toevoegt, bewerkt, samenvoegt of verwijdert.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 2fe1c104a74711c4
---
Iedereen met wie je contact hebt, op volgorde van wie het dichtst bij je staat, uit je berichten en vergaderingen. Nieuwsbrieven, betalingsbewijzen en andere mailings voegen pas iemand toe als je terugschrijft. Ze staan onder Verborgen afzenders, onder de lijst: met **Als persoon tonen** voeg je iemand toe. Velden, tags en importeren werken hetzelfde in alle drie de lijsten. Elke lijst heeft eigen filters: zie [The Graph](graph.md).

Een gedeelde inbox (info@, klantenservice, de naam van een winkel) telt mee voor de organisatie, niet als persoon, ook niet nadat je ernaar hebt geschreven.

## Pagina van iemand

Bovenaan staan hun foto, naam, functie, organisatie en locatie, met één regel over jullie contact ("Dagelijks contact · laatste contact gisteren · volgende vergadering di. 27 okt."). Recent contact wordt weergegeven als "zojuist", "3 uur geleden", "gisteren" of "3 dagen geleden". Ouder contact wordt als datum weergegeven. Beweeg de aanwijzer erover voor de exacte datum. Daaronder:

- **Contact**: hun telefoonnummers en e-mailadressen. Tik op een nummer of adres om te bellen of schrijven, of om het te **Kopiëren**. Hun **Verjaardag** staat hier ook, met de bron erbij (Google Contacten, Google Agenda, Facebook of jij): zie [The Graph](graph.md#birthday).
- **Met jou**: wat ze voor je zijn, een Werk- of Privécontact en je Familie of Fleet, met **Bekijk in Fleet**.
- **Ook op**: de andere plekken waar je met ze praat. **Slack** opent hun profiel in Slack of je nieuwste Slack-thread met ze.
- **Personen** en **Projecten** waar ze deel van uitmaken, **Open tussen jullie** (beloftes over en weer, met **Markeer als gedaan** en **Laten vallen**) en hun **Tijdlijn**.

Adressen en chats van iemand worden automatisch samengevoegd als duidelijk is dat het om dezelfde persoon gaat, bijvoorbeeld een zakelijk e-mailadres met hun eigen adres in de cc.

Staat er **Deze pagina kon niet worden geladen.**, tik dan op **Opnieuw proberen**. Blijft de melding verschijnen, gebruik dan **Klopt er iets niet?** onderaan de pagina.

## Samenvatting

Een paar korte regels bovenaan iemands pagina: wat er is besloten, gevraagd, gepland of beloofd, met vermelding van iedereen. The Machine herschrijft de samenvatting als er iets nieuws is, alleen voor mensen met wie je echt contact hebt, en controleert eerst elke regel. Meestal gebeurt dat één keer per dag. Als er iets verandert in een kwestie met die persoon, bijvoorbeeld een nieuwe deadline of een ingetrokken verzoek, gebeurt het binnen een paar uur.

Een vage regel wordt weggelaten. Als er niets specifieks te melden is, verschijnt er geen samenvatting. Elke regel linkt naar de bron: berichten van dezelfde dag worden gegroepeerd onder één datum, met het aantal berichten erbij, en kunnen samen worden geopend.

**Bewerken** om de tekst naar jouw smaak aan te passen. Als er nieuws is, toont The Machine een **Voorgestelde update**, met **Gebruiken** en **Mijn versie houden**. Met **Laat The Machine het schrijven** geef je de samenvatting weer aan The Machine.

Voorbereidingen voor vergaderingen gebruiken de samenvatting, maar alleen de regels van de kant van die to-do (Werk of Privé). De samenvatting blijft op jouw Machine. Je team kan hem nooit zien.

## Tijdlijn

Elke pagina van een persoon of organisatie heeft een tijdlijn, met de nieuwste items bovenaan: e-mail, vergaderingen en hun Zoom-samenvattingen, Intercom-gesprekken (met **Openen in Intercom**), WhatsApp-, Telegram-, Slack-, LinkedIn- en X-chats, to-do's, beloftes en wijzigingen aan projecten. De filters bovenaan tonen één bron tegelijk. Met **Meer tonen** laad je oudere items.

Aankomende vergaderingen staan bovenaan onder **Binnenkort**, met de eerstvolgende bovenaan. Met **Alles wat eraan komt tonen** zie je de rest. Bij een vergadering staan de aanwezigen, met elke persoon één keer vermeld. Bij een vergadering met notities of een transcript staat **Notities** of **Transcript**. Klik erop om ze te lezen.

Je tijdlijnen zijn alleen van jou. De Graph van het team toont alleen wat volgens je deelinstellingen mag. Op een pagina toont **Team** boven de tijdlijn wat teamgenoten hebben gedeeld, met bij elk item wie het heeft gedeeld. **Van mij** toont alleen jouw items.

## Werk en privé

Op de tabbladen **Werk** en **Privé** staan mensen op basis van hun Type, zoals vermeld op hun pagina. Jouw eigen keuze (**Bewerken**) gaat voor. Anders worden je Familie en Vrienden, en mensen die familie of vrienden van je zijn (een vrouw, een vader), als Privé ingedeeld, ongeacht vanaf welk adres ze schrijven. Je team krijgt nooit toegang tot privécontacten.

## Iemand toevoegen

Kies **Nieuwe persoon** bovenaan Personen, of **+** in de balk bovenaan op een telefoon. Vul een naam in, en ook een e-mailadres en organisatie als je die weet. Als er al iemand in je Graph staat die erop lijkt, toont het formulier die persoon bovenaan, zodat je die pagina kunt openen. Met **Toevoegen** open je de nieuwe pagina.

Iemand die je toevoegt blijft staan, ook als er nog geen berichten zijn. Het eerste bericht wordt automatisch aan die persoon gekoppeld.

## Iemand bewerken

Met **Bewerken** bovenaan hun pagina kun je hun naam, functie, organisatie, locatie, LinkedIn, telefoonnummers en e-mailadressen aanpassen, net als wat ze voor je zijn en of ze Werk of Privé zijn. Het veld **Notities** is voor alles wat je wilt onthouden. Notities blijven behouden als je mensen samenvoegt. Met **Opslaan** bewaar je de wijzigingen. Met **Annuleren** blijven ze zoals ze waren.

Je wijzigingen blijven behouden, ook als hun gegevens opnieuw worden opgezocht, en na **Samenvoegen** en **Ongedaan maken**. Maak een veld leeg om de opgezochte waarde weer te gebruiken. Als je de naam wist, wordt de naam uit hun berichten weer gebruikt.

Klik op hun foto om die te wijzigen: **Afbeelding uploaden**, kies een foto die voor hen is gevonden of **Foto verwijderen**. De foto blijft op jouw Machine.

## Twee personen samenvoegen

Als twee mensen misschien dezelfde persoon zijn, vraagt hun pagina of het om dezelfde persoon gaat. Personen toont ze ook onder **Zelfde persoon?**. Met **Samenvoegen** voeg je ze samen, inclusief al hun berichten, notities, rollen en projecten. Met **Niet dezelfde** houd je ze voorgoed apart. Je keuze wordt even bij het paar getoond, waarna het uit de lijst verdwijnt. De lijst verdwijnt zodra er niets meer te beoordelen is.

Een gedeeld adres, zoals info@ of een mailinglijst, wordt nooit samengevoegd met de mensen die er via schrijven. Een werkcontact van buiten je bedrijf en een privéchat met alleen een naam gemeen worden niet automatisch samengevoegd. Ze worden als vraag getoond.

Met **Alles samenvoegen** voeg je alle paren in de lijst tegelijk samen, behalve de paren die je als **Niet dezelfde** hebt gemarkeerd. Met **Ongedaan maken** maak je alle samenvoegingen direct weer ongedaan.

Wil je zelf twee personen samenvoegen, open dan een van hen en kies **⋯**, **Zelfde persoon als…** en vervolgens de andere persoon. Op de pagina van een samengevoegde persoon staat onder **Samengevoegd vanuit** waarom de personen zijn samengevoegd. Met **Ongedaan maken** splits je ze weer.

## Iemand definitief verwijderen

Open op hun pagina het menu ⋯ en kies **Definitief verwijderen…**. Kies daarna **Verwijderen**. Hiermee verwijder je die persoon en alles wat je Machine over hen weet: hun vermelding, adressen, opgezochte gegevens, berichten die alleen tussen jullie zijn uitgewisseld en notities over hen.

To-do's waar ze bij betrokken zijn blijven staan, maar hun naam wordt eruit gehaald. Ze worden niet opnieuw toegevoegd, ook niet via een import of een Facebook-verjaardagsto-do met hun naam of adres. Dit kun je niet ongedaan maken.

## E-mail niet bezorgd

Als een e-mail aan iemand niet wordt bezorgd, staat **Niet bezorgd** bij hun adres, met de datum. Een ander adres van hen komt dan bovenaan te staan. Nieuwe concepten worden nooit naar dat adres gestuurd als er een ander adres bekend is. Is dit hun enige adres, dan waarschuwt het verzendscherm je, maar je kunt de e-mail nog steeds versturen.

Een e-mail telt als niet bezorgd als de mailserver meldt dat het adres niet bestaat, of na 3 tijdelijke fouten binnen een week. De melding verdwijnt als ze weer vanaf dat adres schrijven of als een e-mail naar dat adres wel aankomt.

## Functie en foto

Bij mensen met een zakelijk adres worden een functietitel, foto, LinkedIn en stad opgezocht, net als [organisatiegegevens](organization-data.md). Op een gehoste Machine worden alleen hun naam en het domein van hun bedrijf opgevraagd. Voor een foto ontvangt Gravatar een hash van hun zakelijke adres, nooit het adres zelf. Schakel dit uit via **Instellingen**, onder Beveiliging: **Werkcontacten opzoeken**.

Als de gegevens zijn opgezocht, toont hun pagina ook hun beschrijving, sinds wanneer ze hun huidige functie hebben en hun twee vorige functies. Voorbereidingen lezen die gegevens ook. De beschrijving wordt alleen gebruikt als ze geen eigen bio hebben.

Je Koppelingen vullen meer gegevens aan op basis van wat ze al hebben ingelezen: een functietitel, telefoonnummer en tijdzone uit Slack, een bio en locatie van X, een kopregel en foto van LinkedIn, functietitels uit Google Contacten en Salesflare, en een contactfoto van Salesflare als Salesflare die zelf heeft. Beweeg de aanwijzer over de regel onder hun naam om te zien waar de informatie vandaan komt.

Outlook voegt foto's toe van collega's bij je organisatie en van je Outlook-contacten, plus de functietitels en bedrijven van je contacten ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Foto's van WhatsApp en Telegram worden opgehaald via je WhatsApp-synchronisatie en je Telegram-chatverbinding: maximaal 50 per dag per dienst, alleen voor mensen die al in je Graph staan. Er wordt niets naar hen verstuurd. Een import van Facebook-verjaardagen voegt de profielfoto toe van iemand die nog geen foto heeft, zodra je die opslaat ([Routines](routines.md)). Alles blijft op jouw Machine.

In de [Team Graph](team-graph.md) van een Werk-Fleet wordt een kleine kopie van een zakelijke foto toegevoegd aan het gedeelde profiel van een persoon. Foto's uit Google Contacten, WhatsApp, Telegram of Facebook, en foto's die je hebt gewijzigd of verwijderd, worden nooit gedeeld.

## Over jou

Je eigen adressen en telefoonnummers, ook aliassen, zijn altijd van jou en nooit van iemand in je Graph. Als je naar jezelf zoekt of iemand toevoegt met een van je adressen, wordt **Over jou** geopend. Bij een import wordt je eigen rij overgeslagen.

In Over jou staan je adressen en de bron van elk adres. Je kunt ze wijzigen via **Instellingen**, onder Account. Kies **Mijn contactgegevens delen** om je eigen contactgegevens naar een teamgenoot of vriend te sturen. Zie [Een contact delen](share-contact.md).

## Wat iemand voor je is

Rollen die je Machine in je berichten leest, staan op hun pagina onder **Voor jou**, met de regel die het heeft gelezen. Je hoeft niets te bevestigen. Klopt het niet? Pas het aan via **Bewerken** op hun pagina of via **⋯** bij de regel onder **Recente wijzigingen**. Je Machine leert van je wijzigingen.

## Wat het over iemand weet

Feiten over iemand staan op hun pagina onder **Bekend over**. Leren bewaart de algemene feiten. Met **Toevoegen** voeg je er zelf een toe. Elk feit heeft een menu:

- Met **Bewerken** pas je het feit direct aan.
- Met **Niet over** maak je er weer een algemeen feit van, onder **Leren**, **Feiten**.
- Met **Verwijderen** verwijder je het feit overal.

## Recente wijzigingen

Onder **Recente wijzigingen**, ingeklapt vlak boven de tijdlijn van een persoon, organisatie of project, staat wat je Machine over hen heeft gewijzigd of geleerd: een rol, waar iemand werkt, de relatie tussen twee mensen, een feit of een wijziging aan een project. Elke regel vermeldt de datum en bron. Tik op de bron om het bericht te lezen.

Klopt een regel niet? Pas hem direct aan via **⋯**: **Bewerken**, **Verwijderen**, **Niet over** of **Ongedaan maken** om een project terug te zetten naar de vorige plek. Je ziet drie regels. Met **Meer tonen** zie je de rest.

Bij iemand die je Machine vandaag heeft bijgewerkt, staat een stip in de lijst Personen. Bovenaan de lijst staat **Vandaag 4 personen bijgewerkt**. Zie [The Graph](graph.md).

## Een to-do over iemand

Met **Nieuwe to-do** in het menu **⋯** van een persoon, organisatie of project maak je een to-do over die persoon, organisatie of dat project.
