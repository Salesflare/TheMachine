---
title: Personen
area: graph
summary: Iedereen met wie je contact hebt: hun pagina, samenvatting en tijdlijn, en hoe je iemand toevoegt, bewerkt, samenvoegt of verwijdert.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: a16cc66e51a64fd2
---
Iedereen met wie je contact hebt, met de mensen met wie je het meest contact hebt bovenaan. Ze komen uit je berichten en vergaderingen. Nieuwsbrieven, bonnetjes en andere mailings voegen pas iemand toe als je terugschrijft. Ze staan onder Verborgen afzenders, onder de lijst. Met Weergeven als persoon voeg je iemand toe. Velden, tags en import werken voor alle drie de lijsten hetzelfde. Elke lijst heeft eigen filters: zie [The Graph](graph.md).

Een gedeelde inbox (info@, klantenservice, de eigen naam van een winkel) telt voor de organisatie, niet als persoon, ook nadat je ernaar hebt geschreven.

## Pagina van iemand

Bovenaan staan de foto, naam, functie, organisatie en plaats, plus één regel over jullie contact ("Dagelijks contact · laatst contact gisteren · volgende vergadering di 27 okt"). Recent contact wordt weergegeven als "zojuist", "3 uur geleden", "gisteren" of "3 dagen geleden". Ouder contact wordt als datum weergegeven. Beweeg de aanwijzer erover voor de exacte datum. Daaronder vind je:

