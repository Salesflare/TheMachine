---
title: Koppelingen
area: connections
summary: Al je bronnen op één plek: bekijk de status, voeg een bron toe of koppel er een los.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 809547189ccfa026
---
## Status bekijken

Op het tabblad **Koppelingen** staan je bronnen per soort, met **Logins** en **Checks** onder een scheidingslijn. Tik op je telefoon op een soort om die te openen en op **Koppelingen** om terug te gaan. Een soort met een bron die op jou wacht, wordt als eerste geopend. Elke bron staat op een eigen regel: de status (Verbonden, Wacht op eerste synchronisatie, Wordt automatisch opnieuw verbonden of Heeft je hulp nodig) en wat er onlangs is binnengekomen. Tik erop voor de kaart en **Details**.

Een mislukte synchronisatie die door een latere is ingehaald, wordt grijs weergegeven. Alleen een mislukte synchronisatie die nog steeds de meest recente is, wordt als probleem weergegeven, met het tijdstip waarop het opnieuw probeert.

De aantallen tonen alles wat de bron heeft binnengebracht, ook de [geschiedenis](history.md), wat er de afgelopen 24 uur is binnengekomen en wat nog niet is gecontroleerd. Bij een agenda tellen de aantallen afspraken.

Elke bron heeft de naam van het account, zoals de dienst die weergeeft: je e-mailadres, een X-profiel, een Slack-werkruimte of van wie de Signal- of Telegram-account is. Onder de naam staat eerst **Werk** of **Privé**, plus het adres of de gebruikersnaam als die nog niet in de naam staat. Als twee bronnen van hetzelfde type dezelfde naam hebben, staat er ook bij wat ze onderscheidt, zoals Slack of X, of het adres van de werkruimte.

Bij elke bron staat ook in één regel wat die binnenbrengt en, als de bron acties kan uitvoeren, dat die dat alleen doet nadat je op **Versturen** drukt of de actie goedkeurt.

## Een bron toevoegen

Open een soort (**E-mail**, **Agenda**, **Chat**, **Afspraken**, **Documenten en bestanden**, **Klanten**, **Projecten en code**, **Andere**) en kies een bron onder **Nog een toevoegen**, of onder de lijst als er nog geen bron is verbonden. Onderaan staan algemene opties: **Andere e-mail** onder E-mail, **Agendalink (ICS)** en **Andere agenda** onder Agenda. Exchange Server haalt afspraken op en staat daarom onder Agenda.

**Voorgesteld voor jou** staat bovenaan **Koppelingen** als je Machine een reden ziet om een bron toe te voegen. Die reden staat er in één regel bij: e-mail van Stripe, Zoom-afspraken in je agenda, berichten met links naar Google Docs of een installatie die niet is voltooid. De bron blijft ook in de eigen groep staan, met het label **Voorgesteld**. Deze suggesties worden op je Machine geteld; er wordt niets van je Machine verstuurd. Een verbonden bron wordt nooit voorgesteld.

Microsoft Teams staat twee keer in de lijst: onder **Chat** voor de chats en onder **Afspraken** als **Teams-meetings** voor de aantekeningen van vergaderingen. Beide gebruiken dezelfde Microsoft-login, dus als je de ene verbindt, wordt de andere ook verbonden.

Als je een bron al hebt verbonden, staat dat in de lijst, met het bijbehorende account. Kies die bron om er nog een toe te voegen: het formulier vermeldt dat en linkt naar de bron die je al hebt.

Vul in wat nodig is, zoals een sleutel of adres, kies **Werk** met de naam van je bedrijf of **Privé** en druk op **Verbinden**. Bij een site als LinkedIn of X wordt de login geopend in de browser van je Machine. Daarna gaat het vanzelf verder. GitHub, WhatsApp en Codex tonen een code die je moet invoeren. Telegram-chats en Signal-chats tonen een QR-code om te scannen.

Met **Annuleren** stop je het toevoegen. Ben je weggegaan voordat het klaar was? Open **Koppelingen** opnieuw, op welk apparaat dan ook, en je gaat verder waar je was gebleven. Zodra de bron is verbonden, begint je Machine die meteen te lezen en zie je hoe de eerste synchronisatie verloopt.

