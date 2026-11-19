---
title: Opvolgingen
area: graph
summary: Volg iemand automatisch op als die niet reageert, voor een heel bord of één project. Je Machine vraagt het eerst, tenzij je dat anders instelt.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 0e7bdfb2c9b2deb5
---
Als iemand op een bord niet meer reageert, maakt je Machine een concept voor de opvolging, in jouw stijl en in hetzelfde gesprek. Opvolgingen staan uit tot je ze aanzet. Als een van je skills bij het bord past, houdt het concept daar rekening mee, ook met de volgorde van de tekst in de e-mail.

## Inschakelen

Klik op **⋯** op een bord en daarna op **Opvolging…**. Vink **Opvolgen als er geen antwoord komt** aan. Dit geldt voor elk project op dat bord. Je kunt ook op **Opvolging uit** onder de naam van het bord klikken, of op **Volg ze op** in een fase met projecten waarop al meer dan 10 dagen geen reactie is gekomen.

Voor één project klik je op **Opvolging…** in het menu **⋯** op het bord of op de projectpagina. Met **Voor dit project** kies je **Aan**, **Uit** of de instelling van het bord. De eigen instelling van een project gaat voor op die van het bord.

## Instellingen

- Standaard wacht je Machine 3 tot 7 dagen op een reactie. Na de kortste wachttijd maakt hij een concept voor de opvolging. Uiterlijk na de langste wachttijd wordt het verstuurd, ook als je gebruik bijna op is.
- **Alleen op werkdagen**: op je vrije dagen maakt of verstuurt je Machine niets (via **Instellingen** > **Meldingen** > **Werkuren**). Wat dan aan de beurt is, wacht tot de volgende werkdag. Deze instelling staat aan voor Werk en uit voor Persoonlijk.
- Standaard volgt je Machine 1 tot 3 keer op. Hij verstuurt altijd het minimumaantal en maakt concepten voor de rest. Als hij denkt dat je beter kunt stoppen, staat in het concept waarom ("Je Machine zou hier stoppen: sinds augustus zijn 9 e-mails onbeantwoord gebleven"). Het concept is dan niet aangevinkt. Je kunt het versturen, overslaan of **Opvolgingen hier stoppen** kiezen. Het maximum wordt nooit overschreden.
- **Fases**: standaard **Alle open fases**, dus niet de laatste fase van het bord en ook niet Vastgelopen of afgewezen. Met **Aanpassen** zet je fases aan of uit en stel je voor een fase een eigen wachttijd in.
- **Kanalen**: de gekoppelde kanalen waarmee je berichten kunt versturen. Een opvolging wordt verstuurd via hetzelfde kanaal als het laatste bericht. Met **Ander kanaal als er geen antwoord komt** probeert je Machine het volgende toegestane kanaal.
- **Na de laatste naar Vastgelopen of afgewezen verplaatsen**: staat aan als het bord die fase heeft.

## Eerst vragen of automatisch versturen

**Vraag het me voor het versturen** is de standaardinstelling: concepten blijven in je to-do's staan. **Versturen zonder te vragen** geldt als een vaste toestemming voor dat bord of project. Alles wat ongebruikelijk is of mislukt, wacht alsnog op je. Op het niveau Zorgvuldig vraagt je Machine het altijd eerst. Een opvolging wordt nooit twee keer verstuurd. Je krijgt geen pushmelding of e-mail over opvolgingen. De concepten staan in je lijst en in het ochtendoverzicht.

Vlak voordat een opvolging wordt verstuurd, controleert je Machine het gesprek opnieuw. Als iemand sinds het maken van het concept iets heeft geschreven, wordt het niet verstuurd: "Niet verstuurd: nieuw bericht in het gesprek". De to-do toont dat bericht, wie het heeft geschreven en wanneer, met **Lezen** en **Opnieuw voor dit bericht**. Daarmee vraag je een nieuw concept aan dat rekening houdt met het bericht.

## Opvolgingen bekijken

De opvolgingen van een bord verschijnen samen in één to-do, nooit als losse to-do's per e-mail. Terwijl de concepten worden gemaakt, staat er "3 opvolgingen schrijven…". Daarna staat er "8 opvolgingen klaar voor Alpha testers".

Met **Nakijken** zie je de opvolgingen onder elkaar, elk helemaal uitgeschreven, zodat je ze allemaal achter elkaar kunt lezen. Bij de huidige opvolging staan **Versturen**, **Bewerken** en **Overslaan**. Met een toetsenbord blader je met j en k (of de pijltjestoetsen), verstuur je met Enter, bewerk je met e, sla je over met s (nogmaals indrukken maakt dit ongedaan), vink je aan of uit met x en wijzig je met c. Met **Alle aangevinkte versturen** verstuur je de opvolgingen die nog zijn aangevinkt.

