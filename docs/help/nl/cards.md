---
title: To-do's
area: cards
summary: Eén to-do per zaak die je aandacht vraagt, klaar om door jou goed te keuren. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: c54b334f5764bdf9
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do aan als er iets is waarvoor je nodig bent. Eén to-do per zaak, ongeacht het aantal berichten.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan staat de laatste stap die je hebt bevestigd, zoals een formulier of een issue dat is verwerkt terwijl je weg was. Hij blijft maximaal een dag staan, totdat je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (het werk is gedaan en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (eerst is je beslissing of antwoord nodig), **Aan het voorbereiden…** (je Machine werkt eraan) of **Om te lezen** (een overzicht of briefing, waarover je niets hoeft te beslissen).
- **Wacht op anderen**: hier staan to-do's ingeklapt waarvoor de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: to-do's die zijn gesnoozed en to-do's waarop geen antwoord kwam op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Bekijk [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, nieuwste eerst, met het tijdstip waarop ze zijn afgerond, zoals "Gedaan: 5 minuten geleden". To-do's die al afgerond lijken, krijgen het label **Lijkt gedaan**.

Nadat je iets hebt verstuurd, staat er kort waar de to-do naartoe is gegaan, zoals "Verstuurd. Verplaatst naar Gedaan." of "Verstuurd. Verplaatst naar Later, tot ma." Met **Openen** ga je naar de to-do. Je kunt zoeken op de titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's waarvan de deadline is verstreken of morgen valt, daarna vragen uit je Fleet, vervolgens vervolgacties van een bord en daarna de rest. Binnen elke groep staan de nieuwste eerst. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en nadat hij is afgerond: alleen het label verandert. In de andere open groepen staan to-do's met een verstreken deadline of een deadline morgen eerst, gevolgd door de rest, nieuwste eerst. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets klaar is, zoals "PR #3451 is gemerged", maar dat het nog niet is gesloten. Met **Heropenen** zet je de to-do terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat getoond. Na een dag sluit hij de to-do automatisch, met **Ongedaan maken** als optie. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld door te antwoorden in Gmail of Slack, wordt ook automatisch gesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, bijvoorbeeld sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: "Dit is Sam Lee niet." Je ziet de afzender met het eigen e-mailadres, nooit met de naam die diegene zelf heeft opgegeven. Je Machine controleert zo'n bericht bij de persoon van wie je het adres al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, staat **Wacht op:** gevolgd door die stap. De to-do staat ingeklapt bij **Wacht op anderen**, boven Komt later terug, totdat een nieuw bericht hem weer naar voren haalt. Hetzelfde geldt nadat je zelf een vraag hebt teruggesteld: de to-do komt terug op de ochtend voor de deadline, op de deadline zelf als die later vandaag valt, of de volgende ochtend als de deadline is verstreken. Je ziet dan ook op wie hij nog wacht.

Gaat een to-do over een resultaat dat iemand anders moet leveren, zoals een ondertekend contract, dan staat dat bij **Details** onder **Klaar als**. Als je jouw deel verstuurt, wordt de to-do niet gesloten: hij blijft bij **Wacht op anderen** staan totdat een bericht het resultaat bevestigt. Daarna sluit hij automatisch, met **Ongedaan maken** als optie. Is er nog niets binnen op het moment dat je erachteraan moet, dan komt hij terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Als iemand een week niets met een to-do heeft gedaan, wordt één keer gevraagd: **Nog nodig?** Met **Niet nodig** sluit je hem, met **Ongedaan maken** als optie. Met **Houden** blijft hij staan en wordt het niet nog een keer gevraagd. Komt er nog een week geen antwoord, dan wordt hij ingeklapt onder Komt later terug en telt hij niet meer mee voor het cijfer op het appicoon of het ochtendoverzicht. Als je hem opent, een chatbericht stuurt, bewerkt, snoozet of er een nieuw bericht binnenkomt, komt hij weer terug.

Eén keer per week kan er voor een project zonder openstaande to-do's een to-do verschijnen met één concrete volgende stap. Dat gebeurt maximaal drie keer per week. Bekijk [Projecten](projects.md).

Als er niets is waarvoor je nodig bent, doet je Machine een dutje en blijft de lijst leeg. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen één soort. Op je telefoon en computer zie je dezelfde selectie. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, bijvoorbeeld een onderdeel dat steeds opnieuw opstart, is niet Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook meteen naar de andere selectie: tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst toont de naam van je laatste ochtend- of avondoverzicht en wat daarin is meegeteld, bijvoorbeeld **Avondoverzicht van gisteren** · 12 afgerond, 3 open. Tik erop om dat overzicht opnieuw te lezen. Met **Kopiëren** kun je het overal plakken. Zodra je het opent of op de **×** tikt, staat het op al je apparaten totdat het volgende overzicht verschijnt.

Als er geen recent overzicht is, staat er **Vandaag tot nu toe**: wat er vandaag is afgerond en wat nog openstaat, voor Werk en Privé of alleen voor de selectie die je hebt gemaakt.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Bekijk [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten die hij mag lezen en versturen, verhuist mee. Met **Ongedaan maken** in de melding verplaats je hem terug.

Als een to-do naar je andere gebied moet om verder te kunnen en de berichten waarop hij is gebaseerd daar allemaal staan, wordt hij automatisch verplaatst en gaat hij verder. Anders staat er **Naar Werk verplaatsen** en wordt er niets verplaatst totdat je erop tikt. Een to-do die je zelf hebt toegevoegd zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd staat er geen Werk of Privé bij en blijft hij privé.

Een to-do kan altijd de berichten lezen waarop hij is gebaseerd. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gemarkeerd, telt als Privé. Mail voor een ander bedrijf van je komt bij de to-do's van dat bedrijf terecht. Een to-do over je privéleven, zoals familie die naar je werkadres mailt, is vanaf het begin Privé.

Werk dat je via een persoonlijk account bereikt, zoals een klant via WhatsApp of een bestelling in je persoonlijke mailbox, is vanaf het begin Werk. Een to-do die je zelf hebt verplaatst of ingedeeld, blijft altijd staan waar je hem hebt neergezet. Werk of Privé bepaalt waar een to-do verschijnt en met wie hij wordt gedeeld, nooit waar hij op antwoordt: een antwoord gaat altijd naar de plek van het gesprek, ook nadat de to-do is verplaatst, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail binnenkwam. Hij verschijnt nooit in een Work Fleet of de Team Graph.

Als er twee of meer to-do's wachten, doorloopt **Doorlopen** in de kop van Voor jou ze één voor één, in de volgorde van de lijst. Je ziet steeds het volledige concept, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Druk op een computer op Enter om te versturen wat op het scherm staat, op `S` om te snoozen, op `→` om over te slaan en op Esc om te stoppen. Onder de titel staat in de kop ook hoelang alles ongeveer duurt als je je eigen tempo aanhoudt, bijvoorbeeld "ongeveer 2 min".

Een to-do waarin je een vraag krijgt, wordt niet meegenomen: daarvoor is je antwoord nodig, niet een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert binnengekomen berichten zodra er 40 berichten wachten of het oudste bericht van iemand al 15 minuten wacht. Nieuwsbrieven, meldingen en betalingsbewijzen worden bij de volgende controle meegenomen, binnen een uur.

's Nachts, van 00:00 tot 06:30, staan de controles stil. Nieuwe berichten worden wel gelezen en bewaard, en om 06:30 tegelijk gecontroleerd, zodat je to-do's klaarstaan voordat je ochtendoverzicht verschijnt. Bij Controles onder Koppelingen staat: "Nachtpauze, haalt de achterstand om 06:30 in". Als je 's nachts in de app klikt, typt of scrolt, in de chat schrijft of op een to-do tikt, lopen de controles zoals gewoonlijk door totdat je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen alle bronnen. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, staat de regel bovenaan op een computer. Een korte regel wordt alleen getoond als er een controle loopt, of als die is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er een regel boven je to-do's met wat je Machine heeft gevonden in elke gelezen bron, bijvoorbeeld "13 berichten gecontroleerd om 16:11 · niets waarvoor je nodig bent" of "· 2 nieuwe to-do's". Als een nieuwe to-do wacht op een beter moment, zoals je ochtendoverzicht, staat erbij tot wanneer: "1 to-do uitgesteld tot morgen 08:30".

Tik op de regel om elke e-mailthread, chat en melding te bekijken, met het pictogram van de bron erbij: wie het bericht heeft geschreven, het onderwerp of de eerste woorden en de nieuwe to-do of de reden dat er niets nodig was, zoals "Alleen in cc, een teamgenoot antwoordt" of "Afspraak staat al voor donderdag". Bij een thread staat geen reden als de controle alleen een vage reden opleverde. Tik erop om het bericht te lezen.

De eerste 10 worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou telt mee. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails die je Machine zelf aan je stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of vermeld. Mail over facturering, je proefperiode of een uitnodiging wordt wel gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Bekijk [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan of, zodra een concept klaarstaat, wat er in het concept moet veranderen. **Markeer als gedaan** betekent dat het is afgehandeld. Bij een klaargezette to-do zonder concept staat de knop in het zicht; anders staat hij bovenaan onder **…**, ook bij een to-do waarvoor je eerst een beslissing moet nemen. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in de melding. Veeg de melding weg of sleep hem met de muis weg om hem eerder te sluiten. De wijziging blijft behouden.

Wil je dat het op een andere manier wordt gedaan, zeg dat dan in de **Chat**.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om de to-do te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt op vaste momenten terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert hiervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt er ook in de chat om vragen, bijvoorbeeld "Hernoem dit naar …". Je titel blijft behouden.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van diegene, maar niet bij je eigen antwoord. Daarna staat erbij wanneer hij is teruggekomen en staat hij als nieuw bovenaan. De chat gaat verder waar je gebleven was, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen kaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender dat de betaling is ontvangen, wordt de to-do automatisch gesloten. Met **Ongedaan maken** kun je hem een dag lang terugzetten.

Een to-do die alleen tot een bepaald moment relevant is, zoals een bevestiging vóór een vergadering, wordt na dat moment automatisch gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding "Niet meer nodig". Met **Ongedaan maken** kun je hem een dag lang terugzetten.

Voordat een bericht of overdracht voor iemand als klaar wordt getoond, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat het al is geregeld, bijvoorbeeld doordat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do automatisch gesloten. Met **Ongedaan maken** kun je hem een dag lang terugzetten.

Als een nieuwer bericht het plan verandert, bijvoorbeeld doordat een feest naar een andere locatie is verplaatst of een boeking is geannuleerd, werkt The Machine zijn to-do's zelf bij. Een to-do die nog relevant is, volgt het nieuwe plan. Als er niets meer te doen is, wordt hij verplaatst naar **Gedaan / afgewezen** met de melding "Niet nodig". In de chat staat "Bijgewerkt:" met de reden. Met **Ongedaan maken** kun je hem een dag lang terugzetten.

Bij je eerste to-do's verschijnt een korte tip over de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**, en dat er niets wordt verstuurd voordat je op **Versturen** drukt. Een tip verdwijnt definitief zodra je de knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en vertelt hij wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat wanneer je aankomt.

Elke to-do begint met de titel. De regel eronder vermeldt op wie de to-do betrekking heeft, de organisatie als het daarover gaat (niet alleen omdat iemand er werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie wordt een foto of logo getoond als de Graph die heeft, anders de initialen. Als een logo op dat formaat niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, worden ook de initialen getoond.

Soms staat er een rustige melding met wat niet bekend is, zoals "Laatste contact 12 dagen geleden via e-mail; sindsdien niets." Die verschijnt als het laatste contact met iemand lang geleden was of nog onbeantwoord is, en noemt kanalen die niet zijn gekoppeld, zoals WhatsApp. Je Machine vertelt wat hij niet weet in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

Een titel vermeldt wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do behoudt zijn titel, met daaronder hoe hij is afgelopen, zoals "Gedaan: Sam heeft het dinsdag ondertekend".

Boven het concept staat een vage regel met de naam van het bericht waarop het is gebaseerd, met het logo van de dienst erbij. Tik erop om de thread te lezen. Bij het concept staat het logo van de bestemming, zodat je meteen ziet of het om een antwoord in Slack of een e-mail gaat.

Als het concept voortbouwt op informatie van iemand anders, bijvoorbeeld een suggestie van een teamgenoot in Slack, staat dat erbij, zoals "Gebaseerd op Sam in #ops". Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt als één gesprek weergegeven, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je eigen berichten rechts, net als in de app. Het bericht waarop de to-do betrekking heeft, is gemarkeerd met "Deze to-do" en wordt geopend in beeld. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mail staat de rest van de thread ingeklapt erboven en eronder.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij binnenkwam. Op Android wordt de Gmail-app geopend als je die hebt.

Onder **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets aan toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Met de link in een to-do open je het bijbehorende bericht hier ook, met **Openen in Slack** onderaan.

Onder **Details** staan de naam, het project en het gebied (tik erop om iets te wijzigen), je laatste notitie en het resultaat van een coding agent. De titel opent de chat. Een afgeronde to-do blijft kort; het bericht waarop hij is gebaseerd, staat onder **Details**.

Een to-do met de status "Wacht op" linkt naar je laatste bericht aan diegene, het bericht waarop je wacht: "E-mail aan Pat · di".

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Als je er een maakt, wordt er niets verstuurd. Als je geen **Werk** of **Privé** kiest, komt de to-do terecht waar hij thuishoort, op basis van voor wie en waarover hij gaat. Je Machine zoekt ook de e-mail op waarop de to-do een vervolg is, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals "morgen", "volgende vr", "3 nov", "14.00 uur" of "over 2 uur". Dat kan ook in je eigen taal. Met het kalendericoon open je snelkeuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt op vaste momenten terug. Bekijk [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waarop de to-do betrekking heeft, maximaal 5.
- Berichtenicoon: voeg het bericht toe waarop de to-do betrekking heeft: een e-mail, Slack-, Teams-, WhatsApp-, Telegram- of ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon maakt de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × haal je een bestand weer weg.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij eraan werkt. Alleen bestanden zijn genoeg: hij maakt de to-do op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding getoond. Tik erop om hem op volledige grootte te zien.
