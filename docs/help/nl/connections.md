---
title: Koppelingen
area: connections
summary: Je bronnen op één plek: bekijk hoe het ermee gaat, voeg een bron toe of koppel er een los.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 353fdfaa67678a1f
---
## Hoe het ermee gaat

Op het tabblad **Koppelingen** staan je bronnen per soort, met **Logins** en **Checks** onder een streep. Tik op je telefoon op een soort om die te openen en op **Koppelingen** om terug te gaan. Een soort met een bron die op jou wacht, wordt als eerste geopend. Elke bron staat op een rij met de status (Verbonden, Wacht op de eerste synchronisatie, Bezig met automatisch opnieuw verbinden of Heeft je hulp nodig) en wat er onlangs is binnengekomen. Tik erop om de kaart en **Details** te bekijken.

Een mislukte synchronisatie die later is ingehaald, wordt grijs weergegeven. Alleen een mislukte synchronisatie die nog steeds de meest recente is, wordt als probleem getoond, met het tijdstip waarop opnieuw wordt geprobeerd.

De aantallen laten alles zien wat de bron heeft binnengebracht, ook de [geschiedenis](history.md), wat er in de afgelopen 24 uur is binnengekomen en wat nog niet is gecontroleerd. Bij een agenda tellen de afspraken mee.

Elke bron heeft de naam van het account, zoals de dienst die weergeeft: je adres, een X-profiel, een Slack-werkruimte of van wie de Signal- of Telegram-account is. Onder de naam staat eerst **Werk** of **Privé**, plus het adres of de gebruikersnaam als die niet al in de naam staat. Hebben twee bronnen van dezelfde soort dezelfde naam, dan staat er ook bij waaraan je ze herkent, zoals Slack of X, of het adres van de werkruimte.

Bij elke bron staat in één regel wat hij binnenbrengt en, als hij dingen kan doen, dat hij dat alleen doet nadat je op **Versturen** drukt of het goedkeurt.

## Een bron toevoegen

Open een soort (**E-mail**, **Agenda**, **Chat**, **Afspraken**, **Documenten en bestanden**, **Klanten**, **Projecten en code**, **Andere**) en kies een bron onder **Nog een toevoegen**, of onder de lijst als er nog geen bron is gekoppeld. Helemaal onderaan vind je een optie voor andere bronnen: **Andere e-mail** onder E-mail, en **Agendalink (ICS)** en **Andere agenda** onder Agenda. Exchange Server leest afspraken en staat daarom onder Agenda.

**Voorgesteld voor jou** verschijnt bovenaan **Koppelingen** als je Machine een reden ziet om een bron toe te voegen. Die reden staat er in één regel bij, bijvoorbeeld e-mail van Stripe, Zoom-afspraken in je agenda, berichten met links naar Google Docs of een instelling die niet is afgerond. De bron blijft ook in de eigen groep staan, met de markering **Voorgesteld**. Je Machine telt dit op je Machine; er wordt niets naar buiten gestuurd. Een gekoppelde bron wordt nooit voorgesteld.

Microsoft Teams staat er twee keer bij: onder **Chat** voor chats en onder **Afspraken** als **Teams-meetings** voor aantekeningen van vergaderingen. Beide gebruiken dezelfde Microsoft-login. Als je de ene koppelt, is de andere dus ook gekoppeld.

Als je een bron al hebt gekoppeld, staat dat in de lijst met het bijbehorende account. Kies die bron om er nog een toe te voegen. Het formulier geeft dit aan en bevat een link naar de bron die je al hebt.

Vul in wat nodig is, zoals een sleutel of adres. Kies **Werk** met de bedrijfsnaam of **Privé**. Bij e-mail en agenda's wordt hier alleen om gevraagd als het adres het niet al aangeeft. Druk daarna op **Verbinden**. Bij een site zoals LinkedIn of X opent de login in de browser van je Machine. Zodra je bent ingelogd, gaat het vanzelf verder. Bij GitHub, WhatsApp en Codex krijg je een code om in te voeren. Voor Telegram- en Signal-chats krijg je een QR-code om te scannen.

Met **Annuleren** stop je het toevoegen. Ben je weggegaan voordat het klaar was? Open dan **Koppelingen** opnieuw, op welk apparaat dan ook. Je gaat verder waar je was gebleven. Zodra de bron is gekoppeld, begint je Machine hem meteen te lezen en zie je hoe de eerste synchronisatie verloopt.

