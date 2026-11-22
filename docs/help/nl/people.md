---
title: Personen
area: graph
summary: Iedereen met wie je contact hebt: hun pagina, samenvatting en tijdlijn, en hoe je iemand toevoegt, bewerkt, samenvoegt of verwijdert.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e808343918f7f47
---
Iedereen met wie je contact hebt, de nauwste contacten eerst, op basis van je berichten en meetings. Nieuwsbrieven, ontvangstbewijzen en andere mailings voegen niemand toe totdat je terugschrijft. Ze staan onder Verborgen afzenders, onder de lijst: met Tonen als persoon voeg je iemand toe. Velden, tags en import werken hetzelfde in alle drie de lijsten. Elke lijst heeft eigen filters: zie [The Graph](graph.md).

Een gedeelde inbox (info@, klantenservice, de eigen naam van een winkel) telt mee voor de organisatie, niet als persoon, ook niet nadat je ernaartoe hebt geschreven.

## Pagina van iemand

Bovenaan staan de foto, naam, functie, organisatie en plaats, plus één regel over jullie contact ("Dagelijks contact · laatste contact gisteren · volgende afspraak di 27 okt"). Recent contact wordt weergegeven als "zojuist", "3 uur geleden", "gisteren" of "3 dagen geleden". Ouder contact wordt als datum weergegeven. Beweeg de muisaanwijzer erover voor de exacte datum. Daaronder:

