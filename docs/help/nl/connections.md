---
title: Koppelingen
area: connections
summary: Al je bronnen op één plek: bekijk hoe het ermee gaat, voeg een bron toe of koppel er een los.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: ec53596a1636fee7
---
## Hoe het ermee gaat

Op het tabblad **Koppelingen** staan je bronnen per soort, met **Logins** en **Checks** onder een scheidingslijn. Tik op je telefoon op een soort om die te openen en op **Koppelingen** om terug te gaan. Een soort met een bron die op jou wacht, wordt als eerste geopend. Elke bron staat op een rij met de status (Connected, Waiting for first sync, Reconnecting automatically of Needs your help) en wat er onlangs is binnengekomen. Tik erop voor de kaart en **Details**.

Een mislukte synchronisatie die door een latere is ingehaald, wordt grijs weergegeven. Alleen een mislukte synchronisatie die nog steeds de laatste is, wordt als probleem getoond, met het tijdstip waarop het opnieuw wordt geprobeerd.

De aantallen laten alles zien wat de bron heeft binnengebracht, ook de [geschiedenis](history.md), wat er de afgelopen 24 uur is binnengekomen en wat nog niet is gecontroleerd. Bij een agenda tellen de aantallen afspraken.

Elke bron krijgt de naam van het bijbehorende account, zoals de dienst die weergeeft: je adres, een X-profiel, een Slack-werkruimte of van wie het Signal- of Telegram-account is. Onder de naam staat eerst **Werk** of **Privé**, plus het adres of de gebruikersnaam als die niet al in de naam staat. Hebben twee bronnen van dezelfde soort dezelfde naam, dan staat er ook bij waaraan je ze kunt herkennen, zoals Slack of X, of het adres van de werkruimte.

Elke bron vermeldt ook in één regel wat hij binnenbrengt en, als hij acties kan uitvoeren, dat hij dat alleen doet nadat je op **Versturen** hebt gedrukt of toestemming hebt gegeven.

## Een bron toevoegen

Open een soort (**E-mail**, **Agenda**, **Chat**, **Afspraken**, **Documenten en bestanden**, **Klanten**, **Projecten en code**, **Andere**) en kies een bron onder **Nog een toevoegen**, of onder de lijst als er nog geen bron is gekoppeld. Helemaal onderaan staan algemene opties: **Andere e-mail** onder E-mail, en **Agendalink (ICS)** en **Andere agenda** onder Agenda. Exchange Server haalt afspraken op en staat daarom onder Agenda.

**Voorgesteld voor jou** staat bovenaan **Koppelingen** als je Machine een reden ziet om een bron toe te voegen. Die reden staat er in één regel bij: e-mail van Stripe, Zoom-afspraken in je agenda, berichten met links naar Google Docs of een installatie die niet is afgerond. De bron blijft ook in de eigen groep staan, met het label **Voorgesteld**. Deze suggesties worden op je Machine geteld; er wordt niets vanaf verstuurd. Een gekoppelde bron wordt nooit voorgesteld.

Microsoft Teams staat op twee plekken: onder **Chat** voor de chats en onder **Afspraken** als **Teams-meetings** voor de aantekeningen van vergaderingen. Beide gebruiken dezelfde Microsoft-login. Als je de ene koppelt, wordt de andere dus ook gekoppeld.

Een bron die je al hebt gekoppeld, staat met het bijbehorende account in de lijst. Kies die bron om er nog een naast toe te voegen: het formulier vermeldt dat en bevat een link naar de bestaande bron.

Vul in wat nodig is, zoals een sleutel of adres, kies **Werk** met de naam van je bedrijf of **Privé**, en druk op **Verbinden**. Bij e-mail en agenda's wordt dit alleen gevraagd als het adres geen uitsluitsel geeft. Bij een site zoals LinkedIn of X wordt de inlogpagina geopend in de browser van je Machine. Zodra je bent ingelogd, gaat het vanzelf verder. Bij GitHub, WhatsApp en Codex krijg je een code die je moet invoeren. Voor Telegram-chats en Signal-chats krijg je een QR-code om te scannen.

Met **Annuleren** stop je het toevoegen. Ben je weggegaan voordat het klaar was? Open **Koppelingen** opnieuw, op welk apparaat dan ook, en je gaat verder waar je was gebleven. Zodra de bron is gekoppeld, begint je Machine die meteen te lezen en zie je hoe de eerste synchronisatie verloopt.

