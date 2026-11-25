---
title: To-do's
area: cards
summary: Eén to-do per ding dat je aandacht nodig heeft, klaar voor jouw akkoord. Lees wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 91b111b2d6f2a97b
---
Je Machine leest alles wat nieuw is en maakt alleen een to-do als iets je aandacht nodig heeft. Eén to-do per onderwerp, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een melding, die is afgehandeld terwijl je weg was. Hij blijft er maximaal een dag staan, totdat je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met eerst wat uiterlijk morgen moet gebeuren. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar, en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (eerst is jouw beslissing of antwoord nodig; als het werk niet verder kan of niet kan worden gebruikt zonder iets wat alleen jij hebt, zoals een prijs, feit of keuze, staat onder de titel wat dat is), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of briefing waarover je niets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws bij is gekomen (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarvoor iemand anders aan zet is (zie hieronder).
- **Komt later terug**: gesnoozede to-do's, berichten die [later worden verstuurd](send-later.md) en to-do's waarop nog geen antwoord is op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het moment waarop ze zijn afgerond, zoals "Gedaan 5 minuten geleden". To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Nadat je iets verstuurt, staat er kort waar de to-do naartoe is verplaatst, zoals "Verstuurd. Verplaatst naar Gedaan." of "Verstuurd. Verplaatst naar Later tot ma." Een antwoord dat alleen belooft het werk te doen, zoals "Ik stuur het dinsdag", laat de to-do open: "Verstuurd. Opengehouden." Met **Openen** ga je ernaartoe. Zoeken vindt to-do's op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan to-do's die te laat zijn of uiterlijk morgen moeten gebeuren bovenaan, daarna vragen van je Fleet, vervolgacties van een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en wanneer hij klaar is. Alleen de markering verandert. In de andere open groepen staan to-do's die te laat zijn of uiterlijk morgen moeten gebeuren bovenaan, gevolgd door de rest, met de nieuwste eerst. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat het klaar is, zoals "PR #3451 samengevoegd", maar dat het nog niet is afgesloten. Met **Heropenen** zet je de to-do terug op je lijst. Je Machine leert hiervan. Deze to-do's worden nooit als te laat weergegeven. Als een bericht laat zien dat iets klaar is, wordt de to-do na een dag vanzelf afgesloten, met **Ongedaan maken**. In andere gevallen wacht hij op **Als gedaan markeren**.

Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf afgesloten. Een antwoord waarin staat dat er een bestand is bijgevoegd terwijl dat niet zo is, sluit de to-do niet af.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, bijvoorbeeld sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: "Dit is niet Sam Lee." De persoon wordt weergegeven met diens eigen adres, nooit met de naam die diegene heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon van wie je het adres al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, zoals een review of antwoord, staat **Wacht op:** die stap. De to-do staat ingeklapt in **Wacht op anderen**, boven Komt later terug, totdat een nieuw bericht hem weer naar voren haalt. Hetzelfde geldt nadat je een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline zelf als die later vandaag is, of de volgende ochtend als de deadline voorbij is. Er staat dan ook op wie de to-do nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Als je jouw deel verstuurt, wordt de to-do niet afgesloten. Hij blijft in **Wacht op anderen** staan totdat een bericht laat zien dat het resultaat er is. Daarna wordt hij vanzelf afgesloten, met **Ongedaan maken**. Als er niets binnenkomt op het moment dat je erachteraan moet, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Een to-do waar een week niets nieuws bij is gekomen, verhuist van Voor jou naar **Ouder**, zodat nieuwe to-do's bovenaan staan als je na een paar dagen terugkomt. Niets nieuws betekent dat er geen nieuw bericht is en dat je er niets mee hebt gedaan, zoals een chatbericht sturen, iets aanpassen of snoozen. Alleen bekijken telt niet.

Dringende to-do's, to-do's die bijna moeten gebeuren en to-do's waarvoor iets onderweg is om te versturen, blijven in Voor jou staan. Met **Alles afwijzen** markeer je na één bevestiging alle to-do's in Ouder als niet nodig, net zoals **Niet nodig** dat voor één to-do doet, met **Ongedaan maken**. Als er iets nieuws bij een to-do komt, gaat hij terug naar Voor jou.

Als een to-do een week lang door niemand is aangeraakt, wordt één keer gevraagd: **Nog nodig?** Met **Niet nodig** sluit je hem af, met **Ongedaan maken**. Met **Houden** behoud je de to-do. Daarna wordt het niet nog eens gevraagd. Als je nog een week niet antwoordt, wordt de to-do ingeklapt onder Komt later terug. Hij telt dan niet meer mee voor het aantal op het appicoon of in het ochtendoverzicht. Als je de to-do opent, een chatbericht stuurt, iets aanpast of snoozet, of als er een nieuw bericht binnenkomt, komt hij weer terug.

Een project dat stil is gevallen en geen openstaande to-do's heeft, kan eens per week een to-do krijgen met één concrete volgende stap. Dat gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als niets je aandacht nodig heeft, doet je Machine een dutje op een lege lijst. Terwijl hij controleert, wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen één soort. Je telefoon en computer laten dezelfde keuze zien. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, is niet Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook rechtstreeks over naar de andere selectie: tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst vermeldt je laatste ochtend- of avondoverzicht en wat erin is geteld, zoals **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen. Met **Kopiëren** kun je het overal plakken. Zodra je het opent of op de **×** tikt, staat het op al je apparaten totdat het volgende overzicht verschijnt.

Als er geen recent overzicht is, staat er **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de selectie die je hebt gemaakt.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Zie [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De bronnen waaruit hij mag lezen en waaruit hij mag versturen, gaan mee. Met **Ongedaan maken** in het bericht zet je hem terug.

Als een to-do naar je andere gebied moet om verder te gaan en alle bijbehorende berichten daar staan, wordt hij automatisch verplaatst en gaat hij verder. Anders staat er **Naar Werk verplaatsen**. Er wordt niets verplaatst totdat je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd staat er niet Werk of Privé bij en blijft de to-do privé.

Een to-do kan altijd de berichten lezen waar hij uit voortkomt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gemarkeerd, telt als Privé. Mail voor een ander bedrijf van je hoort bij de to-do's van dat bedrijf. Een to-do over je privéleven, zoals familie die naar je werkadres mailt, is vanaf het begin Privé.

Werk dat je via een privéaccount bereikt, zoals een klant op WhatsApp, een bestelling in je privémailbox of een [belofte](promises.md) over werk, is vanaf het begin Werk.

Een to-do die je zelf hebt verplaatst of ingesteld, blijft altijd staan waar je hem hebt neergezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, nooit waarvandaan hij antwoordt. Een antwoord wordt altijd verstuurd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij verschijnt nooit in een Werk-Fleet of de Team-Graph.

Als er twee of meer to-do's op je wachten, loop je er met **Doorlopen** in de kop van Voor jou één voor één doorheen, in de volgorde van de lijst. Je ziet elk volledig concept met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Druk op een computer op Enter om te versturen wat er op het scherm staat, op `S` om te snoozen, op `→` om over te slaan en op Esc om te stoppen. In de kop staat hoelang het ongeveer duurt, op jouw tempo, zoals "ongeveer 2 min".

Aan het einde staat hoeveel er zijn verstuurd of afgesloten en hoeveel er nog worden voorbereid.

Een to-do met een vraag voor jou wordt in geen van beide gevallen meegenomen. Daarvoor is je antwoord nodig, niet een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert nieuwe berichten zodra er 40 berichten klaarstaan of zodra het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden bij de volgende controle meegenomen, binnen een uur.

's Nachts, van 00:00 tot 06:30, zijn controles gepauzeerd. Nieuwe berichten worden nog steeds gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan voordat je ochtendoverzicht verschijnt. Bij Controles onder Koppelingen staat "'s Nachts gepauzeerd, wordt om 06:30 ingehaald". Als je 's nachts in de app klikt, typt of scrolt, in de chat schrijft of op een to-do tikt, verlopen controles zoals gewoonlijk totdat je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen alle bronnen. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details**, waarmee Controles onder Koppelingen wordt geopend. Als er to-do's openstaan, staat de regel bovenaan op een computer. Hij is daar alleen kort zichtbaar als er een controle bezig is, is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's wat er is gevonden, uit elke gelezen bron, zoals "13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's" of "· 2 nieuwe to-do's". Dit gaat alleen over die controle. To-do's die al op je lijst stonden, blijven zoals ze waren. Als een nieuwe to-do op een beter moment wacht, zoals je ochtendoverzicht, staat erbij tot wanneer: "1 to-do bewaard tot morgen 08:30".

Tik op de regel om elke e-mailthread, chat en melding te bekijken, met het pictogram van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden en de nieuwe to-do of de reden waarom er niets nodig was, zoals "Alleen in cc, een teamgenoot antwoordt" of "Meeting staat al gepland voor donderdag". Bij een thread staat geen reden als de controle alleen een algemene reden opleverde. Tik erop om het bericht te lezen, samen met de berichten eromheen.

De eerste 10 worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle zichtbaar.

Alleen e-mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails die je Machine zelf naar je stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt zoals gewoonlijk gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Zie [Doe het](do-it.md) en [Snooze](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan of, zodra een concept klaarstaat, wat je daarin wilt aanpassen. Als je je tekst nog niet af hebt, staat die er als je terugkomt. Met **Annuleren** gooi je hem weg.

**Als gedaan markeren** betekent dat het is afgehandeld. Op een computer staat deze knop bij de andere knoppen als ze op één regel passen. Op een telefoon is hij zichtbaar bij een klaargezette to-do zonder concept of bij een to-do met een vraag voor jou. Anders staat hij bovenaan onder **…**. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in het bericht. Veeg het bericht weg of sleep het met de muis weg om het sneller af te sluiten. De wijziging blijft staan.

Wil je dat het op een andere manier wordt gedaan, zeg dat dan in de **Chat**. Het antwoord noemt alleen wat er is veranderd, zoals snoozen en tot wanneer. Als iets niet kon worden aangepast, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om een review](ask-to-review.md).
- **Herhalen…**: de to-do [komt regelmatig terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert hiervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt het ook in de chat vragen, bijvoorbeeld: "Hernoem naar …". De titel die je kiest, blijft staan.

Met **Heropenen** zet je een afgesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van die persoon, maar niet als jij zelf antwoordt. Bij terugkomst wordt dat vermeld en wordt de to-do gesorteerd alsof hij nieuw is. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals een automatische incasso of een opgeslagen kaart, niet. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender, wordt de to-do vanzelf afgesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Een to-do die alleen tot een bepaald moment belangrijk was, zoals een bevestiging vóór een meeting, wordt na dat moment vanzelf afgesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding "Niet meer nodig". Met **Ongedaan maken** zet je hem een dag lang terug.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat iets al geregeld is, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do vanzelf afgesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Als iemand anders iets heeft geschreven in hetzelfde gesprek nadat je concept is gemaakt, houdt **Versturen** het tegen: "Niet verstuurd: nieuw bericht in de thread". Bij de to-do staat dat bericht met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept te versturen zoals het is.

Als een nieuwer bericht het plan verandert, bijvoorbeeld doordat een feest naar een andere locatie is verplaatst of een boeking is vervallen, past The Machine de to-do's zelf aan. Een to-do die nog relevant is, volgt het nieuwe plan. Een to-do waarvoor niets meer hoeft te gebeuren, wordt verplaatst naar **Gedaan / afgewezen** met de melding "Niet nodig". In de chat staat "Bijgewerkt:" met de reden. Met **Ongedaan maken** zet je hem een dag lang terug.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd totdat je op **Versturen** drukt. Een tip verdwijnt voorgoed zodra je de bijbehorende knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en staat erbij wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat als je aankomt.

Elke to-do begint met de titel. Op de regel eronder staat op wie de to-do betrekking heeft, de organisatie als die relevant is (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie staat een foto of logo als de Graph die heeft, en anders de initialen. Als een logo op dat formaat niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, worden ook de initialen getoond.

Soms staat er een korte regel met wat niet bekend is, zoals "Laatste contact 12 dagen geleden per e-mail; sindsdien niets." Die regel verschijnt als het laatste contact met iemand lang geleden was of nog onbeantwoord is, en vermeldt kanalen die niet zijn gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

Een titel zegt wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do behoudt zijn titel, met daaronder hoe hij is afgerond, zoals "Gedaan: Sam heeft het dinsdag ondertekend".

Boven het concept staat een vage regel met het bericht waar het uit voortkomt, met het logo van die dienst. Tik erop om de thread te lezen. Het concept toont het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het een Slack-antwoord of een e-mail is.

Als het concept voortkomt uit iemands bijdrage op een andere plek, zoals een suggestie van een teamgenoot in Slack, staat dat erbij, bijvoorbeeld "Gebaseerd op Sam in #ops". Tik erop om dat bericht te lezen. De regel verdwijnt zodra een update dat concept vervangt.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt als één gesprek weergegeven, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Het bericht van de to-do is gemarkeerd als "Deze to-do" en wordt geopend in beeld. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Een e-mailthread wordt erboven en eronder ingeklapt weergegeven.

Een bericht wordt op dezelfde manier geopend vanuit zoeken, de Graph, antwoorden van Ask of de laatste controle, met de markering "Dit bericht" (of "Nieuwe berichten").

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android wordt hij geopend in de Gmail-app als je die hebt.

Bij **Details** van een e-mail staat alleen wat niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets aan toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread wordt ook getoond wat er is gezegd voordat de thread begon. Met de link van een to-do open je ook hier het bijbehorende bericht, met onderaan **Openen in Slack**.

Bij **Details** staan de naam, het project en het gebied (tik erop om iets te wijzigen), je laatste notitie en het resultaat van een codeeragent. De titel opent de chat. Een afgeronde to-do blijft kort. Het bericht waar hij uit voortkomt, staat onder **Details**.

Een to-do met de status "Wacht op" linkt naar je laatste bericht aan die persoon en het bericht waarop je wacht: "E-mail aan Pat · di".

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Als je er een maakt, wordt er niets verstuurd. Als je geen **Werk** of **Privé** kiest, wordt de to-do geplaatst waar hij hoort, op basis van wie en wat erbij betrokken is. Je Machine zoekt ook de e-mail waarop de to-do een vervolg is, zelfs als die ouder is.

Als je het venster sluit voordat je de to-do hebt toegevoegd, blijven je tekst en keuzes bewaard voor de volgende keer. Bestanden niet. Met **Weggooien** in het bericht verwijder je ze.

- **Deadline**: typ een dag of tijd, zoals "morgen", "volgende vr", "3 nov", "14:00" of "over 2 uur", ook in je eigen taal. Het kalenderpictogram bevat snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt regelmatig terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waar de to-do over gaat, maximaal 5.
- Berichtpictogram: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp- of Telegram-bericht, of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do staan. Je Machine leest ze wanneer hij eraan werkt. Alleen bestanden toevoegen is genoeg: uit een PDF of tekstbestand vult hij de to-do zelf aan. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op volledig formaat te bekijken.
