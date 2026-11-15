---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak die je aandacht nodig heeft, klaar voor jouw akkoord. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 81b65d513aa5941b
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als er iets is waarvoor je nodig bent. Eén to-do per zaak, hoeveel berichten die ook beslaat.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan zie je de laatste stap die je hebt bevestigd, zoals een formulier of issue dat is afgehandeld terwijl je weg was. Hij blijft daar staan totdat je op **Begrepen** tikt, maximaal één dag. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles waarvoor jij aan zet bent, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (het werk is gedaan en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of samenvatting waarover je niets hoeft te beslissen).
- **Wacht op anderen**: ingeklapte to-do's waarbij iemand anders aan zet is (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop je niet hebt gereageerd bij **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij anderen hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: elke afgeronde to-do, nieuwste eerst, met het tijdstip waarop hij is afgerond, bijvoorbeeld ‘Gedaan 5 minuten geleden’. To-do's die al afgerond lijken, hebben het label **Lijkt gedaan**.

Nadat je iets hebt verstuurd, staat er kort waar de to-do naartoe is verplaatst, bijvoorbeeld ‘Verstuurd. Verplaatst naar Gedaan.’ of ‘Verstuurd. Verplaatst naar Later, tot ma.’ Met **Openen** ga je naar de to-do. Met Zoeken vind je een to-do op basis van de titel of de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst de to-do's waarvan de deadline is verstreken of morgen valt, daarna vragen van je Fleet, vervolgens vervolgacties van een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en als hij klaar is: alleen het label verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of morgen valt bovenaan, gevolgd door de rest, nieuwste eerst. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, zoals ‘PR #3451 samengevoegd’, maar de to-do nog niet is gesloten. Met **Heropenen** zet je hem terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat weergegeven. Na een dag wordt de to-do automatisch gesloten, met **Ongedaan maken** als optie. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook automatisch gesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: ‘Dit is Sam Lee niet.’ De afzender wordt weergegeven met het eigen adres, nooit met de naam die diegene heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, staat **Wacht op:** met de volgende stap. De to-do staat ingeklapt onder **Wacht op anderen**, boven Komt later terug, totdat een nieuw bericht hem weer naar voren haalt. Hetzelfde geldt nadat je zelf een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline als die later vandaag valt, of de volgende ochtend als de deadline al verstreken is. Er staat bij op wie de to-do nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet leveren, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Als je jouw deel verstuurt, wordt de to-do niet gesloten: hij blijft onder **Wacht op anderen** staan totdat een bericht het resultaat laat zien. Daarna wordt hij automatisch gesloten, met **Ongedaan maken** als optie. Als er tegen de tijd dat je diegene moet herinneren nog niets is binnengekomen, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Als niemand een week iets met een to-do heeft gedaan, vraagt hij één keer: **Nog nodig?** Met **Niet nodig** sluit je hem, met **Ongedaan maken** als optie. Met **Houden** bewaar je hem en wordt het niet nog een keer gevraagd. Als je nog een week niet reageert, wordt de to-do ingeklapt onder Komt later terug. Het aantal op het appicoon en in het ochtendoverzicht telt hem dan niet meer mee. Als je hem opent, een chatbericht stuurt, iets bewerkt of snoozet, of als er een nieuw bericht binnenkomt, komt hij weer terug.

Eén keer per week kan een project waar niets meer gebeurt en geen openstaande to-do's heeft, een to-do krijgen met één concrete volgende stap. Dit gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als er niets is waarvoor je nodig bent, doet je Machine een dutje bij een lege lijst. Tijdens het controleren wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk geef je aan of je alle to-do's wilt zien of alleen één soort. Op je telefoon en computer zie je dezelfde keuze. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook direct over naar de andere weergave: onder **Alleen privé** tik je op **Werk** of **Alles tonen**.

