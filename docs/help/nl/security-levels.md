---
title: Beveiligingsniveaus
area: security
summary: Eén schakelaar, Standaard of Voorzichtig, bepaalt je beveiligings- en privacy-instellingen. De beheerder van een Werk-Fleet kiest er een voor de Fleet.
covers: settings:security
code: security_levels.py, dashboard.html, fleet.py
order: 2
translated: cf3ba86c8c1a23f3
---
## Twee niveaus

Open **Instellingen** en daarna **Beveiliging**.

- **Standaard**: de huidige standaardinstellingen. Er verandert niets.
- **Voorzichtig**: strenger, voor als je minder op je telefoon wilt en minder wilt bewaren.

Een niveau is een startpunt. Pas je daarna een instelling aan, dan wordt het niveau **Aangepast**. Kies opnieuw een niveau om de instellingen te resetten.

## Wat Voorzichtig voor jou verandert

- **Tekst in meldingen** staat uit: een melding zegt "Nieuwe to-do" of "Klaargezet", niet wat er in de to-do staat.
- **Aanbieden om logins op te slaan** staat uit. Sites waarbij je bent ingelogd en die je hebt opgeslagen, blijven bewaard tot je op **Alle opgeslagen logins vergeten** tikt.
- **Werkcontacten opzoeken**, **Aanbieden om inzichten te delen** en **Delen wat aan Help gevraagd wordt** staan uit.
- **Checken welke van mijn contacten een Machine hebben** en **Laat mensen die mijn e-mailadres hebben mij vinden** staan uit.
- **Details van Doe het 90 dagen bewaren** staat uit: ze worden 30 dagen bewaard.
- **Wat andere Machines de mijne mogen vragen** staat op **Uit**: er wordt niets ingepland met andere Machines. Zie [Vrienden en het Network](friends.md#scheduling-with-other-machines).
- In een Familie-Fleet wordt je eerst gevraagd voordat vrije en bezette tijden gedeeld worden. Bij Vrienden wordt meetingcontext geweigerd.

## Het niveau van een Werk-Fleet

De eigenaar of een beheerder van de Fleet kiest het niveau bij de Fleet-instellingen: ga naar **Instellingen** › **Account** en tik op **Fleet**. Iedereen in de Fleet kan het zien. Als het niveau **Voorzichtig** is:

- Antwoorden aan teamgenoten wachten op jouw toestemming, bevatten geen namen en gaan alleen over mensen uit je werkaccounts.
- Ook introducties en overdrachten wachten op jouw toestemming.
- De Team-Graph deelt klantmails zonder bijlagen.
- Meldingen voor werk-to-do's bevatten geen tekst.
- Werkcontacten worden niet opgezocht.
- Je Machine checkt je contacten niet op het Network en maakt je niet vindbaar via e-mail, tenzij je dat zelf hebt ingeschakeld.
- Iedereen moet elke 7 dagen opnieuw inloggen.
- Een uitnodigingslink werkt alleen voor het e-mailadres waarnaar die is verstuurd.

Leden kunnen strengere instellingen kiezen dan de Fleet, maar geen soepelere. Hun eigen keuzes blijven bewaard en worden weer van kracht als de Fleet teruggaat naar **Standaard**.

## Wat voor beide niveaus geldt

Er wordt niets verstuurd zonder jouw toestemming: je ziet elk concept en tikt op **Versturen**. **Doe het** en codeeragenten werken hetzelfde. Inloggen vereist altijd een verificatiecode van een authenticator of een passkey.