Op een gehoste Machine kun je hier inloggen bij bronnen met een eigen login: Google, Microsoft (Outlook, OneDrive en Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce en Trello.

Kies **Werk** of **Privé** en druk op de login-knop, zoals **Inloggen met Google**. Je komt terug in dit formulier, waar je ziet hoe het is gegaan. De codes voor GitHub, WhatsApp, Codex, Telegram-chats en je Android-telefoon verschijnen hier ook.

Op je eigen computer kun je bij dezelfde bronnen inloggen zodra je Machine aan je account is gekoppeld. Druk de eerste keer op **Koppel deze Machine**. Sommige bronnen bieden ook een andere manier, zoals je eigen app of een sleutel.

Met **Opnieuw verbinden**, bij een bron of onder **Wacht op jou**, open je hetzelfde formulier. Op je eigen computer doet `assistant connect` hetzelfde in een terminal.

## Werk of privé

Elke bron is werk (voor een bedrijf dat je opgeeft) of privé. Je kunt dit wijzigen onder **Details**. **Geschat** betekent dat je Machine dit heeft afgeleid van het adres. To-do's voor werk wachten tot je werkdagen.

Bij e-mail en agenda's van Google en Microsoft wordt het bepaald aan de hand van het adres als dat duidelijk is: een e-mailprovider zoals Gmail of Outlook.com betekent privé, het domein van je team betekent werk. Is dat niet duidelijk, dan wordt het één keer gevraagd, direct nadat je bent ingelogd. Met **Wijzigen** stel je het zelf in. Als je e-mail later op het andere wijst, vraagt de to-do **Haal meer uit The Machine** één keer of je dit wilt aanpassen.

## Mogelijkheden

Een bron kan signalen binnenbrengen, die worden omgezet in to-do's, dingen doen voor je to-do's (een document lezen, of iets versturen, beantwoorden of wijzigen nadat je het hebt goedgekeurd), of allebei. Als hij beide kan, heeft **Details** voor elk een schakelaar: **Brengt signalen binnen** en **Kan dingen doen**. Eén ervan blijft aan. Als je beide wilt uitschakelen, moet je de bron ontkoppelen. Bij een chat is er alleen **Kan dingen doen**.

Als **Brengt signalen binnen** uitstaat, wordt er niet gesynchroniseerd. Als **Kan dingen doen** uitstaat, leest, schrijft of wijzigt je Machine er nooit iets mee.

## Een bron verwijderen

Open de bron en kies **Details** en daarna **Ontkoppelen**. De bron wordt niet meer gelezen. Wat al is binnengebracht, blijft staan. Op een gehoste Machine heeft een bron waarvan de login op je instellingenpagina staat (Google, Microsoft, Google Meet, Slack, Zoom, Stripe en Salesforce) de optie **Ontkoppelen ↗**. Die opent je instellingenpagina.

Onder **Onlangs ontkoppeld** staan de Google-, Microsoft-, Zoom-, Slack-, Stripe- en Salesforce-accounts die je in de afgelopen 30 dagen hebt verwijderd, met het tijdstip erbij. Tot de dienst dit bevestigt, staat er In behandeling en blijft je Machine het opnieuw proberen. Een Google-account wordt maar één keer weergegeven, ook als Google Meet of Docs een eigen login had. Elk account staat onder de eigen soort: een Google- of Microsoft-account onder **E-mail**, Slack onder **Chat**.

## Opgeslagen logins

Vink bij het inloggen op sites zoals LinkedIn of X **Bewaren voor de volgende keer** aan. De site staat dan onder **Logins**. Als de site je Machine uitlogt, kan die met één tik weer inloggen. Wachtwoorden blijven versleuteld op je Machine. Met **Vergeten** verwijder je een login.

Een site kan meerdere accounts hebben, bijvoorbeeld **Werk** en **Privé**. **Opslaan als** gebruikt standaard de categorie van de to-do. Met **Andere naam…** geef je zelf een naam op. Een to-do logt in met het account dat erbij past. Als dat niet duidelijk is, vraagt het dialoogvenster één keer welk account je wilt gebruiken en onthoudt het je keuze voor die to-do.

Onder **Logins** staat elke site één keer, met de accounts eronder: de gebruikersnaam en een menu met de categorie. Je kunt de categorie daar op elk moment wijzigen. Bij logins die zijn opgeslagen voordat accounts beschikbaar waren, staat **Werk of privé?** totdat je een categorie kiest. Als je de categorie wijzigt, kiest een to-do die de login gebruikte opnieuw een account.

Met **Importeren** importeer je logins uit een wachtwoordmanager. Kies er een:

- **LastPass**, **Bitwarden** of **Google Password Manager**: de exportpagina wordt geopend in de browser van je Machine en verschijnt in het dialoogvenster, net als bij **Doe het** voor een to-do. Log daar in. Je Machine klikt verder naar de export. Je ziet in één regel wat je nog moet doen, zoals je hoofdwachtwoord invoeren. Op een telefoon zoomt het scherm in op het invoerveld. Ziet de pagina er anders uit dan verwacht, dan worden de stappen getoond om het handmatig af te ronden. Je Machine haalt het bestand op, leest het één keer en verwijdert het.
- **1Password**: exporteer een CSV-bestand vanuit de 1Password-app op een computer en kies dat bestand. Als 1Password's `op` is ingelogd op je Machine, leest die de gegevens daar vandaan in plaats daarvan. Dat geldt ook voor LastPass met `lpass`.
- **Uit een exportbestand**: een CSV-bestand van 1Password, LastPass, Bitwarden of Chrome. Verwijder het bestand zodra je klaar bent.

Vink daarna aan welke logins je wilt bewaren. Je Machine logt nooit voor je in bij je wachtwoordmanager, typt of leest nooit je hoofdwachtwoord en laat de pagina nooit aan de assistent zien. Je voert het wachtwoord zelf in op de pagina.

Een opgeslagen login wordt alleen gebruikt op het bijbehorende webadres: dezelfde site, `https` en poort. Niet op een vergelijkbaar adres en niet op een ander subdomein.

## Checks

Onder **Checks** zie je hoe je Machine binnenkomende gegevens leest: recente controles en wat die hebben gevonden. Zie [Geen nieuwe to-do's](reviews-paused.md).

Elke koppeling heeft in dit gedeelte een eigen artikel met wat de koppeling leest en kan versturen.
