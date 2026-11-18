---
title: Koppelingen
area: connections
summary: Je bronnen op één plek: hoe het met elke bron gaat, een nieuwe toevoegen of een bron ontkoppelen.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 9f2a2162fe015e0b
---
## Hoe het ermee gaat

Op het tabblad **Koppelingen** staan je bronnen per soort, met **Logins** en **Checks** onder een lijn. Tik op je telefoon op een soort om die te openen, en op **Koppelingen** om terug te gaan. Een soort met een bron die op je wacht, wordt als eerste geopend. Elke bron staat op een eigen regel: hoe het ermee gaat (Verbonden, Wacht op eerste synchronisatie, Automatisch opnieuw verbinden of Hulp nodig) en wat er onlangs is binnengekomen. Tik erop voor de kaart en **Details**.

Een mislukte synchronisatie die later is ingehaald, wordt grijs weergegeven. Alleen een fout die nog steeds de meest recente is, wordt als probleem weergegeven, met de tijd waarop opnieuw wordt geprobeerd.

De aantallen laten alles zien wat de bron heeft binnengebracht, ook de [geschiedenis](history.md), wat er de afgelopen 24 uur is binnengekomen en wat nog niet is gecontroleerd. Bij een agenda tellen de afspraken.

Elke bron is genoemd naar het account, zoals de dienst het noemt: je e-mailadres, een X-profiel, een Slack-werkruimte of van wie het Signal- of Telegram-account is. Onder de naam staat eerst **Werk** of **Privé**, plus het adres of de gebruikersnaam als dat niet al in de naam staat. Zijn er twee bronnen van dezelfde soort met dezelfde naam, dan staat er ook bij waaraan je ze herkent, zoals Slack of X, of het adres van de werkruimte.

Elke bron vermeldt ook in één regel wat hij binnenbrengt en, als hij dingen kan doen, dat hij dat alleen doet nadat je op **Versturen** drukt of toestemming geeft.

## Een bron toevoegen

Open een soort (**E-mail**, **Agenda**, **Chat**, **Afspraken**, **Documenten en bestanden**, **Klanten**, **Projecten en code**, **Andere**) en kies een bron onder **Nog een toevoegen**, of onder de lijst als er nog geen bron is gekoppeld. Helemaal onderaan staan opties voor alle andere gevallen: **Andere e-mail** onder E-mail, en **Agendalink (ICS)** en **Andere agenda** onder Agenda. Exchange Server haalt afspraken op en staat daarom onder Agenda.

**Voorgesteld voor jou** staat bovenaan **Koppelingen** als je Machine een reden ziet om een bron toe te voegen. Die reden staat er in één regel bij: e-mail van Stripe, Zoom-afspraken in je agenda, berichten met links naar Google Docs of een installatie die niet is afgerond. De bron blijft ook in de eigen groep staan, met het label **Voorgesteld**. Je Machine telt dit lokaal; er wordt niets van je Machine verstuurd. Een gekoppelde bron wordt nooit voorgesteld.

Microsoft Teams staat op twee plekken: onder **Chat** voor chats en onder **Afspraken** als **Teams-meetings** voor vergadernotities. Beide gebruiken dezelfde Microsoft-login, dus als je de ene koppelt, wordt de andere ook gekoppeld.

Als je een bron al hebt gekoppeld, staat dat in de lijst, samen met het account. Kies de bron om er nog een toe te voegen. Het formulier vermeldt dat en bevat een link naar de bron die je al hebt.

Vul in wat nodig is, zoals een sleutel of adres. Kies **Werk** met de naam van je bedrijf of **Privé**. Bij e-mail en agenda wordt dit alleen gevraagd als het adres geen uitsluitsel geeft. Druk daarna op **Verbinden**. Bij een site zoals LinkedIn of X opent de login in de browser van je Machine. Zodra je bent ingelogd, gaat alles vanzelf verder. Bij GitHub, WhatsApp en Codex krijg je een code om in te voeren. Bij Telegram- en Signal-chats krijg je een QR-code om te scannen.

Met **Annuleren** stop je het toevoegen. Ben je weggegaan voordat het klaar was? Open dan **Koppelingen** opnieuw, op welk apparaat dan ook. Je gaat verder waar je gebleven was. Zodra de bron is gekoppeld, begint je Machine die meteen te lezen en zie je hoe de eerste synchronisatie verloopt.

