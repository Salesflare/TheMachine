---
title: To-do's
area: cards
summary: Eén to-do per onderwerp waarvoor je iets moet doen, klaar om door jou goedgekeurd te worden. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 88ccf5426e5a538f
---
Je Machine leest alles wat nieuw is en maakt alleen een to-do als je iets moet doen. Eén to-do per onderwerp, hoeveel berichten er ook over gaan.

## Waar je to-do's staan

Op de pagina **To-do's** staan ze in groepen:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een probleem dat is afgehandeld terwijl je weg was. De to-do blijft hier staan tot je op **Begrepen** tikt, maximaal één dag. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar, en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven; als het werk stilstaat omdat alleen jij iets hebt, zoals een feit, login of keuze, staat er onder de titel wat dat is), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of korte briefing, niets om over te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws mee is gebeurd (hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij de volgende stap bij iemand anders ligt (hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop je niet hebt geantwoord bij **Nog nodig?** (hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, nieuwste eerst, met het tijdstip waarop ze zijn afgerond, zoals ‘Gedaan 5 minuten geleden’. To-do's die al afgerond lijken, hebben het label **Lijkt gedaan**.

Nadat je iets hebt verstuurd, staat er kort waar de to-do naartoe is verplaatst, zoals ‘Verstuurd. Verplaatst naar Gedaan.’ of ‘Verstuurd. Verplaatst naar Later tot ma.’ Een antwoord waarin je alleen belooft het werk te doen, zoals ‘Ik stuur het dinsdag’, laat de to-do openstaan: ‘Verstuurd. Open gehouden.’ Met **Openen** ga je naar de to-do. Zoeken vindt to-do's op titel of op de persoon naar wie je ze hebt gestuurd, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's waarvan de deadline is verstreken of morgen valt, daarna vragen van je Fleet, vervolgens vervolgacties op een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en wanneer hij is afgerond. Alleen het label verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of morgen valt bovenaan, en daarna de nieuwste. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets klaar is, zoals ‘PR #3451 samengevoegd’, maar dat het nog niet is afgesloten. Met **Heropenen** zet je het terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat weergegeven. Als een bericht dit laat zien, wordt de to-do na één dag vanzelf afgesloten, met **Ongedaan maken**. Anders wacht hij op **Als gedaan markeren**. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf afgesloten.

Als een bericht afkomstig lijkt van iemand die je kent, maar van een ander adres komt, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: ‘Dit is Sam Lee niet.’ De afzender wordt weergegeven met diens eigen adres, nooit met de naam die hij of zij heeft opgegeven. Je Machine controleert zo'n bericht bij de persoon van wie je het adres al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, zoals een beoordeling of antwoord, staat **Wacht op:** met de volgende stap. De to-do staat ingeklapt in **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem terugbrengt. Dat geldt ook nadat je een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline als die later vandaag valt, of de volgende ochtend als de deadline al voorbij is. Je ziet dan ook op wie hij nog wacht.

Bij een to-do voor een resultaat dat iemand anders moet aanleveren, zoals een ondertekend contract, staat onder **Details** bij **Klaar als** wat het resultaat is. Als je jouw deel verstuurt, wordt de to-do niet afgesloten. Hij blijft in **Wacht op anderen** tot een bericht laat zien dat het resultaat er is. Daarna wordt hij vanzelf afgesloten, met **Ongedaan maken**. Als er niets binnenkomt tegen de tijd dat je die persoon moet herinneren, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Een to-do waar een week niets nieuws mee is gebeurd, wordt verplaatst van Voor jou naar **Ouder**, zodat nieuwe to-do's bovenaan staan als je een paar dagen weg bent geweest. Niets nieuws betekent dat er geen nieuw bericht over is en dat jij er niets mee hebt gedaan, zoals een chatbericht sturen, iets aanpassen of snoozen. Alleen de to-do bekijken telt niet mee.

Dringende to-do's, to-do's waarvan de deadline snel nadert en to-do's die bijna worden verstuurd, blijven in Voor jou staan. Met **Alles afwijzen** markeer je na één bevestiging alle to-do's in Ouder als niet nodig. Dat doet **Niet nodig** ook één voor één, met **Ongedaan maken**. Als er iets nieuws gebeurt met een to-do, komt hij terug in Voor jou.

Bij een to-do die een week lang niemand heeft aangeraakt, wordt één keer gevraagd: **Nog nodig?** Met **Niet nodig** sluit je de to-do af, met **Ongedaan maken**. Met **Houden** houd je de to-do. De vraag wordt dan niet opnieuw gesteld. Als je nog een week niet antwoordt, wordt de to-do ingeklapt onder Komt later terug. Hij telt dan niet meer mee op het appicoon of in het ochtendoverzicht. Als je de to-do opent, een chatbericht stuurt, iets aanpast, snoozet of een nieuw bericht binnenkomt, komt hij terug.

