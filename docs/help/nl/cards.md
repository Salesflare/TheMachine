---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak die je aandacht nodig heeft, klaar om door jou goedgekeurd te worden. Lees wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fcb9a016c9af8551
---
Je Machine leest alle nieuwe berichten en maakt alleen een to-do als iets je aandacht nodig heeft. Eén to-do per zaak, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze in groepen:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een probleem dat is opgelost terwijl je weg was. Hij blijft er maximaal een dag staan, tot je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met wat uiterlijk morgen moet gebeuren bovenaan. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar en **Doe het** of **Versturen** voert het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven; als het werk niet verder kan of niet gebruikt kan worden zonder iets wat alleen jij weet, zoals een prijs, feit of keuze, staat er onder de titel wat dat is), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of korte samenvatting, zonder dat je iets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws mee is gebeurd (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij iemand anders aan zet is (zie hieronder).
- **Komt later terug**: gesnoozede to-do's, berichten die [later worden verstuurd](send-later.md) en to-do's waarop geen antwoord kwam op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, zoals ‘Gedaan 5 minuten geleden’. To-do's die al afgerond lijken, krijgen het label **Lijkt gedaan**.

Na het versturen staat er kort waar de to-do naartoe is gegaan, bijvoorbeeld ‘Verstuurd. Verplaatst naar Gedaan.’ of ‘Verstuurd. Verplaatst naar Later tot ma.’ Als je antwoord alleen belooft dat het werk wordt gedaan, zoals ‘Ik stuur het dinsdag’, blijft de to-do open: ‘Verstuurd. Open gelaten.’ Met **Openen** ga je naar de to-do. Met Zoeken vind je een to-do op titel of op de persoon naar wie hij is verstuurd, ook in Later en Gedaan.

Bij **Voor jou** staan eerst de to-do's waarvan de deadline is verstreken of uiterlijk morgen valt, daarna vragen van je Fleet, vervolgens opvolgingen van een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en wanneer hij is afgerond. Alleen het label verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of uiterlijk morgen valt bovenaan, gevolgd door de rest, met de nieuwste eerst. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets klaar is, zoals ‘PR #3451 samengevoegd’, maar dat de to-do nog niet is gesloten. Met **Heropenen** zet je hem terug op je lijst. Je Machine leert hiervan. Zulke to-do's worden nooit als te laat gemarkeerd. Als een bericht laat zien dat iets klaar is, wordt de to-do na een dag automatisch gesloten. Je kunt dit ongedaan maken met **Ongedaan maken**. Anders blijft hij wachten tot je **Als gedaan markeren** kiest.

Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook automatisch gesloten. Een antwoord waarin staat dat er een bestand is bijgevoegd terwijl dat niet zo is, sluit de to-do niet.

Als een bericht afkomstig is van een adres dat lijkt op dat van iemand die je kent, zoals sam@acme-corp.example terwijl je Sam kent van sam@acmecorp.example, staat dat duidelijk bij de to-do: ‘Dit is niet Sam Lee.’ De afzender wordt weergegeven met het eigen adres, nooit met de naam die diegene heeft opgegeven. Je Machine controleert zo'n bericht bij de persoon van wie je het adres al hebt, nooit bij de afzender.

Bij een to-do waarbij iemand anders aan zet is, bijvoorbeeld voor een beoordeling of antwoord, staat **Wacht op:** met de stap die nog moet gebeuren. De to-do staat ingeklapt in **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem weer naar voren haalt. Hetzelfde geldt nadat je een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline zelf als die later vandaag valt, of de volgende ochtend als de deadline al verstreken is. Er staat bij op wie je nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet leveren, zoals een ondertekend contract, zie je bij **Details** **Klaar als** met dat resultaat. Je eigen deel versturen sluit de to-do niet af. Hij blijft bij **Wacht op anderen** staan tot een bericht laat zien dat het resultaat er is. Daarna wordt hij automatisch gesloten. Je kunt dit ongedaan maken met **Ongedaan maken**. Is er niets binnen tegen de tijd dat je erachteraan moet gaan, dan komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Als er een week niets nieuws met een to-do is gebeurd, gaat hij van Voor jou naar **Ouder**, zodat nieuwe to-do's bovenaan staan als je na een paar dagen terugkomt. Niets nieuws betekent dat er geen nieuw bericht bij is gekomen en dat je zelf ook niets hebt gedaan, zoals een chatbericht sturen, iets bewerken of snoozen. Alleen de to-do bekijken telt niet mee.

Dringende to-do's, to-do's met een naderende deadline en to-do's waarvan iets wordt verstuurd, blijven bij Voor jou staan. Met **Alles afwijzen** markeer je in één keer, na een bevestiging, alle to-do's onder Ouder als niet nodig. Dat kan ook één voor één met **Niet nodig**. Je kunt dit ongedaan maken met **Ongedaan maken**. Als er iets nieuws gebeurt met een to-do, komt hij terug bij Voor jou.

Als een to-do een week onaangeroerd blijft, vraagt hij één keer: **Nog nodig?** Met **Niet nodig** sluit je hem. Je kunt dit ongedaan maken met **Ongedaan maken**. Met **Houden** houd je de to-do en vraagt hij het nooit meer. Als je nog een week niet antwoordt, wordt hij ingeklapt onder Komt later terug en telt hij niet meer mee op het appicoon of in het ochtendoverzicht. Als je hem opent, een chatbericht stuurt, iets bewerkt of snoozet, of als er een nieuw bericht komt, komt hij weer terug.

Een project waar een week niets gebeurt en geen open to-do's heeft, kan één keer per week een to-do krijgen met één concrete volgende stap. Dat gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als er niets is dat je aandacht nodig heeft, doet je Machine een dutje terwijl de lijst leeg blijft. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk kies je of je alle to-do's of alleen één soort wilt zien. Op je telefoon en computer staat dezelfde keuze. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, bijvoorbeeld dat een onderdeel steeds opnieuw opstart, hoort niet bij Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook direct naar de andere weergave. Tik onder **Alleen privé** op **Werk** of **Alles tonen**.

In de balk bovenaan de lijst staat de naam van je laatste ochtend- of avondoverzicht en wat erin is meegeteld, bijvoorbeeld **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om dat overzicht opnieuw te lezen. Met **Kopiëren** plak je het ergens anders. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als je geen recent overzicht hebt, staat er **Vandaag tot nu toe**. Daarin zie je wat er vandaag is afgerond en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt gekozen.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do ervan af. Zie [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De bronnen waaruit hij mag lezen en waaruit hij mag versturen, verhuizen mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waar hij vandaan komt daar staan, wordt hij automatisch daarheen verplaatst en gaat hij verder. Anders staat er **Naar Werk verplaatsen** en wordt er niets verplaatst tot je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra hij weet waar hij thuishoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij je om **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt aangeduid, telt als Privé. Mail voor een ander bedrijf van je komt bij de to-do's van dat bedrijf terecht. Een to-do over je privéleven, zoals familie die naar je werkadres schrijft, is vanaf het begin Privé.

Werk dat je via een privéaccount bereikt, zoals een klant op WhatsApp, een bestelling in je privémailbox of een [belofte](promises.md) over werk, is vanaf het begin Werk.

Een to-do die je zelf hebt verplaatst of aangemaakt, blijft altijd staan waar je hem hebt neergezet. Werk of Privé bepaalt waar een to-do verschijnt en met wie hij wordt gedeeld, nooit waarvandaan hij antwoordt. Een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij verschijnt nooit in een Werk-Fleet of de Team-Graph.

Als er twee of meer to-do's op je wachten, loop je met **Doorlopen** in de kop van Voor jou één voor één door de lijst, in de volgorde waarin ze staan. Je ziet elk volledig concept, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, met `S` snooze je, met `→` sla je over en met Esc stop je. In de kop staat hoelang het ongeveer duurt als je je eigen tempo aanhoudt, bijvoorbeeld ‘ongeveer 2 min’.

Aan het einde zie je hoeveel to-do's zijn verstuurd of gesloten en hoeveel nog worden voorbereid.

Een to-do die je iets vraagt, wordt in geen van beide gevallen meegenomen. Die wacht op je antwoord, niet op een tik.

## Nu checken

Je Machine leest elke paar minuten alle bronnen, dag en nacht. Hij controleert de binnengekomen berichten zodra er 40 berichten wachten of zodra het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden meegenomen bij de volgende controle, uiterlijk binnen een uur.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog wel gelezen en bewaard, maar pas samen gecontroleerd om 06:30. Zo staan je to-do's klaar voordat je ochtendoverzicht verschijnt. Bij Controles onder Koppelingen staat ‘'s Nachts gepauzeerd, bezig met inhalen om 06:30’. Klik, typ of scroll in de app, schrijf in de chat of tik 's nachts op een to-do en de controles gaan weer zoals gewoonlijk door, tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen alle bronnen. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, staat de regel bovenaan op een computer. Hij is alleen kort zichtbaar wanneer er een controle plaatsvindt, mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare hebben hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's wat je Machine heeft gevonden in alle gecontroleerde bronnen, bijvoorbeeld ‘13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's’ of ‘· 2 nieuwe to-do's’. Dit gaat alleen over die controle. To-do's die al op je lijst stonden, blijven gewoon wachten. Als een nieuwe to-do op een beter moment wacht, bijvoorbeeld op je ochtendoverzicht, staat erbij tot wanneer: ‘1 to-do uitgesteld tot morgen 08:30’.

Tik op de regel om alle e-mailthreads, chats en meldingen te zien, met het pictogram van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden en de nieuwe to-do of de reden waarom er niets nodig was, zoals ‘Alleen in cc, een teamgenoot antwoordt’ of ‘Afspraak staat al voor donderdag’. Bij een thread staat geen reden als de controle alleen een vage reden opleverde. Tik op een bericht om het te lezen, samen met de berichten eromheen.

De eerste 10 worden getoond. Tik eronder om de rest te bekijken. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, verschijnt maar één keer. De regel blijft 12 uur na de controle zichtbaar.

Alleen e-mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar gelden niet als nieuwe mail. E-mails van The Machine zelf, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt wel gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe je iets wilt doen of, zodra een concept klaarstaat, wat je eraan wilt aanpassen. **Als gedaan markeren** betekent dat de to-do is afgehandeld. Deze optie staat direct bij een klaargezette to-do zonder concept of bij een to-do die je iets vraagt. In andere gevallen staat hij bovenaan onder **…**. De to-do verdwijnt meteen van de lijst. In het bericht kun je dit ongedaan maken met **Ongedaan maken**. Veeg het bericht weg of sleep het met de muis om het eerder te sluiten. De wijziging blijft staan.

Wil je dat het op een andere manier wordt gedaan, zeg dat dan in de **Chat**. In het antwoord staat alleen wat er is veranderd, zoals een snooze en tot wanneer. Als iets niet kon worden aangepast, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: wijs de to-do toe aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om een beoordeling](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert hiervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt het ook in de chat vragen, bijvoorbeeld ‘Hernoem dit naar …’. De titel blijft staan.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de ander, maar niet na je eigen antwoord. Je ziet dan wanneer hij is teruggekomen en hij wordt behandeld als nieuw. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals een automatische incasso of een opgeslagen kaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender dat de betaling is ontvangen, wordt de to-do automatisch gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Een to-do die maar tot een bepaald tijdstip belangrijk was, zoals een bevestiging vóór een meeting, wordt na dat tijdstip automatisch gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet meer nodig’. Met **Ongedaan maken** zet je hem een dag lang terug.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat iets al is geregeld, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do automatisch gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Als iemand anders in hetzelfde gesprek heeft geschreven nadat je concept is gemaakt, houdt **Versturen** het tegen: ‘Niet verstuurd: nieuw bericht in de thread’. Bij de to-do zie je dat bericht met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan wijzigt, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is vervallen, past The Machine zijn to-do's zelf aan. Een to-do die nog nodig is, volgt het nieuwe plan. Een to-do waarvoor niets meer hoeft te gebeuren, wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet nodig’. In de chat staat ‘Bijgewerkt:’ met de reden. Met **Ongedaan maken** zet je hem een dag lang terug.

Bij je eerste to-do's krijg je een korte tip over de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**. Ook zie je dat er niets wordt verstuurd voordat je op **Versturen** drukt. Een tip verdwijnt definitief zodra je de bijbehorende knop gebruikt of op × drukt.

Op je eerste dag begroet de bovenkant van To-do's je en staat erbij wie al het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat wanneer je aankomt.

Elke to-do begint met de titel. De regel eronder vertelt over wie de to-do gaat, de organisatie als die relevant is, het project, Werk of Privé en wanneer het bericht is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij namen en organisaties staat een foto of logo als die in de Graph beschikbaar is. Anders zie je de initialen. Een logo dat op dat formaat niet goed leesbaar is, zoals witte tekst op een transparante achtergrond of een breed woordmerk, wordt ook vervangen door de initiaal.

Soms staat er een korte regel met wat onbekend is, zoals ‘Laatste contact 12 dagen geleden via e-mail; sindsdien niets’. Die verschijnt als het laatste contact met iemand oud is of nog onbeantwoord blijft. Ook kan er een kanaal bij staan dat niet is gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van iets te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

De titel zegt wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe hij is afgelopen, zoals ‘Gedaan: Sam heeft het dinsdag ondertekend’.

Boven het concept staat een vage regel met het bericht waarop het is gebaseerd en het logo van die dienst. Tik erop om de thread te lezen. Het concept toont het logo van de bestemming, zodat je meteen ziet of het een Slack-antwoord of een e-mail is.

Als het concept is gebaseerd op iemands bijdrage ergens anders, zoals een suggestie van een teamgenoot in Slack, staat dat erbij, bijvoorbeeld ‘Gebaseerd op Sam in #ops’. Tik erop om dat bericht te lezen. Deze regel verdwijnt zodra een update het concept vervangt.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten vóór het bericht waarop de to-do betrekking heeft en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Het bericht waarop de to-do betrekking heeft, is gemarkeerd met ‘Deze to-do’ en wordt geopend in de weergave. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Een e-mailthread is boven en onder het bericht ingeklapt.

Een bericht wordt op dezelfde manier geopend vanuit Zoeken, de Graph, de antwoorden van Ask of de laatste controle, met het label ‘Dit bericht’ of ‘Nieuwe berichten’.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android wordt de Gmail-app geopend als je die hebt.

Bij **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige cc-adressen, bcc of een ander antwoordadres. Als er niets aan toe te voegen is, zijn er geen details.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Met de link bij een to-do open je ook hier het bericht waarop hij betrekking heeft. Onderaan staat **Openen in Slack**.

Bij **Details** staan de naam, het project en het gebied van de to-do. Tik erop om iets aan te passen. Ook zie je je laatste notitie en het resultaat van een codeeragent. Met de titel open je de chat. Een afgeronde to-do blijft kort; het bericht waarop hij is gebaseerd, staat onder **Details**.

Bij een to-do met het label ‘Wacht op’ staat een link naar je laatste bericht aan de persoon op wie je wacht, zoals ‘E-mail aan Pat · di’.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) maak je een to-do voor om het even wat. Als je een to-do maakt, wordt er niets verstuurd. Als je **Werk** of **Privé** niet kiest, komt de to-do terecht waar hij thuishoort, op basis van wie en waarover hij gaat. Je Machine zoekt ook de e-mail erbij waarop de to-do betrekking heeft, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals ‘morgen’, ‘volgende vr’, ‘3 nov’, ‘14.00’ of ‘over 2 uur’. Dat kan ook in je eigen taal. Met het kalenderpictogram zie je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel maximaal 5 personen of bedrijven aan de to-do.
- Berichtenpictogram: voeg het bericht toe waarop de to-do betrekking heeft, zoals een e-mail, Slack-, Teams-, WhatsApp- of Telegram-bericht, of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een schermafbeelding of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Je kunt maximaal 5 bestanden toevoegen, net als in de chat. Zie [Bestanden toevoegen](card-chat.md#add-files). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en je Machine leest ze wanneer hij ermee aan de slag gaat. Alleen bestanden zijn genoeg: hij vult de to-do in aan de hand van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te bekijken.