Op een gehoste Machine kun je hier inloggen bij bronnen met een eigen login: Google, Microsoft (Outlook, OneDrive en Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce en Trello.

Kies **Werk** of **Privé** en druk op de login-knop, zoals **Inloggen met Google**. Je keert terug naar dit formulier, waar je ziet hoe het is gegaan. De codes voor GitHub, WhatsApp, Codex, Telegram-chats en je Android-telefoon verschijnen hier ook.

Op je eigen computer log je bij dezelfde bronnen in zodra je Machine aan je account is gekoppeld. Druk de eerste keer op **Koppel deze Machine**. Sommige bronnen hebben ook een andere manier, zoals je eigen app of een sleutel.

Met **Opnieuw verbinden** bij een bron of onder **Wacht op jou** open je hetzelfde formulier. Op je eigen computer doet `assistant connect` hetzelfde in een terminal.

## Werk of privé

Elke bron is werk (voor een bedrijf dat je opgeeft) of privé. Wijzig dit onder **Details**. **Geschat** betekent dat je Machine dit op basis van het adres heeft bepaald. To-do's voor werk wachten tot je werkdagen.

Bij e-mail en agenda van Google en Microsoft wordt dit bepaald op basis van het adres, als dat duidelijk is: een e-mailprovider zoals Gmail of Outlook.com betekent Privé, het domein van je team betekent Werk. Is het niet duidelijk, dan wordt het één keer gevraagd, direct nadat je bent ingelogd. Met **Wijzigen** stel je dit zelf in. Als er later uit de e-mail blijkt dat de andere optie klopt, vraagt de to-do **Haal meer uit The Machine** één keer of je dit wilt wijzigen.

## Mogelijkheden

Een bron kan signalen binnenbrengen (wat binnenkomt, wordt to-do's), dingen doen voor je to-do's (een document lezen of iets versturen, beantwoorden of wijzigen nadat je toestemming hebt gegeven), of allebei. Bij allebei staan onder **Details** twee schakelaars: **Brengt signalen binnen** en **Kan dingen doen**. Eén ervan blijft aan. Als je beide wilt stoppen, ontkoppel je de bron. Bij een chat staat alleen **Kan dingen doen**.

Als **Brengt signalen binnen** uitstaat, synchroniseert de bron niet. Als **Kan dingen doen** uitstaat, leest, schrijft of wijzigt je Machine er niets mee.

## Een bron verwijderen

Open de bron en ga naar **Details**. Kies daarna **Ontkoppelen**. De bron wordt niet meer gelezen. Alles wat al is binnengebracht, blijft staan. Op een gehoste Machine staat bij bronnen waarvan de login op je instellingspagina wordt beheerd (Google, Microsoft, Google Meet, Slack, Zoom, Stripe en Salesforce) **Ontkoppelen ↗**. Hiermee open je je instellingspagina.

Onder **Onlangs ontkoppeld** staan de Google-, Microsoft-, Zoom-, Slack-, Stripe- en Salesforce-accounts die je de afgelopen 30 dagen hebt verwijderd, met het tijdstip erbij. Zolang de dienst de verwijdering nog niet heeft bevestigd, staat er In behandeling en blijft je Machine het opnieuw proberen. Een Google-account staat er maar één keer, ook als Google Meet of Docs een eigen login had. Elke account staat onder de eigen soort: een Google- of Microsoft-account onder **E-mail**, Slack onder **Chat**.

## Opgeslagen logins

Vink bij het inloggen op sites zoals LinkedIn of X **Bewaren voor de volgende keer** aan. De logins staan dan onder **Logins**. Als een site je Machine uitlogt, kan hij met één tik weer inloggen. Wachtwoorden blijven versleuteld op je Machine. Met **Vergeten** verwijder je een login.

Een site kan meerdere accounts hebben, bijvoorbeeld **Werk** en **Privé**. **Opslaan als** begint met de categorie van de to-do zelf. Met **Andere naam…** geef je de categorie zelf een naam. Een to-do logt in met het account dat erbij past. Is dat niet duidelijk, dan vraagt het venster één keer welk account je wilt gebruiken en onthoudt het je keuze voor die to-do.

Onder **Logins** staat elke site één keer, met de accounts eronder: de gebruikersnaam en een menu met de categorie. Je kunt die categorie daar op elk moment wijzigen. Bij logins die zijn opgeslagen voordat accounts beschikbaar waren, staat **Werk of privé?** totdat je een categorie kiest. Als je de categorie wijzigt, kiest een to-do die de login gebruikte opnieuw een login.

Met **Importeren** haal je logins uit een wachtwoordmanager: via een CSV-export van 1Password, LastPass, Bitwarden of Chrome, of rechtstreeks uit 1Password en LastPass via hun opdrachtregelprogramma's als je daarop bent ingelogd op deze computer. Je vinkt aan welke logins je wilt bewaren. Je Machine logt nooit in bij je wachtwoordmanager en vraagt nooit om het hoofdwachtwoord. Verwijder het exportbestand zodra je klaar bent.

Een opgeslagen login wordt alleen gebruikt op het bijbehorende webadres: dezelfde site, `https` en poort. Dus niet op een adres dat erop lijkt of op een ander subdomein.

## Checks

Onder **Checks** zie je hoe je Machine binnenkomende informatie leest: recente controles en wat elke controle heeft gevonden. Zie [Geen nieuwe to-do's](reviews-paused.md).

Elke koppeling heeft een eigen artikel in dit gedeelte, met informatie over wat de koppeling leest en wat hij kan versturen.