Op een gehoste Machine kun je hier inloggen bij bronnen met een eigen login: Google, Microsoft (Outlook, OneDrive en Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce en Trello.

Kies **Werk** of **Privé** en druk op de login-knop, zoals **Inloggen met Google**. Je komt terug bij dit formulier, waar je ziet hoe het is gegaan. De codes voor GitHub, WhatsApp, Codex, Telegram-chats en je Android-telefoon verschijnen hier ook.

Op je eigen computer log je bij dezelfde bronnen in zodra je Machine aan je account is gekoppeld. Druk de eerste keer op **Koppel deze Machine**. Sommige bronnen bieden ook een andere manier, zoals je eigen app of een sleutel.

Met **Opnieuw verbinden** bij een bron en in **Wacht op jou** open je hetzelfde formulier. Op je eigen computer doet `assistant connect` hetzelfde in een terminal.

## Werk of privé

Elke bron is werkgerelateerd, voor een bedrijf dat je opgeeft, of privé. Je kunt dit wijzigen onder **Details**. **Geschat** betekent dat je Machine dit heeft afgeleid van het adres. Werkgerelateerde to-do's wachten tot je werkdagen.

Bij e-mail en agenda's van Google en Microsoft wordt dit afgeleid van het adres als dat duidelijk is: een e-mailprovider zoals Gmail of Outlook.com betekent Privé, het domein van je team betekent Werk. Anders wordt er één keer naar gevraagd, direct nadat je bent ingelogd. Met **Wijzigen** stel je het zelf in. Als later uit je e-mail blijkt dat de andere optie klopt, vraagt de to-do **Haal meer uit The Machine** één keer of je dit wilt wijzigen.

## Mogelijkheden

Een bron kan signalen binnenbrengen, waarvan to-do's worden gemaakt, dingen doen voor je to-do's, zoals een document lezen of iets versturen, beantwoorden of wijzigen nadat je akkoord hebt gegeven, of beide. Als de bron beide kan, kun je onder **Details** elk van de opties apart in- of uitschakelen: **Brengt signalen binnen** en **Kan dingen doen**. Eén optie blijft altijd aan. Als je beide wilt uitschakelen, koppel je de bron los. Bij een chat is alleen **Kan dingen doen** beschikbaar.

Als **Brengt signalen binnen** uitstaat, wordt de bron niet gesynchroniseerd. Als **Kan dingen doen** uitstaat, leest, schrijft of wijzigt je Machine er nooit iets mee.

## Een bron verwijderen

Open de bron, ga naar **Details** en kies **Ontkoppelen**. De bron wordt niet meer gelezen. Alles wat al is binnengebracht, blijft staan. Op een gehoste Machine wordt bij bronnen waarvan de login op je instelpagina wordt beheerd (Google, Microsoft, Google Meet, Slack, Zoom, Stripe en Salesforce) **Ontkoppelen ↗** weergegeven. Daarmee open je je instelpagina.

Onder **Onlangs ontkoppeld** staan de Google-, Microsoft-, Zoom-, Slack-, Stripe- en Salesforce-accounts die je de afgelopen 30 dagen hebt verwijderd, en wanneer je ze hebt verwijderd. Totdat de dienst dit bevestigt, staat er In behandeling en blijft de Machine het proberen. Een Google-account wordt maar één keer getoond, ook als Google Meet of Docs een eigen login had. Elk account staat onder het eigen type: een Google- of Microsoft-account onder **E-mail**, Slack onder **Chat**.

## Opgeslagen logins

Vink bij het inloggen op sites zoals LinkedIn of X **Bewaren voor de volgende keer** aan. De logins staan dan onder **Logins**. Als een site je Machine uitlogt, kan die met één tik weer inloggen. Wachtwoorden blijven versleuteld op je Machine. Met **Vergeten** verwijder je een login.

Een site kan meerdere accounts hebben, bijvoorbeeld **Werk** en **Privé**. **Opslaan als** begint met de optie die bij de to-do zelf hoort. Met **Andere naam…** geef je die een eigen naam. Een to-do logt in met het account dat erbij past. Als dat niet duidelijk is, vraagt het dialoogvenster één keer welk account je wilt gebruiken. Dat wordt onthouden voor die to-do.

Onder **Logins** staat elke site één keer, met de accounts eronder: de gebruikersnaam en een menu met de bijbehorende optie. Je kunt die optie daar altijd wijzigen. Bij logins die zijn opgeslagen voordat accounts beschikbaar waren, staat **Werk of privé?** totdat je een optie kiest. Een to-do die een login gebruikte, kiest opnieuw een account nadat je de optie ervan wijzigt.

Met **Importeren** importeer je logins vanuit een wachtwoordmanager. Kies een optie:

- **LastPass**, **Bitwarden** of **Google Password Manager**: de exportpagina wordt geopend in de browser van je Machine. Log daar in en exporteer je gegevens. De stappen staan ernaast. Je Machine haalt het bestand op, leest het één keer en verwijdert het daarna.
- **1Password**: exporteer een CSV-bestand vanuit de 1Password-app op een computer en kies dat bestand. Als `op` van 1Password is ingelogd op je Machine, leest die de gegevens daarvandaan. Dat geldt ook voor `lpass` van LastPass.
- **Uit een exportbestand**: een CSV-bestand van 1Password, LastPass, Bitwarden of Chrome. Verwijder het bestand zodra je klaar bent.

Vink daarna aan welke logins je wilt bewaren. Je Machine logt nooit voor je in bij je wachtwoordmanager en vraagt nooit om het hoofdwachtwoord. Je voert dat zelf in op de pagina.

Een opgeslagen login wordt alleen gebruikt op het bijbehorende webadres: dezelfde site, `https` en poort. Niet op een adres dat erop lijkt en ook niet op een ander subdomein.

## Checks

Onder **Checks** zie je hoe je Machine binnenkomende gegevens leest: recente controles en wat er bij elke controle is gevonden. Zie [Geen nieuwe to-do's](reviews-paused.md).

Elke koppeling heeft een eigen artikel in dit gedeelte, met wat de koppeling leest en wat die kan versturen.
