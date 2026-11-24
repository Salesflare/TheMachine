---
title: Microsoft Outlook en agenda
area: connections
summary: Outlook-mail en meetings voor Microsoft 365 en Outlook.com. Er wordt pas een e-mail verstuurd nadat je die hebt goedgekeurd.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 7229063d9365735d
---
## Wat hij leest

- **Outlook**: al je e-mail van de afgelopen 7 dagen wanneer je koppelt, en daarna alle nieuwe e-mail.
- **Outlook-agenda**: je afspraken, alleen-lezen.

E-mail in Overige en nieuwsbrieven worden eerst kort bekeken: de afzender, het onderwerp en een paar woorden. Als iets belangrijk is, wordt het volledig gelezen en kan het een to-do worden.

## Wat hij kan versturen en wijzigen

- Een e-mail vanuit een to-do, alleen nadat je die hebt goedgekeurd. Die wordt verstuurd vanaf het eigen adres van de mailbox, niet vanaf een alias.
- Een antwoord komt in het Outlook-gesprek van de e-mail waarop je antwoordt.
- Nadat een antwoord is verstuurd, worden de berichten in de thread een paar dagen verplaatst naar een map Gesnoozed in Outlook (3 dagen, tenzij de to-do iets anders aangeeft). Daarna komen ze terug in het Postvak IN, of eerder als iemand antwoordt. Ze blijven nooit langer weg dan tot de deadline van de to-do. Voordat je verstuurt, laat het overzicht dit zien.

De agenda wordt nooit gewijzigd.

## Foto's van collega's en contacten

Microsoft wordt ook gevraagd om basisprofielen van mensen in je organisatie (naam, e-mailadres en foto) en je Outlook-contacten te lezen. Je Machine gebruikt die gegevens alleen voor foto's, functietitels en bedrijven van mensen die al in je Graph staan, tot maximaal 200 foto's per dag. Van iemand zonder foto wordt na 30 dagen opnieuw gecontroleerd of er een foto is.

De beheerder van je organisatie moet mogelijk toestemming geven voor foto's van collega's. Zonder die toestemming wordt Outlook nog steeds gekoppeld, maar zonder deze foto's. Een account dat hiervoor al was gekoppeld, krijgt één to-do: druk op **Opnieuw koppelen**, of op **Niet nodig** om de to-do voorgoed te sluiten. Een persoonlijk account (Outlook.com, Hotmail) heeft geen collega's, dus de to-do vraagt alleen om foto's van contacten.

## Koppelen

Op een gehoste Machine:

1. Open je installatiepagina op app.themachine.computer/setup.
2. Druk op **Microsoft koppelen** en log in.
3. Vraagt Microsoft om goedkeuring van een beheerder? Stuur je Microsoft 365-beheerder de link (**Link kopiëren**). Zodra die toestemming geeft, kan iedereen in je organisatie koppelen. Ben jij de beheerder, druk dan op **Ik ben de beheerder: nu goedkeuren**.

Of ga in het dashboard naar **Koppelingen**, **E-mail**, kies Outlook en druk op **Inloggen met Microsoft**. De link voor de beheerder staat direct onder de knop.

Op je eigen computer, nadat die [aan je account is gekoppeld](friends.md#a-machine-on-your-own-computer): open **Koppelingen**, ga naar **E-mail**, kies Outlook en druk op **Inloggen met Microsoft**. Mail en agenda worden samen gekoppeld. Na Microsoft ga je terug naar **Koppelingen** in je dashboard.

Voor IT-teams met een eigen Microsoft Entra-app: open daar **Je eigen app gebruiken**, of voer `assistant connect outlook` uit.

## Loskoppelen

- Op een gehoste Machine: druk naast het account op je installatiepagina op **Ontkoppelen**. Met **Ontkoppelen ↗** bij Koppelingen ga je naar die pagina.
- Op je eigen computer: open **Koppelingen**, open het account en kies **Details**. Druk daarna op **Ontkoppelen**.

## Verwijderen bij Microsoft

Microsoft laat ons een login niet intrekken, dus verwijder de koppeling ook daar:

- Werk- of schoolaccount: myapps.microsoft.com
- Persoonlijk account: account.live.com/consent/Manage
