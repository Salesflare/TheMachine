---
title: Live praten
area: cards
summary: Een gesproken gesprek met The Machine over een to-do, met de stem van OpenAI. Hij werkt in de chat van de to-do en verstuurt een concept pas als je er ja op zegt.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Een gesprek starten

Tik in de chat van een to-do op de golf naast de microfoon. Sta de microfoon toe als je browser erom vraagt. Als de balk **Live** toont, praat je zoals bij een telefoongesprek. The Machine antwoordt hardop, en je kunt erdoorheen praten om hem te onderbreken.

Hij kent de to-do waarin je zit: de berichten, het concept en de chat. Hij kan ook je andere to-do's opzoeken.

Er wordt geluisterd in jouw talen: die van de app en die je browser opgeeft. Een geluid, een kuch of een klank in een andere taal krijgt geen antwoord en komt niet in het verslag.

De balk heeft **Dempen** en **Einde**. Zeg gedag, of dat je klaar bent, en hij stopt vanzelf. Een gesprek duurt hoogstens 10 minuten. Een minuut voor het einde toont de timer hoeveel tijd er nog is. Start opnieuw om verder te gaan.

## Al je to-do's doorpraten

Tik op **Praten** in de zijbalk (in het menu op een telefoon) om alles wat op je wacht met je stem te overlopen. The Machine zegt hoeveel er wachten en neemt ze een voor een door: eerst **Klaar**, dan **Te beslissen**. Hij ziet ook je andere to-do's, zoals die nog **Wordt voorbereid**, en zegt het als er een klaar is.

Praten heeft een eigen pagina: één gesprek van begin tot einde, met bovenaan de to-do waarover hij praat, het concept en **Chat openen**. Hij springt niet van chat naar chat.

Vraag hem een concept voor te lezen, aan te passen, te snoozen, als klaar te markeren of naar de volgende te gaan. Versturen werkt zoals in de chat van een to-do: één concept per vraag, na een duidelijke ja. Wat je over een to-do zegt, komt in de chat van die to-do. Komt er een nieuwe to-do binnen, dan meldt hij die bij een pauze. Zeg "maak een to-do om..." en hij maakt een nieuwe, zonder de huidige te verlaten.

Hij kan ook bij de rest van The Machine. Vraag naar een persoon, een organisatie, een project, een afspraak of een belofte, en hij zoekt het op en toont het. Hij kan een to-do snoozen, als klaar markeren, afwijzen, hernoemen of weer openen, ook een onder **Gedaan / afgewezen**. Voor al de rest maakt hij een to-do, laat de chat ervan het doen en zegt je het antwoord.

Je kunt intussen naar een andere pagina: de balk blijft onderaan, en **Praten** in de zijbalk brengt je terug. Dit gesprek duurt hoogstens 30 minuten. Op computers en Android loopt het door op de achtergrond. Op een iPhone stopt het als de app van het scherm gaat.

## Vraag dingen, en verstuur met een ja

Als je iets vraagt, zoals "schrijf een antwoord dat donderdag past" of "snooze dit tot maandag", geeft The Machine het door aan de chat van de to-do, alsof je het zelf typte. De chat volgt zijn gewone regels: hij kan het concept aanpassen of de to-do snoozen.

De chat kan ook dingen opzoeken, zoals de openingsuren van een winkel op het web. Intussen toont hij **Ermee bezig…**, en je kan gewoon verder praten. Als het antwoord klaar is, zegt The Machine het je, en waar hij het vond. Vraag je intussen iets anders, dan wacht dat zijn beurt af.

Wil je een concept versturen, zeg het dan. The Machine vraagt het eerst, met wie het krijgt en hoe, zoals "Dit antwoord per e-mail naar Lotte sturen?". Eerst leest hij het hele concept voor: naar wie het gaat, het onderwerp en de tekst. Zo werkt het ook met je telefoon in je zak. Antwoord met een duidelijke ja, in elke taal, en dat ene concept gaat weg.

- Hij verstuurt precies het concept dat hij voorlas. Verandert het na de vraag, dan leest hij het opnieuw voor en vraagt hij het opnieuw. Een vraag die je niet binnen 3 minuten beantwoordt, vervalt.
- Is je antwoord geen duidelijke ja, dan gaat er niets weg en vraagt hij het opnieuw. "Nee" verstuurt niets.
- Eén ja verstuurt altijd één concept. Wil je er meerdere versturen, gebruik dan de follow-upreview.
- De chat toont een paar seconden **Goedgekeurd met je stem** met **Ongedaan maken** voor het weggaat.

Je kunt altijd ook op **Goedkeuren** tikken.

## Kies een stem

Kies in **Instellingen**, **Algemeen**, onder **Spraakinvoer**, bij **Stem** hoe The Machine klinkt. Tik op afspelen om een voorbeeld te horen. **Cedar** is de standaard. De stem Cove van ChatGPT is niet beschikbaar voor Live praten.

## Een verslag in de chat

Wat jullie allebei zeggen, wordt in de chat van de to-do geschreven, onder een regel **Live gepraat**. Je kunt het later teruglezen.

## Wat je nodig hebt

Live praten gebruikt de realtime stem van OpenAI, dus OpenAI moet ingesteld zijn in OpenClaw:

- Een ChatGPT-login: inbegrepen in je abonnement, als je abonnement er toegang toe heeft.
- Een OpenAI API-sleutel: OpenAI rekent je sleutel per gespreksminuut aan, en de balk zegt dat. Als beide zijn ingesteld, gebruikt OpenClaw de sleutel.

**Instellingen**, **Algemeen**, **Spraakinvoer** toont of Live praten klaar is. Zonder OpenAI verschijnt de golf niet. Je audio gaat van je browser rechtstreeks naar OpenAI. Je sleutel komt nooit in de browser.

## Als het niet werkt

- **De microfoon is geblokkeerd**: sta de microfoon toe voor deze site in de instellingen van je browser.
- **Live praten kon niet starten**: controleer OpenAI in OpenClaw en probeer opnieuw.
- **Live praten verloor de verbinding**: start opnieuw. Wat tot nu toe gezegd is, blijft in de chat.
