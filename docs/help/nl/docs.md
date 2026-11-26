---
title: Microsoft OneDrive
area: connections
summary: Reacties, vermeldingen en bijgehouden wijzigingen in je Word-bestanden in OneDrive. Nieuwe documenten en wijzigingen wachten op je OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: c8fca3cf0299e327
---
## Wat hij leest

**Microsoft OneDrive** leest je Word-bestanden in OneDrive, op een gehoste Machine en op je eigen computer. Outlook hoeft niet gekoppeld te zijn. Zie hieronder voor Google Docs. Hij haalt het volgende binnen:

- Reacties en antwoorden op je Word-bestanden, en reacties waarin je wordt genoemd.
- Bijgehouden wijzigingen in je Word-bestanden.

De eerste synchronisatie gaat 7 dagen terug. Elk item is gekoppeld aan de mensen en projecten in je [Graph](graph.md). Een reactie waarvoor jij iets moet doen, wordt een to-do.

## Bestanden die anderen met je delen

Microsoft laat deze bestanden vanaf november 2026 niet meer zien. Gedeelde bestanden en vermeldingen in bestanden van anderen komen dan alleen nog via e-mails van Microsoft op je Machine binnen. Koppel ook [Outlook](microsoft.md) en laat die e-mails aan staan. Een to-do uit zo'n e-mail opent de e-mail en de knop daarin opent het bestand. Een gedeeld bestand of een vermelding zonder e-mail wordt niet gezien.

## Wat hij kan doen

Als een to-do de tekst van een document nodig heeft, leest je Machine dat document alleen terwijl hij aan die to-do werkt. Hij kan Word-, PDF- en tekstbestanden lezen.

Hij zoekt ook naar bestanden van elk type in je eigen OneDrive en geeft je de link. Hij doorzoekt geen SharePoint-sites of bestanden die met je zijn gedeeld. Hij kan de tekst van een gescande PDF niet lezen.

Hij kan een antwoord op een reactie opstellen. Word kan geen antwoorden van buitenaf plaatsen, dus kopieer je het concept naar Word.

Hij accepteert nooit een suggestie, lost geen reactie op, deelt geen bestand en wijzigt geen document zonder je OK.

Wil je hem alleen dingen laten doen, zet dan **Brengt signalen binnen** uit onder **Details**. Hij zoekt en leest dan alleen de bestanden die je to-do's nodig hebben en maakt nieuwe bestanden.

## Documenten maken en bewerken

Je Machine kan een nieuw document maken of een document wijzigen waar een to-do over gaat:

- Een nieuw document maakt hij meteen als de to-do of een skill daarom vraagt. Het is privé en staat in je eigen OneDrive of Google Drive. In de to-do staat **Open het document**. Delen of de link versturen wacht op je OK.
- Een wijziging in een bestaand document bereidt hij alleen voor. Druk op **Wijzigingen nakijken** om elke alinea voor en na de wijziging te zien, en druk daarna op **Opslaan**. Een wijziging waar je om vraagt in de chat van de to-do, voert hij meteen door.
- Hij schrijft alleen in het document zoals jij het hebt gezien. Als iemand het ondertussen heeft gewijzigd, wordt er niets opgeslagen en meldt de to-do dat. Vraag om een nieuw concept.
- In Talk leest hij de hele wijziging hardop voor en wacht hij op een duidelijk ja.
- Als Microsoft of Google weigert een nieuw document te maken, legt de to-do uit waarom en verschijnt **Nakijken en maken**, zodat je het opnieuw kunt proberen.

Hij kan tekst vervangen en tekst, alinea's en koppen toevoegen. In Google Docs kan hij ook tekst opmaken: vet, cursief, onderstrepen, links, koppen, opsommingen en genummerde lijsten, en een pagina-einde. **Wijzigingen nakijken** toont elke wijziging. Hij kan geen tabellen maken. Afbeeldingen, bijgehouden wijzigingen en velden blijven zoals ze zijn.

Een document van een Work-to-do komt in het account van dat bedrijf, nooit in een persoonlijk account. Op je eigen computer kan een Google-account dat voor Gmail is gekoppeld en Drive-toegang heeft ook nieuwe Google Docs maken. Past geen account, dan vertelt de to-do wat je voor Work moet koppelen: Microsoft OneDrive, of Google Docs als je Machine dat kan gebruiken.

Als het document niet de laatste stap is, bijvoorbeeld een antwoord met de link ernaar, blijft de to-do open en stelt hij die stap op voor je OK.

Bewerken is inbegrepen bij het koppelen. Bij een oudere koppeling waarmee je alleen kunt lezen, staat **Bewerken toestaan** onder **Koppelingen**. Druk er één keer op en accepteer.

