---
title: Geen nieuwe to-do's
area: troubleshooting
summary: Checks staan uit, wachten of zijn gestopt vanwege de gebruikslimiet van je model. Zo zie je wat er aan de hand is en wat je kunt doen.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: d8a15909ab8164e8
---
To-do's komen van checks: je Machine bekijkt ongeveer elke 15 minuten wat er is binnengekomen.

## Net aangemeld

Op een nieuwe gehoste Machine starten checks vanzelf zodra je AI en mail zijn gekoppeld. Terwijl je Machine je mail leest, staat er bij To-do's: "Je mail wordt gelezen. Je eerste to-do's verschijnen over een paar minuten." Zodra hij weet hoeveel mail er is, geeft hij een geschatte tijd: "Je eerste to-do's verschijnen over ongeveer 10 min." Als er nog iets moet gebeuren, staat dat bij **Wacht op jou**, bijvoorbeeld **Mail koppelen**, met een link naar die stap.

Terwijl hij leest, zie je bij To-do's hoever hij is ("20 van 132 berichten gelezen. De volgende 40 worden gelezen…"), een paar mensen en organisaties die hij is tegengekomen en je eerste to-do zodra die klaar is. Het aantal telt de berichten die hij helemaal heeft gelezen. De voortgangsbalk loopt door terwijl hij de volgende berichten leest. De namen komen uit je eigen mail en alleen jij ziet ze.

Als de eerste controle niets voor je oplevert, staat er wat hij heeft gelezen en krijg je suggesties voor vervolgstappen, zoals een dienst koppelen waarvan je vaak mail krijgt of vragen wat er deze week is veranderd.

## Checks staan uit

Bovenaan To-do's staat: "Checks staan uit, dus er komen nog geen to-do's binnen." Op een gehoste Machine druk je op **Checks aanzetten**. Op je eigen computer voer je `./install.sh --activate` uit.

## De limiet van je model

Om ruimte over te houden voor je eigen chats, pauzeren checks wanneer je ongeveer 65% van de limiet voor 5 uur van je AI-abonnement hebt gebruikt, of 90% van de weeklimiet. Met een back-upmodel op een ander abonnement wachten checks niet. Zie [Model](model.md).

Terwijl checks wachten, staat bovenaan het dashboard tot wanneer, bijvoorbeeld: "Checks wachten tot 07:15 om je ChatGPT-week te sparen." Met **Nu checken** start je toch een check. Je limieten vind je onder **Instellingen**, **Model**.

Er gaat niets verloren: binnengekomen berichten worden gecontroleerd zodra dat weer kan. Na lang wachten worden recente berichten van mensen als eerste gecontroleerd. Bij elke check wordt ook een deel van de oudste berichten verwerkt.

Tot alles is bijgewerkt, verschijnen nieuwe to-do's zonder concept, zodat je abonnement eerst wordt gebruikt voor het controleren van je berichten. De concepten volgen later en urgente to-do's hoeven daar niet op te wachten. Druk op **Doe het** om er meteen een te krijgen.

## 's Nachts

Van 00:00 tot 06:30 pauzeren checks en wachten nieuwe berichten. Om 06:30 worden ze samen gecontroleerd, vóór je ochtendoverzicht. Bij **Checks** staat: "Gepauzeerd voor de nacht, wordt om 06:30 bijgewerkt". Gebruik de app, schrijf in de chat of tik op een to-do. Dan worden checks weer uitgevoerd, totdat je een uur niet actief bent geweest. Met **Nu checken** start je meteen een check.

## Een run is mislukt

Onder **Koppelingen**, **Checks** zie je bij **Recente runs** elke run. Een mislukte run wordt vanzelf opnieuw geprobeerd. Als je AI niet meer reageert, bijvoorbeeld omdat je login is verlopen, log je opnieuw in onder **Instellingen**, **Model**. Checks worden meteen daarna hervat.

Bij een run die is gestopt vanwege de gebruikslimiet van je AI-abonnement staat **De gebruikslimiet van AI is bereikt.** en wanneer de limiet wordt opgeheven. Dat is een pauze, geen fout: de berichten wachten en worden gecontroleerd zodra de limiet is gereset. Er komt niets in [foutrapporten](error-reports.md).

## Opzijgezet

Als een check een bericht twee keer uitstelt, wordt het opzijgezet. Onder **Koppelingen**, **Checks** zie je hoeveel berichten dat zijn. **Opzijgezet** toont de berichten.

Een bericht waardoor elke check mislukt terwijl je AI wel werkt, wordt op dezelfde manier opzijgezet, zodat de rest wel wordt gecontroleerd.

Een bericht van iemand die je schrijft, iemand die je kent of een klant wordt ongeveer 3 dagen na binnenkomst nog een keer gecontroleerd. Die check maakt er een to-do van of sluit het bericht af. Wat je hebt afgewezen of gesnoozed, blijft zo.
