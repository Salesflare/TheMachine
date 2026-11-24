---
title: To-do's
area: cards
summary: Eén to-do voor elk ding dat je aandacht vraagt, klaar om door jou goedgekeurd te worden. Lees wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 4209ed807e753101
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als iets je aandacht vraagt. Eén to-do per kwestie, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, bijvoorbeeld een formulier of een probleem dat is afgehandeld terwijl je weg was. Dit blijft maximaal een dag staan, totdat je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, van meest naar minst urgent. Bij elke to-do staat **Klaargezet** (er staat een concept of resultaat klaar, en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoorden; als het werk is gestopt omdat alleen jij iets hebt, zoals een feit, login of keuze, staat er onder de titel wat dat is), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of briefing, zonder dat je iets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws mee is gebeurd (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop je niet hebt gereageerd bij **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Bekijk [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, zoals ‘Gedaan 5 minuten geleden’. To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Nadat je iets hebt verstuurd, staat er kort waar de to-do naartoe is verplaatst, bijvoorbeeld ‘Verstuurd. Verplaatst naar Gedaan.’ of ‘Verstuurd. Verplaatst naar Later tot ma.’ Als een antwoord alleen belooft het werk te doen, zoals ‘Ik stuur het dinsdag’, blijft de to-do openstaan: ‘Verstuurd. Opengehouden.’ Met **Openen** ga je naar de to-do. Met Zoeken vind je een to-do op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's waarvan de deadline is verstreken of morgen valt, daarna vragen uit je Fleet, dan vervolgacties van een bord en vervolgens de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine eraan werkt en wanneer hij klaar is. Alleen de markering verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of morgen valt bovenaan, gevolgd door de rest, met de nieuwste eerst. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, zoals ‘PR #3451 is samengevoegd’, maar dat het nog niet is gesloten. Met **Heropenen** zet je het terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat weergegeven. Als er een bericht bij staat, wordt de to-do na een dag vanzelf gesloten, met **Ongedaan maken**. Anders wacht hij totdat je **Als gedaan markeren** kiest. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf gesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: ‘Dit is niet Sam Lee.’ De afzender wordt weergegeven met zijn eigen adres, nooit met de naam die hij heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, staat **Wacht op:** met de stap waarop hij wacht. De to-do staat ingeklapt bij **Wacht op anderen**, boven Komt later terug, totdat een nieuw bericht hem weer naar voren haalt. Hetzelfde geldt nadat jij een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline zelf als die later vandaag valt, of de volgende ochtend als de deadline al voorbij is. Er staat bij op wie hij nog wacht.

Gaat een to-do over een resultaat dat iemand anders moet leveren, zoals een ondertekend contract, dan staat dat bij **Details** onder **Klaar als**. Als je jouw deel verstuurt, wordt de to-do niet gesloten. Hij blijft bij **Wacht op anderen** staan totdat een bericht laat zien dat het resultaat er is. Daarna wordt hij vanzelf gesloten, met **Ongedaan maken**. Als er niets binnenkomt op het moment dat je de ander eraan moet herinneren, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit te wijzigen.

Een to-do waar een week niets nieuws mee is gebeurd, wordt verplaatst van Voor jou naar **Ouder**, zodat nieuwe to-do's bovenaan staan als je na een paar dagen terugkomt. Niets nieuws betekent dat er geen nieuw bericht over is en dat jij er niets mee hebt gedaan, zoals een chatbericht sturen, iets bewerken of snoozen. Alleen bekijken telt niet.

Urgente to-do's, to-do's met een naderende deadline en to-do's waarvan iets wordt verstuurd, blijven bij Voor jou staan. Met **Alles afwijzen** markeer je na één bevestiging alle to-do's in Ouder als niet nodig. Dat doet hetzelfde als **Niet nodig**, maar dan één voor één. Je kunt dit ongedaan maken met **Ongedaan maken**. Als er iets nieuws gebeurt met een to-do, komt hij terug bij Voor jou.

Als niemand een to-do een week heeft aangeraakt, vraagt hij één keer: **Nog nodig?** Met **Niet nodig** sluit je hem, met **Ongedaan maken** als optie. Met **Houden** houd je hem en wordt het nooit meer gevraagd. Als je nog een week niet reageert, wordt de to-do ingeklapt onder Komt later terug en telt hij niet meer mee op het appicoon of in het ochtendoverzicht. Als je hem opent, een chatbericht stuurt, iets bewerkt, hem snoozet of er een nieuw bericht binnenkomt, komt hij terug.

Eén keer per week kan een project dat stil is gevallen en geen openstaande to-do's heeft, een to-do krijgen met één concrete volgende stap. Dat gebeurt maximaal drie keer per week. Bekijk [Projecten](projects.md).

Als niets je aandacht vraagt, wacht je Machine op een lege lijst. Tijdens een controle wordt hij weer actief en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat op de regel, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen één soort. Op je telefoon en computer wordt dezelfde keuze weergegeven. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar alle to-do's. Een melding over je Machine zelf, bijvoorbeeld een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en staat alleen bij Alle.

Met de regel bovenaan de lijst schakel je ook meteen naar de andere weergave: tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst toont de naam van je laatste ochtend- of avondoverzicht en hoeveel items erin stonden, bijvoorbeeld **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om het overzicht opnieuw te lezen. Met **Kopiëren** kun je het ergens plakken. Zodra je het opent of op × tikt, staat het op al je apparaten totdat het volgende overzicht verschijnt.

Zonder recent overzicht zie je **Vandaag tot nu toe**: wat er vandaag is afgerond en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt gekozen.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of verwijder je het. Bekijk [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De bronnen die hij mag lezen en waaruit hij mag versturen, gaan mee. Met **Ongedaan maken** in de melding verplaats je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waar hij vandaan komt daar staan, wordt hij vanzelf verplaatst en gaat hij verder. Anders zie je **Naar Werk verplaatsen** en gebeurt er niets totdat je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gemarkeerd, telt als Privé. Mail voor een ander bedrijf van je gaat naar de to-do's van dat bedrijf. Een to-do over je privéleven, zoals familie die naar je werkadres schrijft, is vanaf het begin Privé.

Werk dat binnenkomt op een privéaccount, zoals een klant via WhatsApp, een bestelling in je privé-inbox of een [belofte](promises.md) over werk, is vanaf het begin Werk.

Een to-do die je zelf hebt verplaatst of geplaatst, blijft altijd staan waar je hem hebt neergezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, niet waar hij op antwoordt. Een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij wordt nooit weergegeven in een Werk-Fleet of de Team-Graph.

Als er twee of meer to-do's op je wachten, doorloop je ze met **Doorlopen** bovenaan Voor jou, één voor één en in de volgorde van de lijst. Je ziet elk concept volledig, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stopt Esc. Bovenaan staat hoelang het ongeveer duurt, op jouw tempo, bijvoorbeeld ‘ongeveer 2 min’.

Aan het einde zie je hoeveel items zijn verstuurd of gesloten en hoeveel er nog worden klaargezet.

Een to-do met een vraag voor jou wordt niet meegenomen: die vraagt om je antwoord, niet om een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert wat is binnengekomen zodra er 40 berichten wachten of zodra het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden meegenomen bij de volgende controle, binnen een uur.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog steeds gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan vóór je ochtendoverzicht. Bij Controles onder Koppelingen staat ‘'s Nachts gepauzeerd, wordt om 06:30 bijgewerkt’. Als je 's nachts in de app klikt, typt of scrolt, in de chat schrijft of op een to-do tikt, worden controles weer uitgevoerd zoals gewoonlijk, totdat je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** worden alle bronnen meteen gelezen. Als er geen to-do's openstaan, tik je op de regel van je Machine om hem te bekijken, met **Details** om Controles onder Koppelingen te openen. Als er wel to-do's openstaan, staat de regel bovenaan op een computer. Je ziet er alleen kort iets zolang een controle bezig is of als die is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's wat er is gevonden, van elke gelezen bron, bijvoorbeeld ‘13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's’ of ‘· 2 nieuwe to-do's’. Dit gaat alleen over die controle. To-do's die al op je lijst staan, blijven staan zoals ze zijn. Als een nieuwe to-do op een beter moment wacht, zoals je ochtendoverzicht, staat erbij tot wanneer: ‘1 to-do uitgesteld tot morgen 08:30’.

Tik op de regel om elke e-mailthread, chat en melding te bekijken, met het pictogram van de bron, wie het bericht heeft geschreven, het onderwerp of de eerste woorden en de bijbehorende nieuwe to-do of de reden waarom er niets nodig was. Bijvoorbeeld: ‘Alleen in cc, een teamgenoot antwoordt’ of ‘Afspraak al gepland voor donderdag’. Bij een thread staat geen reden als de controle alleen een algemene reden opleverde. Tik erop om het bericht en de bijbehorende gesprekken te lezen.

De eerste 10 worden getoond. Tik eronder om de rest te bekijken. Een getal na een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat bevat. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails die The Machine zelf naar je stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt zoals gewoonlijk gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Bekijk [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan of, zodra er een concept klaarstaat, wat er in het concept moet veranderen. **Als gedaan markeren** betekent dat het is afgehandeld. Bij een klaargezette to-do zonder concept of een to-do met een vraag voor jou staat deze knop in beeld. Anders staat hij bovenaan onder **…**. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in de melding. Veeg de melding weg of sleep hem met de muis van het scherm om hem sneller te sluiten. De wijziging blijft staan.

Wil je het op een andere manier laten doen, zeg dat dan in de **Chat**. In het antwoord staat alleen wat er is veranderd, bijvoorbeeld een snooze en tot wanneer. Als iets niet kon worden gewijzigd, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: draag de to-do over aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md) of [vraag iemand om een beoordeling](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt het ook in de chat vragen, bijvoorbeeld ‘Hernoem naar …’. De titel blijft staan.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de ander, maar niet na je eigen antwoord. Daarna staat erbij wanneer hij is teruggekomen en wordt hij als nieuw gesorteerd. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betalingsgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen kaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld doordat de afzender bevestigt dat de betaling is binnengekomen, wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem een dag terug.

Een to-do die alleen tot een bepaald tijdstip van belang was, zoals een bevestiging vóór een meeting, wordt na dat tijdstip vanzelf gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet meer nodig’. Met **Ongedaan maken** zet je hem een dag terug.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij totdat Slack ze heeft gelezen. Als een later bericht laat zien dat het al is geregeld, bijvoorbeeld omdat iemand is gevraagd en ja heeft gezegd, wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem een dag terug.

Als iemand anders iets in hetzelfde gesprek heeft geschreven nadat je concept is gemaakt, houdt **Versturen** het tegen: ‘Niet verstuurd: nieuw bericht in de thread’. Bij de to-do staat dat bericht, met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan verandert, bijvoorbeeld doordat een feest naar een andere locatie verhuist of een boeking vervalt, past The Machine zijn to-do's zelf aan. Een to-do die nog nodig is, volgt het nieuwe plan. Een to-do waarvoor niets meer hoeft te gebeuren, wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet nodig’. In de chat staat ‘Bijgewerkt:’ met de reden. Met **Ongedaan maken** zet je hem een dag terug.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**, en de uitleg dat er niets wordt verstuurd totdat je op **Versturen** drukt. Een tip verdwijnt definitief zodra je de bijbehorende knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en staat er wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat zodra je er bent.

Elke to-do begint met de titel. Op de regel eronder staat op wie hij betrekking heeft, de organisatie als het over een organisatie gaat (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer het bericht is binnengekomen. Tik op een naam om de pagina van die persoon in Graph te openen.

Bij een naam en organisatie staat een foto of logo als Graph die heeft, en anders de initialen. Als een logo op dat formaat niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, worden ook de initialen weergegeven.

Soms staat er een rustige melding met informatie die ontbreekt, zoals ‘Laatste contact 12 dagen geleden via e-mail; sindsdien niets’. Die verschijnt als het laatste contact met iemand oud is of nog geen antwoord heeft gekregen. Er staat ook bij welke kanalen niet zijn gekoppeld, zoals WhatsApp. Je Machine geeft aan wat hij niet weet in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

Een titel zegt wat er moet gebeuren en verandert alleen als dat ook verandert. Een afgeronde to-do behoudt zijn titel, met eronder hoe hij is afgerond, bijvoorbeeld ‘Gedaan: Sam heeft dinsdag getekend’.

Boven het concept staat op een lichte regel uit welk bericht het afkomstig is, met het logo van die dienst. Tik erop om de thread te lezen. Bij het concept staat het logo van de bestemming, zodat je meteen ziet of het om een antwoord in Slack of een e-mail gaat.

Als het concept is gebaseerd op iets wat iemand anders ergens anders heeft gezegd, zoals een suggestie van een teamgenoot in Slack, staat dat op een regel, bijvoorbeeld ‘Gebaseerd op Sam in #ops’. Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten van vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan jouw berichten rechts, net als in de app. Bij het bericht waar de to-do over gaat, staat ‘Deze to-do’ en het bericht wordt geopend in beeld. Met **Eerdere berichten tonen** worden oudere berichten toegevoegd. Bij een e-mail wordt de rest van de thread ingeklapt erboven en eronder weergegeven.

Een bericht wordt op dezelfde manier geopend vanuit Zoeken, Graph, de antwoorden van Ask of de laatste controle. Het bericht is gemarkeerd als ‘Dit bericht’ of ‘Nieuwe berichten’.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android wordt de Gmail-app geopend als je die hebt.

Bij een e-mail tonen **Details** alleen wat niet in de kop staat, zoals volledige cc-adressen, bcc of een ander antwoordadres. Als er niets toe te voegen is, worden er geen details getoond.

Bij een antwoord in een Slack-thread wordt ook getoond wat er is gezegd voordat de thread begon. Met de link van een to-do naar het bijbehorende bericht open je het hier ook, met **Openen in Slack** onderaan.

Bij **Details** staan de naam, het project en het gebied van de to-do (tik erop om het te wijzigen), je laatste notitie en het resultaat van een codeeragent. De titel opent de chat. Een afgeronde to-do blijft kort; het bericht waar hij vandaan komt, staat onder **Details**.

Bij een to-do met ‘Wacht op’ staat een link naar je laatste bericht aan de ander, het bericht waarop je wacht: ‘E-mail aan Pat · di’.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je voor alles een to-do toe. Als je er een maakt, wordt er niets verstuurd. Als je **Werk** of **Privé** niet kiest, komt de to-do terecht waar hij hoort op basis van wie en wat het betreft. Hij vindt ook de e-mail waarop hij een vervolg is, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals ‘morgen’, ‘volgende vr’, ‘3 nov’, ‘14:00’ of ‘over 2 uur’. Dat kan ook in je eigen taal. Met het kalendericoon zie je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Bekijk [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waarop de to-do betrekking heeft, maximaal 5.
- Berichticoon: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp-, Telegram- of ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft gestuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een schermafbeelding of sleep bestanden naar het formulier. Op een telefoon maakt de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (bekijk [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij ermee aan de slag gaat. Alleen bestanden zijn al genoeg: de to-do wordt ingevuld op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te bekijken.
