---
title: Koppelingen
area: connections
summary: Je bronnen op één plek: hoe het met elke bron gaat, een nieuwe toevoegen of er een ontkoppelen.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 1ca62ab8f65b77ff
---
## Hoe het ermee gaat

Het tabblad **Koppelingen** toont je bronnen per soort (**E-mail**, **Agenda**, **Chat** en meer), met **Logins** en **Checks** onder een lijn. Op een telefoon tik je op een soort om ze te openen en op **Koppelingen** om terug te gaan. Elke bron is een rij; tik erop voor haar kaart. Elke bron zegt hoe het ermee gaat: Verbonden, Wacht op eerste sync, Verbindt automatisch opnieuw, of Heeft je hulp nodig. Open **Details** voor **Recente syncs**, waar de sync in gewone woorden staat (zoals "Bij" of "Eerste keer lezen"), en wat je moet doen.

Een mislukte sync die een latere sync heeft goedgemaakt staat in grijs; alleen een mislukking die nog de laatste is, staat als probleem, met wanneer hij opnieuw probeert.

De tellers tonen alles wat de bron binnenbracht, ook de [geschiedenis](history.md), hoeveel er de laatste 24 uur bij kwam en wat nog niet is gecheckt. Een agenda telt afspraken: alle, die van de volgende 7 dagen en de laatste 24 uur.

Elke bron heet naar haar account, zoals de dienst het noemt: je adres, een X-profiel, een Slack-workspace, of van wie de Signal of Telegram is. Daaronder: **Werk** of **Privé**, met het adres of de handle als de naam dat nog niet zegt. Hebben twee bronnen op één tabblad dezelfde naam, dan zegt elk ook wat ze onderscheidt, zoals Slack of X, of het adres van de workspace.

Onder de status zegt elke bron in één regel wat ze binnenbrengt en, als ze iets kan doen, dat ze dat pas doet nadat je op **Versturen** drukt of het goedkeurt.

## Een bron toevoegen

Open de soort en kies een bron onder **Nog een toevoegen**, of onder de lijst als er nog geen gekoppeld is. Hij vraagt wat hij nodig heeft, één vraag tegelijk. **Annuleren** stopt het toevoegen. Weggegaan voor het klaar was? Open **Koppelingen** opnieuw, op eender welk toestel, en je gaat verder bij dezelfde stap. Zodra hij gekoppeld is, begint je Machine hem meteen te lezen en opent hij de nieuwe kaart, die toont hoe de eerste sync verloopt. Op een gehoste Machine log je hier in bij Google, Microsoft, Microsoft OneDrive, Zoom, Stripe en Intercom: kies **Werk** of **Privé**, log in en je komt terug in dit formulier, dat toont hoe het koppelen gaat. GitHub, WhatsApp, Codex, Telegram-chats en je Android-telefoon tonen hun code meteen in dit formulier.

Een bron die je al koppelde zegt dat in de lijst, met het account. Kies hem om er nog een naast toe te voegen: het formulier zegt dat en linkt naar de koppeling die je al hebt.

De lijst is gegroepeerd (**E-mail**, **Agenda**, **Chat**, **Afspraken**, **Documenten en bestanden**, **Klanten**, **Projecten en code**, **Andere**), van A tot Z per groep. Een verzamelbron zoals **Andere e-mail** staat als laatste in zijn groep.

**Voorgesteld voor jou** staat bovenaan als je Machine een reden ziet voor een bron, met die reden op één regel: mails van Stripe, Zoom-meetings in je agenda, berichten die naar Google Docs linken, of instellen dat niet is afgerond. De bron staat ook in zijn eigen groep, met het label **Voorgesteld**. Hij telt dat op je Machine; er gaat niets weg. Een gekoppelde bron wordt nooit voorgesteld.

Microsoft Teams staat er twee keer: onder **Chat** voor de chats en onder **Afspraken** als **Teams-meetings** voor de meetingnotities. Beide gebruiken dezelfde Microsoft-aanmelding, dus de ene koppelen koppelt ook de andere.

**Opnieuw verbinden** op een bron en in **Wacht op jou** opent hetzelfde formulier. Op je eigen computer doet `assistant connect` hetzelfde in een terminal.

## Werk of privé

Elke bron telt als werk (voor een bedrijf dat je noemt) of als privé. Wijzig het onder **Details**. Er staat alleen **Geraden** als je Machine het uit het adres afleidde; zodra je zelf kiest, blijft het jouw keuze. Werk-to-do's wachten op je werkdagen.

Mail en agenda van Google en Microsoft volgen hun adres als dat duidelijk is: een mailprovider zoals Gmail of Outlook.com is Privé, het domein van je team is Werk. Anders vraagt hij het één keer, meteen na het inloggen. Met **Wijzigen** stel je het zelf in. Zegt de mail daarna het omgekeerde, dan vraagt de to-do **Haal meer uit The Machine** één keer of je het wilt wijzigen.

## Vaardigheden

Een bron kan signalen binnenbrengen (wat binnenkomt wordt to-do's), dingen doen voor je to-do's (een document lezen als er een nodig is, of iets versturen, beantwoorden of wijzigen na je OK), of allebei. Met allebei heeft **Details** een schakelaar voor elk: **Brengt signalen binnen** en **Kan dingen doen**. Eén blijft aan. Wil je allebei stoppen, ontkoppel de bron dan. De antwoorden van een chat gaan over wat die binnenbrengt, dus een chat heeft alleen **Kan dingen doen**.

Met **Brengt signalen binnen** uit synchroniseert de bron niet en toont de kaart geen aantallen. Met **Kan dingen doen** uit leest je Machine er nooit iets mee op verzoek, schrijft er geen concept mee en wijzigt er niets mee. Bronnen van vroeger hebben allebei aan.

## Een bron verwijderen

Open de bron, **Details**, dan **Ontkoppelen**. Hij stopt met lezen. Wat al binnengehaald is, blijft. Op een gehoste Machine tonen Google, Microsoft, Microsoft OneDrive, Zoom en Stripe **Ontkoppelen ↗**, dat je setuppagina opent.

**Onlangs ontkoppeld** toont de accounts bij Google, Microsoft, Zoom, Slack, Stripe en Salesforce die je de laatste 30 dagen verwijderd hebt, en wanneer. Een Google-account staat er één keer, ook als Google Meet of Docs een eigen login hadden. Elk staat onder zijn eigen soort: een Google- of Microsoft-account onder **E-mail**, Slack onder **Chat**.

## Opgeslagen logins

Sites die de browser van je Machine gebruikt, zoals LinkedIn of X, kunnen een login bewaren: vink **Bewaren voor de volgende keer** aan als je inlogt. Dan toont **Logins** ze. Als een site je Machine uitlogt, logt hij met één tik opnieuw in. Wachtwoorden blijven versleuteld op je Machine. **Vergeten** verwijdert er een.

## Checks

**Checks** toont hoe je Machine leest wat er binnenkomt: recente runs, en wat elke run vond. Zie [Geen nieuwe to-do's](reviews-paused.md).

Elke koppeling heeft een eigen artikel in deze sectie, met wat ze leest en wat ze kan versturen.
