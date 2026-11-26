---
title: Microsoft OneDrive
area: connections
summary: Opmerkingen, vermeldingen en bijgehouden wijzigingen in je Word-bestanden in OneDrive. Nieuwe documenten en wijzigingen wachten op je OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 057429e4c3b6408c
---
## Wat het leest

**Microsoft OneDrive** leest je Word-bestanden in OneDrive, op een gehoste Machine en op je eigen computer. Outlook hoeft niet gekoppeld te zijn. Zie hieronder voor Google Docs. Het brengt het volgende binnen:

- Opmerkingen en reacties op je Word-bestanden, en opmerkingen waarin iemand je vermeldt.
- Bijgehouden wijzigingen in je Word-bestanden.

De eerste synchronisatie haalt gegevens op van de afgelopen 7 dagen. Elk item wordt gekoppeld aan de personen en projecten in je [Graph](graph.md). Een opmerking die actie van je vraagt, wordt een to-do.

## Bestanden die anderen met je delen

Microsoft vermeldt deze bestanden vanaf november 2026 niet meer. Gedeelde bestanden en vermeldingen in bestanden van anderen komen dan alleen via e-mails van Microsoft bij je Machine binnen. Koppel ook [Outlook](microsoft.md) en laat die e-mails staan. Een to-do uit zo'n e-mail opent de e-mail. Met de knop daarin open je het bestand. Een gedeeld bestand of vermelding zonder e-mail wordt niet gezien.

## Wat het kan

Als een to-do de tekst uit een document nodig heeft, leest je Machine dat document terwijl hij aan die to-do werkt. Hij kan Word-, PDF- en tekstbestanden lezen.

Je Machine zoekt ook naar allerlei soorten bestanden in je eigen OneDrive en geeft je de link. Hij zoekt niet in SharePoint-sites of in bestanden die met je zijn gedeeld. Hij kan de tekst in een gescande PDF niet lezen.

Je Machine kan een reactie op een opmerking opstellen. Word kan geen reacties van buitenaf plaatsen, dus kopieer je het concept naar Word.

Je Machine accepteert nooit een suggestie, lost nooit een opmerking op, deelt nooit een bestand en wijzigt nooit een document zonder je OK.

Wil je hem alleen gebruiken om dingen uit te voeren, schakel dan **Brengt signalen binnen** uit onder **Details**. Je Machine zoekt en leest dan alleen de bestanden die je to-do's nodig hebben en maakt nieuwe bestanden.

## Documenten maken en bewerken

Je Machine kan een nieuw document maken of een document aanpassen waar een to-do over gaat:

- Een nieuw document maakt hij meteen als de to-do of een skill daarom vraagt. Het document is privé en staat in je eigen OneDrive of Google Drive. In de to-do staat **Open het document**. Delen of de link versturen wacht op je OK.
- Een wijziging in een bestaand document bereidt hij alleen voor. Kies **Wijzigingen nakijken** om elke alinea voor en na de wijziging te bekijken. Kies daarna **Opslaan**. Een wijziging waar je om vraagt in de chat van de to-do voert hij meteen uit.
- Hij schrijft alleen in het document zoals jij het hebt bekeken. Als iemand het ondertussen heeft gewijzigd, schrijft hij niets en meldt de to-do dat. Vraag om een nieuw concept.
- In Talk leest hij de hele wijziging hardop voor en wacht hij op een duidelijk ja.
- Als Microsoft of Google een nieuw document weigert, legt de to-do uit waarom en toont hij **Nakijken en maken**, zodat je het opnieuw kunt proberen.

Je Machine kan tekst vervangen en tekst, alinea's en koppen toevoegen. In Google Docs kan hij ook opmaak toepassen: vet, cursief, onderstrepen, links, koppen, opsommingstekens en genummerde lijsten, en een pagina-einde. **Wijzigingen nakijken** toont elke wijziging. Tabellen maken kan hij niet. Afbeeldingen, bijgehouden wijzigingen en velden blijven zoals ze zijn.

Een document bij een Werk-to-do komt in het account van dat bedrijf terecht, nooit in een persoonlijk account. Op je eigen computer kan een Google-account dat voor Gmail is gekoppeld en toegang tot Drive heeft, ook nieuwe Google Docs maken. Als geen account geschikt is, vertelt de to-do wat je voor Werk moet koppelen: Microsoft OneDrive, of Google Docs als je Machine dat kan gebruiken.

Als het document niet de laatste stap is, bijvoorbeeld een reactie met de link, blijft de to-do open en maakt je Machine een concept van die stap, dat op je OK wacht.

Bewerken is inbegrepen wanneer je koppelt. Bij een oudere koppeling die alleen lezen toestaat, staat **Bewerken toestaan** in **Koppelingen**. Kies dit één keer en geef toestemming.

## Waar het om vraagt

Microsoft vraagt één keer om je OK om je bestanden te lezen en te wijzigen, ook bestanden die met je zijn gedeeld. Elke wijziging wacht nog steeds op je OK in de bijbehorende to-do. De toegang tot je e-mail en agenda verandert niet.

Als je die toestemming later intrekt, toont Microsoft OneDrive **Wacht op je OK om documenten te lezen** in **Koppelingen**.

## Koppelen

Op een gehoste Machine of op je eigen computer die aan je account is gekoppeld:

- Open **Koppelingen**, kies **Documenten en bestanden** en selecteer **Microsoft OneDrive**.
- Kies **Inloggen met Microsoft** en geef toestemming om je bestanden te lezen en te bewerken.