- **Contact**: telefoonnummers en e-mailadressen. Klik op een nummer om te bellen of op een adres om te mailen, of klik op **Kopiëren**. Ook de **Verjaardag** staat hier, met de bron erbij (Google Contacten, Google Agenda, Facebook, je notities of jij): zie [The Graph](graph.md#birthday).
- **Met jou**: wat iemand voor je is, of diegene een werk- of privécontact is en bij je Familie of Fleet hoort, met **Bekijk in Fleet**.
- **Ook op**: de andere plekken waar je met iemand praat. **Slack** opent die persoon in Slack of opent jullie nieuwste Slack-thread.
- De **Personen** en **Projecten** waar iemand bij hoort, **Open tussen jullie** (beloftes over en weer, met **Als gedaan markeren** en **Laten vallen**) en hun **Tijdlijn**.

Adressen en chats van iemand worden vanzelf samengevoegd als duidelijk is dat ze bij dezelfde persoon horen, bijvoorbeeld een werkadres dat in de CC staat met het eigen adres van die persoon.

Als je **Deze pagina kon niet laden.** ziet, klik dan op **Opnieuw proberen**. Blijft de melding staan, klik dan onderaan de pagina op **Klopt er iets niet?**

## Samenvatting

Een paar korte regels bovenaan iemands pagina: wat er is besloten, gevraagd, gepland of beloofd, met iedereen bij naam genoemd. The Machine schrijft de samenvatting opnieuw als er iets nieuws is, alleen voor mensen met wie je echt contact hebt, en controleert elke regel eerst. Meestal gebeurt dat één keer per dag, maar binnen een paar uur als er iets verandert, zoals een nieuwe deadline of een ingetrokken verzoek.

Een vage regel wordt weggelaten. Als er niets specifieks te melden is, is er geen samenvatting. Elke regel linkt naar de bron: berichten van dezelfde dag staan samen onder één datum, met het aantal erbij, en kunnen samen worden geopend.

Met **Bewerken** kun je de tekst aanpassen. Bij nieuws toont The Machine een **Voorgestelde update**, met **Gebruiken** en **Mijn versie houden**. Met **Laat The Machine het schrijven** geef je de samenvatting weer terug aan The Machine.

Meetingvoorbereidingen gebruiken de samenvatting, maar alleen de regels van de kant van die to-do (Werk of Privé). De samenvatting blijft op je Machine. Je team kan hem nooit zien.

## Tijdlijn

Elke pagina van een persoon of organisatie heeft een tijdlijn, met het nieuwste bovenaan: e-mail, meetings en hun Zoom-samenvattingen, Intercom-gesprekken (met **Openen in Intercom**), WhatsApp-, Telegram-, Slack- en LinkedIn-chats, X-chats, to-do's, beloftes en projectwijzigingen. Met de chips bovenaan kies je één bron tegelijk. Met **Meer tonen** laad je oudere items.

Meetings die nog moeten plaatsvinden staan bovenaan onder **Binnenkort**, de eerstvolgende eerst. Met **Alles wat eraan komt tonen** zie je de rest. Bij een meeting staat wie erbij was, met elke persoon één keer. Bij een meeting met notities of een transcript staat **Notities** of **Transcript**. Klik erop om ze te lezen.

Je tijdlijnen zijn van jou: de Graph van het team toont alleen wat volgens je deelregels is toegestaan. Met **Team** boven de tijdlijn van een pagina zie je wat teamgenoten hebben gedeeld, met bij elk item wie het heeft gedeeld. Met **Van mij** zie je alleen je eigen items.

## Werk en privé

De tabbladen **Werk** en **Privé** tonen mensen op basis van hun Type, dat op hun pagina staat. Wat je zelf kiest met **Bewerken** gaat voor. Anders zijn je Familie en vrienden, en mensen die familie of vrienden van je zijn (een vrouw, een vader), privécontacten, ongeacht vanaf welk adres ze schrijven. Je team krijgt je privécontacten nooit te zien.

## Iemand toevoegen

Klik bovenaan Personen op **Nieuwe persoon**, of op **+** in de bovenbalk op een telefoon. Vul een naam in, en eventueel een e-mailadres en organisatie. Als er al iemand in je Graph staat die erop lijkt, toont het formulier die persoon eerst, zodat je diens pagina kunt openen. Met **Toevoegen** open je de nieuwe pagina.

Iemand die je toevoegt blijft staan, ook als er nog geen berichten zijn. Het eerste bericht wordt aan die persoon gekoppeld.

## Iemand bewerken

Met **Bewerken** bovenaan iemands pagina kun je de naam, functie, organisatie, locatie, LinkedIn, telefoonnummers en e-mailadressen aanpassen, net als wat die persoon voor je is en of het een werk- of privécontact is. Het veld **Notities** is bedoeld voor alles wat je wilt onthouden; notities blijven ook na samenvoegingen staan. Met **Opslaan** bewaar je de wijzigingen. Met **Annuleren** laat je alles zoals het was.

Je bewerkingen blijven behouden, ook wanneer de gegevens opnieuw worden opgezocht en na **Samenvoegen** en **Ongedaan maken**. Maak een veld leeg om de opgezochte waarde weer te gebruiken. Als je de naam wist, wordt de naam uit de berichten weer ingevuld.

Klik op de foto om die te wijzigen: kies **Afbeelding uploaden**, selecteer een foto die voor die persoon is gevonden of klik op **Foto verwijderen**. De foto blijft op je Machine.

## Twee personen samenvoegen

Als twee personen misschien dezelfde zijn, vraagt hun pagina of het om dezelfde persoon gaat. Personen toont ze dan onder **Zelfde persoon?**. Met **Samenvoegen** voeg je ze samen, inclusief al hun berichten, notities, rollen en projecten. Met **Niet dezelfde** houd je ze voorgoed apart. Je antwoord wordt even bij het paar getoond, waarna het paar uit de lijst verdwijnt. De lijst verdwijnt zodra er niets meer te vragen is.

Iemand met een adres dat alleen lijkt op een adres dat je kent, zoals acme-corp.example en acmecorp.example, wordt nooit voorgesteld als dezelfde persoon. Alleen jij kunt zo iemand een rol geven.

Een naam alleen is nooit genoeg om iemand op twee domeinen samen te voegen, want iedereen kan dezelfde naam gebruiken. Twee adressen op verschillende domeinen worden alleen voorgesteld als er nog iets anders overeenkomt, zoals dezelfde personen of een project. Iemand die jouw naam gebruikt met een adres dat niet van jou is, wordt nooit voorgesteld. Voeg in plaats daarvan je andere adressen toe via Instellingen, [Je adressen](settings.md#your-addresses).

Als alleen de voornaam overeenkomt op verschillende domeinen, zoals "Sam" en "Sam Lee", worden ze alleen voorgesteld als ook het telefoonnummer of LinkedIn-profiel overeenkomt.

Een gedeeld adres, zoals info@ of een mailinglijst, wordt nooit samengevoegd met de personen die er berichten mee versturen. Een werkcontact van buiten je bedrijf en een privéchat die alleen een naam gemeen hebben, worden niet automatisch samengevoegd. Ze verschijnen als vraag.

Met **Alles samenvoegen** voeg je alle paren in de lijst tegelijk samen, behalve de paren die je als **Niet dezelfde** hebt gemarkeerd. Met **Ongedaan maken** splits je ze direct daarna weer.

Wil je zelf twee personen samenvoegen? Open een van hun pagina's, klik op **⋯**, kies **Zelfde persoon als…** en selecteer de ander. Op de pagina van een samengevoegde persoon staat onder **Samengevoegd uit** waarom de personen zijn samengevoegd. Met **Ongedaan maken** splits je ze weer.

## Iemand definitief verwijderen

Open op iemands pagina het menu ⋯ en kies **Definitief verwijderen…**. Klik daarna op **Verwijderen**. Hiermee verwijder je die persoon en alles wat je Machine over die persoon weet: de vermelding, adressen, opgezochte gegevens, berichten die alleen tussen jullie zijn uitgewisseld en notities over die persoon.

To-do's waarbij die persoon betrokken is blijven staan, maar de naam wordt verwijderd. De persoon wordt niet opnieuw toegevoegd, ook niet via een import of een Facebook-verjaardagsto-do met diens naam of adres. Dit kan niet ongedaan worden gemaakt.

## Teruggekomen

Als een e-mail aan iemand terugkomt, staat er **Teruggekomen** bij het adres, met de datum. Een ander adres van die persoon komt dan eerst te staan. Nieuwe concepten worden nooit naar dat adres gestuurd als er een ander adres bekend is. Is dit het enige adres, dan krijg je een waarschuwing op het verzendscherm, maar je kunt de e-mail nog steeds versturen.

Een teruggestuurde e-mail telt mee als de mailserver meldt dat het adres niet bestaat, of na 3 tijdelijke fouten binnen een week. De melding verdwijnt wanneer die persoon weer vanaf dat adres schrijft of wanneer een e-mail naar dat adres wordt bezorgd.

## Functie en foto

Van mensen met een zakelijk adres worden de functie, foto, LinkedIn en plaats opgezocht, net als [organisatiegegevens](organization-data.md). Op een gehoste Machine worden alleen hun naam en bedrijfsdomein opgezocht. Voor een foto krijgt Gravatar een hash van het zakelijke adres, nooit het adres zelf. Schakel dit uit via **Instellingen**, onder Beveiliging: **Werkcontacten opzoeken**.

Met die instelling wordt ook de korte zoekopdracht op internet vóór een eerste meeting uitgeschakeld (zie [Klaar voor je meetings](calendar.md#ready-for-your-meetings)).

Als de gegevens zijn gevonden, toont hun pagina ook hun beschrijving, sinds wanneer ze hun huidige functie hebben en hun twee vorige functies. Voorbereidingen lezen die ook, maar alleen de beschrijving als iemand geen eigen bio heeft.

Je koppelingen vullen meer aan met wat ze al lezen: een functie, telefoonnummer en tijdzone uit Slack, een bio en plaats uit X, een kopregel en foto van LinkedIn, functietitels uit Google Contacten en Salesflare, en een contactfoto uit Salesflare als Salesflare die zelf heeft. Beweeg de muisaanwijzer over de regel onder hun naam om te zien waar de informatie vandaan komt.

Outlook voegt foto's toe van collega's bij je organisatie en van je Outlook-contacten, plus de functies en bedrijven van je contacten ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Foto's van WhatsApp en Telegram worden opgehaald via je WhatsApp-synchronisatie en je Telegram-chatkoppeling: maximaal 50 per dag per dienst, alleen voor mensen die al in je Graph staan. Er wordt niets naar hen verstuurd. Een Facebook-verjaardagenimport voegt de profielfoto toe van iemand zonder foto wanneer je die opslaat ([Routines](routines.md)). Alles blijft op je Machine.

In de [Team-Graph](team-graph.md) van een Werk-Fleet wordt een kleine kopie van een werkfoto gedeeld bij iemands gedeelde profiel. Foto's uit Google Contacten, WhatsApp, Telegram of Facebook, en foto's die je hebt gewijzigd of verwijderd, worden nooit gedeeld.

## Over jou

Je eigen adressen en nummers, ook aliassen, zijn altijd van jou en nooit van iemand in je Graph. Als je jezelf zoekt of iemand toevoegt met een van je adressen, wordt **Over jou** geopend. Bij een import wordt je eigen rij overgeslagen.

Bij Over jou staan je adressen met de bron van elk adres. Je kunt ze wijzigen via **Instellingen**, onder Account. Kies **Mijn contactgegevens delen** om je eigen contactgegevens naar een teamgenoot of vriend te sturen. Zie [Een contact delen](share-contact.md).

## Wat iemand voor je is

Rollen die je Machine in je berichten herkent, staan op iemands pagina onder **Voor jou**, met alleen de woorden die de rol aangeven, zoals een functietitel. Alleen zeggen dat iemand je boekhouder of klant is, is niet genoeg: er moet ook iets van jouw kant zijn, zoals je eigen berichten of meetings met die persoon. Niets wacht op je goedkeuring. Klopt het niet? Pas het aan met **Bewerken** op de pagina, of met **⋯** op de regel onder **Recente wijzigingen**. The Machine leert van je aanpassingen.

## Wat hij over iemand weet

Feiten over iemand staan op hun pagina onder **Bekend over**. Bij **Leren** staan de algemene feiten. Met **Toevoegen** voeg je er zelf een toe, in je eigen woorden. Elk feit heeft een menu:

- Met **Bewerken** pas je het direct aan.
- Met **Niet over deze persoon** maak je er weer een algemeen feit van, onder **Leren**, **Feiten**.
- Met **Verwijderen** haal je het overal weg.

## Recente wijzigingen

Onder **Recente wijzigingen**, ingeklapt direct boven de tijdlijn van een persoon, organisatie of project, staat wat je Machine over die persoon, organisatie of dat project heeft gewijzigd of geleerd: een rol, waar iemand werkt, hoe twee personen met elkaar verbonden zijn, een feit of een projectwijziging. Elke regel heeft een datum en bron. Klik op de bron om het bericht te lezen.

Klopt een regel niet? Met **⋯** kun je die direct aanpassen: **Bewerken**, **Verwijderen**, **Niet over deze persoon** of **Ongedaan maken** om een project terug te zetten naar de vorige plek. Je ziet drie regels; met **Meer tonen** bekijk je de rest.

Iemand die je Machine vandaag heeft bijgewerkt, heeft een stip naast de naam in de lijst Personen. Bovenaan de lijst staat **4 personen vandaag bijgewerkt**, met hun namen erbij. Zie [The Graph](graph.md).

## Een to-do over iemand

Met **Nieuwe to-do** in het menu **⋯** van een persoon, organisatie of project maak je een to-do over die persoon, organisatie of dat project.
