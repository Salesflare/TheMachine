---
title: Geen nieuwe to-do's
area: troubleshooting
summary: Checks staan uit, wachten of zijn gestopt vanwege de gebruikslimiet van je model. Zo herken je dat en weet je wat je kunt doen.
covers: 
code: dashboard.html, assistant.py
order: 3
translated: d265e540d9ecef0e
---
To-do's komen voort uit checks: je Machine bekijkt wat er in ongeveer 15 minuten is binnengekomen.

## Net aangemeld

Op een nieuwe gehoste Machine starten checks vanzelf zodra je AI en mail zijn gekoppeld. Terwijl je Machine je mail leest, staat er bij To-do's: "Je mail wordt gelezen. Je eerste to-do's verschijnen over een paar minuten." Zodra hij weet hoeveel mail er is, geeft hij aan hoe lang het ongeveer duurt: "Je eerste to-do's verschijnen over ongeveer 10 min." Als er een stap ontbreekt, vertelt **Wacht op jou** welke stap dat is, zoals **Mail koppelen**, met een link naar die stap.

Terwijl hij leest, laat To-do's zien hoever hij is ("20 van de 132 berichten gelezen. De volgende 40 worden gelezen…"), een paar mensen en organisaties die hij is tegengekomen en je eerste to-do zodra die klaar is. Het getal telt de berichten die hij helemaal heeft gelezen. De balk blijft bewegen terwijl hij de volgende berichten leest. De namen komen uit je eigen mail en alleen jij ziet ze.

Als de eerste controle niets voor je oplevert, vertelt hij wat hij heeft gelezen en stelt hij vervolgstappen voor, zoals een dienst koppelen waarvan je vaak mail krijgt of vragen wat er deze week is veranderd.

## Checks staan uit

Bovenaan To-do's staat: "Checks staan uit, dus er komen nog geen to-do's binnen." Druk op een gehoste Machine op **Checks aanzetten**. Voer op je eigen computer `./install.sh --activate` uit.

## De limiet van je model

Om ruimte te houden voor je eigen chats, worden checks gepauzeerd bij ongeveer 65% van de limiet voor 5 uur van je AI-abonnement en 90% van de wekelijkse limiet. Met een back-upmodel op een ander abonnement hoeven checks niet te wachten. Zie [Model](model.md).

Terwijl checks wachten, staat bovenaan het dashboard tot wanneer, bijvoorbeeld: "Checks wachten tot 07:15 om je ChatGPT-week te sparen." Met **Nu checken** start je toch een check. Bij **Instellingen**, **Model** zie je je limieten.

Er gaat niets verloren: binnengekomen berichten worden gecheckt zodra dat kan.

## 's Nachts

Van 00:00 tot 06:30 worden checks gepauzeerd en wachten nieuwe berichten. Om 06:30 worden ze samen gecheckt, vóór je ochtendoverzicht. Bij **Checks** staat: "'s Nachts gepauzeerd. Inhalen om 06:30". Gebruik de app, schrijf in de chat of tik op een to-do. Dan worden checks weer uitgevoerd, totdat je een uur inactief bent geweest. Met **Nu checken** wordt er meteen gecheckt.

## Een run is mislukt

Bij **Koppelingen**, **Checks** zie je onder **Recente runs** elke run. Een mislukte run wordt vanzelf opnieuw geprobeerd.

## Opzijgezet

Als een check een bericht twee keer opzijzet, wordt het apart gezet. Bij **Koppelingen**, **Checks** zie je hoeveel berichten dat zijn. **Opzijgezet** toont ze. Een bericht van iemand die je schrijft, iemand die je kent of een klant wordt ongeveer 3 dagen na binnenkomst nog een keer bekeken. Die controle maakt er een to-do van of sluit het bericht af. Wat je hebt afgewezen of gesnoozed, blijft zo.
