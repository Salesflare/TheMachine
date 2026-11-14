---
title: Koppelingen
area: connections
summary: Je bronnen op één plek: bekijk hoe het met elke bron gaat, voeg een nieuwe toe of koppel een bron los.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 60304f2504ee5676
---
## Hoe het ermee gaat

Op het tabblad **Koppelingen** staan je bronnen per soort, met **Logins** en **Checks** onder een scheidingslijn. Tik op je telefoon op een soort om die te openen en op **Koppelingen** om terug te gaan. Een soort met een bron die aandacht nodig heeft, wordt als eerste geopend. Elke bron staat op een rij met de status (Verbonden, Wacht op de eerste synchronisatie, Wordt automatisch opnieuw verbonden of Heeft je hulp nodig) en wat er onlangs is binnengekomen. Tik op een bron voor de kaart en **Details**.

Een mislukte synchronisatie die door een latere is ingehaald, wordt grijs weergegeven. Alleen een mislukte synchronisatie die nog steeds de nieuwste is, wordt als probleem getoond, met de tijd van de volgende poging.

De aantallen laten alles zien wat de bron heeft binnengehaald, ook de [geschiedenis](history.md), wat er in de afgelopen 24 uur is binnengekomen en wat nog niet is gecontroleerd. Bij een agenda tellen de afspraken mee.

Elke bron krijgt de naam van het account, zoals de dienst die weergeeft: je adres, een X-profiel, een Slack-werkruimte of van wie het Signal- of Telegram-account is. Onder de naam staat eerst **Werk** of **Privé**, plus het adres of de gebruikersnaam als die niet al in de naam staat. Hebben twee bronnen van dezelfde soort dezelfde naam, dan staat erbij waaraan je ze kunt herkennen, zoals Slack of X, of het adres van de werkruimte.

Bij elke bron staat in één regel wat hij binnenhaalt en, als hij acties kan uitvoeren, dat hij dat alleen doet nadat je op **Versturen** hebt gedrukt of daarvoor OK hebt gegeven.

## Een bron toevoegen

Open een soort (**E-mail**, **Agenda**, **Chat**, **Afspraken**, **Documenten en bestanden**, **Klanten**, **Projecten en code**, **Andere**) en kies een bron onder **Nog een toevoegen**, of onder de lijst als er nog geen bron is gekoppeld. Onderaan staan de opties voor overige bronnen: **Andere e-mail** onder E-mail, **Agendalink (ICS)** en **Andere agenda** onder Agenda. Exchange Server haalt afspraken op en staat daarom onder Agenda.

**Voorgesteld voor jou** staat bovenaan **Koppelingen** als je Machine een reden ziet om een bron toe te voegen. Die reden staat er in één regel bij: e-mail van Stripe, Zoom-afspraken in je agenda, berichten met links naar Google Docs of een installatie die niet is afgerond. De bron blijft ook in de eigen groep staan, met de markering **Voorgesteld**. Deze suggesties worden op je Machine geteld; er wordt niets vanaf gestuurd. Een gekoppelde bron wordt nooit voorgesteld.

Microsoft Teams staat op twee plekken: onder **Chat** voor chats en onder **Afspraken** als **Teams-meetings** voor vergadernotities. Beide gebruiken dezelfde Microsoft-login. Als je de ene koppelt, wordt de andere dus ook gekoppeld.

In de lijst staat bij een bron die je al hebt gekoppeld dat hij verbonden is, met het bijbehorende account. Kies die bron om er nog een naast te zetten. In het formulier staat dat erbij en vind je een link naar de bestaande bron.

Vul in wat nodig is, zoals een sleutel of adres, kies **Werk** met de naam van je bedrijf of **Privé**, en druk op **Verbinden**. Bij e-mail en agenda wordt dit alleen gevraagd als het adres het niet duidelijk maakt. Een site zoals LinkedIn of X opent de login in de browser van je Machine en gaat vanzelf verder zodra je bent ingelogd. GitHub, WhatsApp en Codex tonen een code die je moet invoeren. Voor Telegram-chats en Signal-chats krijg je een QR-code om te scannen.

