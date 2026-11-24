---
title: Microsoft OneDrive
area: connections
summary: Opmerkingen, vermeldingen en bijgehouden wijzigingen in je Word-bestanden in OneDrive. Nieuwe documenten en wijzigingen wachten op je OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: d79388a1c8811d5f
---
## Wat hij leest

**Microsoft OneDrive** leest je Word-bestanden in OneDrive, op een gehoste Machine en op je eigen computer. Outlook hoeft niet gekoppeld te zijn. Zie hieronder voor Google Docs. Hij haalt het volgende binnen:

- Opmerkingen en antwoorden op je Word-bestanden, en opmerkingen waarin iemand je vermeldt.
- Bijgehouden wijzigingen in je Word-bestanden.

De eerste synchronisatie gaat 7 dagen terug. Elk item is gekoppeld aan de mensen en projecten in je [Graph](graph.md). Een opmerking waarvoor je iets moet doen, wordt een to-do.

## Bestanden die anderen met je delen

Microsoft vermeldt deze bestanden vanaf november 2026 niet meer. Gedeelde bestanden en vermeldingen in bestanden van anderen komen dan alleen nog via e-mails van Microsoft op je Machine terecht. Koppel ook [Outlook](microsoft.md) en laat die e-mails binnenkomen. Een to-do die uit zo'n e-mail komt, opent de e-mail en de knop daarin opent het bestand. Een gedeeld bestand of een vermelding zonder e-mail wordt niet gezien.

## Wat hij kan doen

Als een to-do de tekst van een document nodig heeft, leest je Machine dat document. Alleen terwijl hij aan die to-do werkt. Hij kan Word-, PDF- en tekstbestanden lezen.

Hij zoekt ook naar bestanden van elk type in je eigen OneDrive en geeft je de link. Hij zoekt niet in SharePoint-sites of bestanden die met je zijn gedeeld. De tekst van een gescande PDF kan hij niet lezen.

Hij kan een antwoord op een opmerking opstellen. Word kan geen antwoorden van buitenaf plaatsen, dus kopieer je het concept naar Word.

Hij accepteert nooit een suggestie, lost nooit een opmerking op, deelt nooit een bestand en wijzigt nooit een document zonder je OK.

Wil je hem alleen gebruiken om dingen te doen, schakel dan **Brengt signalen binnen** uit onder **Details**. Hij zoekt dan alleen naar bestanden die je to-do's nodig hebben, leest ze en maakt nieuwe bestanden.

## Documenten maken en bewerken

Je Machine kan een nieuw document schrijven of een document wijzigen waar een to-do over gaat:

- Een nieuw document maakt hij meteen als de to-do of een skill daarom vraagt. Het is privé en staat in je eigen OneDrive of Google Drive. De to-do toont **Open het document**. Het delen van het document of versturen van de link wacht op je OK.
- Een wijziging aan een bestaand document bereidt hij alleen voor. Druk op **Wijzigingen nakijken** om elke alinea vóór en na de wijziging te zien en druk daarna op **Opslaan**. Een wijziging waar je in de chat van de to-do om vraagt, voert hij meteen uit.
- Hij schrijft alleen in het document zoals jij het hebt gezien. Heeft iemand het ondertussen gewijzigd, dan schrijft hij niets en laat de to-do dat weten. Vraag om een nieuw concept.
- In Talk leest hij de hele wijziging hardop voor en wacht hij op een duidelijk ja.
- Weigert Microsoft of Google een nieuw document te maken, dan legt de to-do uit waarom en toont hij **Nakijken en maken** om het opnieuw te proberen.

Hij kan tekst vervangen en tekst, alinea's en koppen toevoegen. Tabellen, afbeeldingen, bijgehouden wijzigingen en velden blijven zoals ze zijn.

Een document van een Werk-to-do komt in het account van dat bedrijf terecht, nooit in een persoonlijk account. Op je eigen computer kan een Google-account dat voor Gmail is gekoppeld en toegang tot Drive heeft ook nieuwe Google Docs maken. Past er geen account bij, dan vertelt de to-do wat je voor Werk moet koppelen: Microsoft OneDrive of Google Docs, als je Machine dat kan gebruiken.

Als het document niet de laatste stap is, bijvoorbeeld een antwoord met de link ernaartoe, blijft de to-do open en maakt hij een concept van die stap dat op je OK wacht.

Bewerken is inbegrepen bij het koppelen. Bij een oudere koppeling waarmee alleen lezen mogelijk is, staat **Bewerken toestaan** onder **Koppelingen**. Druk er één keer op en accepteer.

## Waar hij om vraagt

