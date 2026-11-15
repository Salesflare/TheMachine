---
title: Personen
area: graph
summary: Iedereen met wie je contact hebt: hun pagina, samenvatting en tijdlijn, en hoe je iemand toevoegt, bewerkt, samenvoegt of verwijdert.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 907cec019dc70184
---
Iedereen met wie je contact hebt, van meest naar minst recent, uit je berichten en vergaderingen. Nieuwsbrieven, bonnetjes en andere mailings voegen pas iemand toe als je terugschrijft. Ze staan onder Verborgen afzenders, onder de lijst. Met **Als persoon weergeven** voeg je iemand toe. Velden, tags en import werken voor alle drie de lijsten hetzelfde. Elke lijst heeft eigen filters. Zie [The Graph](graph.md).

Een gedeelde inbox (info@, klantenservice of de eigen naam van een winkel) hoort bij de organisatie, niet bij een persoon, ook niet nadat je ernaartoe hebt gemaild.

## Pagina van iemand

Bovenaan staan de foto, naam, functie, organisatie en plaats, met één regel over jullie contact ("Dagelijks contact · laatste contact gisteren · volgende vergadering di 27 okt"). Recent contact wordt weergegeven als "zojuist", "3 uur geleden", "gisteren" of "3 dagen geleden". Oudere contacten worden als datum weergegeven. Beweeg de muisaanwijzer erover om de exacte datum te zien. Daaronder vind je:

- **Contact**: telefoonnummers en e-mailadressen. Tik op een nummer of adres om te bellen of te schrijven, of tik op **Kopiëren**. Ook de **Verjaardag** staat hier, met de bron erbij (Google-contacten, Google Agenda, Facebook, je notities of jij): zie [The Graph](graph.md#birthday).
- **Met jou**: wat iemand voor je is, als werk- of privécontact, en of diegene bij je gezin of Fleet hoort, met **Bekijk in Fleet**.
- **Ook op**: de andere plekken waar jullie contact hebben. Met **Slack** open je die persoon in Slack, of je nieuwste Slack-gesprek met diegene.
- De **Personen** en **Projecten** waar diegene bij hoort, **Open tussen jullie** (beloftes over en weer, met **Markeer als gedaan** en **Laten vallen**) en de **Tijdlijn**.

Adressen en chats worden vanzelf aan iemand gekoppeld als duidelijk is dat het om dezelfde persoon gaat, bijvoorbeeld een werkadres met het eigen e-mailadres in cc.

Als er **Kan deze pagina niet laden.** staat, tik je op **Opnieuw proberen**. Blijft die melding staan, gebruik dan **Klopt er iets niet?** onderaan de pagina.

## Samenvatting

Een paar korte regels bovenaan iemands pagina. Ze vertellen wat er is besloten, gevraagd, gepland of beloofd, en noemen iedereen bij naam. The Machine herschrijft de samenvatting als er iets nieuws is, alleen voor mensen met wie je echt contact hebt, en controleert eerst elke regel. Meestal gebeurt dat één keer per dag, maar binnen een paar uur als er iets verandert, zoals een nieuwe deadline of een ingetrokken verzoek.

Een vage regel wordt weggelaten. Als er niets specifieks te melden is, is er geen samenvatting. Elke regel linkt naar de bron. Berichten van dezelfde dag delen één datum met het aantal berichten en kunnen samen worden geopend.

Met **Bewerken** schrijf je de samenvatting op jouw manier. Als er nieuws is, toont The Machine een **Voorgestelde update** met **Gebruiken** en **Mijn versie houden**. Met **Laat The Machine het schrijven** laat je The Machine de samenvatting weer schrijven.

De voorbereiding voor vergaderingen gebruikt deze samenvatting, maar alleen de regels aan de kant van die to-do (Werk of Privé). De samenvatting blijft op je Machine. Je team kan hem nooit zien.

## Tijdlijn

Elke pagina van een persoon of organisatie heeft een tijdlijn, met het nieuwste bovenaan: e-mails, vergaderingen en hun Zoom-samenvattingen, Intercom-gesprekken (met **Openen in Intercom**), WhatsApp-, Telegram-, Slack-, LinkedIn- en X-chats, to-do's, beloftes en wijzigingen aan projecten. De filters bovenaan tonen één bron tegelijk. Met **Meer tonen** laad je oudere items.

Vergaderingen die nog moeten plaatsvinden staan bovenaan onder **Binnenkort**, met de eerstvolgende bovenaan. Met **Alles wat eraan komt tonen** zie je de rest. Bij een vergadering staat wie erbij was, met elke persoon één keer. Bij een vergadering met notities of een transcript staat **Notities** of **Transcript**. Klik erop om ze te lezen.

Je tijdlijnen zijn van jou. De Graph van je team toont alleen wat je deelinstellingen toestaan. Op een pagina toont **Team** boven de tijdlijn wat teamgenoten hebben gedeeld, met bij elk item wie het heeft gedeeld. **Van mij** toont alleen jouw items.

## Werk en privé

De tabbladen **Werk** en **Privé** tonen mensen op basis van hun Type, zoals dat op hun pagina staat. Jouw keuze (**Bewerken**) heeft voorrang. Anders zijn je gezin en vrienden, en familieleden of vrienden van jou (zoals een vrouw of vader), privécontacten, ongeacht vanaf welk adres ze schrijven. Je team krijgt nooit privécontacten te zien.

## Iemand toevoegen

Kies **Nieuwe persoon** bovenaan Personen, of **+** in de bovenbalk op een telefoon. Vul een naam in, en ook een e-mailadres en organisatie als je die weet. Als iemand die hierop lijkt al in je Graph staat, toont het formulier die persoon bovenaan, zodat je die pagina kunt openen. Met **Toevoegen** open je de nieuwe pagina.

Iemand die je toevoegt blijft staan, ook als er nog geen berichten zijn. Het eerste bericht wordt aan die persoon gekoppeld.

## Iemand bewerken

Met **Bewerken** bovenaan de pagina wijzig je iemands naam, functie, organisatie, locatie, LinkedIn, telefoonnummers en e-mailadressen, wat diegene voor je is en of het een werk- of privécontact is. Het veld **Notities** is voor dingen die je wilt onthouden. Notities blijven behouden bij het samenvoegen. Met **Opslaan** bewaar je de wijzigingen. Met **Annuleren** laat je alles zoals het was.

Je wijzigingen blijven staan als de gegevens opnieuw worden opgezocht, en ook na **Samenvoegen** en **Ongedaan maken**. Maak een veld leeg om de opgezochte waarde weer te gebruiken. Als je de naam wist, wordt de naam uit de berichten weer ingevuld.

Klik op de foto om die te wijzigen: kies **Afbeelding uploaden**, een foto die voor die persoon is gevonden, of **Foto verwijderen**. De foto blijft op je Machine.

## Twee personen samenvoegen

Als twee personen misschien dezelfde persoon zijn, vraagt hun pagina of het om dezelfde persoon gaat. In Personen staan ze dan onder **Zelfde persoon?**. Met **Samenvoegen** voeg je ze samen, inclusief alle berichten, notities, rollen en projecten. Met **Niet dezelfde** houd je ze voorgoed apart. Je keuze wordt even bij het paar getoond, waarna het uit de lijst verdwijnt. De lijst verdwijnt zodra er niets meer te controleren is.

Iemand met een adres dat alleen lijkt op een adres dat je kent, zoals acme-corp.example tegenover acmecorp.example, wordt nooit voorgesteld als dezelfde persoon. Alleen jij kunt diegene een rol geven.

Een naam alleen is nooit genoeg om twee personen van verschillende domeinen samen te voegen, want iedereen kan dezelfde naam opgeven. Twee adressen op verschillende domeinen worden alleen als mogelijke match voorgesteld als er nog iets anders aan elkaar linkt, zoals dezelfde mensen of een project. Iemand die jouw naam gebruikt op een adres dat niet van jou is, wordt nooit voorgesteld. Voeg in plaats daarvan je andere adressen toe via Instellingen, [Je adressen](settings.md#your-addresses).

Een gedeeld adres, zoals info@ of een mailinglijst, wordt nooit gekoppeld aan de mensen die via dat adres schrijven. Een werkcontact van buiten je bedrijf en een privéchat die alleen een naam gemeen hebben, worden niet vanzelf samengevoegd. Ze worden als mogelijke match getoond.

Met **Alles samenvoegen** voeg je alle paren in de lijst tegelijk samen, behalve de paren die je als **Niet dezelfde** hebt gemarkeerd. Met **Ongedaan maken** maak je alle samenvoegingen meteen ongedaan.

Wil je zelf twee personen samenvoegen? Open dan een van hun pagina's, kies **⋯**, **Zelfde persoon als…** en selecteer de andere persoon. Op de pagina van de samengevoegde persoon staat onder **Samengevoegd vanuit** waarom de personen zijn samengevoegd. Met **Ongedaan maken** splits je ze weer.

## Iemand definitief verwijderen

Open op de pagina het menu **⋯**, kies **Definitief verwijderen…** en daarna **Verwijderen**. Hiermee verwijder je die persoon en alles wat je Machine over diegene weet: de vermelding, adressen, opgezochte gegevens, berichten die alleen tussen jullie zijn uitgewisseld en notities over die persoon.

To-do's waar die persoon bij betrokken is, blijven staan, maar de naam wordt verwijderd. Die persoon wordt niet opnieuw toegevoegd, ook niet via een import of een Facebook-verjaardagsto-do met diens naam of adres. Dit kan niet ongedaan worden gemaakt.

## Teruggestuurd

Als een e-mail aan iemand wordt teruggestuurd, staat er **Teruggestuurd** met de datum bij het adres. Een ander adres van die persoon komt dan bovenaan te staan. Nieuwe concepten worden nooit naar het teruggestuurde adres gestuurd als er een ander adres bekend is. Is dit het enige adres, dan waarschuwt het verzendscherm je, maar je kunt de e-mail nog steeds versturen.

Een teruggestuurde e-mail telt mee als de mailserver meldt dat het adres niet bestaat, of na 3 tijdelijke fouten verspreid over een week. De melding verdwijnt als die persoon weer vanaf dat adres schrijft, of als een e-mail naar dat adres wel wordt afgeleverd.

## Functie en foto

Bij mensen met een bedrijfsadres worden een functie, foto, LinkedIn-profiel en stad opgezocht, net als [organisatiegegevens](organization-data.md). Op een gehoste Machine worden alleen hun naam en bedrijfsdomein opgevraagd. Voor een foto krijgt Gravatar een hash van het werkadres, nooit het adres zelf. Je kunt dit uitzetten via **Instellingen**, onder Beveiliging: **Werkcontacten opzoeken**.

Als de gegevens zijn opgezocht, toont de pagina ook de beschrijving van die persoon, hoelang diegene de huidige functie al heeft en de twee functies daarvoor. De voorbereiding voor vergaderingen gebruikt deze gegevens ook. De beschrijving wordt alleen gebruikt als die persoon geen eigen biografie heeft.

Je Koppelingen vullen gegevens aan met wat ze al hebben gelezen: een functie, telefoonnummer en tijdzone uit Slack, een biografie en plaats uit X, een kopregel en foto uit LinkedIn, functietitels uit Google-contacten en Salesflare, en de foto van een contact uit Salesflare als Salesflare die zelf bewaart. Beweeg de muisaanwijzer over de regel onder de naam om te zien waar de informatie vandaan komt.

Outlook voegt foto's toe van collega's bij je organisatie en van je Outlook-contacten, plus de functietitels en bedrijven van je contacten ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Foto's uit WhatsApp en Telegram komen via je WhatsApp-synchronisatie en je Telegram-chatkoppeling: maximaal 50 per dag per app, alleen voor mensen die al in je Graph staan. Er wordt niets naar hen verstuurd. Bij een import van Facebook-verjaardagen wordt de profielfoto toegevoegd van iemand die nog geen foto heeft, als je de import opslaat ([Routines](routines.md)). Alles blijft op je Machine.

In de [Team Graph](team-graph.md) van een werk-Fleet wordt een kleine kopie van een werkfoto gedeeld met het gedeelde profiel van die persoon. Foto's uit Google-contacten, WhatsApp, Telegram of Facebook, en foto's die je hebt gewijzigd of verwijderd, worden nooit gedeeld.

## Over jou

Je eigen adressen en telefoonnummers, ook aliassen, zijn altijd van jou en nooit van iemand in je Graph. Als je jezelf zoekt of iemand toevoegt met een van je adressen, wordt **Over jou** geopend. Bij een import wordt je eigen rij overgeslagen.

Bij Over jou staan je adressen en de bron van elk adres. Je wijzigt ze via **Instellingen**, onder Account. Kies **Mijn contactgegevens delen** om je eigen contactgegevens met een teamgenoot of vriend te delen. Zie [Een contact delen](share-contact.md).

## Wat iemand voor je is

Rollen die je Machine in je berichten leest, staan op iemands pagina onder **Voor jou**, met de regel waarin de rol is gevonden. Je hoeft niets te bevestigen. Klopt er iets niet? Pas het aan via **Bewerken** op de pagina, of via **⋯** bij de regel onder **Recente wijzigingen**. Je Machine leert van je wijzigingen.

## Wat je Machine over iemand weet

Feiten over iemand staan op diens pagina onder **Bekend over**. Bij Leren staan de algemene feiten. Met **Toevoegen** voeg je een feit toe in je eigen woorden. Elk feit heeft een menu:

- Met **Bewerken** wijzig je het meteen.
- Met **Niet over deze persoon** maak je er weer een algemeen feit van, onder **Leren**, **Feiten**.
- Met **Verwijderen** verwijder je het overal.

## Recente wijzigingen

Onder **Recente wijzigingen**, ingeklapt net boven de tijdlijn van een persoon, organisatie of project, staan de dingen die je Machine over diegene heeft gewijzigd of geleerd: een rol, waar iemand werkt, hoe twee mensen aan elkaar verwant zijn, een feit of een projectwijziging. Elke regel toont de datum en de bron. Tik op de bron om het bericht te lezen.

Als een regel niet klopt, kun je die meteen aanpassen via **⋯**: **Bewerken**, **Verwijderen**, **Niet over deze persoon** of **Ongedaan maken** om een project terug te zetten naar de vorige plek. Je ziet drie regels. Met **Meer tonen** zie je de rest.

Bij iemand die je Machine vandaag heeft bijgewerkt, staat een klein puntje in de lijst Personen. Bovenaan de lijst staat **Vandaag 4 personen bijgewerkt**, met hun namen. Zie [The Graph](graph.md).

## Een to-do over iemand

Met **Nieuwe to-do** in het menu **⋯** van een persoon, organisatie of project maak je een to-do over diegene.
