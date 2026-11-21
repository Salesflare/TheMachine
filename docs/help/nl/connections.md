---
title: Koppelingen
area: connections
summary: Al je bronnen op één plek: bekijk de status, voeg een bron toe of ontkoppel er een.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 38d682b69cab758d
---
## Hoe het ermee gaat

Op het tabblad **Koppelingen** staan je bronnen per categorie. Onder de lijn vind je **Logins** en **Checks**. Tik op je telefoon op een categorie om die te openen en op **Koppelingen** om terug te gaan. Een categorie met een bron die op jou wacht, wordt als eerste geopend. Elke bron staat op een eigen regel, met de status (Verbonden, Wacht op de eerste synchronisatie, Maakt automatisch opnieuw verbinding of Heeft je hulp nodig) en wat er onlangs is binnengekomen. Tik erop voor de kaart met **Details**.

Een mislukte synchronisatie die door een latere synchronisatie is ingehaald, wordt grijs weergegeven. Alleen een mislukte synchronisatie die nog steeds de meest recente is, wordt als probleem getoond, met het tijdstip waarop de volgende poging plaatsvindt.

De aantallen laten alles zien wat de bron heeft binnengebracht, ook de [geschiedenis](history.md), wat er de afgelopen 24 uur is binnengekomen en wat nog niet is gecontroleerd. Bij een agenda tellen de afspraken.

Elke bron is genoemd naar het account, zoals de dienst dat weergeeft: je adres, een X-profiel, een Slack-werkruimte of van wie de Signal- of Telegram-account is. Onder de naam staat eerst **Werk** of **Privé**, plus het adres of de gebruikersnaam als dat niet al in de naam staat. Als twee bronnen van dezelfde categorie dezelfde naam hebben, staat er ook bij waaraan je ze kunt herkennen, zoals Slack of X, of het adres van de werkruimte.

Bij elke bron staat in één regel wat hij binnenbrengt en, als hij ook acties kan uitvoeren, dat hij dat alleen doet nadat je op **Versturen** drukt of de actie goedkeurt.

## Een bron toevoegen

Open een categorie (**E-mail**, **Agenda**, **Chat**, **Afspraken**, **Documenten en bestanden**, **Klanten**, **Projecten en code**, **Andere**) en kies een bron onder **Nog een toevoegen**, of onder de lijst als er nog niets is gekoppeld. Helemaal onderaan staan de opties voor overige bronnen: **Andere e-mail** onder E-mail, **Agendalink (ICS)** en **Andere agenda** onder Agenda. Exchange Server leest afspraken en staat daarom onder Agenda.

**Voorgesteld voor jou** staat bovenaan **Koppelingen** als je Machine een reden ziet om een bron toe te voegen. Die reden staat er in één regel bij: e-mail van Stripe, Zoom-afspraken in je agenda, berichten met links naar Google Docs of een installatie die niet is afgerond. De bron blijft ook in de eigen groep staan, met het label **Voorgesteld**. Deze suggesties worden op je Machine geteld; er wordt niets van je Machine verstuurd. Een gekoppelde bron wordt nooit voorgesteld.

Microsoft Teams staat twee keer in de lijst: onder **Chat** voor chats en onder **Afspraken** als **Teams-meetings** voor aantekeningen van vergaderingen. Beide gebruiken dezelfde Microsoft-login. Als je de ene koppelt, wordt de andere ook gekoppeld.

In de lijst staat bij een bron die je al hebt gekoppeld dat hij is gekoppeld, samen met het account. Kies die bron om er nog een naast toe te voegen. Het formulier vermeldt dat en bevat een link naar de bestaande bron.

Vul de benodigde gegevens in, zoals een sleutel of adres, kies **Werk** met de bedrijfsnaam of **Privé**, en druk op **Verbinden**. Bij e-mail en agenda's wordt hier alleen naar gevraagd als het adres niet duidelijk maakt welke optie je moet kiezen. Bij een site zoals LinkedIn of X wordt de login geopend in de browser van je Machine. Zodra je bent ingelogd, gaat het vanzelf verder. Bij GitHub, WhatsApp en Codex krijg je een code om in te voeren. Voor Telegram- en Signal-chats krijg je een QR-code om te scannen.

Met **Annuleren** stop je het toevoegen. Ben je weggegaan voordat het klaar was? Open **Koppelingen** opnieuw, op welk apparaat dan ook, en je gaat verder bij dezelfde stap. Zodra de bron is gekoppeld, begint je Machine hem meteen te lezen en zie je hoe de eerste synchronisatie verloopt.