Met **Annuleren** stop je het toevoegen. Ben je weggegaan voordat het klaar was? Open dan op een apparaat **Koppelingen** opnieuw. Je gaat verder bij dezelfde stap. Zodra de bron is gekoppeld, begint je Machine die meteen te lezen en zie je hoe de eerste synchronisatie verloopt.

Op een gehoste Machine kun je hier inloggen bij bronnen met een eigen login: Google, Microsoft (Outlook, OneDrive en Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce en Trello.

Kies **Werk** of **Privé** en druk op de login-knop, zoals **Inloggen met Google**. Je keert terug naar dit formulier, waar je ziet hoe het is gegaan. GitHub, WhatsApp, Codex, Telegram-chats en je Android-telefoon tonen hun code hier ook.

Op je eigen computer log je bij dezelfde bronnen in zodra je Machine aan je account is gekoppeld. Druk de eerste keer op **Koppel deze Machine**. Sommige bronnen bieden ook een andere manier, zoals je eigen app of een sleutel.

Met **Opnieuw verbinden** bij een bron of onder **Wacht op jou** open je hetzelfde formulier. Op je eigen computer doet `assistant connect` hetzelfde in een terminal.

## Werk of privé

Elke bron wordt ingedeeld als werk (voor een bedrijf dat je opgeeft) of privé. Je kunt dit wijzigen onder **Details**. **Geschat** betekent dat je Machine de indeling heeft afgeleid van het adres. Werk-to-do's wachten tot je werkdagen.

Bij e-mail en agenda van Google en Microsoft wordt de indeling afgeleid van het adres als dat duidelijk is: een e-mailprovider zoals Gmail of Outlook.com betekent Privé, het domein van je team betekent Werk. Anders wordt het je één keer gevraagd, meteen nadat je bent ingelogd. Met **Wijzigen** stel je de indeling zelf in. Als e-mail later een andere indeling aangeeft, vraagt de to-do **Haal meer uit The Machine** één keer of je die wilt wijzigen.

## Mogelijkheden

Een bron kan signalen binnenhalen (wat binnenkomt, wordt omgezet in to-do's), dingen doen voor je to-do's (een document lezen, iets versturen of beantwoorden, of iets wijzigen nadat je daarvoor OK hebt gegeven), of allebei. Als een bron beide kan, staan onder **Details** aparte schakelaars: **Brengt signalen binnen** en **Kan dingen doen**. Een van de twee blijft aan. Wil je beide uitzetten, koppel de bron dan los. Bij een chat is er alleen **Kan dingen doen**.

Als **Brengt signalen binnen** uitstaat, wordt de bron niet gesynchroniseerd. Als **Kan dingen doen** uitstaat, leest, schrijft of wijzigt je Machine nooit iets met die bron.

## Een bron verwijderen

Open de bron en kies **Details** en daarna **Ontkoppelen**. De bron wordt dan niet meer gelezen. Wat hij al heeft binnengehaald, blijft staan. Op een gehoste Machine staat bij een bron waarvan de login op je instellingenpagina wordt beheerd (Google, Microsoft, Google Meet, Slack, Zoom, Stripe en Salesforce) **Ontkoppelen ↗**. Daarmee open je je instellingenpagina.

**Onlangs ontkoppeld** toont de Google-, Microsoft-, Zoom-, Slack-, Stripe- en Salesforce-accounts die je in de afgelopen 30 dagen hebt verwijderd, en wanneer dat was. Tot de dienst de verwijdering bevestigt, staat er In behandeling en blijft The Machine het opnieuw proberen. Een Google-account wordt één keer getoond, ook als Google Meet of Docs een eigen login had. Elke bron staat onder de eigen soort: een Google- of Microsoft-account onder **E-mail**, Slack onder **Chat**.

## Opgeslagen logins

Vink bij het inloggen op sites zoals LinkedIn of X **Bewaren voor de volgende keer** aan. De logins staan dan onder **Logins**. Als een site je Machine uitlogt, logt hij met één tik weer in. Wachtwoorden blijven versleuteld op je Machine. Met **Vergeten** verwijder je een login.

## Checks

Onder **Checks** zie je hoe je Machine binnenkomende informatie verwerkt: recente controles en wat elke controle heeft gevonden. Zie [Geen nieuwe to-do's](reviews-paused.md).

Elke koppeling heeft een eigen artikel in dit gedeelte, met wat de bron leest en wat hij kan versturen.
