---
title: Live praten
area: cards
summary: Een gesproken gesprek met The Machine over een to-do, met de stem van OpenAI. Hij werkt in de chat van de to-do, maar verstuurt nooit iets.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Een gesprek starten

Tik in de chat van een to-do op de golf naast de microfoon. Sta de microfoon toe als je browser erom vraagt. Als de balk **Live** toont, praat je zoals bij een telefoongesprek. The Machine antwoordt hardop, en je kunt erdoorheen praten om hem te onderbreken.

Hij kent de to-do waarin je zit: de berichten, het concept en de chat. Hij kan ook je andere to-do's opzoeken.

De balk heeft **Dempen** en **Einde**. Een gesprek duurt hoogstens 10 minuten. Een minuut voor het einde toont de timer hoeveel tijd er nog is. Start opnieuw om verder te gaan.

## Vanuit een gesprek wordt niets verstuurd

Als je iets vraagt, zoals "schrijf een antwoord dat donderdag past" of "snooze dit tot maandag", geeft The Machine het door aan de chat van de to-do, alsof je het zelf typte. De chat volgt zijn gewone regels: hij kan het concept aanpassen of de to-do snoozen, maar een concept wacht op je **Goedkeuren**.

"Ja" of "verstuur het" zeggen doet niets. Alleen je tik op **Goedkeuren** verstuurt.

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
