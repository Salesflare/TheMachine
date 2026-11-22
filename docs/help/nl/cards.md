---
title: To-do's
area: cards
summary: Eén to-do per zaak die je aandacht nodig heeft, klaar om door jou goedgekeurd te worden. Lees wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fef065570d3fd972
---
Je Machine leest alle nieuwe berichten en maakt alleen een to-do als iets je aandacht nodig heeft. Eén to-do per zaak, ook als die over meerdere berichten gaat.

## Waar to-do's staan

Op de pagina **To-do's** staan ze in groepen:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een probleem dat is afgehandeld terwijl je weg was. Deze blijft maximaal een dag staan, totdat je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles waar jij iets mee moet, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (een concept of resultaat staat klaar en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (eerst is je beslissing of antwoord nodig; als het werk vastloopt op iets wat alleen jij kunt aanleveren, zoals een feit, een login of een keuze, staat er onder de titel wat er nodig is), **Aan het voorbereiden…** (je Machine werkt eraan) of **Om te lezen** (een overzicht of korte briefing, zonder dat je iets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws mee is gebeurd (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop geen antwoord is gekomen op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij anderen hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, bijvoorbeeld '5 minuten geleden gedaan'. To-do's die al afgerond lijken, hebben het label **Lijkt gedaan**.

Na het versturen staat er kort waar de to-do naartoe is gegaan, bijvoorbeeld 'Verstuurd. Verplaatst naar Gedaan.' of 'Verstuurd. Verplaatst naar Later tot ma.' Een antwoord waarin alleen werk wordt beloofd, zoals 'Ik stuur het dinsdag', laat de to-do openstaan: 'Verstuurd. Opengehouden.' Met **Openen** ga je naar de to-do. Zoeken vindt to-do's op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's die over tijd zijn of uiterlijk morgen af moeten zijn, dan vragen van je Fleet, daarna vervolgacties van een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine eraan werkt en wanneer hij klaar is. Alleen de markering verandert. In de andere open groepen staan to-do's die over tijd zijn of uiterlijk morgen af moeten zijn bovenaan, gevolgd door de rest, met de nieuwste eerst. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets klaar is, zoals 'PR #3451 samengevoegd', maar dat de to-do nog niet is gesloten. Met **Heropenen** zet je hem terug op je lijst. Je Machine leert hiervan. Deze to-do's worden nooit als te laat weergegeven. Als een bericht laat zien dat de taak is afgerond, wordt de to-do na een dag automatisch gesloten, met **Ongedaan maken**. Anders wacht hij op **Als gedaan markeren**. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook automatisch gesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: 'Dit is Sam Lee niet.' De afzender wordt weergegeven met zijn eigen adres, nooit met de naam die hij heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, staat **Wacht op:** gevolgd door die stap. De to-do staat ingeklapt in **Wacht op anderen**, boven Komt later terug, totdat een nieuw bericht hem weer opent. Hetzelfde geldt nadat je zelf een vraag hebt teruggestuurd: de to-do komt terug op de ochtend vóór de deadline, op de deadline als die later op die dag valt, of de volgende ochtend als die al voorbij is. Er staat dan op wie hij nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet aanleveren, zoals een ondertekend contract, zie je dat onder **Details** bij **Klaar als**. Alleen jouw deel versturen sluit de to-do niet af. Hij blijft bij **Wacht op anderen** staan totdat een bericht laat zien dat het resultaat er is. Daarna wordt hij automatisch gesloten, met **Ongedaan maken**. Als het tijd is om erachteraan te gaan en er nog niets is binnengekomen, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Een to-do waar een week niets nieuws mee is gebeurd, wordt verplaatst van Voor jou naar **Ouder**. Zo staan nieuwe to-do's bovenaan als je na een paar dagen terugkomt. Er is niets nieuws gebeurd als er geen nieuw bericht over de to-do is en jij er ook niets mee hebt gedaan, zoals een chatbericht sturen, iets bewerken of snoozen. Alleen ernaar kijken telt niet.

