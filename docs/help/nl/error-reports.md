---
title: Foutrapporten
area: security
summary: Als er iets misgaat, laat je Machine het team van The Machine weten wat er misging en waar in de code. Nooit je berichten, namen of adressen.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 2253a0d695fe898c
---
## Wat het is

Als er iets misgaat in The Machine, stuurt je Machine ons team een kort, anoniem bericht over de fout. Zo kunnen we het probleem oplossen voordat iemand het meldt. Dit staat standaard aan en vereist [The Machine Network](/network).

## Wat er wordt verstuurd

Alleen deze gegevens, per soort fout:

- het soort fout, zoals `KeyError`;
- het foutbericht, zonder specifieke gegevens zoals nummers, id's, geciteerde tekst, e-mailadressen, links, bestandspaden, sleutels en woorden die een naam kunnen zijn;
- waar in de eigen code van The Machine de fout is opgetreden, nooit een map op je computer;
- de appversie, hoe vaak de fout is opgetreden en wanneer dat voor het eerst en het laatst gebeurde.

Bijvoorbeeld: `IndexError`, `list index out of range`, op `machine/faults.py:fault_event:246`, versie `05b17ee6ac79`, 1 keer.

## Wat nooit wordt verstuurd

Wat er in je berichten, to-do's, concepten of chats staat. Namen, e-mailadressen, telefoonnummers, links of wachtwoorden. Om welk account of welke persoon het ging.

## Waar fouten vandaan komen

- achtergrondtaken: nieuwe berichten controleren, to-do's voorbereiden, chat, koppelingen en synchronisaties;
- het dashboard, in je browser of de app, inclusief fouten die daarin worden getoond;
- mislukte of verlopen verzoeken vanuit het dashboard: welk verzoek, nooit wat het heeft verstuurd;
- mislukte taken van coding agents: alleen de tool en het soort fout;
- de korte test van je AI als die mislukt: de fout van de AI, zonder specifieke gegevens.

Een connector die je zelf hebt toegevoegd (je eigen bestand in `connectors/`) verstuurt alleen de naam van de service en het foutlabel, zoals `notes` en `notes_http: HTTP unauthorized`, zodat we kunnen helpen het probleem op te lossen. Er wordt verder niets uit de code verstuurd. Op de kaart van de koppeling staat de volledige fout.

Herhaalde exemplaren van dezelfde fout worden geteld, niet opnieuw verstuurd. Er wordt maximaal één batch per 10 minuten verstuurd. We bewaren de gegevens 30 dagen.

## Achtergrondwerk en limieten

Achtergrondwerk wordt gepauzeerd als de limieten van je AI-plan bijna zijn bereikt. Zo blijft er ruimte voor je eigen chats (zie [Je AI-model](model.md)).

Als foutrapporten aanstaan, laat je Machine ons ook één keer per dag weten hoe vaak dat gebeurde. Per pauze wordt vermeld: het uur, welke limiet was bereikt, hoe lang de pauze duurde en hoeveel taken moesten wachten. Er wordt niets verstuurd over de inhoud van die taken.

## Uitzetten

Ga naar **Instellingen** en vervolgens naar **Beveiliging**. Zet **Foutrapporten versturen** uit. Er worden dan geen nieuwe gegevens vastgelegd of verstuurd en gegevens die klaarstonden, worden verwijderd. Fouten zijn nog wel zichtbaar op je eigen Machine, die een oplossing kan voorstellen.

Zie [Beveiliging en privacy](security-and-privacy.md).
