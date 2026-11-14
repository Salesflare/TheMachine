---
title: Foutrapporten
area: security
summary: Als er iets misgaat, laat je Machine het team van The Machine weten wat er fout ging en waar in de code. Nooit wat je berichten, namen of adressen bevatten.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 03a8649f2f634b59
---
## Wat wordt verstuurd

Als er iets misgaat in The Machine, stuurt je Machine ons team een korte, anonieme melding over de fout. Zo kunnen we die oplossen voordat iemand er melding van maakt. Dit staat standaard aan en vereist [The Machine Network](/network).

## Wat wordt verstuurd

Per soort fout alleen dit:

- de soort fout, zoals `KeyError`;
- de melding, nadat alle specifieke gegevens zijn verwijderd: getallen, ID's, geciteerde tekst, e-mailadressen, links, bestandspaden, sleutels en woorden die een naam kunnen zijn;
- waar de fout in de eigen code van The Machine optrad, nooit een map op je computer;
- de appversie, hoe vaak de fout optrad en wanneer dat voor het eerst en het laatst gebeurde.

Bijvoorbeeld: `IndexError`, `list index out of range`, op `machine/faults.py:fault_event:246`, versie `05b17ee6ac79`, 1 keer.

## Wat nooit wordt verstuurd

De inhoud van je berichten, to-do's, concepten of chats. Namen, e-mailadressen, telefoonnummers, links of wachtwoorden. Om welk account of welke persoon het ging.

## Waar fouten vandaan komen

- werk op de achtergrond: nieuwe berichten controleren, to-do's voorbereiden, chats, Koppelingen en synchronisaties;
- het dashboard, in je browser of de app, inclusief fouten die daar aan je zijn getoond;
- mislukte of verlopen verzoeken vanuit het dashboard: welk verzoek het was, nooit wat het verstuurde;
- mislukte opdrachten van codeeragents: alleen de tool en het soort fout.

Herhaalde exemplaren van dezelfde fout worden geteld, niet opnieuw verstuurd. Er wordt maximaal één batch per 10 minuten verstuurd. We bewaren de foutrapporten 30 dagen.

## Beperking

Werk op de achtergrond wordt gepauzeerd als de limieten van je AI-abonnement bijna zijn bereikt. Zo blijft er ruimte over voor je eigen chats (zie [Je AI-model](model.md)).

Als foutrapporten aanstaan, laat je Machine ons ook één keer per dag weten hoe vaak dit is gebeurd: per pauze het uur, welke limiet, hoe lang de pauze duurde en hoeveel opdrachten moesten wachten. Niet waar die opdrachten over gingen.

## Uitzetten

Ga naar **Instellingen** en **Beveiliging** en zet **Foutrapporten sturen** uit. Er wordt niets meer vastgelegd of verstuurd en wat nog klaarstond, wordt verwijderd. Fouten worden nog wel op je eigen Machine getoond. Je Machine kan een oplossing voorstellen.

Zie [Beveiliging en privacy](security-and-privacy.md).