Dringende to-do's, to-do's die bijna moeten worden afgerond en to-do's met een bericht dat onderweg is, blijven bij Voor jou staan. Met **Alles afwijzen** markeer je alle to-do's onder Ouder na één bevestiging als niet nodig, net zoals je dat per to-do doet met **Niet nodig**. Je kunt dit ongedaan maken met **Ongedaan maken**. Als er iets nieuws gebeurt met een to-do, komt hij terug bij Voor jou.

Een to-do waar een week niemand iets mee heeft gedaan, vraagt één keer: **Nog nodig?** Met **Niet nodig** sluit je hem. Je kunt dat ongedaan maken met **Ongedaan maken**. Met **Houden** blijft de to-do staan en wordt dit nooit meer gevraagd. Komt er nog een week geen antwoord, dan wordt hij ingeklapt onder Komt later terug. Hij telt dan niet meer mee op het appicoon en in het ochtendoverzicht. Als je hem opent, een chatbericht stuurt, iets bewerkt of snoozet, of als er een nieuw bericht binnenkomt, komt hij weer terug.

Eén keer per week kan een project dat stil is gevallen en geen openstaande to-do's heeft, een to-do krijgen met één specifieke volgende stap. Dat gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als er niets is dat je aandacht nodig heeft, doet je Machine een dutje en blijft de lijst leeg. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk geef je alle to-do's weer of alleen to-do's van één soort. Op je telefoon en computer wordt dezelfde keuze gebruikt. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, bijvoorbeeld over een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook rechtstreeks naar de andere optie. Tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst toont de naam van je laatste ochtend- of avondoverzicht en wat erin stond, bijvoorbeeld **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen. Met **Kopiëren** kun je het ergens plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Zonder recent overzicht staat er **Vandaag tot nu toe**: wat vandaag is afgerond en wat nog openstaat, voor Werk en Privé of alleen voor de optie die je hebt geselecteerd.

