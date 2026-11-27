---
title: Microsoft OneDrive
area: connections
summary: Reacties, vermeldingen en bijgehouden wijzigingen in je Word-bestanden in OneDrive. Nieuwe documenten en wijzigingen wachten op je akkoord.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: e931920c74158c98
---
## Wat het leest

**Microsoft OneDrive** leest je Word-bestanden in OneDrive, op een gehoste Machine en op je eigen computer. Outlook hoeft niet gekoppeld te zijn. Zie hieronder voor Google Docs. Het haalt het volgende binnen:

- Reacties en antwoorden op je Word-bestanden, en reacties waarin je wordt genoemd.
- Wijzigingen bijhouden in je Word-bestanden.

De eerste synchronisatie gaat 7 dagen terug. Elk item verwijst naar de mensen en projecten in je [Graph](graph.md). Een reactie waarvoor je iets moet doen, wordt een to-do.

## Bestanden die anderen met je delen

Microsoft stopt in november 2026 met het tonen van deze bestanden. Gedeelde bestanden en vermeldingen in bestanden van anderen komen dan alleen nog op je Machine terecht via e-mails van Microsoft. Koppel ook [Outlook](microsoft.md) en laat die e-mails binnenkomen. Een to-do uit zo'n e-mail opent de e-mail, en de knop erin opent het bestand. Een gedeeld bestand of een vermelding zonder e-mail wordt niet gezien.

## Wat het kan doen

Als een to-do tekst uit een document nodig heeft, leest je Machine dat document. Dat doet hij alleen zolang hij aan die to-do werkt. Hij kan Word-, PDF- en tekstbestanden lezen.

Hij zoekt ook naar bestanden van alle soorten in je eigen OneDrive en geeft je de link. Hij zoekt niet in SharePoint-sites of bestanden die met je gedeeld zijn. De tekst in een gescande PDF kan hij niet lezen.

Hij kan een antwoord op een reactie opstellen. Word kan van buitenaf geen antwoorden plaatsen, dus kopieer je het concept naar Word.

Hij accepteert nooit een suggestie, lost nooit een reactie op, deelt nooit een bestand en wijzigt nooit een document zonder je akkoord.

Als je hem alleen wilt gebruiken om dingen te doen, schakel je **Brengt signalen binnen** uit onder **Details**. Dan zoekt en leest hij alleen de bestanden die je to-do's nodig hebben, en maakt hij nieuwe bestanden.

## Documenten maken en bewerken

Je Machine kan een nieuw document maken of een document wijzigen waar een to-do over gaat:

- Een nieuw document maakt hij meteen als de to-do of een skill daarom vraagt. Het is privé en staat in je eigen OneDrive of Google Drive. De to-do toont **Open het document**. Delen of de link versturen wacht op je akkoord.
- Een wijziging aan een bestaand document bereidt hij alleen voor. Druk op **Wijzigingen nakijken** om elke alinea voor en na de wijziging te bekijken, en druk daarna op **Opslaan**. Een wijziging waar je in de chat van de to-do om vraagt, voert hij meteen door.
- Hij schrijft alleen in de versie van het document die jij hebt gezien. Heeft iemand het ondertussen gewijzigd, dan wordt er niets geschreven en meldt de to-do dat. Vraag om een nieuw concept.
- In Talk leest hij de volledige wijziging hardop voor en wacht hij op een duidelijk ja.
- Weigert Microsoft of Google een nieuw document te maken, dan vertelt de to-do waarom en toont hij **Nakijken en maken** om het opnieuw te proberen.

Hij kan tekst vervangen en tekst, alinea's en koppen toevoegen. In Google Docs kan hij ook opmaak toepassen: vet, cursief, onderstrepen, links, koppen, opsommingen en genummerde lijsten, en een pagina-einde. **Wijzigingen nakijken** toont elke wijziging. Hij kan geen tabellen maken. Afbeeldingen, bijgehouden wijzigingen en velden blijven zoals ze zijn.

Een document van een werk-to-do komt in het account van dat bedrijf terecht, nooit in een persoonlijk account. Op je eigen computer kan een Google-account dat voor Gmail is gekoppeld en toegang tot Drive heeft ook nieuwe Google Docs-bestanden maken. Past geen account, dan vertelt de to-do wat je voor Werk moet koppelen: Microsoft OneDrive, of Google Docs als je Machine dat kan gebruiken.

Als het document niet de laatste stap is, bijvoorbeeld een antwoord met de link ernaar, blijft de to-do open en stelt hij die stap op voor je akkoord.

Bewerken is inbegrepen wanneer je koppelt. Bij een oudere koppeling die alleen kan lezen, zie je **Bewerken toestaan** onder **Koppelingen**. Druk er één keer op en geef toestemming.

## Waar het om vraagt

Microsoft vraagt één keer om je akkoord om je bestanden te lezen en te wijzigen, ook bestanden die met je gedeeld zijn. Elke wijziging wacht nog steeds op je akkoord bij de bijbehorende to-do. De toegang tot je e-mail en agenda verandert niet.

Als je die toestemming later intrekt, toont Microsoft OneDrive **Wacht op je OK om documenten te lezen** onder **Koppelingen**.

## Koppelen

Op een gehoste Machine of op je eigen computer die aan je account is gekoppeld:

- Open **Koppelingen**, daarna **Documenten en bestanden**, en kies **Microsoft OneDrive**.
- Druk op **Inloggen met Microsoft** en geef toestemming om je bestanden te lezen en te bewerken.

