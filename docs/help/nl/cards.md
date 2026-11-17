---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak die je aandacht nodig heeft, klaar voor jouw akkoord. Lees wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: baa6b797e040a271
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als iets jouw aandacht nodig heeft. Eén to-do per zaak, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een issue dat is afgehandeld terwijl je weg was. Die blijft hier staan tot je op **Begrepen** tikt, maximaal één dag. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het meest urgente bovenaan. Bij elke to-do staat **Klaargezet** (het werk is gedaan en **Doe het** of **Versturen** voert het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoorden), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of korte briefing, zonder dat je iets hoeft te beslissen).
- **Wacht op anderen**: ingeklapte to-do's waarbij iemand anders aan zet is (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop je niet hebt gereageerd bij **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, nieuwste eerst, met het tijdstip waarop ze zijn afgerond, zoals "5 minuten geleden gedaan". To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Na het versturen verschijnt een korte melding met de plek waar de to-do naartoe is gegaan, zoals "Verstuurd. Verplaatst naar Gedaan." of "Verstuurd. Verplaatst naar Later tot ma." Met **Openen** ga je naar de to-do. Zoeken vindt een to-do op titel of op de persoon naar wie die is gestuurd, ook in Later en Gedaan.

Bij **Voor jou** staan eerst de achterstallige to-do's en de to-do's met een deadline uiterlijk morgen, dan vragen van je Fleet, daarna opvolgingen van een bord en vervolgens de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do behoudt zijn plek terwijl je Machine hem voorbereidt en wanneer hij klaar is. Alleen de status verandert. In de andere open groepen staan achterstallige to-do's en to-do's met een deadline uiterlijk morgen eerst, daarna de rest, nieuwste bovenaan. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat de taak is afgerond, bijvoorbeeld "PR #3451 is gemerged", maar dat hij nog niet is afgesloten. Met **Heropenen** zet je hem terug op je lijst en leert je Machine ervan. Deze to-do's verschijnen nooit als achterstallig. Na een dag wordt de to-do automatisch afgesloten, met de optie **Ongedaan maken**. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook automatisch afgesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: "Dit is Sam Lee niet." Je ziet de persoon met het eigen e-mailadres, nooit met de naam die diegene heeft opgegeven. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Een to-do die nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, vermeldt die stap bij **Wacht op:**. De to-do staat ingeklapt onder **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem weer naar boven haalt. Dat geldt ook als je een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline zelf als die later op de dag valt, of de volgende ochtend als de deadline al voorbij is. Je ziet dan op wie de to-do nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Je eigen deel versturen sluit de to-do niet af: hij blijft onder **Wacht op anderen** staan tot een bericht het resultaat bevestigt. Daarna wordt hij automatisch afgesloten, met de optie **Ongedaan maken**. Als er niets binnenkomt tegen de tijd dat je die persoon moet herinneren, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit te wijzigen.

Als niemand een to-do een week heeft aangeraakt, vraagt hij één keer: **Nog nodig?** Met **Niet nodig** sluit je hem af, met de optie **Ongedaan maken**. Met **Houden** blijft hij staan en wordt dit niet opnieuw gevraagd. Als je nog een week niet reageert, wordt de to-do ingeklapt onder Komt later terug. Het getal op het appicoon en het ochtendoverzicht tellen hem dan niet meer mee. Als je de to-do opent, een chatbericht stuurt, iets bewerkt of snoozet, of als er een nieuw bericht binnenkomt, komt hij weer terug.

Een project zonder activiteit en zonder openstaande taken kan eens per week een to-do krijgen met één concrete volgende stap, maximaal drie per week. Zie [Projecten](projects.md).

Als niets jouw aandacht nodig heeft, doet je Machine een dutje op een lege lijst. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen één soort. Op je telefoon en computer zie je dezelfde keuze. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, is noch Werk noch Privé en verschijnt alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook meteen naar de andere weergave: tik bij **Alleen privé** op **Werk** of **Alles tonen**.

