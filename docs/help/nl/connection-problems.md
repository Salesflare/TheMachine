---
title: Een koppeling heeft hulp nodig
area: troubleshooting
summary: Een bron zegt Heeft je hulp nodig, of brengt niets meer binnen. Wat je kunt proberen.
covers: 
code: onboarding.py, dashboard.html, assistant.py
order: 1
---
## Bekijk de status

Open **Koppelingen**. Elke bron laat zien hoe het ermee gaat:

- **Verbindt automatisch opnieuw**: een korte hapering. Hij probeert het zelf opnieuw.
- **Wacht op eerste sync**: net gekoppeld. Geef hem een paar minuten.
- **Leest weer om** 07:00: X en LinkedIn lezen alleen overdag. Je hoeft niets te doen.
- **Heeft je hulp nodig**: open **Details**. Daar staat wat er misging en wat je moet doen.
- **Telefoon niet verbonden**: de telefoon bereikt OpenClaw niet. Open de OpenClaw-app erop.

Een bron die steeds faalt en urenlang niets nieuws binnenbrengt, langer dan zijn gewone stille periode, staat niet als verbonden. Dat verdwijnt vanzelf zodra er weer iets binnenkomt.

Het getal bij **Koppelingen** telt alleen bronnen die je hulp nodig hebben.

## Veelvoorkomende oplossingen

- "Log opnieuw in bij Google" (of Microsoft): één regel per account. Eén keer **Opnieuw verbinden** brengt al zijn bronnen terug, zoals Gmail en Agenda.
- "moet opnieuw inloggen": druk op **Opnieuw verbinden** en log in. Op een gehoste Machine log je daar meteen in en kom je terug in het dashboard.
- Microsoft is de toegang nog aan het instellen: hij probeert het zelf opnieuw.
- Slack: controleer je Maton API-sleutel en de Slack-koppeling in Maton.
- Android: open de OpenClaw-app op de telefoon en geef hem toegang tot meldingen.

Op je eigen computer controleert `assistant doctor` elke bron en toont hij de oplossing voor elk probleem.

Kom je er nog niet uit? Zie [Hulp krijgen](get-support.md).
