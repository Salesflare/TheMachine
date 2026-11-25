---
title: Geen nieuwe to-do's
area: troubleshooting
summary: Checks staan uit, wachten of zijn gestopt door de gebruikslimiet van je model. Zo zie je wat er aan de hand is en wat je kunt doen.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: 40617b8ac692660b
---
To-do's komen uit checks: je Machine bekijkt wat er in ongeveer 15 minuten is binnengekomen.

## Net aangemeld

Op een nieuwe gehoste Machine starten checks vanzelf zodra je AI en mail zijn gekoppeld. Terwijl je Machine je mail leest, staat er bij To-do's: "Je mail wordt gelezen. Je eerste to-do's verschijnen over een paar minuten." Zodra duidelijk is hoeveel mail er is, staat er ongeveer hoelang het duurt: "Je eerste to-do's verschijnen over ongeveer 10 min." Ontbreekt er een stap, dan noemt **Wacht op jou** welke stap dat is, bijvoorbeeld **Mail koppelen**, met een link naar die stap.

Terwijl je Machine leest, zie je bij To-do's hoe ver hij is ("20 van de 132 berichten gelezen. De volgende 40 worden gelezen…"), een paar mensen en organisaties die hij is tegengekomen en je eerste to-do zodra die klaar is. Het getal telt de berichten die hij helemaal heeft gelezen; de voortgangsbalk loopt door terwijl hij de volgende berichten leest. De namen komen uit je eigen mail en zijn alleen voor jou zichtbaar.

Vindt de eerste controle niets voor je, dan staat er wat er is gelezen en krijg je suggesties voor vervolgstappen, zoals een dienst koppelen waarvan je vaak mail krijgt of vragen wat er deze week is veranderd.

## Checks staan uit

Bovenaan To-do's staat: "Checks staan uit. Er komen dus nog geen to-do's binnen." Druk op een gehoste Machine op **Checks aanzetten**. Voer op je eigen computer `./install.sh --activate` uit.

## De limiet van je model

Om ruimte over te houden voor je eigen chats, pauzeren checks wanneer je ongeveer 65% van de 5-uurslimiet en 90% van de weeklimiet van je AI-abonnement hebt gebruikt. Met een back-upmodel op een ander abonnement hoeven checks niet te wachten. Bekijk [Model](model.md).

Terwijl checks wachten, staat bovenaan het dashboard tot wanneer, bijvoorbeeld: "Checks wachten tot 07:15, zodat je je ChatGPT-weeklimiet niet opgebruikt." Met **Nu checken** start je toch een check. Bij **Instellingen**, **Model** zie je je limieten.

Er gaat niets verloren: wat er is binnengekomen, wordt gecontroleerd zodra dat kan. Na lang wachten krijgen recente berichten van mensen voorrang, en een deel van elke check werkt de oudste berichten af.

Tot alles is bijgewerkt, komen nieuwe to-do's binnen zonder concept, zodat je AI-budget eerst naar je berichten gaat. De concepten volgen later en urgente berichten wachten niet. Druk op **Doe het** om er nu een te krijgen.

## 's Nachts

Van 00:00 tot 06:30 pauzeren checks en wachten nieuwe berichten. Om 06:30 worden ze samen gecontroleerd, voordat je ochtendoverzicht verschijnt. Bij **Checks** staat: "Nachtpauze. De achterstand wordt vanaf 06:30 ingehaald." Gebruik de app, schrijf in de chat of tik op een to-do. Checks worden dan weer uitgevoerd totdat je een uur inactief bent geweest. Met **Nu checken** wordt meteen gecontroleerd.

## Een run is mislukt

Bij **Connections**, **Checks** toont **Recente runs** elke run. Een mislukte run wordt vanzelf opnieuw geprobeerd.

Bij een run die is gestopt omdat de gebruikslimiet van je AI-abonnement is bereikt, staat **De gebruikslimiet van AI is bereikt.** en wanneer de limiet weer wordt opgeheven. Dat is een pauze, geen fout: de berichten wachten en worden na de reset gecontroleerd. Er komt niets in [foutrapporten](error-reports.md).

## Opzijgezet

Als een check een bericht twee keer opzijzet, wordt het apart gezet. Bij **Connections**, **Checks** zie je hoeveel berichten dat zijn; **Opzijgezet** toont ze. Een bericht van iemand die je mailt, iemand die je kent of een klant wordt ongeveer 3 dagen na binnenkomst nog één keer gecontroleerd. Die controle maakt er een to-do van of sluit het bericht af. Wat je hebt afgewezen of gesnoozed, blijft zo.
