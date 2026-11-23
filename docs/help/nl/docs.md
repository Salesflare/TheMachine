---
title: Microsoft OneDrive
area: connections
summary: Opmerkingen, vermeldingen en bijgehouden wijzigingen in je Word-bestanden in OneDrive. Nieuwe documenten en wijzigingen wachten op je OK.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 41e5651f29782588
---
## Wat wordt gelezen

**Microsoft OneDrive** leest je Word-bestanden in OneDrive, op een gehoste Machine en op je eigen computer. Outlook hoeft niet gekoppeld te zijn. Meer over Google Docs lees je hieronder. De integratie brengt het volgende binnen:

- Opmerkingen en reacties op je Word-bestanden, en opmerkingen waarin iemand je vermeldt.
- Bijgehouden wijzigingen in je Word-bestanden.

De eerste synchronisatie gaat 7 dagen terug. Elk item is gekoppeld aan de mensen en projecten in je [Graph](graph.md). Een opmerking waarvoor jij iets moet doen, wordt een to-do.

## Bestanden die anderen met je delen

Microsoft vermeldt deze bestanden vanaf november 2026 niet meer. Gedeelde bestanden en vermeldingen in bestanden van anderen bereiken je Machine dan alleen nog via e-mails van Microsoft. Koppel ook [Outlook](microsoft.md) en laat die e-mails aanstaan. Een to-do die uit zo'n e-mail komt, opent de e-mail en de knop daarin opent het bestand. Een gedeeld bestand of een vermelding zonder e-mail wordt niet gezien.

## Wat de integratie kan doen

Als een to-do de tekst van een document nodig heeft, leest je Machine dat document. Alleen terwijl hij aan die to-do werkt. Hij kan Word-, PDF- en tekstbestanden lezen.

Hij zoekt ook naar bestanden van elk type in je eigen OneDrive en geeft je de link. Hij zoekt niet in SharePoint-sites of in bestanden die met je zijn gedeeld. Hij kan de tekst van een gescande PDF niet lezen.

Hij kan een reactie op een opmerking opstellen. Word biedt geen mogelijkheid om van buitenaf reacties te plaatsen, dus kopieer je het concept naar Word.

Hij accepteert nooit een suggestie, lost nooit een opmerking op, deelt nooit een bestand en wijzigt nooit een document zonder je OK.

Wil je de integratie alleen gebruiken om dingen te doen, zet dan **Brengt signalen binnen** uit onder **Details**. Je Machine zoekt en leest dan alleen de bestanden die nodig zijn voor je to-do's en maakt nieuwe bestanden.

## Documenten maken en bewerken

Je Machine kan een nieuw document maken of een document wijzigen waar een to-do over gaat:

- Een nieuw document maakt hij meteen als de to-do of een skill daarom vraagt. Het is privé en staat in je eigen OneDrive of Google Drive. Bij de to-do staat **Open het document**. Delen of de link versturen wacht op je OK.
- Een wijziging aan een bestaand document bereidt hij alleen voor. Kies **Wijzigingen nakijken** om elke alinea vóór en na de wijziging te bekijken en kies daarna **Opslaan**. Een wijziging waar je om vraagt in de chat van de to-do, voert hij meteen uit.
- Hij schrijft alleen in het document zoals jij het hebt gezien. Heeft iemand het intussen gewijzigd, dan wordt er niets opgeslagen en staat dat bij de to-do. Vraag om een nieuw concept.
- In Talk leest hij de hele wijziging voor en wacht hij op een duidelijk ja.
- Weigert Microsoft of Google een nieuw document te maken, dan staat bij de to-do waarom en zie je **Nakijken en maken** om het opnieuw te proberen.

Hij kan tekst vervangen en tekst, alinea's en koppen toevoegen. Tabellen, afbeeldingen, bijgehouden wijzigingen en velden blijven zoals ze zijn.

Het document van een Werk-to-do komt in het account van dat bedrijf, nooit in een persoonlijk account. Op je eigen computer kan een Google-account dat voor Gmail is gekoppeld en toegang tot Drive heeft, ook nieuwe Google Docs maken. Past er geen account bij, dan staat bij de to-do wat je voor Werk moet koppelen: Microsoft OneDrive, of Google Docs als je Machine dat kan gebruiken.

Is het document niet de laatste stap, bijvoorbeeld omdat je een reactie met de link moet versturen, dan blijft de to-do open en stelt je Machine die stap op ter goedkeuring.

Bewerken is inbegrepen wanneer je koppelt. Bij een oudere koppeling waarmee je alleen kunt lezen, staat **Bewerken toestaan** onder **Koppelingen**. Kies dit eenmalig en geef toestemming.

## Waar toestemming voor wordt gevraagd

Microsoft vraagt je één keer toestemming om je bestanden te lezen en te wijzigen, ook bestanden die met je zijn gedeeld. Elke wijziging wacht nog steeds op je OK bij de bijbehorende to-do. De toegang tot je e-mail en agenda verandert niet.

Als je die toestemming later intrekt, staat bij Microsoft OneDrive onder **Koppelingen** de melding **Wacht op je OK om documenten te lezen**.

## Koppelen

Op een gehoste Machine of op je eigen computer als die aan je account is gekoppeld:

- Open **Koppelingen**, kies **Documenten en bestanden** en selecteer **Microsoft OneDrive**.
- Kies **Inloggen met Microsoft** en geef toestemming om je bestanden te lezen en te bewerken.

Als Microsoft lezen niet toestaat, wordt de koppeling niet toegevoegd. Als je **Bewerken toestaan** kiest en Microsoft bewerken niet toestaat, krijg je daar een melding van.

## Google Docs

Open op een gehoste Machine **Koppelingen**, kies **Documenten en bestanden** en selecteer **Google Docs**. Google vraagt je toestemming om de documenten die je aanwijst te bekijken en te bewerken, en nieuwe documenten te maken. Gmail hoeft niet gekoppeld te zijn en je Gmail-toegang verandert niet.

Je Machine doet daarna het volgende:

- Hij leest een Google Doc waarnaar in berichten van een to-do wordt gelinkt, alleen terwijl hij aan die to-do werkt.
- Hij bereidt wijzigingen in dat document voor. Voor elke wijziging is je OK nodig, zoals hierboven beschreven.
- Hij maakt nieuwe privédocumenten in je Google Drive.

Hij doorzoekt je Drive niet. Hij ziet opmerkingen, gedeelde documenten en suggesties alleen in documenten die hij zelf heeft gemaakt. Voor meer toegang zou hij je hele Drive nodig hebben, maar daar vraagt hij niet om.

Op je eigen computer kan je Machine een nieuw Google Doc maken in een Gmail-account dat daar is ingelogd en al toegang tot Drive heeft. Hij leest je andere Google Docs of de opmerkingen daarin niet. Onder **Documenten en bestanden** staat Google Docs bij dat account. Hij kan daar ook een document wijzigen dat hij voor een to-do heeft gemaakt.

## Werk of persoonlijk

Je Machine volgt het label Werk of Persoonlijk van de koppeling, net als bij e-mail. Werkdocumenten kunnen volgens je [deelregels](sharing-rules.md) in de Graph van je team terechtkomen. Persoonlijke documenten komen daar nooit terecht.

## Ontkoppelen

Open **Koppelingen**, kies Microsoft OneDrive of Google Docs, vervolgens **Details** en **Ontkoppelen**. Je Machine stopt met lezen. Wat hij al heeft binnengebracht, blijft staan. Op een gehoste Machine opent **Ontkoppelen ↗** je installatiepagina, waar de login wordt beheerd.