Op een gehoste Machine kun je hier inloggen bij bronnen waarvoor je zelf een login hebt: Google, Microsoft (Outlook, OneDrive en Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce en Trello.

Kies **Werk** of **Privé** en druk op de inlogknop, bijvoorbeeld **Inloggen met Google**. Je keert terug naar dit formulier, waar je ziet hoe het is gegaan. Ook de codes voor GitHub, WhatsApp, Codex, Telegram-chats en je Android-telefoon verschijnen hier.

Op je eigen computer log je bij dezelfde bronnen in zodra je Machine aan je account is gekoppeld. Druk de eerste keer op **Koppel deze Machine**. Sommige bronnen bieden ook een andere manier, zoals je eigen app of een sleutel.

Met **Opnieuw verbinden** bij een bron, of onder **Wacht op jou**, open je hetzelfde formulier. Op je eigen computer doet `assistant connect` hetzelfde in een terminal.

## Werk of privé

Elke bron is voor werk, voor een bedrijf dat je opgeeft, of voor privé. Je kunt dit wijzigen onder **Details**. **Geschat** betekent dat je Machine dit heeft afgeleid van het adres. To-do's voor werk wachten tot je werkdagen.

Bij e-mail en agenda's van Google en Microsoft wordt de categorie bepaald aan de hand van het adres als dat duidelijk is: een e-maildienst zoals Gmail of Outlook.com betekent Privé, het domein van je team betekent Werk. Is dat niet duidelijk, dan wordt het één keer gevraagd, meteen nadat je bent ingelogd. Met **Wijzigen** stel je de categorie zelf in. Als je e-mail later op de andere categorie wijst, vraagt de to-do **Haal meer uit The Machine** één keer of je die wilt wijzigen.

## Mogelijkheden

Een bron kan signalen binnenbrengen, die to-do's worden, dingen doen voor je to-do's, zoals een document lezen of iets versturen, beantwoorden of wijzigen nadat je toestemming hebt gegeven, of allebei. Als hij beide kan, vind je onder **Details** een schakelaar voor elk: **Brengt signalen binnen** en **Kan dingen doen**. Eén mogelijkheid blijft altijd aan. Wil je beide uitschakelen, koppel de bron dan los. Bij een chat is er alleen **Kan dingen doen**.

Als **Brengt signalen binnen** uitstaat, wordt er niets gesynchroniseerd. Als **Kan dingen doen** uitstaat, leest, schrijft of wijzigt je Machine er niets mee.

## Een bron verwijderen

Open de bron en ga naar **Details**. Kies daarna **Ontkoppelen**. Je Machine stopt met lezen. Alles wat al is binnengebracht, blijft bewaard. Op een gehoste Machine wordt bij bronnen waarvan de login op je instellingenpagina staat (Google, Microsoft, Google Meet, Slack, Zoom, Stripe en Salesforce) **Ontkoppelen ↗** weergegeven. Daarmee open je je instellingenpagina.

Bij **Onlangs ontkoppeld** staan de Google-, Microsoft-, Zoom-, Slack-, Stripe- en Salesforce-accounts die je de afgelopen 30 dagen hebt verwijderd, met het tijdstip. Tot de dienst de verwijdering bevestigt, staat er Pending en blijft je Machine het opnieuw proberen. Een Google-account staat er maar één keer, ook als Google Meet of Docs een eigen login had. Elke bron staat onder de eigen soort: een Google- of Microsoft-account onder **E-mail**, Slack onder **Chat**.

## Opgeslagen logins

Vink bij het inloggen op een site zoals LinkedIn of X **Bewaren voor de volgende keer** aan. De login staat dan onder **Logins**. Als een site je Machine afmeldt, kan hij met één tik weer inloggen. Wachtwoorden blijven versleuteld op je Machine. Met **Vergeten** verwijder je een login.

Een site kan meerdere accounts hebben, bijvoorbeeld **Werk** en **Privé**. **Opslaan als** gebruikt standaard de categorie van de to-do zelf. Met **Andere naam…** geef je de login een eigen naam. Een to-do logt in met het account dat erbij past. Als dat niet duidelijk is, vraagt het dialoogvenster één keer welk account je wilt gebruiken en onthoudt het die keuze voor die to-do.

Onder **Logins** staat elke site één keer, met de accounts eronder. Logins die zijn opgeslagen voordat accounts beschikbaar waren, staan als **Standaard** totdat je daar hun categorie kiest.

Met **Importeren** haal je logins binnen vanuit een wachtwoordmanager: een CSV-export uit 1Password, LastPass, Bitwarden of Chrome, of rechtstreeks uit de opdrachtregelprogramma's van 1Password en LastPass als je daarop bent ingelogd op deze computer. Je vinkt aan welke logins je wilt bewaren. Je Machine logt nooit in bij je wachtwoordmanager en vraagt nooit om het hoofdwachtwoord. Verwijder het exportbestand zodra je klaar bent.

Een opgeslagen login wordt alleen gebruikt voor het bijbehorende webadres: dezelfde site, `https` en poort. Niet voor een adres dat erop lijkt of een ander subdomein.

## Checks

Onder **Checks** zie je hoe je Machine binnenkomende berichten controleert: recente checks en wat elke check heeft gevonden. Zie [Geen nieuwe to-do's](reviews-paused.md).

Elke koppeling heeft in dit gedeelte een eigen artikel, met informatie over wat je Machine leest en wat hij kan versturen.
