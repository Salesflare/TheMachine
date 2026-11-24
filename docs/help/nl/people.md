---
title: Mensen
area: graph
summary: Iedereen met wie je contact hebt: hun pagina, samenvatting en tijdlijn, en hoe je iemand toevoegt, bewerkt, samenvoegt of verwijdert.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e671ff84b143e74
---
Iedereen met wie je contact hebt, van nauw naar minder nauw, op basis van je berichten en meetings. Nieuwsbrieven, ontvangstbewijzen en andere mailings voegen pas iemand toe als je terugschrijft. Ze staan onder Verborgen afzenders, onder de lijst: met Weergeven als persoon voeg je iemand toe. Velden, tags en import werken op alle drie de lijsten hetzelfde. Elke lijst heeft eigen filters: zie [The Graph](graph.md).

Een gedeelde inbox (info@, klantenservice, de naam van een winkel) telt voor de organisatie, niet als persoon, ook nadat je ernaartoe hebt geschreven.

## Iemands pagina

Bovenaan staan hun foto, naam, titel, organisatie en locatie, plus een regel over jullie contact ("Dagelijks contact · laatste contact gisteren · volgende meeting di. 27 okt."). Recent contact wordt weergegeven als "zojuist", "3 uur geleden", "gisteren" of "3 dagen geleden". Ouder contact wordt weergegeven als een datum. Houd de aanwijzer erboven voor de exacte datum. Daaronder vind je:

