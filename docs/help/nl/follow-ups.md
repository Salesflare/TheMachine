---
title: Opvolgingen
area: graph
summary: Volg iemand automatisch op als die niet reageert, voor een heel bord of één project. Je krijgt eerst een concept, tenzij je iets anders instelt.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 76bea8f586963be1
---
Als iemand op een bord niet meer reageert, schrijft je Machine een concept voor de opvolging, in jouw stijl en in hetzelfde gesprek. De functie staat uit totdat je die aanzet. Als een van je skills bij het bord past, houdt het concept zich daaraan, ook aan de volgorde van de informatie in de e-mail.

## Inschakelen

Klik op **⋯** op een bord en daarna op **Opvolging…**. Vink **Opvolgen als er geen antwoord komt** aan. Dit geldt voor elk project op dat bord. Je kunt ook op **Opvolging uit** onder de naam van het bord tikken, of op **Volg ze op** in een fase met projecten waarop al meer dan 10 dagen geen reactie is gekomen.

Voor één project kies je **Opvolging…** in het menu **⋯** op het bord of op de projectpagina. Met **Voor dit project** kies je **Aan**, **Uit** of de instelling van het bord. De eigen instelling van een project gaat voor op die van het bord.

## Instellingen

- Standaard wacht je Machine 3 tot 7 dagen op een antwoord. Na de kortste wachttijd wordt een opvolging opgesteld. Uiterlijk na de langste wachttijd wordt die verstuurd, ook als je gebruikslimiet bijna bereikt is.
- **Alleen op werkdagen**: op je vrije dagen wordt er niets opgesteld of verstuurd. Je vrije dagen stel je in via **Instellingen** > **Meldingen** > **Werkuren**. Wat dan aan de beurt is, wacht tot de eerstvolgende werkochtend. Deze optie staat aan voor Werk en uit voor Privé.
- Standaard volgt je Machine 1 tot 3 keer op. Het minimum wordt altijd verstuurd; voor de rest krijg je een concept. Als je Machine denkt dat je beter kunt stoppen, staat in het concept waarom ("The Machine zou hier stoppen: sinds augustus zijn 9 e-mails onbeantwoord gebleven"). Het concept is niet aangevinkt: je kunt het versturen, overslaan of **Opvolgingen hier stoppen** kiezen. Er worden nooit meer opvolgingen verstuurd dan het maximum.
- **Fases**: standaard **Alle open fases**, dus niet de laatste fase van het bord en ook niet Vastgelopen of afgewezen. Met **Aanpassen** zet je fases aan of uit en geef je een fase een eigen wachttijd.
- **Kanalen**: de gekoppelde kanalen waarmee je berichten kunt versturen. Een opvolging wordt verstuurd via hetzelfde kanaal als het laatste bericht. **Ander kanaal als er geen antwoord komt** probeert het volgende toegestane kanaal.
- **Na de laatste naar Vastgelopen of afgewezen verplaatsen**: staat aan als het bord die fase heeft.

## Eerst vragen of automatisch versturen

**Vraag het me voor het versturen** is de standaardinstelling: concepten wachten in je to-do's. **Versturen zonder te vragen** betekent dat je voor dat bord of project altijd toestemming geeft. Bij iets ongebruikelijks of als er iets misgaat, wacht de opvolging alsnog op jou. Op het niveau Voorzichtig wordt altijd om toestemming gevraagd. Een opvolging wordt nooit twee keer verstuurd. Opvolgingen geven nooit een melding via push of e-mail: de concepten wachten in je lijst en in het ochtendoverzicht.

Vlak voor het versturen wordt het gesprek opnieuw gecontroleerd. Als iemand sinds het opstellen van het concept iets heeft geschreven, wordt het niet verstuurd: "Niet verstuurd: nieuw bericht in het gesprek". In de to-do zie je dat bericht, wie het heeft geschreven en wanneer, met **Lezen** en **Opnieuw voor dit bericht**. Met die laatste optie vraag je een nieuw concept aan waarin het bericht is meegenomen.

## Opvolgingen nakijken

Opvolgingen voor een bord komen samen in één to-do, nooit in een aparte to-do per e-mail. Terwijl ze worden opgesteld, staat er "3 opvolgingen schrijven…". Daarna staat er bijvoorbeeld "8 opvolgingen klaar voor Alpha testers".

Met **Nakijken** zie je alle opvolgingen volledig onder elkaar, zodat je ze in één keer kunt doorlezen. Bij de huidige opvolging staan **Versturen**, **Bewerken** en **Overslaan**. Gebruik je een toetsenbord, dan ga je met j en k (of de pijltjestoetsen) naar de volgende of vorige opvolging. Druk op Enter om te versturen, op e om te bewerken, op s om over te slaan (druk nogmaals om dat ongedaan te maken), op x om aan of uit te vinken en op c om wijzigingen aan te vragen. Met **Alle aangevinkte versturen** verstuur je de opvolgingen die nog aangevinkt zijn.

