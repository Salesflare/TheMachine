---
title: Personen
area: graph
summary: Iedereen met wie je contact hebt: hun pagina, samenvatting en tijdlijn, en hoe je iemand toevoegt, bewerkt, samenvoegt of verwijdert.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 0eb2dcc70fba84c2
---
Iedereen met wie je contact hebt, op volgorde van meest recent contact, op basis van je berichten en vergaderingen. Nieuwsbrieven, bonnetjes en andere mailings voegen pas iemand toe als je terugschrijft. Ze staan onder Verborgen afzenders, onder de lijst: **Als persoon weergeven** voegt iemand toe. Velden, tags en import werken in alle drie de lijsten hetzelfde. Elke lijst heeft eigen filters: bekijk [The Graph](graph.md).

Een gedeelde inbox (info@, klantenservice, de eigen naam van een winkel) telt mee voor de organisatie, niet als persoon, ook nadat je ernaar hebt gemaild.

## Pagina van iemand

Bovenaan staan de foto, naam, functietitel, organisatie en plaats, plus één regel over jullie contact ("Dagelijks contact · laatste contact gisteren · volgende vergadering di. 27 okt."). Recent contact wordt weergegeven als "zojuist", "3 uur geleden", "gisteren" of "3 dagen geleden". Ouder contact wordt als datum weergegeven. Beweeg de muisaanwijzer erover voor de exacte datum. Daaronder:

