---
title: Geen nieuwe to-do's
area: troubleshooting
summary: Checks staan uit, wachten of zijn gestopt vanwege de gebruikslimiet van je model. Zo herken je dat en dit kun je doen.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: 07aca53acc41694d
---
To-do's komen uit checks: je Machine bekijkt wat er in ongeveer 15 minuten is binnengekomen.

## Net aangemeld

Op een nieuwe gehoste Machine beginnen checks vanzelf zodra je AI en mail zijn gekoppeld. Terwijl je Machine je mail leest, staat er bij To-do's: "Je mail wordt gelezen. De eerste to-do's verschijnen over een paar minuten." Zodra duidelijk is hoeveel mail er is, staat er ongeveer hoe lang het duurt: "De eerste to-do's verschijnen over ongeveer 10 min." Ontbreekt er een stap, dan geeft **Wacht op jou** aan wat je moet doen, zoals **Mail koppelen**, met een link naar die stap.

Terwijl je Machine leest, laat To-do's zien hoever hij is ("20 van 132 berichten gelezen. De volgende 40 worden gelezen…"), een paar mensen en organisaties die hij is tegengekomen en je eerste to-do zodra die er is. Het aantal telt de berichten die hij helemaal heeft gelezen. De balk loopt door terwijl hij de volgende berichten leest. De namen komen uit je eigen mail en alleen jij kunt ze zien.

Als de eerste controle niets voor je oplevert, staat er wat er is gelezen en worden vervolgstappen voorgesteld, zoals een dienst koppelen waarvan je vaak mail krijgt of vragen wat er deze week is veranderd.

## Checks staan uit

Bovenaan To-do's staat: "Checks staan uit, dus er komen nog geen to-do's binnen." Druk op een gehoste Machine op **Checks aanzetten**. Voer op je eigen computer `./install.sh --activate` uit.

## De limiet van je model

Om ruimte over te houden voor je eigen chats, pauzeren checks wanneer je ongeveer 65% van de limiet van 5 uur en 90% van de wekelijkse limiet van je AI-abonnement hebt gebruikt. Met een back-upmodel op een ander abonnement hoeven checks niet te wachten. Bekijk [Model](model.md).

Terwijl checks wachten, staat bovenaan het dashboard tot wanneer, bijvoorbeeld: "Checks wachten tot 07:15 om je ChatGPT-week te sparen." Met **Nu checken** start je toch een check. Onder **Instellingen**, **Model** zie je je limieten.

Er gaat niets verloren: de binnengekomen berichten worden gecontroleerd zodra dat kan.

## 's Nachts

Van 00:00 tot 06:30 pauzeren checks en wachten nieuwe berichten. Om 06:30 worden ze samen gecontroleerd, vóór je ochtendoverzicht. Bij **Checks** staat: "'s Nachts gepauzeerd. Haalt de achterstand om 06:30 in." Gebruik de app, schrijf iets in de chat of tik op een to-do. Daarna worden checks weer uitgevoerd, totdat je een uur inactief bent geweest. Met **Nu checken** controleer je berichten meteen.

## Een run is mislukt

Bij **Recente runs** onder **Koppelingen**, **Checks** zie je elke run. Een mislukte run wordt vanzelf opnieuw geprobeerd.

Bij een run die is gestopt vanwege de gebruikslimiet van je AI-abonnement staat **De gebruikslimiet van AI is bereikt.** en wanneer die wordt opgeheven. Dit is een pauze, geen fout: de berichten wachten en worden na de reset gecontroleerd. Er wordt niets naar [Foutrapporten](error-reports.md) gestuurd.

## Opzijgezet

Als een check een bericht twee keer opzijzet, wordt het opzijgezet. Onder **Koppelingen**, **Checks** zie je hoeveel berichten dat zijn. Bij **Opzijgezet** vind je ze terug. Een bericht van iemand die je schrijft, iemand die je kent of een klant wordt ongeveer 3 dagen nadat het is binnengekomen nog een keer gecontroleerd. Daaruit komt een to-do of het bericht wordt gesloten. Wat je hebt afgewezen of gesnoozed, blijft zo.
