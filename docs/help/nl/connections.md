---
title: Koppelingen
area: connections
summary: Al je bronnen op één plek: bekijk de status, voeg een bron toe of ontkoppel er een.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 1ca62ab8f65b77ff
---
## Status bekijken

Op het tabblad **Koppelingen** staan je bronnen per soort, met **Logins** en **Checks** onder een streep. Tik op je telefoon op een soort om die te openen en op **Koppelingen** om terug te gaan. Een soort met een bron die op jou wacht, wordt als eerste geopend. Elke bron staat op een regel met de status (Verbonden, Wacht op eerste synchronisatie, Bezig automatisch opnieuw te verbinden of Heeft je hulp nodig) en wat er onlangs is binnengekomen. Tik erop om de kaart en **Details** te openen.

Een mislukte synchronisatie die later is ingehaald, wordt grijs weergegeven. Alleen een fout bij de meest recente synchronisatie wordt als probleem weergegeven, met het tijdstip waarop er opnieuw wordt geprobeerd.

De aantallen laten zien hoeveel er in totaal is binnengekomen, ook wat in de [geschiedenis](history.md) staat, wat er in de afgelopen 24 uur is binnengekomen en wat nog niet is gecontroleerd. Bij een agenda gaat het om het aantal afspraken.

Elke bron is genoemd naar het account, zoals de dienst dat noemt: je adres, een X-profiel, een Slack-werkruimte of van wie de Signal- of Telegram-account is. Onder de naam staat eerst **Werk** of **Privé**, plus het adres of de gebruikersnaam als die niet al in de naam staat. Als twee bronnen van dezelfde soort dezelfde naam hebben, staat erbij waaraan je ze kunt onderscheiden, zoals Slack of X, of het adres van de werkruimte.

Bij elke bron staat ook in één regel wat die binnenbrengt en, als de bron acties kan uitvoeren, dat hij dat alleen doet nadat je op **Versturen** drukt of de actie goedkeurt.

## Een bron toevoegen

Open een soort (**E-mail**, **Agenda**, **Chat**, **Afspraken**, **Documenten en bestanden**, **Klanten**, **Projecten en code**, **Andere**) en kies een bron onder **Nog een toevoegen**, of onder de lijst als er nog niets is verbonden. Onderaan vind je opties voor alles wat niet in een andere categorie past: **Andere e-mail** onder E-mail, en **Agendalink (ICS)** en **Andere agenda** onder Agenda. Exchange Server leest afspraken en staat daarom onder Agenda.

**Voorgesteld voor jou** staat bovenaan **Koppelingen** als je Machine een reden ziet om een bron toe te voegen. Die reden staat er in één regel bij: e-mail van Stripe, Zoom-afspraken in je agenda, berichten met links naar Google Docs of een installatie die niet is afgerond. De bron blijft ook in de eigen groep staan, met het label **Voorgesteld**. Je Machine telt deze suggesties zelf; er wordt niets verstuurd. Een verbonden bron wordt nooit voorgesteld.

Microsoft Teams staat op twee plekken: onder **Chat** voor chats en onder **Afspraken** als **Teams-meetings** voor aantekeningen van meetings. Voor beide gebruik je dezelfde Microsoft-login. Als je de ene verbindt, wordt de andere ook verbonden.

In de lijst zie je welke bronnen je al hebt verbonden, met het bijbehorende account. Selecteer zo'n bron om er nog een naast te zetten. Het formulier geeft aan dat je een extra bron toevoegt en bevat een link naar de bestaande bron.

Vul de gevraagde gegevens in, zoals een sleutel of adres, kies **Werk** met de naam van je bedrijf of **Privé**, en druk op **Verbinden**. Bij e-mail en agenda wordt er alleen om gevraagd als het adres dit niet duidelijk maakt. Een website zoals LinkedIn of X opent de login in de browser van je Machine en gaat vanzelf verder zodra je bent ingelogd. GitHub, WhatsApp en Codex tonen een code die je moet invoeren. Telegram toont een QR-code om te scannen.