Op een gehoste Machine kun je bij bronnen met een eigen login meteen hier inloggen: Google, Microsoft (Outlook, OneDrive en Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce en Trello.

Kies **Werk** of **Privé** en druk op de login-knop, zoals **Inloggen met Google**. Je keert terug naar dit formulier, waar je ziet hoe het is gegaan. De codes voor GitHub, WhatsApp, Codex, Telegram-chats en je Android-telefoon verschijnen hier ook.

Op je eigen computer kun je bij dezelfde bronnen inloggen zodra je Machine aan je account is gekoppeld. Druk de eerste keer op **Koppel deze Machine**. Sommige bronnen bieden ook een andere manier, zoals een eigen app of een sleutel.

Met **Opnieuw verbinden** bij een bron en in **Wacht op jou** open je hetzelfde formulier. Op je eigen computer doet `assistant connect` hetzelfde in een terminal.

## Werk of privé

Elke bron is voor werk (bij een bedrijf dat je opgeeft) of privé. Je kunt dit wijzigen onder **Details**. **Geraden** betekent dat je Machine dit heeft afgeleid van het adres. Werkgerelateerde to-do's wachten tot je werkdagen.

Bij e-mail en agenda's van Google en Microsoft wordt dit afgeleid van het adres als dat duidelijk is: een e-mailprovider zoals Gmail of Outlook.com betekent Privé, het domein van je team betekent Werk. Als dat niet duidelijk is, wordt het één keer gevraagd, meteen nadat je bent ingelogd. Met **Wijzigen** stel je dit zelf in. Als je e-mail later aangeeft dat de andere optie beter past, vraagt de to-do **Haal meer uit The Machine** één keer of je dit wilt wijzigen.

## Mogelijkheden

Een bron kan signalen binnenbrengen (wat binnenkomt, wordt een to-do), acties uitvoeren voor je to-do's (een document lezen, of iets versturen, beantwoorden of wijzigen nadat je het hebt goedgekeurd), of allebei. Als de bron beide kan, staan er onder **Details** aparte schakelaars: **Brengt signalen binnen** en **Kan dingen doen**. Eén van de twee blijft aan. Wil je allebei uitzetten, ontkoppel de bron dan. Bij een chat staat alleen **Kan dingen doen**.

Als **Brengt signalen binnen** uitstaat, wordt de bron niet gesynchroniseerd. Als **Kan dingen doen** uitstaat, leest, schrijft of wijzigt je Machine er niets mee.

## Een bron verwijderen

Open de bron, kies **Details** en daarna **Ontkoppelen**. De bron wordt niet meer gelezen. Wat al is binnengebracht, blijft staan. Op een gehoste Machine staat bij een bron waarvan de login op je instellingenpagina wordt beheerd (Google, Microsoft, Google Meet, Slack, Zoom, Stripe en Salesforce) **Ontkoppelen ↗**. Daarmee open je je instellingenpagina.

**Onlangs ontkoppeld** toont de Google-, Microsoft-, Zoom-, Slack-, Stripe- en Salesforce-accounts die je de afgelopen 30 dagen hebt verwijderd, en wanneer je dat hebt gedaan. Totdat de dienst de verwijdering bevestigt, staat er In behandeling en blijft je Machine het opnieuw proberen. Een Google-account wordt maar één keer getoond, ook als Google Meet of Docs een eigen login had. Elk account staat onder de eigen categorie: een Google- of Microsoft-account onder **E-mail**, Slack onder **Chat**.

## Opgeslagen logins

Vink **Bewaren voor de volgende keer** aan als je inlogt op sites zoals LinkedIn of X. Daarna staan ze onder **Logins**. Als een site je Machine uitlogt, logt hij met één tik weer in. Wachtwoorden blijven versleuteld op je Machine. Met **Vergeten** verwijder je een login.

Een site kan meerdere accounts hebben, bijvoorbeeld **Werk** en **Privé**. Met **Opslaan als** begin je bij de categorie van de to-do zelf. Met **Andere naam…** geef je die zelf een naam. Een to-do gebruikt de login die erbij past. Als dat niet duidelijk is, vraagt het venster één keer welke login je wilt gebruiken en onthoudt het die keuze voor die to-do.

Onder **Logins** staat elke site één keer, met de bijbehorende accounts eronder: de gebruikersnaam en een menu met de categorie. Je kunt die categorie daar altijd wijzigen. Logins die zijn opgeslagen voordat accounts beschikbaar waren, krijgen het label **Werk of privé?** totdat je een keuze maakt. Een to-do die een login gebruikte, kiest opnieuw zodra je de categorie ervan wijzigt.

Met **Importeren** importeer je logins uit een wachtwoordmanager. Kies er een:

- **LastPass**, **Bitwarden** of **Google Password Manager**: de exportpagina wordt geopend in de browser van je Machine. Log daar in. Je Machine klikt verder naar de export. Er staat in één regel wat je nog moet doen, bijvoorbeeld je hoofdwachtwoord invoeren. Op een telefoon zoomt het scherm in op het veld waarin je moet typen. Ziet de pagina er anders uit dan verwacht, dan verschijnen in plaats daarvan de stappen om de export handmatig af te ronden. Je Machine haalt het bestand op, leest het één keer en verwijdert het.
- **1Password**: exporteer een CSV-bestand vanuit de 1Password-app op een computer en kies daarna dat bestand. Als `op` van 1Password op je Machine is ingelogd, leest je Machine de gegevens daaruit (dat geldt ook voor `lpass` van LastPass).
- **Uit een exportbestand**: een CSV-bestand van 1Password, LastPass, Bitwarden of Chrome. Verwijder het bestand zodra je klaar bent.

Vink daarna aan welke logins je wilt bewaren. Je Machine logt nooit voor je in bij je wachtwoordmanager, typt of leest nooit het hoofdwachtwoord en laat de pagina nooit aan de assistent zien. Je typt het wachtwoord zelf in op de pagina.

Een opgeslagen login wordt alleen gebruikt op het bijbehorende webadres: dezelfde site, `https` en poort. Niet op een adres dat erop lijkt en niet op een ander subdomein.

## Checks

Onder **Checks** zie je hoe je Machine controleert wat er binnenkomt: recente controles en wat elke controle heeft gevonden. Zie [Geen nieuwe to-do's](reviews-paused.md).

Elke koppeling heeft een eigen artikel in dit gedeelte, met informatie over wat de bron leest en kan versturen.
