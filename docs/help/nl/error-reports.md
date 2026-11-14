---
title: Foutrapporten
area: security
summary: Als er iets misgaat, laat je Machine het team van The Machine weten wat er fout ging en waar in de code. Nooit wat er in je berichten staat, of je namen en adressen.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: fd3e1c2d68b93a35
---
## Wat het is

Als er iets misgaat in The Machine, stuurt je Machine ons team een kort, anoniem bericht over de fout. Zo kunnen we die oplossen voordat iemand er melding van maakt. Dit staat standaard aan en vereist [The Machine Network](/network).

## Wat er wordt verstuurd

Alleen dit, per soort fout:

- de soort fout, zoals `KeyError`;
- de melding, nadat alle specifieke informatie eruit is gehaald: getallen, id's, geciteerde tekst, e-mailadressen, links, bestandspaden, sleutels en woorden die een naam kunnen zijn;
- waar in de eigen code van The Machine de fout is opgetreden, nooit een map op je computer;
- de appversie, hoe vaak de fout is opgetreden en wanneer dat de eerste en laatste keer was.

Een echt voorbeeld: `IndexError`, `list index out of range`, bij `assistant.py:fault_event:7899`, versie `05b17ee6ac79`, 1 keer.

## Wat er nooit wordt verstuurd

Wat er in je berichten, to-do's, concepten of chats staat. Namen, e-mailadressen, telefoonnummers, links of wachtwoorden. Om welk account of welke persoon het ging.

## Waar fouten vandaan komen

- achtergrondtaken: nieuwe berichten controleren, to-do's voorbereiden, chat, Koppelingen en synchronisaties;
- het dashboard, in je browser of de app, inclusief fouten die daar worden getoond;
- mislukte of verlopen verzoeken vanuit het dashboard: om welk verzoek het gaat, nooit wat het heeft verstuurd;
- mislukte opdrachten voor codeeragenten: alleen de tool en het soort fout.

Herhaalde fouten van dezelfde soort worden geteld, maar niet opnieuw verstuurd. Er wordt hooguit eens per 10 minuten een bundel verstuurd. We bewaren de gegevens 30 dagen.

## Belasting beheren

Achtergrondtaken worden gepauzeerd als de limieten van je AI-abonnement bijna bereikt zijn. Zo blijft er ruimte over voor je eigen chats (zie [Je AI-model](model.md)).

Als foutrapporten aanstaan, laat je Machine ons ook één keer per dag weten hoe vaak dit is gebeurd. Per pauze: het uur, welke limiet is bereikt, hoe lang de pauze duurde en hoeveel opdrachten hebben gewacht. Er wordt niet vermeld waar die opdrachten over gingen.

## Uitzetten

Ga naar **Instellingen** en **Beveiliging** en zet **Foutrapporten sturen** uit. Er wordt dan niets meer vastgelegd of verstuurd en wat klaarstond, wordt verwijderd. Fouten blijven zichtbaar op je eigen Machine, die een oplossing kan voorstellen.

Zie [Beveiliging en privacy](security-and-privacy.md).
