---
title: Salesflare CRM
area: connections
summary: Accounts, contactpersonen en deals, zodat hij weet wie belangrijk is. Hij leest ze via je API-sleutel.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 3d6041d568843d96
---
## Wat hij leest

Je accounts, contactpersonen en deals in Salesflare, plus de tijdlijn van elke account: e-mails van collega's waarbij je niet in de cc stond en meetings met notities.

## Wat hij kan wijzigen

Niets. (Op je eigen computer kan de instelling `join_pipelines` ervoor zorgen dat je wordt toegevoegd aan accounts in geselecteerde pipelines. Deze optie staat standaard uit.)

## Koppelen

1. Open in Salesflare [Instellingen, API-sleutels](https://app.salesflare.com/#/settings/apikeys) en maak een sleutel aan.
2. Op een gehoste Machine: open je installatiepagina op app.themachine.computer/setup, ga naar **Meer bronnen**, open Salesflare CRM, plak de sleutel en klik op **Koppelen**.
3. In het dashboard: **Koppelingen**, **Klanten**, Salesflare CRM. Plak de sleutel en klik op **Koppelen**. Op de kaart zie je hoever de synchronisatie is.

## Synchronisatiedetails

Bij **Koppelingen**, **Klanten**, zie je bij Salesflare hoever de synchronisatie is: hoeveel accounts deze ronde zijn gelezen en hoeveel zijn overgeslagen omdat Salesflare te traag was. Duurt een ronde uren, dan wordt aangegeven dat de synchronisatie misschien is vastgelopen.

De tegels tonen hoeveel accounts hij kon openen en hoeveel e-mails en meetings hij heeft opgehaald. Kan je API-sleutel in Salesflare geen enkele account openen, dan staat er op de kaart **Heeft je hulp nodig**: gebruik de sleutel van een gebruiker die deze accounts wel kan zien. Loopt Salesflare steeds vast, maar lukt het bij elke nieuwe poging wel, dan staat er dat Salesflare **soms traag is**.

Heeft Salesflare toegang tot de tijdlijn voor API-sleutels voor je team nog niet ingeschakeld, dan staat dat op de kaart. Er worden pas e-mails en meetings opgehaald zodra Salesflare Support dit inschakelt. Hij controleert dit de eerste dag elke 10 minuten opnieuw, daarna ongeveer elk uur. Zodra het werkt, gaat de synchronisatie vanzelf verder.

- **Stoppen**: er worden geen nieuwe gegevens opgehaald totdat je op **Begin** klikt. De synchronisatie gaat verder waar hij was gebleven.
- **Sync herstarten**: de synchronisatie begint opnieuw en leest de afgelopen week opnieuw. Er gaat niets verloren van wat hij al heeft opgehaald.
- **API-sleutels**: opent de pagina met API-sleutels van Salesflare, waar je een nieuwe sleutel kunt maken.

## Verwijderen

- In het dashboard: **Koppelingen**, open Salesflare, **Details** en klik daarna op **Ontkoppelen**. Wat hij al heeft opgehaald, blijft behouden.
- Op een gehoste Machine kun je ook op **Verwijderen** naast Salesflare klikken op je installatiepagina.

## De toegang in Salesflare intrekken

Verwijder de API-sleutel in Salesflare, onder Instellingen, API-sleutels.
