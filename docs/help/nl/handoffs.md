---
title: Overdrachten
area: fleet
summary: Deel een to-do met een teamgenoot of draag hem over aan diens Machine via **Overdragen…** op de to-do. Volg later op of neem hem terug.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: d9b21c04fb0d34a6
---
## Een to-do overdragen

1. Open op de to-do **…**, kies **Overdragen…** en selecteer **Een teamgenoot**.
2. Kies wie de to-do krijgt, controleer wat meegaat (× sluit een onderdeel uit) en voeg een notitie toe. Informatie uit een Personal-account of van een ander bedrijf gaat niet mee.
3. Verstuur de to-do. De Machine van diegene laat hem zien als to-do.

De Machine van diegene stuurt een melding naar diens telefoon of Telegram. Is geen van beide ingesteld, dan stuurt de Machine één e-mail met wie de to-do heeft overgedragen, de titel en een link. Zie [Meldingen](notifications.md).

Een Intercom-gesprek gaat ook mee. Als de Machine van diegene dezelfde Intercom-werkruimte leest, opent **Bericht lezen** het gesprek en wordt diens antwoord teruggestuurd naar Intercom. Zo niet, dan bevat de to-do een link naar het gesprek.

Terwijl je wacht, staat op de to-do wat je hebt gevraagd en wanneer ("Gevraagd aan Pat op di 3 nov: …"), maar alleen als dat iets toevoegt aan de titel. De to-do staat onder **Komt later terug**, met de status "Bij Pat · wacht op antwoord" en een datum om op te volgen. Met **Nu opvolgen** maak je een korte herinnering voor Pat die je kunt versturen. Met **Tijd wijzigen** pas je de datum voor opvolging aan.

Kan de Machine van Pat geen melding sturen, dan staat op de to-do: "Pat krijgt geen melding. Laat het Pat weten." Laat het Pat zelf weten. Deze melding verdwijnt zodra Pat meldingen inschakelt.

De to-do komt alleen weer bovenaan te staan als er iets te beslissen is: Pat heeft geantwoord, de to-do geweigerd of afgerond, de overdracht is mislukt of er is een deadline. De datum voor opvolging hangt af van de deadline: een paar uur voor een deadline vandaag, de werkdag ervoor als de deadline binnenkort is, de volgende ochtend bij spoed, en anders over 3 werkdagen.

Als je de to-do weer ziet omdat het tijd is om op te volgen, staat er "Nog bij Pat". Met **Nu opvolgen** maak je op de to-do een korte herinnering voor Pat, op de plek waar je de vraag stelde (Slack, WhatsApp, Telegram of e-mail). Er wordt pas iets verstuurd als je **Versturen** kiest. Daarna wacht de to-do weer op Pat. Als geen van de gekoppelde diensten Pat een bericht kan sturen, wordt de chat geopend en staat daar waarom. **Terugnemen** en **Overdragen aan iemand anders** staan onder **…** en daarna **Overdragen…**.

In de chat van de to-do zie je wanneer die is overgedragen ("Overgedragen aan de Machine van Pat · 14:02") en wat er terugkwam: geaccepteerd, geweigerd (met diens notitie) of afgerond. Is er nog geen antwoord, dan kun je **Als gedaan markeren**, **Snoozen** of **Niet nodig** kiezen. Wil je Pat herinneren of de to-do terugnemen, zeg dat dan in de chat.

Als de overdracht niet is verstuurd, staat dat op de to-do en in de chat. Kies **Opnieuw proberen**.

## Wat de ander ziet

Alleen die to-do: je verzoek, je notitie, de deadline en het contact, plus kopieën van de berichten die meegaan (maximaal drie, zonder bijlagen). Niet je mailbox of je andere to-do's. De ander kiest **Accepteren** of **Weigeren**.

Zodra de ander de to-do accepteert, is het diens to-do. Die van jou is afgerond, of wacht op het resultaat als je een **Klaar als** hebt ingesteld. Jullie werken niet allebei aan dezelfde to-do. Wil je dat iemand ernaar kijkt terwijl de to-do van jou blijft, gebruik dan [Vraag om review](ask-to-review.md).

## Draag de to-do liever aan iemand anders over

Zolang een teamgenoot de to-do heeft, staat dat op één regel ("Bij Pat · wacht op antwoord"). Onder **…** en daarna **Overdragen…** staan **Terugnemen** en **Overdragen aan iemand anders**. Met **Terugnemen** wordt de to-do weer van jou. De Machine van Pat krijgt hiervan bericht en diens antwoord heeft geen invloed meer op de to-do.

Met **Overdragen aan iemand anders** open je het overdrachtsformulier. Je kunt het ook in de chat van de to-do zeggen ("dit moet naar Kim"). Daarna staat er op de to-do: "Nog bij Pat totdat je hem naar Kim stuurt", met **Bekijk overdracht aan** Kim.

Je kunt een to-do maar één keer aan elke teamgenoot overdragen. Zolang Pat de to-do heeft, is Pat opnieuw kiezen in het overdrachtsformulier een manier om op te volgen. Met **Even polsen** maak je dezelfde herinnering, met een regel van jou als je die toevoegt.

**Terugnemen van** Pat staat standaard aan. Zet dit uit als jullie de to-do allebei mogen hebben. Er wordt pas iets verstuurd als je **Overdragen** kiest. De Machine van Pat krijgt bericht en diens kopie van de to-do verdwijnt.

## Als de ander weigert

De ander kan aangeven waarom: de to-do is niet van diegene, is al afgerond of er is deze week geen tijd voor. Kies daarna **Zelf doen**, **Overdragen aan iemand anders** of **Als gedaan markeren**. Hetzelfde geldt als de ander niet op tijd antwoordt. Met **Zelf doen** wordt de to-do weer van jou en komt die onder **Voor jou** te staan.

## Iemand buiten de Network

Kies **Via e-mail**. Je Machine maakt een e-mail klaar die je kunt versturen. Terwijl je typt, worden eerst mensen uit je Fleet voorgesteld en daarna mensen bij je bedrijf. Voeg een taakpagina toe, zodat de ander met één tik kan antwoorden. Zie [Taakpagina's](task-pages.md).

Dit kan alleen voor Work-to-do's. Vink aan wat je wilt meesturen: een paar regels over de to-do, het concept, links en bestanden. Persoonlijke informatie en inhoud die alleen voor jou is, blijven privé. Met **E-mail klaarzetten** zet je de e-mail op de to-do. Lees hem en verstuur hem daarna vanuit je eigen mailbox. Er wordt niets bijgehouden.

Een to-do uit Intercom of Slack heeft geen eigen mailbox. De e-mail wordt daarom verstuurd vanuit je Work-mailbox.

Daarna houdt de to-do de belofte bij totdat de ander antwoordt dat die is nagekomen, of jij de to-do als gedaan markeert. De e-mail eindigt met "Pak dit op in je eigen Machine". Meldt de ander zich via die link aan, dan kan diegene lid worden van je Fleet en wordt de to-do overgedragen aan diens Machine. Zet die regel uit onder Fleet in **Instellingen**.