Als Microsoft lezen niet toestaat, wordt de koppeling niet toegevoegd. Als je **Bewerken toestaan** kiest en Microsoft bewerken niet toestaat, meldt Microsoft dat.

## Google Docs

Open op een gehoste Machine **Koppelingen**, kies **Documenten en bestanden** en selecteer **Google Docs**. Google vraagt toestemming om de documenten te bekijken die je opgeeft, ze te bewerken en nieuwe documenten te maken. Gmail hoeft niet gekoppeld te zijn en je Gmail-toegang verandert niet.

Je Machine doet daarna het volgende:

- Hij leest een Google-document waarnaar wordt gelinkt in berichten van een to-do of dat in de chat ervan is geplakt, alleen terwijl hij aan die to-do werkt.
- Hij bereidt wijzigingen in dat document voor. Elke wijziging wacht op je OK, zoals hierboven beschreven.
- Hij maakt nieuwe privédocumenten in je Google Drive.

Hij doorzoekt je Drive niet. Hij ziet opmerkingen, gedeelde bestanden en suggesties alleen in documenten die hij zelf heeft gemaakt. Daarvoor zou hij toegang tot je hele Drive nodig hebben, en daar vraagt hij niet om.

## Google Sheets en Slides

Als bij Google Docs onder **Koppelingen** **Toegang geven tot Sheets en Slides** staat, kies je dit en geef je voor beide toestemming. Google vraagt toestemming zodat je Machine je Sheets- en Slides-bestanden kan bekijken. Hij kan ze niet wijzigen.

Je Machine leest daarna ook een Google Sheet- of Slides-bestand waarnaar wordt gelinkt in berichten van een to-do of dat in de chat ervan is geplakt, alleen terwijl hij aan die to-do werkt:

- In een spreadsheet leest hij eerst het gekoppelde tabblad of de gekoppelde cellen en daarna de andere tabbladen, tot maximaal 2.000 cellen. Een formule wordt als waarde weergegeven. Verborgen tabbladen leest hij alleen als ernaar wordt gelinkt of als erom wordt gevraagd.
- In presentaties leest hij de tekst en sprekersnotities op volgorde. Afbeeldingen en grafieken worden niet gelezen.

### Sheets en Slides bewerken

Zodra je Machine deze bestanden kan lezen, kan bij Google Docs ook **Bewerkingen in Sheets en Slides toestaan** staan. Kies dit en geef voor beide toestemming. Je Machine kan dan een gekoppeld Sheet- of Slides-bestand op dezelfde manier wijzigen als een document: hij bereidt de wijziging alleen voor, **Wijzigingen nakijken** toont de wijziging en er wordt niets opgeslagen voordat je **Opslaan** kiest.

- In een spreadsheet kan hij nieuwe celwaarden toevoegen aan een tabblad, rijen onder de laatste rij toevoegen of een nieuw tabblad maken. Voor elke cel worden de oude en nieuwe waarde getoond. Waarden worden als tekst toegevoegd. Een formule wordt alleen als formule toegevoegd als de to-do daarom vraagt.
- In presentaties kan hij tekst op één dia vervangen, met de oude en nieuwe tekst erbij, of een nieuwe dia met een titel en tekst maken.
- Hij schrijft alleen in het bestand zoals jij het hebt bekeken. Als iemand de cellen of dia's ondertussen heeft gewijzigd, schrijft hij niets en meldt de to-do dat.

Opmaak, grafieken, afbeeldingen en Excel- of PowerPoint-bestanden blijven zoals ze zijn.

Vraag bij grote bestanden in de chat om het tabblad, de cellen of de dia's die je bedoelt. Als een bestand privé is voor iemand anders, is verwijderd of een Excel- of PowerPoint-bestand is, meldt de to-do dat. Een Google Drive-link werkt op dezelfde manier als het om een Google Doc, Sheet of Slides-bestand gaat.

## Google Docs op je eigen computer

Op je eigen computer kan je Machine een nieuw Google-document maken in een Gmail-account dat daar is ingelogd en al toegang tot Drive heeft. Hij leest je andere Google-documenten of de opmerkingen daarin niet. Onder **Documenten en bestanden** staat Google Docs bij dat account. Je Machine kan daar ook een document wijzigen dat hij voor een to-do heeft gemaakt.

Hij leest ook een Google Sheet- of Slides-bestand waarnaar wordt gelinkt in een to-do of dat in de chat ervan is geplakt, als die Google-login al toegang heeft tot Drive, Sheets of Slides. Hij vraagt Google nooit om meer toegang en wijzigt die bestanden daar niet. Als Google dit niet toestaat, schakel je de Google Sheets- of Slides-API in bij het eigen Google-project van die login.

## Werk of persoonlijk

Je Machine volgt het label Werk of Persoonlijk van de koppeling, net als bij e-mail. Werkdocumenten kunnen volgens je [deelregels](sharing-rules.md) in de Graph van je team terechtkomen. Persoonlijke documenten komen daar nooit terecht.

## De koppeling verwijderen

Open **Koppelingen**, kies Microsoft OneDrive of Google Docs, daarna **Details** en **Ontkoppelen**. Je Machine stopt met lezen. Wat hij al heeft binnengehaald, blijft staan. Op een gehoste Machine opent **Ontkoppelen ↗** je installatiepagina, waar de login staat.
