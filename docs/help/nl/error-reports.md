---
title: Foutrapporten
area: security
summary: Als er iets misgaat, vertelt je Machine het team van The Machine wat er fout ging en waar in de code. Nooit je berichten, namen of adressen.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: f67d18a44999cfce
---
## Wat het is

Als er iets misgaat in The Machine, stuurt je Machine ons team een korte, anonieme melding over de fout. Zo kunnen we die oplossen voordat iemand hem meldt. Dit staat standaard aan en vereist [The Machine Network](/network).

## Wat er wordt verstuurd

Alleen dit, per soort fout:

- de soort fout, zoals `KeyError`;
- de melding, nadat alles wat specifiek is eruit is gehaald: getallen, id's, geciteerde tekst, e-mailadressen, links, bestandspaden, sleutels en elk woord dat een naam kan zijn;
- waar in de eigen code van The Machine de fout is opgetreden, nooit een map op je computer;
- de appversie, hoe vaak de fout is opgetreden en wanneer dat voor het eerst en het laatst was.

Bijvoorbeeld: `IndexError`, `list index out of range`, bij `machine/faults.py:fault_event:246`, versie `05b17ee6ac79`, 1 keer.

## Wat er nooit wordt verstuurd

Wat er in je berichten, to-do's, concepten of chats staat. Namen, e-mailadressen, telefoonnummers, links of wachtwoorden. Over welk account of welke persoon het ging.

## Waar fouten vandaan komen

- werk op de achtergrond: nieuwe berichten controleren, to-do's voorbereiden, chat, koppelingen en synchronisaties;
- het dashboard, in je browser of de app, inclusief fouten die het liet zien;
- verzoeken vanuit het dashboard die mislukken of een time-out krijgen: om welk verzoek het ging, nooit wat het verstuurde;
- mislukte opdrachten van codeeragents: alleen de tool en het soort fout;
- de korte test van je AI als die mislukt: de fout van de AI, nadat alles wat specifiek is eruit is gehaald.

Een connector die je zelf hebt toegevoegd (je eigen bestand in `connectors/`) verstuurt nooit foutmeldingen. Je ziet ze op de kaart van de koppeling.

Herhalingen van dezelfde fout worden geteld, maar niet opnieuw verstuurd. Er wordt maximaal één keer per 10 minuten een batch verstuurd. We bewaren die 30 dagen.

## Tempo

Achtergrondwerk wordt gepauzeerd als de limieten van je AI-abonnement bijna zijn bereikt, zodat er ruimte overblijft voor je eigen chats (zie [Je AI-model](model.md)).

Als foutrapporten aanstaan, vertelt je Machine ons ook één keer per dag hoe vaak dit is gebeurd: per pauze het uur, welke limiet, hoelang en hoeveel opdrachten hebben gewacht. Er wordt niets verteld over wat die opdrachten waren.

## Uitzetten

Ga in **Instellingen** naar **Beveiliging** en zet **Foutrapporten sturen** uit. Er wordt niets meer vastgelegd of verstuurd en alles wat klaarstond, wordt verwijderd. Fouten blijven zichtbaar op je eigen Machine, die een oplossing kan voorstellen.

Zie [Beveiliging en privacy](security-and-privacy.md).
