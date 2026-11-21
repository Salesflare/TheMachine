---
title: Koppelingen
area: connections
summary: Al je bronnen op één plek: bekijk de status, voeg een bron toe of koppel er een los.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 0896d8f689ca9699
---
## Hoe het ermee gaat

Op het tabblad **Koppelingen** staan je bronnen per soort, met **Logins** en **Checks** onder een streep. Tik op je telefoon op een soort om die te openen en op **Koppelingen** om terug te gaan. Een soort met een bron die op je wacht, wordt als eerste geopend. Elke bron staat op een rij met de status (Verbonden, Wacht op eerste synchronisatie, Opnieuw verbinden of Heeft je hulp nodig) en wat er onlangs is binnengekomen. Tik erop voor de kaart en **Details**.

Een mislukte synchronisatie die door een latere is ingehaald, wordt grijs weergegeven. Alleen een mislukte synchronisatie die nog steeds de laatste is, wordt als probleem getoond, met de tijd waarop opnieuw wordt geprobeerd.

De aantallen laten alles zien wat de bron heeft binnengebracht, ook de [geschiedenis](history.md), wat er de afgelopen 24 uur is binnengekomen en wat nog niet is gecontroleerd. Bij een agenda tellen de afspraken mee.

Elke bron krijgt de naam van het account, zoals de dienst die weergeeft: je adres, een X-profiel, een Slack-werkruimte of van wie de Signal- of Telegram-chat is. Onder de naam staat eerst **Werk** of **Privé**, plus het adres of de gebruikersnaam als die niet al in de naam staat. Als twee bronnen van dezelfde soort dezelfde naam hebben, staat er ook bij waaraan je ze kunt herkennen, zoals Slack of X, of het adres van de werkruimte.

Bij elke bron staat ook in één regel wat die binnenbrengt en, als de bron acties kan uitvoeren, dat hij dat alleen doet nadat je op **Versturen** drukt of toestemming geeft.

## Een koppeling toevoegen

Open een soort (**E-mail**, **Agenda**, **Chat**, **Afspraken**, **Documenten en bestanden**, **Klanten**, **Projecten en code**, **Andere**) en kies een bron onder **Nog een toevoegen**, of onder de lijst als er nog geen bron is gekoppeld. Onderaan staan de opties voor overige bronnen: **Andere e-mail** onder E-mail, en **Agendalink (ICS)** en **Andere agenda** onder Agenda. Exchange Server haalt afspraken op en staat daarom onder Agenda.

**Voorgesteld voor jou** staat bovenaan **Koppelingen** als je Machine een reden ziet om een bron toe te voegen. Die reden staat er in één regel bij, zoals e-mail van Stripe, Zoom-meetings in je agenda, berichten met links naar Google Docs of een installatie die niet is afgerond. De bron blijft ook in de eigen groep staan, met de aanduiding **Voorgesteld**. Deze gegevens worden op je Machine geteld en verlaten hem niet. Een gekoppelde bron wordt nooit voorgesteld.

Microsoft Teams staat op twee plekken: onder **Chat** voor chats en onder **Afspraken** als **Teams-meetings** voor aantekeningen van meetings. Beide gebruiken dezelfde Microsoft-login, dus als je de ene koppelt, wordt de andere ook gekoppeld.

In de lijst staat bij een bron die je al hebt gekoppeld dat die is gekoppeld, samen met het account. Kies de bron om er nog een naast toe te voegen. Dat staat op het formulier, met een link naar de bron die je al hebt.

Vul de gevraagde gegevens in, zoals een sleutel of adres, kies **Werk** met de bedrijfsnaam of **Privé**. Bij e-mail en agenda wordt dit alleen gevraagd als het adres het niet verraadt. Druk daarna op **Verbinden**. Bij een site zoals LinkedIn of X wordt de inlogpagina geopend in de browser van je Machine. Zodra je bent ingelogd, gaat het vanzelf verder. Bij GitHub, WhatsApp en Codex krijg je een code om in te voeren. Voor Telegram- en Signal-chats krijg je een QR-code om te scannen.

Met **Annuleren** stop je het toevoegen. Weggegaan voordat het klaar was? Open **Koppelingen** opnieuw op een apparaat naar keuze. Je gaat dan verder vanaf dezelfde stap. Zodra de bron is gekoppeld, begint je Machine die meteen te lezen en zie je hoe de eerste synchronisatie verloopt.

