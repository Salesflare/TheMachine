---
title: To-do's
area: cards
summary: Eén to-do voor elk ding dat je aandacht nodig heeft, klaar zodat jij alleen nog hoeft te bevestigen. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 84b8879d98f26aa2
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als iets je aandacht nodig heeft. Eén to-do per kwestie, hoeveel berichten er ook bij horen.

## Waar je to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een melding die is verwerkt terwijl je weg was. Hij blijft staan tot je op **Begrepen** tikt, maximaal één dag, en je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (het werk is gedaan en **Doe het** of **Versturen** voert het uit), **Wacht op jou** (er is eerst een beslissing of antwoord van je nodig), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of briefing, zonder dat je iets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws mee is gebeurd (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij iemand anders aan zet is (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop je niet hebt gereageerd bij **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Bekijk [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, bijvoorbeeld "5 minuten geleden gedaan". To-do's die al afgerond lijken, hebben het label **Lijkt gedaan**.

Nadat je iets verstuurt, staat er kort waar de to-do naartoe is verplaatst, bijvoorbeeld "Verstuurd. Verplaatst naar Gedaan." of "Verstuurd. Verplaatst naar Later tot ma." Als een antwoord alleen belooft dat het werk wordt gedaan, zoals "Ik stuur het dinsdag", blijft de to-do open: "Verstuurd. Open gelaten." Met **Openen** ga je naar de to-do. Je kunt een to-do zoeken op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's waarvan de deadline is verstreken of morgen valt, daarna vragen van je Fleet, vervolgens vervolgacties van een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem klaarmaakt en wanneer hij is afgerond: alleen het label verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of morgen valt eerst, daarna de rest, met de nieuwste bovenaan. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, zoals "PR #3451 is samengevoegd", maar dat het nog niet is gesloten. Met **Heropenen** zet je het terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat getoond. Na een dag wordt de to-do vanzelf gesloten, met **Ongedaan maken** als optie. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf gesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: "Dit is Sam Lee niet." De afzender wordt weergegeven met het eigen adres, nooit met de naam die diegene heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Bij een to-do waarbij je nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, staat **Wacht op:** met de stap die nog moet gebeuren. De to-do staat ingeklapt onder **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem weer naar voren haalt. Dat geldt ook nadat je zelf een vraag hebt teruggestuurd: de to-do komt terug op de ochtend vóór de deadline, op de deadline zelf als die later die dag valt, of de volgende ochtend als de deadline al voorbij is. Er staat dan ook bij op wie je nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Je eigen deel versturen sluit de to-do niet af: hij blijft onder **Wacht op anderen** staan tot een bericht laat zien dat het resultaat er is. Daarna wordt hij vanzelf gesloten, met **Ongedaan maken** als optie. Komt er niets binnen voor het tijd is om diegene eraan te herinneren, dan verschijnt de to-do weer met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Een to-do waar een week niets nieuws mee is gebeurd, wordt verplaatst van Voor jou naar **Ouder**. Zo staan nieuwe to-do's bovenaan als je na een paar dagen terugkomt. Er is niets nieuws gebeurd als er geen nieuw bericht over is binnengekomen en je er zelf niets mee hebt gedaan, bijvoorbeeld geen chatbericht, wijziging of snooze. Alleen de to-do bekijken telt niet mee.

Dringende to-do's, to-do's met een deadline die eraan komt en to-do's die worden verstuurd, blijven onder Voor jou staan. Met **Alles als niet nodig markeren** markeer je alle to-do's onder Ouder na één bevestiging als niet nodig, net zoals je dat één voor één kunt doen met **Niet nodig**. Je kunt dit ongedaan maken met **Ongedaan maken**. Als er iets nieuws gebeurt met een to-do, komt hij terug onder Voor jou.

Bij een to-do waar een week niemand iets mee heeft gedaan, verschijnt één keer de vraag **Nog nodig?** Met **Niet nodig** sluit je de to-do, met **Ongedaan maken** als optie. Met **Houden** houd je de to-do en wordt dit nooit meer gevraagd. Als je nog een week niet reageert, wordt de to-do ingeklapt onder Komt later terug. Hij telt dan niet meer mee op het appicoon of in het ochtendoverzicht. Als je de to-do opent, er een chatbericht of wijziging aan toevoegt, hem snoozet of er een nieuw bericht binnenkomt, wordt hij weer zichtbaar.

Een project waar al een tijd niets gebeurt en geen open to-do's heeft, kan één keer per week een to-do krijgen met één specifieke volgende stap. Dit gebeurt maximaal drie keer per week. Bekijk [Projecten](projects.md).

