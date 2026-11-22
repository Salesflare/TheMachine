---
title: Live praten
area: cards
summary: Een gesproken gesprek met The Machine over een to-do, met de stem van OpenAI. Hij werkt in de chat van de to-do en verstuurt een concept pas als je er ja op zegt.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: 60168384f08de74e
---
## Een gesprek starten

Tik in de chat van een to-do op de golf naast de microfoon. Sta de microfoon toe als je browser erom vraagt. Als de balk **Live** toont, praat je zoals bij een telefoongesprek. The Machine antwoordt hardop, en je kunt erdoorheen praten om hem te onderbreken.

Hij kent deze to-do: de berichten, het concept en de chat, en hij kan je andere to-do's opzoeken. Zeg "markeer dit als gedaan", "snooze het tot morgen om 9 uur" of "niet nodig" en hij doet het. Zeg meteen daarna "nee, niet dat" om het terug te draaien. Tijden volgen de tijdzone uit [Werkuren](work-hours.md).

Hij luistert in de taal van de app en de talen die je browser opgeeft. Hoesten, geluid en andere talen krijgen geen antwoord en komen niet in het verslag.

De balk heeft **Dempen** en **Einde**. Zeg gedag en hij stopt vanzelf. Een gesprek duurt hoogstens 10 minuten, met een aftelling in de laatste minuut. Start opnieuw om verder te gaan.

## Al je to-do's doorpraten

Tik op **Praten** in de zijbalk (in het menu op een telefoon). The Machine zegt hoeveel to-do's er wachten en neemt die in **Voor jou** één voor één door, de dringendste eerst. Hij zegt het als een to-do met **Aan het voorbereiden…** klaargezet is.

Praten heeft een eigen pagina: de to-do waarover het gaat staat bovenaan, met het concept en **Chat openen**.

Vraag hem een concept voor te lezen, aan te passen, te snoozen, als gedaan te markeren of naar de volgende te gaan. Wat je over een to-do zegt, komt in de chat van die to-do. Nieuwe to-do's meldt hij bij een pauze. Zeg "maak een to-do om..." en hij voegt er een toe zonder dat je je plek kwijtraakt.

Vraag naar een persoon, organisatie, project, meeting of belofte, en hij zoekt het op en toont het. Hij kan ook to-do's afwijzen, hernoemen of weer openen, ook die onder **Gedaan / afgewezen**. Voor al het andere geeft hij de vraag aan de chat van een nieuwe to-do en vertelt hij je het antwoord.

Hij onthoudt je eerdere gesprekken met hem. Vraag "wat had ik beslist over de offsite?" en hij vertelt het je, en wanneer je het zei. Alleen Praten in de zijbalk doet dit.

Je kunt intussen naar andere pagina's: de balk blijft onderaan, en **Praten** brengt je terug. Dit gesprek duurt hoogstens 30 minuten. Op computers en Android loopt het door op de achtergrond. Op een iPhone stopt het als de app van het scherm gaat.

## Vraag dingen, en verstuur met een ja

Vraag iets, zoals "schrijf een antwoord dat donderdag past", en The Machine geeft het door aan de chat van de to-do, alsof je het zelf typte. De chat volgt zijn gewone regels.

De chat kan ook dingen opzoeken, zoals de openingstijden van een winkel. Hij toont **Ermee bezig…** en je kunt gewoon verder praten. Als het antwoord klaar is, zegt The Machine het je, en waar hij het vond.

Wil je een concept versturen, zeg het dan. The Machine leest het voor (naar wie het gaat, het onderwerp en de tekst) en vraagt het, zoals "Dit antwoord per e-mail naar Sam sturen?". Zo werkt het ook met je telefoon in je zak. Zeg een duidelijke ja, zoals "ja, verstuur maar", en dat concept gaat weg.

- Hij verstuurt precies het concept dat hij voorlas. Verandert het concept, dan leest hij het opnieuw voor en vraagt hij het opnieuw. Een vraag die je niet binnen 3 minuten beantwoordt, vervalt.
- Alles behalve een duidelijke ja verstuurt niets.
- Een concept dat je al zag of hoorde, leest hij niet opnieuw voor. Hij vraagt het alleen, zoals "Naar Pat sturen?".
- Zeg "verstuur alle klaargezette" en hij noemt iedereen in één vraag. Eén ja verstuurt ze allemaal.
- Na een ja toont Praten **Ongedaan maken** met een aftelling. Tik erop, of zeg "ongedaan maken" of "wacht".
- Zodra het verstuurd is, zegt Praten "Verstuurd." en toont de to-do **Verstuurd naar** die persoon met de tijd. Mislukte het, dan zegt Praten waarom. Vraag op elk moment "is het verstuurd?": hij kijkt het na en gokt nooit.

Op **Goedkeuren** tikken werkt ook.

Zeg "doe het" om The Machine aan de to-do te laten beginnen, zoals **Doe het**. Zeg "meld een bug" om een bugmelding te sturen, zoals **Een bug melden** in Help.

## Kies een stem

Kies in **Instellingen**, **Algemeen**, onder **Spraakinvoer**, een **Stem** en tik op afspelen om hem te horen. **Cedar** is de standaard. De stem Cove van ChatGPT is niet beschikbaar.

## Een verslag in de chat

Wat jullie allebei zeggen, wordt in de chat van de to-do geschreven, onder een regel **Live gepraat**. Je kunt het later teruglezen.

## Wat je nodig hebt

Live praten gebruikt de stem van OpenAI, dus je Machine heeft een van deze nodig:

- Een ChatGPT-login: inbegrepen bij abonnementen die het aanbieden.
- Een OpenAI API-sleutel: OpenAI rekent die per minuut aan, en de balk zegt dat. Met beide gebruikt je Machine de sleutel.

**Instellingen**, **Algemeen**, **Spraakinvoer** toont of Live praten klaar is. Zonder OpenAI verschijnt de golf niet. Je audio gaat van je browser rechtstreeks naar OpenAI.

## Als het niet werkt

- **De microfoon is geblokkeerd**: sta de microfoon toe voor deze site in de instellingen van je browser.
- **Live praten kon niet starten**: controleer de ChatGPT-login of OpenAI-sleutel en probeer opnieuw.
- **Live praten verloor de verbinding**: start opnieuw. Wat tot nu toe gezegd is, blijft in de chat.
- Zegt hij dat hij je woorden niet verstaat: controleer je microfoon, of typ in de chat.
