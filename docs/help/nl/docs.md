---
title: Microsoft OneDrive
area: connections
summary: Opmerkingen, vermeldingen, bijgehouden wijzigingen en gedeelde Word-bestanden in OneDrive en SharePoint. Nieuwe documenten en wijzigingen wachten op je OK.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: b06d8ca4f35e5a38
---
## Wat hij leest

**Microsoft OneDrive** leest je Word-bestanden in OneDrive en SharePoint, op een gehoste Machine en op je eigen computer. Outlook hoeft niet gekoppeld te zijn. Zie hieronder voor Google Docs. Hij haalt binnen:

- Documenten die iemand met je deelt.
- Opmerkingen en antwoorden op je documenten, en opmerkingen waarin je wordt vermeld.
- Bijgehouden wijzigingen in je Word-bestanden.

De eerste synchronisatie gaat 7 dagen terug. Elk item is gekoppeld aan de mensen en projecten in je [Graph](graph.md). Een opmerking waarvoor jij aan zet bent, wordt een to-do.

## Wat hij kan doen

Als een to-do de tekst van een document nodig heeft, leest je Machine dat document alleen terwijl hij aan die to-do werkt.

Hij kan een antwoord op een opmerking opstellen. Word kan van buitenaf geen antwoorden plaatsen, dus kopieer het concept naar Word.

Hij accepteert nooit een suggestie, lost nooit een opmerking op, deelt nooit een bestand en wijzigt nooit een document zonder je OK.

Wil je hem alleen gebruiken om dingen te doen, schakel dan **Brengt signalen binnen** uit onder **Details**. Dan zoekt en leest hij alleen de documenten die je to-do's nodig hebben en maakt hij nieuwe documenten.

## Documenten maken en bewerken

Je Machine kan een nieuw document schrijven of een document wijzigen waar een to-do over gaat:

- Een nieuw document maakt hij meteen als de to-do of een skill daarom vraagt. Het is privé en staat in je eigen OneDrive of Google Drive. De to-do toont **Open het document**. Delen of de link versturen wacht op je OK.
- Een wijziging aan een bestaand document bereidt hij alleen voor. Druk op **Wijzigingen nakijken** om elke alinea voor en na te bekijken en druk daarna op **Opslaan**. Een wijziging waar je in de chat van de to-do om vraagt, voert hij meteen door.
- Hij schrijft alleen in het document zoals jij het hebt gezien. Heeft iemand het ondertussen gewijzigd, dan wordt er niets geschreven en laat de to-do dat weten. Vraag om een nieuw concept.
- In Talk leest hij de hele wijziging hardop voor en wacht hij op een duidelijk ja.
- Weigert Microsoft of Google een nieuw document te maken, dan legt de to-do uit waarom en toont hij **Nakijken en maken** om het opnieuw te proberen.

Hij kan tekst vervangen en tekst, alinea's en koppen toevoegen. Tabellen, afbeeldingen, bijgehouden wijzigingen en velden blijven zoals ze zijn.

Het document van een Werk-to-do komt in het account van dat bedrijf, nooit in een persoonlijk account. Op je eigen computer kan een Google-account dat voor Gmail is gekoppeld en toegang tot Drive heeft ook nieuwe Google Docs maken. Past geen account, dan vertelt de to-do wat je voor Werk moet koppelen: Microsoft OneDrive of Google Docs, als je Machine dat kan gebruiken.

Als het document niet de laatste stap is, bijvoorbeeld een antwoord met de link, blijft de to-do open en stelt hij die stap op voor je OK.

Bewerken is inbegrepen wanneer je de koppeling maakt. Bij een oudere koppeling die alleen kan lezen, zie je **Bewerken toestaan** onder **Koppelingen**. Druk er één keer op en geef toestemming.

## Waar hij toestemming voor vraagt

Microsoft vraagt één keer toestemming om je bestanden te lezen en te wijzigen, ook bestanden die met je zijn gedeeld. Elke wijziging wacht nog steeds op je OK bij de bijbehorende to-do. De toegang tot je mail en agenda verandert niet.

Als je die toestemming later intrekt, toont Microsoft OneDrive **Wacht op je OK om documenten te lezen** onder **Koppelingen**.

## Koppelen

Op een gehoste Machine of op je eigen computer, gekoppeld aan je account:

- Open **Koppelingen**, daarna **Documenten en bestanden**, en kies **Microsoft OneDrive**.
- Druk op **Inloggen met Microsoft** en geef toestemming om je bestanden te lezen en te bewerken.

Als Microsoft lezen niet toestaat, wordt de koppeling niet toegevoegd. Druk je op **Bewerken toestaan** en staat Microsoft bewerken niet toe, dan laat hij dat weten.

## Google Docs

Open op een gehoste Machine **Koppelingen**, daarna **Documenten en bestanden**, en kies **Google Docs**. Google vraagt je toestemming om de documenten waarnaar je verwijst te bekijken en te bewerken, en nieuwe documenten te maken. Gmail hoeft niet gekoppeld te zijn en je Gmail-toegang verandert niet.

Je Machine:

- Leest een Google-document waarnaar wordt verwezen in berichten van een to-do, alleen terwijl hij aan die to-do werkt.
- Bereidt wijzigingen aan dat document voor. Elke wijziging wacht op je OK, zoals hierboven beschreven.
- Maakt nieuwe privédocumenten in je Google Drive.

Hij doorzoekt je Drive niet. Hij ziet opmerkingen, gedeelde documenten en suggesties alleen in documenten die hij zelf heeft gemaakt. Voor meer toegang zou hij toegang tot je hele Drive nodig hebben, maar daar vraagt hij niet om.

Op je eigen computer kan je Machine een nieuw Google-document maken in een Gmail-account waarmee daar is ingelogd en dat al toegang tot Drive heeft. Hij leest je andere Google-documenten en de opmerkingen daarin niet. Onder **Documenten en bestanden** wordt dit weergegeven als Google Docs, gekoppeld aan dat account. Hij kan daar ook een document wijzigen dat hij voor een to-do heeft gemaakt.

## Werk of privé

Hij volgt het label Werk of Privé van de koppeling, net als bij mail. Werkdocumenten kunnen volgens je [deelregels](sharing-rules.md) terechtkomen in de Graph van je team. Privédocumenten komen daar nooit terecht.

## Ontkoppelen

Open **Koppelingen**, daarna Microsoft OneDrive of Google Docs, **Details** en **Ontkoppelen**. Hij stopt met lezen. Wat hij al heeft binnengehaald, blijft staan. Op een gehoste Machine opent **Ontkoppelen ↗** je installatiepagina, waar de login staat.
