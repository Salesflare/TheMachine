---
title: Geen nieuwe to-do's
area: troubleshooting
summary: Checks staan uit, wachten of zijn gestopt vanwege de gebruikslimiet van je model. Zo zie je wat er aan de hand is en wat je kunt doen.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: f0e9e4dc6c850b25
---
To-do's komen voort uit checks: je Machine kijkt ongeveer elke 15 minuten naar wat er is binnengekomen.

## Net aangemeld

Op een nieuwe gehoste Machine starten checks vanzelf zodra je AI en mail zijn gekoppeld. Terwijl je Machine je mail leest, staat er bij To-do's: "Je mail wordt gelezen. De eerste to-do's verschijnen over een paar minuten." Zodra hij weet hoeveel mail er is, geeft hij een schatting: "De eerste to-do's verschijnen over ongeveer 10 min." Als er een stap ontbreekt, geeft **Wacht op jou** aan wat je moet doen, bijvoorbeeld **Mail koppelen**, met een link naar die stap.

Terwijl hij leest, laat To-do's zien hoever hij is ("20 van de 132 berichten gelezen. De volgende 40 worden gelezen…"), een paar mensen en organisaties die hij is tegengekomen, en je eerste to-do zodra die klaarstaat. Het getal telt de berichten die hij helemaal heeft gelezen; de voortgangsbalk loopt door terwijl hij de volgende berichten leest. De namen komen uit je eigen mail en zijn alleen voor jou zichtbaar.

Vindt de eerste controle niets voor je, dan zie je wat er is gelezen en krijg je suggesties voor vervolgstappen, zoals een dienst koppelen waarvan je vaak mail krijgt of vragen wat er deze week is veranderd.

## Checks staan uit

Bovenaan To-do's staat: "Checks staan uit. Er komen dus nog geen to-do's binnen." Druk op een gehoste Machine op **Checks aanzetten**. Voer op je eigen computer `./install.sh --activate` uit.

## De limiet van je model

Om ruimte over te houden voor je eigen chats, pauzeren checks wanneer je ongeveer 65% van de limiet van 5 uur van je AI-abonnement en 90% van de wekelijkse limiet hebt gebruikt. Heb je een back-upmodel met een ander abonnement, dan hoeven checks niet te wachten. Bekijk [Model](model.md).

Terwijl checks wachten, staat bovenaan het dashboard tot wanneer, bijvoorbeeld: "Checks wachten tot 07:15 om je ChatGPT-week te sparen." Met **Nu checken** start je toch een check. Je limieten vind je in **Instellingen**, **Model**.

Er gaat niets verloren: berichten worden gecontroleerd zodra dat weer kan. Na lang wachten worden recente berichten van mensen eerst gecontroleerd. Elke check verwerkt ook een deel van de oudste berichten.

## 's Nachts

Van 00:00 tot 06:30 pauzeren checks en wachten nieuwe berichten. Om 06:30 worden ze samen gecontroleerd, vóór je ochtendoverzicht. Bij **Checks** staat: "'s Nachts gepauzeerd. Inhalen om 06:30." Gebruik de app, schrijf in de chat of tik op een to-do. Checks draaien dan weer, totdat je een uur inactief bent geweest. Met **Nu checken** controleer je berichten meteen.

## Een run is mislukt

Bij **Koppelingen**, **Checks** toont **Recente runs** elke run. Een mislukte run wordt vanzelf opnieuw geprobeerd.

Bij een run die is gestopt vanwege de gebruikslimiet van je AI-abonnement staat **De gebruikslimiet van AI is bereikt.** en wanneer de limiet weer wordt opgeheven. Dit is een pauze, geen fout: de berichten wachten en worden na de reset gecontroleerd. Er wordt niets naar [foutrapporten](error-reports.md) gestuurd.

## Opzijgezet

Als een check een bericht twee keer uitstelt, wordt het opzijgezet. Bij **Koppelingen**, **Checks** zie je hoeveel berichten dat zijn. **Opzijgezet** toont ze. Een bericht van iemand die jou mailt, een bekende of een klant wordt ongeveer 3 dagen na binnenkomst nog één keer gecontroleerd. Die controle maakt er een to-do van of sluit het bericht af. Wat je hebt afgewezen of gesnoozed, blijft zo.