Microsoft vraagt één keer om je OK om je bestanden te lezen en te wijzigen, ook bestanden die met je zijn gedeeld. Elke wijziging wacht nog steeds op je OK bij de bijbehorende to-do. Je toegang tot mail en agenda verandert niet.

Als je die OK later intrekt, toont Microsoft OneDrive **Wacht op je OK om documenten te lezen** onder **Koppelingen**.

## Koppelen

Op een gehoste Machine of op je eigen computer die aan je account is gekoppeld:

- Open **Koppelingen**, daarna **Documenten en bestanden**, en kies **Microsoft OneDrive**.
- Druk op **Inloggen met Microsoft** en geef toestemming om je bestanden te lezen en te bewerken.

Als Microsoft lezen niet toestaat, wordt de koppeling niet toegevoegd. Als je op **Bewerken toestaan** drukt en Microsoft bewerken niet toestaat, laat hij dat weten.

## Google Docs

Open op een gehoste Machine **Koppelingen**, daarna **Documenten en bestanden**, en kies **Google Docs**. Google vraagt je toestemming om de documenten waarnaar je verwijst te bekijken en te bewerken, en om nieuwe documenten te maken. Gmail hoeft niet gekoppeld te zijn en je Gmail-toegang verandert niet.

Je Machine:

- Leest een Google-document waarnaar in de berichten van een to-do wordt gelinkt of dat in de chat ervan is geplakt, alleen terwijl hij aan die to-do werkt.
- Bereidt wijzigingen aan dat document voor. Elke wijziging wacht op je OK, zoals hierboven beschreven.
- Maakt nieuwe privédocumenten in je Google Drive.

Hij zoekt niet in je Drive. Hij ziet opmerkingen, gedeelde documenten en suggesties alleen in documenten die hij zelf heeft gemaakt. Voor meer toegang zou hij toegang tot je hele Drive nodig hebben, maar daar vraagt hij niet om.

## Google Sheets en Slides

Staat bij Google Docs onder **Koppelingen** de optie **Toegang geven tot Sheets en Slides**, druk er dan op en geef toestemming voor beide. Google vraagt toestemming om je Machine toegang te geven tot je Sheets- en Slides-bestanden. Hij kan die niet wijzigen.

Je Machine leest dan ook een Google Sheet- of Slides-bestand waarnaar in de berichten van een to-do wordt gelinkt of dat in de chat ervan is geplakt, maar alleen terwijl hij aan die to-do werkt:

- Uit een spreadsheet leest hij eerst het gekoppelde tabblad of de gekoppelde cellen en daarna de andere tabbladen, tot maximaal 2.000 cellen. Een formule wordt als de waarde ervan weergegeven. Verborgen tabbladen leest hij alleen als ernaar wordt gelinkt of om wordt gevraagd.
- Uit presentaties leest hij de tekst en sprekersnotities, in volgorde. Afbeeldingen en grafieken leest hij niet.

Vraag bij een groot bestand in de chat om het tabblad, de cellen of de dia's die je bedoelt. Als een bestand privé is voor iemand anders, verwijderd is of een Excel- of PowerPoint-bestand is, laat de to-do dat weten. Een Google Drive-link werkt op dezelfde manier als het om een Google Docs-, Sheets- of Slides-bestand gaat.

## Google Docs op je eigen computer

Op je eigen computer kan je Machine een nieuw Google-document maken in een Gmail-account dat daar is ingelogd en al toegang tot Drive heeft. Hij leest je andere Google-documenten en de opmerkingen daarin niet. Onder **Documenten en bestanden** staat Google Docs bij dat account. Hij kan daar ook een document wijzigen dat hij voor een to-do heeft gemaakt.

Hij leest ook een Google Sheet- of Slides-bestand waarnaar in een to-do wordt gelinkt of dat in de chat ervan is geplakt, als die Google-login al toegang heeft tot Drive, Sheets of Slides. Hij vraagt Google nooit om meer toegang. Als Google dat weigert, schakel je de Google Sheets- of Slides-API in binnen het eigen Google-project van die login.

## Werk of persoonlijk

Net als bij mail volgt hij het label Werk of Persoonlijk van de koppeling. Werkdocumenten kunnen volgens je [deelregels](sharing-rules.md) in de Graph van je team terechtkomen. Persoonlijke documenten nooit.

## Ontkoppelen

Open **Koppelingen**, daarna Microsoft OneDrive of Google Docs, **Details** en **Ontkoppelen**. Hij stopt met lezen. Wat hij al heeft binnengehaald, blijft staan. Op een gehoste Machine opent **Ontkoppelen ↗** je installatiepagina, waar de login staat.
