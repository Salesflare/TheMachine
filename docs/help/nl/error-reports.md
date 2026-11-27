---
title: Foutrapporten
area: security
summary: Als er iets misgaat, vertelt je Machine het team van The Machine wat er misging en waar in de code. Nooit je berichten, namen of adressen.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: d474cfa6bcefd25a
---
## Wat het is

Als er iets misgaat in The Machine, stuurt je Machine ons team een korte, anonieme melding over de fout. Zo kunnen we het probleem oplossen voordat iemand het meldt. Dit staat standaard aan en vereist [The Machine Network](/network).

## Wat wordt verstuurd

Alleen dit, per type fout:

- het type fout, zoals `KeyError`;
- de foutmelding, zonder specifieke informatie zoals cijfers, ID's, geciteerde tekst, e-mailadressen, links, bestandspaden, sleutels en woorden die een naam kunnen zijn;
- waar in de eigen code van The Machine de fout optrad, nooit een map op je computer;
- de appversie, hoe vaak de fout optrad en wanneer dat voor het eerst en het laatst was.

Bijvoorbeeld: `IndexError`, `list index out of range`, op `machine/faults.py:fault_event:246`, versie `05b17ee6ac79`, 1 keer.

## Wat nooit wordt verstuurd

De inhoud van je berichten, to-do's, concepten of chats. Namen, e-mailadressen, telefoonnummers, links of wachtwoorden. Om welk account of welke persoon het ging.

## Waar fouten vandaan komen

- werk op de achtergrond: nieuwe berichten controleren, to-do's voorbereiden, chats, koppelingen en synchronisaties;
- het dashboard in je browser of de app, inclusief fouten die daar worden getoond;
- mislukte of verlopen verzoeken vanuit het dashboard: om welk verzoek het gaat, nooit wat het heeft verstuurd;
- mislukte taken van codeeragents: alleen de tool en het type fout;
- de korte test van je AI als die mislukt: de fout van de AI, zonder specifieke informatie.

Een controle die stopt omdat je AI-abonnement de gebruikslimiet heeft bereikt, is geen fout en wordt niet verstuurd. De controle wacht tot de limiet is gereset. Ook een controle die mislukt omdat je AI is uitgelogd, is geen fout: **Wacht op jou** vraagt je om opnieuw in te loggen.

Een connector die je zelf hebt toegevoegd (je eigen bestand in `connectors/`) verstuurt alleen de naam van de dienst en het foutlabel, zoals `notes` en `notes_http: HTTP unauthorized`, zodat we kunnen helpen het probleem op te lossen. Er wordt verder niets uit de code verstuurd. Op de kaart van de koppeling staat de volledige fout.

Herhaalde fouten worden geteld, maar niet opnieuw verstuurd. Er wordt maximaal één batch per 10 minuten verstuurd. We bewaren die 30 dagen.

## Tempo

Als de limieten van je AI-abonnement bijna bereikt zijn, wacht werk op de achtergrond. Zo blijft er ruimte voor je eigen chats (zie [Je AI-model](model.md)).

Als foutrapporten aanstaan, laat je Machine ons ook eenmaal per dag weten hoe vaak dit gebeurde: per pauze het uur, welke limiet werd bereikt, hoelang de pauze duurde en hoeveel taken wachtten. Er wordt niets verteld over de taken zelf.

## Uitzetten

Ga naar **Instellingen** en kies **Beveiliging**. Zet **Foutrapporten versturen** uit. Er wordt niets meer vastgelegd of verstuurd en wat nog klaarstond, wordt verwijderd. Fouten blijven zichtbaar op je eigen Machine, waar je een oplossing kunt krijgen.

Zie [Beveiliging en privacy](security-and-privacy.md).
