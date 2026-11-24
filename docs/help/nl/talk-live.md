---
title: Live praten
area: cards
summary: Een gesproken gesprek met The Machine over een to-do, met de stem van OpenAI. Het werkt in de chat van de to-do en verstuurt een concept pas nadat je daar ja op zegt.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: f5555cb693a23682
---
## Een gesprek beginnen

Tik in de chat van een to-do op de golf naast de microfoon. Geef toestemming voor de microfoon als daarom wordt gevraagd. Zodra de balk **Live** aangeeft, kun je praten alsof je aan het bellen bent. The Machine antwoordt hardop. Praat erdoorheen om hem te onderbreken.

Hij kent deze to-do: de berichten, het concept en de chat. Ook kan hij je andere to-do's opzoeken. Zeg bijvoorbeeld ‘markeer dit als gedaan’, ‘snooze dit tot morgen om 9 uur’ of ‘niet nodig’, en hij doet het. Zeg meteen daarna ‘nee, niet dat’ om het ongedaan te maken. Tijden volgen de tijdzone van je [Werkuren](work-hours.md).

Hij luistert in de taal van de app en in de talen die je browser opgeeft. Op hoesten, lawaai en andere talen volgt geen antwoord. Die komen ook niet in het transcript.

De balk bevat **Dempen** en **Beëindigen**. Zeg gedag en het gesprek eindigt vanzelf. Een gesprek duurt maximaal 10 minuten. In de laatste minuut zie je een aftelling. Begin opnieuw om verder te gaan.

## Praten over al je to-do's

Tik op **Praten** in de zijbalk (op je telefoon staat dit in het menu). The Machine vertelt hoeveel to-do's er klaarstaan en behandelt de to-do's onder **Voor jou** één voor één, in de volgorde van je lijst. Hij laat het weten zodra een to-do met de status **Aan het voorbereiden…** klaar is.

Praten heeft een eigen pagina: de to-do waar hij mee bezig is, staat bovenaan, samen met het concept en **Chat openen**.

Vraag hem een concept voor te lezen of te wijzigen, een to-do te snoozen, als gedaan te markeren of naar de volgende te gaan. Wat je over een to-do zegt, komt in de chat ervan terecht. Tijdens een pauze vertelt hij over nieuwe to-do's. Zeg ‘voeg een to-do toe voor...’ om er een toe te voegen zonder je plek kwijt te raken.

Vraag naar een persoon, organisatie, project, meeting of belofte. Hij zoekt die op en laat zien wat hij vindt. Hij kan ook to-do's afwijzen, hernoemen of opnieuw openen, ook to-do's onder **Gedaan / afgewezen**. Voor andere vragen geeft hij de vraag door aan de chat van een nieuwe to-do en vertelt hij je het antwoord.

Hij onthoudt eerdere gesprekken met je. Vraag ‘wat heb ik besloten over de offsite?’ en hij vertelt het je, inclusief wanneer je dat zei. Alleen Praten in de zijbalk kan dit.

Je kunt ondertussen andere pagina's bekijken. De balk blijft onderaan staan en met **Praten** ga je terug. Dit gesprek duurt maximaal 30 minuten. Op computers en Android gaat het op de achtergrond door. Op een iPhone stopt het zodra de app niet meer op het scherm staat.

## Vraag om iets te doen en verstuur met een ja

Vraag bijvoorbeeld ‘schrijf een antwoord waarin je zegt dat donderdag uitkomt’. The Machine geeft dat door aan de chat van de to-do alsof je het zelf hebt getypt. De chat volgt de gebruikelijke regels.

De chat kan ook dingen opzoeken, zoals de openingstijden van een winkel. Hij toont **Ermee bezig…** terwijl jij kunt blijven praten. Zodra het antwoord klaar is, vertelt The Machine je het en laat hij zien waar hij het heeft gevonden.

Zeg dat je een concept wilt versturen. The Machine leest het voor (de ontvanger, het onderwerp en de tekst) en vraagt bijvoorbeeld: ‘Deze reactie per e-mail naar Sam versturen?’ Je hoeft je telefoon niet uit je zak te halen. Zeg duidelijk ja, bijvoorbeeld ‘ja, verstuur maar’, en het concept wordt verstuurd.

- Hij verstuurt precies het concept dat hij heeft voorgelezen. Als het concept verandert, leest hij het opnieuw voor en vraagt hij opnieuw om toestemming. Een vraag waarop je niet binnen 3 minuten antwoordt, verloopt.
- Zonder een duidelijk ja verstuurt hij niets.
- Een concept dat je al hebt gezien of gehoord, leest hij niet opnieuw voor. Hij vraagt alleen bijvoorbeeld: ‘Naar Pat versturen?’
- Zeg ‘verstuur alle klaargezette concepten’ en hij noemt iedereen in één vraag. Met één ja verstuurt hij ze allemaal.
- Na je ja toont Praten **Ongedaan maken** met een aftelling. Tik erop of zeg ‘ongedaan maken’ of ‘wacht’.
- Na het versturen zegt Praten ‘Verstuurd.’ De to-do toont **Verstuurd naar** die persoon, met het tijdstip. Als het versturen niet is gelukt, vertelt Praten waarom. Vraag op elk moment ‘is het verstuurd?’ Hij controleert het en gokt nooit.

Je kunt ook op **Goedkeuren** tikken.

Zeg ‘doe het’ om The Machine met de to-do aan de slag te laten gaan, zoals met **Doe het**. Zeg ‘meld een bug’ om een bugmelding te versturen, zoals met **Een bug melden** in Help.

## Een stem kiezen

Kies onder **Instellingen**, **Algemeen** en **Spraakinvoer** een **Stem**. Tik op afspelen om de stem te horen. **Cedar** is de standaardstem. De Cove-stem van ChatGPT is niet beschikbaar.

## Een verslag in de chat

Alles wat wordt gezegd, komt onder een regel met **Live gepraat** in de chat van de to-do te staan, zodat je het later kunt teruglezen.

## Wat je nodig hebt

Live praten gebruikt de stem van OpenAI. Je Machine heeft daarom een van deze opties nodig:

- Een ChatGPT-login: inbegrepen bij abonnementen die dit aanbieden.
- Een OpenAI API-sleutel: OpenAI rekent kosten per minuut. Dat staat op de balk. Als je beide hebt, gebruikt je Machine de sleutel.

Onder **Instellingen**, **Algemeen** en **Spraakinvoer** zie je of Live praten klaar is. Zonder OpenAI wordt de golf niet getoond. Je audio gaat rechtstreeks vanuit je browser naar OpenAI.

## Als het niet werkt

- **De microfoon is geblokkeerd**: geef deze site toestemming voor de microfoon in de instellingen van je browser.
- **Live praten kon niet starten**: controleer je ChatGPT-login of OpenAI-sleutel en probeer het opnieuw.
- **Live praten heeft de verbinding verloren**: begin opnieuw. Wat er is gezegd, blijft in de chat staan.
- The Machine zegt dat hij je niet kan verstaan: controleer je microfoon of typ in de chat.
