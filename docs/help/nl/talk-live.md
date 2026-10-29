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

De balk heeft **Dempen** en **Einde**. Zeg gedag, of dat je klaar bent, en hij stopt vanzelf. Een gesprek duurt hoogstens 10 minuten. Een minuut voor het einde toont de timer hoeveel tijd er nog is. Start opnieuw om verder te gaan.

## Al je to-do's doorpraten

Tik op **Praten** in de zijbalk (in het menu op een telefoon) om alles wat op je wacht met je stem te overlopen. The Machine zegt hoeveel er wachten en neemt ze een voor een door: eerst **Klaar**, dan **Te beslissen**. Praten heeft een eigen pagina: één gesprek van begin tot einde, met bovenaan de to-do waarover hij praat, het concept en **Chat openen**. Hij springt niet van chat naar chat.

Vraag hem een concept voor te lezen, aan te passen, te snoozen, als klaar te markeren of naar de volgende te gaan. Versturen werkt zoals in de chat van een to-do: één concept per vraag, na een duidelijke ja. Wat je over een to-do zegt, komt in de chat van die to-do. Komt er een nieuwe to-do binnen, dan meldt hij die bij een pauze.

Je kunt intussen naar een andere pagina: de balk blijft onderaan, en **Praten** in de zijbalk brengt je terug. Dit gesprek duurt hoogstens 30 minuten.

## Vraag dingen, en verstuur met een ja

Als je iets vraagt, zoals "schrijf een antwoord dat donderdag past" of "snooze dit tot maandag", geeft The Machine het door aan de chat van de to-do, alsof je het zelf typte. De chat volgt zijn gewone regels: hij kan het concept aanpassen of de to-do snoozen.

De chat kan ook dingen opzoeken, zoals de openingsuren van een winkel op het web. Intussen toont hij **Ermee bezig…**, en je kan gewoon verder praten. Als het antwoord klaar is, zegt The Machine het je, en waar hij het vond. Vraag je intussen iets anders, dan wacht dat zijn beurt af.

Wil je een concept versturen, zeg het dan. The Machine vraagt het eerst, met wie het krijgt en hoe, zoals "Dit antwoord per e-mail naar Lotte sturen?". Op een telefoon leest hij eerst het hele concept voor. Antwoord met een duidelijke ja, in elke taal, en dat ene concept gaat weg.

- Hij vraagt het alleen voor het concept dat in de chat staat. Verandert het concept na de vraag, dan vraagt hij het opnieuw.
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