- **Contact**: hun telefoonnummers en e-mailadressen. Tik op een nummer of adres om te bellen of schrijven, of tik op **Kopiëren**. Hun **Verjaardag** staat hier ook, met de bron erbij (Google Contacts, Google Calendar, Facebook, je notities of jijzelf): zie [The Graph](graph.md#birthday).
- **Met jou**: wat ze voor je zijn, een werk- of privécontact, en je familie of Fleet, met **Bekijk in Fleet**.
- **Ook op**: de andere plekken waar je met hen praat. **Slack** opent hun profiel in Slack, of je nieuwste Slack-thread met hen.
- **Mensen** en **Projecten** waar ze deel van uitmaken, **Open tussen jullie** (beloftes over en weer, met **Als gedaan markeren** en **Laten vallen**), en hun **Tijdlijn**.

Adressen en chats van iemand worden automatisch samengevoegd als duidelijk is dat het om één persoon gaat, bijvoorbeeld een werkadres met hun eigen adres in cc. Dat gebeurt ook als iemand met wie je chat een gesprek boekt via de link die je daar hebt gestuurd, en hun bedrijf of achternaam overeenkomt.

Als er **Deze pagina kan niet worden geladen.** staat, tik je op **Opnieuw proberen**. Blijft dat zo, gebruik dan **Klopt er iets niet?** onderaan de pagina.

## Samenvatting

Bovenaan iemands pagina staan een paar korte regels over wat er is besloten, gevraagd, gepland of beloofd, met iedereen bij naam genoemd. The Machine herschrijft de samenvatting als er iets nieuws is, alleen voor mensen met wie je echt contact hebt. Hij controleert elke regel eerst. Meestal gebeurt dat één keer per dag; als er iets verandert in een kwestie met die persoon, zoals een nieuwe deadline of een ingetrokken verzoek, gebeurt het binnen een paar uur.

Een vage regel wordt weggelaten. Is er niets specifieks te melden, dan is er geen samenvatting. Elke regel linkt naar de bron: berichten van één dag delen één datum met het aantal berichten, en kunnen samen worden geopend.

**Bewerken** om het op jouw manier te verwoorden. Is er nieuws, dan toont The Machine een **Voorgestelde update**, met **Gebruiken** en **Mijn versie houden**. Met **Laat The Machine het schrijven** geef je de tekst weer aan hem terug.

Voorbereidingen voor meetings gebruiken de samenvatting, maar alleen de regels aan de kant van die to-do (Werk of Privé). De samenvatting blijft op je Machine; je team ziet hem nooit.

## Tijdlijn

Elke pagina van een persoon of organisatie heeft een tijdlijn, met de nieuwste items bovenaan: e-mail, meetings en hun Zoom-samenvattingen, Intercom-gesprekken (met **Openen in Intercom**), WhatsApp-, Telegram-, Slack-, LinkedIn- en X-chats, to-do's, beloftes en projectupdates. De chips bovenaan tonen telkens één bron. Met **Meer tonen** laad je oudere items.

Meetings die nog moeten plaatsvinden staan bovenaan onder **Binnenkort**, met de eerstvolgende bovenaan. Met **Alles wat eraan komt tonen** zie je de rest. Bij een meeting zie je wie erbij was, elke persoon één keer. Bij een meeting met notities of een transcript staat **Notities** of **Transcript**. Klik erop om ze te lezen.

Je tijdlijnen zijn van jou: de Graph van je team toont alleen wat volgens je deelinstellingen is toegestaan. Op een pagina voegt **Team** boven de tijdlijn gedeelde items van teamgenoten toe. Bij elk item staat van wie het komt. **Van mij** toont alleen jouw items.

## Werk en Privé

De tabbladen **Werk** en **Privé** tonen mensen op basis van hun type, dat op hun pagina staat. Jouw keuze (**Bewerken**) gaat voor. Anders zijn je familie en vrienden, en familie of vrienden voor jou (een echtgenote, een vader), privécontacten, ongeacht vanaf welk adres ze schrijven. Je team krijgt nooit privécontacten te zien.

## Iemand toevoegen

Kies **Nieuwe persoon** bovenaan Mensen, of **+** in de bovenbalk op een telefoon. Vul een naam in, en een e-mailadres en organisatie als je die weet. Staat er al iemand zoals deze persoon in je Graph, dan toont het formulier die eerst, zodat je die pagina kunt openen. Met **Toevoegen** open je de nieuwe pagina.

Iemand die je toevoegt blijft staan, ook als er nog geen berichten zijn. Het eerste bericht wordt aan die persoon gekoppeld.

## Iemand bewerken

Met **Bewerken** bovenaan hun pagina wijzig je hun naam, titel, organisatie, locatie, LinkedIn, telefoonnummers en e-mailadressen, wat ze voor je zijn en of het om Werk of Privé gaat. Het veld **Notities** is voor dingen die je wilt onthouden. Notities blijven behouden bij samenvoegen. Met **Opslaan** bewaar je de wijzigingen. Met **Annuleren** laat je alles zoals het was.

Je wijzigingen blijven staan, ook als hun gegevens opnieuw worden opgezocht, en na **Samenvoegen** en **Ongedaan maken**. Maak een veld leeg om de opgezochte waarde weer te gebruiken. Maak je de naam leeg, dan wordt de naam uit hun berichten teruggezet.

Klik op hun foto om die te wijzigen: **Afbeelding uploaden**, kies een gevonden foto of **Foto verwijderen**. De foto blijft op je Machine.

## Twee mensen samenvoegen

Als twee mensen misschien dezelfde persoon zijn, vraagt hun pagina of het om dezelfde persoon gaat. Mensen toont ze onder **Zelfde persoon?**. Met **Samenvoegen** voeg je ze samen, met al hun berichten, notities, rollen en projecten. Met **Niet dezelfde** houd je ze voorgoed apart. Je keuze wordt even bij het paar getoond, waarna het uit de lijst verdwijnt. De lijst verdwijnt zodra er niets meer te vragen is.

Iemand met een adres dat alleen lijkt op een adres dat je kent, zoals acme-corp.example en acmecorp.example, wordt nooit als dezelfde persoon voorgesteld. Alleen jij kunt die persoon een rol geven.

Een naam alleen is nooit genoeg om mensen van twee domeinen samen te voegen, omdat iedereen een naam kan typen. Twee adressen op verschillende domeinen worden alleen voorgesteld als er nog iets anders is dat ze aan elkaar linkt, zoals dezelfde mensen of een project. Iemand die jouw naam gebruikt met een adres dat niet van jou is, wordt nooit voorgesteld. Voeg in plaats daarvan je andere adressen toe via **Instellingen**, [Je adressen](settings.md#your-addresses).

Als alleen de voornaam overeenkomt bij verschillende domeinen, zoals "Sam" en "Sam Lee", worden ze alleen voorgesteld als het telefoonnummer of LinkedIn-profiel hetzelfde is.

Als alleen de voornaam overeenkomt met die van iemand in een meeting die vanuit een chat is aangemaakt, of als het adres van iemand is die je al kende en alleen de persoon in de chat zegt dat het van hen is, krijg je de vraag. The Machine opent nooit een link om dit te controleren.

Een gedeeld adres, zoals info@ of een mailinglijst, wordt nooit samengevoegd met de mensen die via dat adres schrijven. Een werkcontact van buiten je bedrijf en een privéchat met alleen een naam gemeen worden niet automatisch samengevoegd: ze verschijnen als vraag.

Met **Alles samenvoegen** voeg je alle paren in de lijst tegelijk samen, behalve de paren die je als **Niet dezelfde** hebt gemarkeerd. Met **Ongedaan maken** splits je ze direct daarna weer allemaal op.

Wil je zelf twee mensen samenvoegen, open dan een van hun pagina's, kies **⋯**, **Zelfde persoon als…** en selecteer de andere persoon. Op de pagina van de samengevoegde persoon staat onder **Samengevoegd vanuit** waarom ze zijn samengevoegd. Met **Ongedaan maken** splits je ze weer op.

## Iemand definitief verwijderen

Open op hun pagina het menu ⋯ en kies **Definitief verwijderen…**, gevolgd door **Verwijderen**. De persoon en alles wat je Machine over hen weet, worden verwijderd: hun profiel, adressen, opgezochte gegevens, berichten die alleen tussen jullie twee zijn uitgewisseld en notities over hen.

To-do's waarbij ze betrokken zijn, blijven staan, maar hun naam wordt verwijderd. Ze worden niet opnieuw toegevoegd, ook niet via een import of een to-do voor Facebook-verjaardagen met hun naam of adres. Dit kan niet ongedaan worden gemaakt.

## Teruggestuurd

Als een e-mail aan iemand wordt teruggestuurd, staat er **Teruggestuurd** bij hun adres, met de datum. Een ander adres van hen komt dan eerst te staan. Nieuwe concepten worden nooit naar dat adres gestuurd als er een ander adres bekend is. Is dat hun enige adres, dan krijg je een waarschuwing op het verstuurblad, maar kun je de e-mail nog steeds versturen.

Een teruggestuurde e-mail telt mee als de mailserver aangeeft dat het adres niet bestaat, of na 3 tijdelijke fouten verspreid over een week. De melding verdwijnt als ze weer vanaf dat adres schrijven of als een e-mail naar dat adres wordt afgeleverd.

## Functietitel en foto

Bij mensen met een zakelijk adres worden hun functietitel, foto, LinkedIn en stad opgezocht, net als bij [gegevens over organisaties](organization-data.md). Op een gehoste Machine worden alleen hun naam en bedrijfsdomein opgezocht. Voor een foto krijgt Gravatar een hash van hun zakelijke adres, nooit het adres zelf. Schakel dit uit via **Instellingen**, onder Beveiliging: **Werkcontacten opzoeken**.

Met die instelling wordt ook voorkomen dat de website wordt gelezen vóór een eerste meeting, en dat er op internet wordt gezocht als die optie is ingesteld (zie [Klaargezet voor je meetings](calendar.md#ready-for-your-meetings)).

Als de gegevens zijn opgezocht, toont hun pagina ook hun over-tekst, hoelang ze hun huidige functie al hebben en hun twee vorige functies. Ook voorbereidingen gebruiken deze gegevens. De over-tekst wordt alleen gebruikt als ze geen eigen bio hebben.

Je contacten worden verder aangevuld met gegevens die ze al hebben gelezen: een titel, telefoonnummer en tijdzone uit Slack, een bio en locatie uit X, een kopregel en foto uit LinkedIn, functietitels uit Google Contacts en Salesflare, en een contactfoto uit Salesflare als die daar zelf is opgeslagen. Houd de aanwijzer boven de regel onder hun naam om te zien waar de informatie vandaan komt.

Outlook voegt foto's toe van collega's bij je organisatie en van je Outlook-contacten, plus de functietitels en bedrijven van je contacten ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Foto's van WhatsApp en Telegram worden opgehaald via je WhatsApp-sync en Telegram-chatskoppeling: maximaal 50 per dag per app, alleen voor mensen die al in je Graph staan. Er wordt niets naar hen verstuurd. Bij een import van Facebook-verjaardagen wordt de profielfoto van iemand zonder foto toegevoegd als je die opslaat ([Routines](routines.md)). Alles blijft op je Machine.

In de [Team-Graph](team-graph.md) van een Werk-Fleet wordt een kleine kopie van een werkfoto met het gedeelde profiel van iemand meegestuurd. Foto's uit Google Contacts, WhatsApp, Telegram of Facebook, en foto's die je hebt gewijzigd of verwijderd, worden nooit meegestuurd.

## Over jou

Je eigen adressen en telefoonnummers, inclusief aliassen, zijn altijd van jou en nooit van iemand in je Graph. Als je jezelf zoekt of iemand toevoegt met een van je adressen, wordt **Over jou** geopend. Bij een import wordt je eigen rij overgeslagen.

Bij Over jou staan je adressen en de bron van elk adres. Je kunt ze wijzigen via **Instellingen**, onder Account. Kies **Mijn contactgegevens delen** om je eigen contactgegevens naar een teamgenoot of vriend te sturen. Zie [Een contact delen](share-contact.md).

## Wat iemand voor je is

Rollen die je Machine in je berichten herkent, staan op hun pagina onder **Voor jou**, met alleen de woorden die de rol aangeven, zoals een functietitel. Dat iemand zegt dat die je accountant of klant is, is niet genoeg. Dat moet ook blijken uit jouw kant, bijvoorbeeld uit je eigen berichten of meetings met die persoon. Je hoeft hiervoor niets te bevestigen. Klopt het niet? Pas het aan via **Bewerken** op hun pagina, of via **⋯** bij de regel in **Recente wijzigingen**. The Machine leert van je aanpassingen.

## Wat de Machine over iemand weet

Feiten over iemand staan op hun pagina onder **Bekend over**. Bij Inzichten staan de algemene feiten. Met **Toevoegen** voeg je er zelf een toe, in je eigen woorden. Elk feit heeft een menu:

- Met **Bewerken** pas je het meteen aan.
- Met **Niet over** maak je er weer een algemeen feit van, onder **Leren**, **Feiten**.
- Met **Verwijderen** haal je het overal weg.

## Recente wijzigingen

**Recente wijzigingen**, ingeklapt net boven de tijdlijn van een persoon, organisatie of project, toont wat je Machine over die persoon, organisatie of dat project heeft gewijzigd of geleerd: een rol, waar iemand werkt, hoe twee mensen aan elkaar verwant zijn, een feit of een projectupdate. Elke regel toont de datum en de bron. Tik op de bron om het bericht te lezen.

Klopt een regel niet? Met **⋯** pas je die meteen aan: **Bewerken**, **Verwijderen**, **Niet over** of **Ongedaan maken** om een project terug te zetten naar de vorige plek. Er worden drie regels getoond. Met **Meer tonen** zie je de rest.

Bij iemand die je Machine vandaag heeft bijgewerkt, staat een kleine stip in de Mensenlijst. Bovenaan de lijst staat **Vandaag 4 mensen bijgewerkt**, met hun namen erbij. Zie [The Graph](graph.md).

## Een to-do over iemand

Met **Nieuwe to-do** in het menu **⋯** van een persoon, organisatie of project maak je een to-do over diegene.
