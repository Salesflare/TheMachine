---
title: Microsoft Teams
area: connections
summary: Teams-chats, chatgesprekken van vergaderingen en vergadernotities voor een werk- of schoolaccount. Antwoorden worden pas verstuurd nadat je ze hebt goedgekeurd.
covers: connector:teams
code: connectors/teams.py, teams_send.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 9ca0bb08466b4d58
---
## Wat wordt gelezen

Je 1-op-1-chats, groepschats en chatgesprekken van vergaderingen in Teams: de laatste 7 dagen op het moment dat je verbinding maakt, en daarna om de paar minuten nieuwe berichten. Ongeveer een jaar aan oudere chats en, met toestemming van je beheerder, kanaalgesprekken wordt later beetje bij beetje ingelezen als [geschiedenis](history.md), zonder dat dit iets ophoudt.

Met toestemming van je beheerder leest The Machine ook:

- Kanaalgesprekken in je teams.
- Transcripties van vergaderingen die je hebt georganiseerd.
- Vergadernotities en actiepunten van Copilot, als je een Microsoft 365 Copilot-licentie hebt.

Elke transcriptie of set notities wordt bij de betreffende vergadering in je agenda opgeslagen, met de markering **Van Teams**. Zonder die transcripties of notities blijft het chatgesprek van de vergadering wel beschikbaar.

Berichten van bots, apps en het systeem worden overgeslagen.

## Wat ermee kan

Antwoorden in een 1-op-1-chat, groepschat of chatgesprek van een vergadering waar een to-do vandaan komt. The Machine stelt het antwoord op. Het wordt pas verstuurd nadat je het hebt gecontroleerd en op **Nu versturen** hebt gedrukt. Het wordt namens jou in die chat verstuurd. The Machine begint nooit zelf een nieuwe chat.

The Machine plaatst geen berichten in kanalen. Wil je reageren in een kanaalgesprek, open het dan met **Openen in Teams**.

## Welke machtigingen nodig zijn

Microsoft vraagt toestemming om The Machine je chats en profiel te laten lezen en namens jou chatberichten te laten versturen. Daar is geen toestemming van een beheerder voor nodig.

Als je Teams hebt gekoppeld voordat The Machine berichten kon versturen, staat er op de Teams-kaart **Opnieuw verbinden om antwoorden te versturen.** Druk op **Opnieuw verbinden** en geef opnieuw toestemming. Tot die tijd kun je het concept zelf in Teams versturen.

Voor kanalen, transcripties en Copilot-notities moet de beheerder van je organisatie één keer toestemming geven. Tot die tijd staat op de Teams-kaart wat The Machine nog niet kan lezen en waarom.

Dit werkt alleen met een Microsoft-account voor werk of school. Met persoonlijke accounts zijn er geen Teams-chats die The Machine op deze manier kan lezen.

## Koppelen

Op een gehoste Machine:

1. Open in het dashboard **Koppelingen** en vervolgens **Chat** voor **Microsoft Teams** of **Afspraken** voor **Teams-meetings**. Voor beide gebruik je dezelfde aanmelding.
2. Druk op **Aanmelden met Microsoft** en geef toestemming. Daarna keer je terug naar het dashboard.
3. Stuur je beheerder de link die op de aanmeldpagina wordt getoond als je kanalen en vergadernotities wilt gebruiken. Koppel Teams opnieuw nadat de beheerder toestemming heeft gegeven.

Tijdens het instellen staat ook **Microsoft Teams koppelen** op de instelpagina.

Op je eigen computer, zodra die [aan je account is gekoppeld](friends.md#a-machine-on-your-own-computer): open **Koppelingen** en vervolgens **Chat** of **Afspraken**, kies **Microsoft Teams** of **Teams-meetings** en druk op **Aanmelden met Microsoft**. The Machine leest daar je chats en chatgesprekken van vergaderingen. Kanalen en vergadernotities zijn daar nog niet beschikbaar.

## Loskoppelen

Open in het dashboard **Koppelingen**, open Microsoft Teams en kies **Details** en daarna **Ontkoppelen**. Wat al is ingelezen, blijft bewaard.

## Toegang intrekken in Microsoft

Open myapps.microsoft.com en verwijder The Machine. Als Outlook met hetzelfde adres is gekoppeld, wordt dat ook losgekoppeld.
