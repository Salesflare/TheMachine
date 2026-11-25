---
title: Een koppeling heeft hulp nodig
area: troubleshooting
summary: Een bron meldt ‘Heeft je hulp nodig’ of haalt niets meer op. Dit kun je proberen.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: cc4b227abd053022
---
## De status controleren

Open **Koppelingen**. Bij elke bron zie je de status:

- **Verbindt automatisch opnieuw**: een korte storing. De bron probeert het zelf opnieuw.
- **Wacht op eerste sync**: net gekoppeld. Wacht een paar minuten.
- **Leest weer om** 07:00: X en LinkedIn lezen alleen overdag. Je hoeft niets te doen.
- **Nog niet ingesteld**: hier is nog niemand ingelogd bij deze bron. Selecteer **Koppelen**. Binnen een minuut gaat de bron aan de slag.
- **Heeft je hulp nodig**: open **Details**. Daar staat wat er misging en wat je kunt doen.
- **Telefoon niet verbonden**: je Android-telefoon bereikt je Machine niet. Open de OpenClaw-app op je telefoon.

Een bron die langer dan normaal niets ophaalt, meldt **Wacht op een nieuwe sync**. Deze melding verdwijnt vanzelf zodra een sync lukt.

Het getal bij **Koppelingen** telt alleen bronnen die je hulp nodig hebben.

## Veelvoorkomende oplossingen

- ‘Log opnieuw in bij Google’ (of Microsoft): met één keer **Opnieuw koppelen** herstel je alle bronnen van dat account, zoals Gmail en Agenda.
- ‘je moet opnieuw inloggen’: selecteer **Opnieuw koppelen** en log in.
- ‘heeft een programma nodig dat niet op deze computer staat’: voer de opdracht op de kaart uit in een terminal op die computer. Daar staat welk programma je moet installeren, of er wordt gezocht naar een programma dat is verplaatst.
- Microsoft is nog bezig met toegang instellen: het probeert het vanzelf opnieuw.
- Slack: selecteer **Opnieuw koppelen**. Gekoppeld met een Maton-sleutel? Controleer de sleutel en de Slack-koppeling in Maton.
- Android: open de OpenClaw-app op je telefoon en geef de app toegang tot meldingen.

Op je eigen computer controleert `assistant doctor` elke bron en vertelt hoe je elk probleem oplost.

Lukt het nog steeds niet? Bekijk [Hulp krijgen](get-support.md).