Op een gehoste Machine log je hier in bij bronnen met een eigen login: Google, Microsoft (Outlook, OneDrive en Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce en Trello.

Kies **Werk** of **Privé** en druk op de inlogknop, bijvoorbeeld **Inloggen met Google**. Je keert terug naar dit formulier, waar je ziet hoe het is gegaan. Bij GitHub, WhatsApp, Codex, Telegram-chats en je Android-telefoon staat de code hier ook.

Op je eigen computer log je bij dezelfde bronnen in zodra je Machine aan je account is gekoppeld. Druk de eerste keer op **Koppel deze Machine**. Sommige bronnen bieden ook een andere manier, zoals je eigen app of een sleutel.

Met **Opnieuw verbinden** bij een bron of onder **Wacht op jou** open je hetzelfde formulier. Op je eigen computer doet `assistant connect` hetzelfde in een terminal.

## Werk of privé?

Elke bron is werk (voor een bedrijf dat je opgeeft) of privé. Je kunt dit wijzigen onder **Details**. **Geschat** betekent dat je Machine dit heeft afgeleid van het adres. Werk-to-do's wachten tot je werkdagen.

Bij e-mail en agenda van Google en Microsoft wordt dit afgeleid van het adres als dat duidelijk is: een e-maildienst zoals Gmail of Outlook.com betekent Privé, het domein van je team betekent Werk. Is het niet duidelijk, dan wordt het één keer gevraagd, meteen nadat je bent ingelogd. Met **Wijzigen** stel je dit zelf in. Als je e-mail later op de andere optie wijst, vraagt de to-do **Haal meer uit The Machine** één keer of je dit wilt wijzigen.

## Mogelijkheden

Een bron kan signalen binnenbrengen (wat binnenkomt, wordt omgezet in to-do's), dingen doen voor je to-do's (een document lezen of iets versturen, beantwoorden of wijzigen nadat je toestemming hebt gegeven), of allebei. Als een bron beide kan, staan er onder **Details** schakelaars voor **Brengt signalen binnen** en **Kan dingen doen**. Eén daarvan blijft aan. Als je beide wilt stoppen, koppel je de bron los. Bij een chat staat alleen **Kan dingen doen**.

Als **Brengt signalen binnen** uitstaat, wordt de bron niet gesynchroniseerd. Als **Kan dingen doen** uitstaat, leest, schrijft of wijzigt je Machine er nooit iets mee.

## Een koppeling verwijderen

Open de bron en kies **Details**, daarna **Ontkoppelen**. De bron wordt niet meer gelezen. Wat al is binnengebracht, blijft staan. Op een gehoste Machine staat bij bronnen waarvan de login op je installatiepagina wordt beheerd (Google, Microsoft, Google Meet, Slack, Zoom, Stripe en Salesforce) **Ontkoppelen ↗**. Daarmee open je je installatiepagina.

Onder **Onlangs ontkoppeld** staan de Google-, Microsoft-, Zoom-, Slack-, Stripe- en Salesforce-accounts die je de afgelopen 30 dagen hebt verwijderd, met het tijdstip. Tot de dienst de verwijdering bevestigt, staat er In behandeling en blijft je Machine het proberen. Een Google-account wordt maar één keer getoond, ook als Google Meet of Docs een eigen login had. Elk account staat onder de eigen soort: een Google- of Microsoft-account onder **E-mail**, Slack onder **Chat**.

## Opgeslagen logins

Vink bij het inloggen op sites zoals LinkedIn of X **Bewaren voor de volgende keer** aan. De logins staan daarna onder **Logins**. Als een site je Machine uitlogt, kan hij met één tik weer inloggen. Wachtwoorden blijven versleuteld op je Machine. Met **Vergeten** verwijder je een login.

Een site kan meerdere accounts hebben, bijvoorbeeld **Werk** en **Privé**. **Opslaan als** begint bij de categorie van de to-do zelf. Met **Andere naam…** geef je een eigen naam op. Een to-do logt in met het account dat erbij past. Als dat niet duidelijk is, vraagt het dialoogvenster één keer welk account je wilt gebruiken en onthoudt het dit voor die to-do.

Onder **Logins** staat elke site één keer, met de accounts eronder: de gebruikersnaam en een menu met de categorie. Je kunt die categorie daar op elk moment wijzigen. Bij logins die zijn opgeslagen voordat accounts beschikbaar waren, staat **Werk of privé?** totdat je een keuze maakt. Een to-do die een login gebruikte, kiest opnieuw nadat je de categorie ervan wijzigt.

Met **Importeren** importeer je logins uit een wachtwoordmanager. Kies er een:

- **LastPass**, **Bitwarden** of **Google Password Manager**: de exportpagina wordt geopend in de browser van je Machine en is meteen zichtbaar in het dialoogvenster, net als bij **Doe het** van een to-do. Log daar in. Je Machine klikt vervolgens door naar de export. In één regel staat wat je nog moet doen, zoals je hoofdwachtwoord invoeren. LastPass e-mailt een link om de export te bevestigen. Je Machine start de export één keer en opent die link zelf zodra de e-mail binnen 10 minuten in een gekoppelde mailbox aankomt. Gebeurt dat niet, dan vraagt je Machine je om opnieuw te bevestigen en te exporteren. Op een telefoon zoomt het scherm in op het veld waarin je typt. Ziet de pagina er anders uit dan verwacht, dan worden de stappen getoond om het handmatig af te ronden. Je Machine haalt het bestand op, leest het één keer en verwijdert het.
- **1Password**: exporteer een CSV vanuit de 1Password-app op een computer en kies daarna dat bestand. Als `op` van 1Password op je Machine is ingelogd, leest je Machine de gegevens daar vandaan (hetzelfde geldt voor `lpass` van LastPass).
- **Uit een exportbestand**: een CSV uit 1Password, LastPass, Bitwarden of Chrome. Verwijder het bestand zodra je klaar bent.

Vink daarna aan welke logins je wilt bewaren. Je Machine logt nooit voor je in bij je wachtwoordmanager, typt of leest nooit je hoofdwachtwoord en toont de pagina nooit aan de assistent. Je typt het wachtwoord zelf in op de pagina.

Een opgeslagen login wordt alleen gebruikt op het bijbehorende webadres: dezelfde site, `https` en poort. Niet op een adres dat erop lijkt en niet op een ander subdomein.

## Checks

Onder **Checks** zie je hoe je Machine binnenkomende gegevens verwerkt: recente controles en wat elke controle heeft gevonden. Zie [Geen nieuwe to-do's](reviews-paused.md).

Elke koppeling heeft in dit gedeelte een eigen artikel, met wat de bron leest en wat hij kan versturen.
