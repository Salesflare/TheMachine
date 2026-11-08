---
title: Koppelingen
area: connections
summary: Je bronnen op één plek: hoe het met elke bron gaat, een nieuwe toevoegen of er een ontkoppelen.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
---
## Hoe het ermee gaat

Het tabblad **Koppelingen** groepeert je bronnen in **Mail en agenda**, **Chat** en **Andere bronnen**. Elke bron zegt hoe het ermee gaat: Verbonden, Wacht op eerste sync, Verbindt automatisch opnieuw, of Heeft je hulp nodig. Open **Details** voor **Recente syncs**, waar de sync in gewone woorden staat (zoals "Bij" of "Eerste keer lezen"), en wat je moet doen.

De tellers tonen wat de bron binnenbracht, hoeveel er de laatste 24 uur bij kwam en wat nog niet is gecheckt. Een agenda telt afspraken: alle, die van de volgende 7 dagen en de laatste 24 uur.

Onder de status zegt elke bron in één regel wat ze binnenbrengt en, als ze iets kan doen, dat ze dat pas doet nadat je op **Versturen** drukt of het goedkeurt.

## Een bron toevoegen

Open **+ Toevoegen** en kies een bron. Hij vraagt wat hij nodig heeft, één vraag tegelijk. **Annuleren** stopt het toevoegen. Weggegaan voor het klaar was? Open **Koppelingen** opnieuw, op eender welk toestel, en je gaat verder bij dezelfde stap. Zodra hij gekoppeld is, herstart je Machine om hem te gaan lezen, en opent dan de nieuwe kaart, die toont hoe de eerste sync verloopt. Op een gehoste Machine log je hier in bij Google, Microsoft, Microsoft OneDrive, Zoom, Stripe en Intercom: kies **Werk** of **Privé**, log in en je komt terug in dit formulier, dat toont hoe het koppelen gaat. GitHub, WhatsApp, Codex, Telegram-chats en je Android-telefoon tonen hun code meteen in dit formulier.

De lijst is gegroepeerd (**Mail en agenda**, **Chat**, **Afspraken**, **Documenten en bestanden**, **Klanten**, **Projecten en code**, **Andere**), van A tot Z per groep.

**Voorgesteld voor jou** staat bovenaan als je Machine een reden ziet voor een bron, met die reden op één regel: mails van Stripe, Zoom-meetings in je agenda, berichten die naar Google Docs linken, of instellen dat niet is afgerond. Hij telt dat op je Machine; er gaat niets weg. Geen reden, geen sectie. Een gekoppelde bron wordt nooit voorgesteld.

**Opnieuw verbinden** op een bron en in **Wacht op jou** opent hetzelfde formulier. Op je eigen computer doet `assistant connect` hetzelfde in een terminal.

## Werk of privé

Elke bron telt als werk (voor een bedrijf dat je noemt) of als privé. Wijzig het onder **Details**. Er staat alleen **Geraden** als je Machine het uit het adres afleidde; zodra je zelf kiest, blijft het jouw keuze. Werk-to-do's wachten op je werkdagen.

## Vaardigheden

Een bron kan signalen binnenbrengen (wat binnenkomt wordt to-do's), dingen doen voor je to-do's (een document lezen als er een nodig is, of iets versturen, beantwoorden of wijzigen na je OK), of allebei. Met allebei heeft **Details** een schakelaar voor elk: **Brengt signalen binnen** en **Kan dingen doen**. Eén blijft aan. Wil je allebei stoppen, ontkoppel de bron dan. De antwoorden van een chat gaan over wat die binnenbrengt, dus een chat heeft alleen **Kan dingen doen**.

Met **Brengt signalen binnen** uit synchroniseert de bron niet en toont de kaart geen aantallen. Met **Kan dingen doen** uit leest je Machine er nooit iets mee op verzoek, schrijft er geen concept mee en wijzigt er niets mee. Bronnen van vroeger hebben allebei aan.

## Een bron verwijderen

Open de bron, **Details**, dan **Ontkoppelen**. Hij stopt met lezen. Wat al binnengehaald is, blijft. Op een gehoste Machine tonen Google, Microsoft, Microsoft OneDrive, Zoom en Stripe **Ontkoppelen ↗**, dat je setuppagina opent.

**Onlangs ontkoppeld** toont de logins bij Google, Microsoft en Zoom die je verwijderd hebt. **Verwijderd, bevestigd** betekent dat Google het uitloggen bevestigd heeft, of voor Microsoft en Zoom dat er geen kopie meer over is. **In behandeling** zegt waarom, en je Machine blijft het proberen.

## Opgeslagen logins

Sites die de browser van je Machine gebruikt, zoals LinkedIn of X, kunnen een login bewaren: vink **Bewaren voor de volgende keer** aan als je inlogt. Dan toont **Logins** ze. Als een site je Machine uitlogt, logt hij met één tik opnieuw in. Wachtwoorden blijven versleuteld op je Machine. **Vergeten** verwijdert er een.

## Checks

**Checks** toont hoe je Machine leest wat er binnenkomt: recente runs, en wat elke run vond. Zie [Geen nieuwe to-do's](reviews-paused.md).

Elke koppeling heeft een eigen artikel in deze sectie, met wat ze leest en wat ze kan versturen.