Bij elke opvolging hoort een concept. Als er nog iets nodig is om er een te schrijven, staat dat erbij ("Geen concept. Eerst nodig: de ontvanger.") en is de opvolging niet aangevinkt. Met **Schrijven** vraag je toch om een concept. Als een concept meerdere mogelijke ontvangers heeft, staat er "Ontvanger: kies bij het versturen". Als je op **Versturen** klikt, vraagt je Machine je om een ontvanger te kiezen.

Met **Overslaan** vink je een concept uit en verplaats je het naar onderaan. Het krijgt het label Overgeslagen en een knop **Ongedaan maken**. Als je de beoordeling sluit, is het definitief overgeslagen. Je kunt een overgeslagen opvolging terughalen met **Terughalen** bij de opvolgingen van het project of bij de to-do in **Gedaan**, zolang er geen nieuwere opvolging is geweest. De opvolging van één project is een gewone to-do.

Met **Wijzigingen vragen…** herschrijft je Machine alle aangevinkte concepten, of alleen het huidige, volgens je aanwijzingen. Er wordt niets verstuurd. Met **Wijziging ongedaan maken** zet je de oude tekst terug. Zolang het invoerveld openstaat of er een nieuwe versie wordt gemaakt, kan er niets worden verstuurd. Een gewijzigd concept wordt opnieuw getoond voordat het kan worden verstuurd.

Als er meerdere opvolgingen achter elkaar worden verstuurd, ook met Versturen zonder te vragen, verstuurt elke mailbox er één om de 30 tot 45 seconden. De to-do laat zien hoever het proces is: "3 van 8 versturen…". Met **Stop met versturen** stop je de rest. Een bericht dat al onderweg is, wordt nog verstuurd. De overige concepten staan weer klaar om later te versturen ("Gestopt. 1 verstuurd, 11 als concept bewaard.").

## E-mails die zijn verstuurd voordat je Machine ze las

Ook e-mails die je vanuit een andere app hebt verstuurd voordat je Machine die mailbox las, tellen mee. Hij leest het gesprek zelf (of, als dat niet lukt, de eerdere e-mails die in je laatste bericht zijn geciteerd). Drie e-mails zonder antwoord tellen dus als drie, en de periode bij "Geen reactie gedurende" begint bij de eerste e-mail. Als je het maximum al hebt bereikt, maakt je Machine geen nieuw concept.

## Wanneer opvolgingen stoppen

Opvolgingen stoppen als de ontvanger reageert, als het project is gewonnen of verloren, als het wordt gearchiveerd of naar een gesloten fase wordt verplaatst, en als je het snoozet of overslaat. Voordat hij een concept maakt, controleert je Machine het gesprek op nieuwe berichten. Zo blijft hij iemand die ergens anders al heeft geantwoord niet lastigvallen.

Met **Pauzeren** in **Opvolging…** pauzeer je een bord of project zonder opvolgingen uit te zetten. Er worden geen concepten gemaakt of verstuurd, er wordt geen ronde afgerond en openstaande to-do's voor opvolgingen blijven open. Kies een dag waarop je verder wilt gaan, of klik op **Hervatten** als je er klaar voor bent. De wachttijd gaat verder waar die was gebleven. Wat al aan de beurt was, wordt één voor één afgehandeld. Ondertussen staat er **Gepauzeerd**.

Na de laatste opvolging zonder reactie staat er bij het project "Geen reactie na 3 opvolgingen". Als die instelling aanstaat, wordt het project naar Vastgelopen of afgewezen verplaatst. Als je stopt voordat er iets is verstuurd, staat er "Opvolgingen gestopt" en blijft het project in dezelfde fase.

Als een e-mail is teruggestuurd en de ontvanger een ander adres heeft, wordt de opvolging daarheen gestuurd ("Teruggestuurd, nu naar <address>"). Als een adres terugkomt voordat een concept is verstuurd, wordt het concept vastgehouden: "Niet verstuurd: <address> is teruggestuurd". Het wordt verplaatst naar het andere adres en wacht daar tot je het verstuurt.

Als er geen ander adres is, schakelen opvolgingen over naar LinkedIn of WhatsApp als dat is toegestaan en je daar contact hebt. Anders stoppen ze met "E-mail teruggestuurd". Als het project belangrijk is, krijg je een to-do om een nieuw adres te zoeken.

## Waar je dit ziet

In de kop van het bord staat "Opvolgingen aan, volgende do". Bij een project op het bord staat de volgende opvolging, of dat er een klaarstaat. Op de projectpagina zie je wat er is verstuurd, ook wat automatisch is verstuurd.

Opvolgingen wachten als je Machine bezig is of bijna aan de gebruikslimiet zit, en worden later ingehaald. Op een gedeeld bord volgt alleen de Machine van de projecteigenaar op.
