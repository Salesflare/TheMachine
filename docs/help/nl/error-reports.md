---
title: Foutrapporten
area: security
summary: Als er iets misgaat, vertelt je Machine het team van The Machine wat er misging en waar in de code. Nooit je berichten, namen of adressen.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: e1d4d602255cde39
---
## Wat wordt verstuurd

Als er iets misgaat in The Machine, stuurt je Machine ons team een kort, anoniem bericht over de fout. Zo kunnen we het probleem oplossen voordat iemand het meldt. Dit staat standaard aan en vereist [The Machine Network](/network).

## Wat wordt verstuurd

Per soort fout wordt alleen dit verstuurd:

- de soort fout, zoals `KeyError`;
- het foutbericht, waaruit specifieke gegevens zijn verwijderd: getallen, ID's, geciteerde tekst, e-mailadressen, links, bestandspaden, sleutels en woorden die een naam kunnen zijn;
- waar in de eigen code van The Machine de fout is opgetreden, nooit een map op je computer;
- de appversie, hoe vaak de fout is opgetreden en wanneer dat voor het eerst en het laatst was.

Bijvoorbeeld: `IndexError`, `list index out of range`, bij `machine/faults.py:fault_event:246`, versie `05b17ee6ac79`, 1 keer.

## Wat nooit wordt verstuurd

De inhoud van je berichten, to-do's, concepten of chats. Namen, e-mailadressen, telefoonnummers, links of wachtwoorden. Om welk account of welke persoon het ging.

## Waar fouten vandaan komen

- achtergrondtaken: nieuwe berichten controleren, to-do's voorbereiden, chatten, Koppelingen en synchronisaties;
- het dashboard, in je browser of de app, inclusief fouten die je te zien kreeg;
- mislukte of verlopen aanvragen vanuit het dashboard: welke aanvraag, nooit wat die heeft verstuurd;
- mislukte taken van codeeragenten: alleen de tool en de soort fout;
- de korte test van je AI als die mislukt: de fout van de AI, zonder specifieke gegevens.

Een controle die stopt omdat je de gebruikslimiet van je AI-plan hebt bereikt, is geen fout en wordt niet verstuurd. De controle wacht tot de limiet opnieuw is ingesteld.

Een connector die je zelf hebt toegevoegd (je eigen bestand in `connectors/`) verstuurt alleen de naam van de service en het foutlabel, zoals `notes` en `notes_http: HTTP unauthorized`, zodat we kunnen helpen het probleem op te lossen. Verder wordt niets uit de code verstuurd. De kaart van de koppeling toont de volledige fout.

Dezelfde fout wordt niet opnieuw verstuurd, maar wel geteld. Er wordt hoogstens één batch per 10 minuten verstuurd. We bewaren de rapporten 30 dagen.

## Spreiding

Achtergrondtaken wachten als de limieten van je AI-plan bijna bereikt zijn, zodat er ruimte blijft voor je eigen chats (zie [Je AI-model](model.md)).

Als foutrapporten aanstaan, vertelt je Machine ons ook één keer per dag hoe vaak dat is gebeurd: per pauze het uur, de betreffende limiet, hoe lang de pauze duurde en hoeveel taken hebben gewacht. Niet wat die taken deden.

## Uitschakelen

Schakel in **Instellingen** onder **Beveiliging** de optie **Foutrapporten versturen** uit. Er worden dan geen nieuwe gegevens vastgelegd of verstuurd en gegevens die nog klaarstonden, worden verwijderd. Fouten blijven zichtbaar op je eigen Machine. Die kan een oplossing voorstellen.

Zie [Beveiliging en privacy](security-and-privacy.md).