Met **Annuleren** stop je het toevoegen. Ben je weggegaan voordat het klaar was? Open **Koppelingen** opnieuw, op welk apparaat dan ook, en je gaat verder bij dezelfde stap. Zodra de bron is verbonden, begint je Machine die meteen te lezen en zie je hoe de eerste synchronisatie verloopt.

Op een gehoste Machine kun je meteen hier inloggen bij Google, Microsoft, Microsoft OneDrive, Zoom, Stripe en Intercom: kies **Werk** of **Privé** en druk op **Inloggen**. Je keert terug naar dit formulier, waar je ziet hoe het is gegaan. GitHub, WhatsApp, Codex, Telegram en je Android-telefoon tonen hun code hier ook.

Met **Opnieuw verbinden** bij een bron of onder **Wacht op jou** open je hetzelfde formulier. Op je eigen computer doet `assistant connect` hetzelfde in een terminal.

## Werk of privé

Elke bron is voor werk (bij een bedrijf dat je opgeeft) of privé. Je kunt dit wijzigen onder **Details**. **Geschat** betekent dat je Machine dit op basis van het adres heeft bepaald. Werkgerelateerde to-do's wachten tot je werkdagen.

Bij e-mail en agenda van Google en Microsoft wordt dit afgeleid van het adres als dat duidelijk is: een e-mailprovider zoals Gmail of Outlook.com betekent Privé, en het domein van je team betekent Werk. Anders wordt het je één keer gevraagd, meteen nadat je bent ingelogd. Met **Wijzigen** stel je dit zelf in. Als e-mails later iets anders aangeven, vraagt de to-do **Haal meer uit The Machine** één keer of je dit wilt aanpassen.

## Mogelijkheden

Een bron kan signalen binnenbrengen (wat binnenkomt, wordt omgezet in to-do's), dingen doen voor je to-do's (een document lezen of iets versturen, beantwoorden of wijzigen nadat je het goedkeurt), of allebei. Als de bron beide kan, staan er onder **Details** twee schakelaars: **Brengt signalen binnen** en **Kan dingen doen**. Eén ervan blijft altijd aan. Zet ze allebei uit door de bron te ontkoppelen. Bij een chat is alleen **Kan dingen doen** beschikbaar.

Als **Brengt signalen binnen** uitstaat, synchroniseert de bron niet. Als **Kan dingen doen** uitstaat, leest, schrijft of wijzigt je Machine er nooit iets mee.

## Een bron verwijderen

Open de bron, ga naar **Details** en kies **Ontkoppelen**. De bron wordt dan niet meer gelezen. Wat al is binnengebracht, blijft staan. Op een gehoste Machine staat bij Google, Microsoft, Microsoft OneDrive, Zoom en Stripe **Ontkoppelen ↗**. Daarmee open je de instellingenpagina.

Onder **Onlangs ontkoppeld** staan de Google-, Microsoft-, Zoom-, Slack-, Stripe- en Salesforce-accounts die je in de afgelopen 30 dagen hebt verwijderd, met de datum. Een Google-account wordt maar één keer weergegeven, ook als Google Meet of Docs een eigen login had. Elk account staat onder de eigen soort: een Google- of Microsoft-account onder **E-mail**, Slack onder **Chat**.

## Opgeslagen logins

Vink bij het inloggen op een website zoals LinkedIn of X **Bewaren voor de volgende keer** aan. De login staat dan onder **Logins**. Als een website je Machine uitlogt, logt hij met één tik weer in. Wachtwoorden blijven versleuteld op je Machine. Met **Vergeten** verwijder je een login.

## Checks

Onder **Checks** zie je hoe je Machine binnenkomende gegevens leest: recente controles en wat elke controle heeft gevonden. Zie [Geen nieuwe to-do's](reviews-paused.md).

Elke koppeling heeft een eigen artikel in dit gedeelte. Daarin staat wat de koppeling leest en wat hij kan versturen.