Bij een to-do voor een project staat de naam van het project onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of verwijder je de koppeling. Zie [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten die hij mag lezen en versturen verhuist mee. Met **Ongedaan maken** bij de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waarop hij is gebaseerd daar staan, wordt hij automatisch verplaatst en gaat hij verder. Anders zie je **Naar Werk verplaatsen** en wordt er niets verplaatst totdat je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waarop hij is gebaseerd. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gemarkeerd, telt als Privé. Mail voor een ander bedrijf van je gaat naar de to-do's van dat bedrijf. Een to-do over je privéleven, zoals familie die naar je werkadres mailt, is vanaf het begin Privé.

Werk dat je via een privéaccount bereikt, zoals een klant op WhatsApp of een bestelling in je privé-inbox, is vanaf het begin Werk. Een to-do die je zelf hebt verplaatst of ingedeeld, blijft altijd staan waar jij hem hebt neergezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, maar niet waarvandaan hij antwoordt. Een antwoord gaat altijd naar de plek waar het gesprek plaatsvindt, ook na een verplaatsing, tenzij je een andere optie kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij verschijnt nooit in een Werk-Fleet of Team-Graph.

Als er twee of meer to-do's op je wachten, loop je er met **Doorlopen** bovenaan Voor jou één voor één doorheen, in de volgorde van de lijst. Je ziet elk volledig concept, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuur je met Enter wat op het scherm staat, snooze je met `S`, sla je over met `→` en stop je met Esc. In de kop staat hoelang het op jouw tempo duurt, bijvoorbeeld 'ongeveer 2 min'.

Aan het einde zie je hoeveel to-do's zijn verstuurd of gesloten en hoeveel er nog worden voorbereid.

Een to-do die je iets vraagt, wordt niet meegenomen. Daarvoor is je antwoord nodig, niet een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert nieuwe berichten zodra er 40 zijn binnengekomen of zodra het oudste bericht van een persoon 15 minuten oud is. Nieuwsbrieven, meldingen en ontvangstbewijzen gaan mee bij de volgende controle, binnen een uur.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog steeds gelezen en bewaard, en om 06:30 in één keer gecontroleerd, zodat je to-do's klaarstaan voordat je ochtendoverzicht verschijnt. Bij Controles onder Koppelingen staat 'Nachtpauze, wordt om 06:30 bijgewerkt'. Als je 's nachts in de app klikt, typt of scrolt, in de chat schrijft of op een to-do tikt, gaan controles weer zoals gewoonlijk door totdat je een uur weg bent geweest. Met **Nu checken** voer je altijd meteen een controle uit.

Met **Nu checken** worden alle bronnen meteen gelezen. Als er geen to-do's openstaan, tik je op de regel van je Machine om hem te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er wel to-do's openstaan, vind je de regel bovenaan op een computer. Een korte melding staat er alleen tijdens een controle, of als een controle is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare volgen hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat boven je to-do's een regel met wat er is gevonden uit alle gelezen bronnen. Bijvoorbeeld: '13 berichten gecontroleerd om 16:11 · niets nodig' of '· 2 nieuwe to-do's'. Als een nieuwe to-do op een beter moment wacht, zoals op je ochtendoverzicht, staat erbij tot wanneer: '1 to-do uitgesteld tot morgen 08:30'.

Tik op de regel om alle e-mailthreads, chats en meldingen te zien, met het pictogram van de bron erbij. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden, en de nieuwe to-do of de reden waarom er niets nodig was, bijvoorbeeld 'Alleen in cc, een teamgenoot antwoordt' of 'Meeting staat al voor donderdag gepland'. Bij een thread wordt geen reden getoond als de controle alleen een vage reden opleverde. Tik op een bericht om het te lezen.

De eerste 10 worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen e-mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails van The Machine zelf aan jou, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of getoond. Mail over facturering, je proefperiode of een uitnodiging wordt wel gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: de manier waarop iets wordt gedaan, of, zodra een concept klaarstaat, wat er in het concept moet veranderen. **Als gedaan markeren** betekent dat de to-do is afgehandeld. Bij een klaargezette to-do zonder concept staat deze optie direct in beeld. Anders vind je hem bovenaan onder **…**, ook bij een to-do waarvoor je nog een beslissing moet nemen. De to-do verdwijnt meteen uit de lijst, met **Ongedaan maken** in het bericht. Veeg het bericht weg of sleep het met de muis weg om het eerder te sluiten. De wijziging blijft behouden.

Wil je dat iets op een andere manier wordt gedaan, zeg dat dan in de **Chat**. Het antwoord vermeldt alleen wat er is veranderd, zoals een snooze en tot wanneer. Als iets niet kon worden aangepast, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om een beoordeling](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt aangeven waarom: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert hiervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt dit ook in de chat vragen, bijvoorbeeld: 'Hernoem dit naar …'. De titel die je kiest, blijft staan.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de ander, maar niet na je eigen antwoord. Je ziet dan wanneer hij is teruggekomen en hij wordt behandeld als nieuw. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via een automatische incasso of een opgeslagen kaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender, wordt de to-do automatisch gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Een to-do die alleen tot een bepaald tijdstip relevant was, zoals een bevestiging vóór een meeting, wordt na dat tijdstip automatisch gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding 'Niet meer nodig'. Met **Ongedaan maken** zet je hem een dag lang terug.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack die heeft gelezen. Als een later bericht laat zien dat iets al is geregeld, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do automatisch gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Als iemand anders in hetzelfde gesprek heeft geschreven nadat het concept is gemaakt, houdt **Versturen** het tegen: 'Niet verstuurd: nieuw bericht in de thread'. Bij de to-do staat dat bericht met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een reservering is vervallen, werkt The Machine de to-do's zelf bij. Een to-do die nog relevant is, volgt het nieuwe plan. Als er niets meer te doen is, wordt de to-do verplaatst naar **Gedaan / afgewezen** met de melding 'Niet nodig'. In de chat staat 'Bijgewerkt:' met de reden. Met **Ongedaan maken** zet je hem een dag lang terug.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd totdat je op **Versturen** drukt. De tip verdwijnt voorgoed zodra je de knop gebruikt of op × drukt.

Op je eerste dag verwelkomt de bovenkant van To-do's je en wordt verteld wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat als je binnenkomt.

Elke to-do begint met de titel. De regel eronder vermeldt over wie de to-do gaat, de organisatie als die relevant is, het project, Werk of Privé en wanneer het bericht is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie wordt een foto of logo getoond als die in de Graph staat. Anders worden de initialen weergegeven. Als een logo op dit formaat niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, wordt ook de eerste letter getoond.

Soms staat er een korte, gedempte regel met wat niet bekend is, zoals 'Laatste contact 12 dagen geleden via e-mail; sindsdien niets'. Die wordt getoond als het laatste contact met iemand lang geleden was of onbeantwoord is gebleven, en vermeldt kanalen die niet gekoppeld zijn, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van iets te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

Een titel vermeldt wat er moet gebeuren en verandert alleen als dat ook verandert. Een afgeronde to-do behoudt zijn titel, met daaronder hoe hij is afgerond, bijvoorbeeld 'Gedaan: Sam heeft het dinsdag ondertekend'.

Boven het concept staat een vage regel met het bericht waarop het is gebaseerd, met het logo van die dienst erbij. Tik erop om de thread te lezen. Het concept toont het logo van de bestemming, zodat je meteen ziet of het om een Slack-antwoord of e-mail gaat.

Als het concept is gebaseerd op iemands input elders, zoals een suggestie van een teamgenoot in Slack, staat dat erbij, bijvoorbeeld 'Gebaseerd op Sam in #ops'. Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt als één gesprek weergegeven, van oud naar nieuw: de berichten vóór het bericht waarop de to-do betrekking heeft en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Het bericht waarop de to-do betrekking heeft, is gemarkeerd met 'Deze to-do' en staat open. Met **Eerdere berichten tonen** voeg je oudere berichten toe. In een e-mailthread zijn de overige berichten erboven en eronder ingeklapt.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop die is binnengekomen. Op Android wordt de Gmail-app geopend als je die hebt.

Bij **Details** van een e-mail staat alleen informatie die niet al in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets toe te voegen is, wordt er niets weergegeven.

Bij een antwoord in een Slack-thread zie je ook wat er vóór het begin van de thread is gezegd. Met de link van een to-do naar het bijbehorende bericht open je het bericht hier ook. Onderaan staat **Openen in Slack**.

Onder **Details** staan de naam, het project en het gebied (tik erop om iets te wijzigen), je laatste notitie en het resultaat van een programmeeragent. Met de titel open je de chat. Een afgeronde to-do blijft beknopt. Het bericht waarop hij is gebaseerd, staat onder **Details**.

Bij een to-do met 'Wacht op' staat een link naar je laatste bericht aan de ander, waarop je wacht, bijvoorbeeld: 'E-mail aan Pat · di'.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) maak je een to-do voor wat je maar wilt. Als je een to-do maakt, wordt er niets verstuurd. Als je niet **Werk** of **Privé** hebt gekozen, komt hij terecht waar hij hoort, op basis van wie en waarover hij gaat. De to-do vindt ook de e-mail waar hij op volgt, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals 'morgen', 'volgende vr', '3 nov', '14:00' of 'over 2 uur'. Dat kan ook in je eigen taal. Met het kalenderpictogram zie je snelle opties en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waarop de to-do betrekking heeft, maximaal 5.
- Berichtenpictogram: voeg het bericht toe waarop de to-do betrekking heeft: een e-mail, Slack-, Teams-, WhatsApp-, Telegram- of ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon maak je met de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij eraan werkt. Je kunt ook alleen bestanden toevoegen. The Machine vult de to-do dan in op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te bekijken.
