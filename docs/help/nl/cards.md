---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak die je aandacht nodig heeft, klaar om door jou goedgekeurd te worden. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: b218e3423a2162c5
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als iets jouw aandacht nodig heeft. Eén to-do per zaak, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** zijn ze gegroepeerd:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een probleem dat is opgelost terwijl je weg was. Dit blijft maximaal een dag staan, tot je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met eerst wat uiterlijk morgen moet gebeuren. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar, en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven; als het werk niet verder kan of niet gebruikt kan worden zonder iets wat alleen jij hebt, zoals een prijs, feit of keuze, staat er onder de titel wat dat is), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of briefing, waarover je niets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws bij is gekomen (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: gesnoozede to-do's, berichten die [later worden verstuurd](send-later.md) en to-do's waarop je **Nog nodig?** niet hebt beantwoord (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, zoals "5 minuten geleden gedaan". To-do's die al afgerond lijken, krijgen het label **Lijkt gedaan**.

Na het versturen staat er kort waar de to-do naartoe is gegaan, bijvoorbeeld "Verstuurd. Verplaatst naar Gedaan." of "Verstuurd. Verplaatst naar Later tot ma." Een antwoord waarin alleen wordt beloofd dat het werk wordt gedaan, zoals "Ik stuur het uiterlijk dinsdag", laat de to-do openstaan: "Verstuurd. Opengehouden." Met **Openen** ga je naar de to-do. Zoeken vindt to-do's op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's waarvan de deadline is verstreken of uiterlijk morgen valt, dan vragen uit je Fleet, daarna vervolgacties van een bord en vervolgens de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en wanneer hij klaar is. Alleen het label verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of uiterlijk morgen valt bovenaan, gevolgd door de rest, met de nieuwste eerst. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets klaar is, zoals "PR #3451 samengevoegd", maar dat de to-do nog niet is afgesloten. Met **Heropenen** zet je hem terug op je lijst, en je Machine leert ervan. Deze to-do's worden nooit als te laat weergegeven. Als een bericht dit laat zien, wordt de to-do na een dag automatisch afgesloten. Je kunt dat ongedaan maken met **Ongedaan maken**. In andere gevallen wacht hij op **Als gedaan markeren**.

Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook automatisch afgesloten. Een antwoord waarin staat dat er een bestand is bijgevoegd terwijl dat niet zo is, sluit de to-do niet af.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: "Dit is niet Sam Lee." De afzender wordt weergegeven met het eigen e-mailadres, nooit met de naam die diegene heeft opgegeven. Je Machine controleert zo'n bericht bij de persoon van wie je het adres al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, bijvoorbeeld op een review of antwoord, staat **Wacht op:** met de stap waar het om gaat. De to-do staat ingeklapt bij **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem weer naar voren haalt. Hetzelfde geldt nadat je een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline als die later vandaag valt, of de volgende ochtend als de deadline al verstreken is. Je ziet dan op wie hij nog wacht.

Als een to-do draait om een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, toont **Details** dit als **Klaar als**. Je eigen deel versturen sluit de to-do niet af. Hij blijft bij **Wacht op anderen** staan tot een bericht het resultaat laat zien. Daarna wordt hij automatisch afgesloten met het resultaat en **Ongedaan maken**. Als er niets binnenkomt tegen de tijd dat je diegene moet herinneren, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt als je dat wilt aanpassen.

Voordat de to-do wordt afgesloten, controleert je Machine het resultaat aan de hand van wat in de thread is afgesproken, zoals de prijs, tekst of link die je hebt verstuurd. De to-do wordt alleen afgesloten als alles overeenkomt. Je Machine laat zien wat hij heeft gecontroleerd. Als er iets afwijkt, iemand jouw akkoord heeft overgeslagen of jouw deel van een ruil nog niet is afgerond, komt de to-do terug en staat erbij waarom.

Als het resultaat te zien zal zijn op een openbare webpagina die in de berichten wordt genoemd, zoals een artikel waarin jij wordt vermeld, leest je Machine die pagina wanneer het tijd is om diegene te herinneren. Staat het resultaat erop en stond het er nog niet toen de to-do op iemand anders begon te wachten, dan wordt het op dezelfde manier gecontroleerd voordat de to-do wordt afgesloten. Je Machine leest alleen de pagina, zoals elke bezoeker dat zou doen, en verstuurt nooit iets.

Staat het resultaat niet op de pagina en is de deadline nog niet verstreken, dan leest je Machine de pagina de ochtend na de deadline nog een keer. Anders komt de to-do terug zoals gewoonlijk, met "Gecontroleerd" of "Kon niet worden geopend" en de pagina in de chat.

Een to-do waar een week niets nieuws bij is gekomen, wordt verplaatst van Voor jou naar **Ouder**. Zo staan nieuwe to-do's bovenaan als je een paar dagen weg bent geweest. Niets nieuws betekent dat er geen nieuw bericht bij is gekomen en dat jij niets aan de to-do hebt gedaan, zoals een chatbericht sturen, iets aanpassen of snoozen. Alleen bekijken telt niet.

Dringende to-do's, to-do's met een deadline die eraan komt en to-do's waarvan iets onderweg is, blijven bij Voor jou staan. Met **Alles afwijzen** markeer je alle to-do's onder Ouder na één bevestiging als niet nodig, net zoals **Niet nodig** dat voor één to-do doet. Je kunt dit ongedaan maken met **Ongedaan maken**. Komt er iets nieuws bij een to-do, dan gaat hij terug naar Voor jou.

Een to-do waar een week niemand iets mee heeft gedaan, vraagt één keer: **Nog nodig?** Met **Niet nodig** sluit je hem af. Je kunt dit ongedaan maken met **Ongedaan maken**. Met **Houden** blijft hij staan en wordt het niet nog eens gevraagd. Komt er de week daarna geen antwoord, dan wordt de to-do ingeklapt onder Komt later terug. Hij telt dan niet meer mee voor het aantal op het appicoon en in het ochtendoverzicht. Als je hem opent, een chatbericht stuurt, iets aanpast, hem snoozet of er een nieuw bericht binnenkomt, komt hij weer terug.

Eén keer per week kan een project waar het stil is geworden en geen open to-do's meer heeft, een to-do krijgen met één concrete volgende stap. Dit gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als er niets is dat je aandacht nodig heeft, doet je Machine een dutje en blijft je lijst leeg. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk geef je aan of je alle to-do's of alleen één soort wilt zien. Op je telefoon en computer staat dezelfde keuze. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, is niet Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook meteen naar de andere weergave: tik bij **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst vermeldt je laatste ochtend- of avondoverzicht en wat erin is meegeteld, zoals **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen en gebruik **Kopiëren** om het ergens te plakken. Zodra je het opent of op **×** tikt, staat het op al je apparaten tot het volgende overzicht.

Zonder recent overzicht zie je **Vandaag tot nu toe**: wat er vandaag is afgerond en wat nog openstaat, voor Werk en Privé, of alleen voor de weergave die je hebt gekozen.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of verwijder je het. Zie [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De berichten die de to-do mag lezen en waaruit hij mag versturen, verhuizen mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waar hij uit voortkomt daar staan, wordt hij automatisch verplaatst en gaat hij verder. Anders zie je **Naar Werk verplaatsen** en wordt er niets verplaatst tot je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij uit voortkomt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gelabeld, telt als Privé. Mail voor een ander bedrijf van jou hoort bij de to-do's van dat bedrijf. Een to-do over je privéleven, zoals familie die naar je werkadres mailt, is vanaf het begin Privé.

Werk dat je via een privéaccount bereikt, zoals een klant op WhatsApp, een bestelling in je persoonlijke mailbox of een [belofte](promises.md) over werk, is vanaf het begin Werk.

Een to-do die je zelf hebt verplaatst of geplaatst, blijft altijd staan waar je hem hebt neergezet. Werk of Privé bepaalt waar een to-do verschijnt en met wie hij wordt gedeeld, nooit waar hij op antwoordt. Een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij verschijnt nooit in een Werk-Fleet of de Team-Graph.

Als er twee of meer to-do's op je wachten, laat **Doorlopen** in de kop van Voor jou je ze één voor één afwerken, in de volgorde van de lijst. Je ziet elk volledig concept, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stopt Esc. In de kop staat hoe lang het duurt als je je eigen tempo aanhoudt, bijvoorbeeld "ongeveer 2 min".

Aan het einde zie je hoeveel er zijn verstuurd of afgesloten en hoeveel er nog worden voorbereid.

Een to-do die jou iets vraagt, wordt overgeslagen. Daarvoor moet je een antwoord geven, niet ergens op tikken.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert wat is binnengekomen zodra er 40 berichten wachten of het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden meegenomen bij de volgende controle, binnen een uur.

's Nachts pauzeren controles van 00:00 tot 06:30. Nieuwe berichten worden nog wel gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan vóór je ochtendoverzicht. Bij Koppelingen staat onder Controles: "'s Nachts gepauzeerd, haalt om 06:30 in". Als je 's nachts in de app klikt, typt of scrolt, in de chat schrijft of op een to-do tikt, lopen de controles zoals gewoonlijk door tot je een uur weg bent geweest. Met **Nu checken** wordt er altijd meteen gecontroleerd.

Met **Nu checken** worden alle bronnen meteen gelezen. Als er geen open to-do's zijn, tik je op de regel van je Machine om hem te zien, met **Details**. Dat opent Controles onder Koppelingen. Als er open to-do's zijn, staat de regel bovenaan op een computer. Daar zie je kort iets zolang er een controle loopt, of als die is mislukt of te laat is. Je kunt er ook naar vragen in de chat.

LinkedIn, X en Salesflare volgen hun eigen tempo.

## Laatste controle

Na een controle waarin nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met wat er is gevonden uit elke gelezen bron, zoals "13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's" of "· 2 nieuwe to-do's". De regel gaat alleen over die controle. To-do's die al op je lijst staan, blijven gewoon staan. Als een nieuwe to-do wordt uitgesteld tot een beter moment, zoals je ochtendoverzicht, staat erbij tot wanneer: "1 to-do uitgesteld tot morgen 08:30".

Tik op de regel om elke e-mailthread, chat en melding te zien, met het pictogram van de bron. Je ziet wie er heeft geschreven, het onderwerp of de eerste woorden, en de bijbehorende to-do of waarom er niets nodig was, zoals "Alleen in cc, een teamgenoot antwoordt" of "Afspraak staat al voor donderdag". Een thread toont geen reden als de controle alleen een vage reden heeft opgeleverd. Tik op een bericht om het te lezen, met wat eromheen is gezegd.

De eerste 10 worden getoond. Tik onderaan om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een Android-melding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor de context en beloftes, maar tellen niet als nieuwe mail. E-mails van The Machine aan jou, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt zoals gewoonlijk gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Zie [Doe het](do-it.md) en [Snooze](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan of, zodra een concept klaarstaat, wat daarin moet worden aangepast. Laat je je tekst onafgemaakt staan, dan staat die er nog als je terugkomt. Met **Annuleren** verwijder je de tekst.

**Als gedaan markeren** betekent dat het is afgehandeld. Op een computer staat deze knop tussen de andere knoppen als ze op één regel passen. Op een telefoon is hij zichtbaar bij een to-do die klaarstaat zonder concept, of bij een to-do die je iets vraagt. Anders staat hij bovenaan onder **…**. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in de melding. Veeg het bericht weg of sleep het met de muis om de to-do meteen af te sluiten. De wijziging blijft staan.

Wil je dat het op een andere manier wordt afgehandeld, zeg dat dan in de **Chat**. In het antwoord staat alleen wat er is veranderd, zoals een snooze en tot wanneer. Als iets niet kon worden aangepast, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: wijs de to-do toe aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md) of [vraag iemand om een review](ask-to-review.md).
- **Herhalen…**: de to-do [komt op vaste momenten terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt dat ook in de chat vragen, bijvoorbeeld: "Hernoem dit naar …". Je titel blijft staan.

Met **Heropenen** zet je een afgesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van diegene, maar niet na jouw eigen antwoord. Je ziet dan wanneer de to-do is teruggekomen en hij wordt gesorteerd als nieuw. De chat gaat verder waar hij was gebleven, ook na een paar weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, bijvoorbeeld via automatische incasso of een opgeslagen kaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, zoals een bevestiging van de afzender, wordt de to-do automatisch afgesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Een to-do die maar tot een bepaald tijdstip belangrijk was, zoals een bevestiging vóór een meeting, wordt na dat tijdstip automatisch afgesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding "Niet meer nodig". Met **Ongedaan maken** zet je hem een dag lang terug.

Voordat een bericht of overdracht voor iemand klaarstaat, controleert je Machine je recente chats met de betrokkenen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat het al is geregeld, bijvoorbeeld omdat iemand erom heeft gevraagd en een akkoord heeft gekregen, wordt de to-do automatisch afgesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Als iemand anders in hetzelfde gesprek heeft geschreven nadat je concept is gemaakt, houdt **Versturen** het tegen: "Niet verstuurd: nieuw bericht in de thread". Bij de to-do zie je dat bericht met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is vervallen, past The Machine zijn to-do's zelf aan. Een to-do die nog nodig is, volgt het nieuwe plan. Als er niets meer te doen is, wordt hij verplaatst naar **Gedaan / afgewezen** met de melding "Niet nodig". In de chat staat "Bijgewerkt:" met de reden. Met **Ongedaan maken** zet je hem een dag lang terug.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**, en met de uitleg dat er niets wordt verstuurd tot je op **Versturen** drukt. Een tip verdwijnt voorgoed zodra je de bijbehorende knop gebruikt of op × drukt.

Op je eerste dag heet de kop van To-do's je welkom en staat erbij wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat als je begint.

Elke to-do begint met de titel. Op de regel eronder staat op wie de to-do betrekking heeft, de organisatie als het om een organisatie gaat (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van diegene in de Graph te openen.

Bij een naam en organisatie wordt de foto of het logo getoond als de Graph er een heeft. Anders zie je de initialen. Een logo dat op dat formaat niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een brede woordmarkering, wordt ook met een initiaal weergegeven.

Soms staat er een rustige melding met wat niet bekend is, zoals "Laatste contact 12 dagen geleden via e-mail; sindsdien niets." Die verschijnt als het laatste contact met diegene lang geleden was of onbeantwoord bleef, en vermeldt kanalen die niet zijn gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

Een titel zegt wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do behoudt zijn titel, met daaronder hoe hij is afgerond, zoals "Gedaan: Sam heeft het dinsdag ondertekend".

Boven het concept staat een vage regel met het bericht waar het uit voortkomt en het logo van de dienst. Tik erop om de thread te lezen. Het concept toont het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het een Slack-antwoord of e-mail is.

Als het concept voortkomt uit iemands input ergens anders, zoals een suggestie van een teamgenoot in Slack, staat dat op een regel, bijvoorbeeld "Gebaseerd op Sam in #ops". Tik erop om dat bericht te lezen. De regel verdwijnt zodra een bijgewerkt concept het huidige vervangt.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten van vóór het bericht waarop de to-do betrekking heeft en de antwoorden erna. In WhatsApp, Telegram of Signal staan jouw berichten rechts, net als in de app. Bij het bericht van de to-do staat "Deze to-do" en het wordt geopend. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mailthread staan de rest van de berichten ingeklapt erboven en eronder.

Een bericht wordt op dezelfde manier geopend vanuit zoeken, de Graph, antwoorden in Ask of de laatste controle. Het krijgt het label "Dit bericht" of "Nieuwe berichten".

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop die is binnengekomen. Op Android wordt hij geopend in de Gmail-app als je die hebt.

Onder **Details** bij een e-mail staat alleen informatie die niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets aan toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Met de link naar het eigen bericht van een to-do open je dat bericht hier ook, met **Openen in Slack** onderaan.

Onder **Details** staan de naam, het project en het gebied (tik erop om het te wijzigen), je laatste notitie en het resultaat van een codeeragent. De titel opent de chat. Een afgeronde to-do blijft kort; het bericht waar hij uit voortkomt staat onder **Details**.

Een to-do met de melding "Wacht op" linkt naar je laatste bericht aan diegene en het bericht waarop je wacht: "E-mail aan Pat · di".

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Een to-do maken verstuurt niets. Als je **Werk** of **Privé** niet kiest, wordt de to-do geplaatst waar hij thuishoort, op basis van wie en wat het betreft. Je Machine zoekt ook de e-mail waarop hij een vervolg is, zelfs als die al ouder is.

Sluit de to-do voordat je hem toevoegt, dan staan je tekst en keuzes er de volgende keer nog. Bestanden blijven niet bewaard. Met **Weggooien** in het bericht verwijder je ze.

- **Deadline**: typ een dag of tijd, zoals "morgen", "volgende vr", "3 nov", "14:00" of "over 2 uur". Dat kan ook in je eigen taal. Met het kalenderpictogram zie je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt op vaste momenten terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de mensen of bedrijven waarop de to-do betrekking heeft, maximaal 5.
- Berichtpictogram: voeg het bericht toe waarop de to-do betrekking heeft, zoals een e-mail, Slack-, Teams-, WhatsApp-, Telegram- of ander bericht waarover The Machine beschikt. Zoek op tekst of afzender. Bij elk resultaat zie je waar het vandaan komt, wie het heeft gestuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon maak je met de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Tik op × om er een te verwijderen.

De bestanden blijven bij de to-do en je Machine leest ze wanneer hij eraan werkt. Alleen bestanden zijn genoeg: hij vult de to-do in op basis van een pdf of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te bekijken.
