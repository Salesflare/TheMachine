---
title: To-do's
area: cards
summary: Eén to-do voor alles waarvoor je iets moet doen, klaar om door jou goedgekeurd te worden. Dit betekenen de verschillende onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e0fd02e557e6daee
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als er iets van je nodig is. Eén to-do per onderwerp, hoeveel berichten het ook beslaat.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een probleem, dat is afgehandeld terwijl je weg was. Hij blijft er maximaal een dag staan, tot je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar, en **Doe het** of **Versturen** voert het uit), **Wacht op jou** (eerst is je beslissing of antwoord nodig; als het werk vastloopt op iets wat alleen jij weet, zoals een feit, login of keuze, staat er een regel onder de titel met wat er nodig is), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of briefing, waarvoor je niets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws mee is gebeurd (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop je **Nog nodig?** niet hebt beantwoord (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het moment waarop ze zijn afgerond, zoals 'Gedaan 5 minuten geleden'. To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Na het versturen staat er kort waar de to-do naartoe is gegaan, bijvoorbeeld 'Verstuurd. Verplaatst naar Gedaan.' of 'Verstuurd. Verplaatst naar Later tot ma.' Een antwoord waarin alleen wordt beloofd dat het werk nog wordt gedaan, zoals 'Ik stuur het dinsdag', laat de to-do open: 'Verstuurd. Open gehouden.' Met **Openen** ga je naar de to-do. Met Zoeken vind je een to-do op titel of op de persoon aan wie hij is gestuurd, ook in Later en Gedaan.

Bij **Voor jou** staan eerst de to-do's waarvan de deadline is verstreken of morgen is, daarna vragen van je Fleet, vervolgens vervolgacties van een bord en daarna de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en wanneer hij klaar is: alleen het label verandert. In de andere open groepen staan eerst de to-do's waarvan de deadline is verstreken of morgen is, daarna de rest, met de nieuwste bovenaan. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat het werk klaar is, bijvoorbeeld 'PR #3451 samengevoegd', maar dat het nog niet is afgesloten. Met **Heropenen** zet je de to-do terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat weergegeven. Als dit in een bericht staat, wordt de to-do na een dag automatisch afgesloten, met **Ongedaan maken** als optie. Anders wacht de to-do op **Als gedaan markeren**. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook automatisch afgesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, vermeldt de to-do dat duidelijk: 'Dit is niet Sam Lee.' De afzender wordt weergegeven met zijn eigen adres, nooit met de naam die hij zelf heeft opgegeven. Je Machine controleert zo'n bericht bij de persoon van wie je het adres al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, bijvoorbeeld op een review of antwoord, staat **Wacht op:** die stap. De to-do staat ingeklapt in **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem terugbrengt. Hetzelfde geldt als jij een vraag hebt teruggesteld: de to-do komt terug op de ochtend voor de deadline, op de deadline als die later vandaag valt, of de volgende ochtend zodra de deadline is verstreken. Er staat dan ook op wie de to-do nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet aanleveren, zoals een ondertekend contract, toont **Details** dit bij **Klaar als**. Je eigen deel versturen sluit de to-do niet af: hij blijft bij **Wacht op anderen** staan tot een bericht het resultaat bevestigt. Daarna wordt de to-do automatisch afgesloten, met **Ongedaan maken** als optie. Als er niets binnenkomt tegen de tijd dat je diegene een herinnering moet sturen, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Een to-do waar een week niets nieuws mee is gebeurd, wordt verplaatst van Voor jou naar **Ouder**, zodat nieuwe to-do's bovenaan staan als je een paar dagen weg bent geweest. Er is niets nieuws gebeurd als er geen nieuw bericht over de to-do is en jij er niets mee hebt gedaan, zoals een chatbericht sturen, een wijziging aanbrengen of snoozen. Alleen ernaar kijken telt niet.

Dringende to-do's, to-do's met een naderende deadline en to-do's waarvoor iets verstuurd zal worden, blijven bij Voor jou. Met **Alles afwijzen** markeer je alle to-do's onder Ouder na één bevestiging als niet nodig, net als met **Niet nodig**, maar dan één voor één. Je kunt dit ongedaan maken met **Ongedaan maken**. Als er iets nieuws gebeurt met een to-do, komt hij terug bij Voor jou.

Bij een to-do waar een week niemand iets mee heeft gedaan, verschijnt één keer de vraag **Nog nodig?** Met **Niet nodig** sluit je hem af. Je kunt dit ongedaan maken met **Ongedaan maken**. Met **Houden** bewaar je de to-do en wordt de vraag niet opnieuw gesteld. Als je nog een week niet antwoordt, wordt de to-do ingeklapt onder Komt later terug. Het aantal op het appicoon en in het ochtendoverzicht telt hem dan niet meer mee. De to-do komt terug als je hem opent, een chatbericht stuurt, iets wijzigt, hem snoozet of als er een nieuw bericht binnenkomt.

Eén keer per week kan een project waar niets meer gebeurt en geen open to-do's heeft, een to-do met een concrete volgende stap krijgen. Dit gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als je niets hoeft te doen, dut je Machine op een lege lijst. Tijdens een controle wordt hij weer wakker en laat hij dat weten. Als een controle is mislukt of vertraging heeft, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen één soort. Op je telefoon en computer staat dezelfde keuze. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, is niet Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook rechtstreeks naar de andere optie: bij **Alleen privé** tik je op **Werk** of **Alles tonen**.

De rij bovenaan de lijst vermeldt je laatste ochtend- of avondoverzicht en wat daarin is meegeteld, bijvoorbeeld **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen. Met **Kopiëren** kun je het overal plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, zie je **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de optie die je hebt geselecteerd.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Zie [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten die hij mag lezen en versturen, verhuist mee. Met **Ongedaan maken** bij de melding zet je hem terug.

Als een to-do verder moet in je andere gebied en alle bijbehorende berichten daar staan, wordt hij automatisch daarheen verplaatst en gaat hij verder. Anders staat er **Naar Werk verplaatsen** en wordt er niets verplaatst tot je erop tikt. Een to-do die je toevoegt zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd is hij niet gemarkeerd als Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij uit is voortgekomen. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gemarkeerd, telt als Privé. Mail voor een ander bedrijf van jou hoort bij de to-do's van dat bedrijf. Een to-do over je privéleven, zoals familie die naar je werkadres mailt, is vanaf het begin Privé.

Werk dat je via een persoonlijk account bereikt, zoals een klant op WhatsApp of een bestelling in je persoonlijke mailbox, is vanaf het begin Werk. Een to-do die je zelf hebt verplaatst of aangemaakt, blijft altijd op de plek die je hebt gekozen. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, nooit waar hij op antwoordt: een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij wordt nooit weergegeven in een Werk-Fleet of de Team-Graph.

Als er twee of meer to-do's op je wachten, doorloopt **Doorlopen** in de kop van Voor jou ze één voor één, in de volgorde van de lijst. Je ziet elk volledig concept, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat er op het scherm staat, snoozet `S`, slaat `→` over en stopt Esc. In de kop staat hoelang het duurt op jouw tempo, bijvoorbeeld 'ongeveer 2 min'.

Aan het einde zie je hoeveel to-do's zijn verstuurd of afgesloten en hoeveel er nog worden voorbereid.

Een to-do die je iets vraagt, wordt niet meegenomen: daarvoor is je antwoord nodig, geen tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert binnengekomen berichten zodra er 40 berichten wachten of het oudste bericht van iemand al 15 minuten wacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden bij de volgende controle meegenomen, uiterlijk binnen een uur.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog wel gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan voor je ochtendoverzicht. Bij Controles onder Koppelingen staat 'Nachtpauze, haalt de achterstand om 06:30 in'. Als je 's nachts in de app klikt, typt of scrolt, in de chat schrijft of op een to-do tikt, worden controles zoals gewoonlijk uitgevoerd tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** worden alle bronnen meteen gelezen. Als er geen open to-do's zijn, tik je op de regel van je Machine om die te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er open to-do's zijn, staat de regel bovenaan op een computer. Je ziet hem daar alleen kort tijdens een controle, of als een controle is mislukt of vertraging heeft. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare volgen hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met wat er is gevonden, van elke gelezen bron. Bijvoorbeeld: '13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's' of '· 2 nieuwe to-do's'. De regel gaat alleen over die controle: to-do's die al op je lijst staan, blijven gewoon staan. Als een nieuwe to-do tot een geschikter moment wordt uitgesteld, zoals je ochtendoverzicht, staat erbij tot wanneer: '1 to-do uitgesteld tot morgen 08:30'.

Tik op de regel om elke e-mailthread, chat en melding te bekijken, met het pictogram van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden en de nieuwe to-do, of waarom er niets nodig was, zoals 'Alleen in cc, een teamgenoot antwoordt' of 'Afspraak staat al voor donderdag'. Bij een thread staat geen reden als de controle alleen een vage reden opleverde. Tik erop om het bericht te lezen, met de berichten eromheen.

De eerste 10 worden weergegeven. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, verschijnt maar één keer. De regel blijft 12 uur na de controle zichtbaar.

Alleen e-mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails van The Machine aan jou, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe je het moet doen, of, zodra er een concept klaarstaat, wat daarin moet veranderen. **Als gedaan markeren** betekent dat het is afgehandeld. Bij een klaargezette to-do zonder concept of een to-do die je iets vraagt, staat deze optie in het zicht. Anders staat hij bovenaan onder **…**. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in het bericht. Veeg het bericht weg of sleep het met de muis weg om het sneller te sluiten. De wijziging blijft behouden.

Wil je het op een andere manier laten doen, laat het weten in de **Chat**. In het antwoord staat alleen wat er is veranderd, bijvoorbeeld een snooze en tot wanneer. Als iets niet kon worden veranderd, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: geef het aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om een review](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt dit ook in de chat vragen, bijvoorbeeld: 'Hernoem dit naar …'. De titel die je kiest, blijft staan.

Met **Heropenen** zet je een afgesloten to-do terug. Hij komt ook automatisch terug als er iets nieuws gebeurt, zoals een nieuw bericht van die persoon, maar niet na je eigen antwoord. De to-do vermeldt dan wanneer hij is teruggekomen en staat als nieuw bovenaan. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betalingsgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen betaalkaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender dat je betaling is ontvangen, wordt de to-do automatisch afgesloten. Je kunt hem een dag lang terughalen met **Ongedaan maken**.

Een to-do die maar tot een bepaald moment relevant was, zoals een bevestiging vóór een meeting, wordt na dat moment automatisch afgesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** als 'Niet meer nodig'. Je kunt hem een dag lang terughalen met **Ongedaan maken**.

Voordat een bericht of overdracht voor iemand als klaargezet wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat het al is afgehandeld, bijvoorbeeld omdat iemand het heeft gevraagd en een bevestigend antwoord heeft gekregen, wordt de to-do automatisch afgesloten. Je kunt hem een dag lang terughalen met **Ongedaan maken**.

Als iemand anders iets in hetzelfde gesprek heeft geschreven nadat je concept is gemaakt, houdt **Versturen** het tegen: 'Niet verstuurd: nieuw bericht in de thread'. Bij de to-do staat dat bericht met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een reservering is geannuleerd, werkt The Machine de to-do's zelf bij. Een to-do die nog relevant is, volgt het nieuwe plan. Een to-do waarvoor niets meer hoeft te gebeuren, wordt verplaatst naar **Gedaan / afgewezen** als 'Niet nodig'. In de chat staat 'Bijgewerkt:' met de reden. Je kunt hem een dag lang terughalen met **Ongedaan maken**.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste opties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd tot je op **Versturen** drukt. De tip verdwijnt voorgoed zodra je op de knop tikt of op × drukt.

Op je eerste dag begroet de bovenkant van To-do's je en staat erbij wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat als je begint.

Elke to-do begint met de titel. De regel eronder vermeldt op wie de to-do betrekking heeft, de organisatie als die relevant is (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie staat de foto of het logo als de Graph die heeft, en anders de initialen. Als een logo op dat formaat niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, wordt ook de initiaal weergegeven.

Soms staat er een ingetogen regel met informatie die niet bekend is, zoals 'Laatste contact 12 dagen geleden via e-mail; sindsdien niets.' Die verschijnt als het laatste contact met die persoon lang geleden was of onbeantwoord bleef. Ook kan er een kanaal bij staan dat niet is gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van het te raden.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

De titel zegt wat er moet gebeuren en verandert alleen als dat verandert. De titel van een afgeronde to-do blijft staan, met eronder hoe die is afgerond, zoals 'Gedaan: Sam heeft het dinsdag ondertekend'.

Boven het concept staat een subtiele regel met het bericht waar het uit voortkomt en het logo van de bijbehorende dienst. Tik erop om de thread te lezen. Bij het concept staat het logo van de bestemming, zodat je meteen ziet of het een Slack-antwoord of een e-mail is.

Als het concept voortkomt uit iemands input op een andere plek, zoals een suggestie van een teamgenoot in Slack, staat dat erbij, bijvoorbeeld 'Gebaseerd op Sam in #ops'. Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Bij het bericht van de to-do staat 'Deze to-do' en het wordt geopend weergegeven. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mailthread staan de overige berichten ingeklapt erboven en eronder.

Een bericht wordt op dezelfde manier geopend vanuit Zoeken, de Graph, antwoorden van Ask of de laatste controle. Het is gemarkeerd als 'Dit bericht' of 'Nieuwe berichten'.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is ontvangen. Op Android wordt hij geopend in de Gmail-app als je die hebt.

Onder **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige cc-adressen, bcc of een ander antwoordadres. Als er niets aan toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread staat ook wat er is gezegd voordat de thread begon. Met de link van een to-do naar het bijbehorende bericht open je dat hier ook, met **Openen in Slack** onderaan.

Onder **Details** staan de naam, het project en het gebied (tik op een ervan om die te wijzigen), je laatste notitie en het resultaat van een codeeragent. De titel opent de chat. Een afgeronde to-do blijft kort; het bericht waar hij uit voortkomt staat onder **Details**.

Een to-do met 'Wacht op' linkt naar je laatste bericht aan die persoon, waarop je wacht: 'E-mail aan Pat · di'.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) maak je voor alles een to-do. Als je er een maakt, wordt er niets verstuurd. Als je geen **Werk** of **Privé** kiest, komt de to-do terecht waar hij thuishoort, afhankelijk van de persoon en het onderwerp. Hij zoekt ook de e-mail op waarop de to-do een vervolg is, zelfs als die al ouder is.

- **Deadline**: typ een dag of tijd, zoals 'morgen', 'volgende vr', '3 nov', '14:00' of 'over 2 uur'. Dat kan ook in je eigen taal. Het kalendericoon bevat snelkeuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waarop de to-do betrekking heeft, maximaal 5.
- Berichticoon: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp-, Telegram- of ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat van welke bron het komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en je Machine leest ze wanneer hij eraan werkt. Alleen bestanden zijn genoeg: hij vult de to-do in aan de hand van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te bekijken.