## Waar hij om vraagt

Microsoft vraagt één keer om je OK om je bestanden te lezen en te wijzigen, ook bestanden die met je zijn gedeeld. Elke wijziging wacht nog steeds op je OK bij de to-do. Je toegang tot e-mail en agenda verandert niet.

Als je die OK later intrekt, staat er bij Microsoft OneDrive onder **Koppelingen**: **Wacht op je OK om documenten te lezen**.

## Koppelen

Op een gehoste Machine of op je eigen computer, gekoppeld aan je account:

- Open **Koppelingen**, daarna **Documenten en bestanden**, en kies **Microsoft OneDrive**.
- Druk op **Inloggen met Microsoft** en geef toestemming om je bestanden te lezen en te bewerken.

Als Microsoft lezen niet toestaat, wordt de koppeling niet toegevoegd. Als je op **Bewerken toestaan** drukt en Microsoft bewerken niet toestaat, meldt hij dat.

## Google Docs

Open op een gehoste Machine **Koppelingen**, daarna **Documenten en bestanden**, en kies **Google Docs**. Google vraagt toestemming om de documenten te bekijken die je aanwijst, ze te bewerken en nieuwe documenten te maken. Gmail hoeft niet gekoppeld te zijn en je toegang tot Gmail verandert niet.

Je Machine doet dan het volgende:

- Hij leest een Google Doc waarnaar in berichten van een to-do wordt gelinkt of die in de chat ervan is geplakt, alleen terwijl hij aan die to-do werkt.
- Hij bereidt wijzigingen in dat document voor. Elke wijziging wacht op je OK, zoals hierboven beschreven.
- Hij maakt nieuwe privédocumenten in je Google Drive.

Hij doorzoekt je Drive niet. Hij ziet reacties, gedeelde bestanden en suggesties alleen in documenten die hij zelf heeft gemaakt. Voor meer toegang zou hij toegang tot je hele Drive nodig hebben, en daar vraagt hij niet om.

## Google Sheets en Slides

Staat bij Google Docs onder **Koppelingen** **Toegang geven tot Sheets en Slides**, druk daar dan op en geef toestemming voor beide. Google vraagt toestemming om je Machine je Sheets- en Slides-bestanden te laten bekijken. Hij kan ze niet wijzigen.

Je Machine leest dan ook een Google Sheet- of Slides-bestand waarnaar in berichten van een to-do wordt gelinkt of dat in de chat ervan is geplakt, alleen terwijl hij aan die to-do werkt:

- Uit een sheet leest hij eerst het gelinkte tabblad of de gelinkte cellen, daarna de andere tabbladen, tot maximaal 2.000 cellen. Een formule wordt getoond als de waarde ervan. Verborgen tabbladen leest hij alleen als ernaar wordt gelinkt of als erom wordt gevraagd.
- Uit slides leest hij de tekst en sprekersnotities, in de juiste volgorde. Afbeeldingen en grafieken worden niet gelezen.

Vraag bij een groot bestand in de chat naar het tabblad, de cellen of de slides die je bedoelt. Als een bestand privé is voor iemand anders, verwijderd is of een Excel- of PowerPoint-bestand is, meldt de to-do dat. Een Google Drive-link werkt op dezelfde manier als die naar een Google Docs-, Sheets- of Slides-bestand verwijst.

## Google Docs op je eigen computer

Op je eigen computer kan je Machine een nieuw Google Doc maken in een Gmail-account dat daar is ingelogd en al toegang tot Drive heeft. Hij leest je andere Google Docs of de reacties daarop niet. Onder **Documenten en bestanden** staat het als Google Docs, bij dat account. Hij kan daar ook een document wijzigen dat hij voor een to-do heeft gemaakt.

Hij leest ook een Google Sheet- of Slides-bestand waarnaar in een to-do wordt gelinkt of dat in de chat ervan is geplakt, als die Google-login al toegang heeft tot Drive, Sheets of Slides. Hij vraagt Google nooit om meer toegang. Als Google weigert, schakel je de Google Sheets- of Slides-API in bij het eigen Google-project van die login.

## Werk of privé

Hij volgt het label Werk of Persoonlijk van de koppeling, net als bij e-mail. Werkdocumenten kunnen volgens je [deelregels](sharing-rules.md) in de Graph van je team terechtkomen. Privédocumenten nooit.

## Verwijderen

Open **Koppelingen**, daarna Microsoft OneDrive of Google Docs, **Details** en **Ontkoppelen**. Hij stopt met lezen. Wat hij al heeft binnengehaald, blijft staan. Op een gehoste Machine opent **Ontkoppelen ↗** je installatiepagina, waar de login staat.
