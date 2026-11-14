---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak waarvoor je iets moet doen, klaar om door jou goed te keuren. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als er iets van je nodig is. Eén to-do per zaak, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze in groepen:

- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (het werk is gedaan en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst iets beslissen of antwoorden) of **Aan het voorbereiden…** (je Machine is ermee bezig).
- **Net gedaan**: een laatste stap die je hebt bevestigd, zoals een formulier of een issue, is uitgevoerd terwijl je weg was. De melding blijft staan tot je op **Begrepen** tikt, maximaal één dag, en je telefoon krijgt er ook een melding van.
- **Komt later terug**: gesnoozede to-do's en to-do's waarop je geen antwoord gaf op **Nog nodig?** (hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, zoals ‘Gedaan 5 minuten geleden’. To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Na het versturen staat er kort waar de to-do naartoe is gegaan, zoals ‘Verstuurd. Verplaatst naar Gedaan.’ of ‘Verstuurd. Verplaatst naar Later tot ma.’ Met **Openen** ga je naar de to-do. Je kunt op titel zoeken, of op de naam van degene naar wie de to-do is gestuurd. Zoeken werkt ook in Later en Gedaan.

Bij **Voor jou** staan eerst de to-do's waarvan de deadline is verstreken of morgen valt, dan vragen van je Fleet en daarna de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en wanneer hij is afgerond. Alleen de markering verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of morgen valt bovenaan, en de rest op volgorde van nieuw naar oud. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, zoals ‘PR #3451 samengevoegd’, maar dat het nog niet is gesloten. Met **Heropenen** zet je het terug op je lijst. Je Machine leert ervan. Deze to-do's worden nooit als te laat weergegeven. Na één dag wordt de to-do vanzelf gesloten, met **Ongedaan maken** als optie. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf gesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: ‘Dit is Sam Lee niet.’ Je ziet de persoon met diens eigen e-mailadres, nooit met de naam die de afzender heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Een to-do die nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, laat zien op welke stap hij wacht met **Wacht op:**. De to-do staat ingeklapt in **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem weer activeert. Hetzelfde gebeurt nadat je een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline als die later vandaag valt, of de volgende ochtend als de deadline al voorbij is. Je ziet dan ook op wie de to-do nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, zie je bij **Details** wat er moet gebeuren onder **Klaar als**. Het versturen van jouw deel sluit de to-do niet af. Hij blijft in **Wacht op anderen** tot een bericht het resultaat bevestigt. Daarna wordt hij vanzelf gesloten, met **Ongedaan maken** als optie. Als er niets binnenkomt tegen de tijd dat je diegene moet herinneren, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Als niemand een week iets met een to-do heeft gedaan, vraagt hij één keer: **Nog nodig?** Met **Niet nodig** sluit je hem, met **Ongedaan maken** als optie. Met **Houden** bewaar je hem en vraagt hij het niet nog eens. Krijgt de to-do nog een week geen antwoord, dan wordt hij ingeklapt onder Komt later terug. Hij telt dan niet meer mee voor het nummer op het appicoon of het ochtendoverzicht. Door de to-do te openen, een bericht in de chat te sturen, iets aan te passen, te snoozen of een nieuw bericht te ontvangen, komt hij weer terug.

Eén keer per week kan een project waar al een tijd niets is gebeurd en waar geen openstaande to-do's bij horen, een to-do krijgen met één concrete volgende stap. Dat gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als er niets is waarvoor je iets moet doen, gaat je Machine slapen en zie je een lege lijst. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk geef je weer welke to-do's worden getoond: allemaal of alleen één soort. Op je telefoon en computer wordt dezelfde keuze gebruikt. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en staat alleen onder Alle.

De regel bovenaan de lijst schakelt ook direct over naar de andere weergave: **Alleen Privé · Werk · Alles tonen**.

De rij bovenaan de lijst vermeldt de naam van je laatste ochtend- of avondoverzicht en wat erin werd meegeteld, bijvoorbeeld **Avondoverzicht van gisteren** · 12 afgerond, 3 open. Tik erop om het overzicht opnieuw te lezen. Met **Kopiëren** kun je het ergens plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, zie je **Vandaag tot nu toe**: wat er vandaag is afgerond en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt geselecteerd.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** kun je het project wijzigen of verwijderen. Zie [To-do's van een project](projects.md#a-projects-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De berichten die de to-do mag lezen en waarop hij mag antwoorden, verhuizen mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waar hij bij hoort daar staan, verhuist hij vanzelf naar dat gebied en gaat hij verder. Anders zie je **Naar Werk verplaatsen** en wordt er niets verplaatst tot je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra duidelijk is waar hij hoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij bij hoort. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij je dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gemarkeerd, telt als Privé. Mail voor een van je andere bedrijven komt terecht bij de to-do's van dat bedrijf. Een to-do over je eigen leven, zoals familie die naar je werkadres mailt, valt vanaf het begin onder Privé.

Werk dat via een persoonlijk account bij je binnenkomt, zoals een klant op WhatsApp of een bestelling in je persoonlijke mailbox, valt vanaf het begin onder Werk. Een to-do die je zelf hebt verplaatst of aangemaakt, blijft altijd staan waar jij hem hebt neergezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, nooit waar hij op antwoordt. Een antwoord gaat altijd naar de plek waar het gesprek plaatsvindt, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n to-do onder Privé antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij verschijnt nooit in een Fleet van Werk of in de Team Graph.

Als er twee of meer to-do's op je wachten, laat **Doorlopen** in de kop van Voor jou ze één voor één zien, in de volgorde van de lijst. Je ziet elk concept volledig, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stopt Esc. Onder de titel vermeldt de kop ook hoelang het ongeveer duurt als je je eigen tempo aanhoudt, bijvoorbeeld ‘ongeveer 2 min’.

Een to-do die je iets vraagt, wordt in beide gevallen overgeslagen: die wacht op je antwoord, niet op een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert nieuwe berichten zodra er 40 berichten klaarstaan, of zodra het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden bij de volgende controle meegenomen, uiterlijk binnen een uur.

's Nachts, van 00:00 tot 06:30, staan de controles stil. Nieuwe berichten worden wel gelezen en bewaard, en om 06:30 tegelijk gecontroleerd. Zo staan je to-do's klaar voordat je ochtendoverzicht verschijnt. Bij Controles onder Koppelingen staat: ‘Gepauzeerd voor de nacht. Haalt om 06:30 in.’ Open je 's nachts de app, schrijf je iets in de chat of tik je op een to-do, dan worden de controles weer normaal uitgevoerd tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen alle bronnen. Als er niets openstaat, tik je op de regel van je Machine om die te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, vind je de regel bovenaan op een computer. Een korte melding wordt daar alleen weergegeven als er een controle bezig is, of als er een is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met wat er is gevonden in alle gelezen bronnen, bijvoorbeeld ‘13 berichten gecontroleerd om 16:11 · niets nodig van jou’ of ‘· 2 nieuwe to-do's’. Als een nieuwe to-do op een beter moment wacht, bijvoorbeeld tot je ochtendoverzicht, staat erbij tot wanneer: ‘1 to-do uitgesteld tot morgen 08:30’.

Tik op de regel om elke e-mailthread, chat en melding te bekijken, met het pictogram van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden, en de nieuwe to-do of waarom er niets nodig was. Bijvoorbeeld: ‘Alleen in cc, een teamgenoot antwoordt’ of ‘Vergadering staat al gepland voor donderdag’. Bij een thread staat geen reden als de controle alleen een vage reden opleverde. Tik op een bericht om het te lezen.

De eerste 10 worden weergegeven. Tik onderaan om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat bevat. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer weergegeven. De regel blijft 12 uur na de controle zichtbaar.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar gelden niet als nieuwe mail. E-mails die The Machine zelf naar je stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt wel gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan, of, zodra er een concept klaarstaat, wat daarin moet worden aangepast. **Markeer als gedaan** betekent dat de to-do is afgehandeld. Bij een klaargezette to-do zonder concept staat deze knop direct in beeld. Anders staat hij bovenaan onder **…**, ook bij een to-do waarvoor je iets moet beslissen. De to-do verdwijnt meteen van de lijst. In de melding staat **Ongedaan maken**. Veeg de melding weg of sleep hem met de muis weg om hem sneller te sluiten. De wijziging blijft bewaard.

Wil je dat het op een andere manier wordt gedaan, zeg dat dan in de **Chat**.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om de to-do te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt aangeven waarom: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je titel blijft behouden.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de ander, maar niet bij je eigen antwoord.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen kaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld doordat de afzender bevestigt dat je betaling is ontvangen, wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem binnen een dag terug.

Een to-do die maar tot een bepaald tijdstip relevant is, zoals een bevestiging die je vóór een vergadering nodig hebt, wordt na dat tijdstip vanzelf gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet meer nodig’. Met **Ongedaan maken** zet je hem binnen een dag terug.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de mensen die erbij betrokken zijn, ook groepschats, en wacht hij tot Slack die heeft ingelezen. Als een later bericht laat zien dat het al is geregeld, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem binnen een dag terug.

Als een nieuwer bericht de plannen verandert, bijvoorbeeld omdat een feest naar een andere locatie verhuist of een boeking wordt geannuleerd, werkt The Machine de to-do's zelf bij. Een to-do die nog relevant is, volgt het nieuwe plan. Als er niets meer te doen is, wordt de to-do verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet nodig’. In de chat staat ‘Bijgewerkt:’ met de reden. Met **Ongedaan maken** zet je de to-do binnen een dag terug.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd voordat je op **Versturen** tikt. Een tip verdwijnt definitief zodra je de bijbehorende knop gebruikt of op × tikt.

Op je eerste dag heet de bovenkant van To-do's je welkom en staat er wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat wanneer je aankomt.

Elke to-do begint met de titel. De regel eronder vermeldt over wie de to-do gaat, de organisatie als die relevant is (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie staat een foto of logo als de Graph die heeft. Anders zie je de initialen. Als een logo op klein formaat niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, wordt ook de initiaal weergegeven.

Soms staat er een rustige melding met informatie die ontbreekt, zoals ‘Laatste contact 12 dagen geleden via e-mail; sindsdien niets’. Die verschijnt als het laatste contact met iemand lang geleden is of onbeantwoord bleef. Ook worden kanalen genoemd die niet zijn gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, open je die koppeling met **Koppelen** ernaast.

Een titel geeft aan wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do behoudt zijn titel. Eronder staat hoe hij is afgerond, zoals ‘Gedaan: Sam heeft het dinsdag ondertekend’.

Boven het concept staat in een lichte regel van welk bericht het afkomstig is, met het logo van de bijbehorende dienst. Tik erop om de thread te lezen. Het concept toont het logo van de bestemming, zodat je meteen ziet of het om een antwoord in Slack of een e-mail gaat.

Als het concept voortbouwt op input van iemand anders, bijvoorbeeld een suggestie van een teamgenoot in Slack, staat dat in een regel, zoals ‘Gebaseerd op Sam in #ops’. Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Bij het bericht van de to-do staat ‘Deze to-do’ en het bericht wordt geopend. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mailthread staan de overige berichten ingeklapt erboven en eronder.

Bij **Details** van een e-mail zie je alleen wat niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets toe te voegen is, wordt dit niet weergegeven.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. De link van een to-do naar het eigen bericht opent dat bericht hier ook, met **Openen in Slack** onderaan.

Bij **Details** zie je de naam, het project en het gebied (tik erop om het te wijzigen), je laatste notitie en het resultaat van een programmeeragent. Met **Chat ›** open je de chat. Een afgeronde to-do blijft kort. Het bericht waar hij vandaan komt, staat onder **Details**.

Een to-do met ‘Wacht op’ linkt naar je laatste bericht aan die persoon, het bericht waarop je wacht: ‘E-mail aan Pat · di’.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer) maak je een to-do voor alles. Als je een to-do maakt, wordt er niets verstuurd. Als je Werk of Privé niet kiest, komt hij terecht waar hij hoort, op basis van wie en wat erbij hoort. Je Machine zoekt ook de e-mail op waarop de to-do een vervolg is, zelfs als die al ouder is.

- **Deadline**: typ een dag of tijd, zoals ‘morgen’, ‘volgende vr’, ‘3 nov’, ‘14:00’ of ‘over 2 uur’. Dat kan ook in je eigen taal. Met het kalendericoon zie je snelle keuzes en **Kies een datum**.
- **Bericht**: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack, Teams, WhatsApp, Telegram of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat zie je waar het vandaan komt, wie het heeft gestuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij eraan werkt. Je kunt ook alleen bestanden toevoegen: The Machine maakt de to-do dan op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te bekijken.