Als niets je aandacht nodig heeft, doet je Machine een dutje en blijft de lijst leeg. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of vertraging heeft, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen één soort. Op je telefoon en computer wordt dezelfde keuze gebruikt. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar de volledige lijst. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, valt niet onder Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook meteen naar de andere weergave: tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst vermeldt de naam van je laatste ochtend- of avondoverzicht en wat daarin is meegeteld, bijvoorbeeld **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om het overzicht opnieuw te lezen. Met **Kopiëren** kun je het overal plakken. Zodra je het opent of op **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, staat er **Vandaag tot nu toe**: wat er vandaag is afgerond en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt gekozen.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Bekijk [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De bronnen waaruit de to-do mag lezen en waaraan hij mag versturen, verhuizen mee. Met **Ongedaan maken** in het bericht zet je de to-do terug.

Als een to-do naar je andere gebied moet om verder te gaan en alle bijbehorende berichten daar staan, wordt hij vanzelf daarheen verplaatst en gaat hij verder. Anders verschijnt **Naar Werk verplaatsen** en wordt er niets verplaatst tot je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd valt hij niet onder Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waaruit hij is ontstaan. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij je om **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt aangemerkt, telt als Privé. Mail voor een ander bedrijf van je komt bij de to-do's van dat bedrijf terecht. Een to-do over je privéleven, zoals familie die naar je werkadres mailt, valt vanaf het begin onder Privé.

Werk dat binnenkomt op een persoonlijk account, zoals een klant op WhatsApp of een bestelling in je persoonlijke mailbox, valt vanaf het begin onder Werk. Een to-do die je zelf hebt verplaatst of toegewezen, blijft altijd staan waar jij hem hebt gezet. Werk of Privé bepaalt waar een to-do wordt getoond en met wie hij wordt gedeeld, nooit waar hij op antwoordt: een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n to-do onder Privé antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen en verschijnt nooit in een Work Fleet of de Team Graph.

Als je op minstens twee to-do's wacht, doorloop je ze met **Doorlopen** in de kop van Voor jou één voor één, in de volgorde van de lijst. Elke to-do wordt volledig weergegeven, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuur je met Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stop je met Esc. Onder de titel staat in de kop ook hoelang het op je eigen tempo duurt, bijvoorbeeld "ongeveer 2 min".

Een to-do met een vraag aan jou wordt overgeslagen: daarvoor is je antwoord nodig, niet een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert wat er is binnengekomen zodra er 40 berichten klaarstaan of het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en betalingsbewijzen worden meegenomen bij de volgende controle, binnen een uur.

Tussen 00:00 en 06:30 staan controles 's nachts stil. Nieuwe berichten worden nog steeds gelezen en bewaard, en om 06:30 tegelijk gecontroleerd, zodat je to-do's klaarstaan vóór je ochtendoverzicht. Bij Controles onder Koppelingen staat "'s Nachts gepauzeerd, haalt de achterstand om 06:30 in". Als je 's nachts in de app klikt, typt of scrollt, in de chat schrijft of op een to-do tikt, worden controles zoals gewoonlijk uitgevoerd tot je een uur weg bent geweest. Met **Nu checken** wordt er altijd meteen gecontroleerd.

Met **Nu checken** worden alle bronnen meteen gelezen. Als er niets openstaat, tik je op de regel van je Machine om die te bekijken, met **Details** om Controles onder Koppelingen te openen. Als er to-do's openstaan, staat de regel bovenaan op een computer. Een korte melding verschijnt daar alleen tijdens een controle, of als er een is mislukt of vertraging heeft. Je kunt er ook naar vragen in de chat.

LinkedIn, X en Salesflare volgen hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met de resultaten van alle gelezen bronnen, bijvoorbeeld "13 berichten gecontroleerd om 16:11 · niets nodig" of "· 2 nieuwe to-do's". Als een nieuwe to-do wacht op een geschikter moment, zoals je ochtendoverzicht, staat erbij tot wanneer: "1 to-do uitgesteld tot morgen 08:30".

Tik op de regel om alle e-mailthreads, chats en meldingen te bekijken, met het pictogram van de bron erbij: wie het bericht heeft gestuurd, het onderwerp of de eerste woorden, en de nieuwe to-do of de reden dat er niets nodig was, zoals "Alleen in cc, een teamgenoot antwoordt" of "Afspraak voor donderdag staat al". Bij een thread wordt geen reden getoond als de controle alleen een vage reden opleverde. Tik op een item om het te lezen.

De eerste 10 worden getoond. Tik eronder om de rest te bekijken. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle zichtbaar.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails van The Machine aan jou, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt zoals gewoonlijk gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Bekijk [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan of, zodra een concept klaarstaat, wat daarin moet worden aangepast. **Markeren als gedaan** betekent dat het is afgehandeld. Deze optie staat direct in beeld bij een klaargezette to-do zonder concept, en anders bovenaan onder **…**, ook bij een to-do waarvoor je eerst een beslissing moet nemen. De to-do verdwijnt meteen van de lijst. Je kunt dit ongedaan maken via het bericht. Veeg het bericht weg of sleep het met de muis naar buiten om het sneller te sluiten. De wijziging blijft behouden.

Wil je het op een andere manier laten doen, zeg dat dan in de **Chat**.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om hem te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt regelmatig terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt dit ook vragen in de chat, bijvoorbeeld "Hernoem naar …". Je eigen titel blijft staan.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, bijvoorbeeld als je een nieuw bericht van diegene krijgt, maar niet na je eigen antwoord. Je ziet dan wanneer de to-do is teruggekomen en hij wordt als nieuw gesorteerd. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, bijvoorbeeld via automatische incasso of een opgeslagen kaart, niet. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender, wordt de to-do vanzelf gesloten. Je kunt dit een dag lang ongedaan maken met **Ongedaan maken**.

Een to-do die maar tot een bepaald tijdstip nodig is, bijvoorbeeld een bevestiging vóór een vergadering, wordt daarna vanzelf gesloten. Hij wordt als "Niet meer nodig" verplaatst naar **Gedaan / afgewezen**. Je kunt dit een dag lang ongedaan maken met **Ongedaan maken**.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokkenen, inclusief groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat iets al is geregeld, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do vanzelf gesloten. Je kunt dit een dag lang ongedaan maken met **Ongedaan maken**.

Als een nieuwer bericht het plan wijzigt, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is geannuleerd, werkt The Machine zijn to-do's zelf bij. Een to-do die nog nodig is, volgt het nieuwe plan. Als er niets meer te doen is, wordt hij als "Niet nodig" verplaatst naar **Gedaan / afgewezen**. In de chat staat "Bijgewerkt:" met de reden. Je kunt dit een dag lang ongedaan maken met **Ongedaan maken**.

Bij je eerste to-do's verschijnt een korte tip over de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd tot je op **Versturen** drukt. De tip verdwijnt voorgoed zodra je de knop gebruikt of op × drukt.

Op je eerste dag staat er bovenaan To-do's een welkomstbericht met de naam van degene die het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat als je aankomt.

Elke to-do begint met de titel. Op de regel eronder staat op wie de to-do betrekking heeft, de organisatie als die relevant is (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer het bericht is binnengekomen. Tik op een naam om de pagina van diegene in Graph te openen.

Bij namen en organisaties wordt een foto of logo getoond als Graph die heeft, anders de initialen. Bij een logo dat op dat formaat niet goed leesbaar is, zoals witte tekst op een transparante achtergrond of een breed woordlogo, wordt ook de initiaal getoond.

Soms staat er een korte, gedempte melding met iets wat niet bekend is, zoals "Laatste contact 12 dagen geleden per e-mail; sindsdien niets." Deze verschijnt als het laatste contact lang geleden was of onbeantwoord is gebleven. Ook worden niet-gekoppelde kanalen genoemd, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van iets te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

Een titel beschrijft wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe hij is afgerond, bijvoorbeeld "Gedaan: Sam heeft het dinsdag ondertekend".

Boven het concept staat een gedempte regel met het bericht waaruit de to-do is ontstaan en het logo van die dienst. Tik erop om de thread te lezen. Het concept toont het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het een Slack-antwoord of een e-mail is.

Als het concept is gebaseerd op iemands bijdrage elders, zoals een suggestie van een teamgenoot in Slack, staat dat op een regel, bijvoorbeeld "Gebaseerd op Sam in #ops". Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt als één gesprek weergegeven, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je eigen berichten rechts, zoals in de app. Bij het bericht waar de to-do over gaat, staat "Deze to-do". Tik erop om het te openen. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Een e-mailthread wordt erboven en eronder ingeklapt weergegeven.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android opent hij in de Gmail-app als je die hebt.

Bij **Details** van een e-mail staan alleen gegevens die niet in de kop staan, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets toe te voegen is, wordt dit niet weergegeven.

Bij een antwoord in een Slack-thread staat ook wat er is gezegd voordat de thread begon. Een link in een to-do naar het bijbehorende bericht opent dat hier ook, met **Openen in Slack** onderaan.

Onder **Details** staan de naam, het project en het gebied (tik erop om dit te wijzigen), je laatste notitie en het resultaat van een codeeragent. De titel opent de chat. Een afgeronde to-do blijft compact; het bijbehorende bericht staat onder **Details**.

Bij een to-do met "Wacht op" staat een link naar je laatste bericht aan diegene, het bericht waarop je wacht: "E-mail aan Pat · di".

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) maak je een to-do voor wat dan ook. Als je er een maakt, wordt er niets verstuurd. Als je **Werk** of **Privé** niet kiest, komt de to-do terecht waar hij hoort, op basis van wie en waarover hij gaat. Ook vindt hij de e-mail waarop hij betrekking heeft, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals "morgen", "volgende vr", "3 nov", "14:00" of "over 2 uur", ook in je eigen taal. Met het kalendericoon zie je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt regelmatig terug. Bekijk [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waar de to-do over gaat, maximaal 5.
- Berichtenicoon: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp- of Telegram-bericht, of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een schermafbeelding of sleep bestanden naar het formulier. Op een telefoon maak je met de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze als hij eraan werkt. Alleen bestanden zijn al genoeg: hij vult de to-do in op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op volledig formaat te bekijken.