Als Microsoft lezen niet toestaat, wordt de koppeling niet toegevoegd. Druk je op **Bewerken toestaan** en staat Microsoft bewerken niet toe, dan meldt hij dat.

## Google Docs

Open op een gehoste Machine **Koppelingen**, daarna **Documenten en bestanden**, en kies **Google Docs**. Google vraagt toestemming om de documenten die je aanwijst te bekijken en te bewerken, en nieuwe documenten te maken. Gmail hoeft niet gekoppeld te zijn en je Gmail-toegang verandert niet.

Je Machine doet daarna het volgende:

- Hij leest een Google-document waarnaar wordt gelinkt in berichten van een to-do, of dat in de chat is geplakt, alleen zolang hij aan die to-do werkt.
- Hij bereidt wijzigingen aan dat document voor. Elke wijziging wacht op je akkoord, zoals hierboven beschreven.
- Hij maakt nieuwe privé-documenten in je Google Drive.

Zijn er meerdere Google Docs-koppelingen beschikbaar bij een to-do, dan leest en wijzigt hij een bestand via een koppeling waarmee hij het kan openen en wijzigen.

Hij zoekt niet in je Drive. Hij ziet reacties, gedeelde bestanden en suggesties alleen in documenten die hij zelf heeft gemaakt. Voor meer toegang zou hij je hele Drive moeten kunnen bekijken, maar daar vraagt hij niet om.

## Google Sheets en Slides

Toont Google Docs onder **Koppelingen** de optie **Toegang geven tot Sheets en Slides**, druk daar dan op en geef voor beide toestemming. Google vraagt toestemming om je Machine toegang te geven tot je Sheets- en Slides-bestanden. Hij kan die niet wijzigen.

Je Machine leest daarna ook een Google Sheets- of Slides-bestand waarnaar wordt gelinkt in berichten van een to-do, of dat in de chat is geplakt, alleen zolang hij aan die to-do werkt:

- Uit een spreadsheet leest hij eerst het gekoppelde tabblad of de gekoppelde cellen, en daarna de andere tabbladen, tot maximaal 2.000 cellen. Een formule wordt als de bijbehorende waarde getoond. Verborgen tabbladen leest hij alleen als ernaar wordt gelinkt of als erom wordt gevraagd.
- Uit presentaties leest hij de tekst en sprekersnotities, in volgorde. Afbeeldingen en grafieken leest hij niet.

### Sheets en Slides bewerken

Zodra je Machine de bestanden kan lezen, kan Google Docs ook **Bewerkingen in Sheets en Slides toestaan** tonen. Druk erop en geef voor beide toestemming. Je Machine kan dan een Sheet- of Slides-bestand wijzigen waarnaar wordt gelinkt in een to-do of dat in de chat is geplakt. Dat werkt hetzelfde als bij een document: hij bereidt de wijziging alleen voor, **Wijzigingen nakijken** toont de wijziging en er wordt niets opgeslagen voordat je op **Opslaan** drukt.

- In een spreadsheet: nieuwe celwaarden op een tabblad, rijen onder de laatste rij of een nieuw tabblad. Voor elke cel zie je de oude en nieuwe waarde. Waarden worden als tekst ingevoerd. Een formule wordt alleen als formule ingevoerd als de to-do dat aangeeft.
- In presentaties: tekst op één dia vervangen, met de oude en nieuwe tekst, of een nieuwe dia met een titel en tekst.
- Hij schrijft alleen in de versie van het bestand die jij hebt gezien. Heeft iemand de cellen of dia's ondertussen gewijzigd, dan wordt er niets geschreven en meldt de to-do dat.

Opmaak, grafieken, afbeeldingen en Excel- of PowerPoint-bestanden blijven zoals ze zijn.

Vraag in de chat naar het tabblad, de cellen of de dia's die je bedoelt als het om een groot bestand gaat. Is een bestand privé voor iemand anders, verwijderd of een Excel- of PowerPoint-bestand, dan meldt de to-do dat. Een Google Drive-link werkt hetzelfde als die naar een Google-document, Sheet- of Slides-bestand verwijst.

## Google Docs op je eigen computer

Op je eigen computer kan je Machine een nieuw Google-document maken in een Gmail-account dat daar is ingelogd en al toegang tot Drive heeft. Hij leest je andere Google-documenten of de reacties daarop niet. Onder **Documenten en bestanden** wordt het weergegeven als Google Docs, bij dat account. Hij kan ook een document wijzigen dat hij daar voor een to-do heeft gemaakt.

Hij leest ook een Google Sheets- of Slides-bestand waarnaar wordt gelinkt in een to-do of dat in de chat is geplakt, als die Google-login al toegang heeft tot Drive, Sheets of Slides. Hij vraagt Google nooit om meer toegang en wijzigt die bestanden daar niet. Zegt Google nee, schakel dan de Google Sheets- of Slides-API in bij het eigen Google-project van die login.

## Werk of persoonlijk

Hij volgt het label Werk of Persoonlijk van de koppeling, net als bij e-mail. Werkdocumenten kunnen volgens je [deelregels](sharing-rules.md) terechtkomen in de Graph van je team. Persoonlijke documenten komen daar nooit terecht.

## Ontkoppelen

Open **Koppelingen**, kies Microsoft OneDrive of Google Docs, daarna **Details** en **Ontkoppelen**. Hij stopt met lezen. Wat hij al heeft binnengehaald, blijft staan. Op een gehoste Machine opent **Ontkoppelen ↗** je installatiepagina, waar de login staat.
