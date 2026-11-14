---
title: Gevolgde webpagina's
area: connections
summary: Een webpagina die je volgt. Alleen een to-do als er iets verandert dat telt.
covers: connector:web_page
code: connectors/web_page.py
---
## Wat het leest

De tekst van één openbare webpagina per koppeling, om de paar uur en hooguit één keer per uur. Menu's, footers, cookiemeldingen en advertenties laat hij weg. Als de tekst veranderde, kijkt The Machine wat er veranderde en maakt hij alleen een to-do als het telt, zoals een nieuwe prijs of een gewijzigd beleid. Datums, tellers en kleine herformuleringen geven nooit een to-do. Een ongewijzigde pagina kost niets.

Hij vraagt eerst de robots.txt van de site en laat de pagina met rust als de site nee zegt. Pagina's achter een login of die alleen met JavaScript gebouwd zijn, kun je niet volgen.

## Wat het kan doen

Niets. Het leest alleen de pagina.

## Koppelen

1. Open in het dashboard **Koppelingen**, dan **Andere**, en kies Webpagina. Of voer `assistant connect web_page` uit.
2. Plak het adres van de pagina.

Of vraag het in je chat: "Volg deze pagina voor prijswijzigingen" met het adres. Vraag welke pagina's je volgt, of om er een niet meer te volgen.

## Verwijderen

In het dashboard: **Koppelingen**, open de pagina, **Details**, dan **Ontkoppelen**. Of vraag je chat om ze niet meer te volgen.
