---
title: Foutrapporten
area: security
summary: Als er iets misgaat, laat je Machine het team van The Machine weten wat er misging en waar in de code. Nooit je berichten, namen of adressen.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 4dc53a854d15f1a3
---
## Wat het is

Als er iets misgaat in The Machine, stuurt je Machine ons team een kort, anoniem bericht over de fout. Zo kunnen we die oplossen voordat iemand er melding van maakt. Dit staat standaard aan en vereist [The Machine Network](/network).

## Wat er wordt verstuurd

Alleen dit, per soort fout:

- de soort fout, zoals `KeyError`;
- het foutbericht, zonder specifieke gegevens zoals nummers, id's, geciteerde tekst, e-mailadressen, links, bestandspaden, sleutels en woorden die een naam kunnen zijn;
- waar in de eigen code van The Machine de fout is opgetreden, nooit een map op je computer;
- de appversie, hoe vaak de fout is opgetreden en wanneer dat voor het eerst en het laatst was.

Bijvoorbeeld: `IndexError`, `list index out of range`, op `machine/faults.py:fault_event:246`, versie `05b17ee6ac79`, 1 keer.

## Wat nooit wordt verstuurd

Wat er in je berichten, to-do's, concepten of chats staat. Namen, e-mailadressen, telefoonnummers, links of wachtwoorden. Over welk account of welke persoon het ging.

## Waar fouten vandaan komen

- achtergrondwerk: nieuwe berichten controleren, to-do's voorbereiden, chats, Koppelingen en synchronisaties;
- het dashboard, in je browser of de app, inclusief fouten die daar worden getoond;
- mislukte aanvragen vanuit het dashboard of aanvragen die een time-out krijgen: welke aanvraag, nooit wat die heeft verstuurd;
- mislukte taken van programmeeragents: alleen de tool en de soort fout;
- de korte test van je AI als die mislukt: de fout van de AI, zonder specifieke gegevens.

Dezelfde fout wordt geteld, maar niet opnieuw verstuurd. Er wordt maximaal één batch per 10 minuten verstuurd. We bewaren die 30 dagen.

## Dosering

Achtergrondwerk wordt gepauzeerd als de limieten van je AI-abonnement bijna op zijn. Zo blijft er ruimte voor je eigen chats (zie [Je AI-model](model.md)).

Als foutrapporten aanstaan, laat je Machine ons ook één keer per dag weten hoe vaak dat is gebeurd: per pauze het uur, welke limiet, hoe lang de pauze duurde en hoeveel taken hebben gewacht. Er wordt niets verstuurd over wat die taken deden.

## Uitzetten

Ga naar **Instellingen** en **Beveiliging** en zet **Foutrapporten sturen** uit. Er wordt niets meer vastgelegd of verstuurd en gegevens die klaarstonden om verstuurd te worden, worden verwijderd. Fouten blijven zichtbaar op je eigen Machine, die een oplossing kan voorstellen.

Zie [Beveiliging en privacy](security-and-privacy.md).
