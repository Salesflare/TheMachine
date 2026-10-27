---
title: Foutrapporten
area: security
summary: Als er iets stukgaat, vertelt je Machine het team van The Machine wat er misging en waar in de code. Nooit je berichten, namen of adressen.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html
order: 4
---
## Wat het is

Als er in The Machine iets stukgaat, stuurt je Machine het team een korte handtekening van de fout, zodat we die kunnen oplossen voor iemand ze moet melden. Het staat standaard aan en heeft [The Machine Network](/network) nodig.

## Wat er meegaat

Alleen dit, per soort fout:

- het soort fout, zoals `KeyError` of `TypeError`;
- de melding ervan, met alles wat specifiek is eruit gehaald: getallen, id's, geciteerde tekst, e-mailadressen, links, bestandspaden en alles wat op een sleutel lijkt. Elk ander woord dat een naam kan zijn, gaat er ook uit;
- waar het gebeurde in de eigen code van The Machine: bestand, functie en regel, nooit een map op je computer;
- de versie van de app, hoe vaak het gebeurde, en wanneer de eerste en de laatste keer.

Een echt voorbeeld: `IndexError`, `list index out of range`, bij `assistant.py:fault_event:7899`, versie `05b17ee6ac79`, 1 keer.

## Wat nooit meegaat

Wat er in je berichten, to-do's, concepten of chats staat. Namen, e-mailadressen, telefoonnummers, links, tokens of wachtwoorden. Over welk account of welke persoon het ging.

## Waar fouten vandaan komen

- de service en zijn taken: reviews, to-do's voorbereiden, chat, koppelingen en syncs;
- het dashboard in je browser;
- taken van Claude Code en Codex die mislukken: alleen de tool en het soort fout.

Dezelfde fout telt één keer, met een aantal. Hooguit één batch per 10 minuten. Het team bewaart ze 30 dagen.

## Pacing

Werk op de achtergrond wacht als de limieten van je AI-abonnement bijna op zijn, zodat er ruimte blijft voor je eigen chats (zie [Model](model.md)). Reviews van wat binnenkwam wachten alleen vlak bij de limieten; zwaarder werk, zoals je geschiedenis doorlopen, wordt over de week verdeeld.

Met foutrapporten aan vertelt je Machine het team ook, één keer per dag, hoe vaak dat gebeurde: per keer het uur waarop het begon, welke limiet, hoeveel minuten het duurde en hoeveel taken wachtten. Alleen aantallen en minuten, niets over wat die taken waren.

## Uitzetten

Zet in Instellingen, Beveiliging **Foutrapporten sturen** uit. Er wordt niets meer bijgehouden of verstuurd, ook geen pacingtellingen, en wat nog wachtte, wordt verwijderd. Fouten verschijnen nog steeds op je eigen Machine, die een oplossing kan voorstellen.

Zie [Beveiliging en privacy](security-and-privacy.md).
