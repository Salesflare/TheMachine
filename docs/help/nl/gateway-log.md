---
title: Machine-status
area: connections
summary: Het eigen logboek van je Machine, zodat hij problemen zelf opmerkt. Hij leest alleen.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 3a06400a28396465
---
## Wat er wordt gelezen

Het eigen logboek van je Machine: mislukte uitvoeringen, geweigerde overdrachten, Telegram-berichten die niet zijn verstuurd en fouten van The Machine zelf. Een to-do laat je weten wanneer er iets moet worden opgelost. Op je eigen computer staat daar ook **Maak de laatste update af** bij: één onderdeel van een update heeft 's nachts een korte herstart nodig, maar dat lukte een paar nachten niet. Vraag het in de chat van je Machine en The Machine maakt het af. De to-do wordt vanzelf gesloten zodra dat onderdeel is geïnstalleerd.

## Fixes die een update opzij heeft gezet

Als The Machine wordt bijgewerkt en een van zijn eigen fixes niet meer past bij de nieuwe versie, zet de update die fix opzij en gaat hij verder. Zo blijft je Machine altijd op de nieuwste versie. Een to-do met de naam **Doe een fix opnieuw die de update opzij zette** vermeldt om welke fix het gaat.

Met **Doe opnieuw** laat je je Machine de fix opnieuw maken voor de nieuwe versie, net als bij elke eigen fix: je bekijkt de wijziging en tikt op **Fix samenvoegen**. Zodra de fix is samengevoegd, wordt de oude kopie verwijderd. Je kunt de to-do ook sluiten.

## Je eigen bestanden die een update heeft behouden

Als een nieuwe versie een bestand bevat met dezelfde naam als een bestand dat je zelf hebt toegevoegd, hernoemt de update jouw bestand in plaats van het te overschrijven. Daarna gaat de update verder. Een to-do vermeldt hoeveel bestanden zijn behouden en geeft van elk bestand de oude en de nieuwe naam. Sluit de to-do zodra je ze hebt gecontroleerd.

## Wat het kan doen

Niets. Het leest alleen het logboek op je eigen Machine.

## Koppelen

- Op een gehoste Machine staat het op je installatiepagina, onder **Meer bronnen**, als Gezondheid van Machine. Eén per Machine.
- Op je eigen computer: voer `assistant connect gateway` uit.

## Verwijderen

- In het dashboard: **Koppelingen**, open de koppeling en kies **Details** en daarna **Ontkoppelen**.
- Op een gehoste Machine kun je ook op **Verwijderen** naast de koppeling op je installatiepagina klikken.

Je hoeft het nergens anders te verwijderen.
