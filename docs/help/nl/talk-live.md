---
title: Live praten
area: cards
summary: Een gesproken gesprek met The Machine over een to-do, met de stem van OpenAI. Het werkt in de chat van de to-do en verstuurt een concept pas nadat je daar ja op zegt.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: da63957f0556ff4f
---
## Een gesprek beginnen

Tik in de chat van een to-do op de golf naast de microfoon en geef toestemming voor de microfoon als daarom wordt gevraagd. Praat zodra de balk **Live** aangeeft, net als tijdens een telefoongesprek. The Machine antwoordt hardop. Praat erdoorheen om hem te onderbreken.

The Machine kent deze to-do: de berichten, het concept en de chat. Hij kan ook je andere to-do's opzoeken. Zeg bijvoorbeeld ‘markeer dit als gedaan’, ‘snooze dit tot morgen om 9 uur’ of ‘niet nodig’ en hij doet het. Zeg meteen daarna ‘nee, niet dat’ om het ongedaan te maken. Tijden volgen de tijdzone van je [Werkuren](work-hours.md).

The Machine luistert in de taal van de app en in de talen die je browser vermeldt. Op hoesten, lawaai en andere talen reageert hij niet. Die komen ook niet in het transcript.

De balk heeft **Dempen** en **Beëindigen**. Zeg gedag en het gesprek wordt vanzelf beëindigd. Een gesprek duurt maximaal 10 minuten. In de laatste minuut zie je een aftelling. Begin opnieuw om verder te praten.

## Praten over al je to-do's

Tik op **Praten** in de zijbalk (op een telefoon vind je dit in het menu). The Machine vertelt hoeveel to-do's er wachten en neemt de to-do's onder **Voor jou** een voor een door, in de volgorde van je lijst. Hij laat weten wanneer een to-do met de status **Aan het voorbereiden…** klaar is.

Praten heeft een eigen pagina. De to-do waar je mee bezig bent staat bovenaan, samen met het concept en **Chat openen**.

Vraag The Machine om een concept voor te lezen of aan te passen, een to-do te snoozen of als gedaan te markeren, of om naar de volgende te gaan. Wat je over een to-do zegt, komt in de chat ervan. Bij een pauze noemt The Machine nieuwe to-do's. Zeg ‘voeg een to-do toe voor...’ om er een toe te voegen zonder je plek te verliezen.

Vraag naar een persoon, organisatie, project, meeting of belofte. The Machine zoekt die op en laat de informatie zien. Hij kan ook to-do's afwijzen, hernoemen of opnieuw openen, ook to-do's onder **Gedaan / afgewezen**. Voor andere vragen stuurt hij je vraag naar de chat van een nieuwe to-do en vertelt hij je het antwoord.

The Machine onthoudt je eerdere gesprekken met hem. Vraag bijvoorbeeld ‘wat heb ik besloten over de offsite?’ en hij vertelt het je, en wanneer je dat zei. Alleen Praten in de zijbalk kan dit.

Je kunt ondertussen andere pagina's openen. De balk blijft onderaan staan en met **Praten** ga je terug. Dit gesprek duurt maximaal 30 minuten. Op computers en Android blijft het op de achtergrond doorgaan. Op iPhone stopt het als de app niet meer op het scherm staat.

## Vraag om iets en verstuur het na bevestiging

Vraag bijvoorbeeld ‘schrijf een antwoord waarin staat dat donderdag goed uitkomt’. The Machine stuurt je verzoek naar de chat van de to-do, alsof je het zelf hebt getypt. De chat volgt de gebruikelijke regels.

De chat kan ook dingen opzoeken, zoals de openingstijden van een winkel. Je ziet dat hij bezig is en kunt ondertussen blijven praten. Zodra het antwoord klaar is, vertelt The Machine je het antwoord en waar hij het heeft gevonden.

Zeg dat je een concept wilt versturen. The Machine leest het hardop voor (de ontvanger, het onderwerp en de tekst) en vraagt bijvoorbeeld: ‘Deze reactie per e-mail naar Sam versturen?’ Je kunt je telefoon gewoon in je zak laten zitten. Zeg duidelijk ja, bijvoorbeeld ‘ja, verstuur maar’, en het concept wordt verstuurd.

- The Machine verstuurt precies het concept dat hij heeft voorgelezen. Als het concept verandert, leest hij het opnieuw voor en vraagt hij opnieuw om bevestiging. Een vraag waarop je niet binnen 3 minuten antwoordt, verloopt.
- Zonder duidelijk ja wordt er niets verstuurd.
- Een concept dat je al hebt gezien of gehoord, wordt niet opnieuw voorgelezen. The Machine vraagt alleen bijvoorbeeld: ‘Naar Pat versturen?’.
- Zeg ‘verstuur alle klaargezette’ en The Machine noemt iedereen in één vraag. Met één keer ja verstuurt hij ze allemaal.
- Na je bevestiging toont Praten **Ongedaan maken** met een aftelling. Tik erop of zeg ‘ongedaan maken’ of ‘wacht’.
- Na het versturen zegt Praten ‘Verstuurd.’ De to-do toont **Verstuurd naar** die persoon, met het tijdstip. Als het versturen niet lukt, vertelt Praten waarom. Vraag op elk moment ‘is het verstuurd?’: The Machine controleert het en doet geen aannames.

Tik op **Goedkeuren** kan ook.

Zeg ‘doe het’ om The Machine aan de to-do te laten beginnen, net als met **Doe het**. Zeg ‘een bug melden’ om een bugrapport te versturen, net als met **Een bug melden** onder Help.

## Een stem kiezen

Kies onder **Instellingen**, **Algemeen** en **Spraakinvoer** een **Stem** en tik op afspelen om die te horen. **Cedar** is de standaardstem. De Cove-stem van ChatGPT is niet beschikbaar.

## Een verslag in de chat

Alles wat je zegt, komt onder de regel **Live gepraat** in de chat van de to-do te staan, zodat je het later kunt teruglezen.

## Wat je nodig hebt

Live praten gebruikt de stem van OpenAI. Je Machine heeft daarom een van deze dingen nodig:

- Een ChatGPT-login: inbegrepen bij abonnementen die dit aanbieden.
- Een OpenAI API-sleutel: OpenAI brengt kosten per minuut in rekening. De balk laat dat weten. Als je beide hebt, gebruikt je Machine de sleutel.

Onder **Instellingen**, **Algemeen** en **Spraakinvoer** zie je of Live praten klaar is. Zonder OpenAI wordt de golf niet weergegeven. Je audio gaat vanuit je browser rechtstreeks naar OpenAI.

## Als het niet werkt

- **De microfoon is geblokkeerd**: geef deze site toestemming voor de microfoon via de instellingen van je browser.
- **Live praten kon niet starten**: controleer je ChatGPT-login of OpenAI-sleutel en probeer het opnieuw.
- **Live praten heeft de verbinding verloren**: begin opnieuw. Wat je hebt gezegd, blijft in de chat staan.
- The Machine zegt dat hij je niet kan verstaan: controleer je microfoon of typ in de chat.
