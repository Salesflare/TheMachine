---
title: Live praten
area: cards
summary: Een gesproken gesprek met The Machine over een to-do, met de stem van OpenAI. Je praat in de chat van de to-do. Er wordt pas een concept verstuurd nadat je daar ja op zegt.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: 60168384f08de74e
---
## Een gesprek starten

Tik in de chat van een to-do op de golf naast de microfoon en geef toegang tot je microfoon als daarom wordt gevraagd. Als de balk **Live** aangeeft, praat je alsof je aan het bellen bent. The Machine antwoordt hardop. Praat erdoorheen om hem te onderbreken.

Hij kent deze to-do: de berichten, het concept en de chat. Ook kan hij je andere to-do's opzoeken. Zeg bijvoorbeeld ‘markeer dit als gedaan’, ‘snooze het tot morgen om 9 uur’ of ‘niet nodig’ en hij voert het uit. Zeg meteen daarna ‘nee, niet die’ om het ongedaan te maken. Tijden volgen de tijdzone van je [Werkuren](work-hours.md).

Hij luistert in de taal van de app en in de talen die je browser vermeldt. Op hoesten, lawaai en andere talen antwoordt hij niet. Die komen ook niet in het transcript.

De balk bevat **Dempen** en **Einde**. Zeg gedag en het gesprek wordt vanzelf beëindigd. Een gesprek duurt maximaal 10 minuten. In de laatste minuut zie je een afteltimer. Start opnieuw om verder te gaan.

## Praten over al je to-do's

Tik op **Praten** in de zijbalk, of in het menu op je telefoon. The Machine vertelt hoeveel to-do's er klaarstaan en behandelt de to-do's onder **Voor jou** één voor één, van meest naar minst dringend. Hij laat weten wanneer een to-do met de status **Aan het voorbereiden…** klaar is.

Praten heeft een eigen pagina: de to-do waar hij mee bezig is, staat bovenaan, met het concept en **Chat openen**.

Vraag hem een concept voor te lezen of te wijzigen, een to-do te snoozen, als gedaan te markeren of naar de volgende te gaan. Wat je over een to-do zegt, komt in de chat ervan. Bij een pauze vertelt hij over nieuwe to-do's. Zeg ‘voeg een to-do toe voor...’ om er een toe te voegen zonder je plek kwijt te raken.

Vraag naar een persoon, organisatie, project, vergadering of belofte. Hij zoekt het op en laat het zien. Hij kan ook to-do's afwijzen, hernoemen of opnieuw openen, ook to-do's onder **Gedaan / afgewezen**. Voor al het andere stuurt hij de vraag naar de chat van een nieuwe to-do en vertelt hij je het antwoord.

Hij onthoudt je eerdere gesprekken met hem. Vraag ‘wat heb ik besloten over de offsite?’ en hij vertelt het je, en wanneer je dat zei. Alleen Praten in de zijbalk kan dit.

Je kunt ondertussen andere pagina's bekijken: de balk blijft onderaan staan en **Praten** brengt je terug. Dit gesprek duurt maximaal 30 minuten. Op computers en Android gaat het op de achtergrond door. Op iPhone stopt het zodra de app niet meer op het scherm staat.

## Vraag iets en verstuur het met je akkoord

Vraag bijvoorbeeld ‘schrijf een antwoord waarin je zegt dat donderdag goed uitkomt’. The Machine stuurt dit naar de chat van de to-do, alsof je het zelf had getypt. De chat volgt de gebruikelijke regels.

De chat kan ook dingen opzoeken, zoals de openingstijden van een winkel. Je ziet **Ermee bezig…** en kunt gewoon blijven praten. Zodra het antwoord klaar is, vertelt The Machine je het antwoord en waar hij het heeft gevonden.

Zeg dat je een concept wilt versturen. The Machine leest het hardop voor, met de ontvanger, het onderwerp en de tekst, en vraagt bijvoorbeeld: ‘Dit antwoord per e-mail naar Sam versturen?’ Je telefoon kan gewoon in je zak blijven. Zeg duidelijk ja, bijvoorbeeld ‘ja, verstuur het’, en het concept wordt verstuurd.

- Hij verstuurt precies het concept dat hij heeft voorgelezen. Als het concept verandert, leest hij het opnieuw voor en vraagt hij opnieuw om je akkoord. Als je niet binnen 3 minuten antwoordt, verloopt de vraag.
- Zonder een duidelijk ja wordt er niets verstuurd.
- Een concept dat je al hebt gezien of gehoord, wordt niet opnieuw voorgelezen. Hij vraagt alleen bijvoorbeeld: ‘Naar Pat versturen?’.
- Zeg ‘verstuur alle klaargezette’ en hij noemt iedereen in één vraag. Met één keer ja verstuurt hij ze allemaal.
- Na je akkoord toont Praten **Ongedaan maken** met een afteltimer. Tik erop of zeg ‘ongedaan maken’ of ‘wacht’.
- Na het versturen zegt Praten ‘Verstuurd.’ en toont de to-do **Verstuurd naar** die persoon, met het tijdstip. Als het versturen niet is gelukt, vertelt Praten waarom. Vraag op elk moment ‘is het verstuurd?’: hij controleert het en raadt nooit.

Je kunt ook op **Goedkeuren** tikken.

Zeg ‘doe het’ om The Machine aan de to-do te laten beginnen, net als met **Doe het**. Zeg ‘een bug melden’ om een bugrapport te versturen, net als met **Een bug melden** in Help.

## Een stem kiezen

Kies onder **Instellingen**, **Algemeen** en **Spraakinvoer** een **Stem**. Tik op afspelen om die te horen. **Cedar** is de standaardstem. De Cove-stem van ChatGPT is niet beschikbaar.

## Een verslag in de chat

Alles wat er wordt gezegd, komt onder een regel met **Live gepraat** in de chat van de to-do te staan, zodat je het later kunt teruglezen.

## Wat je nodig hebt

Live praten gebruikt de stem van OpenAI. Je Machine heeft daarom een van deze dingen nodig:

- Een ChatGPT-account: inbegrepen bij abonnementen waarbij dit beschikbaar is.
- Een OpenAI API-sleutel: OpenAI rekent kosten per minuut en de balk vermeldt dat. Als je beide hebt, gebruikt je Machine de sleutel.

Onder **Instellingen**, **Algemeen** en **Spraakinvoer** zie je of Live praten klaar is. Zonder OpenAI wordt de golf niet weergegeven. Je audio gaat rechtstreeks vanuit je browser naar OpenAI.

## Als het niet werkt

- **De microfoon is geblokkeerd**: geef deze site toegang tot je microfoon in de browserinstellingen.
- **Live praten kon niet starten**: controleer je ChatGPT-account of OpenAI API-sleutel en probeer het opnieuw.
- **De verbinding met Live praten is verbroken**: start opnieuw. Wat er is gezegd, blijft in de chat staan.
- Hij zegt dat hij je niet kan verstaan: controleer je microfoon of typ in de chat.
