---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak die je aandacht vraagt, klaar om door jou goedgekeurd te worden. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 51db64e67403d2ea
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als er iets van je nodig is. Eén to-do per zaak, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze per groep:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een probleem, en die is uitgevoerd terwijl je weg was. Hij blijft er maximaal een dag staan, tot je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (er staat een concept of resultaat klaar en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (eerst moet je een beslissing nemen of antwoord geven; als het werk stilvalt omdat alleen jij iets hebt, zoals een feit, een login of een keuze, staat dat onder de titel), **Aan het voorbereiden…** (je Machine werkt eraan) of **Om te lezen** (een overzicht of briefing, niets om over te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws bij is gekomen (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's zonder antwoord op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, nieuwste eerst, met het tijdstip waarop ze zijn afgerond, zoals "5 minuten geleden gedaan". To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Na het versturen staat er kort waar de to-do naartoe is gegaan, zoals "Verstuurd. Verplaatst naar Gedaan." of "Verstuurd. Verplaatst naar Later tot maandag." Een antwoord waarin alleen wordt beloofd dat het werk wordt gedaan, zoals "Ik stuur het dinsdag", laat de to-do open: "Verstuurd. Open gelaten." Met **Openen** ga je naar de to-do. Zoeken vindt to-do's op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's waarvan de deadline verstreken is of uiterlijk morgen valt, dan vragen van je Fleet, daarna vervolgacties van een bord en dan de rest. Binnen elke groep staan de nieuwste eerst. Een to-do blijft op dezelfde plek staan terwijl je Machine eraan werkt en wanneer hij klaar is. Alleen de markering verandert. In de andere open groepen staan to-do's waarvan de deadline verstreken is of uiterlijk morgen valt bovenaan, en de rest staat op volgorde van nieuw naar oud. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets klaar is, zoals "PR #3451 samengevoegd", maar dat het nog niet is afgesloten. Met **Heropenen** zet je het terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat weergegeven. Als er een bericht bij staat, wordt de to-do na een dag vanzelf afgesloten, met **Ongedaan maken** als optie. Anders wacht hij op **Als gedaan markeren**. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf afgesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: "Dit is Sam Lee niet." De afzender wordt getoond met het eigen e-mailadres, nooit met de naam die is gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, zoals een beoordeling of antwoord, staat **Wacht op:** met die stap. De to-do staat ingeklapt in **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem weer naar voren haalt. Hetzelfde gebeurt nadat jij een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline zelf als die later vandaag valt, of de volgende ochtend nadat de deadline is verstreken. Er staat dan bij op wie hij nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Je eigen deel versturen sluit de to-do niet af. Hij blijft in **Wacht op anderen** tot een bericht het resultaat laat zien en wordt dan vanzelf afgesloten, met **Ongedaan maken** als optie. Als er niets binnenkomt tegen de tijd dat je iemand moet herinneren, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Een to-do waar een week niets nieuws bij is gekomen, gaat van Voor jou naar **Ouder**, zodat je na een paar dagen weg eerst de nieuwe to-do's ziet. Niets nieuws betekent dat er geen nieuw bericht bij is gekomen en dat jij er niets mee hebt gedaan, zoals een chatbericht sturen, iets aanpassen of snoozen. Alleen openen telt niet.

Dringende to-do's, to-do's met een naderende deadline en to-do's die bijna worden verstuurd, blijven in Voor jou staan. Met **Alles afwijzen** markeer je alle to-do's in Ouder na één bevestiging als niet nodig, net zoals je dat één voor één doet met **Niet nodig**, met **Ongedaan maken** als optie. Als er iets nieuws bij een to-do komt, gaat hij terug naar Voor jou.

Een to-do waar een week niemand iets mee heeft gedaan, vraagt één keer: **Nog nodig?** Met **Niet nodig** sluit je hem af, met **Ongedaan maken** als optie. **Houden** laat hem staan. De vraag wordt dan niet meer gesteld. Als er nog een week geen antwoord komt, wordt de to-do ingeklapt onder Komt later terug. Hij telt dan niet meer mee op het appicoon en in het ochtendoverzicht. Openen, een chatbericht, een wijziging, snoozen of een nieuw bericht brengt hem terug.

Eén keer per week kan een project dat stil is komen te liggen en geen open to-do's heeft, een to-do krijgen met één concrete volgende stap. Dat gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als er niets is waarvoor je nodig bent, rust je Machine bij een lege lijst. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk geef je aan of je alle to-do's of maar één soort wilt zien. Op je telefoon en computer wordt dezelfde keuze gebruikt. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en staat alleen onder Alle.

De regel bovenaan de lijst schakelt ook direct naar de andere weergave: tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst toont de naam van je laatste ochtend- of avondoverzicht en wat erin is meegeteld, zoals **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen. Met **Kopiëren** kun je het ergens plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, staat er **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt gekozen.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je het weg. Zie [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De berichten die hij mag lezen en waaruit hij mag versturen, verhuizen mee. Met **Ongedaan maken** in de melding verplaats je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waar hij vandaan komt daar staan, wordt hij vanzelf naar dat gebied verplaatst en gaat hij verder. Anders staat er **Naar Werk verplaatsen** en wordt er niets verplaatst tot je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gemarkeerd, telt als Privé. Mail voor een van je andere bedrijven komt bij de to-do's van dat bedrijf terecht. Een to-do over je eigen leven, zoals familie die naar je werkadres mailt, is vanaf het begin Privé.

Werk dat je via een persoonlijk account bereikt, zoals een klant op WhatsApp of een bestelling in je persoonlijke mailbox, is vanaf het begin Werk. Een to-do die je zelf hebt verplaatst of ingedeeld, blijft altijd staan waar je hem hebt gezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, maar niet waar hij op antwoordt. Een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij verschijnt nooit in een Werk-Fleet of de Team-Graph.

Als er twee of meer to-do's op je wachten, loop je met **Doorlopen** in de kop van Voor jou één voor één door de lijst, in de volgorde waarin ze staan. Je ziet elk concept helemaal, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, met `S` snooze je, met `→` sla je over en met Esc stop je. In de kop staat hoe lang je er op jouw tempo over doet, zoals "ongeveer 2 min".

Aan het einde zie je hoeveel er zijn verstuurd of afgesloten en hoeveel er nog worden voorbereid.

Een to-do waarin je een vraag wordt gesteld, wordt overgeslagen. Daarvoor is een antwoord nodig, geen tik.

## Nu checken

Je Machine leest elke paar minuten elke bron, dag en nacht. Hij controleert wat er is binnengekomen zodra er 40 berichten klaarstaan of het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden bij de volgende controle meegenomen, binnen een uur.

's Nachts, van 00:00 tot 06:30, zijn controles gepauzeerd. Nieuwe berichten worden wel gelezen en bewaard, en om 06:30 tegelijk gecontroleerd, zodat je to-do's klaarstaan vóór je ochtendoverzicht. Bij Controles onder Koppelingen staat "'s Nachts gepauzeerd, haalt om 06:30 in". Klik, typ of scroll je 's nachts in de app, schrijf je in de chat of tik je op een to-do, dan verlopen controles zoals gewoonlijk tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen alle bronnen. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, staat de regel bovenaan op een computer. Er verschijnt alleen kort een regel als er een controle loopt, mislukt is of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare volgen hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat boven je to-do's wat er is gevonden in alle gelezen bronnen, zoals "13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's" of "· 2 nieuwe to-do's". Dit gaat alleen over die controle. To-do's die al op je lijst stonden, blijven gewoon staan. Als een nieuwe to-do wacht op een beter moment, zoals je ochtendoverzicht, staat erbij tot wanneer: "1 to-do bewaard tot morgen 08:30".

Tik op de regel om elke e-mailthread, chat en melding te bekijken, met het pictogram van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden en de nieuwe to-do of de reden waarom er niets nodig was, zoals "Alleen in cc, een teamgenoot antwoordt" of "Meeting staat al gepland voor donderdag". Bij een thread wordt geen reden getoond als de controle alleen een vage reden opleverde. Tik erop om het bericht te lezen.

De eerste 10 worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails van The Machine aan jou, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt wel gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan, of, zodra een concept klaarstaat, wat daarin moet veranderen. Met **Als gedaan markeren** geef je aan dat het is afgehandeld. Deze knop staat direct in beeld bij een to-do die klaarstaat zonder concept of bij een to-do waarin je een vraag wordt gesteld. Anders staat hij bovenaan onder **…**. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in het bericht. Veeg het bericht weg of sleep het met de muis uit beeld om het eerder af te sluiten. De wijziging blijft staan.

Wil je dat het op een andere manier wordt gedaan, zeg dat dan in de **Chat** van de to-do. In het antwoord staat alleen wat er is veranderd, zoals een snooze en tot wanneer. Als iets niet kon worden aangepast, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om een beoordeling](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt ook iets vragen in de chat, zoals "Hernoem dit naar …". Je titel blijft staan.

Met **Heropenen** haal je een afgesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van die persoon, maar niet bij je eigen antwoord. Je ziet dan wanneer hij is teruggekomen en hij wordt gesorteerd als nieuw. De chat gaat verder waar hij gebleven was, ook na een paar weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals een automatische incasso of een opgeslagen kaart, worden dat niet. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender dat de betaling is ontvangen, wordt de to-do vanzelf afgesloten. Met **Ongedaan maken** haal je hem binnen een dag terug.

Een to-do die alleen tot een bepaald tijdstip van belang was, zoals een bevestiging vóór een meeting, wordt na dat tijdstip vanzelf afgesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding "Niet langer nodig". Met **Ongedaan maken** haal je hem binnen een dag terug.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack die heeft gelezen. Als een later bericht laat zien dat het al is geregeld, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do vanzelf afgesloten. Met **Ongedaan maken** haal je hem binnen een dag terug.

Als iemand anders iets in hetzelfde gesprek heeft geschreven nadat het concept is gemaakt, houdt **Versturen** het tegen: "Niet verstuurd: nieuw bericht in de thread". Bij de to-do staat dat bericht, met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is geannuleerd, werkt The Machine de to-do's zelf bij. Een to-do die nog nodig is, volgt het nieuwe plan. Een to-do waarvoor niets meer hoeft te gebeuren, wordt verplaatst naar **Gedaan / afgewezen** met de melding "Niet nodig". In de chat staat "Bijgewerkt:" met de reden. Met **Ongedaan maken** haal je hem binnen een dag terug.

Bij je eerste to-do's zie je een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd tot je op **Versturen** drukt. De tip verdwijnt voorgoed zodra je de bijbehorende knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en staat erbij wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat wanneer je aankomt.

Elke to-do begint met de titel. Op de regel eronder staat op wie de to-do betrekking heeft, de organisatie als die relevant is (niet alleen omdat iemand er werkt), het project, Werk of Privé en wanneer het bericht is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie staat een foto of logo als de Graph die heeft, anders de initialen. Als een logo op die grootte niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, worden ook de initialen getoond.

Soms staat er een rustige melding met informatie die ontbreekt, zoals "Laatste contact 12 dagen geleden via e-mail, sindsdien niets". Die verschijnt als het laatste contact met iemand lang geleden was of onbeantwoord is, en vermeldt kanalen die niet zijn gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van iets te raden.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

De titel zegt wat er moet gebeuren en verandert alleen als dat ook verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe hij is afgerond, zoals "Gedaan: Sam heeft dinsdag getekend".

Boven het concept staat een subtiele regel met het bericht waar het vandaan komt en het logo van die dienst. Tik erop om de thread te lezen. Het concept toont het logo van de bestemming, zodat je meteen ziet of het om een Slack-antwoord of een e-mail gaat.

Als het concept is gebaseerd op input van iemand ergens anders, zoals een suggestie van een teamgenoot in Slack, staat dat op een regel, zoals "Gebaseerd op Sam in #ops". Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt als één gesprek weergegeven, van oud naar nieuw: de berichten vóór het bericht waarop de to-do betrekking heeft en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Het bericht van de to-do is gemarkeerd met "Deze to-do" en wordt geopend in beeld. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mail staat de rest van de thread ingeklapt erboven en eronder.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android wordt de Gmail-app geopend als je die hebt.

Bij **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige cc-adressen, bcc of een ander antwoordadres. Als er niets toe te voegen is, zie je geen details.

Bij een antwoord in een Slack-thread zie je ook wat er vóór de thread is gezegd. De link van een to-do naar het bijbehorende bericht opent dat hier ook, met **Openen in Slack** onderaan.

Bij **Details** staan de naam, het project en het gebied (tik erop om dit te wijzigen), je laatste notitie en het resultaat van een coding agent. Met de titel open je de chat. Een afgeronde to-do blijft compact. Het bericht waar hij vandaan komt, staat onder **Details**.

Bij een to-do met "Wacht op" link je naar je laatste bericht aan die persoon en naar het bericht waarop je wacht: "E-mail aan Pat · di".

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je voor alles een to-do toe. Er wordt niets verstuurd als je er een maakt. Als je **Werk** of **Privé** niet kiest, komt de to-do terecht waar hij thuishoort, op basis van wie en waarover hij gaat. Hij zoekt ook de e-mail op waar hij bij hoort, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals "morgen", "volgende vr", "3 nov", "14:00" of "over 2 uur". Dat kan ook in je eigen taal. Het kalendericoon bevat snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waar de to-do over gaat, maximaal 5.
- Berichticoon: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp-, Telegram- of ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft gestuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Maximaal 5 bestanden, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × haal je een bestand weer weg.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij eraan werkt. Alleen bestanden zijn genoeg: hij vult de to-do in op basis van een PDF- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te bekijken.
