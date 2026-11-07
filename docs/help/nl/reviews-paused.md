---
title: Geen nieuwe to-do's
area: troubleshooting
summary: Checks staan uit, wachten, of zijn gestopt op de gebruikslimiet van je model. Hoe je dat ziet en wat je doet.
covers: 
code: dashboard.html, assistant.py
order: 3
---
To-do's komen uit checks: je Machine leest wat er binnenkwam, in kleine porties, binnen ongeveer 15 minuten.

## Net aangemeld

Op een nieuwe gehoste Machine starten checks vanzelf zodra je AI en je mail gekoppeld zijn. Terwijl je Machine je mail leest, staat bij To-do's "Je mail wordt gelezen, eerste to-do's over een paar minuten". Zodra hij weet hoeveel het is, zegt hij ongeveer hoe lang het duurt: "Eerste to-do's over zo'n 10 min." Ontbreekt er een stap, dan noemt **Wacht op jou** die, zoals **Mail koppelen**, met een link naar die stap.

Terwijl hij leest, toont To-do's hoe ver hij is, een paar van de mensen en organisaties die hij tegenkwam, en je eerste to-do zodra die er is. De namen komen uit je eigen mail, en alleen jij ziet ze.

Vindt hij bij de eerste blik niets voor je, dan zegt hij wat hij las en biedt hij volgende stappen aan, zoals een dienst koppelen die je vaak mailt of vragen wat er deze week veranderd is.

## Checks staan uit

Bovenaan To-do's staat "Checks staan uit, dus er komen nog geen to-do's." Druk op een gehoste Machine op **Checks aanzetten**. Voer op je eigen computer `./install.sh --activate` uit.

## De limiet van je model

Checks van wat binnenkwam pauzeren bij ongeveer 65% van de 5-uurslimiet van je abonnement en bij 90% van de weeklimiet, zodat er ruimte blijft voor je eigen chats. Een bord dat je geschiedenis doorloopt, gaat trager, met ongeveer een zevende van de week per dag. Met een werkend reservemodel op een ander abonnement of bij een andere aanbieder wachten checks niet. Zie [Model](model.md).

Terwijl checks wachten, staat bovenaan het dashboard tot wanneer, zoals "Checks wachten tot 07:15 om je ChatGPT-week te sparen." **Nu checken** start er meteen een. Als een limiet bereikt is, staat bovenaan het dashboard welke en wanneer die weer vrijkomt. **Koppelingen**, dan **Checks**, toont het naast de run. **Instellingen**, **Model** toont je limieten. Zie [Model](model.md).

Er gaat niets verloren terwijl het wacht: wat binnenkwam, wordt gecheckt zodra het kan.

## Een run is mislukt

**Recente runs** onder **Checks** toont elke run. Een mislukte portie wordt vanzelf opnieuw geprobeerd.