De rij bovenaan de lijst toont de naam van je laatste ochtend- of avondoverzicht en wat erin is meegeteld, bijvoorbeeld **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen, met **Kopiëren** om het ergens te plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, staat er **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt gekozen.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Zie [De to-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten die hij mag lezen en versturen, verhuist mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te kunnen en alle berichten waar hij vandaan komt daar staan, wordt hij automatisch verplaatst en gaat hij verder. Anders staat er **Naar Werk verplaatsen** en gebeurt er niets totdat je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd staat er noch Werk, noch Privé bij en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij toestemming met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt aangemerkt, telt als Privé. Mail voor een ander bedrijf van je komt terecht bij de to-do's van dat bedrijf. Een to-do over je privéleven, zoals familie die naar je werkadres schrijft, is vanaf het begin Privé.

Werk dat via een persoonlijk account bij je binnenkomt, zoals een klant op WhatsApp of een bestelling in je persoonlijke mailbox, is vanaf het begin Werk. Een to-do die je zelf hebt verplaatst of ingedeeld, blijft altijd staan waar je hem hebt neergezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, nooit waar hij op antwoordt: een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij verschijnt nooit in een Werk-Fleet of de Team Graph.

Als er twee of meer to-do's op je wachten, doorloop je ze met **Doorlopen** in de kop van Voor jou, één voor één in de volgorde van de lijst. Je ziet elk concept in zijn geheel, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuur je met Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stop je met Esc. Onder de titel staat in de kop ook hoelang je er op je eigen tempo over doet, bijvoorbeeld ‘ongeveer 2 min’.

Een to-do die je iets vraagt, wordt niet meegenomen: die wacht op je antwoord, niet op een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert wat er is binnengekomen zodra er 40 berichten wachten of het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en bonnetjes neemt hij mee bij de volgende controle, binnen een uur.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd: nieuwe berichten worden nog wel gelezen en bewaard, en om 06:30 samen gecontroleerd. Zo staan je to-do's klaar voordat je ochtendoverzicht verschijnt. Bij Controles onder Koppelingen staat ‘'s Nachts gepauzeerd, wordt om 06:30 ingehaald’. Open je de app, schrijf je in de chat of tik je 's nachts op een to-do, dan worden de controles weer normaal uitgevoerd totdat je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen elke bron. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details** om Controles onder Koppelingen te openen. Als er to-do's openstaan, staat de regel bovenaan op een computer. Daar verschijnt alleen een korte melding terwijl er een controle loopt, mislukt is of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare hebben hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's wat hij heeft gevonden, uit elke gelezen bron. Bijvoorbeeld: ‘13 berichten gecontroleerd om 16:11 · niets waarvoor je nodig bent’ of ‘· 2 nieuwe to-do's’. Als een nieuwe to-do wordt bewaard tot een beter moment, bijvoorbeeld je ochtendoverzicht, staat erbij tot wanneer: ‘1 to-do bewaard tot morgen 08:30’.

Tik op de regel om elk e-mailgesprek, elke chat en melding te bekijken, met het pictogram van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden, en de nieuwe to-do of waarom er niets nodig was, bijvoorbeeld ‘Alleen in cc, een teamgenoot antwoordt’ of ‘Afspraak staat al voor donderdag’. Als de controle alleen een vage reden gaf, staat er bij een gesprek geen reden. Tik erop om het te lezen.

De eerste 10 worden weergegeven. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten er in die chat zijn. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer weergegeven. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails van The Machine zelf aan jou, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan, of, zodra er een concept klaarstaat, wat daarin moet worden aangepast. Met **Markeer als gedaan** geef je aan dat het is afgehandeld: bij een klaargezette to-do zonder concept staat de knop direct in beeld, anders staat hij bovenaan onder **…**, ook bij een to-do waarvoor je een beslissing moet nemen. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in de melding. Veeg het bericht weg of sleep het met de muis uit beeld om het sneller te sluiten. De wijziging blijft behouden.

Wil je het op een andere manier laten doen, zeg dat dan in de **Chat**.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om hem te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt regelmatig terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel aangeven waarom: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je titel blijft staan.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van diegene, maar niet bij je eigen antwoord.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen kaart, worden dat niet. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld doordat de afzender bevestigt dat je betaling is ontvangen, wordt de to-do automatisch gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Een to-do die maar tot een bepaald tijdstip relevant is, zoals een bevestiging vóór een vergadering, wordt na dat tijdstip automatisch gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet meer nodig’. Met **Ongedaan maken** zet je hem een dag lang terug.

Voordat een bericht of overdracht voor iemand als klaargezet wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat het al is afgehandeld, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do automatisch gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Als een nieuwer bericht het plan verandert, bijvoorbeeld als een feestje naar een andere locatie is verplaatst of een boeking is geannuleerd, werkt The Machine de to-do's zelf bij. Een to-do die nog nodig is, volgt het nieuwe plan. Een to-do waarvoor niets meer hoeft te gebeuren, wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet nodig’. In de chat staat ‘Bijgewerkt:’ met de reden. Met **Ongedaan maken** zet je de to-do een dag lang terug.

Bij je eerste to-do's zie je een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**, en de uitleg dat er niets wordt verstuurd voordat je op **Versturen** drukt. De tip verdwijnt voorgoed zodra je de bijbehorende knop gebruikt of op × drukt.

Op je eerste dag heet de kop van To-do's je welkom en staat erbij wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat wanneer je aankomt.

Elke to-do begint met de titel. De regel eronder vermeldt over wie de to-do gaat, de organisatie als die relevant is (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in Graph te openen.

Bij een naam en organisatie staat een foto of logo als Graph die heeft, anders de initialen. Als een logo op klein formaat niet goed leesbaar is, bijvoorbeeld witte letters op een transparante achtergrond of een breed woordmerk, wordt ook de initiaal weergegeven.

Soms staat er een korte melding met wat niet bekend is, zoals ‘Laatste contact 12 dagen geleden via e-mail; sindsdien niets’. Die verschijnt als het laatste contact met diegene lang geleden is of nog geen antwoord heeft gekregen, en vermeldt kanalen die niet zijn gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Verbinden** ernaast die koppeling.

Een titel zegt wat er moet gebeuren en verandert alleen als dat verandert. De titel van een afgeronde to-do blijft staan, met daaronder hoe hij is afgerond, bijvoorbeeld ‘Gedaan: Sam heeft het dinsdag ondertekend’.

Boven het concept staat een vage regel met het bericht waar het vandaan komt, met het logo van de dienst. Tik erop om het gesprek te lezen. Bij het concept staat het logo van de bestemming, zodat je meteen ziet of het een Slack-antwoord of e-mail is.

Als het concept is gebaseerd op wat iemand ergens anders heeft gezegd, bijvoorbeeld een suggestie van een teamgenoot in Slack, staat dat op een regel, zoals ‘Gebaseerd op Sam in #ops’. Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Bij het bericht waar de to-do over gaat, staat ‘Deze to-do’. Het bericht wordt geopend en weergegeven. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Een e-mail toont de rest van het gesprek ingeklapt erboven en eronder.

Onder **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Met de link van een to-do naar het eigen bericht open je dat bericht hier ook, met onderaan **Openen in Slack**.

Onder **Details** staan de naam, het project en het gebied (tik erop om ze te wijzigen), je laatste notitie en het resultaat van een codeerassistent. De titel opent de chat. Een afgeronde to-do blijft kort; het bericht waar hij vandaan komt, staat onder **Details**.

Een to-do met ‘Wacht op’ linkt naar je laatste bericht aan diegene, het bericht waar je op wacht: ‘E-mail aan Pat · di’.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) maak je een to-do voor wat dan ook. Als je er een aanmaakt, wordt er niets verstuurd. Als je **Werk** of **Privé** niet selecteert, komt de to-do terecht waar hij hoort, op basis van over wie en wat hij gaat. Hij zoekt ook de e-mail op waar hij een vervolg aan geeft, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, bijvoorbeeld ‘morgen’, ‘volgende vr’, ‘3 nov’, ‘14:00’ of ‘over 2 uur’. Dat kan ook in je eigen taal. Met het kalendericoon vind je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt regelmatig terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel maximaal 5 personen of bedrijven aan de to-do.
- Berichtenicoon: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp- of Telegram-bericht, of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon maakt het camera-icoon ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze als hij ermee aan de slag gaat. Alleen bestanden toevoegen is genoeg: hij vult de to-do in op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te bekijken.