- **Contact**: telefoonnummers en e-mailadressen. Tik op een nummer of adres om te bellen of schrijven, of tik op **Kopiëren**. Ook de **Verjaardag** staat hier, met de bron erbij (Google Contacts, Google Calendar, Facebook, je notities of jij): bekijk [The Graph](graph.md#birthday).
- **Met jou**: wat diegene voor jou is, een contact voor Werk of Privé, en je Family of Fleet, met **Bekijk in Fleet**.
- **Ook op**: de andere plekken waar jullie contact hebben. **Slack** opent diegene in Slack, of jullie nieuwste Slack-gesprek.
- De **Personen** en **Projecten** waar diegene bij hoort, **Open tussen jullie** (beloftes in beide richtingen, met **Markeer als gedaan** en **Laten vallen**) en de **Tijdlijn**.

Adressen en chats van iemand worden vanzelf samengevoegd als duidelijk is dat het om één persoon gaat, bijvoorbeeld een werkmail waarin diegene het eigen adres in cc heeft staan.

Als een pagina de melding **Deze pagina kan niet worden geladen.** toont, tik je op **Opnieuw proberen**. Blijft de melding staan, tik dan onderaan de pagina op **Klopt er iets niet?**

## Samenvatting

Een paar korte regels bovenaan iemands pagina: wat er is besloten, gevraagd, gepland of beloofd, met de namen van iedereen die erbij betrokken is. The Machine herschrijft de samenvatting als er iets nieuws is, alleen voor mensen met wie je echt contact hebt, en controleert eerst elke regel. Meestal gebeurt dat één keer per dag; als er iets verandert, zoals een nieuwe deadline of een ingetrokken verzoek, binnen een paar uur.

Een vage regel wordt weggelaten. Als er niets concreets te melden is, is er geen samenvatting. Elke regel verwijst naar de bron: berichten van één dag delen één datum en tonen het aantal berichten. Tik erop om ze samen te openen.

Met **Bewerken** kun je de tekst aanpassen. Als er nieuws is, toont The Machine een **Voorgestelde update** met **Gebruiken** en **Mijn versie houden**. Met **Laat The Machine het schrijven** geef je de samenvatting weer aan hem over.

Vergaderingsvoorbereidingen gebruiken de samenvatting, maar alleen de regels van de kant van die to-do (Werk of Privé). De samenvatting blijft op je Machine. Je team kan hem nooit zien.

## Tijdlijn

Elke pagina van een persoon of organisatie heeft een tijdlijn, met de nieuwste items bovenaan: e-mail, vergaderingen en hun Zoom-samenvattingen, Intercom-gesprekken (met **Openen in Intercom**), WhatsApp-, Telegram-, Slack-, LinkedIn- en X-chats, to-do's, beloftes en projectupdates. Met de filters bovenaan bekijk je één bron tegelijk. Met **Meer tonen** laad je oudere items.

Aankomende vergaderingen staan bovenaan onder **Binnenkort**, met de eerstvolgende bovenaan. Met **Alles wat eraan komt tonen** zie je de rest. Bij een vergadering staan de deelnemers, ieder één keer. Bij een vergadering met notities of een transcript staat **Notities** of **Transcript**. Klik erop om ze te lezen.

Je tijdlijnen zijn van jou: de Graph van je team toont alleen wat je deelinstellingen toestaan. Met **Team** boven de tijdlijn op een pagina zie je wat teamgenoten hebben gedeeld, met bij elk item wie het heeft gedeeld. Met **Van mij** zie je alleen je eigen items.

## Werk en Privé

De tabbladen **Werk** en **Privé** tonen mensen op basis van hun Type, dat op hun pagina staat. Jouw keuze (**Bewerken**) gaat voor. Anders vallen je Family en Friends, en familie of vrienden voor jou (een vrouw, een vader), onder Privé, ongeacht vanaf welk adres ze schrijven. Je team ziet je privécontacten nooit.

## Iemand toevoegen

Tik bovenaan Personen op **Nieuwe persoon**, of op **+** in de bovenbalk op een telefoon. Vul een naam in, en eventueel een e-mailadres en organisatie. Als er al iemand in je Graph staat die hierop lijkt, toont het formulier die persoon bovenaan, zodat je die pagina kunt openen. Met **Toevoegen** open je de nieuwe pagina.

Iemand die je toevoegt blijft staan, ook als er nog geen berichten zijn. Het eerste bericht wordt aan die persoon gekoppeld.

## Iemand bewerken

Met **Bewerken** bovenaan de pagina pas je de naam, functietitel, organisatie, locatie, LinkedIn, telefoonnummers en e-mailadressen aan, en wat diegene voor jou is en of het een contact voor Werk of Privé is. Het veld **Notities** is bedoeld voor dingen die je wilt onthouden. Notities blijven behouden bij samenvoegen. Met **Opslaan** bewaar je de wijzigingen. Met **Annuleren** laat je alles zoals het was.

Je bewerkingen blijven behouden, ook wanneer de gegevens opnieuw worden opgezocht en bij **Samenvoegen** en **Ongedaan maken**. Maak een veld leeg om de opgezochte waarde weer te gebruiken. Als je de naam wist, wordt de naam uit de berichten weer gebruikt.

Klik op de foto om die te wijzigen: kies **Afbeelding uploaden**, selecteer een foto die voor die persoon is gevonden, of kies **Foto verwijderen**. De foto blijft op je Machine.

## Twee personen samenvoegen

Als twee personen misschien dezelfde zijn, vraagt hun pagina of het om dezelfde persoon gaat. In Personen staan ze dan onder **Zelfde persoon?**. Met **Samenvoegen** voeg je ze samen, inclusief alle berichten, notities, rollen en projecten. Met **Niet dezelfde** houd je ze voorgoed apart. Je keuze wordt even bij het paar weergegeven, waarna het uit de lijst verdwijnt. De lijst verdwijnt zodra er niets meer te beoordelen is.

Iemand met een adres dat alleen lijkt op een adres dat je kent, zoals acme-corp.example en acmecorp.example, wordt nooit voorgesteld als dezelfde persoon. Alleen jij kunt diegene een rol geven.

Een naam alleen is nooit genoeg om twee personen van verschillende domeinen samen te voegen, want iedereen kan een naam invoeren. Twee adressen op verschillende domeinen worden alleen voorgesteld als er nog iets anders is dat ze verbindt, zoals dezelfde personen of een project. Iemand die jouw naam gebruikt met een adres dat niet van jou is, wordt nooit voorgesteld. Voeg in plaats daarvan je andere adressen toe via Instellingen, [Je adressen](settings.md#your-addresses).

Als op verschillende domeinen alleen de voornaam overeenkomt, zoals "Sam" en "Sam Lee", worden ze alleen voorgesteld als ze hetzelfde telefoonnummer of LinkedIn-profiel hebben.

Een gedeeld adres, zoals info@ of een mailinglijst, wordt nooit samengevoegd met de personen die er via schrijven. Een werkcontact van buiten je bedrijf en een privéchat met alleen een naam gemeen worden niet automatisch samengevoegd: ze worden ter beoordeling getoond.

Met **Alles samenvoegen** voeg je alle paren in de lijst tegelijk samen, behalve de paren die je als **Niet dezelfde** hebt gemarkeerd. Met **Ongedaan maken** maak je ze direct weer allemaal ongedaan.

Wil je zelf twee personen samenvoegen, open dan een van hun pagina's en kies **⋯**, **Zelfde persoon als…** en de andere persoon. Op de pagina van een samengevoegde persoon staat onder **Samengevoegd vanuit** waarom ze zijn samengevoegd. Met **Ongedaan maken** splits je ze weer.

## Iemand definitief verwijderen

Open op de pagina het menu ⋯ en kies **Definitief verwijderen…**. Kies daarna **Verwijderen**. De persoon en alles wat je Machine over diegene weet, worden verwijderd: de vermelding, adressen, opgezochte gegevens, berichten die alleen tussen jullie zijn uitgewisseld en notities over diegene.

To-do's waarbij diegene betrokken is blijven staan, maar de naam wordt verwijderd. De persoon wordt niet opnieuw toegevoegd, ook niet via een import of een verjaardags-to-do van Facebook met de naam of het adres. Dit kun je niet ongedaan maken.

## Teruggestuurd

Als een e-mail aan iemand wordt teruggestuurd, staat er **Teruggestuurd** bij het adres, met de datum. Een ander adres van die persoon komt dan bovenaan te staan. Nieuwe concepten worden nooit naar dit adres gestuurd als er een ander adres bekend is. Is het het enige adres, dan krijg je een waarschuwing op het verzendscherm, maar kun je de e-mail nog steeds versturen.

Een teruggestuurde e-mail telt mee als de mailserver meldt dat het adres niet bestaat, of na 3 tijdelijke fouten verspreid over een week. De melding verdwijnt als diegene weer vanaf dat adres schrijft of als een e-mail naar dat adres wordt bezorgd.

## Functietitel en foto

Mensen met een bedrijfsadres krijgen een functietitel, foto, LinkedIn en plaats. Die gegevens worden opgezocht zoals bij [organisatiegegevens](organization-data.md). Op een gehoste Machine wordt alleen hun naam en bedrijfsdomein opgezocht. Voor een foto ontvangt Gravatar een hash van hun werkadres, nooit het adres zelf. Schakel dit uit via **Instellingen**, onder Beveiliging: **Werkcontacten opzoeken**.

Als de gegevens zijn opgezocht, toont hun pagina ook hun profieltekst, hoelang ze hun huidige functie al hebben en de twee functies daarvoor. De voorbereidingen gebruiken die informatie ook. De profieltekst wordt alleen gebruikt als ze geen eigen bio hebben.

Je Koppelingen vullen meer gegevens aan op basis van informatie die ze al hebben: een functietitel, telefoonnummer en tijdzone van Slack, een bio en plaats van X, een kopregel en foto van LinkedIn, functietitels van Google Contacts en Salesflare, en de foto van een contact uit Salesflare als Salesflare die zelf heeft. Beweeg de muisaanwijzer over de regel onder hun naam om te zien waar de informatie vandaan komt.

Outlook voegt foto's toe van collega's bij je organisatie en van je Outlook-contacten, plus de functietitels en bedrijven van je contacten ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Foto's van WhatsApp en Telegram worden opgehaald via je WhatsApp-synchronisatie en je Telegram-chatkoppeling: maximaal 50 per dag voor elke dienst, en alleen voor mensen die al in je Graph staan. Er wordt niets naar hen verstuurd. Een import van verjaardagen van Facebook voegt bij het opslaan de profielfoto toe van iemand die nog geen foto heeft ([Routines](routines.md)). Alles blijft op je Machine.

In een Fleet voor werk wordt een kleine kopie van een werkfoto meegestuurd met het gedeelde persoonsrecord in de [Team Graph](team-graph.md). Foto's uit Google Contacts, WhatsApp, Telegram of Facebook, en foto's die je hebt gewijzigd of verwijderd, worden nooit gedeeld.

## Over jou

Je eigen adressen en telefoonnummers, ook aliassen, zijn altijd van jou en nooit van iemand in je Graph. Als je naar jezelf zoekt of iemand toevoegt met een van je adressen, wordt **Over jou** geopend. Bij een import wordt je eigen rij overgeslagen.

Over jou toont je adressen en waar ze vandaan komen. Wijzig ze via **Instellingen**, onder Account. Kies **Mijn contactgegevens delen** om je eigen contactgegevens met een teamgenoot of vriend te delen. Bekijk [Een contact delen](share-contact.md).

## Wat iemand voor jou is

Rollen die je Machine in je berichten herkent, staan op hun pagina onder **Voor jou**, met de regel die hij heeft gelezen. Je hoeft niets te bevestigen. Klopt er iets niet? Pas het aan via **Bewerken** op hun pagina, of via **⋯** bij de regel onder **Recente wijzigingen**. The Machine leert van je bewerkingen.

## Wat de Machine over iemand weet

Feiten over iemand staan op hun pagina onder **Bekend over**. Bij Leren staan de algemene feiten. Met **Toevoegen** voeg je er zelf een toe. Elk feit heeft een menu:

- Met **Bewerken** pas je het direct aan.
- Met **Niet over deze persoon** maak je er weer een algemeen feit van, onder **Leren**, **Feiten**.
- Met **Verwijderen** verwijder je het overal.

## Recente wijzigingen

**Recente wijzigingen**, ingeklapt net boven de tijdlijn van een persoon, organisatie of project, toont wat je Machine over diegene heeft gewijzigd of geleerd: een rol, waar diegene werkt, hoe twee personen aan elkaar verwant zijn, een feit of een projectupdate. Bij elke regel staan de datum en de bron. Tik op de bron om het bericht te lezen.

Als een regel niet klopt, kun je dat direct aanpassen via **⋯**: **Bewerken**, **Verwijderen**, **Niet over deze persoon** of **Ongedaan maken** om een project terug te zetten naar de vorige plek. Je ziet drie regels. Met **Meer tonen** bekijk je de rest.

Bij iemand die je Machine vandaag heeft bijgewerkt, staat een stip in de Personenlijst. Bovenaan de lijst staat **Vandaag 4 personen bijgewerkt** met hun namen. Bekijk [The Graph](graph.md).

## Een to-do over iemand

Met **Nieuwe to-do** in het menu **⋯** van een persoon, organisatie of project maak je een to-do over diegene.
