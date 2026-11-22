---
title: Gezondheid van je Machine
area: connections
summary: Het eigen logboek van je Machine, zodat hij problemen zelf opmerkt. Hij leest alleen mee.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 7d66ff6a6a5d5b1d
---
## Wat hij leest

Het eigen logboek van je Machine: mislukte uitvoeringen, geweigerde overdrachten, Telegram-berichten die niet zijn verstuurd en fouten van The Machine zelf. Een to-do laat je weten wanneer er iets moet worden opgelost. Op je eigen computer staat daar ook **Rond de installatie van de laatste update af** bij: voor één onderdeel van een update is 's nachts een korte herstart nodig, maar dat is een paar nachten niet gelukt. Vraag het in zijn chat, dan maakt The Machine het af. De to-do verdwijnt vanzelf zodra dat onderdeel is geïnstalleerd.

## Fixes die een update opzij heeft gezet

Wanneer The Machine een update uitvoert en een van zijn eigen fixes niet meer bij de nieuwe versie past, zet de update die fix opzij en gaat verder. Zo blijft je Machine nooit op een oude versie staan. Een to-do, **Doe een fix opnieuw die de update opzij zette**, vermeldt om welke fix het gaat.

Met **Opnieuw doen** laat je je Machine de fix opnieuw maken voor de nieuwe versie, net als bij elke eigen fix: je ziet de wijziging en tikt op **Fix mergen**. Zodra de fix is samengevoegd, wordt de oude versie verwijderd. Of sluit de to-do.

## Je eigen bestanden die een update heeft behouden

Als een nieuwe versie een bestand bevat met dezelfde naam als een bestand dat je zelf hebt toegevoegd, geeft de update jouw bestand een andere naam in plaats van het te overschrijven, en gaat verder. Een to-do vermeldt hoeveel bestanden zijn behouden en geeft van elk de oude en nieuwe naam. Sluit de to-do zodra je ze hebt gecontroleerd.

## Wat hij kan doen

Niets. Hij leest alleen het logboek op je eigen Machine.

## Koppelen

- Op een gehoste Machine staat het op je installatiepagina, onder **Meer bronnen**, als Gezondheid van je Machine. Eén per Machine.
- Op je eigen computer: **Koppelingen**, **Andere**, Gezondheid van je Machine. Of voer `assistant connect gateway` uit.

## Verwijderen

- In het dashboard: **Koppelingen**, open de koppeling en kies **Details** en daarna **Ontkoppelen**.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je installatiepagina.

Je hoeft het nergens anders te verwijderen.