- **Contact**: hun telefoonnummers en e-mailadressen. Tik op een nummer of adres om te bellen of schrijven, of tik op **Kopiëren**. Hun **Verjaardag** staat hier ook, met de bron erbij (Google Contacten, Google Agenda, Facebook, je notities of jij): zie [The Graph](graph.md#birthday).
- **Met jou**: wat voor relatie je met hen hebt, of ze een werk- of privécontact zijn en of ze bij je familie of Fleet horen, met **Bekijk in Fleet**.
- **Ook op**: de andere plekken waar je met hen praat. **Slack** opent hun profiel in Slack of je nieuwste Slack-thread met hen.
- De **Personen** en **Projecten** waar ze deel van uitmaken, **Open tussen jullie** (beloftes over en weer, met **Markeer als gedaan** en **Laten vallen**) en hun **Tijdlijn**.

Adressen en chats van iemand worden automatisch samengevoegd als duidelijk is dat ze bij dezelfde persoon horen, bijvoorbeeld een werkadres met hun eigen adres in de cc.

Als er **Deze pagina kon niet worden geladen.** staat, tik je op **Opnieuw proberen**. Blijft de melding staan, tik dan onderaan de pagina op **Klopt er iets niet?**.

## Samenvatting

Een paar korte regels bovenaan iemands pagina. Ze vertellen wat er is besloten, gevraagd, gepland of beloofd, met vermelding van iedereen. The Machine herschrijft de samenvatting als er iets nieuws is, alleen voor mensen met wie je echt contact hebt. Hij controleert eerst elke regel. Meestal gebeurt dit één keer per dag. Als er iets verandert, zoals een nieuwe deadline of een ingetrokken verzoek, gebeurt het binnen een paar uur.

Een vage regel wordt weggelaten. Als er niets specifieks te melden is, verschijnt er geen samenvatting. Elke regel linkt naar de bron. Berichten van één dag worden gegroepeerd onder één datum, met het aantal berichten erbij, en kunnen samen worden geopend.

Tik op **Bewerken** om de tekst aan te passen. Als er nieuws is, toont The Machine een **Voorgestelde update**, met **Gebruiken** en **Mijn versie houden**. Met **Laat The Machine het schrijven** geef je de samenvatting weer aan hem.

De voorbereidingen voor vergaderingen gebruiken deze samenvatting, maar alleen de regels aan de kant van die to-do (Werk of Privé). De samenvatting blijft op je Machine. Je team ziet hem nooit.

## Tijdlijn

Elke pagina van een persoon of organisatie heeft een tijdlijn, met de nieuwste items bovenaan: e-mail, vergaderingen en hun Zoom-samenvattingen, Intercom-gesprekken (met **Openen in Intercom**), WhatsApp-, Telegram-, Slack-, LinkedIn- en X-chats, to-do's, beloftes en projectupdates. De filters bovenaan tonen telkens één bron. Met **Meer tonen** laad je oudere items.

Vergaderingen die nog moeten plaatsvinden staan bovenaan onder **Binnenkort**, met de eerstvolgende bovenaan. Met **Alles wat eraan komt tonen** bekijk je de rest. Bij een vergadering zie je wie erbij was, elke persoon één keer. Bij een vergadering met notities of een transcript staat **Notities** of **Transcript**. Klik erop om ze te lezen.

Je tijdlijnen zijn van jou. De Graph van je team toont alleen wat volgens je deelregels is toegestaan. Met **Team** boven de tijdlijn op een pagina zie je wat teamleden hebben gedeeld. Bij elk item staat van wie het komt. **Van mij** toont alleen je eigen items.

## Werk en Privé

De tabbladen **Werk** en **Privé** tonen mensen op basis van hun Type, dat op hun pagina staat. Je eigen keuze (**Bewerken**) gaat voor. Anders worden je familie en vrienden, en mensen die voor jou familie of vrienden zijn (zoals je vrouw of vader), als Privé ingedeeld, ongeacht het adres waarvan ze schrijven. Je team krijgt nooit privécontacten te zien.

## Iemand toevoegen

Tik bovenaan Personen op **Nieuwe persoon** of op **+** in de bovenbalk op je telefoon. Vul een naam in, en eventueel een e-mailadres en organisatie. Als er al iemand in je Graph staat die erop lijkt, toont het formulier die persoon bovenaan. Zo kun je die pagina openen. Met **Toevoegen** open je de nieuwe pagina.

Iemand die je toevoegt, blijft staan, ook als er nog geen berichten zijn. Het eerste bericht wordt aan die persoon gekoppeld.

## Iemand bewerken

Met **Bewerken** bovenaan de pagina pas je de naam, functie, organisatie, locatie, LinkedIn, telefoonnummers en e-mailadressen aan, en geef je aan wat voor relatie je met die persoon hebt en of het om een werk- of privécontact gaat. Het veld **Notities** is bedoeld voor informatie die je wilt onthouden. Notities blijven behouden bij het samenvoegen. Met **Opslaan** bewaar je de wijzigingen. Met **Annuleren** laat je alles zoals het was.

Je wijzigingen blijven behouden als de gegevens opnieuw worden opgezocht, en ook na **Samenvoegen** en **Ongedaan maken**. Maak een veld leeg om de opgezochte waarde weer te gebruiken. Als je de naam wist, wordt de naam uit hun berichten teruggezet.

Klik op de foto om die te wijzigen: kies **Afbeelding uploaden**, selecteer een gevonden foto of kies **Foto verwijderen**. De foto blijft op je Machine.

## Twee personen samenvoegen

Als twee personen mogelijk dezelfde zijn, vraagt hun pagina of het om dezelfde persoon gaat. In Personen staan ze dan onder **Zelfde persoon?**. Met **Samenvoegen** voeg je hun berichten, notities, rollen en projecten samen. Met **Niet dezelfde** houd je ze definitief uit elkaar. Je antwoord verschijnt even bij het paar, waarna het paar uit de lijst verdwijnt. De lijst verdwijnt zodra er niets meer te vragen is.

Iemand met een adres dat alleen lijkt op een adres dat je kent, zoals acme-corp.example en acmecorp.example, wordt nooit als dezelfde persoon voorgesteld. Alleen jij kunt die persoon een rol geven.

Een naam alleen is nooit genoeg om twee mensen op verschillende domeinen samen te voegen, want iedereen kan dezelfde naam gebruiken. Twee adressen op verschillende domeinen worden alleen als dezelfde persoon voorgesteld als er nog iets anders overeenkomt, zoals dezelfde mensen of een project. Iemand die jouw naam gebruikt op een adres dat niet van jou is, wordt nooit voorgesteld. Voeg in plaats daarvan je andere adressen toe onder Instellingen, [Je adressen](settings.md#your-addresses).

Als op verschillende domeinen alleen de voornaam overeenkomt, zoals bij "Sam" en "Sam Lee", worden ze alleen voorgesteld als ook het telefoonnummer of LinkedIn-profiel hetzelfde is.

Een gedeeld adres, zoals info@ of een mailinglijst, wordt nooit samengevoegd met de mensen die er via schrijven. Een werkcontact van buiten je bedrijf en een persoonlijk gesprek waarbij alleen de naam overeenkomt, worden niet automatisch samengevoegd. Ze verschijnen als een vraag.

Met **Alles samenvoegen** voeg je alle paren in de lijst tegelijk samen, behalve de paren die je als **Niet dezelfde** hebt gemarkeerd. Met **Ongedaan maken** direct daarna splits je ze allemaal weer.

Wil je zelf twee personen samenvoegen, open dan een van hun pagina's en kies **⋯**, **Zelfde persoon als…** en de andere persoon. Op de pagina van een samengevoegde persoon staat onder **Samengevoegd vanuit** waarom de personen zijn samengevoegd. Met **Ongedaan maken** splits je ze weer.

## Iemand definitief verwijderen

Open op de pagina van die persoon het menu ⋯ en kies **Definitief verwijderen…**. Kies daarna **Verwijderen**. Hiermee verwijder je die persoon en alles wat je Machine over hen weet: hun vermelding, adressen, opgezochte gegevens, berichten die alleen tussen jullie zijn uitgewisseld en notities over hen.

To-do's waarbij die persoon betrokken is, blijven staan, maar hun naam wordt verwijderd. De persoon wordt niet opnieuw toegevoegd, ook niet via een import of een Facebook-verjaardagsto-do met hun naam of adres. Dit kun je niet ongedaan maken.

## Niet bezorgd

Als een e-mail aan iemand wordt geweigerd, staat bij hun adres **Niet bezorgd**, met de datum. Een ander adres van die persoon komt dan bovenaan te staan. Nieuwe concepten worden nooit naar dat adres verstuurd als er een ander adres bekend is. Is dit het enige adres, dan waarschuwt het verzendvenster je, maar je kunt de e-mail nog steeds versturen.

Een e-mail wordt als geweigerd beschouwd als de mailserver zegt dat het adres niet bestaat, of na 3 tijdelijke fouten binnen een week. De melding verdwijnt als die persoon weer vanaf dat adres schrijft of als een e-mail naar dat adres wordt bezorgd.

## Functie en foto

Bij mensen met een bedrijfsadres worden hun functie, foto, LinkedIn en woonplaats opgezocht, net als bij [organisatiegegevens](organization-data.md). Op een gehoste Machine worden alleen hun naam en bedrijfsdomein opgezocht. Voor een foto krijgt Gravatar een hash van hun werkadres, nooit het adres zelf. Schakel dit uit via **Instellingen**, onder Beveiliging: **Werkcontacten opzoeken**.

Als de gegevens zijn opgezocht, zie je op hun pagina ook hun profieltekst, sinds wanneer ze hun huidige functie hebben en hun twee vorige functies. Ook voorbereidingen gebruiken deze informatie. De profieltekst wordt alleen gebruikt als ze zelf geen bio hebben.

Je contacten krijgen meer informatie van bronnen die ze al hebben geraadpleegd: een functietitel, telefoonnummer en tijdzone uit Slack, een bio en plaats uit X, een kopregel en foto uit LinkedIn, functietitels uit Google Contacten en Salesflare, en een foto van een contact uit Salesflare als Salesflare die zelf bewaart. Beweeg de aanwijzer over de regel onder hun naam om te zien waar de informatie vandaan komt.

Outlook voegt foto's toe van collega's bij je organisatie en van je Outlook-contacten, plus de functies en bedrijven van je contacten ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Foto's van WhatsApp en Telegram worden opgehaald via je WhatsApp-synchronisatie en je Telegram-chatkoppeling: maximaal 50 per dag per app, alleen voor mensen die al in je Graph staan. Er wordt niets naar hen verstuurd. Een import van Facebook-verjaardagen voegt de profielfoto toe van iemand zonder foto wanneer je die opslaat ([Routines](routines.md)). Alles blijft op je Machine.

In de [Team Graph](team-graph.md) van een Work Fleet wordt een kleine kopie van een werkfoto gedeeld bij iemands gedeelde profiel. Foto's uit Google Contacten, WhatsApp, Telegram of Facebook, en foto's die je hebt gewijzigd of verwijderd, worden nooit gedeeld.

## Over jou

Je eigen adressen en nummers, inclusief aliassen, zijn altijd van jou en nooit van iemand in je Graph. Als je jezelf zoekt of iemand toevoegt met een van je adressen, wordt **Over jou** geopend. Bij een import wordt je eigen rij overgeslagen.

Onder Over jou staan je adressen en de bron van elk adres. Wijzig ze in **Instellingen**, onder Account. Kies **Mijn contactgegevens delen** om je contactgegevens met een teamgenoot of vriend te delen. Zie [Een contact delen](share-contact.md).

## Wat je voor iemand bent

Rollen die je Machine in je berichten herkent, staan op hun pagina onder **Voor jou**, met alleen de woorden waaruit de rol blijkt, zoals een functietitel. Iemand die zegt dat diegene je boekhouder of klant is, is niet genoeg. Daarvoor is ook informatie van jouw kant nodig, zoals je eigen berichten of vergaderingen met die persoon. Je hoeft niets goed te keuren. Klopt er iets niet? Pas het aan met **Bewerken** op hun pagina, of met **⋯** bij de regel onder **Recente wijzigingen**. The Machine leert van je wijzigingen.

## Wat de Machine over iemand weet

Feiten over iemand staan op hun pagina onder **Bekend over**. Onder **Leren** staan de algemene inzichten. Met **Toevoegen** voeg je een feit toe in je eigen woorden. Elk feit heeft een menu:

- Met **Bewerken** pas je het direct aan.
- Met **Niet over deze persoon** maak je er weer een algemeen feit van, onder **Leren**, **Feiten**.
- Met **Verwijderen** verwijder je het overal.

## Recente wijzigingen

**Recente wijzigingen** staat ingeklapt vlak boven de tijdlijn van een persoon, organisatie of project. Je vindt er wat je Machine over hen heeft gewijzigd of geleerd: een rol, waar iemand werkt, hoe twee personen aan elkaar verwant zijn, een feit of een projectupdate. Bij elke regel staan de datum en de bron. Tik op de bron om het bericht te lezen.

Klopt een regel niet? Met **⋯** pas je die direct aan: **Bewerken**, **Verwijderen**, **Niet over deze persoon** of **Ongedaan maken** om een project terug te zetten naar de vorige plek. Er worden drie regels getoond. Met **Meer tonen** zie je de rest.

Iemand over wie je Machine vandaag informatie heeft bijgewerkt, heeft een klein stipje in de lijst Personen. Bovenaan de lijst staat **Vandaag 4 personen bijgewerkt**, met hun namen. Zie [The Graph](graph.md).

## Een to-do over iemand

Met **Nieuwe to-do** in het menu **⋯** van een persoon, organisatie of project maak je een to-do over diegene.
