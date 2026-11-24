---
title: Beveiliging en privacy
area: security
summary: Je eigen privé-Machine, versleuteld opgeslagen e-mail en niets wordt verstuurd zonder jouw akkoord. Kort samengevat, met links.
covers:
code: message_seal.py, next_actions.py, SECURITY.md
order: 1
keywords: private, privacy, data, gdpr, encrypted, who can see, safe, stored, keep
translated: 27c910c92b215ad3
---
## Kort samengevat

- Je eigen Machine: een gehoste Machine draait in de EU-cloud, helemaal voor jou en nooit gedeeld. Of gebruik je eigen computer.
- We lezen je e-mail niet: berichten worden versleuteld opgeslagen en onze supporttools kunnen ze niet openen.
- Er wordt niets verstuurd zonder jouw akkoord: The Machine leest en maakt concepten, jij bepaalt wat er wordt verstuurd. Zie [Doe het](do-it.md).
- Niet gebruikt om AI te trainen: we hebben geen eigen AI. Je provider werkt onder jouw account en volgens de voorwaarden van die provider.
- Inzichten voor het team, tenzij je ze uitschakelt: af en toe een paar algemene tips, niets persoonlijks, gecontroleerd voordat ze worden gedeeld. Zie [Inzichten delen](share-learnings.md).
- Foutrapporten, tenzij je ze uitschakelt: als er iets misgaat, worden het soort fout en de plek in de code doorgegeven. Nooit je berichten, namen of adressen. Zie [Foutrapporten](error-reports.md).
- Gebruiksstatistieken op een gehoste Machine: dagelijkse aantallen van wat je hebt gedaan (zoals geopende to-do's of verstuurde e-mails), nooit de inhoud ervan. Ook wordt bijgehouden hoe snel je dashboard opent (alleen laadtijden, op je telefoon of computer, in de app of browser).
- Neem je gegevens mee of verwijder ze: exporteer alles via **Instellingen** › **Algemeen**, of verwijder je Machine en de back-ups met één knop. Zie [Opzeggen of verwijderen](cancel-and-delete.md).
- Onze toegang wordt bijgehouden: telkens wanneer iemand uit ons team het rapport of de logboeken van je gehoste Machine bekijkt. Eigenaren en beheerders van een Fleet zien dit onder **Activiteit**. Zie [Fleets](fleet.md).

## Back-ups

Een gehoste Machine maakt elke nacht een back-up van je gegevens. De back-up wordt versleuteld op je Machine voordat die wordt verstuurd en opgeslagen in Microsoft Azure in Nederland (EU). De laatste 7 dagelijkse, 4 wekelijkse en 3 maandelijkse back-ups blijven bewaard, dus ongeveer 3 maanden. Ze worden verwijderd wanneer je Machine wordt verwijderd.

Kunnen we ze openen? Ja, om een defecte Machine te herstellen: de sleutel bewaren we apart van de back-ups. De berichten in een back-up worden nogmaals versleuteld met een tweede sleutel die we ook bewaren. Die sleutel is verzegeld en staat nooit in de back-up.

Back-ups zijn een vangnet, dus bewaar zelf een kopie van wat je niet kwijt wilt: **Alles**, via **Instellingen** › **Algemeen** › **Exporteren**. Zie [Verplaatsen naar een andere computer](moving.md).

Op je eigen computer worden niet automatisch back-ups gemaakt en hebben we zelf geen kopie. Een versleutelde nachtelijke back-up van je thuismap is genoeg: zie [Aan de slag](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md#later).

## Beveiligingsniveaus

**Standaard** behoudt de huidige standaardinstellingen. **Voorzichtig** toont geen tekst in meldingen, bewaart geen logins en houdt minder gegevens bij. Een beheerder van een Werk-Fleet kan de Fleet op Voorzichtig instellen. Zie [Beveiligingsniveaus](security-levels.md).

## Inloggen

Voor een gehost dashboard heb je een passkey nodig, of een login met Google of Microsoft plus een code uit een authenticator-app.

## Koppelingen

In het artikel over elke koppeling staat wat die leest en wat die kan versturen. Je kunt elke koppeling op elk moment loskoppelen: zie [Koppelingen](connections.md).

## Hulp

Hulp draait op je eigen Machine en kan je gegevens niet zien. Alleen het onderwerp van elke vraag gaat naar het team van The Machine, nooit je eigen woorden. Zie [Help vragen](help-chat.md#what-the-team-sees).

## Meer

- [Beveiliging](/security): hoe de beveiliging is opgebouwd, wat onze medewerkers wel en niet kunnen zien en hoe we naar problemen zoeken.
- [Privacyverklaring](/privacy) en [voorwaarden voor gegevensverwerking](/dpa).
- Een beveiligingsprobleem gevonden? Bekijk het [beveiligingsbeleid](https://github.com/Salesflare/TheMachine/blob/main/SECURITY.md).
