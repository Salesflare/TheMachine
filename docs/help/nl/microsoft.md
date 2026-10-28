---
title: Microsoft Outlook en agenda
area: connections
summary: Mail en afspraken in Outlook, voor Microsoft 365 en Outlook.com. Verstuurt een e-mail pas nadat je hem goedkeurt.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, onboarding.py
site: Connect Microsoft, Copy link for your admin, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
---
## Wat het leest

- **Outlook**: al je mail, de laatste 7 dagen als je koppelt, daarna alles wat nieuw is.
- **Outlook-agenda**: je afspraken, alleen lezen.

Mail in Overige en nieuwsbrieven krijgen eerst een snelle blik: afzender, onderwerp en een paar woorden, veel tegelijk. Als er een belangrijk is, wordt die volledig gelezen en kan die een to-do worden. Niets wordt ongezien overgeslagen.

## Wat het kan versturen en wijzigen

- Een e-mail vanuit een to-do, pas nadat je hem goedkeurt in het voorbeeld.
- Als je een to-do over een e-mail snoozet, gaan de berichten van de thread naar een map Snoozed in Outlook en komen ze terug wanneer de to-do terugkomt.

De agenda wordt nooit gewijzigd.

## Koppelen

Op een gehoste Machine:

1. Open je setuppagina op app.themachine.computer/setup.
2. Druk op **Microsoft koppelen** en log in.
3. Vraagt Microsoft om goedkeuring van een beheerder, druk dan op **Link kopiëren voor je beheerder**, of op **Ik ben de beheerder: nu goedkeuren** als jij dat bent.

Of in het dashboard: **Koppelingen**, **+ Toevoegen**, kies Outlook en druk op **Inloggen met Microsoft**. Als je klaar bent, ben je terug in het dashboard.

Op je eigen computer, zodra hij [aan je account gekoppeld is](fleet.md): open **Koppelingen**, dan **+ Toevoegen**, kies Outlook en druk op **Inloggen met Microsoft**. Mail en agenda worden samen gekoppeld.

Met je eigen app: open daar **Je eigen app gebruiken**, of voer `assistant connect outlook` of `assistant connect outlook_calendar` uit. Het gebruikt je eigen app-registratie in Microsoft Entra en een inlogcode. Hij vraagt of hij ook moet versturen wat je goedkeurt.

## Verwijderen

- Op een gehoste Machine: druk op **Ontkoppelen** naast het account op je setuppagina. In het dashboard brengt **Ontkoppelen ↗** op Koppelingen je daarheen. **Opnieuw verbinden** daar logt opnieuw in zonder het dashboard te verlaten.
- Op je eigen computer: **Koppelingen**, open het account, **Details**, dan **Ontkoppelen**.

## Verwijderen bij Microsoft

Microsoft geeft ons geen manier om een login in te trekken, dus verwijder hem daar ook:

- Werk- of schoolaccount: myapps.microsoft.com
- Persoonlijk account: account.live.com/consent/Manage