De balk bovenaan de lijst toont de naam van je laatste ochtend- of avondoverzicht en wat erin is meegeteld, zoals **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om het overzicht opnieuw te lezen, met **Kopiëren** om het ergens te plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, zie je **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt geselecteerd.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Zie [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot wat hij mag lezen en versturen verhuist mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle bijbehorende berichten daar staan, wordt hij automatisch verplaatst en gaat hij verder. Anders zie je **Naar Werk verplaatsen** en gebeurt er niets tot je erop tikt. Een to-do die je zelf hebt toegevoegd zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd staat er geen Werk of Privé bij en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij je om **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gelabeld, telt als Privé. Mail voor een ander bedrijf van jou gaat naar de to-do's van dat bedrijf. Een to-do over je eigen leven, zoals familie die naar je werkadres mailt, is vanaf het begin Privé.

Werk dat je via een persoonlijk account bereikt, zoals een klant op WhatsApp of een bestelling in je persoonlijke mailbox, is vanaf het begin Werk. Een to-do die je zelf hebt verplaatst of geplaatst, blijft altijd staan waar jij hem hebt gezet. Werk of Privé bepaalt waar een to-do verschijnt en met wie hij wordt gedeeld, nooit waar hij op antwoordt: een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail binnenkwam en verschijnt nooit in een Fleet voor Werk of in de Team Graph.

Als er twee of meer to-do's op je wachten, doorloopt **Doorlopen** in de kop van Voor jou ze één voor één, in de volgorde van de lijst. Je ziet elk concept helemaal, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stopt Esc. Onder de titel staat in de kop ook hoelang ze ongeveer duren als je ze op je eigen tempo doorloopt, zoals "ongeveer 2 min".

Een to-do die je iets vraagt, wordt bij beide groepen overgeslagen: daarvoor moet je antwoorden, niet ergens op tikken.

## Nu checken

Je Machine leest elke paar minuten elke bron, dag en nacht. Hij controleert wat er is binnengekomen zodra er 40 berichten klaarstaan of het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen gaan mee met de volgende controle, binnen een uur.

's Nachts, van 00:00 tot 06:30, zijn controles gepauzeerd: nieuwe berichten worden nog wel gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan vóór je ochtendoverzicht. Bij Controles onder Koppelingen staat dan "'s Nachts gepauzeerd, haalt de achterstand om 06:30 in". Klikken, typen of scrollen in de app, iets schrijven in de chat of 's nachts op een to-do tikken, zorgt ervoor dat controles weer gewoon lopen tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen elke bron. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details** om Controles onder Koppelingen te openen. Als er to-do's openstaan, vind je de regel bovenaan op een computer. Een korte melding verschijnt daar alleen tijdens een controle of als er een is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met wat er is gevonden in alle gelezen bronnen, zoals "13 berichten gecontroleerd om 16:11 · niets nodig" of "· 2 nieuwe to-do's". Als een nieuwe to-do op een beter moment wacht, bijvoorbeeld tot je ochtendoverzicht, staat erbij tot wanneer: "1 to-do uitgesteld tot morgen 08:30".

Tik op de regel om elk e-mailgesprek, elke chat en elke melding te zien, met het pictogram van de bron: wie het schreef, het onderwerp of de eerste woorden, en de nieuwe to-do of de reden waarom er niets nodig was, zoals "Alleen in cc, een teamgenoot antwoordt" of "Vergadering staat al op donderdag". Als de controle alleen een vage reden opleverde, staat er geen reden bij het gesprek. Tik erop om het te lezen.

De eerste 10 worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails van The Machine zelf aan jou, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of getoond. Mail over facturering, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan, of, als er al een concept klaarstaat, wat daarin moet worden aangepast. **Markeer als gedaan** betekent dat het is afgehandeld. Bij een to-do die klaarstaat zonder concept staat de knop direct in beeld, anders bovenaan onder **…**. Je ziet hem ook bij to-do's waarvoor je een beslissing moet nemen. De to-do verdwijnt meteen uit de lijst, met **Ongedaan maken** in de melding. Veeg de melding weg of sleep hem met de muis weg om hem sneller af te sluiten. De wijziging blijft staan.

Wil je dat het op een andere manier wordt gedaan, zeg dat dan in de **Chat**.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om het te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. De titel die je kiest, blijft staan.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook automatisch terug als er iets nieuws gebeurt, zoals een nieuw bericht van die persoon, maar niet na je eigen antwoord.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen kaart, worden dat niet. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld doordat de afzender bevestigt dat je betaling is aangekomen, wordt de to-do automatisch afgesloten. Met **Ongedaan maken** zet je hem één dag terug.

Een to-do die alleen tot een bepaald tijdstip van belang was, zoals een bevestiging vóór een vergadering, wordt na dat tijdstip automatisch afgesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** als "Niet meer nodig". Met **Ongedaan maken** zet je hem één dag terug.

Voordat een bericht of overdracht voor iemand als klaar wordt getoond, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack ze heeft ingelezen. Als een later bericht laat zien dat het al geregeld is, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do automatisch afgesloten. Met **Ongedaan maken** zet je hem één dag terug.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is vervallen, past The Machine zijn to-do's zelf aan. Een to-do die nog relevant is, volgt het nieuwe plan. Als er niets meer te doen is, wordt hij verplaatst naar **Gedaan / afgewezen** als "Niet nodig". In de chat staat dan "Bijgewerkt:" met de reden. Met **Ongedaan maken** zet je hem één dag terug.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**, en de uitleg dat er niets wordt verstuurd tot je op **Versturen** drukt. Een tip verdwijnt definitief zodra je de bijbehorende knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en staat erbij wie al het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat als je aankomt.

Elke to-do begint met de titel. De regel eronder vermeldt om wie het gaat, de organisatie als die relevant is (niet alleen omdat iemand er werkt), het project, Werk of Privé en wanneer het bericht is binnengekomen. Tik op een naam om de pagina van die persoon in Graph te openen.

Bij een naam en organisatie wordt de foto of het logo getoond als Graph die heeft, anders de initialen. Bij een logo dat op die grootte niet leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, worden ook de initialen getoond.

Soms staat er een stille melding met wat niet bekend is, zoals "12 dagen geleden voor het laatst contact via e-mail; sindsdien niets." Die verschijnt als het laatste contact met die persoon lang geleden was of nog onbeantwoord is. Ook niet-gekoppelde kanalen, zoals WhatsApp, worden genoemd. Je Machine zegt wat hij niet weet in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

Een titel zegt wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do behoudt zijn titel, met daaronder hoe het is afgelopen, zoals "Gedaan: Sam heeft het dinsdag ondertekend".

Boven het concept staat een vage regel met het bericht waar het vandaan komt en het logo van de bijbehorende dienst. Tik erop om het gesprek te lezen. Het concept toont het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het een Slack-antwoord of een e-mail is.

Als het concept voortbouwt op wat iemand ergens anders heeft gezegd, zoals een suggestie van een teamgenoot in Slack, staat dat erbij, bijvoorbeeld "Gebaseerd op Sam in #ops". Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt als één gesprek getoond, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je eigen berichten rechts, net als in de app. Het bericht van de to-do is gemarkeerd als "Deze to-do" en staat in beeld. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mail staat de rest van het gesprek ingeklapt erboven en eronder.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android opent hij in de Gmail-app als je die hebt.

Onder **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets aan toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Een link van een to-do naar het bijbehorende bericht opent het hier ook, met **Openen in Slack** onderaan.

Onder **Details** staan de naam, het project en het gebied (tik erop om ze te wijzigen), je laatste notitie en het resultaat van een codeeragent. De titel opent de chat. Een afgeronde to-do blijft compact; het bericht waar hij vandaan komt staat onder **Details**.

Een to-do met de status "Wacht op" linkt naar je laatste bericht aan die persoon, waarop je wacht: "E-mail aan Pat · di".

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Een to-do aanmaken verstuurt niets. Als je geen **Werk** of **Privé** kiest, komt hij terecht waar hij thuishoort, op basis van wie en wat erbij hoort. Hij vindt ook de e-mail waarop hij voortbouwt, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals "morgen", "volgende vr", "3 nov", "14:00" of "over 2 uur", ook in je eigen taal. Het kalenderpictogram bevat snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waar de to-do over gaat, maximaal 5.
- Berichtpictogram: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack, Teams, WhatsApp, Telegram of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat zie je waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon maakt de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij eraan werkt. Alleen bestanden zijn genoeg: hij vult de to-do in op basis van een PDF- of tekstbestand. Een foto wordt als kleine afbeelding getoond. Tik erop om hem op ware grootte te bekijken.