Eén keer per week kan een project waar niets meer gebeurt en waarvoor geen open to-do's zijn, een to-do krijgen met één specifieke volgende stap. Dit gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als je niets hoeft te doen, wacht je Machine op een lege lijst. Tijdens een controle wordt hij weer actief en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk geef je aan of je alle to-do's of maar één soort wilt zien. Op je telefoon en computer geldt dezelfde keuze. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, is geen Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook meteen naar de andere weergave: tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst toont de naam van je laatste ochtend- of avondoverzicht en wat daarin is meegeteld, zoals **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen. Met **Kopiëren** kun je het ergens plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Zonder recent overzicht zie je **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt geselecteerd.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of verwijder je de koppeling. Zie [De to-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De berichten die hij mag lezen en van waaruit hij mag versturen, verhuizen mee. Met **Ongedaan maken** op de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waar hij vandaan komt daar staan, wordt hij vanzelf verplaatst en gaat hij verder. Anders zie je **Naar Werk verplaatsen** en gebeurt er niets tot je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd staat er geen Werk of Privé bij en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij je om die te gebruiken met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gelabeld, geldt als Privé. Mail voor een van je andere bedrijven hoort bij de to-do's van dat bedrijf. Een to-do over je eigen leven, zoals familie die naar je werkadres schrijft, is vanaf het begin Privé.

Werk dat binnenkomt op een persoonlijk account, zoals een klant via WhatsApp of een bestelling in je persoonlijke mailbox, geldt vanaf het begin als Werk. Een to-do die je zelf hebt verplaatst of ingedeeld, blijft altijd staan waar je hem hebt gezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, nooit waar hij op antwoordt. Een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij wordt nooit weergegeven in een Werk-Fleet of Team-Graph.

Als er twee of meer to-do's op je wachten, loop je ze met **Doorlopen** in de kop van Voor jou één voor één af, in de volgorde van de lijst. Je ziet elk concept volledig, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, met `S` snooze je, met `→` sla je over en met Esc stop je. In de kop staat hoelang het duurt als je je eigen tempo aanhoudt, zoals ‘ongeveer 2 min’.

Aan het einde staat hoeveel er zijn verstuurd of afgesloten en hoeveel er nog worden voorbereid.

Een to-do die je iets vraagt, wordt overgeslagen. Daarvoor is je antwoord nodig, niet een tik.

## Nu checken

Je Machine leest elke paar minuten elke bron, dag en nacht. Hij controleert wat er is binnengekomen zodra er 40 berichten klaarstaan of het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden meegenomen bij de volgende controle, binnen een uur.

's Nachts, van 00:00 tot 06:30, staan de controles stil. Nieuwe berichten worden nog wel gelezen en bewaard, en om 06:30 tegelijk gecontroleerd, zodat je to-do's klaarstaan vóór je ochtendoverzicht. Bij Controles onder Koppelingen staat ‘'s Nachts gepauzeerd, haalt de achterstand om 06:30 in’. Als je 's nachts in de app klikt, typt of scrolt, in de chat schrijft of op een to-do tikt, worden controles zoals gewoonlijk uitgevoerd tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine alle bronnen meteen. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, staat de regel op een computer bovenaan. Daar verschijnt een korte melding alleen als er een controle loopt, is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare hebben hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met wat er is gevonden in alle gecontroleerde bronnen, zoals ‘13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's’ of ‘· 2 nieuwe to-do's’. De regel gaat alleen over die controle. To-do's die al op je lijst stonden, blijven staan zoals ze zijn. Als een nieuwe to-do wordt uitgesteld tot een beter moment, zoals je ochtendoverzicht, staat erbij tot wanneer: ‘1 to-do uitgesteld tot morgen 08:30’.

Tik op de regel om alle e-mailthreads, chats en meldingen te zien, met het pictogram van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden en de nieuwe to-do, of waarom er niets nodig was, zoals ‘Alleen in cc, een teamgenoot antwoordt’ of ‘Meeting staat al voor donderdag gepland’. Bij een thread wordt geen reden getoond als de controle alleen een vaag antwoord gaf. Tik op een bericht om het te lezen.

De eerste 10 worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat bevat. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer weergegeven. De regel blijft 12 uur na de controle staan.

Alleen e-mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar gelden niet als nieuwe mail. E-mails die The Machine zelf naar je stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of vermeld. Mail over facturering, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe je Machine het moet doen, of, zodra een concept klaar is, wat er in het concept moet veranderen. **Als gedaan markeren** betekent dat het is afgehandeld. Deze optie staat direct in beeld bij een klaargezette to-do zonder concept. Anders staat hij bovenaan onder **…**, ook bij een to-do waarvoor je nog een beslissing moet nemen. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in de melding. Veeg het bericht weg of sleep het met de muis opzij om het sneller af te sluiten. De wijziging blijft staan.

Wil je dat het op een andere manier gebeurt? Geef dat aan in de **Chat** van de to-do. Het antwoord vermeldt alleen wat is veranderd, zoals een snooze en tot wanneer. Als iets niet kon worden gewijzigd, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om de to-do te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt regelmatig terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt het ook in de chat vragen, bijvoorbeeld ‘Hernoem dit naar …’. De titel die je opgeeft, blijft staan.

Met **Heropenen** zet je een afgesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van die persoon, maar niet na je eigen antwoord. Je ziet dan wanneer hij is teruggekomen en hij wordt gerangschikt als nieuw. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals een automatische incasso of een opgeslagen betaalkaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender dat je betaling is ontvangen, wordt de to-do vanzelf afgesloten. Met **Ongedaan maken** zet je hem binnen een dag terug.

Een to-do die maar tot een bepaald tijdstip relevant was, zoals een bevestiging vóór een meeting, wordt na dat tijdstip vanzelf afgesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet meer nodig’. Met **Ongedaan maken** zet je hem binnen een dag terug.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat het al is geregeld, bijvoorbeeld omdat iemand iets heeft gevraagd en een bevestigend antwoord kreeg, wordt de to-do vanzelf afgesloten. Met **Ongedaan maken** zet je hem binnen een dag terug.

Als iemand anders in hetzelfde gesprek heeft geschreven nadat je concept was gemaakt, houdt **Versturen** het tegen: ‘Niet verstuurd: nieuw bericht in de thread’. Bij de to-do staat dat bericht met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is vervallen, past The Machine zijn to-do's zelf aan. Een to-do die nog relevant is, volgt het nieuwe plan. Als er niets meer te doen is, wordt hij verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet nodig’. In de chat staat ‘Bijgewerkt:’ met de reden. Met **Ongedaan maken** zet je hem binnen een dag terug.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**, en de uitleg dat er niets wordt verstuurd tot je op **Versturen** drukt. De tip verdwijnt definitief zodra je de knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en staat erbij wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat als je aankomt.

Elke to-do begint met de titel. De regel eronder vermeldt over wie het gaat, de organisatie als het om een organisatie gaat (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer het bericht is binnengekomen. Tik op een naam om de pagina van die persoon in Graph te openen.

Bij een naam en organisatie wordt een foto of logo getoond als Graph die heeft. Anders worden de initialen getoond. Een logo dat op klein formaat niet goed leesbaar is, zoals witte tekst op een transparante achtergrond of een breed woordmerk, wordt ook vervangen door de beginletter.

Soms staat er een korte, gedempte regel met wat niet bekend is, zoals ‘Laatste contact 12 dagen geleden via e-mail; sindsdien niets’. Deze verschijnt als het laatste contact al lang geleden was of onbeantwoord bleef. Ook niet-gekoppelde kanalen, zoals WhatsApp, worden vermeld. Je Machine vertelt wat hij niet weet in plaats van iets te raden.

Als er een niet-gekoppeld kanaal wordt vermeld, opent **Koppelen** ernaast die koppeling.

De titel zegt wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe hij is afgerond, zoals ‘Gedaan: Sam heeft het dinsdag ondertekend’.

Boven het concept staat een vage regel met het bericht waar het vandaan komt en het logo van de dienst. Tik erop om de thread te lezen. Het concept toont het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het om een Slack-antwoord of een e-mail gaat.

Als het concept voortkomt uit wat iemand ergens anders heeft gezegd, zoals een suggestie van een teamgenoot in Slack, staat er een regel bij, zoals ‘Gebaseerd op Sam in #ops’. Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je eigen berichten rechts, net als in de app. Het bericht waarop de to-do is gebaseerd, heeft het label ‘Deze to-do’ en wordt in beeld geopend. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mail wordt de rest van de thread ingeklapt erboven en eronder weergegeven.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android wordt hij geopend in de Gmail-app als je die hebt.

Onder **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige cc-adressen, bcc of een ander antwoordadres. Als er niets aan toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Met de link van een to-do naar het bijbehorende bericht open je dat bericht hier ook, met **Openen in Slack** onderaan.

Onder **Details** staan de naam, het project en het gebied (tik erop om iets aan te passen), je laatste notitie en het resultaat van een programmeeragent. Met de titel open je de chat. Een afgeronde to-do blijft beknopt. Het bericht waar hij vandaan komt, staat onder **Details**.

Bij een to-do met de status ‘Wacht op’ staat een link naar je laatste bericht aan de persoon op wie je wacht: ‘E-mail aan Pat · di’.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Als je er een maakt, wordt er niets verstuurd. Als je geen **Werk** of **Privé** kiest, gaat de to-do naar de plek waar hij thuishoort, op basis van wie en wat het onderwerp is. Ook vindt hij de e-mail waarop hij een vervolg is, zelfs als die al ouder is.

- **Deadline**: typ een dag of tijd, zoals ‘morgen’, ‘volgende vr’, ‘3 nov’, ‘14:00’ of ‘over 2 uur’. Dat kan ook in je eigen taal. Met het kalenderpictogram zie je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt regelmatig terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waarop de to-do betrekking heeft, maximaal 5.
- Berichtenpictogram: voeg het bericht toe waarop de to-do betrekking heeft, zoals een e-mail, Slack-, Teams-, WhatsApp- of Telegram-bericht, of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon maak je met de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en je Machine leest ze als hij eraan werkt. Alleen bestanden toevoegen is genoeg: hij vult de to-do in op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op volledig formaat te bekijken.
