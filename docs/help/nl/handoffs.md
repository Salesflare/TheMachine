---
title: Overdrachten
area: fleet
summary: Draag een to-do over aan de Machine van een teamgenoot, met alles wat die nodig heeft. Volg later op of neem de to-do terug.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: acb60a24ef374625
---
## Een to-do overdragen

1. Open bij de to-do **…**, kies **Overdragen…** en selecteer **Een teamgenoot**.
2. Kies aan wie je de to-do wilt overdragen, controleer wat er meegaat (× laat een onderdeel achterwege) en voeg een notitie toe. Niets uit een Personal-account of van een ander bedrijf wordt meegestuurd.
3. Verstuur de overdracht. De Machine van die teamgenoot toont de to-do aan diegene.

De Machine stuurt diegene een melding op de telefoon of via Telegram. Als geen van beide is ingesteld, stuurt de Machine één e-mail met wie de to-do heeft overgedragen, de titel en een link. Bekijk [Meldingen](notifications.md).

Een Intercom-gesprek wordt ook meegestuurd. Als de Machine van die teamgenoot dezelfde Intercom-werkruimte kan lezen, opent **Bericht lezen** het gesprek en komt het antwoord terug in Intercom. Zo niet, dan bevat de to-do een link naar het gesprek.

Terwijl je wacht, staat op de to-do wat je hebt gevraagd en wanneer ("Gevraagd aan Pat op di 3 nov: …"), maar alleen als dat iets toevoegt aan de titel. De to-do staat onder **Komt later terug**, met de status "Bij Pat · wacht op antwoord" en een datum om op te volgen. **Nu opvolgen** maakt een korte herinnering voor Pat die je kunt versturen. Met **Tijd wijzigen** pas je het opvolgmoment aan.

Als de Machine van Pat geen melding kan sturen, staat op de to-do: "Pat krijgt geen melding. Laat het Pat weten." Breng Pat zelf op de hoogte. Deze tekst verdwijnt zodra Pat meldingen inschakelt.

De to-do komt pas weer bovenaan te staan als er iets te beslissen is: Pat heeft geantwoord, de to-do geweigerd of afgerond, de overdracht is mislukt of er is een deadline. Het opvolgmoment hangt af van de deadline: een paar uur als die vandaag is, de werkdag ervoor als die binnenkort is, de volgende ochtend als die urgent is, en anders over 3 werkdagen.

Wanneer de to-do terugkomt om op te volgen, staat er "Nog steeds bij Pat". **Nu opvolgen** maakt een korte herinnering voor Pat op de plek waar je de to-do hebt aangevraagd (Slack, WhatsApp, Telegram of e-mail), in de to-do. Er wordt niets verstuurd totdat je **Versturen** kiest. Daarna wacht de to-do weer op Pat. Als geen van de gekoppelde apps Pat een bericht kan sturen, wordt de chat geopend en staat daar waarom. **Terugnemen** en **Overdragen aan iemand anders** vind je onder **…** en daarna **Overdragen…**.

In de chat van de to-do staat wanneer de overdracht is verstuurd ("Overgedragen aan de Machine van Pat · 14:02") en wat er is teruggekomen: geaccepteerd, geweigerd (met de notitie van Pat) of afgerond. Als Pat nog niet heeft geantwoord, kun je kiezen uit **Markeer als gedaan**, **Snoozen** en **Niet nodig**. Wil je Pat een herinnering sturen of de to-do terugnemen, zeg dat dan in de chat.

Als de overdracht niet is verstuurd, staat dat op de to-do en in de chat, met **Opnieuw proberen**.

## De to-do aan iemand anders overdragen

Zolang een teamgenoot de to-do heeft, staat dat op één regel ("Bij Pat · wacht op antwoord"). Onder **…** en daarna **Overdragen…** vind je **Terugnemen** en **Overdragen aan iemand anders**. Met **Terugnemen** komt de to-do weer bij jou: de Machine van Pat krijgt een melding en een antwoord van Pat heeft daarna geen invloed meer op de to-do.

Met **Overdragen aan iemand anders** open je het overdrachtsformulier. Je kunt het ook in de chat van de to-do zeggen ("deze moet naar Kim"). Dan staat er op de to-do: "Nog steeds bij Pat totdat je hem naar Kim verstuurt", met **Bekijk overdracht aan** Kim.

Een to-do wordt maar één keer aan elke teamgenoot overgedragen. Als Pat de to-do al heeft, is Pat opnieuw kiezen in het overdrachtsformulier een opvolging. **Even polsen** maakt dezelfde herinnering, met een regel van jou als je die toevoegt.

**Terugnemen bij** Pat staat standaard aan. Zet dit uit als je wilt dat jullie de to-do allebei houden. Er wordt niets verstuurd totdat je **Overdragen** kiest. De Machine van Pat krijgt een melding en de kopie van de to-do bij Pat verdwijnt.

## Als ze weigeren

Ze kunnen aangeven waarom: de to-do is niet voor hen, is al gedaan of ze hebben deze week geen tijd. Kies daarna **Zelf doen**, **Overdragen aan iemand anders** of **Markeer als gedaan**. Hetzelfde geldt als ze niet op tijd reageren. Met **Zelf doen** wordt het weer jouw to-do, onder Voor jou.

## Iemand buiten de Network

Kies **Via e-mail**. Je Machine maakt een conceptmail die je zelf kunt versturen. Terwijl je typt, stelt de Machine eerst mensen uit je Fleet voor en daarna mensen van je bedrijf. Voeg een taakpagina toe, zodat ze met één tik kunnen reageren. Bekijk [Taakpagina's](task-pages.md).

Dit werkt alleen voor Work-to-do's. Vink aan wat meegaat: een paar regels over de to-do, het concept, links en bestanden. Inhoud uit Personal en Alleen voor jou wordt niet meegestuurd. Met **E-mail klaarzetten** zet je de e-mail op de to-do. Lees hem door en verstuur hem vanuit je eigen mailbox. Er wordt niets bijgehouden.

Een to-do uit Intercom of Slack heeft geen eigen mailbox. Daarom wordt de e-mail verstuurd vanuit je Work-mailbox.

Daarna houdt de to-do de belofte bij totdat diegene antwoordt dat de taak is afgerond, of totdat je de to-do als gedaan markeert. De e-mail eindigt met "Neem dit op je in je eigen Machine". Als diegene zich via die link aanmeldt, kan diegene lid worden van je Fleet en wordt de to-do verplaatst naar diens Machine. Je kunt die regel uitschakelen in **Instellingen**, onder Fleet.