Bij elke opvolging hoort een concept. Als er geen concept kan worden geschreven, staat er wat er eerst nodig is ("Geen concept. Eerst nodig: de ontvanger."). Het concept is dan niet aangevinkt. Met **Schrijven** vraag je het concept alsnog aan. Als er meerdere mogelijke ontvangers voor een concept zijn, staat er "Ontvanger: kies bij versturen". Met **Versturen** kies je dan eerst een ontvanger.

Met **Overslaan** vink je een concept uit en verplaats je het naar onderaan. Het krijgt de markering Overgeslagen en de optie **Ongedaan maken**. Het wordt definitief overgeslagen zodra je het nakijken sluit. Je kunt een overgeslagen opvolging terughalen met **Terughalen** bij de opvolgingen van het project of in de to-do van het project onder Gedaan, zolang er geen nieuwere opvolging is verstuurd. De opvolging van één project is een gewone to-do.

Met **Wijzigingen vragen…** herschrijf je alle aangevinkte concepten of alleen het huidige, zoals je aangeeft. Er wordt niets verstuurd en met **Wijziging ongedaan maken** herstel je de oude tekst. Zolang het invoerveld openstaat of een tekst wordt herschreven, kan er niets worden verstuurd. Een aangepast concept wordt opnieuw getoond voordat het kan worden verstuurd.

Als er meerdere opvolgingen achter elkaar worden verstuurd, ook met **Versturen zonder te vragen**, verstuurt elke mailbox er elke 30 tot 45 seconden één. In de to-do zie je hoe ver het is: "3 van de 8 versturen…". Met **Stop met versturen** stop je de rest. Wat al onderweg is, wordt nog verstuurd. De andere opvolgingen staan weer als concepten bij het nakijken, zodat je ze later kunt versturen ("Gestopt. 1 verstuurd, 11 als concept bewaard.").

## E-mails verstuurd voordat je Machine ze las

Ook e-mails die je vanuit een andere app hebt verstuurd voordat je Machine die mailbox las, tellen mee. Je Machine leest het gesprek zelf. Als dat niet lukt, leest hij de eerdere e-mails die in je laatste bericht zijn geciteerd. Drie e-mails zonder antwoord tellen dus als drie, en "Geen antwoord sinds" telt vanaf de eerste e-mail. Als je het maximum al hebt bereikt, wordt er geen nieuw concept opgesteld.

## Wanneer de opvolging stopt

Opvolgingen stoppen als iemand antwoordt, als het project gewonnen, verloren of gearchiveerd is, als het naar een gesloten fase wordt verplaatst, en als je een opvolging snoozet of overslaat. Voordat je Machine een concept opstelt, controleert hij het gesprek op nieuwe berichten. Zo blijft hij iemand niet lastigvallen die ergens anders al heeft geantwoord.

Een opvolging wordt ook afgesloten als iemand in hetzelfde gesprek alweer iets heeft geschreven. Een opvolging van een ander project telt niet mee. Als je Machine om een andere reden denkt dat opvolgen niet nodig is, blijft de to-do open en staat erbij waarom. Jij beslist wat je ermee doet.

Met **Pauzeren** in **Opvolging…** pauzeer je een bord of project zonder opvolgingen uit te zetten. Er wordt niets opgesteld of verstuurd en er wordt geen ronde afgerond. Open to-do's voor opvolgingen blijven open. Kies een dag waarop je wilt hervatten of tik op **Hervatten** als je er klaar voor bent. De wachttijd gaat verder vanaf waar die was gebleven en wat al aan de beurt was, komt één voor één terug. Ondertussen staat er **Gepauzeerd**.

Na de laatste opvolging zonder antwoord staat er bij het project "Geen antwoord na 3 opvolgingen". Het project wordt naar Vastgelopen of afgewezen verplaatst als die instelling aanstaat. Als je stopt voordat er iets is verstuurd, staat er "Opvolgingen gestopt" en blijft het project in dezelfde fase.

Als de e-mail is teruggestuurd en iemand een ander e-mailadres heeft, wordt de opvolging daarheen verstuurd ("Teruggestuurd, nu naar <address>"). Als het e-mailadres van een concept wordt teruggestuurd voordat het is verstuurd, wordt het concept vastgehouden: "Niet verstuurd: <address> is teruggestuurd". Het wordt verplaatst naar het andere e-mailadres en wacht daar tot je het verstuurt.

Als er geen ander e-mailadres is, gaan opvolgingen verder via LinkedIn of WhatsApp als dat is toegestaan en je daar contact hebt. Anders stoppen ze met "E-mail teruggestuurd". Als het project belangrijk is, krijg je een to-do om een nieuw e-mailadres te zoeken.

## Waar je het ziet

In de kop van het bord staat "Opvolging aan, volgende do". Bij een project op het bord staat wanneer de volgende opvolging is, of dat er een klaarstaat. Op de projectpagina zie je welke opvolgingen zijn verstuurd, ook de opvolgingen die automatisch zijn verstuurd.

Opvolgingen wachten als je Machine het druk heeft of bijna aan de gebruikslimiet zit. Later haalt hij ze in. Op een gedeeld bord volgt alleen de Machine van de projecteigenaar op.
